from qt_ui import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.ticker import LinearLocator , FuncFormatter,IndexLocator
from datetime import datetime, timedelta, date
from qt_ui import ttk, messagebox, Toplevel
from qt_ui.filedialog import askdirectory
# import matplotlib.animation as manimation
import matplotlib,os,calendar,math,io
import matplotlib.ticker as ticker
from qtfontchooser import askfont
from qt_calendar import DateEntry
# from matplotlib import animation
import matplotlib.pyplot as plt
from util import Utilitarios,VerticalScrolledFrame,DadoIdioma
# from Calcigrf import IGRF12
matplotlib.use("QtAgg")
from qt_ui import *  
from scipy import interpolate
import qt_ui as tk
import numpy as np
class Graficosetor(Toplevel):
###########################|Bob ô construtor|##############################################################################################################################################################
	def __init__(self,root):
		Toplevel.__init__(self,root) 
		self.MATRIZ_CONTO_VD = []
		self.canvas = ""
		self.toolbar = ""
		self.filedir = ""#r"C:\Users\Mateus_Pillat\Google Drive\Estágio\STD" #askdirectory(initialdir="c:/",title = "SELECIONE UM DIRETÓRIO :")
		plt.rc('font', weight='bold')
		plt.rc('axes',linewidth=2)
		self.fonty = self.fontt = self.fontb = self.fontLTXY = self.fontx = {'family' : 'Arial',
		'weight' : 'bold',
		'size'   : 18}
		self.matriz_tec = []
		self.uti = Utilitarios()
		# self.utiC = DadoIdioma()
		self.Dado_config = DadoIdioma()
		self.framep = VerticalScrolledFrame(self)#Frame(self,bd=3,relief=GROOVE,bg='gray')
		self.framep.pack(fill='both',side='left')
		nb = ttk.Notebook(self)
		self.page1 = Frame(self)
		self.page2 = Frame(self)
		self.page1.bind('<FocusIn>',lambda e: self.refreshCanvas())

		self.fig, self.axes = plt.subplots()
		self.canvas = FigureCanvasTkAgg(self.fig,self.page1)
		self.canvas.draw()
###############################|Has deprecated ... breves...|#########################################################################################################################################################		
		self.toolbar = NavigationToolbar2Tk(self.canvas, self.page1)

		nb.add(self.page1,text =self.Dado_config.idioma(7))
		nb.add(self.page2,text =self.Dado_config.idioma(17))
		nb.pack(expand=1,side='right',fill='both')
		self.framepg1 = Frame(self.framep.interior,bd=3,bg='gray',relief=GROOVE)
		self.framepg1.pack(side='left',fill=BOTH)
		self.framepg2 = Frame(self.framepg1,bd=3,bg='gray',relief=GROOVE)
		self.framepg2.pack(side='top',fill=BOTH,expand=1)
		self.framepg3 = Frame(self.framepg2,bd=3,bg='gray',relief=GROOVE)
		self.framepg3.pack(side='bottom',fill='both')
		self.framepg4 = Frame(self.framepg1,bg='gray',relief=GROOVE)
		self.framepg4.pack()
		self.dirstd = Button(self.framepg2, text=self.Dado_config.idioma(18),command=self.selecionar,relief=RIDGE)
		self.dirstd.pack(side='top',fill=X)
		self.listaobs = Listbox(self.framepg2,exportselection=0,bd=3,relief='groove',selectmode='multiple')
		self.listaobs.pack(side='left',fill=BOTH,expand=1)
		self.listaobs.bind("<<ListboxSelect>>",self.seta)
		self.sb = Scrollbar(self.framepg2)
		self.sb.pack(side=RIGHT,fill=Y)
		self.sb.configure(command=self.listaobs.yview)
		self.listaobs.configure(yscrollcommand=self.sb.set)
		Label(self.framepg3,text=self.Dado_config.idioma(107)).pack(fill=X)
		self.maisdata = Button(self.framepg3,text="→",command=self.righh,font="SimHei 10 bold roman")
		self.menosdata = Button(self.framepg3,text="←",command=self.leff,font="SimHei 10 bold roman")
		self.ano = 0
		self.dData = StringVar (self)
###########################|Calendario|##############################################################################################################################################################
		self.cal = DateEntry(self.framepg3, background='darkblue',foreground='white', borderwidth=1 ,textvariable = self.dData)#,year = 2015,day=16,month=3)
		self.cal.pack(fill='both',expand = True)
		self.cal.bind('<<DateEntrySelected>>',self.atuaAno)
###########################|Títulos do gráfico X Y Barra Gráf|##############################################################################################################################################################
		self.titulo = str(datetime.strptime(self.cal.get(), '%d/%m/%Y').date())
		self.tituloy = self.Dado_config.idioma(40)
		self.titulox = self.Dado_config.idioma(41)
		self.titulob = "VTEC"
###########################|Títulos do gráfico X Y Barra Gráf|##############################################################################################################################################################
###########################|Latitude Travado a 300|##############################################################################################################################################################
		# for obss in self.listaobs.curselection():
		# 		print('oi')
		# 		self.estacao_select.append(self.listaobs.get(obss).replace(",","").replace("(","").replace(")","").split())
		# 		incli = IGRF12()
		# 		res_incli = incli.get_igrf(float(self.setD.year),float(300),float(self.estacao_select[-1][1]),float(self.estacao_select[-1][2]),float(self.estacao_select[-1][3]),float(self.estacao_select[-1][4]))
		# 		tmpincli = res_incli.split(' ')     
		# 		if tmpincli[0].startswith('-'):
		# 			inclinacao = ("%.3f" % (int(tmpincli[0]) - (int(tmpincli[1])/60))) 
		# 		else:
		# 			inclinacao = ("%.3f" % (int(tmpincli[0]) + (int(tmpincli[1])/60))) 
		# 		diplat = (math.degrees(math.atan(((math.tan(math.radians(float(inclinacao)))/2)))))
		# 		self.estacao_select[-1].append(diplat)
		#print(self.estacao_select)
###########################|Paleta de propriedades rápidas|##############################################################################################################################################################
			
		self.atuaAno()
		#self.ano = self.uti.refresh_list(self.ano,float(datetime.strptime(self.cal.get(), '%d/%m/%Y').year),self.listaobs)
		self.framel=[]
		for rowl in range(16):
			self.framel.append(Frame(self.framepg4,bd=3,bg='gray',relief=GROOVE))
			self.framel[rowl].pack(fill=BOTH)
			#self.framel[rowl].grid(column=0,rows=rowl+1,sticky=E+W)
		self.lblInicioHoras = Label(self.framel[0], text=self.Dado_config.idioma(19),relief=GROOVE)
		self.lblInicioHoras.pack(side='left',fill=X,expand=True)
		vcmd = (self.register(self.uti.onValidatesigla),'%S', '%s','%d',2,4)
		self.IHoras = Entry(self.framel[0],exportselection=0,validate="key",validatecommand=vcmd)
		self.IHoras.pack(side='right')
		self.lblFimHoras = Label(self.framel[1], text=self.Dado_config.idioma(20),relief=GROOVE)
		self.lblFimHoras.pack(side='left',fill=X,expand=True)       
		vcmd = (self.register(self.uti.onValidatesigla),'%S', '%s','%d',2,4)
		self.FHoras = Entry(self.framel[1],exportselection=0,validate="key",validatecommand=vcmd) 
		self.FHoras.pack(side='right')      
		self.lblvmax = Label(self.framel[2], text=self.Dado_config.idioma(23),relief=GROOVE)
		self.lblvmax.pack(side='left',fill=X,expand=True)               
		vcmd = (self.register(self.uti.onValidatesigla),'%S', '%s','%d',2,4)
		self.txtvmax = Entry(self.framel[2],exportselection=0,validate="key",validatecommand=vcmd)
		self.txtvmax.pack(side='right')
		self.varaxixY = IntVar(self)
		self.varaxixY.set(1)
		Label(self.framel[3],text=self.Dado_config.idioma(120),relief=GROOVE).pack(fill=X)
		Radiobutton(self.framel[3],variable=self.varaxixY,value=1,text='Latitude',relief=GROOVE,command=lambda p=1:self.plotar()).pack(side='right',fill=X,expand=1)
		Radiobutton(self.framel[3],variable=self.varaxixY,value=5,text='Dip.Lat',relief=GROOVE,command=lambda p=1:self.plotar()).pack(side='left',fill=X,expand=1)
		# self.lblgrid = Label(self.framel[4],text=self.Dado_config.idioma(24))
		# self.lblgrid.pack(side='left',fill=X,expand=True)
		# self.checkgrid = Checkbutton(self.framel[4],variable=self.vargrid,width=5,command=self.atua_grid)
		# self.checkgrid.pack(side='right')
		self.vargrid_X = BooleanVar(self)
		self.vargrid_Y = BooleanVar(self)
		Label(self.framel[4],text=self.Dado_config.idioma(24),relief=GROOVE).pack(fill=X)
		Label(self.framel[4],text="Horizontal",relief=GROOVE).pack(side='left',fill=BOTH)
		Checkbutton(self.framel[4],variable=self.vargrid_X,width=5,command=self.atua_grid_X).pack(side='left')
		Checkbutton(self.framel[4],variable=self.vargrid_Y,width=5,command=self.atua_grid_Y).pack(side='right')
		Label(self.framel[4],text="Vertical",relief=GROOVE).pack(side='right',fill=BOTH)			
		self.lblsave = Label(self.framel[5],text=self.Dado_config.idioma(25),relief=GROOVE)
		self.lblsave.pack(side='left',fill=BOTH,expand=True)
		self.varsave = BooleanVar(self)
		self.checksave = Checkbutton(self.framel[5],variable=self.varsave,width=5,command=self.save_png)
		self.checksave.pack(side='right')
		self.lblmat = Label(self.framel[6],text=self.Dado_config.idioma(91),relief=GROOVE)
		self.lblmat.pack(side='left',fill=BOTH,expand=True)
		self.varmatriz = BooleanVar(self)
		self.checkmat = Checkbutton(self.framel[6],variable=self.varmatriz,width=5,command=self.salvar_matriz)
		self.checkmat.pack(side='right')
		self.lblest = Label(self.framel[7],text=self.Dado_config.idioma(109),relief=GROOVE)
		self.lblest.pack(side='left',fill=BOTH,expand=True)
		self.varest = BooleanVar(self)
		self.checkest = Checkbutton(self.framel[7],variable=self.varest,width=5,command=self.atua_est)
		self.checkest.pack(side='right')
		Button(self.framel[8], width=20, text=self.Dado_config.idioma(108),relief=RIDGE, command= lambda p=1:self.plotar()).pack(side='bottom',fill=X)
		# self.lblGV = Label(self.framel[8],text=self.Dado_config.idioma(114))
		# self.lblGV.pack(fill=X,expand=True)
		# self.lblVD = Label(self.framel[9],text=self.Dado_config.idioma(110))
		# self.lblVD.pack(side='left',fill=X,expand=True)
		# self.varVD = BooleanVar(self)
		# self.checkVD = Checkbutton(self.framel[9],variable=self.varVD,width=5)
		# self.checkVD.pack(side='right')
		# self.btnVD2 = Button(self.framel[10], width=20, text=self.Dado_config.idioma(112),relief=RIDGE,command = self.deletarULT)
		# self.btnVD3 = Button(self.framel[11], width=20, text=self.Dado_config.idioma(113),relief=RIDGE,command = self.clearVD)
		# self.btnVD = Button(self.framel[12], width=20, text=self.Dado_config.idioma(111),relief=RIDGE, command= self.criarVD)
		# self.btnplot = Button(self.framel[13], width=20, text=self.Dado_config.idioma(108),relief=RIDGE, command= self.plotar)
		# self.btnplot.pack(side='bottom',fill=X)
		# self.btnRefresh = Button(self.framel[14],text="Refresh",relief=RIDGE,command= self.refreshCanvas)
		# self.btnRefresh.pack(fill=X)
		# self.EST_ausent = Text(self.framel[15],bg="gray72",height=2,width=1)
		self.EST_ausent = Listbox(self.framel[9],exportselection=0,bg="gray72",relief='groove')#,selectmode=EXTENDED)
		self.sbau = Scrollbar(self.framel[9],command=self.EST_ausent.yview)
		
		# self.EST_ausent.bind()

		self.EST_ausent.config(yscrollcommand=self.sbau.set)

		# self.listaobs.configure(yscrollcommand=self.sb.set)
		#self.EST_ausent.pack(fill=X)
		#self.EST_ausent.insert(END,'oi\nasdsadasd')
		#self.EST_ausent.config(state='disabled')
###########################|Propriedades gráfico|##############################################################################################################################################################
###########################|Titulo e Fonte|##############################################################################################################################################################
		self.framefront = Frame(self.page2,bd=3,bg="blue",relief=GROOVE)
		self.framefront.pack(side='left',fill=Y)
		self.framep=[]
		for rowp in range(10):
			self.framep.append(Frame(self.framefront,bd=3,bg='gray',relief=GROOVE))
			self.framep[rowp].pack(fill=X)
		self.lblindica = Label(self.framep[0],relief='groove', text=self.Dado_config.idioma(27))
		self.lblindica.pack(fill='both')
		self.lblntickx = Label(self.framep[1],relief='groove' ,text=self.Dado_config.idioma(28))
		self.lblntickx.pack(side='left',fill=X,expand=1)
		vcmd = (self.register(self.uti.onValidatesigla),'%S', '%s','%d',2,10)
		self.ntickx = Entry(self.framep[1],exportselection=0,validate="key",validatecommand=vcmd)
		self.ntickx.pack(side='right',fill=X)
		self.ntickx.bind("<FocusOut>",lambda habil:self.habil(self.ntickx,self.nlblx))
		self.lblnticky = Label(self.framep[2],relief='groove', text=self.Dado_config.idioma(29))
		self.lblnticky.pack(side='left',fill=X,expand=1)   
		vcmd = (self.register(self.uti.onValidatesigla),'%S', '%s','%d',2,10)
		self.nticky = Entry(self.framep[2],exportselection=0,validate="key",validatecommand=vcmd)
		self.nticky.pack(side='right',fill=X)
		self.nticky.bind("<FocusOut>",lambda habil=1:self.habil(self.nticky,self.nlbly))
		self.lblnlblx = Label(self.framep[3],relief='groove', text=self.Dado_config.idioma(30))
		self.lblnlblx.pack(side='left') 
		vcmd = (self.register(self.uti.onValidatesigla),'%S', '%s','%d',2,10)
		self.nlblx = Entry(self.framep[3],exportselection=0,validate="key",validatecommand=vcmd)
		self.nlblx.pack(side='right')
		self.nlblx.bind("<FocusOut>",lambda habil:self.habil(self.nlblx,self.ntickx))       
		self.lblnlbly = Label(self.framep[4],relief='groove', text=self.Dado_config.idioma(31))
		self.lblnlbly.pack(side='left')       
		vcmd = (self.register(self.uti.onValidatesigla),'%S', '%s','%d',2,10)
		self.nlbly = Entry(self.framep[4],exportselection=0,validate="key",validatecommand=vcmd)
		self.nlbly.pack(side='right')
		self.nlbly.bind("<FocusOut>",lambda habil=1:self.habil(self.nlbly,self.nticky))
		self.lbltix = Label(self.framep[5],relief='groove',text=self.Dado_config.idioma(32))
		self.lbltix.pack(side='left',fill=X,expand=1)
		self.txttix = Entry(self.framep[5],exportselection=0)
		self.txttix.pack(side='right')
		self.lbltiy = Label(self.framep[6],relief='groove',text=self.Dado_config.idioma(33))
		self.lbltiy.pack(side='left',fill=X,expand=1)
		self.txttiy = Entry(self.framep[6],exportselection=0)
		self.txttiy.pack(side='right')
		self.lblti = Label(self.framep[7],relief='groove', text=self.Dado_config.idioma(34))
		self.lblti.pack(side='left',fill=X,expand=1)        
		self.txtti = Entry(self.framep[7],exportselection=0)
		self.txtti.pack(side='right')
		self.lbltib = Label(self.framep[8],relief='groove', text=self.Dado_config.idioma(35))
		self.lbltib.pack(fill=X)        
		self.txttib = Entry(self.framep[9],exportselection=0)
		self.txttib.pack(fill=X)
		self.framef=[]
		for rowf in range(17):
			self.framef.append(Frame(self.framefront,bd=3,bg='gray',relief=GROOVE))
			self.framef[rowf].pack(fill=X)
		Label(self.framef[0],relief='groove',text=self.Dado_config.idioma(36)).pack(fill='both')
###########################|Propriedades Fonte geral|##############################################################################################################################################################
		#Label(self.framef[1],relief='groove',text='Fonte geral').pack(side='left',ipady=2)
		#Button(self.framef[1],text='Selecionar Fonte',command=lambda id='G':self.selecionarfonte(id)).pack(side='right')		
###########################|Propriedades Fonte geral|##############################################################################################################################################################
		Label(self.framef[2],relief='groove',text=self.Dado_config.idioma(32)).pack(side='left',fill='both',expand=1)
		Button(self.framef[2],text=self.Dado_config.idioma(37),command=lambda id='X':self.selecionarfonte(id,self.titulox),relief='ridge').pack(side='right')
		Label(self.framef[3],relief='groove',text=self.Dado_config.idioma(33)).pack(side='left',fill='both',expand=1)
		Button(self.framef[3],text=self.Dado_config.idioma(37),command=lambda id='Y':self.selecionarfonte(id,self.tituloy),relief='ridge').pack(side='right')
		Label(self.framef[4],relief='groove',text=self.Dado_config.idioma(34)).pack(side='left',fill='both',expand=1)
		Button(self.framef[4],text=self.Dado_config.idioma(37),command=lambda id='T':self.selecionarfonte(id,self.titulo),relief='ridge').pack(side='right')
		Label(self.framef[5],relief='groove',text=self.Dado_config.idioma(35)).pack(fill='both')
		Button(self.framef[6],text=self.Dado_config.idioma(37),command=lambda id='B':self.selecionarfonte(id,self.titulob),relief='ridge').pack(fill='both')
		Label(self.framef[7],relief='groove',text=self.Dado_config.idioma(115)).pack(fill='both',expand=1)
		self.sizetick = StringVar(self)
		# self.sizetick.set('16')
		self.sizetick.set(self.utiC.getSizeLabelsTick(1))		
		Button(self.framef[8],relief='ridge',text='-',font = {'font.size': 22},command=lambda e='-' :self.uti.sizeTICK(self.sizetick,e,plt)).pack(fill='x',side="left",expand=True)		
		Button(self.framef[8],relief='ridge',text='+',font = {'font.size': 22},command=lambda e='+' :self.uti.sizeTICK(self.sizetick,e,plt)).pack(fill='x',side="right",expand=True)		
		self.lbllltick = Label(self.framef[8],relief='groove',textvariable=self.sizetick,font = 'Levenim\ MT 10 bold roman',width=10)
		self.lbllltick.pack(fill='both',expand=True)
		Label(self.framef[9],relief='groove',text=self.Dado_config.idioma(116)).pack(fill=X,expand=1)
		self.largtick = StringVar(self)
		# self.largtick.set('2.0')
		self.largtick.set(self.utiC.getWidthTickMajor(1))
		Button(self.framef[10],relief='ridge',text='-',command=lambda e='-' :self.uti.largTICK(self.largtick,e,'major',plt)).pack(fill='x',side="left",expand=True)		
		Button(self.framef[10],relief='ridge',text='+',command=lambda e='+' :self.uti.largTICK(self.largtick,e,'major',plt)).pack(fill='x',side="right",expand=True)		
		self.lbllllargtick = Label(self.framef[10],relief='groove',textvariable=self.largtick,font = 'Levenim\ MT 10 bold roman',width=10)
		self.lbllllargtick.pack(fill='both',expand=True)	
		Label(self.framef[11],relief='groove',text=self.Dado_config.idioma(117)).pack(fill=X,expand=1)
		self.alttick = StringVar(self)
		# self.alttick.set('9.0')
		self.alttick.set(self.utiC.getHeightTickMajor(1))
		Button(self.framef[12],relief='ridge',text='-',command=lambda e='-' :self.uti.altTICK(self.alttick,e,'major',plt)).pack(fill='x',side="left",expand=True)		
		Button(self.framef[12],relief='ridge',text='+',command=lambda e='+' :self.uti.altTICK(self.alttick,e,'major',plt)).pack(fill='x',side="right",expand=True)		
		self.lblllalttick = Label(self.framef[12],relief='groove',textvariable=self.alttick,font = 'Levenim\ MT 10 bold roman',width=10)
		self.lblllalttick.pack(fill='both',expand=True)	
		Label(self.framef[13],relief='groove',text=self.Dado_config.idioma(118)).pack(fill=X,expand=1)
		self.largtickMinor = StringVar(self)
		# self.largtickMinor.set('2.0')
		self.largtickMinor.set(self.utiC.getWidthTickMinor(1))		
		Button(self.framef[14],relief='ridge',text='-',command=lambda e='-' :self.uti.largTICK(self.largtickMinor,e,'minor',plt)).pack(fill='x',side="left",expand=True)		
		Button(self.framef[14],relief='ridge',text='+',command=lambda e='+' :self.uti.largTICK(self.largtickMinor,e,'minor',plt)).pack(fill='x',side="right",expand=True)		
		self.lbllllargtickMinor = Label(self.framef[14],relief='groove',textvariable=self.largtickMinor,font = 'Levenim\ MT 10 bold roman',width=10)
		self.lbllllargtickMinor.pack(fill='both',expand=True)	
		Label(self.framef[15],relief='groove',text=self.Dado_config.idioma(119)).pack(fill=X,expand=1)
		self.alttickMinor = StringVar(self)
		# self.alttickMinor.set('4.5')
		self.alttickMinor.set(self.utiC.getHeightTickMinor(1))		
		Button(self.framef[16],relief='ridge',text='-',command=lambda e='-' :self.uti.altTICK(self.alttickMinor,e,'minor',plt)).pack(fill='x',side="left",expand=True)		
		Button(self.framef[16],relief='ridge',text='+',command=lambda e='+' :self.uti.altTICK(self.alttickMinor,e,'minor',plt)).pack(fill='x',side="right",expand=True)		
		self.lblllalttickMinor = Label(self.framef[16],relief='groove',textvariable=self.alttickMinor,font = 'Levenim\ MT 10 bold roman',width=10)
		self.lblllalttickMinor.pack(fill='both',expand=True)	
		self.bind("<Return>",lambda p=1:self.plotar())
		self.bind('<Left>', self.leff)
		self.bind('<Right>', self.righh)
		self.protocol("WM_DELETE_WINDOW",self.quit)
		self.geometry('800x600')
		self.iconbitmap(r'icone.ico')
		self.state('zoomed')

	

		
	def quit(self):
		self.uti.troca(root,self,plt)
		for val,i in zip([self.sizetick.get(),self.largtick.get(),self.alttick.get(),self.largtickMinor.get(),self.alttickMinor.get()],range(6,11)):
			self.utiC.setConfig(val,i,1)
###########################|Picker Demo_TEST#####################################################################################################		
	# def onpick1(self,event):
	# 	if isinstance(event.artist, Line2D):
	# 		thisline = event.artist
	# 		xdata = thisline.get_xdata()
	# 		ydata = thisline.get_ydata()
	# 		ind = event.ind
	# 		print('onpick1 line:', zip(np.take(xdata, ind), np.take(ydata, ind)))
	# 	elif isinstance(event.artist, Rectangle):
	# 		patch = event.artist
	# 		print('onpick1 patch:', patch.get_path())
	# 	elif isinstance(event.artist, Text):
	# 		text = event.artist
	# 		print('onpick1 text:', text.get_text())
###########################|Atualiza ano para o dip|##############################################################################################################################################################
	def save_png(self):
		if self.varsave.get() == True:
			plt.savefig(("%s\%s.png")%(self.filedir,self.titulo))
	def salvar_matriz(self):
###########################|Atualiza ano para o dip|##############################################################################################################################################################
###########################| |\/|Atriz do tipo Tripa...|##############################################################################################################################################################
		print(self.matriz_tripa)
		if self.varmatriz.get() == True:
			try:
				arqTri = open(((r"%s\%s.Std")%(self.filedir,self.titulo)),'w',encoding="UTF-8")
				for index_tripa in range(len(self.matriz_tripa)):
					cont_horas  = 0.00
					for index_listaTR in self.matriz_tripa[index_tripa]:
						arqTri.write((("%5.3f\t%s\t%5.3f\n")%(cont_horas,self.estacao_select[index_tripa][self.varaxixY.get()],index_listaTR)).replace('.',','))
						cont_horas+=1/60
					else:
						cont_horas = 0
				arqTri.close()
			except AttributeError:
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
				self.axes.yaxis.set_major_locator(ticker.LinearLocatoselfr(round(Nlbly)))
			elif self.nticky.get() !="":
				Nticky = float(self.nticky.get().strip(' ').replace(",","."))
				self.axes.yaxis.set_major_locator(ticker.IndexLocator(base=(Nticky), offset=self.vIHoras))
			else:
				if self.varest.get() == True:
					self.axes.yaxis.set_major_locator(ticker.IndexLocator(base=(1), offset=self.vIHoras))
				else:	
					self.axes.yaxis.set_major_locator(ticker.LinearLocator())            
			if self.nlblx.get() !="":
				Nlblx = int(self.nlblx.get().strip(' '))
				self.axes.xaxis.set_major_locator(ticker.LinearLocator(round(Nlblx)))
			elif self.ntickx.get() !="":
				Ntickx = float(self.ntickx.get().strip(' ').replace(",","."))
				self.axes.xaxis.set_major_locator(ticker.IndexLocator(base=(Ntickx*60), offset=0))
			else:
				# self.axes.xaxis.set_major_locator(ticker.LinearLocator(24))
				self.axes.xaxis.set_major_locator(ticker.IndexLocator(base=(60), offset=0))
		except AttributeError:
			pass
		plt.title(self.titulo,**self.fontt)
		plt.ylabel(self.tituloy,rotation=90,**self.fonty)
		plt.xlabel(self.titulox,**self.fontx)
		try:
			self.cbar.ax.set_title(self.titulob,**self.fontb) 
			self.cbar.ax.tick_params(width=float(self.largtick.get()),size=float(self.alttick.get()),labelsize=float(self.sizetick.get())) 
		except AttributeError:
			pass
	def atua_est(self):
		try:
			self.axes.yaxis.set_major_locator(ticker.IndexLocator(base=(1), offset=self.vIHoras))
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
	def atuaAno(self,*event):
		# self.ano = self.uti.refresh_list(self.ano,float(datetime.strptime(self.cal.get(), '%d/%m/%Y').year),self.listaobs)
		self.ano,conteudo_lista = self.uti.Refresh_list_obs(self.filedir,self.cal.get()[-4:])
		[self.listaobs.insert(END, item) for item in conteudo_lista]


###########################|Atualiza ano para o dip|##############################################################################################################################################################
	def seta(self,e):
		if len(self.listaobs.curselection()) > 1:
			self.cal.pack_forget()
			self.maisdata.pack(side="right")
			self.menosdata.pack(side="left")
			self.cal.pack(fill='both',expand = True)
		else:
			self.maisdata.pack_forget()
			self.menosdata.pack_forget()
###########################|Propriedades Fonte geral|##############################################################################################################################################################
	# def largTICK(self,vt,op,tick):
	# 	if op == '+':
	# 		vt.set(('%.1f')%(float(vt.get())+.1))
	# 	elif op == '-':
	# 		vt.set(('%.1f')%(float(vt.get())-.1))
	# 	plt.tick_params(axis='both', which=tick, width=float(vt.get()))
	# def altTICK(self,vt,op,tick):
	# 	if op == '+':
	# 		vt.set(('%.1f')%(float(vt.get())+.1))
	# 	elif op == '-':
	# 		vt.set(('%.1f')%(float(vt.get())-.1))
	# 	plt.tick_params(axis='both', which=tick, size=float(vt.get()))
	# def sizeTICK(self,vt,op):
	# 	if op == '+':
	# 		vt.set(int(vt.get())+1)
	# 	elif op == '-':
	# 		vt.set(int(vt.get())-1)
	# 	plt.tick_params(axis='both', labelsize=int(vt.get()))#width=1.5 ,size=4)
###########################|Mais e menos dias pelas Setas|##############################################################################################################################################################
	def leff(self,*key):
		res = datetime.strptime(self.cal.get(), "%d/%m/%Y") + timedelta(days=-1)
		self.dData.set((("%s/%s/%s")%(res.day,res.month,res.year)))
		if len(self.listaobs.curselection()) > 1:
			self.plotar()
###########################|Mais e menos dias pelas Setas|##############################################################################################################################################################
	def righh(self,*key):
		res = datetime.strptime(self.cal.get(), "%d/%m/%Y") + timedelta(days=1)
		self.dData.set((("%s/%s/%s")%(res.day,res.month,res.year)))
		if len(self.listaobs.curselection()) > 1:
			self.plotar()
###########################|Selecionar pasta na qual tenha todos dados std|##############################################################################################################################################################
	def selecionar(self):
		file = askdirectory(initialdir="c:/",title = self.Dado_config.idioma(40),parent=self)
		if file:
			self.filedir = file
		# else:
		# 	del(self.filedir)
###########################|Propriedades Fonte geral|##############################################################################################################################################################
	"""
	Controle de quantidade das labels vs o intervalo delas
	"""
	def habil(self,objt1,objt2):
		if objt1.get().strip() != "":
			objt2.config(state="disabled",bg="gray")
		elif objt2['state']=="disabled":
			objt2.config(state="normal",bg="white")
###########################|Replot Canvas Plotar gráfico|##############################################################################################################################################################
	def refreshCanvas(self):
		self.atua_titulos()
		self.fig.canvas.draw()
###########################|Plotar gráfico|##############################################################################################################################################################
	def plotar(self):
		if self.filedir:
			if len(self.listaobs.curselection()) > 1:
				self.matriz_tec = []
				self.estacao_select = []
				self.setD = datetime.strptime(self.cal.get(), '%d/%m/%Y')
				dia_ano = self.setD.timetuple().tm_yday
				for obss in self.listaobs.curselection():
					self.estacao_select.append(self.listaobs.get(obss).replace(","," ").replace("(","").replace(")","").split())
				self.estacao_select.sort(key=lambda srt: int(float(srt[self.varaxixY.get()])))
				print(self.estacao_select)
				self.max_lat = int(float(self.estacao_select[-1][self.varaxixY.get()]))
				self.min_lat = int(float(self.estacao_select[0][self.varaxixY.get()]))
				delta_lat = (self.max_lat-self.min_lat)
				self.matriz_tripa=[]
				self.eixoG = []
				if self.EST_ausent.size() > 0:
					self.EST_ausent.delete(0,END)
				for cont_index in np.arange(self.min_lat,self.max_lat+1):
					lista_lat_select = [int(float(x[self.varaxixY.get()])) for x in self.estacao_select]
					lista_dup = self.uti.list_duplicates_of(lista_lat_select,int(cont_index))
					if lista_dup:
						matriz_media = []
						matriz_ausent = []
						eixoG_dup=""
						for index_dub in lista_dup:
							eixoG_dup+=((" %s")%(self.estacao_select[index_dub][0]))
							nfile = (("/%s%.3i-%s-%.2i-%.2i.Std") % (self.estacao_select[index_dub][0].lower(),dia_ano,self.setD.year,self.setD.month,self.setD.day))						
							try:
								with open(self.filedir+nfile,'r',encoding="UTF-8") as arqDiaTec:
									tecest =  arqDiaTec.readlines()
									TMP_TEC = []
									for tmp_line in tecest:
										VTEC = ((tmp_line.split('\t')[1]).replace(",",".").strip())
										if VTEC == "-" or float(VTEC) < 0:
											TMP_TEC.append(-999.0)
										else:
											TMP_TEC.append(float(VTEC))
									tec_len = len(tecest)
									if  tec_len < 1440:
										tmp_delt = (1440 - tec_len)
										for inter_tmp in range(tmp_delt): 
											TMP_TEC.append(-999.0)
									self.matriz_tripa.append(TMP_TEC)
									matriz_media.append(TMP_TEC)
									arqDiaTec.close()
							except (IOError,IndexError):
								matriz_ausent.append(('%s (%s %s,%s %s) %s\n')%(self.estacao_select[index_dub][0],self.estacao_select[index_dub][1],self.estacao_select[index_dub][2],self.estacao_select[index_dub][3],self.estacao_select[index_dub][4],self.Dado_config.idioma(121)))
								self.matriz_tripa.append([-999.0]*1440)
								TMP_TEC = [-999.0]*1440
						for item_ausent in matriz_ausent:
							self.EST_ausent.insert(END,item_ausent)
						self.eixoG.append(eixoG_dup)
						len_matmed = len(matriz_media)		
						if len_matmed <= 1:
							self.matriz_tec.append(TMP_TEC)
						else:
							for item_media in range(len_matmed):
								if matriz_media[item_media] == ([-999.0]*1440):
									del(matriz_media[item_media])
							if matriz_media:
								self.matriz_tec.append([sum(e)/len(e) for e in zip(*matriz_media) if e != -999.0])
							else:
								self.matriz_tec.append([np.nan]*1440)
					else:
						self.eixoG.append("")
						self.matriz_tec.append([np.nan]*1440)
				self.titulo = self.setD.date()
				self.salvar_matriz()
				plt.clf()
				self.axes = self.fig.subplots()
				plt.minorticks_on()
	###########################|Títulos padrões|##############################################################################################################################################################
				if self.varaxixY.get() == 1:self.tituloy = self.Dado_config.idioma(63)
				else:self.tituloy = "Dip.Latitude"
				self.titulox = self.Dado_config.idioma(41)
				self.titulob = "VTEC"
	###########################|Personalizar o Gráfico|##############################################################################################################################################################
				#ao alterar latitude para Dip. a coluna Y(lat) deve-ser alterada
				try:
					if self.IHoras.get().strip(" ").replace(",",".") !="":
						self.vIHoras = float(self.IHoras.get().strip(" ").replace(",","."))
					else:
						self.vIHoras = 0
					if self.FHoras.get().strip(" ").replace(",",".") !="":  
						self.vFHoras = float(self.FHoras.get().strip(" ").replace(",","."))
					else:
						self.vFHoras = 24#23.983
					if self.txtvmax.get().strip(" ") != "" and float(self.txtvmax.get().strip(" ").replace(',','.')) != 0:
						self.vmax = float(self.txtvmax.get().strip(" ").replace(',','.'))
					else:
						self.vmax = 100.00
				except ValueError:
					messagebox.showerror(self.Dado_config.idioma(49),self.Dado_config.idioma(93),parent=self)
				self.atua_titulos()
				self.atua_grid_X()
				self.atua_grid_Y()
				self.passo = self.vmax/15
				self.level=np.arange(0,(self.vmax+(self.passo)),self.passo)
				plt.minorticks_on()
				plt.xlim(self.vIHoras*60,self.vFHoras*60)
				plt.tick_params(axis='both', which='major', width=float(self.largtick.get()),size=float(self.alttick.get()),labelsize=float(self.sizetick.get()))
				plt.tick_params(axis='both', which='minor' ,width=float(self.largtickMinor.get()) ,size=float(self.alttickMinor.get()))
				self.axes.yaxis.set_major_formatter(ticker.FuncFormatter(self.major_formatterest))
				self.axes.xaxis.set_major_formatter(ticker.FuncFormatter(self.major_formatterhora))
				self.matriz_tec = self.interpool(self.matriz_tec)
				cmap = plt.cm.get_cmap("jet")
				cmap.set_under("white")
				cmap.set_over("darkred")	
				self.EST_ausent.pack(fill=BOTH,expand=1,side=LEFT)
				self.sbau.pack(side=RIGHT,fill=Y)
	###########################|ColorBar|##############################################################################################################################################################
				self.passo_ctick = 10
				self.cbar = plt.colorbar(plt.contourf(self.matriz_tec,cmap=cmap,levels = self.level,vmin = 0,vmax=self.vmax, extend="both"),ticks = np.arange(0,self.vmax+1,self.passo_ctick))
				self.cbar.ax.set_title(self.titulob,**self.fontb) 
				self.cbar.ax.tick_params(width=float(self.largtick.get()),size=float(self.alttick.get()),labelsize=float(self.sizetick.get())) 
				self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
				self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
				self.toolbar.update()
				self.fig.canvas.draw()
	###########################|ColorBar|##############################################################################################################################################################
	###########################|Filme dos gráficos|##############################################################################################################################################################
				# buf = io.BytesIO()
				# plt.savefig(buf, format='png')
				# buf.seek(0)
				# img = PIL.Image.open(buf)
				#plt.rcParams['figure.figsize'] = 6.4,4.8
				#im.show()
				#buf.close()
	###########################|Filme dos gráficos|##############################################################################################################################################################
	###########################|Salvar gráfico ao plot|##############################################################################################################################################################
				self.save_png()		
				# if self.varVD.get() == True:
				# 	self.MATRIZ_CONTO_VD.append(img)
	###########################|Filme dos gráficos|##############################################################################################################################################################
				# if len(self.MATRIZ_CONTO_VD) > 1: 
				# 	self.framel[11].grid(column=0,rows=11,sticky=E+W)
				# 	self.framel[12].grid(column=0,rows=12,sticky=E+W)onpick1
				# 	self.framel[13].grid(column=0,rows=13,sticky=E+W)
				# 	self.btnVD.pack(side='bottom',fill=X)
				# 	self.btnVD2.pack(side='bottom',fill=X)
				# 	self.btnVD3.pack(side='bottom',fill=X)
				# 	self.framel14.grid_forget()
				# 	self.framel14.grid(column=0,rows=11,sticky=E+W)
				# 	# self.btnplot.pack_forget()
				# 	# self.btnplot.pack(side='bottom',fill=X)
				# else:
				# 	self.btnVD.pack_forget()
				# 	self.btnVD2.pack_forget()
				# 	self.btnVD3.pack_forget()
				# 	self.framel[11].grid_forget()
				# 	self.framel[12].grid_forget()
				# 	self.framel[13].grid_forget()
			else:
				messagebox.showerror(Utilitarios().idioma(49),Utilitarios().idioma(129),parent=self)
				self.focus_force()	
		else:
			messagebox.showerror(Utilitarios().idioma(49),Utilitarios().idioma(126),parent=self)
			self.selecionar()
			self.plotar()
			self.focus_force()
		plt.tight_layout()
		self.focus()
###########################|Filme dos gráficos|##############################################################################################################################################################
###########################|Interpolação da Matriz|##############################################################################################################################################################
	def interpool(self,array):
###########################|Interpolação Manual|##############################################################################################################################################################
		# matriz_tec_inter = []
		# #array = np.array(array)
		# for item_array_tec in zip(*array):
		# 	#for item_list_tec in item_array_tec:
		# 	lista_nan = self.list_duplicates_of(item_array_tec,np.nan)#array numpy error

		# 	print(lista_nan)	
		# 	# print(item_array_tec)
		# 	# print(lista_nan)
			
		# 	# array_indice = []
		# 	# for cont_ind in range(len(item_array_tec)):

		# 	# 	if not np.isnan(item_array_tec[cont_ind]):
		# 	# 		array_indice.append(item_array_tec[cont_ind])
		# 	# 	else:
		# 	# 		pass
		# return matriz_tec_inter
###########################|Interpolação Linha a Linha|##############################################################################################################################################################
		# from scipy.interpolate import interp1d
		# array = np.array(array)
		# matriz_tec_inter=[]
		
		# for item_array_tec in array.T:
		# 	x = np.array(item_array_tec)
		# 	not_nan = np.logical_not(np.isnan(x))
		# 	indices = np.arange(len(x))
		# 	interp = interp1d(indices[not_nan], x[not_nan])
		# 	matriz_tec_inter.append(interp(indices))
		# print(matriz_tec_inter)
		# return np.array(matriz_tec_inter).T
###########################|Interpolação SCIPY|##############################################################################################################################################################
		print(array)
		array = np.array(array)
		x = np.arange(0, array.shape[1])
		y = np.arange(0, array.shape[0])
		array = np.ma.masked_invalid(array)
		xx, yy = np.meshgrid(x, y)
		x1 = xx[~array.mask]
		y1 = yy[~array.mask]
		newarr = array[~array.mask]
		GD1 = interpolate.griddata((x1, y1), newarr.ravel(),(xx, yy),method='linear')
		return GD1	
###########################|Filme Gráfico|##############################################################################################################################################################
	"""
	Deletar ultima estação adiciona ao filme....
	"""
	def deletarULT(self):
		del(self.MATRIZ_CONTO_VD[-1])
		if len(self.MATRIZ_CONTO_VD) == 1: 
			self.btnVD.pack_forget()
			self.btnVD2.pack_forget()
			self.btnVD3.pack_forget()
			self.framel11.grid_forget()
			self.framel12.grid_forget()
			self.framel13.grid_forget()
###########################|Filme Gráfico|##############################################################################################################################################################
	"""
	Deletar todo o filme....
	"""
	def clearVD(self):
		self.MATRIZ_CONTO_VD.clear()
		if len(self.MATRIZ_CONTO_VD) < 1: 
			self.btnVD.pack_forget()
			self.btnVD2.pack_forget()
			self.btnVD3.pack_forget()
			self.framel11.grid_forget()
			self.framel12.grid_forget()
			self.framel13.grid_forget()
###########################|Propriedades Fonte geral|##############################################################################################################################################################
	"""
	Chamar a exibição do filme....
	"""
	def criarVD(self):
		for tmp_img in self.MATRIZ_CONTO_VD:
			tmp_img.show()
		#self.anim = animation.FuncAnimation(self.fig, self.animate, frames=len(self.MATRIZ_CONTO_VD))
		#print(self.MATRIZ_DATA_VD)
		#self.MATRIZ_DATA_VD = (list(set(self.MATRIZ_DATA_VD)))
		#FFMpegWriter = manimation.writers['ffmpeg']
		#fig = plt.figure()
		#self.anim = animation.FuncAnimation(fig, self.animate, frames=len(self.MATRIZ_DATA_VD))
		#self.anim.save('animation.mp4')
		#plt.show()
		#plt.showplt.savefig()

		# if len(self.MATRIZ_DATA_VD) > 1:
		#   metadata = dict(title='Compilação_ESTAÇÕES', artist='UTECDA - IP&DII',comment=(('Video criado em : %s pela ferramenta UTECDA')%(datetime.today())))
		#   writer = FFMpegWriter(fps=15, metadata=metadata)

		#   with writer.saving(fig, "writer_test.mp4", 100):
		#        for i in range(100):
		#           l.set_data(x0, y0)
		#           writer.grab_frame()
###########################|Propriedades Fonte geral|##############################################################################################################################################################
	def selecionarfonte(self,id,demo):
		font = askfont(self,str(demo),self.Dado_config.idioma(37))
	#"""    rguments:
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
			if id == 'X':
				self.fontx = font
			elif id == 'Y':
				self.fonty = font
			elif id == 'T':
				self.fontt = font
			elif id == 'B':
				self.fontb = font
			elif id == 'LTXY':
				self.fontLTXY = font
###########################|Itens duplicados de uma lista|##############################################################################################################################################################
###########################|Formatação dos EIXOS X|##############################################################################################################################################################
	def major_formatterhora(self,x, pos):
		return "%i" % ((x)/60)
###########################|Formatação dos EIXOS Y|##############################################################################################################################################################
	def major_formatterest(self,x, pos):
		resp = (("%.2f")%(x+(self.min_lat)))		
		if self.varest.get() == True and x % 1 == 0:
			print(self.eixoG,int(x),len(self.eixoG))
			resp = (("%s →%s")%((x+(self.min_lat)),self.eixoG[int(x)])  ) # ("%s ► %s") % (self.estacao_select[int(x)][0],self.estacao_select[int(x)][1])
		return resp

if __name__ == "__main__":
	root = Tk()
	teste = Graficosetor(root)
	root.mainloop()




















# def Carregar_prop(self):
# 		print('carreguei..')
# 		try:
# 			if self.IHoras.get().strip(" ").replace(",",".") !="":
# 				self.vIHoras = float(self.IHoras.get().strip(" ").replace(",","."))
# 			else:
# 				self.vIHoras = 0
# 			if self.FHoras.get().strip(" ").replace(",",".") !="":  
# 				self.vFHoras = float(self.FHoras.get().strip(" ").replace(",","."))
# 			else:
# 				self.vFHoras = 23.983
# 			if self.txtvmax.get().strip(" ") != "" and float(self.txtvmax.get().strip(" ").replace(',','.')) != 0:
# 				self.vmax = float(self.txtvmax.get().strip(" ").replace(',','.'))
# 			else:
# 				self.vmax = 100.00
# 		except ValueError:
# 			messagebox.showerror(self.Dado_config.idioma(49),self.Dado_config.idioma(93))
# 		self.passo = self.vmax/15
# 		self.level=np.arange(0,(self.vmax+1),self.passo)
# 		# if self.vargrid.get() == True:
# 		# 	plt.grid(True)
# 		# else:
# 		# 	plt.grid(False)
# 		self.titulo = str(datetime.strptime(self.cal.get(), '%d/%m/%Y').date())
# 		self.tituloy = self.Dado_config.idioma(40)
# 		self.titulox = self.Dado_config.idioma(41)
# 		self.titulob = "VTEC"
# 		try:
# 			if self.txtti.get().strip(' ') !="":
# 				self.titulo = self.txtti.get().strip(' ')
# 			if self.txttix.get().strip(' ') !="":
# 				self.titulox = self.txttix.get().strip(' ')
# 			if self.txttiy.get().strip(' ') !="":
# 				self.tituloy = self.txttiy.get().strip(' ')
# 			if self.txttib.get().strip(' ') !="":
# 				self.titulob = self.txttib.get().strip(' ')
# 			if self.nlbly.get() !="":
# 				Nlbly = int(self.nlbly.get().strip(' '))
# 				self.axes.yaxis.set_major_locator(ticker.LinearLocatoselfr(round(Nlbly)))
# 			elif self.nticky.get() !="":
# 				Nticky = float(self.nticky.get().strip(' ').replace(",","."))
# 				self.axes.yaxis.set_major_locator(ticker.IndexLocator(base=(Nticky), offset=self.vIHoras))
# 			else:
# 				if self.varest.get() == True:
# 					self.axes.yaxis.set_major_locator(ticker.IndexLocator(base=(1), offset=self.vIHoras))
# 				else:	
# 					self.axes.yaxis.set_major_locator(ticker.LinearLocator())            
			
# 			if self.nlblx.get() !="":
# 				Nlblx = int(self.nlblx.get().strip(' '))
# 				self.axes.xaxis.set_major_locator(ticker.LinearLocator(round(Nlblx)))
# 			elif self.ntickx.get() !="":
# 				Ntickx = float(self.ntickx.get().strip(' ').replace(",","."))
# 				self.axes.xaxis.set_major_locator(ticker.IndexLocator(base=(Ntickx*60), offset=0))
# 			else:
# 				self.axes.xaxis.set_major_locator(ticker.IndexLocator(base=(60), offset=0))
# 		except AttributeError:
# 			pass

# 		plt.title(self.titulo,**self.fontt)
# 		#plt.minorticks_on()
# 		plt.ylabel(self.tituloy,rotation=90,**self.fonty)
# 		plt.xlim(self.vIHoras*60,self.vFHoras*60)
# 		self.axes.yaxis.set_major_formatter(ticker.FuncFormatter(self.major_formatterest))
# 		self.axes.xaxis.set_major_formatter(ticker.FuncFormatter(self.major_formatterhora))
# 		plt.xlabel(self.titulox,**self.fontx)

# 		try:
# 			self.p.set_vmax(self.vmax)
# 			self.p.set_level(self.level)
# 			self.cbar.set_ticks(np.arange(0,self.vmax+1,self.passo_ctick))
		
# 		except:
# 			print('except')
# 			pass
# 		#update_ticks() 	
# 		print('passei aqui')	