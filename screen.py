from Tkinter import *
import thread, time

class App():
	def __init__(self, master):
		self.master = master
		
		frame = Frame(master)
		frame.pack()
		
def display(threadName):
	print("Starting " + threadName)

	root = Tk()
	root.wm_title("The Best Extruder")
	app = App(root)
	root.geometry("480x800")
	root.mainloop()	
	'''
	root = Tk()
	topFrame = Frame(root)
	topFrame.pack(side=TOP)
	bottomFrame = Frame(root)
	bottomFrame.pack(side=BOTTOM)
	
	button1 = Button(topFrame, text="Start", bg="white", fg="green")
	button2 = Button(topFrame, text="End", bg="white", fg="blue")
	button3 = Button(topFrame, text="Exit", bg="white", fg="red", command=exitProgram)
	button4 = Button(bottomFrame, text="Bottom", bg="black", fg="yellow")
	button5 = Button(bottomFrame, text="Fill", bg="black", fg="yellow")
	entry1 = Entry(bottomFrame)
	
	c = Checkbutton(bottomFrame, text="checkbox")
	
	button1.pack(side=LEFT, fill=X)
	button2.pack(side=LEFT, fill=Y)
	button3.pack(side=LEFT)
	
	button4.grid(row=0,column=0, sticky="N")
	button5.grid(row=0,column=1, sticky="E")
	entry1.grid(row=1,column=0, sticky="S")
	c.grid(columnspan=2, sticky="S")
	
	theLabel = Label(topFrame, text="hi hello world")
	theLabel.pack(side=TOP)
	
	root.mainloop()
'''
