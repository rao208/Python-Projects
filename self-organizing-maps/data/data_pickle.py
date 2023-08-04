import pickle
import numpy as np
import json

def unpickle_data(path: str):

    """
    :param path: path to the .pickle file to unpickle and convert the byte stream into a Python object

    """

    mel_spectrogram_input = []
    audio_name = []
    with open(path, "rb") as f:
        content = pickle.load(f)
        for dictionary in content:
            mel_spectrogram_input.append(np.array(dictionary['mel_spectrogram']))
            audio_name.append(dictionary['filename'])
    return audio_name, np.array(mel_spectrogram_input)

def pickle_data(out_path: str, data:list):

    """
    :param data: input data to pickle
    :param out_path: output filepath that contains converted python object into a byte stream
    """

    with open(out_path, 'wb') as file:
        pickle.dump(data, file)

def json_data(out_path: str, data:list):
    """

    :param data: input data to convert into json format
    :type out_path: output filepath that contains converted python object to json string
    """
    with open(out_path, 'w') as file:
        file.write(json.dumps(data, indent=4, separators=(',', ': ')))
