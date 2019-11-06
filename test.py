from file_versioning import *
from tensorflow import keras
from tensorflow.keras import layers

inputs = keras.Input(shape=(784,), name='digits')
x = layers.Dense(64, activation='relu', name='dense_1')(inputs)
x = layers.Dense(64, activation='relu', name='dense_2')(x)
outputs = layers.Dense(10, activation='softmax', name='predictions')(x)

model = keras.Model(inputs=inputs, outputs=outputs, name='3_layer_mlp')
stupid__dict = {"hats":0}

v = Versioner("here/there/everywhere.h5", model, save_function=lambda x, y: x.save(y), load_function = lambda x: keras.models.load_model(x))
for x in range(5):
    stupid__dict["ver"] = x
    v.minor_increment_save()
v.normal_increment_save()
for x in range(5):
    v.minor_increment_save()
v.major_increment_save()
for x in range(5):
    v.minor_increment_save()
v.normal_increment_save()
for x in range(5):
    v.minor_increment_save()

s = v.load_specific(1,0,2)
s = v.load_latest()
print(s)
