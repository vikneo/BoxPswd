import sqlite3
import tkinter as tk
import webbrowser
from functools import partial
from pathlib import Path
from typing import Dict, List

from .app import CreateApp, create_app
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
        self.side_bar_frame: tk.Frame = tk.Frame()
        self.content_frame: tk.Frame = tk.Frame()

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
        self.app: CreateApp = create_app
        self.data: Dict[str, str] = {}
        self.dict_btn: Dict[tk.Button, List[tk.Label | tk.Entry]] = {}
        self.buttons: List[tk.Button] = []
        self.label_contents: List[tk.Label | tk.Entry] = []

        self.run()

    def content_field(self) -> None:
        self.content_frame = tk.Frame(
            self.window, width=500, height=700, bd=2, bg="#727272"
        )
        self.content_frame.grid(row=0, column=1, padx=10, pady=13, sticky="n")

        for i, nav_menu in enumerate(navbar_list):
            tk.Label(
                self.content_frame,
                text=nav_menu,
                bg="#727272",
                font="Arial, 9",
                fg="white",
            ).grid(row=0, column=i, ipady=2, ipadx=10, padx=40, pady=1, sticky="n")

        tag_hr = tk.LabelFrame(self.content_frame)
        tag_hr.grid(row=1, columnspan=5, sticky="we")

        try:
            if self.user:
                items: List[BoxPass] | None = create_app.get_items(self.user.login)
                for item in items if items else []:
                    fields = BoxPass.__table__.columns.keys()
                    i = 0
                    for field in fields:
                        text_var = tk.StringVar()
                        value = getattr(item, field)
                        text_var.set(value)
                        if field in ["link", "user_id", "id"]:
                            continue
                        elif field in ["name_site", "login", "password"]:
                            content: tk.Entry = tk.Entry(
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
                            row=item.id + 1,
                            column=i,
                            pady=0,
                            padx=2,
                            ipadx=4,
                            sticky="we",
                        )
                        i += 1
                        content.config(borderwidth=0, highlightthickness=0)
                        self.label_contents.append(content)

                    del_btn = tk.Button(
                        self.content_frame,
                        text="-",
                        bg="#FF5252",
                        fg="#000000",
                    )
                    del_btn.grid(
                        row=item.id + 1,
                        column=len(fields) + 1,
                        padx=3,
                        ipadx=5,
                        pady=1,
                    )
                    del_btn.post_id = item.id  # type: ignore
                    del_btn.config(
                        command=partial(self.delete_password, del_btn),
                        borderwidth=0,
                        highlightthickness=0,
                    )
                    link_btn = tk.Button(
                        self.content_frame,
                        text="->",
                        bg="#17E74B",
                        fg="#000000",
                    )
                    link_btn.grid(row=item.id + 1, column=len(fields) + 2, pady=1)
                    link_btn.config(
                        command=partial(self.open_link, item.link),
                        borderwidth=0,
                        highlightthickness=0,
                    )

                    self.dict_btn.setdefault(del_btn, self.label_contents)
                    self.label_contents = []
        except TypeError as err:
            print(f"Не найден пользователь\n{err}")

    def open_link(self, link: str) -> None:
        webbrowser.open(link)

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
        inp_button.grid(row=0, column=1, ipadx=50, ipady=2, padx=2, pady=6, sticky="n")

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
                add_btn = tk.Button(
                    self.side_bar_frame,
                    text="Добавить пароль",
                    bg="#A1AAA2",
                    command=lambda: self.add_password_dialog_window("Добавить пароль"),
                )
                add_btn.grid(
                    row=2, column=1, ipadx=20, ipady=2, padx=3, pady=6, sticky="n"
                )
                self.buttons.append(add_btn)
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

        for key, items in self.dict_btn.items():
            key.grid_forget()
            for label in items:
                label.grid_forget()

        self.user = None  # type: ignore
        self.window.title("Личный сейф")
        self.run()

    def delete_password(self, btn_del: tk.Button) -> None:
        items = self.dict_btn.get(btn_del)
        self.content_frame.destroy()
        self.dict_btn.clear()
        btn_del.destroy()
        for item in items:  # type: ignore
            item.destroy()

        try:
            create_app.del_password(btn_del.post_id)  # type: ignore
            self.run()
        except AttributeError as err:
            print(err)

    def create_user(self, dialog: tk.Toplevel) -> None:
        self.data.update(
            login=self.login.get(),
            password=self.password.get(),
        )
        try:
            create_app.created_user(self.data)  # type: ignore
            self.user = create_app.get_user(self.data["login"])  # type: ignore
            dialog.destroy()
            self.data = {}
            self.content_frame.destroy()
            self.dict_btn.clear()
        except sqlite3.IntegrityError:
            pass
        self.run()

    def created_boxpswd(self, dialog: tk.Toplevel) -> None:
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
            self.content_frame.destroy()
            self.dict_btn.clear()
            self.data = {}
        except sqlite3.IntegrityError as err:
            print(err)
        except IndexError as err:
            print(err)
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
