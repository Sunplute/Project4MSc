import pandas as pd
import re
from nltk.tokenize import word_tokenize
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

def clean_text(data):
    
    # remove hashtags and @usernames
    data = re.sub(r"(#[\d\w\.]+)", '', data)# eg. #example123
    data = re.sub(r"(@[\d\w\.]+)", '', data)
    
    # tekenization using nltk / 分词
    data = word_tokenize(data)
    
    return data

def gen_mess(mess):
    data_train = pd.read_csv('data/data_train.csv', encoding='utf-8')
    data_test = pd.read_csv('data/data_test.csv', encoding='utf-8')

    data = data_train.append(data_test, ignore_index=True)

    texts = [' '.join(clean_text(text)) for text in data.Text]

    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(texts)

    seq = tokenizer.texts_to_sequences(mess)
    padded = pad_sequences(seq, maxlen=500)

    return padded

if __name__ == '__main__':
    Mess = "I hate you."
    padded_mess = gen_mess(Mess)
    print(padded_mess)