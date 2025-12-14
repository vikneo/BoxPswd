import sqlite3
import tkinter as tk
from typing import Dict

from .app import create_app
from .encrypt import is_valid_hash
from .models import User


class Window:
    def __init__(self):
        self.window: tk.Tk = tk.Tk()
        self.width = self.window.winfo_screenwidth()
        self.height = self.window.winfo_screenheight()

    def __screen_pos__(self):
        """
        Установка разрешений окна и позиции на экране.
        Запрет на изменение размеров окна.
        """
        width = self.width // 4
        height = (self.height * 0) + 80
        self.window.geometry(f"673x825-{width}+{height}")
        self.window.resizable(width=False, height=False)
        self.window.title("Личный сейф")

    def __dialog_window__(self) -> tk.Toplevel:
        dialog = tk.Toplevel()
        dialog.title("Получить доступ")
        dialog.geometry("330x250")
        dialog.resizable(False, False)
        dialog.transient(self.window)  # Делает окно зависимым от главного
        dialog.grab_set()  # Блокирует взаимодействие с главным окном
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
        self.user: User


class BoxPassword(Users):

    def __init__(self):
        super().__init__()
        self.app = create_app
        self.data: Dict[str, str] = {}

        self.run()

    def register_dialog_window(self) -> None:
        dialog = self.__dialog_window__()
        tk.Label(dialog, text="Имя:").grid(
            row=0, column=0, padx=10, pady=10, sticky="w"
        )
        self.first_name = tk.Entry(dialog, width=25)
        self.first_name.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(dialog, text="Фамилия:").grid(
            row=1, column=0, padx=10, pady=10, sticky="w"
        )
        self.last_name = tk.Entry(dialog, width=25)
        self.last_name.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(dialog, text="Логин:").grid(
            row=2, column=0, padx=10, pady=10, sticky="w"
        )
        self.login = tk.Entry(dialog, width=25)
        self.login.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(dialog, text="Пароль:").grid(
            row=3, column=0, padx=10, pady=10, sticky="w"
        )
        self.password = tk.Entry(dialog, width=25)
        self.password.grid(row=3, column=1, padx=10, pady=10)

        save_btn = tk.Button(
            dialog,
            text="Войти",
            bg="blue",
            fg="white",
            command=lambda: self.auth_user(dialog),
        )
        save_btn.grid(row=4, column=0, padx=10, pady=10, sticky="w")
        create_btn = tk.Button(
            dialog,
            text="Создать доступ",
            bg="grey",
            fg="white",
            command=lambda: self.create_user(dialog),
        )
        create_btn.grid(row=4, column=1, padx=10, pady=10, sticky="e")

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
            create_app.created_user(self.data)
            self.user = create_app.read_user(self.data["login"])  # type: ignore
            dialog.destroy()
            self.data = {}
        except sqlite3.IntegrityError:
            self.register_dialog_window()
        self.run()

    def run(self) -> None:
        if self.user is None:
            self.register_dialog_window()
        if self.user:
            tk.Label(
                self.window, text=f"Welcome - {self.user.login.capitalize()}"
            ).pack()
            self.window.title(
                self.window.title() + f" - {self.user.login.capitalize()}"
            )


rout = BoxPassword()

rout.mainloop()
