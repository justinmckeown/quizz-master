import logging
import typing
import tkinter as tk
from tkinter import ttk
from tkinter import  Tk, Label, LabelFrame, Button, Entry, W, N, E, S, X,Y, Frame, LEFT, RIGHT, CENTER, Text, messagebox, Scrollbar, StringVar, OptionMenu, PhotoImage
from tkinter import ttk
from tkinter.ttk import *
from tkinter.messagebox import askquestion

from scipy.misc import central_diff_weights
from interface.styling import *
from interface.addcert import *
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
        #self.configure(bg=BG_COLOR_2)

        #split screen in two halfs
        self.top_frame = tk.Frame(self)
        self.bottom_frame = tk.Frame(self)
        self.top_frame.pack(side=TOP, anchor=N, fill=BOTH, expand=True, padx=5, pady=5)
        self.bottom_frame.pack(side=BOTTOM, anchor=S, fill=BOTH, expand=True, padx=5, pady=5)

        #NOTE: Add menu...
        self.menubar = tk.Menu(self)
        self.configure(menu=self.menubar)
        self.case_menu = tk.Menu(self.menubar, tearoff=False)
        self.menubar.add_cascade(label='Certifications', menu=self.case_menu)
        self.case_menu.add_command(label='Add New Certification...', command=self.add_question_set)

        #Cert Tree display
        self.columns = ('cert_body', 'cert_name', 'num_questions', 'passing_score', 'exam_duration', 'practiced', 'passed')
        #self.report_header = LabelFrame(self, text='Certification in Database')
        self.tree = ttk.Treeview(self.top_frame, columns=self.columns, show='headings')
        self.tree.heading('cert_body', text='Certification Body')
        self.tree.heading('cert_name', text='Certification Name')
        self.tree.heading('num_questions', text='Number of Exam Questions')
        self.tree.heading('passing_score', text='Passing Score')
        self.tree.heading('exam_duration', text='Exam Duration')
        self.tree.heading('practiced', text='Times Practiced')
        self.tree.heading('passed', text='Times Passed')
        
        #self.report_text = Text(self.report_header)
        #self.scrollbar = Scrollbar(self.report_header, command=self.tree.yview)
        #self.tree['yscrollcommand'] = self.scrollbar.set
        self.tree.pack(side=TOP, anchor=N, fill=BOTH, expand=True)

        self.add_cert = Button(self.top_frame, text='Add New Cert', command=lambda: self.enable())
        self.practice = Button(self.top_frame, text='Practice', command= lambda: self._practice_questions())
        self.learn = Button(self.top_frame, text='Learn Mode')
        self.add_cert.pack(side=RIGHT, padx=5, pady=5)
        self.practice.pack(side=RIGHT, padx=5, pady=5)
        self.learn.pack(side=RIGHT, padx=5, pady=5)

        self.add_cert_view = AddNewCertification(self.bottom_frame, self.add_cert, self.practice, self.learn, self.tree)
        self.add_cert_view.pack(side=TOP, anchor=S, fill=BOTH, expand=TRUE)

        self.add_to_table()

    def _practice_questions(self):
        logger.debug('rootview._practice_questions() called')
        curItem = self.tree.focus()
        print(self.tree.item(curItem))
        #TODO: Returns dictionary you need the list of values with key 'values' use first two to get associated questions. 



    def add_to_table(self):
        db = CertificationDB()
        certifications = db.get_certifications()
        if certifications:
            for cert in certifications:
                self.tree.insert('',tk.END, values=(cert.awarding_body, cert.cert_name, cert.num_questions, cert.passing_score, cert.exam_time, '0', '0'))


    def enable(self):
        self.add_cert.configure(state='disable')
        self.practice.configure(state='disable')
        self.learn.configure(state='disable')
        self.add_cert_view.enable_fields('enable')
      
           

    

    def add_question_set(self):
        logger.debug(f'You chose Add a certification form the menu')
        x = self.winfo_rootx()
        y = self.winfo_rooty()
        add_cert = AddCertification(self, x, y)
        add_cert.grab_set()

    

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