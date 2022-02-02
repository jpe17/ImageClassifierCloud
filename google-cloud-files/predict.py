from ImageClassifier import ImageClassifier
import base64
import warnings
warnings.filterwarnings("ignore")

"""Reading and Decoding Image"""
with open("01.png", "rb") as image_file:
    data = base64.b64encode(image_file.read())
    print('Data in base 64: {}'.format(data))
    result = ImageClassifier(data)
    print(result)
