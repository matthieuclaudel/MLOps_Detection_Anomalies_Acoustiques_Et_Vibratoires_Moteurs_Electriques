import pandas as pd
import numpy as np
from pathlib import Path
import logging,pickle
from sklearn.preprocessing import StandardScaler
import os,inspect

def main(input_filepath='./data/interim', output_filepath='./data/processed') :
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in../preprocessed).
    """
    global logger
    logger = logging.getLogger(__name__)
    logger.info('making final data set from interim')

    fX_test = f"{input_filepath}/X_test.csv"
    fX_train = f"{input_filepath}/X_train.csv"
    f_ytrain = f"{input_filepath}/y_train.csv"
    f_ytest = f"{input_filepath}/y_test.csv"
    process_data(fX_test, fX_train, output_filepath, f_ytrain,f_ytest)

def process_data(fX_test, fX_train, output_filepath, f_ytrain,f_ytest) :
    # Import datasets
    X_test = import_dataset(fX_test).drop(columns=["moyenne", "ecartype", "mediane", "min", "max"])
    X_train = import_dataset(fX_train).drop(columns=["moyenne", "ecartype", "mediane", "min", "max"])
    y_train = import_dataset(f_ytrain).fillna(10000).astype(int)
    y_test = import_dataset(f_ytest).astype(int)
    # Remplacement des valeurs entre 1 et 99 inclus par -1
    y_test[(y_test>= 1) & (y_test <= 999)] = -1
    y_train[(y_train>= 1) & (y_train <= 999)] = -1
    #StandardScaler
    scaler = StandardScaler()
    print(X_train.head(2))
    X_train_scaled=scaler.fit_transform(X_train)
    X_test_scaled=scaler.transform(X_test)
    model_filename = 'models/trained_SC_model.pkl'
    with open(model_filename, 'wb') as file:
       pickle.dump(scaler, file)
    logger.info('f"Modèle entraîné sauvegardé sous {model_filename}')
    create_folder_if_necessary(output_filepath)

    # Save dataframes to their respective output file paths
    save_dataframes(X_train_scaled, X_test_scaled, output_filepath, y_train, y_test)

def import_dataset(file_path, **kwargs) :    
    logger = logging.getLogger(inspect.currentframe().f_code.co_name)
    logger.info(f'Import {file_path}')
    return pd.read_csv(file_path, **kwargs)

def create_folder_if_necessary(output_folderpath) :
    logger = logging.getLogger(inspect.currentframe().f_code.co_name)
    logger.info('create_folder_if_necessary')
    # Create folder if necessary
    if os.path.exists(output_folderpath)==False:
        os.makedirs(output_folderpath)

def save_dataframes(X_train_scaled, X_test_scaled, output_folderpath, y_train,y_test) :
    logger = logging.getLogger(inspect.currentframe().f_code.co_name)
    logger.info('save dataframes')
    # Save dataframes to their respective output file paths
    for file, filename in zip([X_train_scaled, X_test_scaled, y_train,y_test], ['X_train_scaled', 'X_test_scaled','y_train','y_test']) :
        output_filepath = os.path.join(output_folderpath, f'{filename}.csv')
        #file.to_csv(output_filepath, index=False)
        np.savetxt(output_filepath, file, delimiter=",")
    for file, filename in zip([y_train,y_test], ['y_train','y_test']) :
        output_filepath = os.path.join(output_folderpath, f'{filename}.csv')
        file.to_csv(output_filepath, index=False)
        
if __name__ == '__main__' :
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    main()    