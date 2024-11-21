import pytest
from unittest.mock import patch, MagicMock

from data.make_dataset import main

@patch("data.make_dataset.pull_data_with_dvc")
@patch("data.make_dataset.import_dataset")
@patch("data.make_dataset.split_data")
@patch("data.make_dataset.create_folder_if_necessary")
@patch("data.make_dataset.save_dataframes")
@patch("data.make_dataset.sys")
def test_main_success(mock_sys, mock_save_dataframes, mock_create_folder, mock_split_data, 
                      mock_import_dataset, mock_pull_data):
    # Configurer les mocks
    mock_sys.argv = ["make_dataset", "secret_value"]
    mock_pull_data.return_value = "Data pulled successfully"
    mock_import_dataset.return_value = (
        MagicMock(),  # df
        MagicMock(),  # df_ng
    )
    mock_split_data.return_value = (
        MagicMock(),  # X_train
        MagicMock(),  # X_test
        MagicMock(),  # y_train
        MagicMock(),  # y_test
    )

    mock_logger = MagicMock()

    # Appeler la fonction principale
    main()

    # Vérifier que les fonctions externes ont été appelées avec les bons arguments
    mock_pull_data.assert_called_once()
    mock_import_dataset.assert_called_once()
    mock_split_data.assert_called_once()
    mock_create_folder.assert_called_once_with('./data/interim')
    mock_save_dataframes.assert_called_once()

    # Vérifier les retours et le comportement général
    assert mock_pull_data.call_count == 1


@patch("data.make_dataset.modifconfigsecret")
@patch("data.make_dataset.logging.getLogger")
def test_main_modifconfig_error(mock_logger, mock_modifconfig):
    # Configurer les mocks
    mock_modifconfig.side_effect = Exception("Erreur dans modifconfigsecret")
    mock_logger.return_value = MagicMock()

    # Appeler la fonction et vérifier qu'elle gère l'erreur
    with pytest.raises(Exception, match="Erreur dans modifconfigsecret"):
        main()

    # Vérifier que l'erreur est loguée
    mock_logger.return_value.info.assert_any_call("making data set from raw data")
