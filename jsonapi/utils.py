def valueArrayFromString(text):
    # common sense parsing of text containing list of values
    text = text.strip()
    if text.startswith('{') and text.endswith('}') or text.startswith('[') and text.endswith(']'):
        text = text[1:-1]
    values = [v.strip() for v in text.split(',')]
    return values
# end
