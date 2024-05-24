from pyparsing import ParserElement, Word, alphas, alphanums, nums, OneOrMore, Optional, Group

class SpeechMarkdownParser:
    def __init__(self):
        self.parser = self.create_grammar()

    def create_grammar(self):
        # Define grammar here
        ParserElement.setDefaultWhitespaceChars(' \t\r')  # Setting default whitespace characters

        # Example elements
        text = Word(alphas + nums + '- ')  # Example of parsing normal words with spaces and hyphens
        number = Word(nums)
        break_time = Group('[' + number + 's]')  # Example for break times like [3s]

        # Example simple grammar
        speech_markdown = OneOrMore(text | break_time)

        return speech_markdown

    def parse(self, speechmarkdown):
        try:
            parsed_data = self.parser.parseString(speechmarkdown, parseAll=True)
            return parsed_data.asList()  # Convert pyparsing.ParseResults to a list
        except Exception as e:
            print("Error parsing Speech Markdown:", e)
            return None