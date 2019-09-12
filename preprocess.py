import re
from number_cleaning import normalize_numbers

_abbreviations = [(re.compile('\\b%s\\.' % x[0], re.IGNORECASE), x[1]) for x in [
                  ('mrs', 'misess'),
                  ('mr', 'mister'),
                  ('dr', 'doctor'),
                  ('st', 'saint'),
                  ('co', 'company'),
                  ('jr', 'junior'),
                  ('sr', 'senior'),
                  ('maj', 'major'),
                  ('gen', 'general'),
                  ('drs', 'doctors'),
                  ('rev', 'reverend'),
                  ('lt', 'lieutenant'),
                  ('hon', 'honorable'),
                  ('sgt', 'sergeant'),
                  ('capt', 'captain'),
                  ('esq', 'esquire'),
                  ('ltd', 'limited'),
                  ('col', 'colonel'),
                  ('ft', 'fort'),
                  ('II', 'second'),
                  ('III', 'third'),
                  ('IV', 'fourth'),
                  ('V', 'fifth'),
                  ('jan', 'january'),
                  ('feb', 'february'),
                  ('mar', 'march'),
                  ('apr', 'april'),
                  ('jun', 'june'),
                  ('jul', 'july'),
                  ('aug', 'august'),
                  ('sep', 'september'),
                  ('oct', 'october'),
                  ('nov', 'november'),
                  ('dec', 'december'),
                  ('&', 'and')]]


def expand_abbr(text):
    for i, sen in enumerate(text):
        for abbr, replacement in _abbreviations:
            text[i] = re.sub(abbr, replacement, sen)
    return text


def find_all_capital(text):
    for i, sen in enumerate(text):
        sen = sen.split(' ')
        for j, word in enumerate(sen):
            if word.isupper() and len(word) > 1:
                if re.match(r"OAF(\W*)|ISIS(\W*)|ISIL(\W*)|PAC(\W*)|STEM(\W*)|AIDS(\W*)|NASA(\W*)|TED(\W*)|FOIA(\W*)|"
                            r"NABTU(\W*)|CHIP(\W*)|NATO(\W*)|AIDS(\W*)", word):
                    continue
                print(' '.join(sen) + 'has' + word)
                if word[-1] in [',', '.']:  # FBI. -> F B I.
                    sen[j] = ' '.join(list(word[:-1])) + word[-1]
                else:
                    sen[j] = ' '.join(list(word))  # FBI -> F B I
        sen = ' '.join(sen)
        print("After fixing" + sen)
        text[i] = sen
    return text


def find_punc_btw_two_chr(text):
    for i, sen in enumerate(text):
        sen = sen.split(' ')
        for j, word in enumerate(sen):
            if re.match(r'(\w+)(\W)(\w+)', word):
                word = re.sub(r'(\w+)(\W+dddd)(\w+)', r'\1 \3', word)  # 10:23 -> 10 23
                print(word)
                sen[j] = word
        sen = ' '.join(sen)
        text[i] = sen
    return text


def collapse_whitespace(text):
    for i, sen in enumerate(text):
        text[i] = re.sub(re.compile(r'\s+'), ' ', sen)
    return text


def clean_punc(text):
    for i, sen in enumerate(text):
        text[i] = re.sub(r'\"|\'|!|\?|\)|\(|\;|\]|\[\:', '', sen)
    return text


def expand_number(text):
    for i, sen in enumerate(text):
        sen = sen.split(' ')
        for j, word in enumerate(sen):
            sen[j] = normalize_numbers(word)
        text[i] = ' '.join(sen)
    return text


if __name__ == '__main__':
    with open('output.txt', 'r') as output:
        lines = output.read().splitlines()

    lines = [line.strip() for line in lines]

    lines = expand_number(lines)
    lines = expand_abbr(lines)
    lines = clean_punc(lines)
    lines = collapse_whitespace(lines)
    lines = find_all_capital(lines)
    lines = find_punc_btw_two_chr(lines)

    with open('output_processed.txt', 'w') as w:
        for line in lines:
            w.write(line + '\n')
