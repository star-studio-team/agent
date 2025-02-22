class Writer:
    def __init__(self) -> None:
        self.output: str = ''

    def write(
        self,
        data: str,
        end: str = '',
    ):
        data += end
        self.output += data

