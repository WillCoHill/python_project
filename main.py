import tkinter as tk
import pytube


class MyGUI:
    def __init__(self):
        self.root = tk.Tk()

        self.root.geometry("800x600")
        self.root.title("YouTube Downloader")

        self.label = tk.Label(self.root, text="YouTube Downloader", font=('Arial', 20))
        self.label.pack(padx=20, pady=20)

        self.textbox = tk.Text(self.root, height=2, font=('Arial', 16))
        self.textbox.pack(padx=10, pady=10)

        self.button = tk.Button(self.root, text='Download', font=('Arial', 18))
        self.button.pack(padx=10, pady=10)
        self.button2 = tk.Button(self.root, text='Delete', font=('Arial', 18))
        self.button2.pack(padx=10, pady=10)

        self.root.mainloop()


MyGUI()
