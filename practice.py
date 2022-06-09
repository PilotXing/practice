from sys import argv
from time import time
from Models import Question, Choice, engine, Base
from sqlalchemy.orm import sessionmaker
from random import shuffle


DBsession = sessionmaker(bind=engine)
session = DBsession()
# start_number = int(argv[1])
# end_number = int(argv[2])
start_number = 100
end_number = 200


def get_questions(session, category):
    res = session.query(Question).filter(
        Question.category == category).filter(Question.familiarity < 100).all()
    return res
def get_all_questions(session):
    return session.query(Question).all()

def select_question(questions):
    res=[]
    for question in questions:
        if question.familiarity<86 or question.anverage_time>15 or question.speed>0.2:
            res.append(question)
    return res
def show_answer(questions):
    for q in questions:
        q.show_answer()

def auto_practice(questions):
    shuffle(questions)
    wrong = 0
    correct = 0
    start_time = time()
    while questions:
        q = questions.pop(0)
        print('{:d}/{:d}/{:d}\t{speed:.2f}\t {anverage_time:.2f}'.format(len(questions),correct,wrong,speed=q.speed,anverage_time=q.anverage_time))
        q.show_question()
        if not q.check_answer():
            questions.insert(4, q)
            questions.insert(-1, q)
            wrong += 1
        correct += 1

        print('Time used:{time:.1f} TPQ:{TPQ:.1f}'.format(
            time=(time()-start_time), TPQ=(time()-start_time)/(correct+wrong)))


def show_category(session):
    categorys = session.query(Question.category).distinct().all()
    for cat in categorys:
        total = session.query(Question).filter(
            Question.category == cat[0]).filter(Question.familiarity != 100).count()
        print(categorys.index(cat), cat[0], total)
    return categorys[int(input('Select a category:'))][0]


if __name__ == '__main__':
    # c = show_category(session)
    questions = get_all_questions(session)
    auto_practice(select_question(questions))
