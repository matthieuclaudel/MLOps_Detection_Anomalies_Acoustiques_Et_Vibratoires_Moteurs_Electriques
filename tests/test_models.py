import pytest

import pickle

import numpy as np
import pandas as pd

from unittest.mock import patch, MagicMock

from models.train_model import (
    normalize_prediction, 
    import_dataset, 
    save_model,
    fit_model
)

def test_normalize_prediction():
    y = np.array([-1, 1, 1, -1])
    y_ref = np.array([-1, 0, 0, -1])

    y_res = normalize_prediction(y)
    assert np.all(y_ref == y_res), "Error in normalize prediction"


@pytest.fixture
def mock_csv_file(tmp_path):
    # Crée un fichier temporaire avec des données CSV fictives
    data = "col1,col2,col3\n1,2,3\n4,5,6"
    file_path = tmp_path / "test_file.csv"
    file_path.write_text(data)
    return str(file_path)


def test_import_dataset_success(mock_csv_file):
    # Teste si le fichier est chargé correctement
    df = import_dataset(mock_csv_file)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert list(df.columns) == ["col1", "col2", "col3"]
    assert df.iloc[0]["col1"] == 1

def test_import_dataset_file_not_found():
    # Teste si une exception est levée pour un fichier inexistant
    with pytest.raises(FileNotFoundError, match=r".*does not exist !"):
        import_dataset("non_existent_file.csv")

def test_import_dataset_with_kwargs(mock_csv_file):
    # Teste si les arguments supplémentaires sont bien passés
    df = import_dataset(mock_csv_file, usecols=["col1", "col2"])
    assert list(df.columns) == ["col1", "col2"]


@pytest.fixture
def mock_model():
    # Fixture pour créer un objet modèle fictif
    return {"param1": 1, "param2": 2}

def test_save_model_success(mock_model, tmp_path):
    # Chemin temporaire pour le fichier du modèle
    model_filename = tmp_path / "test_model.pkl"
    
    # Appeler la fonction pour sauvegarder le modèle
    save_model(model_filename, mock_model)
    
    # Vérifie que le fichier a bien été créé
    assert model_filename.exists()
    
    # Vérifie que le contenu du fichier est correct
    with open(model_filename, "rb") as file:
        loaded_model = pickle.load(file)
        assert loaded_model == mock_model


def test_save_model_invalid_path(mock_model):
    # Test avec un chemin invalide
    invalid_path = "/invalid_path/test_model.pkl"
    
    # Vérifie qu'une exception est levée
    with pytest.raises(OSError):
        save_model(invalid_path, mock_model)


@pytest.fixture
def mock_model_class():
    # Crée une classe modèle simulée
    mock_model = MagicMock()
    mock_model_instance = MagicMock()
    mock_model.return_value = mock_model_instance
    return mock_model

@pytest.fixture
def mock_import_dataset():
    # Simule la fonction `import_dataset`
    with patch("models.train_model.import_dataset") as mock:
        mock.side_effect = [
            [[1, 2], [3, 4]],  # Simule X_train
            [0, 1],  # Simule y_train
        ]
        yield mock

@pytest.fixture
def mock_normalize_prediction():
    # Simule la fonction `normalize_prediction`
    with patch("models.train_model.normalize_prediction") as mock:
        mock.return_value = [0, 1]  # Normalisation des prédictions
        yield mock


def test_fit_model_success(
    mock_model_class,
    mock_import_dataset,
    mock_normalize_prediction,
    # mock_classification_report,
):
    # Paramètres pour le modèle
    params = {"param1": 10, "param2": 20}
    
    # Appeler la fonction à tester
    model = fit_model(mock_model_class, params)
    
    # Vérifie que la classe du modèle est instanciée avec les bons paramètres
    mock_model_class.assert_called_once_with(**params)
    
    # Vérifie que `import_dataset` a été appelé pour X_train et y_train
    assert mock_import_dataset.call_count == 2
    
    # Vérifie que `fit` a été appelé avec les bonnes données
    mock_model_class.return_value.fit.assert_called_once_with([[1, 2], [3, 4]], [0, 1])
    
    # Vérifie que `predict` a été appelé
    mock_model_class.return_value.predict.assert_called_once_with([[1, 2], [3, 4]])
    
    # Vérifie que les prédictions ont été normalisées
    mock_normalize_prediction.assert_called_once_with(mock_model_class.return_value.predict.return_value)
    
    # Vérifie que le modèle est retourné
    assert model == mock_model_class.return_value

def test_fit_model_import_dataset_error(mock_model_class):
    with patch("models.train_model.import_dataset", side_effect=FileNotFoundError("Dataset not found")):
        params = {"param1": 10, "param2": 20}
        with pytest.raises(FileNotFoundError, match="Dataset not found"):
            fit_model(mock_model_class, params)
