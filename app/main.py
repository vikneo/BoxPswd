import sqlite3
import tkinter as tk
from typing import Dict, List

from .app import create_app
from .config import navbar_list
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
        self.window.geometry(f"855x600-{self.width}+{self.height}")
        self.window.resizable(width=False, height=False)
        self.window.title("Личный сейф")
        self.window.configure(background="#D3D3D3")

    def __dialog_window__(self, action: str) -> tk.Toplevel:
        dialog = tk.Toplevel()
        dialog.title(action)
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
    
    def content_field(self) -> None:
        self.content_frame = tk.Frame(self.window, width=500, height=700, bd=2, bg="#B8B6B6")
        self.content_frame.grid(row=0, column=1, pady=9, sticky="n")


        for i, nav_menu in enumerate(navbar_list):
            tk.Label(
                self.content_frame, text=nav_menu, bg="#B8B6B6", font=("Arial, 9")
                ).grid(row=0, column=i, ipadx=2, padx=43, pady=2, sticky="n")
        
        if self.user:
            items = create_app.get_items(self.user.login)
            for item in items:
                print(item)
        
    
    def sidebar_field(self) -> None:
        self.side_bar_frame = tk.Frame(self.window, width=200, height=700, bd=2, bg="#D3D3D3")
        self.side_bar_frame.grid(row=0, column=0, pady=5, sticky="n")

        inp_button = tk.Button(
            self.side_bar_frame,
            text="Войти",
            bg="#D6A3A3",
            command=lambda: self.register_dialog_window("Авторизация")
        )
        inp_button.grid(row=0, column=1, ipadx=54, ipady=2, padx=2, pady=3, sticky="n")

        create_button = tk.Button(
            self.side_bar_frame,
            text="Создать пользователя",
            bg="#A1AAA2",
            command=lambda: self.register_dialog_window("Регистрация")
        )
        create_button.grid(row=1, column=1, ipadx=10, ipady=2, padx=3, pady=3, sticky="n")
        try:
            if self.user:
                inp_button.config(text="Выйти", bg="#87F087", command=self.out_user)
        except AttributeError as err:
            print(err)

    def out_user(self):
        self.user = None  # type: ignore
        self.window.title("Личный сейф")
        self.sidebar_field()
        self.run()

    def register_dialog_window(self, action: str) -> None:
        dialog = self.__dialog_window__(action=action)
        tk.Label(dialog, text="Логин:").grid(
            row=0, column=0, padx=10, pady=10, sticky="w"
        )
        self.login = tk.Entry(dialog, width=25)
        self.login.grid(row=0, column=1, columnspan=3, padx=10, pady=10)

        tk.Label(dialog, text="Пароль:").grid(
            row=1, column=0, padx=10, pady=10, sticky="w"
        )
        self.password = tk.Entry(dialog, width=25)
        self.password.grid(row=1, column=1, columnspan=3, padx=10, pady=10)

        self.button = tk.Button(
            dialog,
            text="Войти",
            bg="blue",
            fg="white",
        )
        self.button.grid(row=2, column=1, ipadx=15, padx=15, pady=10, sticky="we")

        if action.lower() == "авторизация":
            self.button.configure(command=lambda: self.auth_user(dialog))
        else:
            self.button.configure(
                text="Создать",
                command=lambda: self.create_user(dialog)
                )


    def auth_user(self, dialog: tk.Toplevel | None) -> None:
        self.data.update(
            login=self.login.get(),
            password=self.password.get(),
        )
        self.user = create_app.get_user(self.data["login"])  # type: ignore
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
            self.user = create_app.get_user(self.data["login"])  # type: ignore
            dialog.destroy()
            self.data = {}
        except sqlite3.IntegrityError:
            pass
        self.run()

    def run(self) -> None:
        self.sidebar_field()
        self.content_field()
        try:
            if self.user:
                self.window.title(
                    f"Личный сейф - {self.user.login.capitalize()}"
                )
        except AttributeError as err:
            print(err)


rout = BoxPassword()

rout.mainloop()
