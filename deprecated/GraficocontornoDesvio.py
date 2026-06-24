from pyqt_utils import FigureCanvasQTAgg, NavigationToolbar2QT

from matplotlib.ticker import LinearLocator , FuncFormatter,IndexLocator,FixedLocator
from pyqt_utils import Toplevel, ttk, messagebox
from datetime import datetime, timedelta, date
from pyqt_utils.filedialog import askdirectory
from calendar_widget import Calendar
import matplotlib.ticker as ticker
from qtfontchooser import askfont
from qt_calendar import DateEntry
import matplotlib,calendar,math
import matplotlib.pyplot as plt
from util import Utilitarios,VerticalScrolledFrame,DadoIdioma

# from Trash import DraggableRectangle
from pyqt_utils import *
import pyqt_utils as ui
import numpy as np
from Est_selector import EstSelector
matplotlib.use("QtAgg")
class Graficodesvio(Toplevel):
###########################|Bob ô construtor|##############################################################################################################################################################
	def __init__(self,root):
		Toplevel.__init__(self,root)
		plt.rc('font', weight='bold')
		plt.rc('axes',linewidth=2)
		self.temp = np.array([x for x in np.arange(0,24,(1/60))])					
		self.titulo=self.titulox=self.tituloy=""
		self.fonty = self.fontt = self.fontb = self.fontLTXY = self.fontx = {'family' : 'Arial',
		'weight' : 'bold',
		'size'   : 18}
		self.vargrid_X = BooleanVar(self)
		self.vargrid_Y = BooleanVar(self)
		self.varsave = BooleanVar(self)
		self.varmatriz = BooleanVar(self)
		self.filedir =r"C:\Users\Mateus_Pillat\Google Drive\Estágio\Dados\STD"
		# self.filedir =r"C:\Users\Mateus-Not\Google Drive\Estágio\Dados\STD")
		#C:\Users\  mateu     \Google Drive\Estágio\STD - note
		#C:\Users\  teste     \Google Drive\Estágio\STD - lab
		self.uti = Utilitarios()
		self.utiC = DadoIdioma()
		# self.teste_frame = Frame(self)
		# self.teste_frame.pack(fill='both',expand=1)
		self.frame_canvas = VerticalScrolledFrame(self)#.teste_frame)
		self.frame_canvas.pack(side='left',fill='both')

		nb = ttk.Notebook(self)
		
		self.page1 = Frame(self,bg='gray')
		self.page2 = Frame(self)
		self.page1.bind('<FocusIn>',lambda e: self.refreshCanvas())
		
		nb.add(self.page1,text = self.Dado_config.idioma(7))
		nb.add(self.page2,text = self.Dado_config.idioma(17))
		nb.pack(expand=1,side='right',fill='both')


		self.fig, self.axes = plt.subplots()
		self.canvas = FigureCanvasQTAgg(self.fig,self.page1)
		self.canvas.draw()
		self.toolbar = NavigationToolbar2QT(self.canvas, self.page1)
		# plt.tight_layout()
		# self.canvas_frame()
		# self.toolbar = NavigationToolbar2QT(self.canvas, self.page1)
###########################|Canvas para a scrollbar..|##############################################################################################################################################################
		# self.canvas_prop = Canvas(self)
		# self.canvas_prop.pack(fill = 'both',expand=1)
		self.frame_prop_rap = Frame(self.frame_canvas.interior,bg = 'gray',bd=3,relief=GROOVE)
		self.frame_prop_rap.pack(side='left',fill='both')
		# self.canvas_prop.create_window((0,0),window=self.frame_prop_rap,anchor='nw')
		# self.sb_prop = Scrollbar(self.frame_prop_rap,command=self.canvas_prop.yview)
		# self.sb_prop.pack(side=LEFT,fill=Y)
		# self.canvas_prop.configure(yscrollcommand = self.sb_prop.set)
		# self.canvas_prop.bind('<Configure>', self.on_configure)


###########################|Canvas para a scrollbar..|##############################################################################################################################################################
###########################|Lista Estações|##############################################################################################################################################################
		self.frame_listaobs = Frame(self.frame_prop_rap)
		self.frame_listaobs.pack(fill='both',expand=1)
###########################|Lista frame lista.....extend|##############################################################################################################################################################
		self.dirstd = Button(self.frame_listaobs, text=self.Dado_config.idioma(18),command=self.selecionar,relief=RIDGE)
		self.dirstd.pack(side='top',fill=X)
		self.listaobs = Listbox(self.frame_listaobs,selectmode="single",highlightthickness=0,exportselection=0,bd=3,relief='groove')
		self.listaobs.bind("<<ListboxSelect>>",lambda e:self.plotar(1))
		self.listaobs.pack(side='left',fill=BOTH,expand=1)

		n_list,conteudo_lista = self.uti.Refresh_list_obs(self.filedir,int(2019),True)
		# self.listaobs.configure(source=(conteudo_lista+[item + " ("+ self.Dado_config.idioma(144) +")" for item in n_list]) )
		# self.listaobs.configure(source=[item + " ("+ self.Dado_config.idioma(144) +")" for item in n_list])
		[self.listaobs.insert(END, item) for item in conteudo_lista]
		[self.listaobs.insert(END, item + " ("+ self.Dado_config.idioma(144) +")") for item in n_list]

		# self.listaobs.select_set(1)
		#self.listaobs.bind("<<ListboxSelect>>",self.seta)
		self.sb = Scrollbar(self.frame_listaobs)
		self.sb.pack(side=RIGHT,fill=Y)
		self.sb.configure(command=self.listaobs.yview)
		self.listaobs.configure(yscrollcommand=self.sb.set)
###########################|Lista Estações|##############################################################################################################################################################
###########################|Calendario seletor..dias..|##############################################################################################################################################################
		self.frame_seletor_dias = Frame(self.frame_prop_rap,bd=3,relief=GROOVE)
		self.frame_seletor_dias.pack(fill='both')
###########################|Calendario seletor..dias..|##############################################################################################################################################################
###########################|Lista Estações|##############################################################################################################################################################


###########################|Mapa estações..|##############################################################################################################################################################
		# Button(self.frame_seletor_dias,text='MAPA...',command=lambda e=self:EstSelector(e)).pack(side=BOTTOM)
###########################|Mapa estações.. |##############################################################################################################################################################
		
		Label(self.frame_seletor_dias,text=self.Dado_config.idioma(123)).pack(fill=X)
		#self.maisdata = Button(self.framepg3,text="→",command=self.righh,font="SimHei 10 bold roman")
		#self.menosdata = Button(self.framepg3,text="←",command=self.leff,font="SimHei 10 bold roman")
		#self.ano = 0
		#self.dData = StringVar ()
###########################|Selecionar dias calmos|##############################################################################################################################################################
		# print(self.Dado_config.idioma(0))
		self.cal_days = Calendar(self.frame_seletor_dias, font="Arial 10", selectmode='day',cursor="hand2",Locator=self.Dado_config.idioma(0),day=1,year = 2017,month=9)
		self.cal_days.pack(fill="both", expand=True)		
		# vcmd = (self.register(self.uti.onValidateself.sigla),'%S', '%s','%d',2)
		# self.txt_dias_calmos = Entry(self.frame_seletor_dias,validatecommand=vcmd,validate='key')
		# self.txt_dias_calmos.pack(fill=X)
###########################|Selecionar dias pertubados |##############################################################################################################################################################
		Label(self.frame_seletor_dias,text=self.Dado_config.idioma(124),relief=RIDGE).pack(fill=X)
		Label(self.frame_seletor_dias,text=self.Dado_config.idioma(53)).pack(fill=X)
		self.cal = DateEntry(self.frame_seletor_dias, background='darkblue',foreground='white', borderwidth=1,year = 2017,day=26,month=9)
		self.cal.bind('<<DateEntrySelected>>',self.atuaAno)
		self.cal.pack(fill='both',expand = True)
		self.ano = 0
		# self.atuaAno()
		Label(self.frame_seletor_dias,text=self.Dado_config.idioma(54)).pack(fill=X)
		self.cal2 = DateEntry(self.frame_seletor_dias, background='darkblue',foreground='white', borderwidth=1,year = 2017,day=30,month=9)
		self.cal2.pack(fill='both',expand = True)
###########################|Selecionar dias pertubados |##############################################################################################################################################################
		self.frame_prop = Frame(self.frame_prop_rap)
		self.frame_prop.pack(fill=X)
		self.frame_prop_it = []
		for rowit in range(11):
			self.frame_prop_it.append(Frame(self.frame_prop,bd=3,relief=GROOVE))
			self.frame_prop_it[rowit].pack(fill=X)
		Label(self.frame_prop_it[0],text=self.Dado_config.idioma(24),relief=GROOVE).pack(fill=X)
		Label(self.frame_prop_it[1],text="Horizontal",relief=GROOVE).pack(side='left')
		Checkbutton(self.frame_prop_it[1],variable=self.vargrid_Y,width=5,command=self.atua_grid_Y).pack(side='left')
		Checkbutton(self.frame_prop_it[1],variable=self.vargrid_X,width=5,command=self.atua_grid_X).pack(side='right')
		Label(self.frame_prop_it[1],text="Vertical",relief=GROOVE).pack(side='right')			
		Label(self.frame_prop_it[2],text=self.Dado_config.idioma(25),relief=GROOVE).pack(side='left')	
		Checkbutton(self.frame_prop_it[2],variable=self.varsave,width=5,command=self.save_png).pack(side='left')
		Checkbutton(self.frame_prop_it[2],variable=self.varmatriz,width=5,command=self.salvar_matriz).pack(side='right')
		Label(self.frame_prop_it[2],text=self.Dado_config.idioma(91),relief=GROOVE).pack(side='right')	
		Label(self.frame_prop_it[3],text=self.Dado_config.idioma(130),relief=GROOVE).pack()	
		self.DateFormat = IntVar(self)
		self.DateFormat.set(1)
		Radiobutton(self.frame_prop_it[4],relief=GROOVE,variable=self.DateFormat,command=self.refreshCanvas ,value=1,text=self.Dado_config.idioma(40)).pack(side='left',fill=X,expand=1)
		Radiobutton(self.frame_prop_it[4],relief=GROOVE,variable=self.DateFormat,command=self.refreshCanvas ,value=0,text=self.Dado_config.idioma(131)).pack(side='right',fill=X,expand=1)
		self.Legend = BooleanVar(self)
		Label(self.frame_prop_it[5], text=self.Dado_config.idioma(134),relief=GROOVE).pack(side="left")
		Checkbutton(self.frame_prop_it[5],variable=self.Legend,command=self.atua_legend).pack(fill=X,expand=1,side='left')
		Label(self.frame_prop_it[5], text=self.Dado_config.idioma(136),relief=GROOVE).pack(side='left')
		self.sub_plt = BooleanVar(self)
		Checkbutton(self.frame_prop_it[5],variable=self.sub_plt,command=self.atua_sb_plt).pack(fill=X,expand=1,side='left')
		Label(self.frame_prop_it[7], width=20, text=self.Dado_config.idioma(133),relief=GROOVE).pack(side='left')
		vcmd = (self.register(self.uti.onValidatesigla),'%S', '%s','%d',2)
		self.Tmax = Entry(self.frame_prop_it[7],exportselection=0,validate="key",validatecommand=vcmd)
		self.Tmax.pack(side='right')
		Label(self.frame_prop_it[8], width=20, text=self.Dado_config.idioma(132),relief=GROOVE).pack(side='left')
		self.Tmin = Entry(self.frame_prop_it[8],exportselection=0,validate="key",validatecommand=vcmd)
		self.Tmin.pack(side='right')
		Button(self.frame_prop_it[9], width=20, text=self.Dado_config.idioma(108),relief=RIDGE, command= self.plotar).pack(side='bottom',fill=X)
		# Button(self.frame_prop_it[10], text='refresh',relief=RIDGE, command= self.refreshCanvas).pack(side='bottom',fill=X)
		# Button(self.frame_prop_it[9], width=20, text=self.Dado_config.idioma(26),relief=RIDGE, command= self.refreshCanvas).pack(side='bottom',fill=X)
###########################|Propriedades Gráfico|##############################################################################################################################################################
		self.framefront = Frame(self.page2,bd=3,bg="blue",relief=GROOVE)
		self.framefront.pack(side='left',fill=Y)
		self.framep=[]
		for rowp in range(10):
			self.framep.append(Frame(self.framefront,bd=3,bg='gray',relief=GROOVE))
			self.framep[rowp].pack(fill=X)
		self.lblindica = Label(self.framep[0],relief='groove', text=self.Dado_config.idioma(27))
		self.lblindica.pack(fill='both')
		# self.lblntickx = Label(self.framep[1],relief='groove' ,text=self.Dado_config.idioma(28))
		# self.lblntickx.pack(side='left',fill=X,expand=1)
		# vcmd = (self.register(self.uti.onValidatesigla),'%S', '%s','%d',2,10)
		# self.ntickx = Entry(self.framep[1],exportselection=0,validate="key",validatecommand=vcmd)
		# self.ntickx.pack(side='right',fill=X)
		# self.ntickx.bind("<FocusOut>",lambda habil:self.habil(self.ntickx,self.nlblx))
		# self.lblnlblx = Label(self.framep[3],relief='groove', text=self.Dado_config.idioma(30))
		# self.lblnlblx.pack(side='left') 
		# vcmd = (self.register(self.uti.onValidatesigla),'%S', '%s','%d',2,10)
		# self.nlblx = Entry(self.framep[3],exportselection=0,validate="key",validatecommand=vcmd)
		# self.nlblx.pack(side='right')
		# self.nlblx.bind("<FocusOut>",lambda habil:self.habil(self.nlblx,self.ntickx))    
		Label(self.framep[2],relief=GROOVE, text=self.Dado_config.idioma(29)).pack(side='left',fill=X,expand=1)   
		vcmd = (self.register(self.uti.onValidatesigla),'%S', '%s','%d',2,10)
		self.nticky = Entry(self.framep[2],exportselection=0,validate="key",validatecommand=vcmd)
		self.nticky.pack(side='right',fill=X)
		self.nticky.bind("<FocusOut>",lambda habil=1:self.habil(self.nticky,self.nlbly))
		Label(self.framep[4],relief=GROOVE, text=self.Dado_config.idioma(31)).pack(side='left')       
		vcmd = (self.register(self.uti.onValidatesigla),'%S', '%s','%d',2,10)
		self.nlbly = Entry(self.framep[4],exportselection=0,validate="key",validatecommand=vcmd)
		self.nlbly.pack(side='right')
		self.nlbly.bind("<FocusOut>",lambda habil=1:self.habil(self.nlbly,self.nticky))
		# self.lbltix 
		Label(self.framep[5],relief=GROOVE,text=self.Dado_config.idioma(32)).pack(side='left',fill=X,expand=1)
		self.txttix = Entry(self.framep[5],exportselection=0)
		self.txttix.pack(side='right')
		# self.lbltiy
		Label(self.framep[6],relief=GROOVE,text=self.Dado_config.idioma(33)).pack(side='left',fill=X,expand=1)
		self.txttiy = Entry(self.framep[6],exportselection=0)
		self.txttiy.pack(side='right')
		# self.lblti
		Label(self.framep[7],relief=GROOVE, text=self.Dado_config.idioma(34)).pack(side='left',fill=X,expand=1)        
		self.txtti = Entry(self.framep[7],exportselection=0)
		self.txtti.pack(side='right')
		self.framef=[]
		for rowf in range(17):
			self.framef.append(Frame(self.framefront,bd=3,bg='gray',relief=GROOVE))
			self.framef[rowf].pack(fill=X)
		Label(self.framef[0],relief=GROOVE,text=self.Dado_config.idioma(36)).pack(fill='both')
###########################|Propriedades Fonte geral|##############################################################################################################################################################
		#Label(self.framef[1],text='Fonte geral').pack(side='left',ipady=2)
		#Button(self.framef[1],text='Selecionar Fonte',command=lambda id='G':self.selecionarfonte(id)).pack(side='right')		
###########################|Propriedades Fonte geral|##############################################################################################################################################################
		Label(self.framef[2],relief=GROOVE,text=self.Dado_config.idioma(32)).pack(side='left',fill='both',expand=1)
		Button(self.framef[2],text=self.Dado_config.idioma(37),command=lambda id='X':self.selecionarfonte(id,self.titulox),relief=RIDGE).pack(side='right')
		Label(self.framef[3],relief=GROOVE,text=self.Dado_config.idioma(33)).pack(side='left',fill='both',expand=1)
		Button(self.framef[3],text=self.Dado_config.idioma(37),command=lambda id='Y':self.selecionarfonte(id,self.tituloy),relief=RIDGE).pack(side='right')
		Label(self.framef[4],relief=GROOVE,text=self.Dado_config.idioma(34)).pack(side='left',fill='both',expand=1)
		Button(self.framef[4],text=self.Dado_config.idioma(37),command=lambda id='T':self.selecionarfonte(id,self.titulo),relief=RIDGE).pack(side='right')
		self.sizetick = StringVar(self)
		# self.sizetick.set('16')
		self.sizetick.set(self.utiC.getSizeLabelsTick(2))
		Label(self.framef[5],relief=GROOVE,text=self.Dado_config.idioma(115)).pack(fill=X,expand=1)
		Button(self.framef[8],relief='ridge',text='-',font = {'font.size': 22},command=lambda e='-' :self.sizeTICK(self.sizetick,e)).pack(fill='x',side="left",expand=True)		
		Button(self.framef[8],relief='ridge',text='+',font = {'font.size': 22},command=lambda e='+' :self.sizeTICK(self.sizetick,e)).pack(fill='x',side="right",expand=True)		
		self.lbllltick = Label(self.framef[8],relief=GROOVE,textvariable=self.sizetick,font = 'Levenim\ MT 10 bold roman',width=10)
		self.lbllltick.pack(fill='both',expand=True)
		Label(self.framef[9],relief=GROOVE,text=self.Dado_config.idioma(116)).pack(fill=X,expand=1)
		self.largtick = StringVar(self)
		# self.largtick.set('2.0')
		self.largtick.set(self.utiC.getWidthTickMajor(2))
		Button(self.framef[10],relief='ridge',text='-',command=lambda e='-' :self.largTICK(self.largtick,e,'major')).pack(fill='x',side="left",expand=True)		
		Button(self.framef[10],relief='ridge',text='+',command=lambda e='+' :self.largTICK(self.largtick,e,'major')).pack(fill='x',side="right",expand=True)		
		self.lbllllargtick = Label(self.framef[10],relief=GROOVE,textvariable=self.largtick,font = 'Levenim\ MT 10 bold roman',width=10)
		self.lbllllargtick.pack(fill='both',expand=True)	
		Label(self.framef[11],relief=GROOVE,text=self.Dado_config.idioma(117)).pack(fill=X,expand=1)
		self.alttick = StringVar(self)
		# self.alttick.set('9.0')
		self.alttick.set(self.utiC.getHeightTickMajor(2))
		Button(self.framef[12],relief='ridge',text='-',command=lambda e='-' :self.altTICK(self.alttick,e,'major')).pack(fill='x',side="left",expand=True)		
		Button(self.framef[12],relief='ridge',text='+',command=lambda e='+' :self.altTICK(self.alttick,e,'major')).pack(fill='x',side="right",expand=True)		
		self.lblllalttick = Label(self.framef[12],relief=GROOVE,textvariable=self.alttick,font = 'Levenim\ MT 10 bold roman',width=10)
		self.lblllalttick.pack(fill='both',expand=True)	
		Label(self.framef[13],relief=GROOVE,text=self.Dado_config.idioma(118)).pack(fill=X,expand=1)
		self.largtickMinor = StringVar(self)
		# self.largtickMinor.set('2.0')
		self.largtickMinor.set(self.utiC.getWidthTickMinor(2))
		Button(self.framef[14],relief='ridge',text='-',command=lambda e='-' :self.largTICK(self.largtickMinor,e,'minor')).pack(fill='x',side="left",expand=True)		
		Button(self.framef[14],relief='ridge',text='+',command=lambda e='+' :self.largTICK(self.largtickMinor,e,'minor')).pack(fill='x',side="right",expand=True)		
		self.lbllllargtickMinor = Label(self.framef[14],relief=GROOVE,textvariable=self.largtickMinor,font = 'Levenim\ MT 10 bold roman',width=10)
		self.lbllllargtickMinor.pack(fill='both',expand=True)	
		Label(self.framef[15],relief=GROOVE,text=self.Dado_config.idioma(119)).pack(fill=X,expand=1)
		self.alttickMinor = StringVar(self)
		# self.alttickMinor.set('4.5')
		self.alttickMinor.set(self.utiC.getHeightTickMinor(2))
		Button(self.framef[16],relief='ridge',text='-',command=lambda e='-' :self.altTICK(self.alttickMinor,e,'minor')).pack(fill='x',side="left",expand=True)		
		Button(self.framef[16],relief='ridge',text='+',command=lambda e='+' :self.altTICK(self.alttickMinor,e,'minor')).pack(fill='x',side="right",expand=True)		
		self.lblllalttickMinor = Label(self.framef[16],relief=GROOVE,textvariable=self.alttickMinor,font = 'Levenim\ MT 10 bold roman',width=10)
		self.lblllalttickMinor.pack(fill='both',expand=True)	
###########################|Propriedades Fonte geral|##############################################################################################################################################################
		self.bind("<Up>",lambda e: self.uti.up_lista(self.listaobs))
		self.bind("<Down>",lambda e: self.uti.down_lista(self.listaobs))
		# self.wait_visibility(self)
		# self.grab_set()
		# self.lift()
		self.bind("<Return>",self.plotar)
		self.protocol("WM_DELETE_WINDOW",self.quit)
		self.geometry('800x600')
		self.iconbitmap(r'icone.ico')
		self.state('zoomed')
		#São Gabriel da Cachoeira, AM, SAGA, 93913, -0° 09', -67° 3', 
#🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥
	def quit(self):
		self.uti.troca(root,self,plt)
		for val,i in zip([self.sizetick.get(),self.largtick.get(),self.alttick.get(),self.largtickMinor.get(),self.alttickMinor.get()],range(11,16)):
			self.utiC.setConfig(val,i,2)
	def plotar(self,*e):
		plt.tight_layout()
		if self.filedir:
			if len(self.listaobs.curselection()) > 0:
				if self.cal_days.selection_get():
					if self.sub_plt.get() == True:
						self.atua_sb_plt()
						return 0
					plt.clf()
					self.fig.clf()
					self.axes = self.fig.subplots()
					id = self.listaobs.curselection()
					self.coleta_dados(id)

					if np.mean(self.matriz_tec_p) == -999.0 or np.mean(self.matriz_tec_p) == np.nan:
						plt.text(.5,.5, Utilitarios().idioma(94), size=16,ha="center", va="center" )
					else:
						re = self.delta.days + 1
						self.temp_fr = np.array([x for x in np.arange(0,24*re,(1/60))])
						self.y1 = np.tile(self.media_calmo-self.desvio_calmo,re)
						self.y2 = np.tile(self.media_calmo+self.desvio_calmo,re)
						self.m_p = np.tile(self.media_calmo,re)
						self.titulo = ('%s-%s-%.2i(%s-%s)')%(self.sigla.lower(),self.dataI.year,self.dataI.month,self.dataI.day,self.dataF.day) 
						self.tituloy = "TEC"
						self.titulox = self.Dado_config.idioma(40)
						# self.fig, self.axes = plt.subplots()
###########################|linewidth=10|##############################################################################################################################################################
						'''
							Ideia:Poder editar a grossura da linha dos plots vermelhos e pretos..
						'''
						plt.fill_between(self.temp_fr,self.y1,self.y2, color='gray', label=self.Dado_config.idioma(125))
						plt.plot(self.temp_fr,self.m_p, color='black', label=self.Dado_config.idioma(138) ,linewidth=3.0)
						plt.plot(self.temp_fr,self.te_p_reshape, color='r', label='Tec',linewidth=2.5)
###########################|linewidth=10|##############################################################################################################################################################
###########################|Aplicação das Propriedades|##############################################################################################################################################################
						self.fig.patch.set_facecolor('lightgrey')
						self.axes.set_facecolor("lightgrey")
						self.axes.xaxis.grid(self.vargrid_X.get())
						self.axes.yaxis.grid(self.vargrid_Y.get())
						self.axes.xaxis.set_major_locator(ticker.IndexLocator(base=(24), offset=0))
						self.axes.xaxis.set_major_formatter(ticker.FuncFormatter(self.major_format_x))
						self.atua_titulos()
						plt.xlim(0,24*re)
						self.atua_limY()
						self.setar_legends()
						plt.tick_params(axis='both',direction='inout', which='major',top=True,right=True, width=float(self.largtick.get()),size=float(self.alttick.get()),labelsize=float(self.sizetick.get()))
						plt.tick_params(axis='both',direction='inout', which='minor' ,top=True,right=True,width=float(self.largtickMinor.get()) ,size=float(self.alttickMinor.get()))
						plt.minorticks_on()
						plt.title(self.titulo,**self.fontt)
						plt.ylabel(self.tituloy,rotation=90,**self.fonty)
						plt.xlabel(self.titulox,**self.fontx)
						
###########################|Aplicação das Propriedades|##############################################################################################################################################################
					self.fig.set_facecolor('lightgrey')
					self.axes.set_facecolor("lightgrey")
					self.fig.canvas.draw()
					# self.canvas.draw()

					self.canvas.get_widget().pack(side=ui.BOTTOM, fill=ui.BOTH, expand=True)
					self.canvas._qt_canvas.pack(side=ui.TOP, fill=ui.BOTH, expand=True)
					self.toolbar.update()
					self.save_png()
					self.salvar_matriz()
				else:
					messagebox.showerror(self.Dado_config.idioma(49),self.Dado_config.idioma(128),parent=self)
					self.focus_force()

			else:
				messagebox.showerror(self.Dado_config.idioma(49),self.Dado_config.idioma(127),parent=self)
				self.focus_force()	
		else:
			messagebox.showerror(self.Dado_config.idioma(49),self.Dado_config.idioma(126),parent=self)
			self.selecionar()
			self.plotar()	
			self.focus_force()

		# self.listaobs.focus_force()
	def coleta_dados(self,id):
		self.sigla = self.listaobs.get(id).replace(",","").replace("(","").replace(")","").split()[0]
		self.dip_lat = float(self.listaobs.get(id).replace(",","").replace("(","").replace(")","").split()[5])
		self.dataI = datetime.strptime(self.cal.get(), '%d/%m/%Y')
		self.dataF = datetime.strptime(self.cal2.get(), '%d/%m/%Y')
		self.delta = self.dataF - self.dataI
		



		self.matrizstd = []
		for dia_select in self.cal_days.selection_get():
			nomefile = ("/%s%.3i-%i-%.2i-%.2i.Std") % (self.sigla.lower(),dia_select.timetuple().tm_yday,dia_select.year,dia_select.month,dia_select.day)
			caminho_arquivo = self.filedir + nomefile
			self.matrizstd.append(self.uti.Leitura_trip(caminho_arquivo))
		self.matrizstd = np.array(self.matrizstd).T
		


		self.media_calmo = []
		self.desvio_calmo = []
		for tec_lst in [s for e in self.matrizstd for s in e]:
			lista_e = np.array([x for x in tec_lst if x>0])
			self.desvio_calmo.append(np.std(lista_e))
			self.media_calmo.append(np.mean(lista_e))			
		self.media_calmo = np.array(self.media_calmo)
		self.desvio_calmo = np.array(self.desvio_calmo)
		

		
		
		
		
		self.matriz_tec_p = []
		self.datas_axes_X = []
		for contd in range(self.delta.days+1):
			datafile = (self.dataI + timedelta(days=contd))
			self.datas_axes_X.append([datafile.date(),datafile.day])
			nomefile_p = ("/%s%.3i-%i-%.2i-%.2i.Std") % (self.sigla.lower(),datafile.timetuple().tm_yday,datafile.year,datafile.month,datafile.day)
			caminho_arquivo_p = self.filedir + nomefile_p
			self.matriz_tec_p.append(self.uti.Leitura_trip(caminho_arquivo_p))
		else:
			self.datas_axes_X.append([(self.dataF+ timedelta(days=1)).date(),((self.dataF+ timedelta(days=1)).date()).day ])
		
		self.matriz_tec_p = np.array(self.matriz_tec_p)
		self.te_p_reshape = []
		for tt_ in self.matriz_tec_p:
			for ss_ in tt_:
				for ff_ in ss_:
					if ff_ < 0:
						self.te_p_reshape.append(np.nan)
					else: 
						self.te_p_reshape.append(ff_)

###########################|Propriedades Fonte geral|##############################################################################################################################################################
	# def canvas_frame(self):
		# self.fig, self.axes = plt.subplots()
	
	"""
		Controle de quantidade das labels vs o intervalo delas
	"""
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

	def habil(self,objt1,objt2):
		if objt1.get().strip() != "":
			objt2.config(state="disabled",bg="gray")
		elif objt2['state']=="disabled":
			objt2.config(state="normal",bg="white")
	def salvar_matriz(self):
		# print('sei')
###########################| |\/|Atriz do tipo Tripa...|##############################################################################################################################################################
		if self.varmatriz.get() == True:
			try:
				tec_m = np.array(self.C_tec).reshape(len(self.C_tec),int(len(self.te_p_reshape)/1440),1440)
				print(tec_m)
				for tec_n,sigla,med,desv in zip(tec_m,self.C_sigla,self.C_media,self.C_desvio):
					nome = ('%s-%s-%.2i(%s-%s)')%(sigla,self.dataI.year,self.dataI.month,self.dataI.day,self.dataF.day)
					self.matriz_linha((r"%s\%s.Std")%(self.filedir,nome),tec_n,med,desv)
			except AttributeError:
				tec_n = np.array(self.te_p_reshape).reshape(int(len(self.te_p_reshape)/1440),1440)
				self.matriz_linha((r"%s\%s.Std")%(self.filedir,self.titulo),tec_n,self.media_calmo,self.desvio_calmo)
###########################| |\/|Atriz do tipo Tripa...|##############################################################################################################################################################
	def matriz_linha(self,caminho,tec_n,med_calm,desv_calmo):
		try:
			with open(caminho,'w') as arqTri:
				arqTri.write("Média\tMed+Des\tMed-Des")
				for contd in range(self.delta.days+1):
					datafile = (self.dataI + timedelta(days=contd)) 
					arqTri.write(("\tHora\tTec %i")%(datafile.day))
				else:
					arqTri.write("\n")
				for t,tec_est,m,d in zip(self.temp,tec_n.T,med_calm,desv_calmo):
					arqTri.write(((("%.2f\t%.2f\t%.2f")%(m,(m+d),(m-d))).replace("nan","-999,0")).replace(".",","))
					for tec_dia in tec_est:
						arqTri.write(((("\t%.2f\t%.2f")%(t,tec_dia)).replace("nan","-999,0")).replace(".",","))
					else:
						arqTri.write("\n")
		except (IOError):
				pass

	def atua_titulos(self):
		if self.txtti.get().strip(' ') !="":
			self.titulo = self.txtti.get().strip(' ')
		if self.txttix.get().strip(' ') !="":
			self.titulox = self.txttix.get().strip(' ')
		if self.txttiy.get().strip(' ') !="":
			self.tituloy = self.txttiy.get().strip(' ')
		if self.sub_plt.get() == True:
			if len(self.listaobs.curselection()) >1:
				for ax_s in self.axes:
					ax_s[0].set_ylabel(self.tituloy,rotation=90,**self.fonty)
			else:
				self.axes[0].set_ylabel(self.tituloy,rotation=90,**self.fonty)
			

			if self.nlbly.get() !="":
				Nlbly = int(self.nlbly.get().strip(' '))
				for axs in self.axes.flatten():
					axs.yaxis.set_major_locator(ticker.LinearLocator(int(Nlbly)))
			elif self.nticky.get() !="":
				Nticky = float(self.nticky.get().strip(' ').replace(",","."))
				for axs in self.axes.flatten():
					axs.yaxis.set_major_locator(ticker.IndexLocator(base=(Nticky), offset=0))
				# self.fig.suptitle(self.titulo,**self.fontt)
				# self.fig.suptitle(self.titulox,**self.fontt,y=.06)
			# self.fig.text(.504,.02, self.titulox,ha='center', fontsize=20)
			# plt.xlabel(self.titulox,**self.fontx)
			
		else:
			if self.nlbly.get() !="":
				Nlbly = int(self.nlbly.get().strip(' '))
				self.axes.yaxis.set_major_locator(ticker.LinearLocator(round(Nlbly)))
			elif self.nticky.get() !="":
				Nticky = float(self.nticky.get().strip(' ').replace(",","."))
				self.axes.yaxis.set_major_locator(ticker.IndexLocator(base=(Nticky), offset=0))
			plt.title(self.titulo,**self.fontt)
			plt.ylabel(self.tituloy,rotation=90,**self.fonty)
			plt.xlabel(self.titulox,**self.fontx)
# 

		# if self.Tmin.get or self.Tmax:

		# else:
			# self.axes.yaxis.set_major_locator(ticker.LinearLocator())            
			# if self.nlblx.get() !="":
			# 	Nlblx = int(self.nlblx.get().strip(' '))
			# 	self.axes.xaxis.set_major_locator(ticker.LinearLocator(round(Nlblx)))
			# elif self.ntickx.get() !="":
			# 	Ntickx = float(self.ntickx.get().strip(' ').replace(",","."))
			# 	self.axes.xaxis.set_major_locator(ticker.IndexLocator(base=(Ntickx*60), offset=0))
			# else:
			# 	self.axes.xaxis.set_major_locator(ticker.IndexLocator(base=(60), offset=0))
		# except AttributeError:
		# 	pass
	def atua_sb_plt(self):

		# fig = plt.figure()
		# ax = fig.add_subplot(111)
		# rects = ax.bar(range(10), 20*np.random.rand(10))
		
		# drs = 	[]
		# for rect in rects:
		#     dr = DraggableRectangle(rect)
		#     dr.connect()
		#     drs.append(dr)
		try:
			if self.sub_plt.get() == True:
				self.listaobs.configure(selectmode="multiple")
				id = self.sort_dip_(self.listaobs.curselection())
				self.fig.clf()
				self.axes = self.fig.subplots(nrows=len(id), ncols=int(self.delta.days+1),sharex='col', sharey=True)
				self.titulox = 'UT'
				self.tituloy = 'VTEC'
				self.titulo = ('%s-%s-%.2i(%s-%s)')%(self.listaobs.get(self.listaobs.curselection()[0]).replace(",","").replace("(","").replace(")","").split()[0],self.dataI.year,self.dataI.month,self.dataI.day,self.dataF.day)
				# self.fig.set_title(self.titulo)
				# self.fig.suptitle(self.titulo,fontsize=16,**self.fontt)
				self.fig.subplots_adjust(left=0.1,right=.95, wspace=0,hspace=0)
				# self.fig.suptitle(self.titulox,**self.fontt,y=.06)
				self.atua_titulos()

				if len(id) > 1: 
					self.C_dip_lat = []
					self.C_desvio = []
					self.C_sigla = []
					self.C_media = []
					self.C_tec = []
					for item_id in id:
						self.coleta_dados(item_id)
						self.C_sigla.append(self.sigla)
						self.C_dip_lat.append(self.dip_lat)
						self.C_media.append(self.media_calmo)					
						self.C_desvio.append(self.desvio_calmo)
						self.C_tec.append(self.te_p_reshape)

					max_G = np.nanmax(self.C_tec)
					if np.isnan(max_G):
						self.fig.subplots()
						plt.text(.5,.5, Utilitarios().idioma(94), size=16,ha="center", va="center" )
					else:
						for (dip_lat,axes,media,desvio,tec,sigla) in zip(self.C_dip_lat,self.axes,self.C_media,self.C_desvio,self.C_tec,self.C_sigla):
							self.sub_plot(axes,media,desvio,tec,sigla,dip_lat,len(id),max_G)
							
						for ax_ in self.axes[-1]:
							# plt.setp(ax_.get_xticklabels(), visible=True)
							ax_.xaxis.set_major_locator(FixedLocator([0,4,8,12,16,20]))
						else:
							ax_.xaxis.set_major_locator(FixedLocator([0,4,8,12,16,20,24]))
						for ax_,c in zip(self.axes[0],(range(len(self.axes[0])))):
							ax_.set_title(self.datas_axes_X[int(c)][0],fontdict=self.fontt)

				else:
					self.coleta_dados(id)
					max_G = np.nanmax(self.te_p_reshape)
					if np.isnan(max_G):
						self.fig.subplots()
						plt.text(0.5,0.5, Utilitarios().idioma(94), size=16,ha="center", va="center" )
					else:
						self.sub_plot(self.axes,self.media_calmo,self.desvio_calmo,self.te_p_reshape,self.sigla,self.dip_lat,len(id),max_G)
						for _axes,c in zip(self.axes,range(len(self.axes))):
							# plt.setp(_axes.get_xticklabels(), visible=True)	
							_axes.xaxis.set_major_locator(FixedLocator([0,4,8,12,16,20]))
							_axes.set_title(self.datas_axes_X[int(c)][0],fontdict=self.fontt)
						else:
							_axes.xaxis.set_major_locator(FixedLocator([0,4,8,12,16,20,24]))
				
				self.atua_limY()
				# self.fig.canvas.flush_events()
				self.fig.canvas.draw()
				self.save_png()
				self.salvar_matriz()
			else:
				# lin,cows
				self.listaobs.configure(selectmode="single")
				repos=self.listaobs.curselection()[0]
				self.listaobs.selection_clear(0,END)
				self.listaobs.selection_set(repos)
				# self.fig.clf()
				# self.axes = self.fig.subplots()
				self.plotar()
				# plt.tight_layout()
		except (AttributeError,IndexError):
			pass

	def sub_plot(self,_axes,_media,_desvio,_tec,_sigla,_dip_lat,len_id,max_G):
		cont=0
		for AX in _axes:
			y1 = (_media+_desvio)
			y2 = (_media-_desvio)
			# self. = np.array([x for x in np.arange(0,24,(1/60))])
			# AX.set_title(self.datas_axes_X[int(cont)][0],fontdict=self.fontt)
			AX.fill_between(self.temp,y1,y2,color = 'gray',label=self.Dado_config.idioma(125))
			AX.plot(self.temp,_media, color ='black',label=self.Dado_config.idioma(138),linewidth=3.0)
			AX.plot(self.temp,_tec[cont*1440:(cont+1)*1440], color='r',label='Tec',linewidth=2.5)

			AX.set_facecolor("lightgrey")
			AX.tick_params(axis='both',direction='inout', which='major',top=True,right=True, width=float(self.largtick.get()),size=float(self.alttick.get()),labelsize=float(self.sizetick.get()))
			AX.tick_params(axis='both',direction='inout', which='minor' ,top=True,right=True,width=float(self.largtickMinor.get()) ,size=float(self.alttickMinor.get()))
			AX.set_xlim(0,24)
			AX.set_ylim(0,max_G+(max_G *(.05*len_id)))
			AX.minorticks_on()
			AX.xaxis.grid(self.vargrid_X.get())
			AX.yaxis.grid(self.vargrid_Y.get())

			# plt.setp(AX.get_yticklabels(), visible=False)
			# plt.setp(AX.get_xticklabels(), visible=False)
			cont+=1
		else:
			# plt.setp(_axes[0].get_yticklabels(), visible=True)
			_axes[0].text(1,max_G-(max_G *(len_id)),("%s(dip latitide %s)")%(_sigla,_dip_lat), fontsize=12)
			_axes[0].set_ylabel(self.tituloy,**self.fonty)
			# AX.xaxis.set_major_locator(FixedLocator([0,4,8,12,16,20,24]))

	
	def on_configure(self,event):
		self.canvas_prop.configure(scrollregion=self.canvas_prop.bbox('all'))
	def atua_limY(self):
		if self.sub_plt.get() == True:
			if self.Tmin.get():
				for axs in self.axes.flatten():
					axs.set_ylim(ymin=int(self.Tmin.get()))
			else:
				for axs in self.axes.flatten():
					axs.set_ylim(ymin=0)
			if self.Tmax.get():
				for axs in self.axes.flatten():
					axs.set_ylim(ymax=int(self.Tmax.get()))
		else:
			if self.Tmin.get():
				plt.ylim(ymin=int(self.Tmin.get()))
			else:
				plt.ylim(ymin=0)
			if self.Tmax.get():
				plt.ylim(ymax=int(self.Tmax.get()))
	def major_format_x(self,x, pos):
		try:
			return (self.datas_axes_X[int(x/24)][self.DateFormat.get()])
		except IndexError:
			pass
	def setar_legends(self):
		if self.Legend.get() ==  False:
			plt.legend().remove()
		elif self.Legend.get() == True:
			plt.legend()
	def atua_legend(self):
		self.setar_legends()
		self.refreshCanvas()
	def atua_grid_X(self):
		try:
			if self.sub_plt.get() == True:
				for axs in self.axes.flatten():
					axs.xaxis.grid(self.vargrid_X.get())
			else:
				self.axes.xaxis.grid(self.vargrid_X.get())
			self.refreshCanvas()
		except AttributeError:
			pass
	def atua_grid_Y(self):
		try:
			if self.sub_plt.get() == True:
				for axs in self.axes.flatten():
					axs.yaxis.grid(self.vargrid_Y.get())
			else:
				self.axes.yaxis.grid(self.vargrid_Y.get())
			self.refreshCanvas()
		except AttributeError:
			pass

	def save_png(self):
		if self.varsave.get() == True:
			self.fig.savefig(("%s\%s.png")%(self.filedir,self.titulo),facecolor=self.fig.get_facecolor())
	def atuaAno(self,*event):
		self.ano = self.uti.refresh_list(self.ano,float(datetime.strptime(self.cal.get(), '%d/%m/%Y').year),self.listaobs)
	
	def selecionar(self):
		file = askdirectory(initialdir="c:/",title = self.Dado_config.idioma(40),parent=self)
		if file:
			self.filedir = file
	def refreshCanvas(self):
		self.atua_limY()
		# self.atua_titulos()
		self.atua_titulos()
		self.fig.canvas.draw()
		self.janelaprincipal.wait_window(self.janelaprincipal)
		# self.img.tight_layout()
	def sort_dip_(self,id):
		d_lat = []
		for idS in id:
			d_lat.append(float(self.listaobs.get(idS).replace(",","").replace("(","").replace(")","").split()[5]))
		id_re = [x for _,x in sorted(zip(d_lat,id),reverse=True)]
		return id_re
	def largTICK(self,vt,op,tick):
		if op == '+':
			vt.set(('%.1f')%(float(vt.get())+.1))
		elif op == '-':
			vt.set(('%.1f')%(float(vt.get())-.1))

		try: 	
			for axes_ in self.axes.flatten():
				axes_.tick_params(axis='both', which=tick, width=float(vt.get()))
		except AttributeError:
			self.axes.tick_params(axis='both', which=tick, width=float(vt.get()))
			pass

	def altTICK(self,vt,op,tick):
		if op == '+':
			vt.set(('%.1f')%(float(vt.get())+.1))
		elif op == '-':
			vt.set(('%.1f')%(float(vt.get())-.1))
		try: 	
			for axes_ in self.axes.flatten():
				axes_.tick_params(axis='both', which=tick, size=float(vt.get()))
		except AttributeError:
			self.axes.tick_params(axis='both', which=tick, size=float(vt.get()))
			pass

	def sizeTICK(self,vt,op):
		if op == '+':
			vt.set(int(vt.get())+1)
		elif op == '-':
			vt.set(int(vt.get())-1)
		try: 	
			for axes_ in self.axes.flatten():
				axes_.tick_params(axis='both', labelsize=int(vt.get()))#width=1.5 ,size=4)
		except AttributeError:
			self.axes.tick_params(axis='both', labelsize=int(vt.get()))#width=1.5 ,size=4)
			pass





if __name__ == "__main__":
	root = Tk()
	teste = Graficodesvio(root)
	# teste.grab_set()
	root.mainloop()