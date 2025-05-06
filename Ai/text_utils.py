def make_quote_message(text: str) -> str:
    if 'NO QUOTE' in text:
        return 'NO QUOTE'
    quote = text.split('|')[0]
    author = text.split('|')[1]
    return quote + '\n\n' + f'_{author}_'


def make_love_list_message(text: str) -> str:
    quote = text.split("\n\n")[0]
    author = text.split("\n\n")[1]
    return quote + '\n\n' + f'_{author}_'
