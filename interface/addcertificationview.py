import logging
import tkinter as tk
from tkinter import ttk
from tkinter import  *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from tkinter.ttk import *
from tkinter.messagebox import askquestion
from database import CertificationDB
from datamodels import CertQuestion, Certification
from interface.styling import *
from pathlib import Path
import threading
from threading import Thread
import concurrent.futures
import csv
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

        self.cert_body = ttk.Label(self, text='Certification Body:', justify=tk.RIGHT)
        self.cert_body_input = ttk.Entry(self, justify=LEFT)
        
        self.cert_name = ttk.Label(self, text='Certification Name:', justify=RIGHT)
        self.cert_name_input = ttk.Entry(self, justify=LEFT)


        self.num_questions = ttk.Label(self, text='Number of Questions:', justify=tk.RIGHT)
        self.num_questions_input = ttk.Entry(self, justify=LEFT)

        self.passing_score = ttk.Label(self, text='Passing Score:', justify=tk.RIGHT)
        self.passing_score_input = ttk.Entry(self, justify=LEFT)

        self.time_given = ttk.Label(self, text=' Time given in Exam (mins):', justify=tk.RIGHT)
        self.time_given_input = ttk.Entry(self, justify=LEFT)

        
        self.questions = ttk.Label(self, text='Questions File:', justify=RIGHT)
        self.questions_input = ttk.Entry(self, justify=LEFT)

        self.file_path_button = tk.Button(self, font=BOLD_FONT, text='select csv file', bg='white', fg=BG_COLOR, command=lambda: self._open_file())
        
        self.cancel_button = tk.Button(self, font=BOLD_FONT, text='Cancel', bg='white', fg=BG_COLOR, command=lambda: self.destroy())
        self.add_button = tk.Button(self, font=BOLD_FONT, text='Import Questions', bg='white', fg=BG_COLOR, command=lambda: self._import_cert())

        #LAYOUT GRID...
        self.cert_body.grid(row=0, column=0, columnspan=1, sticky='E')
        self.cert_body_input.grid(row=0, column=1, columnspan=2, **self.padding)
        
        self.cert_name.grid(row=0, column=3, columnspan=1, sticky='E')
        self.cert_name_input.grid(row=0, column=4, columnspan=2, **self.padding)
        

        self.num_questions.grid(row=1, column=0, columnspan=1, sticky='E')
        self.num_questions_input.grid(row=1, column=1, columnspan=2, **self.padding)

        self.passing_score.grid(row=1, column=3, columnspan=1, sticky='E')
        self.passing_score_input.grid(row=1, column=4, columnspan=2, **self.padding)

        self.time_given.grid(row=2, column=0, columnspan=1, sticky='E')
        self.time_given_input.grid(row=2, column=1, columnspan=2, **self.padding)


        self.questions.grid(row=3, column=0, columnspan=1, sticky='E')
        self.questions_input.grid(row=3, column=1, columnspan=3, **self.padding, sticky='E,W')
        self.file_path_button.grid(row=3, column=4, columnspan=1, **self.padding, sticky='E,W')
        
        self.cancel_button.grid(row=5, column=3, columnspan=1, **self.padding, sticky='E,W,S')
        self.add_button.grid(row=5, column=4, columnspan=1, **self.padding, sticky='E,W,S')
    
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
                self.destroy()
            logger.debug(f'SUCCESS: {success}')
        
        #cert_setup = AddCertificationController((cert_body, cert_name, num_questions, passing_score, exam_time),self.questions_path)
        #cert_setup = threading.Thread(target=cert_setup.add_cert)
        #cert_setup.start()

        messagebox.showinfo('Import complete', 'Import has been completed.')
        #self.destroy()



        
    


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
       


                
        
