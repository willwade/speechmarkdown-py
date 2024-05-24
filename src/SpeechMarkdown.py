class SpeechOptions:
    def __init__(self, include_formatter_comment=False, include_paragraph_tag=False,
                 include_speak_tag=True, platform='', preserve_empty_lines=True):
        self.include_formatter_comment = include_formatter_comment
        self.include_paragraph_tag = include_paragraph_tag
        self.include_speak_tag = include_speak_tag
        self.platform = platform
        self.preserve_empty_lines = preserve_empty_lines

class SpeechMarkdown:
    def __init__(self, options=None):
        self.defaults = SpeechOptions()
        self.options = self.merge_options(self.defaults, options)
        self.parser = None

    def merge_options(self, defaults, options):
        if options is None:
            return defaults
        # Update default options with any specified options
        merged = SpeechOptions(
            include_formatter_comment=options.include_formatter_comment if options.include_formatter_comment is not None else defaults.include_formatter_comment,
            include_paragraph_tag=options.include_paragraph_tag if options.include_paragraph_tag is not None else defaults.include_paragraph_tag,
            include_speak_tag=options.include_speak_tag if options.include_speak_tag is not None else defaults.include_speak_tag,
            platform=options.platform if options.platform else defaults.platform,
            preserve_empty_lines=options.preserve_empty_lines if options.preserve_empty_lines is not None else defaults.preserve_empty_lines
        )
        return merged

    def get_parser(self):
        if not self.parser:
            from speech_markdown_parser import SpeechMarkdownParser
            self.parser = SpeechMarkdownParser()
        return self.parser

    def to_text(self, speechmarkdown, options=None):
        method_options = self.merge_options(self.options, options)
        ast = self.get_parser().parse(speechmarkdown)
        # Assuming we have a factory function to create formatters based on options
        from formatter_factory import create_text_formatter
        formatter = create_text_formatter(method_options)
        return formatter.format(ast)

    def to_ssml(self, speechmarkdown, options=None):
        method_options = self.merge_options(self.options, options)
        ast = self.get_parser().parse(speechmarkdown)
        from formatter_factory import create_formatter
        formatter = create_formatter(method_options)
        return formatter.format(ast)

    def to_ast(self, speechmarkdown):
        return self.get_parser().parse(speechmarkdown)

    def to_ast_string(self, speechmarkdown):
        ast = self.to_ast(speechmarkdown)
        return str(ast)