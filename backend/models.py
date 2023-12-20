import io
import autochord
import whisper
from .formatter import Formatter


class Backend:
    def __init__(self) -> None:
        self.formatter = Formatter()
        self.model = whisper.load_model("medium", device="cuda:4")

        self.model.encoder.to("cuda:4")
        self.model.decoder.to("cuda:5")
        self.model.decoder.register_forward_pre_hook(lambda _, inputs: tuple([inputs[0].to("cuda:5"), inputs[1].to("cuda:5")] + list(inputs[2:])))
        self.model.decoder.register_forward_hook(lambda _, inputs, outputs: outputs.to("cuda:4"))

    def query_pdf(self, *, audio: str, add_tabs: bool) -> io.BytesIO:
        ...

    def query_txt(self, *, audio: str) -> io.BytesIO:
        ...

    def query(self, *, audio: str) -> str:
        text = self.model.transcribe(audio=audio)
        chords = autochord.recognize(audio)
        return self.formatter.format(chords, text)
