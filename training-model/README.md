# How to Train Multi-class Image Classifier?
## Use the Convolutional Neural Network (CNN) to train an image classifier on your own dataset.

### Steps to train this library on your own dataset

1. Create a folder named *data* with the structure bellow.
```
data/
...class_a/
......a_image_1.jpg
......a_image_2.jpg
...class_b/
......b_image_1.jpg
......b_image_2.jpg
```

2. Replace the folder *data* inside *training-model* by your own pictures.

3. Install the *tensorflow* library using pip.
```
pip install tensorflow
```
4. Execute the script ```trainer.py```.
```
python trainer.py
```

5. The trained model (CNN, weights, biases, etc..) will be stored in *trained_model*
