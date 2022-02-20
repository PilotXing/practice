import pdfplumber
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import insert

from Models import Question, Choice, Base, engine


def parse_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        res = []
        pages = pdf.pages
        for page in pages:
            table = page.extract_tables()
            for line in table[0]:
                res.append(line)
    res.pop(0)

    return process_data(res)
def process_data(data):
    res=[]
    for line in data:
        new_line = []
        for column in line:
            new_line.append(column.replace(
                '\n', '').replace('\'', '’'))
        new_line[5] = new_line[5].replace(',', '')
        new_line[0] = int(new_line[0])
        res.append(new_line)
    return res

def insert_db(data):
    DBsession = sessionmaker(bind=engine)
    session = DBsession()
    for line in data:
        question = Question(
            id=line[0], category=line[2], stem=line[4], answer=line[5], qusetion_type=line[3])
        for c in line[6:]:
            choice =Choice(choice=c,question=question)
            session.add(choice)
        session.add(question)
    session.commit()
    session.close()

if __name__ == '__main__':
    data = parse_pdf('test.pdf')
    insert_db(data)
    # new_category = Category(id =0, category_name = 'name')
    # session.add(new_category)
    # session.commit()
    # session.close()
