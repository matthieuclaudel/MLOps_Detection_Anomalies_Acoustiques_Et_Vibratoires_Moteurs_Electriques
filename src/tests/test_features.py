from unittest.mock import patch, MagicMock
import pytest
import pandas as pd
from src.features.build_features import import_dataset
from src.features.build_features import create_folder_if_necessary
from src.features.build_features import save_dataframes
from src.features.build_features import main
import os
@patch("pandas.read_csv")
def test_import_dataset(mock_read_csv):
    # Simuler le comportement de pandas.read_csv
    mock_df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
    mock_read_csv.return_value = mock_df

    # Appeler la fonction import_dataset
    result = import_dataset("dummy_path.csv", index_col="index")

    # Vérifier que pandas.read_csv a été appelé correctement
    mock_read_csv.assert_called_once_with("dummy_path.csv", index_col="index")
    
    # Vérifier que le résultat est bien le DataFrame simulé
    pd.testing.assert_frame_equal(result, mock_df)
