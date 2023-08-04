import librosa
import numpy as np
import random

class AudioUtil:
    # ----------------------------
    # Load an audio file. Return the signal and the sample rate
    # ----------------------------
    @staticmethod
    def open(audio_file:str, sample_rate=44100 ):
        """

        :param audio_file: path to the input audio file
        :param sample_rate: number of samples per second that are taken of a waveform to create a discete digital signal
        :return: sig: audio time series.
        :return sample_rate: sampling rate of sig
        """
        sig, sample_rate = librosa.load(audio_file, sr=sample_rate)
        return (sig, sample_rate)

    # ----------------------------
    # Pad (or truncate) the signal to a fixed length 'max_ms' in milliseconds
    # ----------------------------

    @staticmethod
    def pad_trunc(aud, max_ms):

        """
        :param aud: a tuple of audio time series data and sanpling rate
        :param max_ms: the total length of the audio file in milliseconds
        :return: sig: audio time series.
        :return sample_rate: sampling rate of sig
        """

        sig, sample_rate = aud
        sig = np.expand_dims(sig, axis=0)
        num_rows, sig_len = sig.shape
        max_len = sample_rate // 1000 * max_ms

        if sig_len > max_len:
            # Truncate the signal to the given length
            sig = sig[:, :max_len]

        elif sig_len < max_len:
            # Length of padding to add at the beginning and end of the signal
            pad_begin_len = random.randint(0, max_len - sig_len)
            pad_end_len = max_len - sig_len - pad_begin_len

            # Pad with 0s
            pad_begin = np.zeros((num_rows, pad_begin_len))
            pad_end = np.zeros((num_rows, pad_end_len))

            sig = np.concatenate((pad_begin, sig, pad_end), 1)

        return (sig, sample_rate)
