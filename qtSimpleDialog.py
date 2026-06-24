"""Loading dialog and simple dialogs migrated from tkSimpleDialog using PyQt6."""

from __future__ import annotations

from threading import Thread
from typing import Any

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox, QFileDialog
from qt_ui import BOTH, HORIZONTAL, WORD, DoubleVar, StringVar, TclError
from qt_ui.ttk import Progressbar
from util import Utilitarios


class Loading(QDialog):
    def __init__(
        self,
        parent,
        title=None,
        orient_u=HORIZONTAL,
        maximum_u=100,
        length_u=100,
        mode_u="determinate",
        icon=None,
        progress_var=None,
        info_loading=None,
        uti=None,
        Dado_config=None,
        stop_thread=False,
        threads=None,
        cancelable=True,
        _thread_name=None,
    ):
        tk.Toplevel.__init__(self, parent)

        self.transient(parent)
        self._uti = uti
        self._stop_thread = stop_thread
        self._threads = threads or []
        self._Dado_config = Dado_config
        self.result = None

        body = tk.Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)
        lblinfo = tk.Label(self, width=500, wraplength=520, anchor="center", font="Helvetica 8 bold")
        lblinfo.pack(fill=BOTH, expand=True)

        if info_loading:
            lblinfo.config(textvariable=info_loading)
        else:
            lblinfo.config(text="Loading")

        self.progress = Progressbar(
            self,
            variable=progress_var,
            orient=orient_u,
            maximum=maximum_u,
            length=length_u,
            mode=mode_u,
        )
        self.progress.pack(pady=10)
        self.grab_set()
        if not self.initial_focus:
            self.initial_focus = self

        if cancelable:
            self.protocol("WM_DELETE_WINDOW", self.cancel)
        if title:
            self.title(title)
        self.parent = parent
        if self._uti:
            self._uti.center(self.parent, self, 550, 90)
        if icon:
            self.iconbitmap(icon)

        self.initial_focus.focus_force()
        self.resizable(False, False)

        thread_fim = Thread(target=self.finished, args=(self.progress, maximum_u))
        thread_fim.start()

    def finished(self, pro, maxs):
        try:
            while True:
                if pro["value"] == maxs:
                    if self._Dado_config:
                        from qt_ui import messagebox

                        messagebox.showinfo(
                            self._Dado_config.idioma(182),
                            self._Dado_config.idioma(180),
                            parent=self,
                        )
                    if self._stop_thread:
                        self._stop_thread.set(True)
                    if self._threads and hasattr(self._threads, "kill"):
                        self._threads.kill()
                    self.parent.focus_set()
                    self.destroy()
                    break
        except TclError as e:
            print(e)

    def re_prog(self):
        return self.progress

    def body(self, master):
        pass

    def cancel(self):
        from qt_ui import messagebox

        if self._Dado_config and messagebox.askokcancel(
            self._Dado_config.idioma(47),
            self._Dado_config.idioma(48),
            parent=self,
        ):
            if self._stop_thread:
                self._stop_thread.set(True)
            if self._threads and hasattr(self._threads, "kill"):
                self._threads.kill()
            self.parent.focus_set()
            self.destroy()

    def validate(self):
        return 1

    def apply(self):
        pass


class Dialog(QDialog):
    """Simple scrollable info dialog."""

    def __init__(self, parent, title, info_lines, icon=None):
        tk.Toplevel.__init__(self, parent)
        self.title(str(title))
        self.transient(parent)
        self.grab_set()

        text = tk.Text(self, width=90, height=20, wrap=WORD)
        text.pack(fill=BOTH, expand=True, padx=5, pady=5)
        if isinstance(info_lines, (list, tuple)):
            content = "\n".join(str(line) for line in info_lines)
        else:
            content = str(info_lines)
        text.insert("1.0", content)
        text.config(state="disabled")

        btn = tk.Button(self, text="OK", command=self.destroy)
        btn.pack(pady=5)

        if icon:
            self.iconbitmap(icon)

        uti = Utilitarios()
        uti.center(parent, self, 700, 400)
        self.wait_window(self)


if __name__ == "__main__":
    from qt_ui import Tk

    tela_graf = Tk()
    var_barra_loading = DoubleVar()
    var_barra_loading.set(0)
    var_barra_loading_lbl = StringVar()
    var_barra_loading_lbl.set("TESTE " * 10)

    Loading(
        tela_graf,
        "loading...",
        orient_u=HORIZONTAL,
        maximum_u=50,
        length_u=500,
        mode_u="determinate",
        icon="icone.ico",
        progress_var=var_barra_loading,
        info_loading=var_barra_loading_lbl,
    )
    tela_graf.mainloop()
