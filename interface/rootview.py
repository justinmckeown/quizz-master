import logging
import tkinter as tk
from tkinter import ttk
from tkinter import  Tk, Label, LabelFrame, Button, Entry, W, N, E, S, X,Y, Frame, LEFT, RIGHT, CENTER, Text, messagebox, Scrollbar, StringVar, OptionMenu, PhotoImage
from tkinter import ttk
from tkinter.ttk import *
from tkinter.messagebox import askquestion
from interface.styling import *
import threading
from interface.addcertificationview import AddCertification

logger = logging.getLogger()

class RootViewController(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title('Certification Trainer')
        self.minsize(750, 500)
        self.width = self.winfo_screenwidth()
        self.height = self.winfo_screenheight()
        self.file_count_display: int = 0
        self.protocol("WM_DELETE_WINDOW", self._ask_before_closing)
        self.configure(bg=BG_COLOR)

        #NOTE: Add Case Materials menu...
        self.menubar = tk.Menu(self)
        self.configure(menu=self.menubar)
        self.case_menu = tk.Menu(self.menubar, tearoff=False)
        self.menubar.add_cascade(label='Certifications', menu=self.case_menu)
        self.case_menu.add_command(label='Add New Certification...', command=self.add_question_set)
    

    def add_question_set(self):
        logger.debug(f'You chose Add a certificaiotn form the menu')
        x = self.winfo_rootx()
        y = self.winfo_rooty()
        add_cert = AddCertification(self, x, y)
        add_cert.grab_set()
        #self.new_window = tk.Toplevel(AddCertification(x, y))
        #self.add_person_window = tk.Toplevel(self)
        #self.add_person_window.configure(bg=BG_COLOR)
        #self.add_person_window.title('Add New Person')
        #self.add_person_window.attributes('-topmost', 'true')
        #self.add_person_window.geometry(f"+{x + 80}+{y + 30}")
        #self.add_person_window.geometry("600x200")
        #self.add_person_window.grab_set()
#
        #self.name = ttk.Label(self.add_person_window, text='Name:', justify=tk.RIGHT)
        #self.name_box = ttk.Entry(self.add_person_window, justify=LEFT)
        #self.address = ttk.Label(self.add_person_window, text='Address:', justify=RIGHT)
        #self.address_box = ttk.Entry(self.add_person_window, justify=LEFT)
        #self.telephone = ttk.Label(self.add_person_window, text='Telephone:', justify=RIGHT)
        #self.telephone_box = ttk.Entry(self.add_person_window, justify=LEFT)
        #self.is_suspect = ttk.Checkbutton(self.add_person_window, text = 'Suspect') 
        #self.is_person_of_interest = ttk.Checkbutton(self.add_person_window, text = 'Person of Interest') 
        #self.is_witness = ttk.Checkbutton(self.add_person_window, text = 'Witness')
        #self.is_victim = ttk.Checkbutton(self.add_person_window, text = 'Victim')
#
        #self.cancel_button = tk.Button(self.add_person_window, font=BOLD_FONT, text='Cancel', bg='white', fg=BG_COLOR, command=lambda: self.add_person_window.destroy())
        #self.add_button = tk.Button(self.add_person_window, font=BOLD_FONT, text='Add', bg='white', fg=BG_COLOR)
    

    def _ask_before_closing(self):
        '''
        Triggered when the user clicks the close button in the interface. 
        Used to contorl what happens just before the interface closes. 
        '''
        result = askquestion("Confirmation", "Do you really want to exit the application?")
        if result == "yes":
            #NOTE: Everytime you add a new exchange to connectors you need to do the same thing as is done for Binance below 
            logger.info('close any processes before shutting window')
            self.destroy()