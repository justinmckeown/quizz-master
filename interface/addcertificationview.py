import logging
import tkinter as tk
from tkinter import ttk
from tkinter import  *
from tkinter.ttk import *
from tkinter.messagebox import askquestion
from interface.styling import *
import threading

logger = logging.getLogger()

class AddCertification(tk.Toplevel):
    def __init__(self, parent, x_pos: int, y_pos: int):
        super().__init__(parent)
        self.configure(bg=BG_COLOR)
        self.title('Add New Certification')
        #self.attributes('-topmost', 'true')
        self.geometry(f"+{x_pos + 80}+{y_pos + 30}")
        self.geometry("600x200")

        #Styling
        self.padding = {'padx' : 5, 'pady' : 5}
        self.entry_font = {'font' : ('Helvetica', 11)} 
        self.style = ttk.Style()
        logger.debug(self.style.theme_names())
        self.style.configure("TLabel", font=('Helvetica', 11),foreground=FG_COLOR, background=BG_COLOR)
        self.style.configure("TCheckbutton", font=('Helvetica', 11),foreground=FG_COLOR, background=BG_COLOR)
        self.style.configure("TMenubutton", font=('Helvetica', 11),foreground=FG_COLOR, background=BG_COLOR)
        self.style.configure("TButton", font=('Helvetica', 11), background=BG_COLOR)
        #TODO: Add inputs for: Num Questions in exam, Passing Score, Time given in live exam  

        self.certification_body = ttk.Label(self, text='Certification Body:', justify=tk.RIGHT)
        self.certification_body_input = ttk.Entry(self, justify=LEFT)
        self.address = ttk.Label(self, text='Certification Name:', justify=RIGHT)
        self.address_box = ttk.Entry(self, justify=LEFT)
        self.telephone = ttk.Label(self, text='Questions File:', justify=RIGHT)
        self.telephone_box = ttk.Entry(self, justify=LEFT)

        self.cancel_button = tk.Button(self, font=BOLD_FONT, text='Cancel', bg='white', fg=BG_COLOR, command=lambda: self.destroy())
        self.add_button = tk.Button(self, font=BOLD_FONT, text='Import Questions', bg='white', fg=BG_COLOR)

        self.certification_body.grid(row=0, column=0, columnspan=1)
        self.certification_body_input.grid(row=0, column=1, columnspan=2, **self.padding)
        self.address.grid(row=1, column=0, columnspan=1)
        self.address_box.grid(row=1, column=1, columnspan=2, **self.padding)
        self.telephone.grid(row=2, column=0, columnspan=1)
        self.telephone_box.grid(row=2, column=1, columnspan=2, **self.padding)
        self.cancel_button.grid(row=4, column=3, columnspan=1, **self.padding)
        self.add_button.grid(row=4, column=4, columnspan=1, **self.padding)
        
