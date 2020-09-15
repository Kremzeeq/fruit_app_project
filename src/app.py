# noinspection PyUnresolvedReferences,PyUnresolvedReferences
from common.database import Database
# noinspection PyUnresolvedReferences,PyUnresolvedReferences
from models.fruit import Fruit
# noinspection PyUnresolvedReferences,PyUnresolvedReferences
from models.fact import Fact
# noinspection PyUnresolvedReferences,PyUnresolvedReferences
from database_updater import DatabaseUpdater
from flask import Flask, render_template
from waitress import serve
import logging
# noinspection PyUnresolvedReferences
import config
import os


class FruitAppMaker:
    def __init__(self):
        self.app = Flask(__name__)
        self.config_env_set = True

    def execute(self):
        self.set_up_logging()
        self.first_logging_messages()
        self.get_app_mode()
        if self.config_env_set == True:
            if self.get_user_defined_params(self.app.config["DB_USERNAME"],
                                            self.app.config["DB_PASSWORD"],
                                            self.app.config["UPDATE_FRUIT_AND_FACTS"]):
                if self.validate_database_credentials():
                    logging.info("Ready to serve app")
                    return True

    # noinspection SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection
    def set_up_logging(self):
        """
        This sets up logging messages to console and .log file
        """
        logging.basicConfig(filename='fruit_app.log', filemode='w', level=logging.DEBUG,
                            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                            datefmt='%m-%d %H:%M')
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)

    def first_logging_messages(self):
        logging.info("Started running app.py for fruit_app")
        logging.info("Writing log file to fruit_app.log")

    def get_app_mode(self):
        logging.info("Getting app mode")
        self.app.config["ENV"] = os.environ.get("FLASK_ENV")
        if self.app.config["ENV"] == "production":
            self.app.config.from_object(config.ProductionConfig)
        elif self.app.config["ENV"] == "development":
            self.app.config.from_object(config.DevelopmentConfig)
        else:
            self.config_env_set = False
            return logging.error("Please ensure FLASK_ENV is set to 'production' or 'development' "
                                 "\ne.g.: export FLASK_ENV=development")
        logging.info(f'ENV is set to: {self.app.config["ENV"]}')

    def get_user_defined_params(self, db_username, db_password, update_fruit_and_facts):
        """
        Params set here should be defined by the user in the command line
        as per the configuration file. Parameters are passed to the function so
        it can be more easily tested.
        """
        logging.info("Getting User-defined parameters")
        self.db_username = db_username
        self.db_password = db_password
        self.update_fruit_and_facts = update_fruit_and_facts
        user_defined_params_dict = {"DB_USERNAME": self.db_username,
                                    "DB_PASSWORD": self.db_password,
                                    "UPDATE_FRUIT_AND_FACTS": self.update_fruit_and_facts}
        for k, v in user_defined_params_dict.items():
            if v == None or v == "":
                logging.info(f"Here's the value {v}")
                logging.error(f"Please ensure parameter is exported and set for {k} in the command line")
                return False
            if k == "UPDATE_FRUIT_AND_FACTS":
                if v == str(True):
                    self.update_fruit_and_facts = True
                elif v == str(False):
                    self.update_fruit_and_facts = False
                else:
                    logging.error(
                        f"Please ensure UPDATE_FRUIT_AND_FACT is set to 'True' or 'False' in the command line")
                    return False

        logging.info("User parameters have been set")
        return True

    def validate_database_credentials(self):
        """
        Note: port is set to 27017 for localhost. It cannot be written as localhost in the mongo command
        Using subprocess to capture exception instead of os.system
        https://stackoverflow.com/questions/12373563/python-try-block-does-not-catch-os-system-exceptions
        Note this is not the best way to capture the exception. Ideally, we want to capture the
        'exception: login failed' message in the code.
        The mongo command should not be printed to the consolve because it would
        surface the credentials as plain text which has security implications.
        """

        logging.info("Validating database credentials")

        self.db_name = self.app.config["DB_NAME"]
        self.database_uri = f"mongodb://{self.db_username}:" \
                            f"{self.db_password}@" \
                            f"{self.app.config['DB_SERVER']}/" \
                            f"{self.db_name}"
        try:
            Database.ping_client(self.database_uri)
            logging.info("Credentials have been validated")
            return True
        except Exception as e:
            logging.error(e)
            return False


if __name__ == '__main__':
    fruit_app_maker = FruitAppMaker()
    if fruit_app_maker.execute():
        app = fruit_app_maker.app


        @app.before_first_request
        def initialize_database():
            db_instance = Database.initialize(fruit_app_maker.database_uri, fruit_app_maker.db_name)
            if fruit_app_maker.update_fruit_and_facts:
                logging.info("Running database updater")
                database_updater = DatabaseUpdater(fruit_app_maker.
                                                   app.config["FRUIT_CSV_PATH"],
                                                   db_instance)
                database_updater.execute()
                logging.info("Completed running database updater")


        @app.route('/')
        def home_template():
            """
            5 Random facts are fetched from the database for the home page
            """
            fruits = Fruit.find_random_sample(5)
            # we need to get 5 facts
            facts = []
            for fruit in fruits:
                query = {'fruit_id': fruit._id, 'fact_true': True}
                fact = Fact.find_one_by_using_query(query)
                facts.append(fact)
            return render_template('home.html', fruits=fruits, facts=facts)


        logging.info("Serving app")
        serve(app, host=app.config["HOST"], port=app.config["RUN_PORT"])
