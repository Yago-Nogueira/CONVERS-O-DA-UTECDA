from qt_ui import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.ticker import LinearLocator , FuncFormatter,IndexLocator
from qt_ui.filedialog import askdirectory
import matplotlib.ticker as ticker
from qtfontchooser import askfont
import matplotlib.pyplot as plt
from util import Utilitarios
from qt_ui import ttk,messagebox
from qt_ui import *
import matplotlib,os
matplotlib.use("QtAgg")
import qt_ui as tk
import numpy as np
#from sys import platform
#from matplotlib import *
#from tkinter.font import Font
#from matplotlib.figure import Figure
#import matplotlib.axes,os
#import sys
class Graficocontorno:		
############################CONSTRUÇÃO-GRÁFICOS-CONTORNO###################################################################################
	def formulariocontorno(self,root):
		global vargrid; global varsave
		self.uti = Utilitarios()
		self.janelagraphcontorno = Tk()
		self.framepri = Frame(self.janelagraphcontorno, bd=3,bg="gray",highlightbackground ="white" ,relief=GROOVE )
		self.framepri.pack(expand=1,fill='both')
		#self.framedo = Frame(self.janelagraphcontorno, bd=3,bg="gray",highlightbackground ="red" ,relief=GROOVE, width=200, height=200 )
		#self.framedo.pack(expand=1,fill='both')
		nb = ttk.Notebook(self.framepri)
		self.page1 = Frame(self.framepri)
		self.page2 = Frame(self.framepri)
		nb.add(self.page1,text =self.Dado_config.idioma(7))
		nb.add(self.page2,text =self.Dado_config.idioma(17))
		nb.pack(expand=1,side='right',fill='both')
		vargrid = BooleanVar(self.janelagraphcontorno)
		varsave = BooleanVar(self.janelagraphcontorno)
		#self.barramenugraph = Menu(self.janelagraphcontorno)
		#self.barramenugraph.add_cascade(label='Personalizar Gráfico',command=self.formulariopersonal)		
		#self.janelagraphcontorno.config(menu=self.barramenugraph)
		self.framed = Frame(self.framepri, bd=3,bg="gray",highlightbackground ="red" ,relief=GROOVE)
		self.framed.pack(side ="right",fill=Y)		
		self.frame = Frame(self.framed, bd=3,bg="gray",highlightbackground ="red")
		self.frame.pack(side=TOP,fill=BOTH,expand=1)
		#self.frame.grid(sticky=W+E+N+S)
		self.select = Button(self.frame, width=20, text=self.Dado_config.idioma(18),command=self.selecionar)
		self.select.pack(side="top",fill=X)
		self.listafile = Listbox(self.frame,exportselection=0,relief='groove',width=25)
		self.listafile.bind("<<ListboxSelect>>",lambda g=1:self.GerarContorno(1))
		#self.listafile.bind("<FocusOut>",lambda e:self.listafile.focus_set())
		#menor = self.janelagraphcontorno.winfo_screenheight()
		#tamanholist =round(0.2490234375 * menor)
		self.listafile.pack(side="left",fill=BOTH)			
		self.sb = Scrollbar(self.frame)
		self.sb.pack(side=RIGHT,fill=Y)
		self.sb.configure(command=self.listafile.yview)
		self.listafile.configure(yscrollcommand=self.sb.set)
#arrumar
		self.frameTEXT = Frame(self.framed, bd=3,bg="gray",relief=GROOVE)
		self.frameTEXT.pack(side='bottom')
		#self.frameTEXT.grid(sticky=SW)
		self.framel1 = Frame(self.frameTEXT, bd=3,bg="gray",relief=GROOVE)
		self.framel1.grid(column=0,rows=1,sticky=E+W)
		self.framel2 = Frame(self.frameTEXT, bd=3,bg="gray",relief=GROOVE)
		self.framel2.grid(column=0,rows=2,sticky=E+W)
		self.framel3 = Frame(self.frameTEXT, bd=3,bg="gray",relief=GROOVE)
		self.framel3.grid(column=0,rows=3,sticky=E+W)
		self.framel4 = Frame(self.frameTEXT, bd=3,bg="gray",relief=GROOVE)
		self.framel4.grid(column=0,rows=4,sticky=E+W)
		self.framel5 = Frame(self.frameTEXT, bd=3,bg="gray",relief=GROOVE)
		self.framel5.grid(column=0,rows=5,sticky=E+W)
		self.framel6 = Frame(self.frameTEXT, bd=3,bg="gray",relief=GROOVE)
		self.framel6.grid(column=0,rows=6,sticky=E+W)
		self.framel7 = Frame(self.frameTEXT, bd=3,bg="gray",relief=GROOVE)
		self.framel7.grid(column=0,rows=7,sticky=E+W)
		self.framel8 = Frame(self.frameTEXT, bd=3,bg="gray",relief=GROOVE)
		self.framel8.grid(column=0,rows=8,sticky=E+W)
		self.lblInicioDias = Label(self.framel1,width=10, text=self.Dado_config.idioma(19))
		self.lblInicioDias.pack(side='left')
		vcmd = (self.janelagraphcontorno.register(self.uti.onValidatesigla),'%S', '%s','%d',2,4)
		self.diaIDias = Entry(self.framel1,width=14,exportselection=0,validate="key",validatecommand=vcmd)
		self.diaIDias.pack(side='right')
		self.lblFimDias = Label(self.framel2, text=self.Dado_config.idioma(20),width=10)
		self.lblFimDias.pack(side='left')		
		vcmd = (self.janelagraphcontorno.register(self.uti.onValidatesigla),'%S', '%s','%d',2,4)
		self.diaFDias = Entry(self.framel2,width=14,exportselection=0,validate="key",validatecommand=vcmd)
		self.diaFDias.pack(side='right')
		self.lblInicioHoras = Label(self.framel3, text=self.Dado_config.idioma(21),width=10)
		self.lblInicioHoras.pack(side='left')
		vcmd = (self.janelagraphcontorno.register(self.uti.onValidatesigla),'%S', '%s','%d',2,4)
		self.diaIHoras = Entry(self.framel3,width=14,exportselection=0,validate="key",validatecommand=vcmd)
		self.diaIHoras.pack(side='right')
		self.lblFimHoras = Label(self.framel4, text=self.Dado_config.idioma(22),width=10)
		self.lblFimHoras.pack(side='left')		
		vcmd = (self.janelagraphcontorno.register(self.uti.onValidatesigla),'%S', '%s','%d',2,4)
		self.diaFHoras = Entry(self.framel4,width=14,exportselection=0,validate="key",validatecommand=vcmd)	
		self.diaFHoras.pack(side='right')		
		self.lblvmax = Label(self.framel5, text = self.Dado_config.idioma(23),width=17)
		self.lblvmax.pack(side='left')				
		vcmd = (self.janelagraphcontorno.register(self.uti.onValidatesigla),'%S', '%s','%d',2,4)
		self.txtvmax = Entry(self.framel5,width=6,exportselection=0,validate="key",validatecommand=vcmd)
		self.txtvmax.pack(side='right')
		self.lblgrid = Label(self.framel6,text = self.Dado_config.idioma(24),width=17)
		self.lblgrid.pack(side='left')
		self.checkgrid = Checkbutton(self.framel6,variable=vargrid)
		self.checkgrid.pack(side='right')
		self.lblsave = Label(self.framel7,text =self.Dado_config.idioma(25),width=17)
		self.lblsave.pack(side='left')
		self.checksave = Checkbutton(self.framel7,variable=varsave,pady=0)
		self.checksave.pack(side='right')
		self.btnatualiza = Button(self.framel8, width=20, text=self.Dado_config.idioma(26), command=lambda g=2:self.GerarContorno(2))
############################propriedades gráfico ###################################################################################			
		self.framefront = Frame(self.page2,bd=3,width=200,bg="gray",relief=GROOVE)
		self.framefront.pack(side='left',fill=Y)
		self.frameback = Frame(self.page2,bd=3,bg='gray',relief=GROOVE)
		self.frameback.pack(side='left',fill=Y)
		#self.btnfontx = Button(self.framel2,text='Selecionar Fonte',command=lambda id='X':self.selecionarfonte(id))			
		#self.btnfontx.pack(side='right')
		self.framep=[]
		for rowp in range(10):
			self.framep.append(Frame(self.framefront,bd=3,bg='gray',relief=GROOVE))
			self.framep[rowp].pack(fill=X)
			#self.framep[rowp].grid(column=0,row=rowp+1,sticky=E+W)
		self.lblindica = Label(self.framep[0], text=self.Dado_config.idioma(27))
		self.lblindica.pack()
		self.lblntickx = Label(self.framep[1] ,text=self.Dado_config.idioma(28))
		self.lblntickx.pack(side="left",fill=X,expand=1)
		vcmd = (self.janelagraphcontorno.register(self.uti.onValidatesigla),'%S', '%s','%d',2,10)
		self.ntickx = Entry(self.framep[1],exportselection=0,validate="key",validatecommand=vcmd)
		self.ntickx.pack(fill=X)
		self.ntickx.bind("<FocusOut>",lambda habil:self.habil(self.ntickx,self.nlblx))
		self.lblnticky = Label(self.framep[2], text=self.Dado_config.idioma(29))
		self.lblnticky.pack(side="left",fill=X,expand=1)	
		vcmd = (self.janelagraphcontorno.register(self.uti.onValidatesigla),'%S', '%s','%d',2,10)
		self.nticky = Entry(self.framep[2],exportselection=0,validate="key",validatecommand=vcmd)
		self.nticky.pack(fill=X)
		self.nticky.bind("<FocusOut>",lambda habil=1:self.habil(self.nticky,self.nlbly))
		self.lblnlblx = Label(self.framep[3], text=self.Dado_config.idioma(30))
		self.lblnlblx.pack(side='left',fill=X)
		vcmd = (self.janelagraphcontorno.register(self.uti.onValidatesigla),'%S', '%s','%d',2,10)
		self.nlblx = Entry(self.framep[3],exportselection=0,validate="key",validatecommand=vcmd)
		self.nlblx.pack(side='right',fill=X)
		self.nlblx.bind("<FocusOut>",lambda habil:self.habil(self.nlblx,self.ntickx))
		self.lblnlbly = Label(self.framep[4], text=self.Dado_config.idioma(31))
		self.lblnlbly.pack(side='left',fill=X)		
		vcmd = (self.janelagraphcontorno.register(self.uti.onValidatesigla),'%S', '%s','%d',2,10)
		self.nlbly = Entry(self.framep[4],exportselection=0,validate="key",validatecommand=vcmd)
		self.nlbly.pack(side='right',fill=X)
		self.nlbly.bind("<FocusOut>",lambda habil=1:self.habil(self.nlbly,self.nticky))
		self.lbltix = Label(self.framep[5],text=self.Dado_config.idioma(32))
		self.lbltix.pack(side='left',fill=X,expand=1)
		self.txttix = Entry(self.framep[5],exportselection=0)
		self.txttix.pack(side='right',fill=X)
		self.lbltiy = Label(self.framep[6],text=self.Dado_config.idioma(33))
		self.lbltiy.pack(side='left',fill=X,expand=1)
		self.txttiy = Entry(self.framep[6],exportselection=0)
		self.txttiy.pack(side='right',fill=X)
		self.lblti = Label(self.framep[7], text=self.Dado_config.idioma(34))
		self.lblti.pack(side='left',fill=X,expand=1)		
		self.txtti = Entry(self.framep[7],exportselection=0)
		self.txtti.pack(side='right',fill=X)
		self.lbltib = Label(self.framep[8], text=self.Dado_config.idioma(35))
		self.lbltib.pack(fill=X)		
		self.txttib = Entry(self.framep[9],exportselection=0)
		self.txttib.pack(fill=X)
		

		self.framef=[]
		for rowf in range(7):
			self.framef.append(Frame(self.frameback,bd=3,bg='gray',relief=GROOVE))
			self.framef[rowf].grid(column=0,row=rowf+1,sticky=W+E)

		Label(self.framef[0],text=self.Dado_config.idioma(36)).pack()
		#Label(self.framef[1],text='Fonte geral').pack(side='left',ipady=2)
		#Button(self.framef[1],text='Selecionar Fonte',command=lambda id='G':self.selecionarfonte(id)).pack(side='right')
		Label(self.framef[2],text=self.Dado_config.idioma(32)).pack(side='left',fill=X,expand=1)
		Button(self.framef[2],text=self.Dado_config.idioma(37),command=lambda id='X':self.selecionarfonte(id),relief=RIDGE).pack(side='right',fill=X)
		Label(self.framef[3],text=self.Dado_config.idioma(33)).pack(side='left',fill=X,expand=1)
		Button(self.framef[3],text=self.Dado_config.idioma(37),command=lambda id='Y':self.selecionarfonte(id),relief=RIDGE).pack(side='right',fill=X)
		Label(self.framef[4],text=self.Dado_config.idioma(34)).pack(side='left',fill=X)
		Button(self.framef[4],text=self.Dado_config.idioma(37),command=lambda id='T':self.selecionarfonte(id),relief=RIDGE).pack(side='right',fill=X)
		Label(self.framef[5],text=self.Dado_config.idioma(35)).pack(fill=X)
		Button(self.framef[6],text=self.Dado_config.idioma(37),command=lambda id='B':self.selecionarfonte(id),relief=RIDGE).pack(fill=X)
		self.janelagraphcontorno.title(self.Dado_config.idioma(38))
		#self.janelagraphcontorno.protocol("WM_DELETE_WINDOW",lambda tk=root:self.controlejanela(tk))
		self.janelagraphcontorno.protocol("WM_DELETE_WINDOW",lambda tk=root:self.uti.troca(tk,self.janelagraphcontorno,plt))
		self.janelagraphcontorno.iconbitmap(r'icone.ico')
		self.janelagraphcontorno.geometry("1800x1600")
		self.janelagraphcontorno.state('zoomed')
		self.janelagraphcontorno.mainloop()
############################TROCA-LABEL(dia/hora)###################################################################################	
	def selecionarfonte(self,id):
		font = askfont(self.janelagraphcontorno,"Demo",self.Dado_config.idioma(37))
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
			#print(font)
			#font['family'] = font['family'].replace(' ', '\ ')
			#font_str = "%(family)s %(size)i %(weight)s %(slant)s" % font
			# if font['underline']:
			# 	font_str += ' underline'
			# if font['overstrike']:
			# 	font_str += ' overstrike'
			# #print(font_str)	
			if id == 'X':
				global fontx
				fontx = font
			elif id == 'Y':
				global fonty
				fonty = font
			elif id == 'T':
				global fontt
				fontt = font
			elif id == 'B':
				global fontb
				fontb = font 	
				#elif id== 'G':
			#	fonttotal = font

	def habil(self,objt1,objt2):
		if objt1.get().strip() != "":
			objt2.config(state="disabled",bg="gray")
		elif objt2['state']=="disabled":
			objt2.config(state="normal",bg="white")
############################FORMATADOR-EIXOS DO GRÁFICO###################################################################################
	def major_formatterhora(self,x, pos):
		#print('chorando...^.^.^.')
		return "%.f" % (x/60)
	def major_formatterdia(self,x, pos):
		return "%.f" % (x+1)
############################LOCALIZAR-DIRETORIO###########################################################################################
	def selecionar(self):
		global filename
		fi = askdirectory(initialdir = "C:/",title = self.Dado_config.idioma(39),parent=self)
		if fi:
			if fi != "":
				filename = fi 
			self.btnatualiza.pack_forget()
			self.listafile.delete(0,END)
			if filename != "":
				for i in os.listdir(filename):	
					if i.lower().endswith("_matriz.std") :
						self.listafile.insert(END,i)
				#self.listafile.sort()
#--------------------------LER-MATRIZ-GERAR GRÁFICO--------------------------------------------------------------
	def GerarContorno(self,crit):
		id = self.listafile.curselection()
		if not id:
			self.selecionar()
		else:
			global dados;global canvas;global toolbar;global filename;global vargrid; global varsave; global fontx;global fonty;global fontb
			filematriz = self.listafile.get(id)
			titulo = filematriz[:len(filematriz)-11]
			titulox = self.Dado_config.idioma(40)
			tituloy = self.Dado_config.idioma(41)
			titulob = "VTEC"
			self.btnatualiza.pack(side='bottom',fill=X)
			try:
				plt.close('all')
				canvas.get_tk_widget().pack_forget()
				canvas._tkcanvas.pack_forget()
				toolbar.pack_forget()
			except:
				pass
			try:
				fig, axes = plt.subplots()
				if self.diaIDias.get().strip(" ") !="":
					Idia = int(self.diaIDias.get().strip(" "))
				else:
					Idia = 1
				if self.diaFDias.get().strip(" ") !="":
					Fdia = int(self.diaFDias.get().strip(" "))
				else:
					Fdia = 31
				if self.diaIHoras.get().strip(" ").replace(",",".") !="":
					IHoras = float(self.diaIHoras.get().strip(" ").replace(",","."))
				else:
					IHoras = 0
				if self.diaFHoras.get().strip(" ").replace(",",".") !="":	
					FHoras = float(self.diaFHoras.get().strip(" ").replace(",","."))
				else:
					FHoras = 23.983
				if self.txtvmax.get().strip(" ") != "":
					vmax = float(self.txtvmax.get().strip(" ").replace(',','.'))
				else:
					vmax = 100.00
			except ValueError:
				messagebox.showerror(self.Dado_config.idioma(49),self.Dado_config.idioma(93),parent=self)
	#-------------------------------------melhorar-------------------------------------------------------------------------------
			try:
				if self.txtti.get().strip(' ') !="":
					titulo = self.txtti.get().strip(' ')
				if self.txttix.get().strip(' ') !="":
					titulox = self.txttix.get().strip(' ')
				if self.txttiy.get().strip(' ') !="":
					tituloy = self.txttiy.get().strip(' ')
				if self.txttib.get().strip(' ') !="":
					titulob = self.txttib.get().strip(' ')
				
				if self.nlbly.get() !="":
					Nlbly = int(self.nlbly.get().strip(' '))
					axes.yaxis.set_major_locator(ticker.LinearLocator(round(Nlbly)))
				elif self.nticky.get() !="":
					Nticky = float(self.nticky.get().strip(' ').replace(",","."))
					axes.yaxis.set_major_locator(ticker.IndexLocator(base=(Nticky*60), offset=IHoras))
				else:
					axes.yaxis.set_major_locator(ticker.LinearLocator())			
				if self.nlblx.get() !="":
					Nlblx = int(self.nlblx.get().strip(' '))
					axes.xaxis.set_major_locator(ticker.LinearLocator(round(Nlblx)))
				elif self.ntickx.get() !="":
					Ntickx = float(self.ntickx.get().strip(' ').replace(",","."))
					axes.xaxis.set_major_locator(ticker.IndexLocator(base=(Ntickx), offset=Idia-1))
				else:
					axes.xaxis.set_major_locator(ticker.LinearLocator())
			except AttributeError:
				pass
			# plt.rc('font', size=SMALL_SIZE)         
			# plt.rc('axes', titlesize=SMALL_SIZE)    
			# plt.rc('axes', labelsize=MEDIUM_SIZE)   
			# plt.rc('xtick', labelsize=SMALL_SIZE)   
			# plt.rc('ytick', labelsize=SMALL_SIZE)   
			# plt.rc('legend', fontsize=SMALL_SIZE)   
			# plt.rc('figure', titlesize=BIGGER_SIZE) 
	#---------------------------------------------------------------------------------------------------------------------------
			if crit == 1:
				arq=open(filename+"//"+filematriz,'r',encoding="UTF-8")
				dia=[];ut=[];tec=[];dados=[];l1=''
				i=0
				for line in arq:
					if i>1:
						line=line.replace(',','.')
						l=line[:int(len(line)-28)].split()
						for j in range(len(l)):
							if l[j]=='-----' or l[j]=='------': l[j]=-999.0		
						for j in range(len(l)-1,-1,-1):
							if j%2==0:# or l[j]=='-----'or l[j]=='----':
								del l[j]
						# for j in range(len(l)):
							# if l[j]==-999.0 and j>1:
								# l[j]=l[j-1]
							# if l[j]==-999.0 and j<len(l)-1:
								# l[j]=l[j+1]
						dados.append(l)
					else:
						i=i+1
				arq.close()
				dados=np.array(dados)
			passo = vmax/15
			level=np.arange((passo*-1),(vmax+(passo*2)),passo)
			#level=np.arange(0.0,(vmax),passo)
			#print(level)
			#cor = ['r','r','#FF4001','#FF8001','#FFBE00','#FFFF01','#AAFF01','#55FF00','#00FF01','#00FF41','#00FE81','#01FFBF','#01FFFF','#00AAFF','#0055FE','gray','white']
			if vargrid.get() == True:
				plt.grid(True)
			else:
				plt.grid(False)
			plt.title(titulo,**fontt)
			#print(plt.title())
			plt.minorticks_on()
			#ax.set_ylabel("Median Population", fontname="Arial", fontsize=12)
			plt.ylabel(tituloy,rotation=90,**fonty)#ideia de mudar a rotação------------------------AQUIIOSS
			plt.ylim(IHoras*60,FHoras*60)
			plt.xlim(Idia-1,Fdia-1)
			axes.yaxis.set_major_formatter(ticker.FuncFormatter(self.major_formatterhora))
			axes.xaxis.set_major_formatter(ticker.FuncFormatter(self.major_formatterdia))
			plt.xlabel(titulox,**fontx)
			p=plt.contourf(dados,levels=level,cmap='jet',vmin = 0,vmax=vmax)
			#plt.show()
			p.cmap.set_under(color='white')
			p.cmap.set_over(color='darkred')
			if vmax % 10 ==0:
				cbar = plt.colorbar(ticks=[i for i in range(int(vmax+10)) if i % 10==0])#0 a 100
			else:
				contcbar = 0
				tickscolor =[]
				while (contcbar < (vmax+passo)):
					tickscolor.append(contcbar)
					contcbar+=passo
				cbar = plt.colorbar(ticks=tickscolor)
			cbar.ax.set_title(titulob,**fontb)
			canvas = FigureCanvasTkAgg(fig,self.page1)
			canvas.show()
			canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
			toolbar = NavigationToolbar2Tk(canvas, self.page1)
			toolbar.update()
			canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
			canvas._tkcanvas.bind("<FocusIn>",lambda e:self.listafile.focus_set())
			if varsave.get() == True:
				#dest = os.path.dirname(os.path.realpath(__file__))+r"/GráficosPNG/"
				dest = filename 
				if(os.path.exists(dest) == False):
					os.makedirs(dest)
				plt.savefig(dest +"/"+ titulo)
			#except:
			#	messagebox.showerror('Erro',"Erro")
fontx ={'family' : 'Arial',
		'weight' : 'normal',
		'size'   : 12}
fonty = fontx
fontt = fontx
fontb = fontx
#fonttotal = fontx

filename = []
dados = []	
