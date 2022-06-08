# -*- coding:UTF-8 -*-
import sndhdr
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


    def _show_question_info(self):
        for i in self.historys:
            cprint('■', 'green' if i.is_correct else 'red', end='')
        print('{:.3f}'.format(self.familiarity))

    def _show_question_stem(self):
        cprint(str(self.id) + ('[S]' if self.qusetion_type == '单选题' else '[M]') + self.stem,
               'grey' if self.qusetion_type == '单选题' else 'white', 'on_cyan' if self.qusetion_type == '单选题' else 'on_blue')
    
    def _show_choices(self):
        for abcd, c in zip(self.char_list, self.choices):
            if c.choice == '':
                break
            cprint(abcd+'.'+c.choice,  'grey', 'on_white')

    def show_question(self):
        self._show_question_info()
        self._show_question_stem()
        self._show_choices()

    def _show_choice_with_answer(self):
        for abcd, c in zip(self.char_list, self.choices):
            if c.choice == '':
                break
            if abcd in self.answer:
                cprint(abcd+'.'+c.choice, 'green',attrs=['bold','reverse'])
            else:
                cprint(abcd+'.'+c.choice)

    def _update_familiarity(self):
        familiarity = int(input(''))
        if familiarity >1 & familiarity <101:
            self.familiarity = familiarity
            session.query(Question).filter(
                Question.id == self.id).first().familiarity = familiarity
        
        
    def show_answer(self):
        self._show_question_info()
        self._show_question_stem()
        self._show_choice_with_answer()
        input()
        # self._update_familiarity()
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
            self.show_answer()
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
            familiarity = 50 # initiate familiarity
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

    @property
    def get_history(self):
        temp = session.query(History).filter(History.question_id == self.id).all()
        res = []
        for i in temp:
            res.append(i.get_time_used)
        return res

    @property
    def anverage_time(self):
        total_time = 0
        for i in self.historys:
            print(i.get_time_used[0])

    @property
    def count_chars(self):
        choice_length= 0
        for i in self.choices:
            choice_length+= len(i.choice)
        return len(self.stem)+ choice_length

    def speed(self):
        pass

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

    @property
    def get_time_used(self):
        time_used = 60
        if self.id != 1:
            time_used = self.date - session.query(History).filter(History.id == self.id-1).first().date
        return time_used,self.is_correct

if __name__ == '__main__':
    # Base.metadata.drop_all(engine)
    # Base.metadata.create_all(engine)
    a= session.query(Question).filter(Question.id ==4).first()
    a.anverage_time()