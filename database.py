
from asyncio.log import logger
import sqlite3
import sqlite3
import typing

from datamodels import CertQuestion, Certification



class CertificationDB:
    def __init__(self) -> None:
        self.conn = sqlite3.connect("certdatabase.db")
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

        self.cursor.execute("CREATE TABLE IF NOT EXISTS certification (awarding_body TEXT, cert_name TEXT, num_questions TEXT, passing_score TEXT, exam_time TEXT, times_practiced TEXT, times_passed TEXT, UNIQUE(awarding_body, cert_name))")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS question (awarding_body TEXT, cert_name TEXT, catagory TEXT, catagory_title TEXT, difficulty TEXT, region TEXT, question TEXT, opt1 TEXT, opt2 TEXT, opt3 TEXT, opt4 TEXT, opt5 TEXT, answer TEXT, explanation TEXT)")
    
    
    def get_certifications(self) -> typing.Union[typing.List[Certification], None]:
        logger.info(f'database.get_certifications()')
        sql_stmt = "SELECT * FROM certification"
        try:
            self.cursor.execute(sql_stmt)
            data = self.cursor.fetchall()
        except Exception as e:
            logger.info(f'database.get_certifications: {str(e)}')
        finally:
            return [Certification(x) for x in data] if data is not None else None

    
    
    def add_certification(self, cert: Certification) -> bool:
        success = True
        sql_stmt = f"INSERT OR IGNORE INTO certification (`awarding_body`, `cert_name`, `num_questions`, `passing_score`, `exam_time`) VALUES('{cert.awarding_body}', '{cert.cert_name}', '{cert.num_questions}', '{cert.passing_score}', '{cert.exam_time}')"
        logger.debug(f'SQL STATEMENT: {sql_stmt}')
        try:
            self.cursor.execute(sql_stmt)
        except Exception as e:
            success = False
            logger.exception(f'database.add_certification: {str(e)}')
        else:
            self.conn.commit()
        finally:
            return success
    
    def add_cert_questions(self, body: str, name: str, q: CertQuestion) ->bool:
        success = True
        sql_stmt = f"INSERT INTO question (`awarding_body`, `cert_name`, `catagory`, `catagory_title`, `difficulty`, `region`, `question`, `opt1`, `opt2`, `opt3`, `opt4`, `opt5`, `answer`, `explanation`) VALUES('{body}', '{name}', '{q.catagory}', '{q.catagory_title}', '{q.difficulty}', '{q.region}', '{q.question}', '{q.opt_1}', '{q.opt_2}', '{q.opt_3}', '{q.opt_4}', '{q.opt_5}', '{q.ans}', '{q.explanation}')"
        try:
            self.cursor.execute(sql_stmt)
        except Exception as e:
            success = False
            logger.exception(f'database.add_cert_questions: {str(e)}')
        else:
            self.conn.commit()
        finally:
            return success
    



  
