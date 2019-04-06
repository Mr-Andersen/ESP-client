#!/usr/bin/env python3

import tkinter as tk
from tkinter import font
from tkinter import ttk

from lib import TigraClient, SmartEntry


def make_connect(addr):
    def monitor(event):
        pass

    def connect(event):
        conn = TigraClient(addr)
        devices = dict.fromkeys(conn.devices(), None)
        devices = {dev: conn.device(dev) for dev in devices}
        frame = tk.Frame()
        nb.add(frame, text=addr)

        inner_nb = ttk.Notebook(frame)
        start_button = tk.Button(frame, text='Monitor!')
        start_bind

        inner_nb.grid(row=0, column=0)
        start_button.grid(row=1, column=0)
    return connect


if __name__ == '__main__':
    import sys
    print(sys.version)

    root = tk.Tk()
    root.config(width=800, height=600, padx=10, pady=10)

    global nb
    nb = ttk.Notebook(root)

    addr = SmartEntry(root, 'Mc address', 'http://esp32.local',
                      r'(https?://)?\w+(\-\w+)?(\.\w+(\-\w+)?)*'
                      r'\.[A-Za-z]+(:\d+)?/?',
                      font=font.Font(size=24))
    addr.bind('<Return>', make_connect(addr.str_var.get()))

    nb.add(addr, text='Startup')
    nb.pack()
    root.mainloop()
