import time
import sys
import tkinter as tk
import tracemalloc
from io import BytesIO
from tkinter import *
import socket
import asyncio
import random

import requests
import tkinter.filedialog
import validators
from PIL import Image, ImageTk
from pytube import YouTube
from pytube.exceptions import VideoUnavailable

#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.connect((socket.gethostname(), 1234))

tracemalloc.start()

weather_master = ''
def get_weather ():
    global weather_master
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((socket.gethostname(), 1234))

    ret_val = ''
    ret_val += s.recv(1024).decode("utf-8")
    weather_master += ret_val

try:
    get_weather()
except:
    weather_master += 'The socket was unable to connect'


class MyGUI:
    def __init__(self):
        self.img = Image.new("RGB", (800, 1280), (255, 255, 255))
        self.root = tk.Tk()

        self.root.geometry("800x600")
        self.root.title("YouTube Downloader")
        self.root.configure(background='#fff')

        self.label = tk.Label(self.root, text="YouTube Downloader", bg='red', font=('Arial', 20))
        self.label.pack(padx=5, pady=5)

        self.canvas = tk.Canvas(self.root, width=300, height=200)
        self.canvas.pack()

        self.title_text = tk.Label(self.root, height=1, width=65)
        self.title_text.pack()

        self.label = tk.Label(self.root, width=0, height=0, font=('Arial', 16))
        self.label.pack()
        # img = PhotoImage(file="ball.ppm")
        # canvas.create_image(20, 20, anchor=NW, image=img)

        self.url_state = tk.StringVar(self.root, value="")
        self.check_state = tk.IntVar()

        self.checkBox = tk.Checkbutton(self.root, text="Audio only?", font=('Arial', 16), variable=self.check_state)
        self.checkBox.pack()

        self.input_textbox = tk.Text(self.root, height=1, width=65, font=('Arial', 16))
        self.input_textbox.insert(tk.END, "URL goes here")
        self.input_textbox.pack(padx=10, pady=10)

        self.output_textbox = tk.Text(self.root, height=1, width=65)
        self.output_textbox.pack(padx=10, pady=10)

        self.weather_box = tk.Label(self.root, text=weather_master, height=1, width=65, font=('Arial', 16))
        self.weather_box.pack(padx=10, pady=10)

        self.frame = tk.Frame(self.root)
        self.frame.pack()

        self.MyText = tk.StringVar(self.root, value="")

        # self.dirLabel = tk.Label(self.root, font=('Arial', 20))
        # self.dirLabel.pack()

        self.buttons_frame = tk.Frame(self.root)
        self.button = tk.Button(self.buttons_frame, text='Download', bg='#5CDB5C', font=('Arial', 16), command=self.show_url)
        self.button.pack(side=tk.LEFT, padx=10, pady=2)
        self.buttonC = tk.Button(self.buttons_frame, text='Reconnect', bg='#ffa500', font=('Arial', 16), command=self.try_reconnect)
        self.buttonC.pack(side=tk.LEFT, padx=10, pady=2)
        self.button2 = tk.Button(self.buttons_frame, text='Browse', bg='#5A66FF', font=('Arial', 16), command=self.displayDir)
        self.button2.pack(side=tk.LEFT, padx=10, pady=2)
        self.buttons_frame.pack()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def show_url(self):
        if self.input_textbox.get('1.0', tk.END):
            self.output_textbox.delete('1.0', tk.END)
            self.url_state = self.input_textbox.get('1.0', tk.END)
            print(self.url_state)
            self.output_textbox.insert(tk.END, ('File downloading to ' + str(self.MyText)))
            if validators.url(self.url_state):
                yt = YouTube(self.url_state)
                # print(f'Video {self.MyText} is unavaialable, skipping.')
                # print(yt.thumbnail_url)
                self.title_text.config(text=yt.title)
                response = requests.get(yt.thumbnail_url)
                im = Image.open(BytesIO(response.content))
                im_resize = im.resize((200, 300))
                ph = ImageTk.PhotoImage(im_resize)
                self.label.image = ph
                self.canvas.create_image(200, 300, image=ph, anchor='center')
                if self.output_textbox.get('1.0', tk.END) != '':
                    self.title_text.config(text="Downloading...")
                    print(self.check_state.get())
                    print(self.MyText)
                    if self.check_state.get() == 1:
                        yt.streams.filter(only_audio=True).first().download(self.MyText)
                    elif self.check_state.get() == 0:
                        yt.streams.get_lowest_resolution().download(self.MyText)
                    # ytStream.download(self.MyText)
                    self.title_text.config(text=("Downloaded to " + self.MyText))
                else:
                    self.title_text.config(text="Invalid URL")
                    print("Invalid URL")
            else:
                self.title_text.config(text="Invalid URL")
                print("Invalid URL")

    def on_closing(self):
        if tk.messagebox.askyesno(title="Quit?", message="Are you really trying to quit?"):
            self.root.destroy()

    def connect(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ret_val = ''
        s.connect((socket.gethostname(), 1234))
        ret_val += s.recv(1024).decode("utf-8")
        self.weather_box.config(text=ret_val)

    def try_reconnect(self):
        tried = 0
        while tried < 3:
            try:
                self.connect()
                break
            except:
                print("unable to connect")
                tried += 1
                time.sleep(0.2)
                if tried >= 3:
                    print("Run the weather server to get data")
                    self.weather_box.config(text="Can't connect to weather; reestablish connection")


    def displayDir(self):
        filename = tkinter.filedialog.askdirectory()
        # tkinter.pathlabel.config(text=filename)
        self.MyText = filename
        self.output_textbox.insert(tk.END, filename)


MyGUI()
