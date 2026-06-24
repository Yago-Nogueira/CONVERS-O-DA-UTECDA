import qt_ui as tk
from util import Utilitarios,DadoIdioma
from qt_ui import *	
class EntryTick(tk.Toplevel):
	def __init__(self,master,plt=None):#,master,titulo = "asd",Valor="",font_c=True):
		Toplevel.__init__(self, master)
		
		# self.overrideredirect(True)
		self.resizable(False, False)

		font = 'Levenim\ MT 10 bold roman'
		windowWidth = self.winfo_reqwidth()
		windowHeight = self.winfo_reqheight()
		positionRight = int(self.winfo_screenwidth()/2 - windowWidth/2)
		positionDown = int(self.winfo_screenheight()/2 - windowHeight/2)
		# self.geometry(('%i+%i')%(positionRight,positionDown))
		
		self.wait_visibility(self)
		self.grab_set()
		# self.entry_family.focus_set()
		self.lift()



		self.uti = Utilitarios()
		self.Dado_config = DadoIdioma()
		
		self.framef = []
		for rowf in range(19):
			self.framef.append(Frame(self,bd=3,bg='gray',relief=GROOVE))
			self.framef[rowf].pack(fill=X)


		Label(self.framef[0],relief=GROOVE,text=self.Dado_config.idioma(115)).pack(fill=X,expand=1)
		self.sizetick = StringVar(self)
		self.sizetick.set('16')
		# self.sizetick.set(self.utiC.getSizeLabelsTick(0))
		Button(self.framef[1],relief='ridge',text='-',font = {'font.size': 22},command=lambda e='-' :self.uti.sizeTICK(self.sizetick,e,plt)).pack(fill='x',side="left",expand=True)		
		Button(self.framef[1],relief='ridge',text='+',font = {'font.size': 22},command=lambda e='+' :self.uti.sizeTICK(self.sizetick,e,plt)).pack(fill='x',side="right",expand=True)		
		Label(self.framef[1],textvariable=self.sizetick,font = font ,width=10).pack(fill='both',expand=True)
		Label(self.framef[2],relief='groove',text=self.Dado_config.idioma(116)).pack(fill='both',expand=1)
		self.largtick = StringVar(self)
		self.largtick.set('2.0')
		# self.largtick.set(self.utiC.getWidthTickMajor(0))
		Button(self.framef[3],relief='ridge',text='-',command=lambda e='-' :self.uti.largTICK(self.largtick,e,'major',plt)).pack(fill='x',side="left",expand=True)		
		Button(self.framef[3],relief='ridge',text='+',command=lambda e='+' :self.uti.largTICK(self.largtick,e,'major',plt)).pack(fill='x',side="right",expand=True)		
		Label(self.framef[3],textvariable=self.largtick,font = font ,width=10).pack(fill='both',expand=True)	
		Label(self.framef[4],relief='groove',text=self.Dado_config.idioma(117)).pack(fill='both',expand=1)
		self.alttick = StringVar(self)
		self.alttick.set('9.0')
		# self.alttick.set(self.utiC.getHeightTickMajor(0))
		Button(self.framef[5],relief='ridge',text='-',command=lambda e='-' :self.uti.altTICK(self.alttick,e,'major',plt)).pack(fill='x',side="left",expand=True)		
		Button(self.framef[5],relief='ridge',text='+',command=lambda e='+' :self.uti.altTICK(self.alttick,e,'major',plt)).pack(fill='x',side="right",expand=True)		
		Label(self.framef[5],textvariable=self.alttick,font = font ,width=10).pack(fill='both',expand=True)	
		Label(self.framef[6],relief='groove',text=self.Dado_config.idioma(118)).pack(fill='both',expand=1)
		self.largtickMinor = StringVar(self)
		self.largtickMinor.set(2.0)
		# self.largtickMinor.set(self.utiC.getWidthTickMinor(0))
		Button(self.framef[7],relief='ridge',text='-',command=lambda e='-' :self.uti.largTICK(self.largtickMinor,e,'minor',plt)).pack(fill='x',side="left",expand=True)		
		Button(self.framef[7],relief='ridge',text='+',command=lambda e='+' :self.uti.largTICK(self.largtickMinor,e,'minor',plt)).pack(fill='x',side="right",expand=True)		
		Label(self.framef[7],textvariable=self.largtickMinor,font = font ,width=10).pack(fill='both',expand=True)	
		Label(self.framef[8],relief='groove',text=self.Dado_config.idioma(119)).pack(fill='both',expand=1)
		self.alttickMinor = StringVar(self)
		self.alttickMinor.set('4.5')
		# self.alttickMinor.set(self.utiC.getHeightTickMinor(0))
		Button(self.framef[9],relief='ridge',text='-',command=lambda e='-' :self.uti.altTICK(self.alttickMinor,e,'minor',plt)).pack(fill='x',side="left",expand=True)		
		Button(self.framef[9],relief='ridge',text='+',command=lambda e='+' :self.uti.altTICK(self.alttickMinor,e,'minor',plt)).pack(fill='x',side="right",expand=True)		
		Label(self.framef[9],textvariable=self.alttickMinor,font = font ,width=10).pack(side='left',fill='both',expand=True)	
		vcmd = (self.register(self.uti.onValidatesigla),'%S', '%s','%d',2,4)
		Label(self.framef[10],text=self.Dado_config.idioma(19),font = font ).pack(side='left',fill='both',expand=True)	
		minX = IntVar(self)
		minX.set("")
		Entry(self.framef[10],width=4,textvariable = minX,exportselection=0,font = font,validate="key",validatecommand=vcmd).pack(fill=BOTH,side='left')
		maxX = IntVar(self)
		maxX.set("")
		Entry(self.framef[10],width=4,textvariable = maxX,exportselection=0,font = font,validate="key",validatecommand=vcmd).pack(fill=BOTH,side='right')
		Label(self.framef[10],text=self.Dado_config.idioma(20),font = font ).pack(side='right',fill='both',expand=True)	
		Label(self.framef[11],text=self.Dado_config.idioma(21),font = font ).pack(side='left',fill='both',expand=True)	
		minY = IntVar(self)
		minY.set("")
		Entry(self.framef[11],width=4,textvariable = minX,exportselection=0,font = font,validate="key",validatecommand=vcmd).pack(fill=BOTH,side='left')
		maxY = IntVar(self)
		maxY.set("")
		Entry(self.framef[11],width=4,textvariable = maxX,exportselection=0,font = font,validate="key",validatecommand=vcmd).pack(fill=BOTH,side='right')
		Label(self.framef[11],text=self.Dado_config.idioma(22),font = font ).pack(side='right',fill='both',expand=True)	


		# maxX = IntVar(self)

		# self.diaIHoras.pack(side='right',expand=1,fill=X)



		# Label(self.framef[10],text=self.Dado_config.idioma(19),font = font ).pack(fill='both',expand=True)	
		# Label(self.framef[10],text=self.Dado_config.idioma(20),font = font ).pack(fill='both',expand=True)	
		# Label(self.framef[10],text=self.Dado_config.idioma(21),font = font ).pack(fill='both',expand=True)	
		# Label(self.framef[10],text=self.Dado_config.idioma(22),font = font ).pack(fill='both',expand=True)	

		# Button(self.framef[10],text="OK",bd=5,command=self.set_res,relief="ridge").pack(fill='both',expand=True)



	def set_res(self):
		# self.res = self.eb.get()
		self.quit()
	def quit(self):
		self.destroy()
	# def get_res(self):
	# 	pass
		# if self.font_conf == True:
			# return self.res,self.font
		# else:
			# return self.res

def askEntrytick(master=None, plt = None):   
		value = EntryTick(master,plt)
		value.wait_window(value)
		# return value.get_res()

if __name__ == "__main__":

	root = Tk()
	# def example():
	askEntrytick(root)
	# print(a)
	# print(s)
	# print(resp())
	# Button(root, text='OK', command=example).pack(padx=10, pady=10)
	root.mainloop()