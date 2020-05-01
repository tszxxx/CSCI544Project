import tensorflow as tf
import numpy as np
import pandas as pd
from gensim.models.word2vec import Word2Vec
from numpy import random
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler
import re
import time

class Encoder(tf.keras.layers.Layer):
    def __init__(self, batch_size, enc_units, input_dim, embedding_dim):
        super(Encoder, self).__init__()
        self.batch_size = batch_size
        self.enc_units = enc_units
        self.embedding = tf.keras.layers.Embedding(input_dim, embedding_dim)
        
        self.lstm = tf.keras.layers.LSTM(self.enc_units, dropout = 0.2, recurrent_dropout=0.2, return_sequences = True, return_state = True)
    
    def call(self, x):
        x = self.embedding(x)
        _, state, _ = self.lstm(x)
        return state

class AudioEncoder(tf.keras.layers.Layer):
    def __init__(self, batch_size):
        super(AudioEncoder, self).__init__()
        self.batch_size = batch_size
        self.denseLayer1 = tf.keras.layers.Dense(256, activation = 'relu')
        self.denseLayer2 = tf.keras.layers.Dense(128, activation = 'relu')
        self.denseLayer3 = tf.keras.layers.Dense(32)
    
    def call(self, x):
        x = tf.cast(x, tf.float32)
        hidden1 = self.denseLayer1(x)
        hidden2 = self.denseLayer2(hidden1)
        output = self.denseLayer3(hidden2)
        return output

class Decoder(tf.keras.layers.Layer):
    def __init__(self, batch_size, dec_units, activation):
        super(Decoder, self).__init__()
        self.dec_units = dec_units
        self.batch_size = batch_size
        self.activation = activation
        self.dense = tf.keras.layers.Dense(self.dec_units, activation = self.activation)

    def call(self, x, audio):
        x = tf.dtypes.cast(x, tf.float32)
        print(audio.shape)
        audio = tf.dtypes.cast(audio, tf.float32)
        inputs = tf.concat([x, audio], axis = 1)
        
        output = self.dense(inputs)
        return output

optimizer = tf.keras.optimizers.Adam(learning_rate=1e-5)
loss_object = tf.keras.losses.BinaryCrossentropy(from_logits=True, reduction='none')
def loss_function(pred, real):
    real = tf.expand_dims(real, 1)
    loss_ = loss_object(real, pred)
    loss = tf.reduce_mean(loss_)

    return loss

def checknan(array):
    array_sum = np.sum(array)
    array_has_nan = np.isnan(array_sum)
    return array_has_nan

#@tf.function
def train_step(text, audio, labels):
    loss = 0
    
    with tf.GradientTape() as tape: 
        state = encoder(text)
        # if checknan(state.numpy()):
        #     np.savetxt('test.out', state.numpy(), delimiter=',')   # X is an array

        np.savetxt('audio_before_conversion.txt', audio)
        audio = tf.convert_to_tensor(audio)
        # np.savetxt('audio.txt', audio.numpy())
        audio_feature = audioEncoder(audio)
        # np.savetxt('audio_feature.txt', audio_feature.numpy())
        output = decoder(state, audio_feature)
        batch_loss = loss_function(output, labels)
        loss += batch_loss
        
        variables = encoder.trainable_variables + decoder.trainable_variables

        gradients = tape.gradient(loss, variables)

        optimizer.apply_gradients(zip(gradients, variables))

        return loss

data_path = 'processed_data_small_char.csv'
wv_model_path = 'pad_word2vec_small_char_model'
data = pd.read_csv(data_path)
data = data[['descriptions', 'id', 'scores']]
data.head()


audio_path = 'Audio_Data.csv'
audio = pd.read_csv(audio_path)
audio = audio[['Id', 'chroma_stft', 'rmse', 'spectral_centroid',
       'spectral_bandwidth', 'rolloff', 'zero_crossing_rate', 'mfcc1', 'mfcc2',
       'mfcc3', 'mfcc4', 'mfcc5', 'mfcc6', 'mfcc7', 'mfcc8', 'mfcc9', 'mfcc10',
       'mfcc11', 'mfcc12', 'mfcc13', 'mfcc14', 'mfcc15', 'mfcc16', 'mfcc17',
       'mfcc18', 'mfcc19', 'mfcc20', 'label']]
audio = audio.rename(columns = {'Id':'id'})

text_audio = data.merge(audio, on = 'id', how = 'left')
text_audio = text_audio.dropna()
wv_model_path = 'pad_word2vec_small_char_model'
wv_model = Word2Vec.load(wv_model_path)

vocab = {word: index for index, word in enumerate(wv_model.wv.index2word)}
reverse_vocab = {index: word for index, word in enumerate(wv_model.wv.index2word)}

embedding_matrix = wv_model.wv.vectors
embedding_matrix.shape


def train_test_split(data):
    test_index = random.choice(range(len(data)), data.shape[0] // 4)
    test_data = data[data.index.isin(test_index)]
    train_data = data[~data.index.isin(test_index)]
    
    return train_data, test_data

text_audio['scores'] = text_audio['label'].apply(lambda x: 1 if str(x).strip() == 'high' else 0)
# text_audio = text_audio.drop([71, 469])
train_data, test_data = train_test_split(text_audio)

unk_index = vocab['<UNK>']
def transform_data(sentence,vocab):
    words=sentence.split(' ')
    idxs=[vocab[word] if word in vocab else unk_index for word in words]
    return idxs

train_idxs = train_data['descriptions'].apply(lambda x:transform_data(x,vocab))
test_idxs = test_data['descriptions'].apply(lambda x:transform_data(x,vocab))
all_idxs = data['descriptions'].apply(lambda x:transform_data(x,vocab))

train_text = np.array(train_idxs.tolist())
test_text = np.array(test_idxs.tolist())
all_text = np.array(all_idxs.tolist())
train_label = np.array(train_data['scores'].values)
test_label = np.array(test_data['scores'].values)
all_label = np.array(data['scores'].values)
label_list = [train_label, test_label, all_label]

train_audio = train_data.iloc[:, 3:-1].values
test_audio = test_data.iloc[:, 3:-1].values

def normalize(train, test = None):
    scaler = StandardScaler()
    scaler.fit(train)
    train = scaler.transform(train)
    if test is not None:
        test = scaler.transform(test)
    return train, test

train_audio, test_audio = normalize(train_audio, test_audio)

# print(test_text.shape, test_audio.shape)
# print(train_text.shape, train_audio.shape)
# print(test_label.shape)

def get_batches(batch_size, train_text, train_audio, train_y):
    for i in range(0, len(train_text), batch_size):
        if i + batch_size < len(train_text):
            yield train_text[i: i+batch_size], train_audio[i: i+batch_size], train_y[i: i+batch_size]
        else:
            yield train_text[i:], train_audio[i:], train_y[i:]


BATCH_SIZE = train_data.shape[0] // 3

ENC_UNITS = 32
DEC_UNITS = 1

EMBEDDING_DIM = 100

max_len = len(vocab)

encoder = Encoder(batch_size = BATCH_SIZE, enc_units = ENC_UNITS, input_dim = max_len, embedding_dim = EMBEDDING_DIM)
audioEncoder = AudioEncoder(batch_size = BATCH_SIZE)
decoder = Decoder(batch_size = BATCH_SIZE, dec_units = DEC_UNITS, activation = 'sigmoid')
EPOCHS = 5

for epoch in range(EPOCHS):
    start = time.time()
    total_loss = 0
    
    for batch, (batch_text, batch_audio, batch_label) in enumerate(get_batches(BATCH_SIZE, train_text, train_audio, train_label)):
        
        batch_loss = train_step(batch_text, batch_audio, batch_label)
        total_loss += batch_loss
        
        if batch % 2 == 0:
            print('Epoch {} Batch {} Loss {:.4f}'.format(epoch + 1,
                                                         batch,
                                                         batch_loss.numpy()))

        

    print('Epoch {} Loss {:.4f}'.format(epoch + 1, total_loss.numpy()))
    print('Time taken for 1 epoch {} sec\n'.format(time.time() - start))

def evaluate(test_text, test_audio):
    test_text = tf.convert_to_tensor(test_text)
    test_audio = tf.convert_to_tensor(test_audio)

    state = encoder(test_text)
    audio_feature = audioEncoder(test_audio)
    output = decoder(state, audio_feature)
    return output.numpy()

def analyze(output, test_label):
    output = np.squeeze(output)
    output[output > 0.5] = 1
    output[output <= 0.5] = 0
    test_label = np.squeeze(test_label)
    # print(classification_report(test_label, output))
    return classification_report(test_label, output)

output = evaluate(test_text, test_audio)
report = analyze(output, test_label)



