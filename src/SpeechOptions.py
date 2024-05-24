class SpeechOptions:
    def __init__(self, platform=None, include_formatter_comment=False,
                 include_paragraph_tag=False, include_speak_tag=True,
                 preserve_empty_lines=True, escape_xml_symbols=False, voices=None):
        self.platform = platform if platform is not None else ''
        self.include_formatter_comment = include_formatter_comment
        self.include_paragraph_tag = include_paragraph_tag
        self.include_speak_tag = include_speak_tag
        self.preserve_empty_lines = preserve_empty_lines
        self.escape_xml_symbols = escape_xml_symbols
        self.voices = voices if voices is not None else {}

    def __str__(self):
        return (f"SpeechOptions(platform={self.platform}, include_formatter_comment={self.include_formatter_comment}, "
                f"include_paragraph_tag={self.include_paragraph_tag}, include_speak_tag={self.include_speak_tag}, "
                f"preserve_empty_lines={self.preserve_empty_lines}, escape_xml_symbols={self.escape_xml_symbols}, "
                f"voices={self.voices})")