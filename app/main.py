import sqlite3
import tkinter as tk
from typing import Dict

from .app import create_app


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

    def mainloop(self):
        self.__screen_pos__()
        self.window.mainloop()


class User(Window):

    def __init__(self):
        super().__init__()
        self.first_name = tk.Entry(self.window, width=25)
        self.last_name = tk.Entry(self.window, width=25)
        self.login = tk.Entry(self.window, width=25)
        self.password = tk.Entry(self.window, width=25)
        self.user = None


class BoxPassword(User):

    def __init__(self):
        super().__init__()
        self.app = create_app
        self.data: Dict[str, str] = {}

        self.run()

    def __auth__(self) -> bool:
        """Проверка авторизации пользователя"""
        return bool(self.app.read_user())

    def dialog_window_auth_or_reg(self):
        # Создаём новое окно
        dialog = tk.Toplevel()
        dialog.title("Получить доступ")
        dialog.geometry("330x250")
        dialog.resizable(False, False)
        dialog.transient(self.window)  # Делает окно зависимым от главного
        dialog.grab_set()  # Блокирует взаимодействие с главным окном

        # Метки и поля ввода
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

    def create_user(self, dialog: tk.Toplevel):
        self.data.update(
            first_name=self.first_name.get() or "",
            last_name=self.last_name.get() or "",
            login=self.login.get(),
            password=self.password.get(),
        )
        try:
            create_app.created_user(self.data)
            dialog.destroy()
        except sqlite3.IntegrityError:
            pass
            self.dialog_window_auth_or_reg()
        self.run()

    def run(self) -> None:
        if self.__auth__():
            login = create_app.read_user()
            tk.Label(self.window, text=f"Welcome - {login.login.capitalize()}").pack()
            self.window.title(self.window.title() + f" - {login.login.capitalize()}")
        else:
            self.dialog_window_auth_or_reg()


rout = BoxPassword()

rout.mainloop()
