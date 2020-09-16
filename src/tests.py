import app
import pytest
import os
from mockupdb import *
from config import Config
from common.database import Database
from database_updater import DatabaseUpdater


def app_mode_tester(monkeypatch, flask_env_parameter, config_env_set):
    fruit_app_maker = app.FruitAppMaker()
    monkeypatch.setenv("FLASK_ENV", flask_env_parameter)
    fruit_app_maker.get_app_mode()
    assert fruit_app_maker.config_env_set == config_env_set


def test_get_app_mode_dev(monkeypatch):
    flask_env_parameter = "development"
    app_mode_tester(monkeypatch, flask_env_parameter, True)


def test_get_app_mode_dev_caps(monkeypatch):
    flask_env_parameter = "DEVELOPMENT"
    app_mode_tester(monkeypatch, flask_env_parameter, False)


def test_get_app_mode_prod(monkeypatch):
    flask_env_parameter = "production"
    app_mode_tester(monkeypatch, flask_env_parameter, True)


def test_get_app_mode_none(monkeypatch):
    flask_env_parameter = "none"
    app_mode_tester(monkeypatch, flask_env_parameter, False)


def test_get_app_mode_empty_str(monkeypatch):
    flask_env_parameter = ""
    app_mode_tester(monkeypatch, flask_env_parameter, False)


def user_defined_parameter_tester(db_username, db_password, update_fruit_and_facts, expected_bool):
    fruit_app_maker = app.FruitAppMaker()
    assert fruit_app_maker.get_user_defined_params(db_username, db_password, update_fruit_and_facts) == expected_bool


def test_user_defined_params_captured():
    user_defined_parameter_tester("test_username", "test_password", "True", True)


def test_user_defined_params_captured_with_no_username():
    user_defined_parameter_tester("", "test_password", "True", False)


def test_user_defined_params_captured_with_no_password():
    user_defined_parameter_tester("test_username", "", "True", False)


def test_user_defined_params_captured_with_no_update_fruit():
    user_defined_parameter_tester("test_username", "test_password", "", False)


def test_user_defined_params_captured_with_update_fruit_set_to_false():
    user_defined_parameter_tester("test_username", "test_password", "False", True)


def test_fruit_csv_path():
    assert Config.FRUIT_CSV_PATH == "./static/assets/data_source/fruit.csv"


def database_updater_tester():
    server = MockupDB()
    db_instance = Database.initialize(database_uri=server.uri, db_name='test_db')
    fruit_csv_path = "./static/assets/data_source/fruit.csv"
    database_updater = DatabaseUpdater(fruit_csv_path, db_instance)
    return database_updater


def test_database_updater_get_db_name():
    database_updater_instance = database_updater_tester()
    assert database_updater_instance.get_db_name() == 'test_db'


def test_database_updater_execute_fruit_section():
    database_updater_instance = database_updater_tester()
    result = database_updater_instance.execute_fruit_section()
    assert result == True


def test_database_updater_execute_fact_section():
    database_updater_instance = database_updater_tester()
    result = database_updater_instance.execute_fruit_section()
    assert result == True


def test_database_updater_insert_fruit_jsons_in_db_with_wrong_df():
    database_updater_instance = database_updater_tester()
    fruit_df = database_updater_instance.df[['Name', 'Family', 'Fruit image', 'Fruit image reference']].copy()
    result = database_updater_instance.insert_fruit_jsons_in_db(fruit_df)
    assert result == False


def test_database_updater_insert_fact_jsons_in_db_with_wrong_df():
    database_updater_instance = database_updater_tester()
    fruit_df = database_updater_instance.df[['Name', 'Question', 'Answer', 'Source']].copy()
    result = database_updater_instance.insert_fact_jsons_in_db(fruit_df)
    assert result == False


if __name__ == '__main__':
    pytest.main(args=['-s', os.path.abspath(__file__)])
