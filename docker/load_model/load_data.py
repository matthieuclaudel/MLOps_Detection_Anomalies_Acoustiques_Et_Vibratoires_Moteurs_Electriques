import pandas as pd

data_train = pd.read_csv('https://raw.githubusercontent.com/matthieuclaudel/MLOps_Detection_Anomalies_Acoustiques_Et_Vibratoires_Moteurs_Electriques/refs/heads/master/data/raw/DATASET_LIGHT_SCALED.csv', sep=';', decimal=',', index_col=0)

data_train.to_csv('/app/test/data_train.csv', index=False)

data_test = pd.read_csv('https://raw.githubusercontent.com/matthieuclaudel/MLOps_Detection_Anomalies_Acoustiques_Et_Vibratoires_Moteurs_Electriques/refs/heads/master/data/raw/DATASET_VALIDATION_SCALED.csv', sep=';', decimal=',', index_col=0)

data_test.to_csv('/app/test/data_test.csv', index=False)


print(data_train.columns)
print('Data loaded successfully')