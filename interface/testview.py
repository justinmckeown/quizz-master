from cProfile import label
from cmath import exp
import logging
import tkinter as tk
from tkinter import ttk
from tkinter import  *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from tkinter.ttk import *
from tkinter.messagebox import askquestion
from turtle import bgcolor
import typing

from numpy import size
from database import CertificationDB
from datamodels import CertQuestion, Certification
from interface.styling import *
from pathlib import Path
import threading
from threading import Thread
import concurrent.futures
import csv
logger = logging.getLogger()

class CertificationTest(tk.Toplevel):
    def __init__(self, parent, cert: typing.Dict, x_pos: int, y_pos: int):
        super().__init__(parent)
        self.body = cert.get('body')
        self.cert = cert.get('cert')

        self.title(f" {self.body.upper()} {self.cert.upper()} Test Simulation")
        self.geometry(f"+{x_pos + 80}+{y_pos + 30}")
        self.geometry("800x500")

        #Frames
        self.welcome_frame = tk.Frame(self)
        self.test_frame = tk.Frame(self)
        self.welcome_frame.pack(side="top", fill=BOTH, expand=TRUE, anchor=CENTER)

        #Welcome Frame
        welcome_text = f'This is a practice test for the {self.body} {self.cert} certification. You have {cert["duration"]} minutes to answer {cert["num_questions"]}. To pass you must answer {cert["pass_score"]} questions correctly.'
        self.welcome_text_label = ttk.Label(self.welcome_frame, text=welcome_text, font=("Arial", 16), anchor=CENTER)
        self.welcome_text_label.bind('<Configure>', lambda e: self.welcome_text_label.config(wraplength=self.welcome_text_label.winfo_width()))
        self.welcome_text_label.pack(padx=10, pady=10, expand=True, fill=BOTH, anchor=CENTER)


    
