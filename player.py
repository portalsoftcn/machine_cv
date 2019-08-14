from tkinter import *
from PIL import Image, ImageTk
from io import BytesIO
import base64

root = Tk()
root.title('测试组python毕业题')

byte_data = base64.b64decode(base64_data)
image_data = BytesIO(byte_data)
img = Image.open(image_data)

img.save("base.jpg")

Label(root, text="Answer:").grid(row=1, column=0, sticky=S + N)

answerEntry = Entry(root)


answerEntry.grid(row=1, column=1)


mainloop()