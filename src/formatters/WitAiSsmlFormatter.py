from ssml_formatter_base import SsmlFormatterBase

class CustomSSMLFormatter(SsmlFormatterBase):
    def __init__(self, options):
        super().__init__(options)

    def format_from_ast(self, ast, lines=[]):
        tag_name = ast.get('name')
        attributes = ast.get('attributes', {})
        text = ast.get('text', '')

        if tag_name == 'speak':
            lines.append('<speak>')
            self.process_ast(ast.get('children', []), lines)
            lines.append('</speak>')

        elif tag_name in ['p', 's']:
            lines.append(f'<{tag_name}>')
            self.process_ast(ast.get('children', []), lines)
            lines.append(f'</{tag_name}>')

        elif tag_name == 'break':
            time = attributes.get('time', '1s')
            lines.append(f'<break time="{time}"/>')

        elif tag_name in ['w', 'token']:
            role = attributes['role']
            lines.append(f'<w role="{role}">{text}</w>')

        elif tag_name == 'say-as':
            interpret_as = attributes['interpret-as']
            format_str = f' format="{attributes["format"]}"' if 'format' in attributes else ''
            lines.append(f'<say-as interpret-as="{interpret_as}"{format_str}>{text}</say-as>')

        elif tag_name == 'emphasis':
            level = attributes.get('level', 'moderate')
            lines.append(f'<emphasis level="{level}">{text}</emphasis>')

        elif tag_name == 'prosody':
            rate = attributes.get('rate', 'medium')
            pitch = attributes.get('pitch', 'medium')
            volume = attributes.get('volume', 'medium')
            lines.append(f'<prosody rate="{rate}" pitch="{pitch}" volume="{volume}">{text}</prosody>')

        elif tag_name == 'phoneme':
            ph = attributes['ph']
            alphabet = attributes['alphabet']
            lines.append(f'<phoneme alphabet="{alphabet}" ph="{ph}">{text}</phoneme>')

        elif tag_name == 'sfx':
            character = attributes.get('character', '')
            environment = attributes.get('environment', '')
            char_str = f' character="{character}"' if character else ''
            env_str = f' environment="{environment}"' if environment else ''
            lines.append(f'<sfx{char_str}{env_str}>{text}</sfx>')

        elif tag_name == 'voice':
            style = attributes.get('style', 'default')
            lines.append(f'<voice style="{style}">{text}</voice>')

        return lines

    def process_ast(self, children, lines):
        for child in children:
            self.format_from_ast(child, lines)

# Example usage
formatter = CustomSSMLFormatter(options={})
ast = {
    'name': 'speak',
    'children': [
        {'name': 'p', 'children': [
            {'name': 's', 'children': [{'name': 'text', 'text': 'This is a sentence within a paragraph.'}]}
        ]}
    ]
}
ssml_output = formatter.format_from_ast(ast, [])
print(''.join(ssml_output))