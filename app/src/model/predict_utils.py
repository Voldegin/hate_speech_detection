import re
import string
import emoji
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

nltk.download('stopwords')
nltk.download('punkt')
stop_words = set(stopwords.words('english'))

banned_list = string.punctuation
punctuation_reg_exp = "[" + banned_list + "]"


def get_emoji_regexp():
    # Sort emoji by length to make sure multi-character emojis are
    # matched first
    emojis = sorted(emoji.EMOJI_DATA, key=len, reverse=True)
    pattern = u'(' + u'|'.join(re.escape(u) for u in emojis) + u')'
    return re.compile(pattern)


emoji_reg_exp = get_emoji_regexp()


def stemmer(text):
    tokenized = nltk.word_tokenize(text)
    ps = PorterStemmer()
    return ' '.join([ps.stem(words) for words in tokenized])


def clean_text(text, stem=True):
    text = text.replace('\r', '').replace('\n', ' ').lower()
    text = re.sub(r"(?:\@|https?\://)\S+", "", text)

    text = [word for word in text.split() if word not in stop_words]
    text = ' '.join(text)

    text = " ".join(word.strip() for word in
                    re.split('#(?!(?:hashtag)\b)[\w-]+(?=(?:\s+#[\w-]+)*\s*$)',
                             text))

    text = re.sub(punctuation_reg_exp, "", text)

    text = re.sub("\s\s+", " ", text)

    text = re.sub(emoji_reg_exp, r"", text)

    if stem:
        text = stemmer(text)
    return text
