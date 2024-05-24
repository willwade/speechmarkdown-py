import re
from formatter_base import FormatterBase

class TextFormatter(FormatterBase):
    def __init__(self, options):
        super().__init__(options)

    def format(self, ast):
        lines = []
        self.format_from_ast(ast, lines)
        txt = ''.join(lines).strip()
        # Replace multiple whitespace with a single space
        txt = re.sub(r' +', ' ', txt)
        return txt

    def format_from_ast(self, ast, lines=[]):
        if ast['name'] == 'document' or ast['name'] == 'paragraph' or ast['name'] == 'simpleLine':
            self.process_ast(ast['children'], lines)
        
        elif ast['name'] == 'lineEnd':
            lines.append(ast['allText'])
        
        elif ast['name'] == 'emptyLine':
            if self.options.preserve_empty_lines:
                lines.append(ast['allText'])

        elif ast['name'] in ['plainText', 'plainTextSpecialChars', 'plainTextEmphasis', 'plainTextPhone', 'plainTextModifier']:
            lines.append(ast['allText'])

        elif ast['name'] == 'audio':
            pass  # Assuming audio tags might be processed or handled differently
        
        else:
            if 'children' in ast:
                self.process_ast(ast['children'], lines)

        return lines

    def process_ast(self, children, lines):
        for child in children:
            self.format_from_ast(child, lines)