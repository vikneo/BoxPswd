import sqlite3
import tkinter as tk
from typing import Dict

from .app import create_app
from .encrypt import is_valid_hash


class Window:
    def __init__(self):
        self.window: tk.Tk = tk.Tk()
        self.width = self.window.winfo_screenwidth()
        self.height = self.window.winfo_screenheight()
        self.button = tk.Button()
        self.lable = tk.Label()
        self.side_bar_frame = tk.Frame()
        self.content_frame = tk.Frame()

    def __screen_pos__(self):
        """
        Установка разрешений окна и позиции на экране.
        Запрет на изменение размеров окна.
        """
        self.width = self.width // 4
        self.height = (self.height * 0) + 10
        self.window.geometry(f"673x701-{self.width}+{self.height}")
        self.window.resizable(width=False, height=False)
        self.window.title("Личный сейф")
        self.window.configure(background="#D3D3D3")

    def __dialog_window__(self) -> tk.Toplevel:
        dialog = tk.Toplevel()
        dialog.title("Авторизация / Регистрация")
        dialog.geometry(f"290x145-400+140")
        dialog.resizable(False, False)
        dialog.transient(self.window)
        dialog.grab_set()
        return dialog

    def mainloop(self):
        self.__screen_pos__()
        self.window.mainloop()


class Users(Window):

    def __init__(self):
        super().__init__()
        self.first_name: tk.Entry = tk.Entry(self.window, width=25)
        self.last_name: tk.Entry = tk.Entry(self.window, width=25)
        self.login: tk.Entry = tk.Entry(self.window, width=25)
        self.password: tk.Entry = tk.Entry(self.window, width=25)
        self.user = None


class BoxPassword(Users, Window):

    def __init__(self):
        super().__init__()
        self.app = create_app
        self.data: Dict[str, str] = {}

        self.run()
    
    def pos_frame(self):
        self.side_bar_frame = tk.Frame(self.window, width=200, height=700, bd=2, bg="#D3D3D3")
        self.side_bar_frame.grid(row=0, column=0, pady=5, sticky="n")
        self.content_frame = tk.Frame(self.window, width=500, height=700, bd=2, bg="#808080")
        self.content_frame.grid(row=0, column=1, sticky="w")

        self.lable = tk.Label(
            self.side_bar_frame, text="Доступ", bg="#A9A9A9", font="Arial, 15"
            )
        self.lable.grid(row=0, column=0, ipadx=54, pady=3)
        inp_button = tk.Button(
            self.side_bar_frame, text="@", bg="#A52A2A", command=self.register_dialog_window
        )
        inp_button.grid(row=0, column=1, ipadx=3, ipady=2, padx=2, pady=3, sticky="n")

        self.lable = tk.Label(
            self.side_bar_frame, text="Добавить", bg="#A9A9A9", font="Arial, 16"
            )
        self.lable.grid(row=1, column=0, ipadx=40, pady=3)
        create_button = tk.Button(
            self.side_bar_frame, text="#", bg="#1CB624", command=self.register_dialog_window
        )
        create_button.grid(row=1, column=1, ipadx=5, ipady=2, padx=3, pady=3, sticky="n")
        try:
            if self.user:
                inp_button.config(bg="#00FF00", pady=-2, command=self.out_user)
        except AttributeError as err:
            print(err)
        
        # self.window.grid_columnconfigure(0, weight=1)
        # self.window.grid_columnconfigure(1, weight=1)

    def out_user(self):
        self.user = None  # type: ignore
        self.window.title("Личный сейф")
        self.pos_frame()

    def register_dialog_window(self) -> None:
        dialog = self.__dialog_window__()
        tk.Label(dialog, text="Логин:").grid(
            row=2, column=0, padx=10, pady=10, sticky="w"
        )
        self.login = tk.Entry(dialog, width=25)
        self.login.grid(row=2, column=1, columnspan=3, padx=10, pady=10)

        tk.Label(dialog, text="Пароль:").grid(
            row=3, column=0, padx=10, pady=10, sticky="w"
        )
        self.password = tk.Entry(dialog, width=25)
        self.password.grid(row=3, column=1, columnspan=3, padx=10, pady=10)

        self.button = tk.Button(
            dialog,
            text="Войти",
            bg="blue",
            fg="white",
            command=lambda: self.auth_user(dialog),
        )
        self.button.grid(row=4, column=0, padx=15, pady=10, sticky="w")
        self.button = tk.Button(
            dialog,
            text="Создать доступ",
            bg="grey",
            fg="white",
            command=lambda: self.create_user(dialog),
        )
        self.button.grid(row=4, column=1, columnspan=3, padx=10, pady=10, sticky="e")

    def auth_user(self, dialog: tk.Toplevel | None) -> None:
        self.data.update(
            login=self.login.get(),
            password=self.password.get(),
        )
        self.user = create_app.read_user(self.data["login"])  # type: ignore
        if self.user is None:
            self.login.config(bg="red", fg="white")
        elif is_valid_hash(self.user.password, self.data["password"]):
            self.data = {}
            self.run()
            if dialog:
                dialog.destroy()
        else:
            self.password.config(bg="red", fg="white")

    def create_user(self, dialog: tk.Toplevel):
        self.data.update(
            first_name=self.first_name.get() or "",
            last_name=self.last_name.get() or "",
            login=self.login.get(),
            password=self.password.get(),
        )
        try:
            create_app.created_user(self.data)  # type: ignore
            self.user = create_app.read_user(self.data["login"])  # type: ignore
            dialog.destroy()
            self.data = {}
        except sqlite3.IntegrityError:
            self.register_dialog_window()
        self.run()

    def run(self) -> None:
        self.pos_frame()
        try:
            if self.user:
                self.window.title(
                    self.window.title() + f" - {self.user.login.capitalize()}"
                )
        except AttributeError as err:
            self.register_dialog_window()
            print(err)


rout = BoxPassword()

rout.mainloop()
