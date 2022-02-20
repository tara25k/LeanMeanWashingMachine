from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np
import os

def tensorModel(imagePath):
    # Load the model
    model = load_model(os.path.abspath('website')+'/'+'keras_model.h5')

    # Create the array of the right shape to feed into the keras model
    # The 'length' or number of images you can put into the array is
    # determined by the first position in the shape tuple, in this case 1.
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    # Replace this with the path to your image
    image = Image.open(imagePath)
    #resize the image to a 224x224 with the same strategy as in TM2:
    #resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    print('a')
    image = ImageOps.fit(image, size, Image.ANTIALIAS)
    #turn the image into a numpy array
    image_array = np.asarray(image)
    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    # Load the image into the array
    data[0] = normalized_image_array

    # run the inference
    prediction = model.predict(data)
    labels = ['washAtOrBelow30', 'washAtOrBelow40', 'doNotBleach', 'tumbleDryMediumTemp', 'ironLowTemp', 'doNotDry', 'doNotTumbleDry', 'doNotIron', 'normalHandWash', 'dripDry', 'tumbleDryLowTemp', 'dryClean', 'ironMediumTemp', 'normalMachineWash', 'Bleach', 'dryFlat']
    newArray = []
    print(prediction)
    prediction = prediction.tolist()
    print(prediction)
    for item in prediction:
        for thing in item:
            thing = float(thing)
            newArray.append(thing)
    print(newArray)
    maxIndex = max(newArray)
    indexOfMax = newArray.index(maxIndex)
    print(labels[indexOfMax])
    prediction = labels[indexOfMax]
    return prediction
