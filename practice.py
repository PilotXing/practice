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


def auto_practice(session, category):
    res = session.query(Question).filter(
        Question.category == category).filter(Question.familiarity < 100).all()
    shuffle(res)
    wrong = 0
    correct = 0
    start_time = time()
    while res:
        q = res.pop(0)
        print(str(len(res)) + '|'+str(correct)+'/'+str(wrong) , q.familiarity)
        q.show_question()
        if not q.check_answer():
            res.insert(4, q)
            res.insert(-1, q)
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
    c = show_category(session)
    auto_practice(session, c)
