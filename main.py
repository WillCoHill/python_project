import tkinter as tk
from io import BytesIO
from tkinter import *


import requests
import tkinter.filedialog
import validators
from PIL import Image, ImageTk
from pytube import YouTube


class MyGUI:
    def __init__(self):
        self.img = Image.new("RGB", (800, 1280), (255, 255, 255))
        self.root = tk.Tk()

        self.root.geometry("800x600")
        self.root.title("YouTube Downloader")
        self.root.configure(background='#fff')

        self.label = tk.Label(self.root, text="YouTube Downloader", bg='red', font=('Arial', 20))
        self.label.pack(padx=20, pady=20)

        self.canvas = tk.Canvas(self.root, width=300, height=300)
        self.canvas.pack()

        self.title_text = tk.Label(self.root, height=1, width=65)
        self.title_text.pack()

        self.label = tk.Label(self.root, font=('Arial', 18))
        self.label.pack()
        #img = PhotoImage(file="ball.ppm")
        #canvas.create_image(20, 20, anchor=NW, image=img)

        self.url_state = tk.StringVar(self.root, value="")
        self.check_state = tk.IntVar()

        self.checkBox = tk.Checkbutton(self.root, text="Audio only?", font=('Arial', 16), variable=self.check_state)
        self.checkBox.pack()

        self.input_textbox = tk.Text(self.root, height=1, width=65, font=('Arial', 16))
        self.input_textbox.insert(tk.END, "URL goes here")
        self.input_textbox.pack(padx=10, pady=10)

        self.output_textbox = tk.Text(self.root, height=1, width=65)
        self.output_textbox.pack(padx=10, pady=10)

        self.frame = tk.Frame(self.root)
        self.frame.pack()

        self.MyText = tk.StringVar(self.root, value="")

        #self.dirLabel = tk.Label(self.root, font=('Arial', 20))
        #self.dirLabel.pack()

        self.button = tk.Button(self.root, text='Download', bg='#ADD8E6', font=('Arial', 16), command=self.show_url)
        self.button.pack(side=tk.LEFT, padx=10, pady=10)
        #self.buttonC = tk.Button(self.root, text='Dark Mode', font=('Arial', 18), command=self.show_url)
        #self.buttonC.pack(side=tk.BOTTOM)
        self.button2 = tk.Button(self.root, text='Browse', bg='#ADD8E6', font=('Arial', 16), command=self.displayDir)
        self.button2.pack(side=tk.RIGHT, padx=10, pady=10)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def show_url(self):
        if self.input_textbox.get('1.0', tk.END):
            self.output_textbox.delete('1.0', tk.END)
            self.url_state = self.input_textbox.get('1.0', tk.END)
            print(self.url_state)
            self.output_textbox.insert(tk.END, ('Video downloaded to ' + str(self.MyText)))
            if type(validators.url(self.url_state)):
                yt = YouTube(self.url_state)
                #print(yt.thumbnail_url)
                self.title_text.config(text=yt.title)
                response = requests.get(yt.thumbnail_url)
                im = Image.open(BytesIO(response.content))
                ph = ImageTk.PhotoImage(im)
                self.label.image = ph
                self.canvas.create_image(275, 275, image=ph, anchor="center")
                if self.output_textbox.get('1.0', tk.END) != '':
                    self.title_text.config(text="Downloading...")
                    if self.check_state.get() == 1:
                        ytStream = yt.streams.filter(only_audio=True).first().download(self.MyText)
                    else:
                        ytStream = yt.streams.get_lowest_resolution().download(self.MyText)
                    #ytStream.download(self.MyText)
                    self.title_text.config(text=("Downloaded to " + self.MyText))
                else:
                    self.title_text.config(text="Invalid URL")
                    print("Invalid URL")

    def on_closing(self):
        if tk.messagebox.askyesno(title="Quit?", message="Are you really trying to quit?"):
            self.root.destroy()

    def displayDir(self):
        filename = tkinter.filedialog.askdirectory()
        #tkinter.pathlabel.config(text=filename)
        self.MyText = filename
        self.output_textbox.insert(tk.END, filename)


MyGUI()
