from pyparsing import Word, alphas, nums, alphanums, oneOf, Optional, Combine, Group, delimitedList, ZeroOrMore, OneOrMore, QuotedString, nestedExpr, LineEnd, White, LineStart, StringEnd, ParserElement, Forward, Suppress, Keyword, Literal

# Set up basic characters and whitespace handling
ParserElement.setDefaultWhitespaceChars(" \t\r")

# Helper function to escape special characters
def escape_chars(chars):
    return "".join("\\" + char if char in "[]()*~`@#\\_!+-" else char for char in chars)

# Grammar Definitions
specialCharSet = "[]()"
specialCharSetEmphasis = escape_chars(specialCharSet + "*~`@#\\_!+-")
nonSpecialChar = "".join(c for c in alphanums + ' ' if c not in specialCharSetEmphasis)

# Basic textual elements
integer = Word(nums)
decimal = Combine(integer + Optional('.' + Optional(Word(nums))))
timeUnit = oneOf("s ms")
time = Group(decimal + timeUnit)
nonSpecialWord = Word(nonSpecialChar)
plainText = OneOrMore(nonSpecialWord | White())

# Emphasis
emphasisMarker = oneOf("+ ++ ~ -")
emphasis = Group(emphasisMarker + plainText + emphasisMarker)

# Modifiers
modifierKey = oneOf("emphasis address number cardinal characters chars digits drc expletive bleep fraction interjection ordinal telephone phone unit time date whisper ipa sub vol volume rate pitch timbre lang voice excited disappointed")
modifierValue = QuotedString('"') | QuotedString("'")
modifier = Group(modifierKey + Optional(Suppress(':') + modifierValue))
modifierList = nestedExpr(content=delimitedList(modifier, delim=';'))

# Text with modifiers
textWithModifier = Group(plainText + Suppress('[') + modifierList + Suppress(']'))

# Breaks
breakSpec = Group(Suppress('[') + 'break' + Suppress(':') + (modifierValue | time) + Suppress(']'))

# Paragraphs and sections
paragraph = OneOrMore(plainText | emphasis | textWithModifier | breakSpec)

# Define the overall document structure
document = ZeroOrMore(paragraph + LineEnd())

# Create a parser element based on the document
speech_markdown_parser = document.ignore(White())

def parse_speech_markdown(text):
    try:
        result = speech_markdown_parser.parseString(text, parseAll=True)
        return result.asList()
    except Exception as e:
        print("Parsing error:", str(e))
        return []

# Example usage
example_text = "This is an example of [emphasis: 'strong'] speech markdown with a break of [3s]."
parsed_data = parse_speech_markdown(example_text)
print(parsed_data)