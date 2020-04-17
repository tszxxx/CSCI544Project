import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import shutil
import os
from os import listdir
from os.path import isfile, isdir, join
import csv

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder,StandardScaler
from sklearn.metrics import classification_report
from keras import models
from keras import layers

def getFeatures(audiopath):

	y, sr = librosa.load(audiopath, mono=True, duration=60)

	# Compute a chromagram	
	chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)

	#root-mean-square (RMS) energy for each frame
	rmse = librosa.feature.rms(y=y)[0]

	#Spectral Centroid
	spec_cent = librosa.feature.spectral_centroid(y=y, sr=sr)

	#Spectral bandwidth
	spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
	
	#Spectral rolloff
	rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
	
	#Zero Crossing Rate
	zcr = librosa.feature.zero_crossing_rate(y)

	#MFCC — Mel-Frequency Cepstral Coefficients 20 coefficients
	mfcc = librosa.feature.mfcc(y=y, sr=sr)

	featureStr = ' '+str(np.mean(chroma_stft))
	featureStr += ' '+str(np.mean(rmse))
	featureStr += ' '+str(np.mean(spec_cent))
	featureStr += ' '+str(np.mean(spec_bw))
	featureStr += ' '+str(np.mean(rolloff))
	featureStr += ' '+str(np.mean(zcr))
	
	for e in mfcc:
		featureStr += ' '+str(np.mean(e))

	return y,sr,chroma_stft,rmse,spec_cent,spec_bw,rolloff,zcr,mfcc,featureStr

def plotFeatures(y,sr,chroma_stft,rmse,spec_cent,spec_bw,rolloff,zcr,mfcc):
	S, phase = librosa.magphase(librosa.stft(y))

	#display waveform
	f1 = plt.figure(1, figsize=(10,4))
	librosa.display.waveplot(y,sr=sr)
	plt.title('Monophonic')

	#display power spectrogram
	f2 = plt.figure(2, figsize=(10, 4))
	librosa.display.specshow(chroma_stft, y_axis='chroma', x_axis='time')
	plt.colorbar()
	plt.title('Chromagram')
	plt.tight_layout()

	#display root-mean-square(RMS) value for each frame
	f3 = plt.figure(3)
	plt.subplot(2, 1, 1)
	plt.semilogy(rmse.T, label='RMS Energy')
	plt.xticks([])
	plt.xlim([0, rmse.shape[-1]])
	plt.legend(loc='best')
	plt.subplot(2, 1, 2)
	librosa.display.specshow(librosa.amplitude_to_db(S, ref=np.max),y_axis='log', x_axis='time')
	plt.title('log Power spectrogram')
	plt.tight_layout()

	#display extracted spectral centroid
	f4 = plt.figure(4)
	plt.semilogy(spec_cent.T, label='Spectral centroid')
	plt.ylabel('Hz')
	plt.xticks([])
	plt.xlim([0, spec_cent.shape[-1]])
	plt.legend()

	#display spectral bandwidth
	f5 = plt.figure(5)
	plt.semilogy(spec_bw.T, label='Spectral bandwidth')
	plt.ylabel('Hz')
	plt.xticks([])
	plt.xlim([0, spec_bw.shape[-1]])
	plt.legend()

	#display rolloff
	f6 = plt.figure(6)
	plt.semilogy(rolloff.T, label='Roll-off frequency')
	plt.ylabel('Hz')
	plt.xticks([])
	plt.xlim([0, rolloff.shape[-1]])
	plt.legend()
	plt.show()

	#display mcff
	plt.figure(7, figsize=(10, 4))
	librosa.display.specshow(mfcc, x_axis='time')
	plt.colorbar()
	plt.title('MFCC')
	plt.tight_layout()
	plt.show()

def creatData():
	failedF = open('failedList.txt','w')

	header = 'filename chroma_stft rmse spectral_centroid spectral_bandwidth rolloff zero_crossing_rate'
	for i in range(1, 21):
		header += f' mfcc{i}'
	header += ' label'
	header = header.split()
	
	file = open('../Audio_Data.csv', 'w', newline='')
	with file:
		writer = csv.writer(file)
		writer.writerow(header)
	
	labels = 'high low'.split()
	for l in labels:
		for filename in os.listdir(f'./tmp/{l}'):
			audiopath = f'./tmp/{l}/{filename}'
			try:
				y,sr,chroma_stft,rmse,spec_cent,spec_bw,rolloff,zcr,mfcc,featureStr = getFeatures(audiopath)
			except:
				failedF.write(audiopath+'\n')
				continue
			to_append = filename+featureStr
			to_append += f' {l}'
			file = open('../Audio_Data.csv', 'a', newline='')
			with file:
				writer = csv.writer(file)
				writer.writerow(to_append.split())
	failedF.close()

def creatAudioDataSet():
	movie_rating = {}

	with open('../Movie_information.csv','r') as read_obj:
		dict_reader = csv.DictReader(read_obj)
		list_of_dict = list(dict_reader)

	for i in range(len(list_of_dict)):
		movie_rating[list_of_dict[i]['id']] = list_of_dict[i]['评分']

	audiopath = '../Audio_data'
	highdir = './tmp/high'
	lowdir = './tmp/low'

	if not os.path.exists(highdir):
		os.makedirs(highdir)
	if not os.path.exists(lowdir):
		os.makedirs(lowdir)

	for f in (f for f in listdir(audiopath) if isfile(join(audiopath,f))):
		f_id = f.split('.')[0]
		if(float(movie_rating[f_id]) > 5):
			shutil.copy(join(audiopath,f),highdir)
		elif(float(movie_rating[f_id]) > 0):
			shutil.copy(join(audiopath,f),lowdir)

def train():
	#reading a dataset
	data = pd.read_csv('../Audio_Data.csv')
	data.head()
	data = data.drop(['filename'],axis=1)
	data.head()

	#preprocessing
	label_list = data.iloc[:,-1]
	encoder = LabelEncoder()
	y = encoder.fit_transform(label_list)

	scaler = StandardScaler()
	X = scaler.fit_transform(np.array(data.iloc[:, :-1], dtype = float))


	#using 20% data to test
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

	model = models.Sequential()
	model.add(layers.Dense(256, activation='relu', input_shape=(X_train.shape[1],)))
	model.add(layers.Dense(128, activation='relu'))
	model.add(layers.Dense(64, activation='relu'))
	model.add(layers.Dense(2, activation='softmax'))

	model.compile(optimizer='adam',
              	loss='sparse_categorical_crossentropy',
              	metrics=['accuracy'])

	history = model.fit(X_train,
                    y_train,
                    epochs=20,
                    batch_size=16)

	test_loss, test_acc = model.evaluate(X_test,y_test)
	print('test_acc: ',test_acc)

	y_pred = model.predict(X_test)
	y_pred_bool = np.argmax(y_pred, axis = 1)

	print(classification_report(y_test,y_pred_bool))
	

if __name__ == '__main__':
	creatAudioDataSet()
	creatData()
	#getFeatures('./tmp/high/11598977.mp4')
	#train()





