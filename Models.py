# -*- coding:UTF-8 -*-
from sqlalchemy import Column, INTEGER, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import backref, relationship
from sqlalchemy.orm.session import make_transient, sessionmaker
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.selectable import Select
from sqlalchemy.sql.sqltypes import DateTime
from datetime import datetime
from termcolor import cprint
from os import get_terminal_size
import sys

width, hight = get_terminal_size()

engine = create_engine("sqlite:///data.db")
Base = declarative_base()


DBsession = sessionmaker(bind=engine)
session = DBsession()


class Question(Base):

    __tablename__ = 'questions'
    char_list = 'ABCD'
    id = Column(Integer, primary_key=True, autoincrement=True)
    choices = relationship('Choice', backref='question')
    historys = relationship('History', backref='question')
    category = Column(String)
    stem = Column(String)
    answer = Column(String)
    familiarity = Column(Integer, default=-1)
    qusetion_type = Column(String)

    def show_question(self):
        cprint(str(self.id) + ('[S]' if self.qusetion_type == '单选题' else '[M]') + self.stem,
               'grey' if self.qusetion_type == '单选题' else 'white', 'on_cyan' if self.qusetion_type == '单选题' else 'on_blue')
        for abcd, c in zip(self.char_list, self.choices):
            if c.choice == '':
                break
            cprint(abcd+'.'+c.choice,  'grey', 'on_white')

    def _show_answer(self):
        print(self.answer)

    def _remove(self):
        q = session.query(Question).filter(Question.id == self.id).first()
        q.familiarity = 100
        session.commit()
        session.close()

    def check_answer(self):
        raw_answer = input("ANSWER((Q)uit (N)ext (S)how (R)emove):")

        my_answer = ''
        for i in raw_answer:
            if i not in 'abcdABCDQqSsRr1234':
                print('invalid input')
                break
        # convert 1234 to abcd
        for i in raw_answer:
            if i in '1234':
                my_answer += chr(int(i)+ord('a')-1)
            else:
                my_answer += i

        if my_answer and my_answer.lower() in 'q':
            sys.exit()

        elif my_answer.lower() in 's':
            self._show_answer()
            return False

        elif my_answer.lower() in 'r':
            self._remove()
            return True

        elif sorted(my_answer.lower()) == sorted(self.answer.lower()):
            cprint('✓'*width, 'grey', 'on_green')
            self.update_last_practice(my_answer, True)
            return True
        else:
            cprint('x'*width, 'grey', 'on_red')
            self.update_last_practice(my_answer, False)
            return False

    def update_last_practice(self, selected, is_correct):
        history = History(question_id=self.id,
                          selected_answer=selected,
                          is_correct=is_correct)
        familiarity = session.query(Question).filter(
            Question.id == self.id).first().familiarity
        if familiarity == None or familiarity == -1:
            familiarity = 50
        new_familiarity = 100 - (100-familiarity)/3 * \
            2 if is_correct else familiarity/3
        session.query(Question).filter(
            Question.id == self.id).first().familiarity = new_familiarity
        session.add(history)
        session.commit()
        session.close()
        return 0
        # 写入日期
        # 更新熟练度


class Choice(Base):
    __tablename__ = 'choices'
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    question_id = Column(Integer, ForeignKey('questions.id'))
    choice = Column(String)


class History(Base):
    __tablename__ = 'historys'
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    question_id = Column(Integer, ForeignKey('questions.id'))
    date = Column(DateTime, default=datetime.now)
    selected_answer = Column(String)
    is_correct = Column(Integer)


if __name__ == '__main__':
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    pass
