import os
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"

import io
from faster_whisper import WhisperModel
import pandas as pd
import subprocess
from .formatter import Formatter, Event
import tensorflow as tf

gpus = tf.config.list_physical_devices('GPU')
if gpus:
    for gpu in gpus:
        tf.config.experimental.set_memory_growth(gpu, True)

import autochord


def get_free_gpus():
    gpu_stats = subprocess.check_output(["nvidia-smi", "--format=csv", "--query-gpu=memory.used,memory.free"], text=True)
    gpu_df = pd.read_csv(io.StringIO(gpu_stats),
                         names=['memory.used', 'memory.free'],
                         skiprows=1)
    gpu_df['memory.free'] = gpu_df['memory.free'].map(lambda x: x.rstrip(' [MiB]')).astype(int)
    idx = gpu_df.nlargest(1, ['memory.free']).index
    return idx[0]

class Backend:
    def __init__(self) -> None:
        self.formatter = Formatter()
        gpu = get_free_gpus()
        self.model = WhisperModel("large", device="cuda", device_index=gpu)

        # Moving encoder and decoder to separate gpus
        # self.model.encoder.to(f"cuda:{gpu1}")
        # self.model.decoder.to(f"cuda:{gpu2}")
        # self.model.decoder.register_forward_pre_hook(lambda _, inputs: tuple([inputs[0].to(f"cuda:{gpu2}"), inputs[1].to(f"cuda:{gpu2}")] + list(inputs[2:])))
        # self.model.decoder.register_forward_hook(lambda _, inputs, outputs: outputs.to(f"cuda:{gpu1}"))

    def query_pdf(self, *, audio: str, add_tabs: bool) -> io.BytesIO:
        ...

    def query_txt(self, *, audio: str) -> io.BytesIO:
        return io.BytesIO(bytes(self.query(audio=audio), 'utf-8'))

    def query(self, *, audio: str, compute_word_timestamps: bool = True) -> str:
        text, _ = self.model.transcribe(audio=audio, word_timestamps=compute_word_timestamps, vad_filter=True)
        chords = autochord.recognize(audio)
        return self.formatter.format(chords, text, use_word_timestamps=compute_word_timestamps)

    def query_quality(self, *, audio: str, compute_word_timestamps: bool = True) -> list[Event]:
        chords = autochord.recognize(audio)
        return self.formatter.parse_raw(chords, [])

    
