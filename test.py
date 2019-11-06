from file_versioning import *
keras = False
if keras == True:
    from tensorflow import keras
    from tensorflow.keras import layers

    inputs = keras.Input(shape=(784,), name='digits')
    x = layers.Dense(64, activation='relu', name='dense_1')(inputs)
    x = layers.Dense(64, activation='relu', name='dense_2')(x)
    outputs = layers.Dense(10, activation='softmax', name='predictions')(x)

    model = keras.Model(inputs=inputs, outputs=outputs, name='3_layer_mlp')

    v2 = Versioner("here/there/everywhere.h5", model, save_function=lambda x, y: x.save(y), load_function = lambda x: keras.models.load_model(x))

    @v2.auto_save
    def train_model(x):
        print(f"Pretending to train epoch {x}!!!") 

stupid__dict = {"some_var":0}
v = Versioner("here/there/hats.pickle", stupid__dict)

@v.auto_save
def increment_a_dict(d, x):
    d["some_var"] = x

for x in range(5):
    if keras:
        train_model(x)
    increment_a_dict(stupid__dict, x)

s = v.load_specific(1,0,2)
print(s)
s = v.load_latest()
print(s)
