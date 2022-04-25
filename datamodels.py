from typing import *
import typing
import logging

logger = logging.getLogger()



class Certification:
    def __init__(self, data) -> None:
        logger.debug(f'New Certification Object created. Data len: {len(data)}')
        self.awarding_body = data[0].lower()
        self.cert_name = data[1].lower()
        self.num_questions = data[2]
        self.passing_score = data[3]
        self.exam_time = data[4]
        self.times_practice = data[5] if len(data) > 5 else '0' 
        self.times_passed = data[6] if len(data) > 6 else '0'
        self.questions: typing.List[CertQuestion] = []


class CertQuestion:
    def __init__(self, data) -> None:
        logger.debug('New CertQuestion Object created')
        self.catagory = data[0] 
        self.catagory_title = data[1]  
        self.difficulty = data[2] 
        self.region = data[3] 
        self.question = self._clean_str(data[4])
        self.opt_1 = self._clean_str(data[5]) 
        self.opt_2 = self._clean_str(data[6])    
        self.opt_3 = self._clean_str(data[7])    
        self.opt_4 = self._clean_str(data[8])    
        self.opt_5 = self._clean_str(data[9]) 
        self.ans = self._clean_str(data[10]) 
        self.explanation = self._clean_str(data[11]) 
    
    def _clean_str(self, input_string: str) -> str:
        return input_string.replace("'","")

