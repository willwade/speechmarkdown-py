def create_formatter(options):
    platform = getattr(options, 'platform', 'default')
    if platform == 'amazon-alexa':
        return AmazonAlexaSsmlFormatter(options)
    elif platform == 'amazon-polly':
        return AmazonPollySsmlFormatter(options)  # Define this class similarly to AmazonAlexaSsmlFormatter
    elif platform == 'google-assistant':
        return GoogleAssistantSsmlFormatter(options)  # Define this class
    elif platform == 'samsung-bixby':
        return SamsungBixbySsmlFormatter(options)  # Define this class
    elif platform == 'microsoft-azure':
        return MicrosoftAzureSsmlFormatter(options)  # Define this class
    else:
        return TextFormatter(options)

def create_text_formatter(options):
    return TextFormatter(options)