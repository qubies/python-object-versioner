from file_versioning import *
keras = True


if keras == True:
    from keras_versioning import auto_save_model
    from tensorflow.keras import layers
    from tensorflow import keras

    inputs = keras.Input(shape=(784,), name='digits')
    x = layers.Dense(64, activation='relu', name='dense_1')(inputs)
    x = layers.Dense(64, activation='relu', name='dense_2')(x)
    outputs = layers.Dense(10, activation='softmax', name='predictions')(x)

    ASM = auto_save_model("saved_models/model", inputs=inputs, outputs=outputs, name="test")

stupid__dict = {"some_var":0}
v = Versioner("here/there/hats.pickle", stupid__dict)

@v.auto_save
def increment_a_dict(d, x):
    d["some_var"] = x

for x in range(5):
    if keras:
        ASM.mock_train()
    increment_a_dict(stupid__dict, x)

s = v.load_specific(1,0,2)
print(s)
s = v.load_latest()
print(s)
