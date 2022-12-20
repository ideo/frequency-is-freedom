from time import time

import bz2
import pickle
import _pickle as cPickle


def timer_func(func):
    """
    This function shows the execution time of the function object passed
    """
    def wrap_func(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        
        delta = t2-t1   #duration in seconds
        minutes = int(delta//60)
        seconds = round(delta%60)
        print(f"Function {func.__name__}() executed in {minutes} minutes {seconds} seconds.")

        # print(f"Function {func.__name__!r} executed in {(t2-t1):.4f}s.")
        return result
    return wrap_func


# Pickle a file and then compress it into a file with extension 
def compressed_pickle(data, filepath_with_extension):
    """
    Loads a .pbz2 files. This will expect that file extension.
    """
    with bz2.BZ2File(filepath_with_extension, "w") as write_file: 
        cPickle.dump(data, write_file)


# Load any compressed pickle file
def decompress_pickle(filepath_with_extension):
    """
    Include the .pbz2 extension in the file arg.
    """
    data = bz2.BZ2File(filepath_with_extension, "rb")
    data = cPickle.load(data)
    return data