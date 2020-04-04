import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np


def getFeatures(songpath):
	y, sr = librosa.load(songpath, mono=True, duration=60)

	chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)

	rmse = librosa.feature.rms(y=y)[0]

	spec_cent = librosa.feature.spectral_centroid(y=y, sr=sr)

	spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
	
	rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
	
	zcr = librosa.feature.zero_crossing_rate(y)

	mfcc = librosa.feature.mfcc(y=y, sr=sr)
	
	return y,sr,chroma_stft,rmse,spec_cent,spec_bw,rolloff,zcr,mfcc

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


y,sr,chroma_stft,rmse,spec_cent,spec_bw,rolloff,zcr,mfcc = getFeatures('../Audio_data/sample_yewen.mp4')

plotFeatures(y,sr,chroma_stft,rmse,spec_cent,spec_bw,rolloff,zcr,mfcc)




