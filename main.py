import customtkinter
import tkinter
from tkinter import messagebox
import os
from PIL import Image
from tkinter import filedialog
from data_download import DataDownload
import json
import threading

MAIN_COLOR = "#36007e"
SCND_COLOR = "#7f19ff"
WHITE_COLOR = "#FFFFFF"
BLACK_COLOR = "#000000"
FG_COLOR = "#DADADA"


class YfinanceGUI:

    customtkinter.set_appearance_mode("System")
    customtkinter.set_default_color_theme("blue")

    def __init__(self, app):

        self.app = app
        self.app.title("Yahoo finance OHLC downloader")
        self.app.geometry("{}x{}+{}+{}".format(570, 570, 750, 250))
        self.app.resizable(False, True)
        self.app.iconbitmap("images/icon.ico")

        self.t = 0
        self.added_elements = []

        self.logo = customtkinter.CTkImage(
            light_image=Image.open("images/yfinance logo.png"), size=(100, 40)
        )
        self.plus = customtkinter.CTkImage(
            light_image=Image.open("images/add_ticker.png"), size=(30, 30)
        )
        self.minus = customtkinter.CTkImage(
            light_image=Image.open("images/delete_ticker.png"), size=(30, 30)
        )

        self.app.grid_rowconfigure(0, weight=1)
        self.app.grid_columnconfigure(0, weight=1)

        #  Creating scrollable frame
        self.frame = customtkinter.CTkFrame(master=self.app)
        self.frame.grid(row=0, column=0, padx=15, pady=(15, 5), sticky="NSEW")

        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        self.canvas = customtkinter.CTkCanvas(
            master=self.frame, highlightbackground=FG_COLOR, highlightthickness=0
        )
        self.canvas.grid(row=0, column=0, sticky="NSEW")

        self.canvas.grid_rowconfigure(0, weight=1)
        self.canvas.grid_columnconfigure(0, weight=1)

        self.frame_1 = customtkinter.CTkFrame(master=self.canvas, fg_color=FG_COLOR)

        self.scrollbar = customtkinter.CTkScrollbar(
            master=self.frame,
            orientation="vertical",
            command=self.canvas.yview,
            height=570,
            width=15,
            button_color=MAIN_COLOR,
            button_hover_color=SCND_COLOR,
        )

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        self.window = self.canvas.create_window(
            (0, 0), window=self.frame_1, anchor="nw", height=440
        )

        #  Creating elements of scrollable frame
        self.label_1 = customtkinter.CTkLabel(
            master=self.frame_1, text="", image=self.logo, justify=tkinter.LEFT
        )
        self.label_1.grid(row=1, column=1, padx=10, pady=10, sticky="N")

        self.create_entry("")

        self.create_combobox_2("Interval")

        self.create_combobox_1("Period")

        self.entry_list = [
            {
                "Ticker": self.entry_1,
                "Period": self.combobox_1,
                "Interval": self.combobox_2,
            }
        ]

        self.add_ticker_button = customtkinter.CTkButton(
            master=self.frame_1,
            text="",
            image=self.plus,
            command=self.add_ticker,
            fg_color="transparent",
            hover_color=FG_COLOR,
            width=1,
            height=1,
        )
        self.add_ticker_button.grid(row=2, column=3, padx=5, pady=10, sticky="w")

        self.delete_ticker_button = customtkinter.CTkButton(
            master=self.frame_1,
            text="",
            image=self.minus,
            command=self.delete_ticker,
            fg_color="transparent",
            hover_color=FG_COLOR,
            width=1,
            height=1,
        )
        self.delete_ticker_button.grid(row=3, column=3, padx=5, pady=10, sticky="w")

        #  Creating frame_2 and its elements

        self.frame_2 = customtkinter.CTkFrame(master=self.app, fg_color=FG_COLOR)
        self.frame_2.grid(row=1, column=0, columnspan=3, padx=15, pady=0, sticky="NSEW")

        self.add_folder_button = customtkinter.CTkButton(
            master=self.frame_2,
            text="Select destination",
            command=self.add_folder,
            fg_color=MAIN_COLOR,
            hover_color=SCND_COLOR,
        )
        self.add_folder_button.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.label_2 = customtkinter.CTkLabel(
            master=self.frame_2,
            text="No folder selected yet",
            justify=tkinter.LEFT,
            width=1,
        )
        self.label_2.grid(row=3, column=0, columnspan=3, padx=10, pady=5, sticky="NSEW")

        self.check_box = customtkinter.CTkCheckBox(
            master=self.frame_2,
            text="Create excel file",
            fg_color=MAIN_COLOR,
            hover_color=SCND_COLOR,
        )
        self.check_box.grid(row=2, column=1, padx=10, pady=15, sticky="E")

        self.load_last_button = customtkinter.CTkButton(
            master=self.frame_2,
            text="Load last set",
            command=self.load_last,
            fg_color=MAIN_COLOR,
            hover_color=SCND_COLOR,
        )
        self.load_last_button.grid(row=1, column=0, padx=10, pady=10)

        self.save_set_button = customtkinter.CTkButton(
            master=self.frame_2,
            text="Save set",
            command=self.save_set,
            fg_color=MAIN_COLOR,
            hover_color=SCND_COLOR,
        )
        self.save_set_button.grid(row=1, column=1, padx=10, pady=10)

        self.load_set_button = customtkinter.CTkButton(
            master=self.frame_2,
            text="Load set",
            command=self.load_set,
            fg_color=MAIN_COLOR,
            hover_color=SCND_COLOR,
        )
        self.load_set_button.grid(row=1, column=2, padx=10, pady=10)

        #  Creating frame_3 and its elements
        self.frame_3 = customtkinter.CTkFrame(master=self.app, fg_color=FG_COLOR)
        self.frame_3.grid(
            row=2, column=0, columnspan=3, padx=15, pady=(5, 15), sticky="NSEW"
        )

        #  This button is only for creating a space and making "Start" button centered
        self.space_button = customtkinter.CTkButton(
            master=self.frame_3,
            text="",
            state="disabled",
            fg_color="transparent",
            hover_color=FG_COLOR,
        )
        self.space_button.grid(row=1, column=0, padx=10, pady=5, sticky="NSEW")

        self.start_button = customtkinter.CTkButton(
            master=self.frame_3,
            text="Start",
            command=lambda: threading.Thread(target=self.button_callback).start(),
            fg_color=MAIN_COLOR,
            hover_color=SCND_COLOR,
        )
        self.start_button.grid(row=1, column=1, padx=10, pady=10, sticky="NSEW")

        #  Adding label informing about script status
        self.status = customtkinter.CTkLabel(
            master=self.frame_3, text="Preparing data...", font=("CTkDefaultFont", 12)
        )

    def add_ticker(self):
        """Adding row with ticker entry and interval & period optionboxes"""

        self.t = self.t + 1

        self.create_entry("")

        self.interval = self.combobox_2.get()
        self.create_combobox_2(self.interval)
        self.added_elements.append(self.combobox_2)

        self.period = self.combobox_1.get()
        self.create_combobox_1(self.period)
        self.added_elements.append(self.combobox_1)

        self.entry_dir = {
            "Ticker": self.entry_1,
            "Period": self.combobox_1,
            "Interval": self.combobox_2,
        }
        self.entry_list.append(self.entry_dir)

        self.check_canvas()

    def delete_ticker(self):
        """Deleting last added row with ticker entry and interval & period optionboxes"""
        self.row_of_elements = self.added_elements[-3:]
        self.added_elements = self.added_elements[:-3]
        for element in self.row_of_elements:
            element.grid_forget()
        self.t -= 1
        self.entry_list.pop(-1)

        self.check_canvas()

    def add_folder(self):
        """Selection of the folder where the data will be saved"""

        path = filedialog.askdirectory()
        self.label_2.configure(text=path, width=1)

    def button_callback(self):
        """Operations performed when the start button is pressed: downloading and saving data"""

        for pos in self.entry_list:
            print(pos["Ticker"].get())

        for pos in self.entry_list:
            if pos["Ticker"].get() == "":
                return messagebox.showerror(
                    "Empty entry", "One of ticker entry is empty!"
                )

            elif pos["Interval"].get() == "Interval":
                return messagebox.showerror(
                    "Interval error", "Interval is not selected!"
                )
            elif pos["Period"].get() == "Period":
                return messagebox.showerror("Period error", "Period is not selected!")
            elif self.label_2.cget("text") == "No folder selected yet":
                return messagebox.showerror(
                    "Destination error", "Destination folder is not selected!"
                )
        if self.check_box.get() == 0:
            result = messagebox.askyesno(
                "Excel file not selected",
                "Are you sure you want to start without creating excel files for your data?",
            )
            if result == 0:
                return

        self.start_button.configure(state="disabled")
        self.status.grid(row=2, column=1, padx=10, pady=0, sticky="NSEW")
        self.values_list = []
        for x in self.entry_list:
            x = {
                "Ticker": x["Ticker"].get(),
                "Period": x["Period"].get(),
                "Interval": x["Interval"].get(),
            }
            self.values_list.append(x)

        #  Save set to be able to load it next time
        with open("last_set.json", "w") as file:
            json.dump(self.values_list, file)
        self.data_download = DataDownload(self.values_list, self.label_2.cget("text"))
        self.data_download.csv_data(self.check_box.get(), self.status)
        if len(self.values_list) == 1:
            tkinter.messagebox.showinfo(
                "End Message", f"Downloading 1 file is done. Data is ready."
            )
        else:
            tkinter.messagebox.showinfo(
                "End Message",
                f"Downloading {len(self.values_list)} files is done. Data is ready.",
            )
        self.start_button.configure(state="normal")
        self.status.grid_forget()

    def load_last(self):
        """Loading a previously used set of tickers"""

        for x in self.added_elements:
            x.grid_forget()

        self.t = 0
        self.added_elements = []
        self.set_list = []

        with open("last_set.json", "r") as file:
            self.set_list = json.load(file)
            for position in self.set_list:
                ticker = tkinter.StringVar(self.app, value=position["Ticker"])
                self.create_entry(ticker)
                self.added_elements.append(self.entry_1)

                self.create_combobox_2(position["Interval"])
                self.added_elements.append(self.combobox_2)

                self.create_combobox_1(position["Period"])
                self.added_elements.append(self.combobox_1)

                self.entry_dir = {
                    "Ticker": self.entry_1,
                    "Period": self.combobox_1,
                    "Interval": self.combobox_2,
                }
                self.entry_list.append(self.entry_dir)
                self.t += 1

                self.check_canvas()

    def save_set(self):
        """Saving current set of tickers"""

        self.values_list = []
        for x in self.entry_list:
            x = {
                "Ticker": x["Ticker"].get(),
                "Period": x["Period"].get(),
                "Interval": x["Interval"].get(),
            }
            self.values_list.append(x)

        file_path = filedialog.asksaveasfilename(
            defaultextension=".json", filetypes=[("JSON Files", "*.json")]
        )
        with open(file_path, "w") as file:
            json.dump(self.values_list, file)

    def load_set(self):
        """Loading set of tickers from .json file"""

        for x in self.added_elements:
            x.grid_forget()

        self.t = 0
        self.added_elements = []
        self.set_list = []
        self.entry_list = []
        self.entry_dir = []

        file_path = filedialog.askopenfilename(
            defaultextension=".json", filetypes=[("JSON Files", "*.json")]
        )

        with open(file_path, "r") as file:
            self.set_list = json.load(file)

            for position in self.set_list:
                ticker = tkinter.StringVar(self.app, value=position["Ticker"])
                self.create_entry(ticker)
                self.added_elements.append(self.entry_1)

                self.create_combobox_2(position["Interval"])
                self.added_elements.append(self.combobox_2)

                self.create_combobox_1(position["Period"])
                self.added_elements.append(self.combobox_1)

                self.entry_dir = {
                    "Ticker": self.entry_1,
                    "Period": self.combobox_1,
                    "Interval": self.combobox_2,
                }
                self.entry_list.append(self.entry_dir)

                self.t += 1

                self.check_canvas()

    # UTILITY FUNCTIONS PART

    def create_entry(self, entry_variable):
        """Creates entry field to enter ticker"""
        self.entry_variable = entry_variable

        self.entry_1 = customtkinter.CTkEntry(
            master=self.frame_1,
            placeholder_text="TICKER",
            textvariable=self.entry_variable,
        )

        self.entry_1.grid(row=2 + self.t, column=0, padx=10, pady=10, sticky="w")

        return self.entry_1

    def create_combobox_2(self, set):
        """Creates combobox of avaible intervals"""
        self.set = set

        self.combobox_2 = customtkinter.CTkOptionMenu(
            self.frame_1,
            values=[
                "1m",
                "2m",
                "5m",
                "15m",
                "30m",
                "90m",
                "1h",
                "1d",
                "5d",
                "1wk",
                "1mo",
                "3mo",
            ],
            fg_color=WHITE_COLOR,
            text_color=BLACK_COLOR,
            button_color=MAIN_COLOR,
            button_hover_color=SCND_COLOR,
            dropdown_hover_color=SCND_COLOR,
        )
        self.combobox_2.grid(row=2 + self.t, column=1, padx=10, pady=10, sticky="e")
        self.combobox_2.set(self.set)

        return self.combobox_2

    def create_combobox_1(self, set):
        """Creates combobox of avaible periods"""
        self.set = set

        self.combobox_1 = customtkinter.CTkOptionMenu(
            self.frame_1,
            values=[
                "1d",
                "7d",
                "1mo",
                "3mo",
                "6mo",
                "1y",
                "2y",
                "5y",
                "10y",
                "ytd",
                "max",
            ],
            fg_color=WHITE_COLOR,
            text_color=BLACK_COLOR,
            button_color=MAIN_COLOR,
            button_hover_color=SCND_COLOR,
            dropdown_hover_color=SCND_COLOR,
        )
        self.combobox_1.grid(row=2 + self.t, column=2, padx=10, pady=10, sticky="ew")
        self.combobox_1.set(set)

        return self.combobox_1

    def check_canvas(self):
        """Updates scrollbar in canvas, used once row is added"""

        self.canvas.itemconfigure(
            self.window, height=440 + self.entry_1.winfo_height() * self.t * 2
        )
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        if self.t > 4:
            self.scrollbar.grid(row=0, column=0, sticky="NE")


app = customtkinter.CTk()
running = YfinanceGUI(app)
app.mainloop()
