from time import time
start_time = time()
print('Importing packages')
from tkinter import Tk, Frame, Label, Entry, Button, INSERT, Text, IntVar, END
from tkinter.filedialog import askopenfile
from google.cloud import pubsub_v1
import os
import base64
from concurrent.futures import TimeoutError

def main():
    """Publishes multiple messages to a Pub/Sub topic with an error handler."""
    """Reading and Decoding Image"""
    GUI_window = GUI()
    time_0 = time()
    file_path = GUI_window.box_1_fill.get()

    print(file_path)

    with open(file_path, "rb") as image_file:
        encoded_img = base64.b64encode(image_file.read())

    """Publisher"""
    credentials_path = 'image-classifier-project-credentials.json'
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path

    topic_id = "projects/image-classifier-project/topics/IncomingImages"
    publisher = pubsub_v1.PublisherClient()

    data = encoded_img

    message_id = publisher.publish(topic_id, data)
    print(f'Published message id {message_id.result()}')

    """Subscriber"""
    timeout = 70.0
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = 'projects/image-classifier-project/subscriptions/ImageResults-sub'

    def callback(message):
        print(f'Received message')
        print('Result: {}'.format(message.attributes[next(iter(message.attributes))]))
        message.ack()

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f'Listening for messages on {subscription_path}')

    with subscriber:
        try:
            streaming_pull_future.result(timeout=timeout)
            streaming_pull_future.result()
        except TimeoutError:
            streaming_pull_future.cancel()
            streaming_pull_future.result()

    print(f'Wrote excel output in {(time() - time_0):.1f} seconds')


class GUI:
    STANDARD_PADDING = 10
    STANDARD_WIDTH = 50

    def __init__(self):
        self.window = Tk()
        self.window.title('Image Classifier')
        self.row = 0

        # Input 1 row
        self.row += 1

        # Input 1 declaration
        label_1_declare = Frame(master=self.window)
        label_1_declare.grid(row=self.row, column=0, sticky='W', padx=self.STANDARD_PADDING, pady=self.STANDARD_PADDING)
        label_1_text = Label(master=label_1_declare, text="Select a picture to classify:")
        label_1_text.pack(anchor="w")

        # Input 1 file path
        box_1_declare = Frame(master=self.window)
        box_1_declare.grid(row=self.row, column=1, padx=self.STANDARD_PADDING, pady=self.STANDARD_PADDING)
        self.box_1_fill = Entry(master=box_1_declare, width=self.STANDARD_WIDTH)
        self.box_1_fill.pack()

        # Input 1 file button
        button_1_declare = Frame(master=self.window)
        button_1_declare.grid(row=self.row, column=2, padx=self.STANDARD_PADDING, pady=self.STANDARD_PADDING)
        box_1_command = lambda: self.choose_file(self.box_1_fill)
        self.button_1_text = Button(master=button_1_declare, text="Choose file", padx=20, command=box_1_command)
        self.button_1_text.pack()

        # Classify button
        frm_run = Frame(master=self.window)
        frm_run.grid(row=self.row, column=1, padx=self.STANDARD_PADDING, pady=self.STANDARD_PADDING)
        var = IntVar()
        self.btn_run = Button(master=frm_run, text='Classify', width=self.STANDARD_WIDTH - 25, borderwidth=2, command=lambda: var.set(1))
        self.btn_run.pack()
        self.btn_run.wait_variable(var)

    def choose_file(self, entry):
        Tk().withdraw()
        entry.delete(0, END)
        entry.insert(INSERT, askopenfile(filetypes=[('image files', '.png'),('image files', '.jpg')]).name)

    def close_window(self):
        self.window.destroy()

if __name__ == '__main__':
    main()