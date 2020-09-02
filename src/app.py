from flask import Flask, render_template
from src.common.database import Database
from src.models.fruit import Fruit
from src.models.fact import Fact
from src.database_updater import DatabaseUpdater

app = Flask(__name__)


if app.config["ENV"] == "production":
    app.config.from_object("src.config.ProductionConfig")
else:
    app.config.from_object("src.config.DevelopmentConfig")

print(f'ENV is set to: {app.config["ENV"]}')


def get_database_uri(db_username, db_password, db_server, db_name):
    return "mongodb://{}:{}@{}/{}".format(db_username,
                                          db_password,
                                          db_server,
                                          db_name)


FRUIT_CSV_PATH = app.config["FRUIT_CSV_PATH"]
DB_NAME = app.config["DB_NAME"]
DB_USERNAME = app.config["DB_USERNAME"]
DB_PASSWORD = app.config["DB_PASSWORD"]
DB_SERVER = app.config["DB_SERVER"]
DATABASE_URI = get_database_uri(DB_USERNAME, DB_PASSWORD, DB_SERVER, DB_NAME)

UPDATE_FRUIT_AND_FACTS = app.config["UPDATE_FRUIT_AND_FACTS"]


@app.before_first_request
def initialize_database():
    db_instance = Database.initialize(DATABASE_URI, DB_NAME)
    if UPDATE_FRUIT_AND_FACTS:
        database_updater = DatabaseUpdater(FRUIT_CSV_PATH,
                                           db_instance)
        database_updater.execute()

@app.route('/')
def home_template():
    fruits = Fruit.find_random_sample(5)
    # we need to get 5 facts
    facts = []
    for fruit in fruits:
        query = {'fruit_id': fruit._id, 'fact_true': True}
        fact = Fact.find_one_by_using_query(query)
        facts.append(fact)
    return render_template('home.html', fruits=fruits, facts=facts)

if __name__ == '__main__':
    app.run()
    #app.run(port=5001)
