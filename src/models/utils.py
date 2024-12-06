import os
import pandas as pd
import numpy as np
from os.path import (
    join,
    abspath,
    dirname,
    normpath
)

HERE = dirname(__file__)

data_directory_path = normpath(abspath(join(HERE, '../../', 'data')))
models_directory_path = normpath(abspath(join(HERE, '../../', 'models')))
input_filepath = join(data_directory_path, 'processed')
fX_train = join(f"{input_filepath}", "X_train_scaled.csv")
fy_train = join(f"{input_filepath}", "y_train.csv")
fX_test = join(f"{input_filepath}", "X_test_scaled.csv")
fy_test = join(f"{input_filepath}", "y_test.csv")
default_model_filename = join(models_directory_path, 'trained_LOF_model.pkl')


def normalize_prediction(y: 'np.ndarray') -> 'np.ndarray':
    y[y == 1] = 0
    # y[y == -1] = 1
    return y


def import_dataset(file_path,**kwargs):
    if os.path.exists(file_path):
        return pd.read_csv(file_path, index_col="index", **kwargs)
    else:
        raise FileNotFoundError(f'{file_path} does not exist !')