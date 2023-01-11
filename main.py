import os
import tkinter
import tkinter.messagebox
import tkinter.filedialog
from tkinter import StringVar, IntVar
import tkinter as tk
import customtkinter
from im_exec import compress_dir_jpg
import threading
import configparser

customtkinter.set_appearance_mode(
    "System"
)  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme(
    "green"
)  # Themes: "blue" (standard), "green", "dark-blue"


config_path = os.path.abspath("config.ini")


class App(customtkinter.CTk):

    WIDTH = 780
    HEIGHT = 400

    def __init__(self):
        super().__init__()
        self.threads = []

        self.title("Image compressor")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol(
            "WM_DELETE_WINDOW", self.on_closing
        )  # call .on_closing() when app gets closed

        self.iconbitmap("icons/press.ico")

        # ============ create two frames ============
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.frame_top = customtkinter.CTkFrame(
            master=self, width=180, corner_radius=0
        )
        self.frame_top.grid(row=0, column=0, sticky="nswe")
        # configure grid layout (3x5)
        self.frame_top.grid_rowconfigure(
            5, minsize=10
        )  # empty row with minsize as spacing
        self.frame_top.columnconfigure(0, weight=2)
        self.frame_top.columnconfigure(1, weight=3)
        self.frame_top.columnconfigure(2, weight=1)

        self.frame_extensions = customtkinter.CTkFrame(
            master=self, corner_radius=0
        )
        self.frame_extensions.grid(row=1, column=0, sticky="nswe")
        self.frame_extensions.grid_rowconfigure(1, minsize=20)
        self.frame_extensions.columnconfigure(0, weight=4)
        self.frame_extensions.columnconfigure(1, weight=4)
        self.frame_extensions.columnconfigure(2, weight=4)

        self.frame_bottom = customtkinter.CTkFrame(master=self)
        self.frame_bottom.grid(
            row=2, column=0, sticky="nswe", padx=20, pady=20
        )
        self.frame_bottom.grid_rowconfigure(5, minsize=10)
        self.frame_bottom.columnconfigure((0, 1), weight=1)
        self.frame_bottom.columnconfigure((2), weight=0)

        ### Parts of upper frame

        self.label_1 = customtkinter.CTkLabel(
            master=self.frame_top,
            text="Folder wejściowy: ",
            font=("Roboto Medium", -16),
        )  # font name and size in px
        self.label_1.grid(row=1, column=0, pady=10, padx=10)
        self.source_dir = StringVar()
        self.source_dir.set("")
        self.entry_1 = customtkinter.CTkEntry(
            master=self.frame_top,
            width=350,
            textvariable=self.source_dir,
            font=("Roboto Medium", -10),
        )  # font name and size in px
        self.entry_1.grid(row=1, column=1, pady=10, padx=10)

        self.button_1 = customtkinter.CTkButton(
            master=self.frame_top,
            text="Browse",
            command=self.get_source_dir,
        )
        self.button_1.grid(row=1, column=2, pady=10, padx=20)

        self.label_2 = customtkinter.CTkLabel(
            master=self.frame_top,
            text="Folder wyjściowy: ",
            font=("Roboto Medium", -16),
        )  # font name and size in px
        self.label_2.grid(row=2, column=0, pady=10, padx=10)
        self.output_dir = StringVar()
        self.output_dir.set("")
        self.entry_2 = customtkinter.CTkEntry(
            master=self.frame_top,
            width=350,
            textvariable=self.output_dir,
            font=("Roboto Medium", -10),
        )  # font name and size in px
        self.entry_2.grid(row=2, column=1, pady=10, padx=10)

        self.button_2 = customtkinter.CTkButton(
            master=self.frame_top, text="Browse", command=self.get_output_dir
        )
        self.button_2.grid(row=2, column=2, pady=10, padx=20)

        self.label_quality = customtkinter.CTkLabel(
            master=self.frame_top,
            text="Jakość [1-100]: ",
            font=("Roboto Medium", -16),
        )  # font name and size in px
        self.label_quality.grid(row=3, column=0, pady=10, padx=10)
        self.quality = IntVar()
        self.last_quality = 1
        self.quality.trace(
            "w",
            lambda name, index, mode, sv=self.quality: self.validate_quality(),
        )
        self.slider_quality = customtkinter.CTkSlider(
            master=self.frame_top, from_=1, to=100, variable=self.quality
        )
        self.slider_quality.bind("<ButtonRelease-1>", self.save_config)
        self.slider_quality.grid(
            row=3, column=1, pady=10, padx=20, sticky=tk.EW
        )
        self.entry_quality = customtkinter.CTkEntry(
            master=self.frame_top,
            width=100,
            textvariable=self.quality,
            font=("Roboto Medium", -10),
        )  # font name and size in px

        self.entry_quality.grid(row=3, column=2, pady=10)

        ### Extensions
        self.check_jpg_var = customtkinter.BooleanVar()
        self.check_jpg = customtkinter.CTkCheckBox(
            master=self.frame_extensions,
            text=".jpg",
            command=self.save_config,
            variable=self.check_jpg_var,
        )
        self.check_jpg.grid(row=1, column=0, pady=10, padx=20)
        self.check_jpeg_var = customtkinter.BooleanVar()
        self.check_jpeg = customtkinter.CTkCheckBox(
            master=self.frame_extensions,
            text=".jpeg",
            command=self.save_config,
            variable=self.check_jpeg_var,
        )
        self.check_jpeg.grid(row=1, column=1, pady=10, padx=20)
        self.check_png_var = customtkinter.BooleanVar()
        self.check_png = customtkinter.CTkCheckBox(
            master=self.frame_extensions,
            text=".png",
            command=self.save_config,
            variable=self.check_png_var,
        )
        self.check_png.grid(row=1, column=2, pady=10, padx=20)

        ### Parts of bottom frame

        self.btn_start_comp = customtkinter.CTkButton(
            master=self.frame_bottom,
            text="Kompresuj",
            command=self.compress_images_btn,
        )
        self.btn_start_comp.grid(
            row=1, column=0, columnspan=3, pady=10, padx=20
        )
        self.btn_stop_comp = customtkinter.CTkButton(
            master=self.frame_bottom,
            text="STOP",
            fg_color="red",
            hover_color="darkred",
        )
        self.btn_stop_comp.grid(
            row=1, column=4, columnspan=1, pady=10, padx=20
        )
        self.btn_stop_comp.grid_forget()

        self.label_3 = customtkinter.CTkLabel(
            master=self.frame_bottom,
            text="Aktualny plik: ",
            font=("Roboto Medium", -16),
        )  # font name and size in px
        self.label_3.grid(row=2, column=0, pady=10, padx=10)
        self.current_file = StringVar()
        self.current_file.set("")
        self.entry_3 = customtkinter.CTkEntry(
            master=self.frame_bottom,
            textvariable=self.current_file,
            width=200,
            font=("Roboto Medium", -16),
            state=tkinter.DISABLED,
        )  # font name and size in px
        self.entry_3.grid(row=2, column=1, columnspan=2, pady=10, padx=10)

        self.progressbar = customtkinter.CTkProgressBar(
            master=self.frame_bottom
        )
        self.progressbar.grid(
            row=4, column=0, columnspan=2, sticky="ew", padx=15, pady=15
        )
        self.current_no = StringVar()
        self.current_no.set("")
        self.label_4 = customtkinter.CTkLabel(
            master=self.frame_bottom,
            textvariable=self.current_no,
            font=("Roboto Medium", -16),
        )  # font name and size in px
        self.label_4.grid(row=4, column=2, pady=10, padx=10)

        self.error_var = StringVar()
        self.error_var.set("")
        self.label_5 = customtkinter.CTkLabel(
            master=self.frame_bottom,
            textvariable=self.error_var,
            font=("Roboto Medium", -16),
        )  # font name and size in px
        self.label_5.grid(row=5, column=0, pady=10, padx=10)

        self.progressbar.set(0)
        self.set_from_config()

    def validate_quality(self):
        q = self.quality.get()
        if q:
            try:
                q = int(q)
                if q > 0 and q <= 100:
                    self.quality.set(q)
                    self.last_quality = q
                    return True
                else:
                    self.quality.set(self.last_quality)
                    return False
            except ValueError:
                self.quality.set(self.last_quality)
                return False
        else:
            self.quality.set(self.last_quality)
            return False

    def get_source_dir(self):
        self.source_dir.set(
            tkinter.filedialog.askdirectory(title="Source image directory")
        )
        self.save_config()

    def get_output_dir(self):
        self.output_dir.set(
            tkinter.filedialog.askdirectory(title="Output image directory")
        )
        self.save_config()

    def compress_images_btn(self):
        if len(self.output_dir.get()) > 0 and len(self.source_dir.get()) > 0:
            self.progressbar.set(0)
            self.error_var.set("")
            x = threading.Thread(target=self.compress_images_thread)
            self.threads.append(x)
            x.start()

    def compress_images_thread(self):
        self.btn_start_comp.configure(state=tkinter.DISABLED)
        self.btn_stop_comp.grid(
            row=1, column=4, columnspan=1, pady=10, padx=20
        )
        try:
            extensions = []
            if self.check_png_var.get():
                extensions.append(".png")
            if self.check_jpg_var.get():
                extensions.append(".jpg")
            if self.check_jpeg_var.get():
                extensions.append(".jpeg")
            compress_dir_jpg(
                source_dir=self.source_dir.get(),
                output_dir=self.output_dir.get(),
                quality=self.quality.get(),
                label_var=self.current_file,
                label_current_no=self.current_no,
                progress_bar_fn=self.progressbar.set,
                compress_btn_handle=self.btn_start_comp,
                stop_btn_handle=self.btn_stop_comp,
                error_var=self.error_var,
                extension=extensions,
            )
        except Exception:
            self.btn_start_comp.configure(state=tkinter.NORMAL)
            self.btn_stop_comp.grid_forget()

    def set_from_config(self):
        config = configparser.ConfigParser()
        config.read(config_path)
        self.source_dir.set(config["Main"]["last_source_dir"])
        self.output_dir.set(config["Main"]["last_output_dir"])
        self.quality.set(int(config["Main"]["quality"]))
        self.check_png_var.set(config["Main"]["check_png"] == "True")
        self.check_jpeg_var.set(config["Main"]["check_jpeg"] == "True")
        self.check_jpg_var.set(config["Main"]["check_jpg"] == "True")

    def save_config(self, *args):
        config = configparser.ConfigParser()
        if os.path.exists(config_path):
            config.read(config_path)

        else:
            config.add_section("Main")
            config["Main"]["last_source_dir"] = ""
            config["Main"]["last_output_dir"] = ""
            config["Main"]["quality"] = 80
            config["Main"]["check_png"] = str(True)
            config["Main"]["check_jpg"] = str(True)
            config["Main"]["check_jpeg"] = str(True)

        config["Main"]["last_source_dir"] = self.source_dir.get()
        config["Main"]["last_output_dir"] = self.output_dir.get()
        config["Main"]["quality"] = str(self.quality.get())
        config["Main"]["check_png"] = str(self.check_png_var.get())
        config["Main"]["check_jpg"] = str(self.check_jpg_var.get())
        config["Main"]["check_jpeg"] = str(self.check_jpeg_var.get())
        with open(config_path, "w") as configfile:
            config.write(configfile)

    def on_closing(self, event=0):
        for thread in self.threads:
            thread.join()
        self.destroy()


def widget_show(widget: customtkinter.CTkButton):
    widget.grid()


def widget_hide(widget: customtkinter.CTkButton):
    widget.grid_forget()


if __name__ == "__main__":
    app = App()
    app.mainloop()
