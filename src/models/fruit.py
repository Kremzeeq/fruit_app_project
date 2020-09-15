import uuid
from .model import Model


class Fruit(Model):
    collection = 'fruits'

    def __init__(self, **kwargs):
        super().__init__()
        """
        Fruit have a one to many relationship with the Fact model
        fruit_name: name of the fruit
        plant_family: the taxonomical family for the fruit
        fruit_image_path: the path for where the fruit image is stored
        image_source: the source for the image
        Note: 
        The source for the image should be displayed below images for the fruit
        in the front-end application.
        The fruit images are stored here: "src/static/assets/fruit_images"
        """
        self.fruit_name = kwargs.get('fruit_name')
        self.plant_family = kwargs.get('plant_family')
        self.fruit_image_path = kwargs.get('fruit_image_path')
        self.image_source = kwargs.get('image_source')
        self._id = uuid.uuid4().hex if kwargs.get('_id') is None else kwargs.get('_id')

    def json(self):
        return {"fruit_name": self.fruit_name,
                "plant_family": self.plant_family,
                "fruit_image_path": self.fruit_image_path,
                "image_source": self.image_source,
                "_id": self._id
                }
