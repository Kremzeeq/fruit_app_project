from pymongo import MongoClient

class Database(object):
    DATABASE = None

    @staticmethod
    def initialize():
        client = MongoClient(host ='localhost', port=27017)
        Database.DATABASE = client['celebration_of_fruit']
        return Database.DATABASE

    @staticmethod
    def drop_collection(collection):
        Database.DATABASE[collection].drop()

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def update(collection, query, data):
        Database.DATABASE[collection].update(query, data, upsert=True)

    @staticmethod
    def insert_many(collection, data):
        Database.DATABASE[collection].insert_many(data)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_and_spec_columns(collection, query, columns):
        return Database.DATABASE[collection].find(query, columns)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def remove(collection, query):
        Database.DATABASE[collection].remove(query)

    @staticmethod
    def delete_id(collection, id):
        Database.DATABASE[collection].delete_one({"id": id})

    @staticmethod
    def find_random(collection, sample_size):
        return Database.DATABASE[collection].aggregate([{"$sample":{"size": sample_size}}])

