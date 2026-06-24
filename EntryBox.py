from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                           QLineEdit, QPushButton, QWidget, QFrame)
from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QFont
from qtfontchooser import askfont


class EntryBoxColorBar(QDialog):   
	def __init__(self, master=None, **kw):
		super().__init__(master)
		self.setWindowTitle("Color Bar Settings")
		self.setModal(True)
		
		window = kw.pop("window", None)
		self.uti = kw.pop("uti", None)
		valorMax = kw.pop("valorMax", "")
		valorMin = kw.pop("valorMin", "")
		_vTicksCbar = kw.pop("vTicksCbar", "")
		_vDivTicks = kw.pop("vDivTicks", "")
		self.Dado_config = kw.pop("Dado_config", None)
		
		self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
		self.setGeometry(250, 370, 250, 370)
		self.fontt = "Nirmala\ UI 14 bold roman"
		self.protocol("WM_DELETE_WINDOW", self.quit)
		self.bind('<Return>',self.set_res)
		self.overrideredirect(1)
		self.resizable(False, False)
		pos_x=(window.winfo_x() +  (window.winfo_reqwidth()/3))
		pos_y=(window.winfo_y() +  (window.winfo_reqheight()/3))
		self.geometry(('250x%i+%i+%i')%(370,pos_x,pos_y))



		self.framePrincipal = Frame(self,relief=RIDGE,bg='gray',bd=5)
		self.framePrincipal.pack()
		
		
		self.frameTituloVmax = Frame(self.framePrincipal,relief=RIDGE,bg='gray',bd=5)
		self.frameTituloVmax.pack(fill=X)
		Label(self.frameTituloVmax,text="VMAX",font=self.fontt).pack(fill=X)
		self.frameEntryVmax = Frame(self.framePrincipal,relief=RIDGE,bg='gray',bd=5)
		self.frameEntryVmax.pack(fill=X)
		self.vMax = StringVar(self)
		self.vMax.set(valorMax)
		Entry(self.frameEntryVmax,font=self.fontt,validate = "key", validatecommand = vcmd_get_number, textvariable = self.vMax).pack(fill=X)



		self.frameTituloVmin = Frame(self.framePrincipal,relief=RIDGE,bg='gray',bd=5)
		self.frameTituloVmin.pack(fill=X)
		Label(self.frameTituloVmin,text="VMin",font=self.fontt).pack(fill=X)
		self.frameEntryVmin = Frame(self.framePrincipal,relief=RIDGE,bg='gray',bd=5)
		self.frameEntryVmin.pack(fill=X)
		self.vMin = StringVar(self)
		self.vMin.set(valorMin)
		Entry(self.frameEntryVmin,font=self.fontt,validate = "key", validatecommand = vcmd_get_number, textvariable = self.vMin).pack(fill=X)




		self.frameTicks = Frame(self.framePrincipal,relief=RIDGE,bg='gray',bd=5)
		self.frameTicks.pack(fill=X)
		Label(self.frameTicks,text="ticks",font=self.fontt).pack(fill=X)
		self.frameEntryTicks = Frame(self.framePrincipal,relief=RIDGE,bg='gray',bd=5)
		self.frameEntryTicks.pack(fill=X)
		self.vTicksCbar = StringVar(self)
		self.vTicksCbar.set(_vTicksCbar)
		Entry(self.frameEntryTicks,font=self.fontt,validate = "key", validatecommand = vcmd_get_number,textvariable = self.vTicksCbar).pack(fill=X)



		self.frameTicks = Frame(self.framePrincipal,relief=RIDGE,bg='gray',bd=5)
		self.frameTicks.pack(fill=X)
		Label(self.frameTicks,text="ticks p/ divisão",font=self.fontt).pack(fill=X)
		self.frameEntryTicks = Frame(self.framePrincipal,relief=RIDGE,bg='gray',bd=5)
		self.frameEntryTicks.pack(fill=X)
		self.vDivTicks = StringVar(self)
		self.vDivTicks.set(_vDivTicks)
		Entry(self.frameEntryTicks,font=self.fontt,validate = "key", validatecommand = vcmd_get_number,textvariable = self.vDivTicks).pack(fill=X)
		





		
		self.wait_visibility(self)
		self.grab_set()
		self.lift()
		Button(self,text='OK',bd=5,command=self.set_res,relief=RIDGE).pack(fill='both')




	def set_res(self,*event):
		self.res = [float(self.vMax.get().replace(",", ".")), float(self.vMin.get().replace(",", ".")), int(self.vTicksCbar.get()), int(self.vDivTicks.get())]
		self.quit()

	def quit(self):
		self.destroy()

	def get_res(self):
		return self.res

class EntryBox(QDialog):   
	def __init__(self,master = None,**kw):
		
		titulo = kw.pop("titulo","teste")
		font_u = kw.pop("font_u",None)
		valor = kw.pop("valor","")
		window = kw.pop("window",None)
		font_c = kw.pop("font_c",True)
		self.Numeric = kw.pop("Numeric",None)
		self.uti = kw.pop("uti",None)
		self.Dado_config = kw.pop("Dado_config",None)
		Toplevel.__init__(self, master)
		self.res = ''
		self.comfirm_font = False
		self.font_conf = font_c
		self.font = {'family' : 'Arial','weight' : 'bold','size'   : 18}
		
		self.fontt = "Nirmala\ UI 14 bold roman"
		self.protocol("WM_DELETE_WINDOW", self.quit)
		self.bind('<Return>',self.set_res)
		self.overrideredirect(1)
		self.resizable(False, False)
		if font_c == True:tam = 154
		else:tam = 122
		pos_x=(window.winfo_x() +  (window.winfo_reqwidth()/3))
		pos_y=(window.winfo_y() +  (window.winfo_reqheight()/3))
		self.geometry(('250x%i+%i+%i')%(tam,pos_x,pos_y))
		self.frame1 = Frame(self,relief=RIDGE,bg='gray',bd=5)
		self.frame1.pack()
		self.frame2 = Frame(self.frame1,relief=RIDGE,bg='gray',bd=5)
		self.frame2.pack(fill=X)
		Label(self.frame2,text=titulo,font=self.fontt).pack(fill=X)
		self.frame3 = Frame(self.frame1,relief=RIDGE,bg='gray',bd=5)
		self.frame3.pack()
		if self.Numeric:
			vcmd_get_number = (self.master.register(self.uti.onValidatesigla),'%S', '%s','%d',2,4)
			self.eb = Entry(self.frame3,font=self.fontt,validate = "key", validatecommand = vcmd_get_number)
		else:
			self.eb = Entry(self.frame3,font=self.fontt)
		self.eb.pack(fill=X)
		self.eb.insert(0,valor)
		self.wait_visibility(self)
		self.grab_set()
		self.lift()
		if self.font_conf:
			Button(self,text='Font',bd=5,command=lambda : self.selecionarfonte(valor),relief=RIDGE).pack(fill=X)

		Button(self,text='OK',bd=5,command=self.set_res,relief=RIDGE).pack(fill='both')
		self.eb.focus()
		self.eb.selection_to(END)

	def selecionarfonte(self,demo):
		self.comfirm_font = True
		font = askfont(self,str(demo),self.Dado_config.idioma(37))
		if font:
			del(font['slant'])
			del(font['underline'])
			del(font['overstrike'])
			self.font=font
	def set_res(self,*event):
		if self.Numeric:
			self.res = self.eb.get().replace(",",".")
		else:
			self.res = self.eb.get()
		self.quit()
	def quit(self):
		self.destroy()
	def get_res(self):
		retorno = None
		if self.font_conf: 
			retorno = self.res, self.font
		else:
			retorno = self.res
		return retorno


class EntryBoxTick(QDialog):
	def __init__(self,master=None,**kw):
		self.titulo = kw.pop("titulo","Teste")
		
		
		
		
		
		
		
		self.window = kw.pop("window",None)
		self.interface = kw.pop("interface",None)
		self.uti = kw.pop("uti",None)
		self.Dado_config = kw.pop("Dado_config",None)
		
		
		
		
		
		
		
		
		
		



		
		Toplevel.__init__(self, master)
		font = 'Levenim\ MT 10 bold roman'
		self.sizetick_tam = StringVar(self)
		self.sizetick_tam.set(self.Dado_config.Settings[self.interface]["fSizeLabelsTick_%s"%self.titulo])
		
		self.sizetick_larg_major = StringVar(self)
		self.sizetick_larg_major.set(self.Dado_config.Settings[self.interface]["fWidthTickMajor_%s"%self.titulo])

		self.sizetick_alt_major = StringVar(self)
		self.sizetick_alt_major.set(self.Dado_config.Settings[self.interface]["fHeightTickMajor_%s"%self.titulo])

		self.sizetick_larg_minor = StringVar(self)
		self.sizetick_larg_minor.set(self.Dado_config.Settings[self.interface]["fWidthTickMinor_%s"%self.titulo])

		self.sizetick_alt_minor = StringVar(self)
		self.sizetick_alt_minor.set(self.Dado_config.Settings[self.interface]["fHeightTickMinor_%s"%self.titulo])


		self.res_tam = '';self.res_lmj = '';self.res_amj = '';self.res_lmn = '';self.res_amn = ''
		self.bind('<Return>', self.set_res)
		self.overrideredirect(1)
		self.resizable(False, False)
		self.wait_visibility(self)
		self.grab_set()
		self.lift()
		
		
		
		
		
		pos_x=(self.window.winfo_x() +  (self.window.winfo_reqwidth()/3))
		pos_y=(self.window.winfo_y() +  (self.window.winfo_reqheight()/3))
		self.geometry(('+%i+%i')%(pos_x,pos_y))

		self.framep = []
		for rowf in range(8):
			self.framep.append(Frame(self,bd=3,bg='gray',relief=GROOVE))
			self.framep[rowf].pack(fill=X)

		Label(self.framep[0],relief=GROOVE,text='Tamanho Label '+self.titulo,font = font).pack(fill=X,expand=1)
		Button(self.framep[0],relief='ridge',text='-',font = {'font.size': 22},command=lambda :self.Tick_size(-.1,self.sizetick_tam)).pack(fill='x',side="left",expand=True)
		Button(self.framep[0],relief='ridge',text='+',font = {'font.size': 22},command=lambda :self.Tick_size(.1,self.sizetick_tam)).pack(fill='x',side="right",expand=True)
		Label(self.framep[0],relief='groove',textvariable=self.sizetick_tam,font = font,width=10).pack(fill='both',expand=1)

		Label(self.framep[1],relief=GROOVE,text='Largura Major '+self.titulo,font = font).pack(fill=X,expand=1)
		Button(self.framep[1],relief='ridge',text='-',font = {'font.size': 22},command=lambda :self.Tick_size(-.1,self.sizetick_larg_major)).pack(fill='x',side="left",expand=True)
		Button(self.framep[1],relief='ridge',text='+',font = {'font.size': 22},command=lambda :self.Tick_size(.1,self.sizetick_larg_major)).pack(fill='x',side="right",expand=True)
		Label(self.framep[1],relief='groove',textvariable=self.sizetick_larg_major,font = font,width=10).pack(fill='both',expand=1)

		Label(self.framep[2],relief=GROOVE,text='Altura Major '+self.titulo,font = font).pack(fill=X,expand=1)
		Button(self.framep[2],relief='ridge',text='-',font = {'font.size': 22},command=lambda :self.Tick_size(-.1,self.sizetick_alt_major)).pack(fill='x',side="left",expand=True)
		Button(self.framep[2],relief='ridge',text='+',font = {'font.size': 22},command=lambda :self.Tick_size(.1,self.sizetick_alt_major)).pack(fill='x',side="right",expand=True)
		Label(self.framep[2],relief='groove',textvariable=self.sizetick_alt_major,font = font,width=10).pack(fill='both',expand=1)

		Label(self.framep[3],relief=GROOVE,text='Largura Minor '+self.titulo,font = font).pack(fill=X,expand=1)
		Button(self.framep[3],relief='ridge',text='-',font = {'font.size': 22},command=lambda :self.Tick_size(-.1,self.sizetick_larg_minor)).pack(fill='x',side="left",expand=True)
		Button(self.framep[3],relief='ridge',text='+',font = {'font.size': 22},command=lambda :self.Tick_size(.1,self.sizetick_larg_minor)).pack(fill='x',side="right",expand=True)
		Label(self.framep[3],relief='groove',textvariable=self.sizetick_larg_minor,font = font,width=10).pack(fill='both',expand=1)

		Label(self.framep[4],relief=GROOVE,text='Altura Minor '+self.titulo,font = font).pack(fill=X,expand=1)
		Button(self.framep[4],relief='ridge',text='-',font = {'font.size': 22},command=lambda :self.Tick_size(-.1,self.sizetick_alt_minor)).pack(fill='x',side="left",expand=True)
		Button(self.framep[4],relief='ridge',text='+',font = {'font.size': 22},command=lambda :self.Tick_size(.1,self.sizetick_alt_minor)).pack(fill='x',side="right",expand=True)
		Label(self.framep[4],relief='groove',textvariable=self.sizetick_alt_minor,font = font,width=10).pack(fill='both',expand=1)


		vcmd = (self.register(self.uti.onValidatesigla),'%S', '%s','%d',2,4)
		Label(self.framep[5],text="Min "+self.titulo,font = font ).pack(side='left',fill='both',expand=True)	
		self.min_ax = StringVar(self)
		self.min_ax.set(self.Dado_config.Settings[self.interface]["fValueMin_Axes_%s_temp"%self.titulo])
		Entry(self.framep[5],width=5,textvariable = self.min_ax,exportselection=0,font = font,validate="key",validatecommand=vcmd).pack(fill=BOTH,side='left')
		self.max_ax = StringVar(self)
		self.max_ax.set(self.Dado_config.Settings[self.interface]["fValueMax_Axes_%s_temp"%self.titulo])
		Entry(self.framep[5],width=5,textvariable = self.max_ax,exportselection=0,font = font,validate="key",validatecommand=vcmd).pack(fill=BOTH,side='right')
		Label(self.framep[5],text="Max "+self.titulo,font = font ).pack(side='right',fill='both',expand=True)	
		

		
		Label(self.framep[6],text=self.Dado_config.idioma(29)+self.titulo,font = font ).pack(side='left',fill='both',expand=True)	
		self.passo_tick = StringVar(self)
		entry_passo = Entry(self.framep[6],width=5,exportselection=0,textvariable = self.passo_tick,validate="key",validatecommand=vcmd,font = font)
		entry_passo.pack(fill=BOTH,side='left')
		entry_passo.bind("<FocusOut>",lambda habil:self.habil(entry_passo, entry_n_rotulo))
		
		self.n_rotulo_tick = StringVar(self)
		entry_n_rotulo = Entry(self.framep[6],width=5,exportselection=0,textvariable =self.n_rotulo_tick,validate="key",validatecommand=vcmd,font = font)
		entry_n_rotulo.pack(fill=BOTH,side='right')
		entry_n_rotulo.bind("<FocusOut>",lambda habil:self.habil(entry_n_rotulo,entry_passo))
		Label(self.framep[6],text=self.Dado_config.idioma(31)+self.titulo,font = font ).pack(side='right',fill='both',expand=True)	

		Button(self.framep[7],relief='ridge',bd=1,text='OK',font = font,command=self.set_res).pack(fill=X,expand=True)

	def habil(self,objt1,objt2):
		if objt1.get().strip() != "":
			objt2.config(state="disabled",bg="gray")
		elif objt2['state']=="disabled":
			objt2.config(state="normal",bg="white")

	def Tick_size(self,v,var):
		var.set(("%.1f")%(float(var.get())+v))

	def set_res(self,*event):
		self.Dado_config.Settings[self.interface]["fSizeLabelsTick_%s"%self.titulo] = float(self.sizetick_tam.get())
		self.Dado_config.Settings[self.interface]["fHeightTickMajor_%s"%self.titulo] = float(self.sizetick_larg_major.get())
		self.Dado_config.Settings[self.interface]["fWidthTickMajor_%s"%self.titulo] = float(self.sizetick_alt_major.get())
		self.Dado_config.Settings[self.interface]["fWidthTickMinor_%s"%self.titulo] = float(self.sizetick_larg_minor.get())
		self.Dado_config.Settings[self.interface]["fHeightTickMinor_%s"%self.titulo] = float(self.sizetick_alt_minor.get())
		
		if self.min_ax.get():self.Dado_config.Settings[self.interface]["fValueMin_Axes_%s_temp"%self.titulo] = float(self.min_ax.get().replace(",","."))
		else:self.Dado_config.Settings[self.interface]["fValueMin_Axes_%s_temp"%self.titulo] = None

		if self.max_ax.get():self.Dado_config.Settings[self.interface]["fValueMax_Axes_%s_temp"%self.titulo] = float(self.max_ax.get().replace(",","."))
		else:self.Dado_config.Settings[self.interface]["fValueMax_Axes_%s_temp"%self.titulo] = None

		if self.passo_tick.get():
			self.Dado_config.Settings[self.interface]["fValue_Passo_Ticks_%s_temp"%self.titulo] = float(self.passo_tick.get().replace(",","."))
			self.Dado_config.Settings[self.interface]["iValue_Num_Ticks_%s_temp"%self.titulo] = None

		elif self.n_rotulo_tick.get():
			self.Dado_config.Settings[self.interface]["iValue_Num_Ticks_%s_temp"%self.titulo] = int(self.n_rotulo_tick.get().replace(",","."))
			self.Dado_config.Settings[self.interface]["fValue_Passo_Ticks_%s_temp"%self.titulo] = None
		
		else:
			self.Dado_config.Settings[self.interface]["iValue_Num_Ticks_%s_temp"%self.titulo] = None
			self.Dado_config.Settings[self.interface]["fValue_Passo_Ticks_%s_temp"%self.titulo] = None



		self.quit()

	def quit(self):
		self.destroy()

def askEntrytick(master=None,**kw):
	value = EntryBoxTick(master,**kw)
	value.wait_window(value)
	



def askEntry(master=None,**kw):
	value = EntryBox(master,**kw)
	value.wait_window(value)
	return value.get_res()


def askEntryBoxColorBar(master=None,**kw):
	value = EntryBoxColorBar(master,**kw)
	value.wait_window(value)
	return value.get_res()


