from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

root = Tk()
root.title("Text from image extractor")

newline = Label(root)
uploaded_img = Label(root)
scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y)


def extract(path):
    actual_img = cv2.imread(path)
    sample_img = cv2.resize(actual_img, (400, 350))
    image_ht, image_wd, image_thickness = sample_img.shape
    sample_img = cv2.cvtColor(sample_img, cv2.COLOR_BGR2RGB)
    texts = pytesseract.image_to_data(sample_img)
    my_text = ""
    prevy = 0
    for cnt, text in enumerate(texts.splitlines()):
        if cnt == 0:
            continue
        text = text.split()
        if len(text) == 12:
            x, y, w, h = int(text[6]), int(text[7]), int(text[8]), int(text[9])
            if len(my_text) == 0:
                prevy = y
            if prevy - y >= 10 or y - prevy >= 10:
                print(my_text)
                Label(root, text=my_text, font=('consolas', 15, 'bold')).pack()
                my_text = ""
            my_text = my_text + text[11] + " "
            prevy = y
        Label(root, text=my_text, font=('consolas', 15, 'bold')).pack()


def show_extract_button(path):
    extract_btn = Button(root, text="Extract text", command=lambda: extract(path), bg="#2f2f77", fg="gray", pady=15,
                         padx=15, font=('consolas', 15, 'bold'))
    extract_btn.pack()


def upload():
    path = filedialog.askopenfilename()
    image = Image.open(path)
    img = ImageTk.PhotoImage(image)
    uploaded_img.configure(image=img)
    uploaded_img.image = img
    show_extract_button(path)


upload_btn = Button(root, text="Upload an image", command=upload, bg="#2f2f77", fg="gray", height=2, width=20,
                    font=('consolas', 15, 'bold'))
upload_btn.pack()
newline.configure(text='\n')
newline.pack()
uploaded_img.pack()

root.mainloop()
