from tkinter import *
import curses


class Display:

	def __init__(self, root, one, two, three, four):
		topFrame = Frame(root)
		botFrame = Frame(root)

		topFrame.pack(side=TOP)
		botFrame.pack(side=BOTTOM)

		self.button1 = Button(topFrame, text=one)
		self.button2 = Button(topFrame, text=two)
		self.button3 = Button(botFrame, text=three)
		self.button4 = Button(botFrame, text=four)

		self.button1.config(height=14, width=47, activebackground=self.button1.cget('background'))
		self.button2.config(height=14, width=47, activebackground=self.button2.cget('background'))
		self.button3.config(height=13, width=47, activebackground=self.button3.cget('background'))
		self.button4.config(height=13, width=47, activebackground=self.button4.cget('background'))

		self.button1.pack(side=LEFT)
		self.button2.pack(side=LEFT)
		self.button3.pack(side=LEFT)
		self.button4.pack(side=LEFT)



	def update(self, one, two, three, four):
		#isplay(self, one, two, three, four)
		
		self.button1.configure(text = "test")
		#t_left.set(one)
		#t_right.set(two)
		#b_left.set(three)
		#b_right.set(four)


root = Tk()
root.overrideredirect(True)
root.config(cursor="none")

temp = Display(root, 1, 2, 3, 4)
#Display.update(root, 1, 2, 3, 4)

root.mainloop()
