class CodeGen:
    pass


class ScratchBuffer:
    body: str
    indent: int

    def __init__(self, indent: int = 0):
        self.body = ""
        self.indent = indent

    def writeln(self, line: str):
        self.body += " " * self.indent * 4 + line + "\n"

    def write(self, line: str):
        self.body += " " * self.indent * 4 + line

    def __str__(self):
        return self.body

    def merge(self, other: "ScratchBuffer"):
        self.body += other.body
