from flask import Flask, render_template
from src.common.database import Database
from src.models.fruit import Fruit
from src.models.fact import Fact

app = Flask(__name__)

print(app.config["ENV"])

if app.config["ENV"] == "production":
    app.config.from_object("src.config.ProductionConfig")
else:
    app.config.from_object("src.config.DevelopmentConfig")

print(f'ENV is set to: {app.config["ENV"]}')


FRUIT_IMAGES_PATH = "src/static/assets/fruit_images"


@app.before_first_request
def initialize_database():
    Database.initialize()

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
    app.run(port=5001)
