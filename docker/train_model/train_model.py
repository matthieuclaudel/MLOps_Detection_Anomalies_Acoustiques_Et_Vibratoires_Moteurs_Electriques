import os
import pandas as pd
#import numpy as np
from sklearn.neighbors import LocalOutlierFactor
from sklearn.metrics import classification_report, accuracy_score, roc_auc_score, matthews_corrcoef, average_precision_score
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix, average_precision_score, precision_score,recall_score,f1_score,roc_curve
import pickle

# Charger les données
def load_data():
    data_train = pd.read_csv('/app/test/data_train.csv', sep=',')
    data_test = pd.read_csv('/app/test/data_test.csv', sep=',')
    return data_train, data_test

# Entraîner et évaluer le modèle
def train_and_evaluate_model():
    X_train, data_test = load_data()        
    X_test = data_test.drop(columns=['target','index'],axis=1)
    y_test = data_test['target']

    best_model = None
    best_score = -float('inf')
    cont = ['auto', 0.01, 0.05, 0.1, 0.25, 0.5]
    neig = [2, 5, 10, 20, 30]
    met = ["cityblock", "minkowski"]

    for m in met:
        for n in neig:
            for c in cont:
                model = LocalOutlierFactor(novelty=True, n_neighbors=n, contamination=c, metric=m, n_jobs=-1)
                model.fit(X_train)
                y_pred = model.predict(X_test)
                y_pred[y_pred == 1] = 0
                y_pred[y_pred == -1] = 1
                #score = (y_pred == y_test).mean()
                n_errors = (y_pred!=y_test.values).sum()
                f1 = 100 * f1_score(y_test, y_pred)
                precision = 100 * precision_score(y_test, y_pred)
                recall = 100 * recall_score(y_test, y_pred)
                roc_auc = 100 * roc_auc_score(y_test, y_pred)
                accuracy = 100 * accuracy_score(y_test, y_pred)
                mcc_score = 100 * matthews_corrcoef(y_test, y_pred)
                cm = confusion_matrix(y_test.values, y_pred=y_pred)
                FN_rate = 100 * (cm[1][0] / (cm[1][0]+cm[1][1]))
                FP_rate = 100 * (cm[0][1] / (cm[0][1]+cm[0][0]))
                Sensibility = 100 * (cm[1][1] / (cm[1][1]+cm[1][0]))
                Specificity = 100 * (cm[0][0] / (cm[0][0]+cm[0][1]))
                
                
                if f1 > best_score:
                    best_score = f1
                    best_nerrors = n_errors
                    best_precision = precision
                    best_recall = recall
                    best_roc_auc = roc_auc
                    best_accuracy = accuracy
                    best_mcc_score = mcc_score
                    best_FN_rate = FN_rate
                    best_FP_rate = FP_rate
                    best_specificity = Specificity
                    best_sensibility = Sensibility
                    best_model = model
                    m_params = m
                    n_params = n
                    c_params = c

    params_dict = {
        'metric': m_params,
        'n_neighbors': n_params,
        'contamination': c_params,
        'novelty': True,
        'n_jobs': -1
    }

    scores_dict = {
        'f1-score': best_score,
        'nerrors': best_nerrors,
        'precision': best_precision,
        'recall': best_recall,
        'roc_auc': best_roc_auc,
        'accuracy': best_accuracy,
        'mcc_score': best_mcc_score,
        'FN_rate': best_FN_rate,
        'FP_rate': best_FP_rate,
        'specificity': best_specificity,
        'sensibility': best_sensibility
    }


    # Enregistrer le meilleur modèle et le score dans un fichier
    with open('/app/test/best_model.pkl', 'wb') as f:
        pickle.dump(best_model, f)
    with open('/app/test/best_score.pkl', 'wb') as f:
        pickle.dump(scores_dict, f)
    with open('/app/test/model_params.pkl', 'wb') as f:
        pickle.dump(params_dict, f)

if __name__ == "__main__":
    train_and_evaluate_model()
