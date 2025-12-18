import sqlite3
import tkinter as tk
from pathlib import Path
from typing import Dict, List

from .app import create_app
from .config import navbar_list
from .encrypt import is_valid_hash
from .models import BoxPass


class Window:
    def __init__(self):
        self.window = self.get_window()
        self.width = self.window.winfo_screenwidth()
        self.height = self.window.winfo_screenheight()
        self.button = tk.Button()
        self.label = tk.Label()
        self.side_bar_frame = tk.Frame()
        self.content_frame = tk.Frame()

    def __screen_pos__(self):
        """
        Установка разрешений окна и позиции на экране.
        Запрет на изменение размеров окна.
        """
        self.width = self.width // 6
        self.height = (self.height * 0) + 10
        self.window.geometry(f"955x600+{self.width}+{self.height}")
        self.window.resizable(width=False, height=False)
        self.window.title("Личный сейф")
        self.window.configure(background="#D3D3D3")

    def __dialog_window__(self, action: str, height: str = "145") -> tk.Toplevel:
        dialog = tk.Toplevel()
        dialog.title(action)
        dialog.transient(self.window)
        dialog.geometry(f"320x{height}+300+50")
        dialog.resizable(False, False)
        dialog.configure(background="#D3D3D3")
        dialog.grab_set()
        dialog.focus_set()
        return dialog

    def get_window(self) -> tk.Tk:
        self.window = tk.Tk()
        return self.window

    def instal_icon(self):
        path_dir = Path(__file__).parent.parent / "static"
        icon_file = path_dir / "favicon.png"
        icon = tk.PhotoImage(file=icon_file)
        self.window.iconphoto(False, icon)

    def mainloop(self):
        self.__screen_pos__()
        self.instal_icon()
        self.window.mainloop()


class Users(Window):

    def __init__(self):
        super().__init__()
        self.link: tk.Entry = tk.Entry(width=25)
        self.login: tk.Entry = tk.Entry(width=25)
        self.password: tk.Entry = tk.Entry(width=25)
        self.phone: tk.Entry = tk.Entry(width=25)
        self.pincode: tk.Entry = tk.Entry(width=25)
        self.user = None


class BoxPassword(Users, Window):

    def __init__(self):
        super().__init__()
        self.app = create_app
        self.data: Dict[str, str] = {}
        self.buttons: List = []
        self.label_contents: List = []

        self.run()

    def content_field(self) -> None:
        self.content_frame = tk.Frame(
            self.window, width=500, height=700, bd=2, bg="#727272"
        )
        self.content_frame.grid(row=0, column=1, padx=10, pady=10, sticky="n")

        for i, nav_menu in enumerate(navbar_list):
            tk.Label(
                self.content_frame,
                text=nav_menu,
                bg="#727272",
                font="Arial, 9",
                fg="white",
            ).grid(row=0, column=i, ipady=2, ipadx=14, padx=40, pady=1, sticky="n")

        tag_hr = tk.LabelFrame(self.content_frame)
        tag_hr.grid(row=1, columnspan=5, sticky="we")

        try:
            if self.user:
                items = create_app.get_items(self.user.login)
                row = 3
                for item in items:
                    fields = BoxPass.__table__.columns.keys()
                    for i, field in enumerate(fields):
                        text_var = tk.StringVar()
                        value = getattr(item, field)
                        text_var.set(value)
                        if field in ["user_id", "id"]:
                            continue
                        if field in ["link", "login", "password"]:
                            content = tk.Entry(
                                self.content_frame,
                                textvariable=text_var,
                                state="readonly",
                                readonlybackground="#ECE8E8",
                            )
                        else:
                            content = tk.Label(
                                self.content_frame, text=value, bg="#9B9B9B", fg="white"
                            )  # type: ignore
                        content.grid(
                            row=item.id + 1, column=i, pady=1, ipadx=2, sticky="we"
                        )
                        self.label_contents.append(content)
                    row += 1
        except TypeError as err:
            print(f"Не найден пользователь\n{err}")

    def sidebar_field(self) -> None:
        self.side_bar_frame = tk.Frame(
            self.window, width=200, height=700, bd=2, bg="#D3D3D3"
        )
        self.side_bar_frame.grid(row=0, column=0, pady=5, sticky="n")

        inp_button = tk.Button(
            self.side_bar_frame,
            text="Войти",
            bg="#D6A3A3",
            command=lambda: self.register_dialog_window("Авторизация"),
        )
        inp_button.grid(row=0, column=1, ipadx=50, ipady=2, padx=2, pady=1, sticky="n")

        create_button = tk.Button(
            self.side_bar_frame,
            text="Создать пользователя",
            bg="#A1AAA2",
            command=lambda: self.register_dialog_window("Регистрация"),
        )
        create_button.grid(
            row=1, column=1, ipadx=6, ipady=2, padx=3, pady=6, sticky="n"
        )
        try:
            if self.user:
                self.add_btn = tk.Button(
                    self.side_bar_frame,
                    text="Добавить пароль",
                    bg="#A1AAA2",
                    command=lambda: self.add_password_dialog_window("Добавить пароль"),
                )
                self.add_btn.grid(
                    row=2, column=1, ipadx=22, ipady=2, padx=3, pady=6, sticky="n"
                )
                self.buttons.append(add_button)
                inp_button.config(text="Выйти", bg="#87F087", command=self.out_user)
        except AttributeError as err:
            print(err)

    def add_password_dialog_window(self, action: str) -> None:
        dialog = self.__dialog_window__(action=action, height="280")
        tk.Label(dialog, text="Сайт:", bg="#D3D3D3").grid(
            row=0, column=0, padx=10, pady=10, sticky="w"
        )
        self.link = tk.Entry(dialog, width=25)
        self.link.grid(row=0, column=1, columnspan=3, padx=10, pady=10)

        tk.Label(dialog, text="Телефон:", bg="#D3D3D3").grid(
            row=1, column=0, padx=10, pady=10, sticky="w"
        )
        self.phone = tk.Entry(dialog, width=25)
        self.phone.grid(row=1, column=1, columnspan=3, padx=10, pady=10)

        tk.Label(dialog, text="Пин-код:", bg="#D3D3D3").grid(
            row=2, column=0, padx=10, pady=10, sticky="w"
        )
        self.pincode = tk.Entry(dialog, width=25)
        self.pincode.grid(row=2, column=1, columnspan=3, padx=10, pady=10)

        tk.Label(dialog, text="Логин:", bg="#D3D3D3").grid(
            row=3, column=0, padx=10, pady=10, sticky="w"
        )
        self.login = tk.Entry(dialog, width=25)
        self.login.grid(row=3, column=1, columnspan=3, padx=10, pady=10)

        tk.Label(dialog, text="Пароль:", bg="#D3D3D3").grid(
            row=4, column=0, padx=10, pady=10, sticky="w"
        )
        self.password = tk.Entry(dialog, width=25)
        self.password.grid(row=4, column=1, columnspan=3, padx=10, pady=10)

        btn = tk.Button(
            dialog,
            text="Добавить пароль",
            bg="#A1AAA2",
            command=lambda: self.created_boxpswd(dialog),
        )
        btn.grid(row=5, column=1, columnspan=3, padx=10, pady=10, sticky="we")

    def register_dialog_window(self, action: str) -> None:
        dialog = self.__dialog_window__(action=action)
        tk.Label(dialog, text="Логин:", bg="#D3D3D3").grid(
            row=0, column=0, padx=10, pady=10, sticky="w"
        )
        self.login = tk.Entry(dialog, width=25)
        self.login.grid(row=0, column=1, columnspan=3, padx=10, pady=10)

        tk.Label(dialog, text="Пароль:", bg="#D3D3D3").grid(
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
        self.button.grid(
            row=2, column=1, columnspan=3, ipadx=15, padx=15, pady=10, sticky="we"
        )

        if action.lower() == "авторизация":
            self.button.configure(command=lambda: self.auth_user(dialog))
        else:
            self.button.configure(
                text="Создать", command=lambda: self.create_user(dialog)
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

    def out_user(self):
        for btn in self.buttons:
            btn.grid_forget()

        for label in self.label_contents:
            label.grid_forget()

        self.user = None  # type: ignore
        self.window.title("Личный сейф")
        self.run()

    def create_user(self, dialog: tk.Toplevel):
        self.data.update(
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

    def created_boxpswd(self, dialog: tk.Toplevel):
        self.data.update(
            link=self.link.get(),
            login=self.login.get(),
            password=self.password.get(),
            phone=self.phone.get(),
            pincode=self.pincode.get(),
            user_id=self.user.id,  # type: ignore
        )
        try:
            create_app.created_password(self.data)
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
                self.window.title(f"Личный сейф - {self.user.login.capitalize()}")
        except AttributeError as err:
            print(err)


rout = BoxPassword()

rout.mainloop()
