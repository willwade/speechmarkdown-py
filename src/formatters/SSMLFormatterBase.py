class TagsObject:
    def __init__(self, base):
        self.base = base
        self.tags = {}
        self.text = ""

    def tag(self, tag_name, attrs, augment=False):
        sort_id = self.base.ssml_tag_sort_order.index(tag_name)
        if tag_name not in self.tags:
            self.tags[tag_name] = {'sort_id': sort_id, 'attrs': {}}
        if augment:
            self.tags[tag_name]['attrs'].update(attrs)
        else:
            self.tags[tag_name]['attrs'] = attrs

    def voice_tag_named(self, voices, name):
        info = voices.get(name) if voices else None
        if info:
            if not isinstance(info, dict):
                info = {'voice': {'name': name}}
            for tag, attributes in info.items():
                self.tag(tag, attributes)
            return True
        return False

    def voice_tag(self, tag, value):
        name = self.base.sentence_case(value or 'device')
        return self.voice_tag_named(self.base.options.voices, name) or \
               self.voice_tag_named(self.base.valid_voices, name)
            
            import html
from FormatterBase import FormatterBase

class SsmlFormatterBase(FormatterBase):
    XML_ESCAPE_MAPPING = {
        '<': '&lt;',
        '>': '&gt;',
        '&': '&amp;',
        '"': '&quot;',
        "'": '&apos;'
    }

    def __init__(self, options):
        super().__init__(options)
        self.section_tags = []
        self.valid_voices = {}
        self.ssml_tag_sort_order = [
            'emphasis', 'say-as', 'prosody', 'amazon:domain',
            'amazon:effect', 'amazon:emotion', 'voice', 'lang', 'sub', 'phoneme'
        ]

    def format(self, ast):
        lines = []
        self.format_from_ast(ast, lines)
        return ''.join(lines)

    def start_tag(self, tag, attrs=None, new_line=False):
        attr_str = ' '.join(f'{k}="{v}"' for k, v in (attrs or {}).items())
        return f"<{tag} {attr_str}>{'\n' if new_line else ''}"

    def end_tag(self, tag, new_line=False):
        return f"{'\n' if new_line else ''}</{tag}>"

    def void_tag(self, tag, attrs=None):
        attr_str = ' '.join(f'{k}="{v}"' for k, v in (attrs or {}).items())
        return f"<{tag} {attr_str}/>"

    def sentence_case(self, text):
        return text.capitalize()

    def escape_xml_characters(self, unescaped):
        return html.escape(unescaped)

    def format_from_ast(self, ast, lines):
        raise NotImplementedError("Must implement format_from_ast")