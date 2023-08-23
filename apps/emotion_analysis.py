import os
os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"]="0"

os.environ['OPENAI_API_KEY'] = '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'

import ktrain

import time
from keras.models import load_model
import numpy as np
import preprocess

def clf_emotion(msg, model = 'lstm'):
    if model == 'bert':
        clf_bert = ktrain.load_predictor(fpath='models\\bert_model')

        start_time = time.time()
        prediction = clf_bert.predict(msg)
        consumed_time = time.time() - start_time
    elif model == 'lstm':
        clf_lstm = load_model('models/biLSTM_w2v.h5')

        class_names = ['joy', 'fear', 'anger', 'sadness', 'neutral']
        padded = preprocess.gen_mess([msg])
        start_time = time.time()
        pred = clf_lstm.predict(padded)
        prediction = class_names[np.argmax(pred)]
        consumed_time = (time.time() - start_time)


    return prediction, consumed_time

    

if __name__ == "__main__":
    message = 'I just broke up with my boyfriend'
    # message = 'How would you feel if I gave you your copy in person?'

    pred, consumed_time = clf_emotion(message, model='lstm')
    print('predicted: {} ({:.2f})'.format(pred, consumed_time))