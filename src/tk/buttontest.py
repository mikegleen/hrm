from tkinter import *
from functools import partial

class ButtonsTest:
   def __init__(self):
      self.top = Tk()
      self.top.title("Click a button to remove")
      Label(self.top, text="Click a button to remove it",
            bg="lightyellow").grid(row=0)

      self.top_frame = Frame(self.top, width =400, height=400)
      self.button_dic = {}
      self.buttons()
      self.top_frame.grid(row=1, column=0)

      Button(self.top_frame, text='Exit', bg="orange",
             command=self.top.quit).grid(row=10,column=0, columnspan=5)

      self.top.mainloop()

   ##-------------------------------------------------------------------         
   def buttons(self):
      b_row=1
      b_col=0
      for but_num in range(1, 11):
         ## create a button and send the button's number to
         ## self.cb_handler when the button is pressed
         b = Button(self.top_frame, text = str(but_num), 
                    command=partial(self.cb_handler, but_num))
         b.grid(row=b_row, column=b_col)
         ## dictionary key=button number --> button instance
         self.button_dic[but_num] = b

         b_col += 1
         if b_col > 4:
            b_col = 0
            b_row += 1

   ##----------------------------------------------------------------
   def cb_handler( self, cb_number ):
      print("\ncb_handler", cb_number)
      self.button_dic[cb_number].grid_forget()

##===================================================================
BT=ButtonsTest()

