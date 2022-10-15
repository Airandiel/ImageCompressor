from os import stat
import tkinter
import tkinter.messagebox
import tkinter.filedialog
from tkinter import StringVar
import customtkinter
from im_exec import compress_dir_jpg
import threading

customtkinter.set_appearance_mode(
    "System"
)  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme(
    "green"
)  # Themes: "blue" (standard), "green", "dark-blue"


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
        self.grid_rowconfigure(1, weight=1)

        self.frame_top = customtkinter.CTkFrame(
            master=self, width=180, corner_radius=0
        )
        self.frame_top.grid(row=0, column=0, sticky="nswe")

        self.frame_bottom = customtkinter.CTkFrame(master=self)
        self.frame_bottom.grid(row=1, column=0, sticky="nswe", padx=20, pady=20)
        self.frame_bottom.grid_rowconfigure(5, minsize=10)
        self.frame_bottom.columnconfigure((0, 1), weight=1)
        self.frame_bottom.columnconfigure((2), weight=0)

        ### Parts of upper frame

        # configure grid layout (3x5)
        self.frame_top.grid_rowconfigure(
            5, minsize=10
        )  # empty row with minsize as spacing
        self.frame_top.columnconfigure((0), weight=1)
        self.frame_top.columnconfigure((1), weight=2)
        self.frame_top.columnconfigure((2), weight=1)
        # self.frame_top.columnconfigure(5, weight=0)
        self.label_1 = customtkinter.CTkLabel(
            master=self.frame_top,
            text="Folder wejściowy: ",
            text_font=("Roboto Medium", -16),
        )  # font name and size in px
        self.label_1.grid(row=1, column=0, pady=10, padx=10)
        self.source_dir = StringVar()
        self.source_dir.set("")
        self.entry_1 = customtkinter.CTkEntry(
            master=self.frame_top,
            width=350,
            textvariable=self.source_dir,
            text_font=("Roboto Medium", -10),
        )  # font name and size in px
        self.entry_1.grid(row=1, column=1, columnspan=3, pady=10, padx=10)

        self.button_1 = customtkinter.CTkButton(
            master=self.frame_top,
            text="Browse",
            command=self.get_source_dir,
        )
        self.button_1.grid(row=1, column=4, pady=10, padx=20)

        self.label_2 = customtkinter.CTkLabel(
            master=self.frame_top,
            text="Folder wyjściowy: ",
            text_font=("Roboto Medium", -16),
        )  # font name and size in px
        self.label_2.grid(row=2, column=0, pady=10, padx=10)
        self.output_dir = StringVar()
        self.output_dir.set("")
        self.entry_2 = customtkinter.CTkEntry(
            master=self.frame_top,
            width=350,
            textvariable=self.output_dir,
            text_font=("Roboto Medium", -10),
        )  # font name and size in px
        self.entry_2.grid(row=2, column=1, columnspan=2, pady=10, padx=10)

        self.button_2 = customtkinter.CTkButton(
            master=self.frame_top, text="Browse", command=self.get_output_dir
        )
        self.button_2.grid(row=2, column=4, pady=10, padx=20)

        ### Parts of bottom frame

        self.button_3 = customtkinter.CTkButton(
            master=self.frame_bottom, text="Kompresuj", command=self.compress_images_btn
        )
        self.button_3.grid(row=1, column=0, columnspan=3, pady=10, padx=20)

        self.label_3 = customtkinter.CTkLabel(
            master=self.frame_bottom,
            text="Aktualny plik: ",
            text_font=("Roboto Medium", -16),
        )  # font name and size in px
        self.label_3.grid(row=2, column=0, pady=10, padx=10)
        self.current_file = StringVar()
        self.current_file.set("")
        self.entry_3 = customtkinter.CTkEntry(
            master=self.frame_bottom,
            textvariable=self.current_file,
            width=200,
            text_font=("Roboto Medium", -16),
            state=tkinter.DISABLED,
        )  # font name and size in px
        self.entry_3.grid(row=2, column=1, columnspan=2, pady=10, padx=10)

        self.progressbar = customtkinter.CTkProgressBar(master=self.frame_bottom)
        self.progressbar.grid(
            row=4, column=0, columnspan=2, sticky="ew", padx=15, pady=15
        )
        self.current_no = StringVar()
        self.current_no.set("")
        self.label_4 = customtkinter.CTkLabel(
            master=self.frame_bottom,
            textvariable=self.current_no,
            text_font=("Roboto Medium", -16),
        )  # font name and size in px
        self.label_4.grid(row=4, column=2, pady=10, padx=10)

        self.error_var = StringVar()
        self.error_var.set("")
        self.label_5 = customtkinter.CTkLabel(
            master=self.frame_bottom,
            textvariable=self.error_var,
            text_font=("Roboto Medium", -16),
        )  # font name and size in px
        self.label_5.grid(row=5, column=0, pady=10, padx=10)

        self.progressbar.set(0)

    def get_source_dir(self):
        self.source_dir.set(
            tkinter.filedialog.askdirectory(title="Source image directory")
        )

    def get_output_dir(self):
        self.output_dir.set(
            tkinter.filedialog.askdirectory(title="Output image directory")
        )

    def compress_images_btn(self):
        if len(self.output_dir.get()) >0 and len(self.source_dir.get()) >0:
            self.progressbar.set(0)
            self.error_var.set("")
            x = threading.Thread(target=self.compress_images_thread)
            self.threads.append(x)
            x.start()

    def compress_images_thread(self):
        self.button_3.configure(state=tkinter.DISABLED)
        compress_dir_jpg(
            source_dir=self.source_dir.get(),
            output_dir=self.output_dir.get(),
            label_var=self.current_file,
            label_current_no=self.current_no,
            progress_bar_fn=self.progressbar.set,
            compress_btn_handle=self.button_3,
            error_var=self.error_var,
            extension=".jpg",
        )

    def on_closing(self, event=0):
        for thread in self.threads:
            thread.join()
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
