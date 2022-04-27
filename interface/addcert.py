import logging
from re import T
from textwrap import fill
import tkinter as tk
from tkinter import ttk
from tkinter import  *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from tkinter.ttk import *
from tkinter.messagebox import askquestion

from numpy import expand_dims
from database import CertificationDB
from datamodels import CertQuestion, Certification
from interface.styling import *
from pathlib import Path
import threading
from threading import Thread
import concurrent.futures
import csv
from time import sleep


logger = logging.getLogger()


class AddNewCertification(tk.Frame):
    def __init__(self, pr: Frame, new_cert: Button, practice: Button, learn: Button, tree: Treeview):
        super().__init__()

        self.top_frame = tk.Frame(self)
        self.mid_frame = tk.Frame(self)
        self.bottom_frame = tk.Frame(self)
        self.learn = learn
        self.practice = practice
        self.new_cert = new_cert
        self.tree_view = tree

        self.top_frame.pack(side=TOP, anchor=S, fill=BOTH, expand=True, padx=10)
        self.mid_frame.pack(side=TOP, anchor=E, fill='x', expand=True, padx=10)
        self.bottom_frame.pack(side=BOTTOM, anchor=S, fill=BOTH, expand=True, padx=10)

       
        self.cert_body = ttk.Label(self.top_frame, text='Certification Body:', justify=RIGHT)
        self.num_questions = ttk.Label(self.top_frame, text='Number of Questions:', justify=RIGHT)
        self.cert_name = ttk.Label(self.top_frame, text='Certification Name:', justify=RIGHT)
        self.passing_score = ttk.Label(self.top_frame, text='Passing Score:', justify=RIGHT)
        self.time_given = ttk.Label(self.top_frame, text=' Time given in Exam (mins):', justify=RIGHT)
        self.questions = ttk.Label(self.mid_frame, text='Questions File:', justify=RIGHT)
        
        self.cert_body_input = ttk.Entry(self.top_frame, justify=LEFT)
        self.cert_name_input = ttk.Entry(self.top_frame, justify=LEFT)
        self.num_questions_input = ttk.Entry(self.top_frame, justify=LEFT)
        self.passing_score_input = ttk.Entry(self.top_frame, justify=LEFT)
        self.time_given_input = ttk.Entry(self.top_frame, justify=LEFT)
        self.questions_input = ttk.Entry(self.mid_frame, justify=LEFT)
        
        #self.cancel_button = tk.Button(self, font=BOLD_FONT, text='Cancel', command=lambda: self.destroy())
        
        self.file_path_button = Button(self.mid_frame, text='select csv file', command=lambda: self._open_file())
        self.cancel_button = Button(self.bottom_frame, text='Cancel', command=lambda: self._cancel_add_cert())
        self.add_button = Button(self.bottom_frame, text='Add Cert', command=lambda: self._import_cert())
        
        
        self.cert_body.pack(side=LEFT, padx=2, pady=2)
        self.cert_body_input.pack(side=LEFT, padx=2, pady=2)
        self.cert_name.pack(side=LEFT, padx=2, pady=2)
        self.cert_name_input.pack(side=LEFT, padx=2, pady=2)
        self.num_questions.pack(side=LEFT, padx=2, pady=2)
        self.num_questions_input.pack(side=LEFT, padx=2, pady=2)
        self.passing_score.pack(side=LEFT, padx=2, pady=2)
        self.passing_score_input.pack(side=LEFT, padx=2, pady=2)
        self.time_given.pack(side=LEFT, padx=2, pady=2)
        self.time_given_input.pack(side=LEFT, padx=2, pady=2)
        self.questions.pack(side=LEFT, padx=2, pady=2)
        self.questions_input.pack(side=LEFT, padx=2, pady=2, expand=True, fill='x')
        self.file_path_button.pack(side=RIGHT, padx=5, pady=2) 
        self.cancel_button.pack(side=RIGHT, padx=2, pady=5)
        self.add_button.pack(side=RIGHT, padx=2, pady=10)
        
        self.enable_fields('disable')

    def enable_fields(self, status: str):
        for child in self.winfo_children():
            for c in child.winfo_children():
                c.configure(state=status)
        logger.info(f'enable_fields completed')
    
    def toggle_buttons(self, status: str):
        self.new_cert.configure(state= status)
        self.practice.configure(state= status)
        self.learn.configure(state= status)
        print(f'staus is : {status}')
        if status is 'enable':
            logger.debug(f'status is status: delete input fields')
            self.cert_body_input.delete(0, END)
            self.cert_name_input.delete(0, END)
            self.num_questions_input.delete(0, END)
            self.passing_score_input.delete(0, END)
            self.time_given_input.delete(0, END)
            self.questions_input.delete(0, END)
          
    
    def _cancel_add_cert(self):
        self.toggle_buttons('enable')
        self.enable_fields('disable')



    def _open_file(self):
        logger.debug('Open File called')
        self.questions_path = Path(askopenfilename(title='Choose a .csv file'))
        logger.info(f'Selected: {self.questions_path}')
        self.questions_input.delete(0,END)
        self.questions_input.insert(0,self.questions_path)
    
    
    def _import_cert(self):
        logger.debug('_import_cert called')
        cert_body = self.cert_body_input.get()
        cert_name = self.cert_name_input.get()
        num_questions = self.num_questions_input.get()
        passing_score = self.passing_score_input.get()
        exam_time = self.time_given_input.get()
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            cert_setup = AddCertificationController((cert_body, cert_name, num_questions, passing_score, exam_time),self.questions_path)
            future = executor.submit(cert_setup.add_cert)
            success = future.result()
            if success:
                messagebox.showinfo('Import complete', 'Import has been completed.')

        self.toggle_buttons('enable')
        self.enable_fields('disable')
        self.tree_view.delete()
        db = CertificationDB()
        certifications = db.get_certifications()
        self.tree_view.delete(*self.tree_view.get_children())
        if certifications:
            for cert in certifications:
                self.tree_view.insert('',tk.END, values=(cert.awarding_body, cert.cert_name, cert.num_questions, cert.passing_score, cert.exam_time, '0', '0'))



class AddCertificationController():
    def __init__(self, data, p) -> None:
        logger.debug('AddCertificationController: New object')
        self.certification = Certification(data)
        self.questions_path = p

    def add_cert(self):
        cert_sucess = True
        questions_sucess = True

        logger.debug(f'AddCertificationController.add_cert()')
        cert_db = CertificationDB()
        cert_sucess = cert_db.add_certification(self.certification)
        with open(self.questions_path, newline='', encoding='utf-8-sig') as cert_questions:
            reader = csv.reader(cert_questions, delimiter=',')
            next(reader) #NOTE: skips title line of csv. comment out if your input has no title line
            for line in reader:
                q = CertQuestion(line)
                result = cert_db.add_cert_questions(self.certification.awarding_body, self.certification.cert_name, q)
                if result != True:
                    questions_sucess = False

        if cert_sucess and questions_sucess:
            return True
        else:
            return False
       


                
        
