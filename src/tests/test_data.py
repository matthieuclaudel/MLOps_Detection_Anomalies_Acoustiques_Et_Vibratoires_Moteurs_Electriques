import pytest
from unittest.mock import patch, MagicMock

from src.data.make_dataset import main

@patch("src.data.make_dataset.pull_data_with_dvc")
@patch("src.data.make_dataset.import_dataset")
@patch("src.data.make_dataset.split_data")
@patch("src.data.make_dataset.create_folder_if_necessary")
@patch("src.data.make_dataset.save_dataframes")
@patch("src.data.make_dataset.sys")
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

@patch("src.data.make_dataset.logging.getLogger")  # Ce patch est appliqué EN DERNIER, donc injecté en PREMIER
@patch("src.data.make_dataset.modifconfigsecret")
def test_main_argument_missing_sys_exit(mock_modifconfig, mock_get_logger):
    # Configurer les mocks
    mock_modifconfig.side_effect = Exception("Erreur dans modifconfigsecret")
    mock_logger_instance = MagicMock()
    mock_get_logger.return_value = mock_logger_instance

    # Vérifier que sys.exit est levé lorsqu'il manque un argument
    with pytest.raises(SystemExit) as exc_info:
        main(args=[])
    assert exc_info.value.code == 1  # Vérifier que le code de sortie est 1

    # Vérifier que le logger a logué le message attendu
    mock_logger_instance.info.assert_any_call("Veuillez fournir un paramètre str en argument.")
