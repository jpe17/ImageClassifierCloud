# ImageClassifierCloud
## Uploading any image from the Fashion MNIST test dataset and receiving the predicted label and corresponding accuracy, through a message broker.

Convolutional neural network models are used extensively as the state-of-the-art technique for computer vision tasks like image classification, object detection, image recognition, etc... image. The Fashion MNIST dataset is popularly used for testing such models and its training data was used to train a multi-class image classifier that was constructed for this project. After being pre-trained to make accurate predictions the model was deployed as a machine learning service, such that a client can consume it through the Google Cloud Platform. This is done via Pub/sub, an unified API (message broker) that can receive a stream of requests from a client and return a stream of results back to the same client. The message broker communicates with a Model Server (via cloud-function) where the Machine Learning model is deployed, and publishes the results back to the message broker. The following schematic helps understanding this flow

![Modelo John drawio](https://user-images.githubusercontent.com/58306521/152159267-f94d220d-ee30-4279-9943-f6b44f8d2167.png)

### Requied packages and their versions
* google-cloud-pubsub

### Usage

```
usage: python client.py
