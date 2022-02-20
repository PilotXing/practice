import npyscreen
import os
import curses
from Models import Question, Choice
TERMINAL_WIDTH=os.get_terminal_size()[0]



# class MyMultiSelect(npyscreen.MultiSelect):
#     def set_up_handlers(self):
#         super(MyMultiSelect, self).set_up_handlers()
#         self.handlers.update({
#             curses.ascii.CR:self.h_submit,
#             })
#    
#     def h_submit(self):
#         self.how_exited=1
#             
#     def h_select_exitqqq(self, ch):
#         # self.how_exited=True
#         self.values[1] =ch
# 
class PickingOptions(npyscreen.Form):
    min_c =30

    def afterEditing(self):
        self.parentApp.setNextForm(None)

    def _submit(self,ch):
        self.info.value = str(self.MultiChoice.value)


    def create(self):
        self.stem = 'stem'
        new_handlers = {curses.ascii.CR:self._submit,
                "n":self._submit} 

        self.add_handlers(new_handlers)
        self.myFixed = self.add(npyscreen.TitleFixedText,value='self.stem',name='1.')

        self.MultiChoice= self.add(
                npyscreen.MultiSelect,
                max_height=-2,
                value=[1,],
                values=['a','b','c','d'])
        self.info =self.add(npyscreen.Textfield, name='textField',value ='value')
        self.add_handlers({'a':self.A_selected})
        self.add_handlers({'b':self.B_selected})
        self.add_handlers({'c':self.C_selected})
        self.add_handlers({'d':self.D_selected})

    def A_selected(self,key):
        if 0 not in self.MultiChoice.value:
            self.MultiChoice.value.append(0)
        else:
            self.MultiChoice.value.remove(0)

    def B_selected(self,key):
        if 1 not in self.MultiChoice.value:
            self.MultiChoice.value.append(1)
        else:
            self.MultiChoice.value.remove(1)

    def C_selected(self,key):
        if 2 not in self.MultiChoice.value:
            self.MultiChoice.value.append(2)
        else:
            self.MultiChoice.value.remove(2)

    def D_selected(self,key):
        if 3 not in self.MultiChoice.value:
            self.MultiChoice.value.append(3)
        else:
            self.MultiChoice.value.remove(3)

class MyApplication(npyscreen.NPSAppManaged):
   def onStart(self):
       # TODO query database
       # self.addForm('MAIN', TextWidget, name='Test Text')
       # A real application might define more forms here.......
       self.addForm('MAIN', PickingOptions,columns=TERMINAL_WIDTH, scroll_exit=True,return_exit=True,exit_down=True)
if __name__ == '__main__':
   TestApp = MyApplication().run()
