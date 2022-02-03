from time import time
start_time = time()
print('Importing packages...')
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from tkinter import Tk, Frame, Label, Entry, Button, INSERT, Text, IntVar, END
from tkinter.filedialog import askopenfile
from ImageClassifier import ImageClassifier
import base64

def main():
    """Reading Image"""
    GUI_window = GUI()
    time_0 = time()
    file_path = GUI_window.box_1_fill.get()
    GUI_window.close_window()

    with open(file_path, "rb") as image_file:
        encoded_img = base64.b64encode(image_file.read())

    result = ImageClassifier(encoded_img)
    print(result)


class GUI:
    STANDARD_PADDING = 20
    STANDARD_WIDTH = 40

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
        frm_run.grid(row=self.row, column=3, padx=self.STANDARD_PADDING, pady=self.STANDARD_PADDING)
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
