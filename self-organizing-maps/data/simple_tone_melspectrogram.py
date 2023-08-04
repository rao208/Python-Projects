import sys
import os
from os.path import dirname, abspath

d = dirname(dirname(abspath(__file__)))
sys.path.insert(0, d)

from matplotlib import pyplot as plt
import numpy as np
import scipy
from scipy import signal
import librosa.display
import plotting_helper
import create_image_folder
from audio_module import AudioUtil
import data_pickle

np.set_printoptions(suppress=True)

if __name__ == "__main__":

    download_path = os.path.join(os.getcwd(), 'audio')

    spectrogram_out_path = os.path.join(os.getcwd(), 'Results', 'spectrogram_images')
    input_subplot_path = os.path.join(os.getcwd(), 'Results','input_subplots')

    create_image_folder.create_folder(spectrogram_out_path)
    create_image_folder.create_folder(input_subplot_path)

    #######################################################################################################################

    res = []
    for sound_name in os.listdir(download_path):
        # check if current path is a file
        if os.path.isfile(os.path.join(download_path, sound_name)):
            res.append(sound_name)
    print(res)

    audio = AudioUtil()

    #######################################################################################################################

    sr = 44100
    n_fft = 2048
    win_length = int(round(0.04 * sr)) # seconds * sr = samples
    hop_length = win_length # int(round(hop_length))
    fix_length_size = 0.4*sr

    meta_data = []

    #######################################################################################################################

    for inp in res:

        path = os.path.join(download_path, inp)

        sound = audio.open(path, sample_rate= sr)
        trimmed_audio = librosa.util.fix_length(sound[0], size=int(fix_length_size))
        emphasized_sound = librosa.effects.preemphasis(trimmed_audio)


        mel_spectrogram = librosa.feature.melspectrogram(y=emphasized_sound,
                                                         sr=sound[1],
                                                         n_fft=n_fft,
                                                         win_length = win_length,
                                                         hop_length= hop_length,
                                                         window=scipy.signal.windows.hamming,
                                                         )

        max_mel = np.max(mel_spectrogram)
        mel_spectrogram = mel_spectrogram/max_mel

        mel_image_path = spectrogram_out_path + '/' + inp.split(".")[0] + '.png'

        fig1, ax1 = plt.subplots(figsize=(15, 15))
        plotting_helper.plot_data(ax=ax1,
                                  data= mel_spectrogram,
                                  sample_rate = sound[1],
                                  hop_length = hop_length,
                                  win_length= win_length,
                                  n_fft= n_fft)
        plotting_helper.save_fig(fig= fig1, path = mel_image_path)

        fig3, ax3 = plt.subplots(3, 1, figsize=(15, 15))
        plotting_helper.input_subplot_save(ax = ax3,
                                           sound_input=sound[0],
                                           trimmed_input=trimmed_audio,
                                           emphasized_input=emphasized_sound)

        plotting_helper.save_fig(fig= fig3, path= input_subplot_path + '/' + inp.split(".")[0] + '.png')

        data_dict = {
            'filename': inp,
            'sample_rate': sound[1],
            'duration': librosa.get_duration(y=emphasized_sound, sr=sound[1]),
            'mel_spectrogram': mel_spectrogram.tolist(),
            'mel_spectrogram_image_path': mel_image_path
        }

        meta_data.append(data_dict)

    data_pickle.pickle_data(out_path='meta_data.pickle', data=meta_data)
    # data_pickle.json_data(out_path='res_list.txt', data=new_dataset)
