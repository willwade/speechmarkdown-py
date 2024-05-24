from .text_formatter import TextFormatter
from .amazon_alexa_ssml_formatter import AmazonAlexaSsmlFormatter
from .amazon_polly_ssml_formatter import AmazonPollySsmlFormatter
from .google_assistant_ssml_formatter import GoogleAssistantSsmlFormatter
from .microsoft_azure_ssml_formatter import MicrosoftAzureSsmlFormatter
from .samsung_bixby_ssml_formatter import SamsungBixbySsmlFormatter

def create_formatter(options):
    # This function could dynamically select which formatter to use
    if options.platform == 'amazon-alexa':
        return AmazonAlexaSsmlFormatter(options)
    elif options.platform == 'google-assistant':
        return GoogleAssistantSsmlFormatter(options)
    # add other conditions here
    else:
        return TextFormatter(options)

def create_text_formatter(options):
    return TextFormatter(options)