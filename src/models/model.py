from abc import ABCMeta, abstractmethod
from common.database import Database

class Model(metaclass=ABCMeta):
    collection: str
    _id: str

    def __init__(self, *args, **kwargs):
        pass

    def save_to_mongo(self):
        Database.insert(self.collection, self.json())

    def update_mongo(self):
        Database.update(self.collection,
                        {"_id": self._id},
                        self.json())

    def remove_from_mongo(self):
        Database.remove(self.collection, {"_id": self._id})

    @classmethod
    def get_by_id(cls, _id):
        return cls.find_one_by("_id", _id)

    @abstractmethod
    def json(self):
        raise NotImplementedError

    @classmethod
    def all(cls):
        elems_from_db = Database.find(cls.collection, {})
        return [cls(**elem) for elem in elems_from_db]

    @classmethod
    def find_one_by(cls, attribute, value):
        return cls(**Database.find_one(cls.collection, {attribute:value}))

    @classmethod
    def find_one_by_using_query(cls, query):
        return cls(**Database.find_one(cls.collection, query))

    @classmethod
    def find_many_by(cls, attribute, value):
        return [cls(*elem) for elem in Database.find(cls.collection, {attribute:value})]

    def find_multiple(cls, query):
        return Database.find(cls.collection, query)

    @classmethod
    def find_random_sample(cls, sample_size):
        elems_from_db = Database.find_random(cls.collection, sample_size)
        return [cls(**elem) for elem in elems_from_db]