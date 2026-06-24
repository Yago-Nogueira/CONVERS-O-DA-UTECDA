#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pyqt_utils import FigureCanvasQTAgg, NavigationToolbar2QT 
from matplotlib.ticker import LinearLocator , FuncFormatter,IndexLocator
from datetime import datetime, timedelta, date
from pyqt_utils.filedialog import askdirectory
from pyqt_utils import ttk, messagebox,Toplevel
import matplotlib.ticker as ticker
from qtfontchooser import askfont
from qt_calendar import DateEntry
import matplotlib.pyplot as plt
import matplotlib,os,calendar
from util import Utilitarios,VerticalScrolledFrame,DadoIdioma
matplotlib.use("QtAgg")
from pyqt_utils import *  
import pyqt_utils as ui
import numpy as np
class GraficocontornoINDV(ui.Toplevel):
	def __init__(self,root):
		Toplevel.__init__(self,root)
		plt.rc('font', weight='bold')
		plt.rc('axes',linewidth=2)
		matplotlib.rcParams['xtick.direction'] = 'out'
		matplotlib.rcParams['ytick.direction'] = 'out'
		# matplotlib.rcParams['xtick.direction'] = 'out'
		# matplotlib.rcParams['ytick.direction'] = 'out'
		self.fonty = self.fontt = self.fontb = self.fontx = {'family' : 'Arial',
		'weight' : 'bold',
		'size'   : 18}
		self.matrizstd_list=[]
		self.root = root
		self.uti = Utilitarios()
		# self.utiC = DadoIdioma()
		self.Dado_config = DadoIdioma()
		self.titulo = ''#(("%s-%s-%.2i") % (sigla.lower(),dataI.year,dataI.month)) 
		self.titulox = self.Dado_config.idioma(40)
		self.tituloy = self.Dado_config.idioma(41)
		self.titulob = "VTEC"
		self.filedir = r"C:\Users\Mateus_Pillat\Google Drive\Estágio\Dados\STD"
		# self.filedir = r"C:\Users\Mateus-Not\Google Drive\Estágio\Dados\STD"
		self.title(self.Dado_config.idioma(38))
		self.framep = VerticalScrolledFrame(self) #Frame(self,bd=3,relief=GROOVE,bg='gray')
		self.framep.pack(side='left',fill='both')
		nb = ttk.Notebook(self)
		self.page1 = Frame(self)
		self.page2 = Frame(self)
		self.page1.bind('<FocusIn>',lambda e: self.refreshCanvas())
		self.fig, self.axes = plt.subplots()
		self.canvas = FigureCanvasQTAgg(self.fig,self.page1)
		self.canvas.draw()
###############################|Has deprecated ... breves...|#########################################################################################################################################################		
		self.toolbar = NavigationToolbar2QT(self.canvas, self.page1)
		# self.canvas.get_widget().pack(side=ui.BOTTOM, fill=ui.BOTH, expand=True)
		# self.canvas._qt_canvas.pack(side=ui.TOP, fill=ui.BOTH, expand=True)
		# self.toolbar.update()
		nb.add(self.page1,text =self.Dado_config.idioma(7))
		nb.add(self.page2,text =self.Dado_config.idioma(17))
		nb.pack(expand=1,side='right',fill='both')
		self.vargrid = BooleanVar(self)
		self.varsave = BooleanVar(self)
		self.varmatriz = BooleanVar(self)		
		self.framepg1 = Frame(self.framep.interior,bd=3,bg='gray',relief=GROOVE)
		self.framepg1.pack(side='left',fill=BOTH)
		self.framepg2 = Frame(self.framepg1,bd=3,bg='gray',relief=GROOVE)
		self.framepg2.pack(side='top',fill=BOTH,expand=1)#-----------------####Expand para lista preencher..
		self.framepg3 = Frame(self.framepg1,bd=3,bg='gray',relief=GROOVE)
		self.framepg3.pack(fill=BOTH)
		self.framepg4 = Frame(self.framepg1,bd=3,bg='gray',relief=GROOVE)
		self.framepg4.pack(fill=BOTH)
		self.dirstd = Button(self.framepg2, text=self.Dado_config.idioma(18),command=self.selecionar,relief=RIDGE)
		self.dirstd.pack(side='bottom',fill=X)
		self.listaobs = Listbox(self.framepg2,exportselection=0,relief='groove',selectmode='single')
		self.listaobs.pack(side='left',fill=BOTH,expand=1)
		self.listaobs.bind("<<ListboxSelect>>",lambda p:self.plotar())
		self.sb = Scrollbar(self.framepg2)
		self.sb.pack(side=RIGHT,fill=Y)
		self.sb.configure(command=self.listaobs.yview)
		self.listaobs.configure(yscrollcommand=self.sb.set)
		

		Label(self.framepg3,text=self.Dado_config.idioma(53)).pack(fill=X)
		self.cal = DateEntry(self.framepg3, background='darkblue',foreground='white', borderwidth=2)#,year = 2017,day=1,month=9)
		self.cal.bind('<<DateEntrySelected>>',self.atuaAno)
		self.cal.pack(fill=X)
		Label(self.framepg3,text=self.Dado_config.idioma(54)).pack(fill=X)
		self.cal2 = DateEntry(self.framepg3, background='darkblue',foreground='white', borderwidth=2)#,year = 2017,day=30,month=9)
		self.cal2.pack(fill=X)
		self.ano = 0
		# self.atuaAno()
		n_list,conteudo_lista = self.uti.Refresh_list_obs(self.filedir,int(2019),True)
		# self.listaobs.configure(source=(conteudo_lista+[item + " ("+ self.Dado_config.idioma(144) +")" for item in n_list]) )
		# self.listaobs.configure(source=[item + " ("+ self.Dado_config.idioma(144) +")" for item in n_list])
		[self.listaobs.insert(END, item) for item in conteudo_lista]
		[self.listaobs.insert(END, item + " ("+ self.Dado_config.idioma(144) +")") for item in n_list]

		
		self.framel=[]
		for rowl in range(8):
			self.framel.append(Frame(self.framepg4,bd=3,bg='gray',relief=GROOVE))
			self.framel[rowl].pack(fill=BOTH)


		Label(self.framel[0],relief=GROOVE,text=self.Dado_config.idioma(21),width=10).pack(side='left')
		vcmd = (self.register(self.uti.onValidatesigla),'%S', '%s','%d',2,4)
		self.diaIHoras = Entry(self.framel[0],exportselection=0,validate="key",validatecommand=vcmd)
		self.diaIHoras.pack(side='right',expand=1,fill=X)
		Label(self.framel[1],relief=GROOVE, text=self.Dado_config.idioma(22),width=10).pack(side='left')		
		self.diaFHoras = Entry(self.framel[1],exportselection=0,validate="key",validatecommand=vcmd)	
		self.diaFHoras.pack(side='right',expand=1,fill=X)		
		Label(self.framel[2],relief=GROOVE, text=self.Dado_config.idioma(23)).pack(side='left',expand=1,fill=X)				
		self.txtvmax = Entry(self.framel[2],width=6,exportselection=0,validate="key",validatecommand=vcmd)
		self.txtvmax.pack(side='right',fill=X,expand=1)
		self.vargrid_X = BooleanVar(self)
		self.vargrid_Y = BooleanVar(self)


		Label(self.framel[3],text=self.Dado_config.idioma(24),relief=GROOVE).pack(fill=X)
		Label(self.framel[3],text="Horizontal",relief=GROOVE).pack(side='left',fill=Y)
		Checkbutton(self.framel[3],variable=self.vargrid_X,width=5,command=self.atua_grid_X).pack(side='left')
		Checkbutton(self.framel[3],variable=self.vargrid_Y,width=5,command=self.atua_grid_Y).pack(side='right')
		Label(self.framel[3],text="Vertical",relief=GROOVE).pack(side='right',fill=Y)	
		Label(self.framel[4],text=self.Dado_config.idioma(130),relief=GROOVE).pack(fill=X)	
		self.DateFormat = IntVar(self)
		self.DateFormat.set(1)
		Radiobutton(self.framel[4],variable=self.DateFormat,relief=GROOVE,command=self.refreshCanvas ,value=1,text=self.Dado_config.idioma(40)).pack(side='left',fill=X,expand=1)
		Radiobutton(self.framel[4],variable=self.DateFormat,relief=GROOVE,command=self.refreshCanvas ,value=0,text=self.Dado_config.idioma(135)).pack(side='right',fill=X,expand=1)		
		Label(self.framel[5],relief=GROOVE,text=self.Dado_config.idioma(25)).pack(side='left',fill=BOTH,expand=1)
		self.checksave = Checkbutton(self.framel[5],variable=self.varsave,width=5,command=self.save_png)
		self.checksave.pack(side='right')
		Label(self.framel[6],relief=GROOVE,text=self.Dado_config.idioma(91)).pack(side='left',fill=BOTH,expand=1)
		self.checkmat = Checkbutton(self.framel[6],variable=self.varmatriz,width=5,command=self.salvar_matriz)
		self.checkmat.pack(side='right')
		# self.btnatualiza = Button(self.framel[7], width=20, text=self.Dado_config.idioma(26),relief=RIDGE, command=self.plotar)
		#########################PAGE PROPRIEDADES#######################
		self.framefront = Frame(self.page2,bd=3,bg="blue",relief=GROOVE)
		self.framefront.pack(side='left',fill=Y)
		self.framep=[]
		for rowp in range(10):
			self.framep.append(Frame(self.framefront,bd=3,bg='gray',relief=GROOVE))
			self.framep[rowp].pack(fill=X)
			#self.framep[rowp].grid(column=0,row=rowp+1,sticky=E+W)
		Label(self.framep[0], relief=GROOVE,text=self.Dado_config.idioma(27)).pack(fill='both')
		Label(self.framep[1] ,relief=GROOVE,text=self.Dado_config.idioma(28)).pack(side='left',fill=X,expand=1)
		vcmd = (self.register(self.uti.onValidatesigla),'%S', '%s','%d',2,10)
		self.ntickx = Entry(self.framep[1],exportselection=0,validate="key",validatecommand=vcmd)
		self.ntickx.pack(side='right',fill=X)
		self.ntickx.bind("<FocusOut>",lambda habil:self.habil(self.ntickx,self.nlblx))
		Label(self.framep[2], relief=GROOVE,text=self.Dado_config.idioma(29)).pack(side='left',fill=X,expand=1)	
		# vcmd = (self.register(self.uti.onValidatesigla),'%S', '%s','%d',2,10)
		self.nticky = Entry(self.framep[2],exportselection=0,validate="key",validatecommand=vcmd)
		self.nticky.pack(side='right',fill=X)
		self.nticky.bind("<FocusOut>",lambda habil=1:self.habil(self.nticky,self.nlbly))
		Label(self.framep[3], relief=GROOVE,text=self.Dado_config.idioma(30)).pack(side='left')	
		# vcmd = (self.register(self.uti.onValidatesigla),'%S', '%s','%d',2,10)
		self.nlblx = Entry(self.framep[3],exportselection=0,validate="key",validatecommand=vcmd)
		self.nlblx.pack(side='right')
		self.nlblx.bind("<FocusOut>",lambda habil:self.habil(self.nlblx,self.ntickx))
		Label(self.framep[4],relief=GROOVE, text=self.Dado_config.idioma(31)).pack(side='left')		
		# vcmd = (self.register(self.uti.onValidatesigla),'%S', '%s','%d',2,10)
		self.nlbly = Entry(self.framep[4],exportselection=0,validate="key",validatecommand=vcmd)
		self.nlbly.pack(side='right')
		self.nlbly.bind("<FocusOut>",lambda habil=1:self.habil(self.nlbly,self.nticky))
		Label(self.framep[5],relief=GROOVE,text=self.Dado_config.idioma(32)).pack(side='left',fill=X,expand=1)
		self.txttix = Entry(self.framep[5],exportselection=0)
		self.txttix.pack(side='right')
		Label(self.framep[6],relief=GROOVE,text=self.Dado_config.idioma(33)).pack(side='left',fill=X,expand=1)
		self.txttiy = Entry(self.framep[6],exportselection=0)
		self.txttiy.pack(side='right')
		Label(self.framep[7],relief=GROOVE, text=self.Dado_config.idioma(34)).pack(side='left',fill=X,expand=1)		
		self.txtti = Entry(self.framep[7],exportselection=0)
		self.txtti.pack(side='right')
		Label(self.framep[8],relief=GROOVE, text=self.Dado_config.idioma(35)).pack(fill=X)		
		self.txttib = Entry(self.framep[9],exportselection=0)
		self.txttib.pack(fill=X)
		self.framef=[]
		for rowf in range(19):
			self.framef.append(Frame(self.framefront,bd=3,bg='gray',relief=GROOVE))
			self.framef[rowf].pack(fill=X)
			#self.framef[rowf].grid(column=0,row=rowf+1,sticky=W+E)
		Label(self.framef[0],relief=GROOVE,text=self.Dado_config.idioma(36)).pack(fill='both')
		#Label(self.framef[1],relief=GROOVE,text='Fonte geral').pack(side='left',ipady=2)
		#Button(self.framef[1],text='Selecionar Fonte',command=lambda id='G':self.selecionarfonte(id)).pack(side='right')
		Label(self.framef[2],relief=GROOVE,text=self.Dado_config.idioma(32)).pack(side='left',fill='both',expand=1)
		Button(self.framef[2],relief='ridge',text=self.Dado_config.idioma(37),command=lambda id='X':self.selecionarfonte(id,self.titulox)).pack(side='right')
		Label(self.framef[3],relief=GROOVE,text=self.Dado_config.idioma(33)).pack(side='left',fill='both',expand=1)
		Button(self.framef[3],relief='ridge',text=self.Dado_config.idioma(37),command=lambda id='Y':self.selecionarfonte(id,self.tituloy)).pack(side='right')
		Label(self.framef[4],relief=GROOVE,text=self.Dado_config.idioma(34)).pack(side='left',fill='both',expand=1)
		Button(self.framef[4],relief='ridge',text=self.Dado_config.idioma(37),command=lambda id='T':self.selecionarfonte(id,self.titulo)).pack(side='right')
		Label(self.framef[7],relief=GROOVE,text=self.Dado_config.idioma(35)).pack(fill=X)
		Button(self.framef[8],relief='ridge',text=self.Dado_config.idioma(37),command=lambda id='B':self.selecionarfonte(id,self.titulob)).pack(fill=X)
		Label(self.framef[9],relief=GROOVE,text=self.Dado_config.idioma(115)).pack(fill=X,expand=1)
		self.sizetick = StringVar(self)
		self.sizetick.set('16')
		# self.sizetick.set(self.utiC.getSizeLabelsTick(0))
		Button(self.framef[10],relief='ridge',text='-',font = {'font.size': 22},command=lambda e='-' :self.uti.sizeTICK(self.sizetick,e,plt)).pack(fill='x',side="left",expand=True)		
		Button(self.framef[10],relief='ridge',text='+',font = {'font.size': 22},command=lambda e='+' :self.uti.sizeTICK(self.sizetick,e,plt)).pack(fill='x',side="right",expand=True)		
		Label(self.framef[10],textvariable=self.sizetick,font = 'Levenim\ MT 10 bold roman',width=10).pack(fill='both',expand=True)
		Label(self.framef[11],relief='groove',text=self.Dado_config.idioma(116)).pack(fill='both',expand=1)
		self.largtick = StringVar(self)
		self.largtick.set('2.0')
		# self.largtick.set(self.utiC.getWidthTickMajor(0))
		Button(self.framef[12],relief='ridge',text='-',command=lambda e='-' :self.uti.largTICK(self.largtick,e,'major',plt)).pack(fill='x',side="left",expand=True)		
		Button(self.framef[12],relief='ridge',text='+',command=lambda e='+' :self.uti.largTICK(self.largtick,e,'major',plt)).pack(fill='x',side="right",expand=True)		
		Label(self.framef[12],textvariable=self.largtick,font = 'Levenim\ MT 10 bold roman',width=10).pack(fill='both',expand=True)	
		Label(self.framef[13],relief='groove',text=self.Dado_config.idioma(117)).pack(fill='both',expand=1)
		self.alttick = StringVar(self)
		self.alttick.set('9.0')
		# self.alttick.set(self.utiC.getHeightTickMajor(0))
		Button(self.framef[14],relief='ridge',text='-',command=lambda e='-' :self.uti.altTICK(self.alttick,e,'major',plt)).pack(fill='x',side="left",expand=True)		
		Button(self.framef[14],relief='ridge',text='+',command=lambda e='+' :self.uti.altTICK(self.alttick,e,'major',plt)).pack(fill='x',side="right",expand=True)		
		Label(self.framef[14],textvariable=self.alttick,font = 'Levenim\ MT 10 bold roman',width=10).pack(fill='both',expand=True)	
		Label(self.framef[15],relief='groove',text=self.Dado_config.idioma(118)).pack(fill='both',expand=1)
		self.largtickMinor = StringVar(self)
		self.largtickMinor.set(2.0)
		# self.largtickMinor.set(self.utiC.getWidthTickMinor(0))
		Button(self.framef[16],relief='ridge',text='-',command=lambda e='-' :self.uti.largTICK(self.largtickMinor,e,'minor',plt)).pack(fill='x',side="left",expand=True)		
		Button(self.framef[16],relief='ridge',text='+',command=lambda e='+' :self.uti.largTICK(self.largtickMinor,e,'minor',plt)).pack(fill='x',side="right",expand=True)		
		Label(self.framef[16],textvariable=self.largtickMinor,font = 'Levenim\ MT 10 bold roman',width=10).pack(fill='both',expand=True)	
		Label(self.framef[17],relief='groove',text=self.Dado_config.idioma(119)).pack(fill='both',expand=1)
		self.alttickMinor = StringVar(self)
		self.alttickMinor.set('4.5')
		# self.alttickMinor.set(self.utiC.getHeightTickMinor(0))
		Button(self.framef[18],relief='ridge',text='-',command=lambda e='-' :self.uti.altTICK(self.alttickMinor,e,'minor',plt)).pack(fill='x',side="left",expand=True)		
		Button(self.framef[18],relief='ridge',text='+',command=lambda e='+' :self.uti.altTICK(self.alttickMinor,e,'minor',plt)).pack(fill='x',side="right",expand=True)		
		Label(self.framef[18],textvariable=self.alttickMinor,font = 'Levenim\ MT 10 bold roman',width=10).pack(fill='both',expand=True)	
		self.bind("<Up>",lambda e: self.uti.up_lista(self.listaobs))
		self.bind("<Down>",lambda e: self.uti.down_lista(self.listaobs))
		self.bind('<Return>',lambda p:self.plotar())
		self.protocol("WM_DELETE_WINDOW",self.quit)
		self.geometry('800x438')
		self.iconbitmap(r'icone.ico')
		self.state('zoomed')
		self.mainloop()
	def quit(self):
		self.uti.troca(self.root,self,plt)
		for val,i in zip([self.sizetick.get(),self.largtick.get(),self.alttick.get(),self.largtickMinor.get(),self.alttickMinor.get()],range(1,6)):
			self.utiC.setConfig(val,i,0)



	def atuaAno(self,*event):
		self.ano = self.uti.refresh_list(self.ano,float(datetime.strptime(self.cal.get(), '%d/%m/%Y').year),self.listaobs)
		print(self.cal.get())
	def save_png(self):
		if self.varsave.get() == True:
			if self.filedir and self.titulo:
				self.fig.savefig(("%s\%s.png")%(self.filedir,self.titulo))
	def salvar_matriz(self):
###########################|Matriz do tipo all|##############################################################################################################################################################
		try:
			Matriz_std = "Hora"
			barra_std = "------"
			for diaTEC in self.TECdias:
				Matriz_std+=(("\tTEC%.2i")%(diaTEC))
				barra_std+=("\t-----")
			Matriz_std+=(("\tMEDIA\tDESV\tM+DES\tM-DES\n%s\t------\t------\t------\t------\n")%barra_std)
			Horas = 0
			for matriz_tmp in self.matrizstd:
				Matriz_std+= (("%06.3f\t")%(Horas/60)).replace(".",",")
				Horas+=1
				for tecN in matriz_tmp:
					if tecN < 0 :#np.isnan(tecN):
						Matriz_std+=("-----\t")
					else:	
						Matriz_std+=(("%05.2f\t")%(tecN)).replace(".",",")
				#tmp_media = [float(n) for n in matriz_tmp if not np.isnan(n)]
				tmp_media = [float(n) for n in matriz_tmp if n>0]
				try:
					mediaTEC = sum(tmp_media)/float(len(tmp_media))
				except ZeroDivisionError:
					messagebox.showerror(self.Dado_config.idioma(49),self.Dado_config.idioma(94),parent=self)
					raise IOError
				des_std = np.std(tmp_media)
				Matriz_std+=(("%06.3f\t")%(mediaTEC)).replace(".",",")
				Matriz_std+=(("%06.3f\t")%(des_std)).replace(".",",")
				Matriz_std+=(("%06.3f\t")%(mediaTEC+des_std)).replace(".",",")
				Matriz_std+=(("%06.3f\n")%(mediaTEC-des_std)).replace(".",",")
			with open((self.filedir  + ("/%s_matriz.std")%(self.titulo)), 'w',encoding="UTF-8") as arquivoMat:
				arquivoMat.write(Matriz_std)				
				arquivoMat.close()
				# print(self.filedir + ("/%s_matriz.std")%(self.titulo))
		except PermissionError:
			messagebox.showerror(self.Dado_config.idioma(49),self.Dado_config.idioma(95),parent=self)
		except (IOError,IndexError,AttributeError):
			pass
	def atua_titulos(self):
		try:
			if self.txtti.get().strip(' ') !="":
				self.titulo = self.txtti.get().strip(' ')
			if self.txttix.get().strip(' ') !="":
				self.titulox = self.txttix.get().strip(' ')
			if self.txttiy.get().strip(' ') !="":
				self.tituloy = self.txttiy.get().strip(' ')
			if self.txttib.get().strip(' ') !="":
				self.titulob = self.txttib.get().strip(' ')
			if self.nlbly.get() !="":
				Nlbly = int(self.nlbly.get().strip(' '))
				self.axes.yaxis.set_major_locator(ticker.LinearLocator(round(Nlbly)))
			elif self.nticky.get() !="":
				Nticky = float(self.nticky.get().strip(' ').replace(",","."))
				self.axes.yaxis.set_major_locator(ticker.IndexLocator(base=(Nticky*60), offset=self.IHoras))
			else:
				# self.axes.yaxis.set_major_locator(ticker.IndexLocator(base=(60), offset=self.IHoras))
				self.axes.yaxis.set_major_locator(ticker.LinearLocator(24))
			if self.nlblx.get() !="":
				Nlblx = int(self.nlblx.get().strip(' '))
				self.axes.xaxis.set_major_locator(ticker.LinearLocator(round(Nlblx)))
			elif self.ntickx.get() !="":
				Ntickx = float(self.ntickx.get().strip(' ').replace(",","."))
				self.axes.xaxis.set_major_locator(ticker.IndexLocator(base=(Ntickx), offset=0))
			else:
				self.axes.xaxis.set_major_locator(ticker.IndexLocator(base=(2), offset=0))
		except AttributeError:
			pass
		plt.title(self.titulo,**self.fontt)
		plt.ylabel(self.tituloy,rotation=90,**self.fonty)
		plt.xlabel(self.titulox,**self.fontx)
		try:
			self.cbar.ax.set_title(self.titulob,**self.fontb) 
			self.cbar.ax.tick_params(width=float(self.largtick.get()),size=float(self.alttick.get()),labelsize=float(self.sizetick.get())) 
			# self.cbar.ax.tick_params(labelsize=float(self.sizetick.get())) 
		except AttributeError:
			pass

	def atua_est(self):
		try:
			self.axes.xaxis.set_major_locator(ticker.IndexLocator(base=(1), offset=self.vIHoras))
		except AttributeError:
			pass
		self.refreshCanvas()
	
	def atua_grid_X(self):
		try:
			self.axes.xaxis.grid(self.vargrid_X.get())
			self.refreshCanvas()
		except (AttributeError,ValueError):
			pass
	def atua_grid_Y(self):
		try:
			self.axes.yaxis.grid(self.vargrid_Y.get())
			self.refreshCanvas()
		except (AttributeError,ValueError):
			pass
	def habil(self,objt1,objt2):
		if objt1.get().strip() != "":
			objt2.config(state="disabled",bg="gray")
		elif objt2['state']=="disabled":
			objt2.config(state="normal",bg="white")
	def refreshCanvas(self):
		self.atua_titulos()
		try:
			self.fig.canvas.draw()
		except ValueError:
			pass
			
	def selecionar(self):
		file = askdirectory(initialdir="c:/",title = self.Dado_config.idioma(40),parent=self)
		# file = r"C:\Users\teste\Google Drive\Estágio\STD" #askdirectory(initialdir="c:/",title = "SELECIONE UM DIRETÓRIO :")
		if file:
			self.filedir = file 



	def plotar(self):
		self.matrizstd = []
		if self.filedir:
			if len(self.listaobs.curselection()) > 0:
				id = self.listaobs.curselection()
				sigla = self.listaobs.get(id).replace(",","").replace("(","").replace(")","").split()[0]
				dataI = datetime.strptime(self.cal.get(), '%d/%m/%Y')
				dataF = datetime.strptime(self.cal2.get(), '%d/%m/%Y')
				delta = dataF - dataI  
				nfile =''
				self.titulo =(("%s-%s-%.2i") % (sigla.lower(),dataI.year,dataI.month)) 
				self.TECdias = []
				self.matriz_dias = []
				for contd in range(delta.days + 1):
					datafile = (dataI + timedelta(days=contd))
					self.TECdias.append(datafile.day)
					dia_ano = datafile.timetuple().tm_yday
					self.matriz_dias.append([('%s/%s')%(datafile.day,datafile.month),('%s')%(datafile.day)])
					nfile = ("/%s%.3i-%i-%.2i-%.2i.Std") % (sigla.lower(),dia_ano,datafile.year,datafile.month,datafile.day)
					destino = self.filedir + nfile
					self.matrizstd.append(self.uti.Leitura_trip(destino))
				self.matrizstd = np.array(self.matrizstd).transpose()
				# print(self.matriz_dias)	
	###########################|AJUSTAR LER TRIPS|##############################################################################################################################################################
			# '''
			# 	arrumando matriz...fix
			# '''

				tec_fix = []
				for x in [a for s in self.matrizstd for a in s]:
					tec_fix.append(x)
	###########################|AJUSTAR LER TRIPS|##############################################################################################################################################################
				plt.clf()
				self.axes = self.fig.subplots()
				if np.mean(tec_fix) == -999.0 or np.mean(tec_fix) == np.nan:
					plt.text(.5,.5, Utilitarios().idioma(94), size=16,ha="center", va="center" )
				else:
					self.atua_titulos()
					self.atua_grid_X()
					self.atua_grid_Y()
					try:
						if self.diaIHoras.get().strip(" ").replace(",",".") !="":
							self.IHoras = float(self.diaIHoras.get().strip(" ").replace(",","."))
						else:
							self.IHoras = 0
						if self.diaFHoras.get().strip(" ").replace(",",".") !="":	
							self.FHoras = float(self.diaFHoras.get().strip(" ").replace(",","."))
						else:
							self.FHoras = 24#23.983
						if self.txtvmax.get().strip(" ") != "" and float(self.txtvmax.get().strip(" ").replace(',','.')) != 0:
							vmax = float(self.txtvmax.get().strip(" ").replace(',','.'))
						else:
							vmax = 100.00
					except ValueError:
						messagebox.showerror(self.Dado_config.idioma(49),self.Dado_config.idioma(93),parent=self)
						
					passo = vmax/15
					level=np.arange(0,(vmax+1),passo)
					plt.title(self.titulo,**self.fontt)
					plt.minorticks_on()
					plt.ylabel(self.tituloy,rotation=90,**self.fonty)
					plt.ylim(self.IHoras*60,self.FHoras*60)
					plt.tick_params(axis='both', which='major', width=float(self.largtick.get()),size=float(self.alttick.get()),labelsize=float(self.sizetick.get()))
					plt.tick_params(axis='both', which='minor' ,width=float(self.largtickMinor.get()) ,size=float(self.alttickMinor.get()))
					self.axes.yaxis.set_major_formatter(ticker.FuncFormatter(self.major_formatterhora))
					self.axes.xaxis.set_major_formatter(ticker.FuncFormatter(self.major_formatterdia))
					plt.xlabel(self.titulox,**self.fontx)
					yyy = np.arange(1440)
					cmap = plt.cm.get_cmap("jet")
					cmap.set_under("white")
					cmap.set_over("darkred")	
					# self.p=plt.contourf(self.matrizstd,levels=level,cmap=cmap,vmin = 0,vmax=vmax,extend="both")
					# self.p=plt.contourf(tec_fix,levels=level,cmap=cmap,vmin = 0,vmax=vmax,extend="both")
					# self.p=plt.contourf(tec_fix,yyy,self.matrizstd,levels=level,cmap=cmap,vmin = 0,vmax=vmax,extend="both")
					self.passo_ctick = 10
					self.cbar = plt.colorbar(self.axes.contourf(tec_fix,levels=level,cmap=cmap,vmin = 0,vmax=vmax,extend="both"),ax = self.axes,ticks = np.arange(0,vmax+1,self.passo_ctick))
						
					self.cbar.ax.set_title(self.titulob,**self.fontb)
					self.cbar.ax.tick_params(width=float(self.largtick.get()),size=float(self.alttick.get()),labelsize=float(self.sizetick.get())) 
					# self.cbar.set_canvas(self.canvas)
				
				self.canvas.get_widget().pack(side=ui.BOTTOM, fill=ui.BOTH, expand=True)
				self.canvas._qt_canvas.pack(side=ui.TOP, fill=ui.BOTH, expand=True)
				self.toolbar.update()
				self.fig.canvas.draw()

				if self.varmatriz.get() == True:
					self.salvar_matriz()
				self.save_png()	
		else:
			messagebox.showerror(Utilitarios().idioma(49),Utilitarios().idioma(126),parent=self)
			self.selecionar()
			self.plotar()	
			# self.focus_force()
		# self.focus()
		plt.tight_layout()
		

	def selecionarfonte(self,id,demo):
		# print('estou entrando nas fontes .^.^.^.^.^.^.')
		font = askfont(self,str(demo),self.Dado_config.idioma(37))
	#"""	rguments:
	 #   master: master window
	 #   text: sample text to be displayed in the font chooser
	 #   title: dialog title
	 #   font_args: family, size, slant (=roman/italic),
				 #  weight (=normal/bold), underline (bool), overstrike (bool)
	#"""
		if font:
			del(font['slant'])
			del(font['underline'])
			del(font['overstrike'])
			#underline
			#font['family'] = font['family'].replace(' ', '\ ')
			#font_str = "%(family)s %(size)i %(weight)s %(slant)s" % font
			# if font['underline']:
			# 	font_str += ' underline'
			# if font['overstrike']:
			# 	font_str += ' overstrike'
			if id == 'X':
				self.fontx = font
			elif id == 'Y':
				self.fonty = font
			elif id == 'T':
				self.fontt = font
			elif id == 'B':
				self.fontb = font
			#elif id== 'G':
				#fonttotal = font
	def major_formatterhora(self,x, pos):
		try:
			return "%.f" % (x/60)
		except IndexError:
			pass
	def major_formatterdia(self,x, pos):
		try:
			return (self.matriz_dias[int(x)][self.DateFormat.get()])
		except IndexError:
			pass
		
		return (("%s") % (self.matriz_dias[(int(x))]))
if __name__ == "__main__":
	root = Tk()
	#root.withdraw()
	teste = GraficocontornoINDV(root)
	#root.mainloop()