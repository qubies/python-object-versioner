from tensorflow import keras
from file_versioning import *

class auto_save_model(keras.models.Model):
    def __init__(self, path="./saved_models/some_model_you_forgot_to_name", *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        if path[-3:] != ".h5":
            path += ".h5"
        self.__versioner = Versioner(path, self, save_function=lambda x, y: x.save(y), load_function = lambda x: keras.models.load_model(x, custom_objects={"auto_save_model":auto_save_model}))


    def train(self, *args, **kwargs):
        self.__versioner.auto_save(partial(super().fit, *args, **kwargs))()

    def mock_train(self, *args, **kwargs):
        self.__versioner.auto_save(partial(print,"training...."))()

    def load(self, major=-1, normal=-1, minor=-1):
        if major == -1:
            return self.__versioner.load_latest()
        else:
            return self.__versioner.load_specific(major, normal, minor)

