import io
import autochord
from .formatter import Formatter


class Backend:
    def __init__(self) -> None:
        self.formatter = Formatter()

    def query_pdf(self, *, audio: str, add_tabs: bool) -> io.BytesIO:
        ...

    def query_txt(self, *, audio: str) -> io.BytesIO:
        return io.BytesIO(bytes(self.query(audio), 'utf-8'))

    def query(self, *, audio: str) -> str:
        chords = autochord.recognize(audio)
        return self.formatter.format(chords)
