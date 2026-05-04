from pathlib import Path
from models import MapData
from .lex import Lexer
from .validation import Assembler, GraphValidator


class Parser:
    def __init__(self) -> None:
        self.lexer: Lexer = Lexer()
        self.assembler: Assembler = Assembler()
        self.graph_validator: GraphValidator = GraphValidator()

    def parse(self, path: str | Path) -> MapData:
        entities = self.lexer.lex(path)
        data = self.assembler.assemble(entities)
        self.graph_validator.validate(data)
        return data
