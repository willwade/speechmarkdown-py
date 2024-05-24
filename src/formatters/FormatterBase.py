from abc import ABC, abstractmethod

class FormatterBase(Formatter, ABC):
    def __init__(self, options):
        self.options = options

    @abstractmethod
    def format(self, ast):
        pass

    def add_array(self, ast, lines):
        for child in ast:
            lines = self.format_from_ast(child, lines)
        return lines

    @abstractmethod
    def format_from_ast(self, ast, lines):
        pass

    def process_ast(self, ast, lines):
        if isinstance(ast, list):
            return self.add_array(ast, lines)
        else:
            return self.format_from_ast(ast, lines)