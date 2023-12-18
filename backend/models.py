import io

class Backend:
    def __init__(self) -> None:
        ...

    def query_pdf(self, *, audio: io.BytesIO, add_tabs: bool) -> io.BytesIO:
        ...

    def query_txt(self, *, audio: io.BytesIO) -> io.BytesIO:
        ...