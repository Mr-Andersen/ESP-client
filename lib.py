#!/usr/bin/env python3

import requests
import json
import socket

import tkinter as tk
import re


class TigraClient:
    def __init__(self, root='http://esp32.local:80/', method='post'):
        self.root = root if root[-1] == '/' else root + '/'
        self.default_method = {'get': self.get, 'post': self.post}[method]

    def get(self, pargs=[], jargs=None):
        if jargs is None:
            res = requests.get(self.root + '/'.join(pargs))
        else:
            res = requests.get(self.root + '/'.join(pargs),
                               json=json.dumps(jargs))
        dct = json.loads(res.text) if res.ok else {'error': 'NotOkResponce'}
        dct['ok'] = 'error' in dct
        return dct

    def post(self, pargs=[], jargs=None):
        if jargs is None:
            res = requests.post(self.root + '/'.join(pargs))
        else:
            res = requests.post(self.root + '/'.join(pargs),
                                json=json.dumps(jargs))
        dct = json.loads(res.text) if res.ok else {'error': 'NotOkResponce'}
        dct['ok'] = 'error' not in dct
        return dct

    def __call__(self, *args, **kwargs):
        return self.default_method(*args, **kwargs)

    def devices(self):
        return self(['devices'])

    def device(self, dev_name):
        return self(['device', dev_name])

    def get_value(self, dev_name, sens_name):
        return self(['get_value', dev_name, sens_name])

    def set_value(self, dev_name, sens_name, value):
        return self(['set_value', dev_name, sens_name], value)

    def start_stream(self, port, srcs, callback):
        '''
        conn.start_stream(12345, {'Gyro': ['X', 'Y'], 'Accel': ['Y', 'Z']}) -->
        data will flow like b"<Gyro-X><Gyro-Y><Accel-Y><Accel-Z>" to 12345 port
        '''
        if hasattr(self, 'sock'):
            self.sock.close()
        self.sock = socket.socket()
        self.sock.bind(('0.0.0.0', port))
        self.sock.listen()
        return self({'port': port, 'sources': srcs})


class SmartEntry(tk.Entry):
    def __init__(self, master, placeholder=None, text=None,
                 valid_re=None,
                 placeholder_fg='#b9b9b9', **kwargs):
        super().__init__(master, **kwargs)
        if placeholder is not None:
            self.placeholder = placeholder
            self.placeholder_fg = placeholder_fg
            self.valid_re = [re.compile(valid_re)]\
                if isinstance(valid_re, str) else (
                    [re.compile(i) for i in valid_re]
                    if isinstance(valid_re, (list, tuple)) else []
            )
            self.valid = True
            self.fg = self['fg']
            self.show = self['show']
            self.str_var = tk.StringVar(value=placeholder)
            self.config(textvariable=self.str_var, fg=placeholder_fg, show='')
            self.empty = True
            self.bind('<FocusIn>', self.on_focus)
            self.bind('<FocusOut>', self.off_focus)

            if text:
                self.str_var.set(text)
                self.config(fg=self.fg, show=self.show)
                self.off_focus()

    def on_focus(self, event=None):
        if self.empty:
            self.str_var.set('')
            self.config(show=self.show)
        self.config(fg=self.fg)

    def off_focus(self, event=None):
        self.empty = self.str_var.get() == ''
        if self.empty:
            self.str_var.set(self.placeholder)
            self.config(fg=self.placeholder_fg, show='')
        else:
            if len(self.valid_re) != 0 and\
               not any(i.fullmatch(self.str_var.get()) for i in self.valid_re):
                self.config(fg='#ee0000')
                self.valid = False
            else:
                self.valid = True
