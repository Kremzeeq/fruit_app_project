from src.common.database import Database
from src.models.fruit import Fruit
from src.models.fact import Fact
import pandas as pd
import json


class DatabaseUpdater():
    """
    This class reads a CSV from the fruit_csv_path location
    and converts this to a pandas dataframe.
    The CSV contains tabular information for fruits and facts.
    This information is split between different dataframes.
    The dataframes are converted to json format as per required
    by the fact and fruit models saved here: src/models
    They are then saved to the database.
    """
    def __init__(self, fruit_csv_path):
        self.fruit_csv_path = fruit_csv_path
        self.df = pd.read_csv(self.fruit_csv_path)

    def execute(self):
        result_dict = self.get_db_connection_result_dict()
        if result_dict["success"]:
            self.delete_collections_in_db(result_dict['result'])
            if self.execute_fruit_section():
                if self.execute_fact_section():
                    self.final_notifcations()


    def get_db_connection_result_dict(self):
        try:
            db = Database.initialize()
            print("Initialized database:", db.name)
            return {"result": db, "success":True}
        except Exception as e:
            print("Error:", e)
            return {"success": False}

    def delete_collections_in_db(self, db):
        collection_names = db.list_collection_names()
        print("Here are existing collections:", collection_names)
        for collection in collection_names:
            db.drop_collection(collection)
            print("Dropped collection:", collection)
        return True


    def execute_fruit_section(self):
        fruit_df = self.get_fruit_df()
        return self.insert_fruit_jsons_in_db(fruit_df)

    def execute_fact_section(self):
        fact_df = self.get_fact_df()
        return self.insert_fact_jsons_in_db(fact_df)


    def get_fruit_df(self):
        """
        This produces a dataframe needed
        for the fruit model
        """
        fruit_df = self.df[['Name', 'Family', 'Fruit image', 'Fruit image reference']].copy()
        fruit_df.columns = ['fruit_name', 'plant_family', 'fruit_image_path', 'image_source']
        return fruit_df

    def insert_fruit_jsons_in_db(self, fruit_df):
            list_of_fruit_jsons = json.loads(fruit_df.to_json(orient="records"))
            print("Writing Fruit collection to database")
            try:
                for fruit_json in list_of_fruit_jsons:
                    fruit = Fruit(**fruit_json)
                    fruit.save_to_mongo()
                print("Fruit collection written to database")
                return True
            except Exception as e:
                print("Problem writing fruit collection to database")
                print("Error:", e)
                return False

    def get_fact_df(self):
        """
        This produces a dataframe needed
        for the fact model
        """
        fact_df_p1 = self.df[['Name', 'Question', 'Answer', 'Source']].copy()
        fact_df_p2 = self.df[['Name', 'Fact', 'Source']].copy()
        fact_df_p2['Fact'].rename('Question', inplace=True)

        fact_df_p2.rename(columns = {'Fact':'Question'}, inplace=True)
        fact_df_p2['Answer'] = True
        fact_df = pd.concat([fact_df_p1, fact_df_p2])
        fact_df.columns = ['fruit_name', 'fact_text', 'fact_true', 'fact_source']
        return fact_df

    def insert_fact_jsons_in_db(self, fact_df):
        list_of_fact_jsons = json.loads(fact_df.to_json(orient="records"))
        print("Writing Fact collection to database")
        try:
            for fact_json in list_of_fact_jsons:
                fruit_name = fact_json['fruit_name']
                fruit = Fruit.find_one_by('fruit_name', fruit_name)
                fruit_id = fruit._id
                fact_json['fruit_id'] = fruit_id
                fact = Fact(**fact_json)
                fact.save_to_mongo()
            print("Fact collection written to database")
            return True
        except Exception as e:
            print("Problem writing fact collection to database")
            print("Error:", e)
            return False

    def final_notifcations(self):
        print("Database update complete")
        print("New fruit and facts can be added to the CSV file:", self.fruit_csv_path)
        print("Afterwards this updater can be run to overwrite the database collections"
              " for the database configured for the project")


FRUIT_CSV = './static/assets/data_source/fruit.csv'
database_updater = DatabaseUpdater(FRUIT_CSV)
database_updater.execute()