import uuid
from .model import Model


class Fact(Model):
    collection = 'facts'

    def __init__(self, **kwargs):
        super().__init__()
        """
        Fact model has a many to one relationship with the Fruit model
        fact_text: text relating to the fact related to a fruit
        fact_true: indicates if the fact is correct
        fact_source: the source of the fact. Typically a wikipedia page for ease. 
        fruit_id: the id for the related fruit model
        Note: if the fact is false, the false fact has been derived from 
        applying logic to the source, to decide that it is indeed a false fact.
        """
        self.fact_text = kwargs.get('fact_text')
        self.fact_true = kwargs.get('fact_true')
        self.fact_source = kwargs.get('fact_source')
        self.fruit_id = kwargs.get('fruit_id')
        self._id = uuid.uuid4().hex if kwargs.get('_id') is None else kwargs.get('_id')

    def json(self):
        return {"fact_text": self.fact_text,
                "fact_true": self.fact_true,
                "fact_source": self.fact_source,
                "fruit_id": self.fruit_id,
                "_id": self._id
                }
