import os

def create_folder(path):
    """
    :param path: create a folder if the path did not exist
    """
    if not os.path.exists(path):
        os.makedirs(path)

