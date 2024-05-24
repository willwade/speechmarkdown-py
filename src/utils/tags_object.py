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