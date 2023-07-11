import os
os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"]="0"

os.environ['OPENAI_API_KEY'] = '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'

import ktrain
import time

def clf_emotion(msg):
    clf_bert = ktrain.load_predictor(fpath='models\\bert_model')

    start_time = time.time()
    prediction = clf_bert.predict(msg)
    consumed_time = time.time() - start_time

    return prediction, consumed_time

    

if __name__ == "__main__":
    message = 'I just broke up with my boyfriend'
    # message = 'How would you feel if I gave you your copy in person?'

    print('predicted: {} ({:.2f})'.format(clf_emotion(message)[0], clf_emotion(message)[1]))