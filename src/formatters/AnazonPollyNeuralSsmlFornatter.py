from ssml_formatter_base import SsmlFormatterBase, TagsObject

class AmazonPollyNeuralSsmlFormatter(SsmlFormatterBase):
    def __init__(self, options):
        super().__init__(options)
        self.modifier_key_to_ssml_tag_mappings.update({
            'cardinal': 'say-as',
            'digits': 'say-as',
            'drc': 'amazon:effect',
            'lang': 'lang',
            'newscaster': 'amazon:domain'
        })
        self.modifier_key_mappings.update({
            'digits': 'digits',
            'cardinal': 'cardinal'
        })

    def get_text_modifier_object(self, ast):
        text_modifier_object = TagsObject(self)
        for child in ast['children']:
            if child['name'] in ['plainText', 'plainTextSpecialChars', 'plainTextEmphasis', 'plainTextPhone', 'plainTextModifier']:
                text_modifier_object.text = child['allText']
            elif child['name'] == 'textModifierKeyOptionalValue':
                key = self.modifier_key_mappings.get(child['children'][0]['allText'], child['children'][0]['allText'])
                value = child['children'][1]['allText'] if len(child['children']) == 2 else ''
                ssml_tag = self.modifier_key_to_ssml_tag_mappings[key]
                text_modifier_object.tag(ssml_tag, {'interpret-as': key, 'format': value or 'default'}, augment=True)
        return text_modifier_object

    def format_from_ast(self, ast, lines=[]):
        if ast['name'] == 'document':
            if self.options.include_formatter_comment:
                self.add_comment('Converted from Speech Markdown to SSML for Amazon Polly', lines)
            if self.options.include_speak_tag:
                return self.add_speak_tag(ast['children'], True, False, None, lines)
            else:
                self.process_ast(ast['children'], lines)
                return lines
        # Handle other AST nodes similarly
        # This is a simplified translation of the detailed switch-case logic in TypeScript
        # More specific cases should be implemented following the same pattern

# Example usage
options = SpeechOptions(preserve_empty_lines=True, include_formatter_comment=True)
formatter = AmazonPollyNeuralSsmlFormatter(options)
ast = {'name': 'document', 'children': [{'name': 'plainText', 'allText': 'Example text'}]}
output = formatter.format(ast)
print(output)