import warnings
warnings.filterwarnings("ignore")


def ImageClassifier(image):
    import tensorflow as tf
    from tensorflow import keras
    import numpy as np
    import base64
    import warnings
    warnings.filterwarnings("ignore")

    image_size = (64, 64)

    savedModel = keras.models.load_model('trained_model/')

    print('Model Loaded!')
    print('Image Coded 64: {}'.format(image))
    image_64_decode = base64.b64decode(image)
    print('Image Decoded 64: {}'.format(image_64_decode))

    image_decode_tf = tf.io.decode_image(image_64_decode, channels=3)
    print('Image Decoded TF: {}'.format(image_decode_tf))

    image_final = tf.image.resize(image_decode_tf, method="bilinear", size=image_size)
    print('Image Final: {}'.format(image_final))

    input_array = np.array(image_final)
    print('Input Array: {}'.format(image_final))

    predictions = savedModel.predict(np.expand_dims(input_array, axis=0))
    score = tf.nn.softmax(predictions[0])

    class_names = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    return ("This image most likely belongs to {} with a {:.2f} percent confidence."
            .format(class_names[np.argmax(score)], 100 * np.max(score)))

