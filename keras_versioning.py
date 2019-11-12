from tensorflow import keras
from file_versioning import *

def useMethodDecorator(decoratorMethod):
    def applyDecorator(method):
        def realDecorator(self, *args, **kwargs):
            return decoratorMethod(self._auto_save_model__versioner, method)(self, *args, **kwargs)
        return realDecorator
    return applyDecorator

class auto_save_model(keras.models.Model):
    def __init__(self, path="./saved_models/some_model_you_forgot_to_name", *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        if path[-3:] != ".h5":
            path += ".h5"
        self.__versioner = Versioner(path, self, save_function=lambda x, y: x.save(y), load_function = lambda x: keras.models.load_model(x))


    #  @useMethodDecorator(Versioner.auto_save)
    @Versioner.auto_save
    def train(self, *args, **kwargs):
        super().fit(*args, **kwargs)

    @Versioner.auto_save
    def mock_train(self, *args, **kwargs):
        print("training...")

