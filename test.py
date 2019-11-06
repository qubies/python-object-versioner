from file_versioning import *
from tensorflow import keras
from tensorflow.keras import layers

inputs = keras.Input(shape=(784,), name='digits')
x = layers.Dense(64, activation='relu', name='dense_1')(inputs)
x = layers.Dense(64, activation='relu', name='dense_2')(x)
outputs = layers.Dense(10, activation='softmax', name='predictions')(x)

model = keras.Model(inputs=inputs, outputs=outputs, name='3_layer_mlp')
stupid__dict = {"hats":0}

v = Versioner("here/there/hats.pickle", stupid__dict)
v2 = Versioner("here/there/everywhere.h5", model, save_function=lambda x, y: x.save(y), load_function = lambda x: keras.models.load_model(x))

@v2.auto_save
def train_model(x):
    print(f"Pretending to train epoch {x}!!!") 

@v.auto_save
def increment_a_dict(d, x):
    d["hats"] = x

for x in range(5):
    train(x)
    increment_a_dict(stupid__dict, x)

s = v.load_specific(1,0,2)
print(s)
s = v.load_latest()
print(s)
