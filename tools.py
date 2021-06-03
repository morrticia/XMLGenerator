import re


# ფუნქცია გვიბრუნებს სიტყვებისაგან გამოყოფილ სასვენ ნიშნებს, რომელსაც XML თეგის tail ატრიბუტად გამოვიყენებთ
def get_punctuation(word_token):
    punctuation_marks = '''!(){}[];:'"\, <>./?@#$%^&*_~'''

    punctuation = ''
    for e in word_token:
        if e in punctuation_marks:
            punctuation = e

    return punctuation


# ფუნქცია გვიბრუნებს ტოკენებს მუხლებიდან სასვენი ნიშნებით
def word_tokenize(verse):

    new_verse = verse.replace('\xa0', ' ')
    new_verse = new_verse.replace('\n', ' ')
    new_verse = new_verse.replace('\t', ' ')

    tokens = str(new_verse).split(' ')
    new_tokens = []
    first = 0
    index = 0
    # პოულობს სიტყვებში "[]"-ებს, რათა გამოყოს აღდგენილი ნაწილები
    res = re.findall(r'\[.*?\]', new_verse)

    str = ''
    while index < len(res):
        str = new_verse.replace(f'{res[index]}', 'res')
        new_verse = str
        index += 1

    tokens = str(new_verse).split(' ')
    index = 0
    for token in tokens:
        if 'res' in token:
            token = token.replace('res', f'{res[index]}')
            index += 1
        new_tokens.append(token)

    return new_tokens


# ფუნქცია გვიბრუნებს თავისა და მუხლის რიგით ნომერს
def get_key(verse):
    key = ""

    for char in verse[0:6]:
        if char.isnumeric() or char == ',' or char == '.':
            key += char
    return key


# ფუნქციას პარამეტრად გადეცემა თავი და იღებს მუხლის ნომერს, როგორც დელმიტერს თავის მუხლებად დასაყოფად
def get_delimiter(chapter):
    chapter = chapter.split(',')

    for token in chapter:
        if map(str.isdigit, token):
            return f'{token},'
