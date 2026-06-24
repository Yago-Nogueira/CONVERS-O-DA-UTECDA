import math,os,shutil,time,sys,traceback
import matplotlib
matplotlib.use('QtAgg')
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox, QFileDialog
from datetime import date, datetime, timedelta
# PyQt6 imports handled explicitly
from qt_ui import Toplevel, messagebox, ttk
from qt_ui.filedialog import askdirectory
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from qt_ui import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.offsetbox import AnnotationBbox, TextArea
from matplotlib.patches import Polygon
from mpl_toolkits.basemap import Basemap
from scipy import interpolate
import qtSimpleDialog
from Balloon_info import ToolTip
from cadastrarMAPA import askLOC
from cadastrarOBS import CadObs
from comp_DESVIO import COMP_DESVIO
from comp_INDV import COMP_INDV
from comp_ROT import COMP_ROT
from deprecated.comp_SETOR import COMP_SETOR
from comp_EIA import COMP_EIA
from deprecated.comp_MAPA_OLD import COMP_MAPA
from EntryBox import askEntry, askEntrytick
from gerardoric import Geradordeinclinacao
from licença import getli
from ordena import Ordena
from qt_calendar import DateEntry
from tkcalendar_Days import Calendar
from util import DadoIdioma, Utilitarios, VerticalScrolledFrame, thread_with_trace



class Principal():
	def __init__(self,janelaprincipal=None):
		plt.rc('axes', linewidth=2)
		plt.rc('font', weight='bold')


		self.titulo_graph_indv = self.titulo_axe_y_indv = self.titulo_axe_x_indv = self.tick_bar_indv = self.passo_tickX_indv = self.n_rotuloX_indv = self.minX_indv = self.maxX_indv = self.passo_tickY_indv = self.n_rotuloY_indv = self.minY_indv = self.maxY_indv = None
		self.titulo_graph_setor = self.y_min_est_setor = self.y_max_est_setor = self.titulo_axe_y_setor = self.titulo_axe_x_setor = self.tick_bar_setor = self.passo_tickX_setor = self.n_rotuloX_setor = self.minX_setor = self.maxX_setor = self.passo_tickY_setor = self.n_rotuloY_setor = self.minY_setor = self.maxY_setor = None
		self.titulo_graph_EIA = self.y_min_est_EIA = self.y_max_est_EIA = self.titulo_axe_y_EIA = self.titulo_axe_x_EIA = self.tick_bar_EIA = self.passo_tickX_EIA = self.n_rotuloX_EIA = self.minX_EIA = self.maxX_EIA = self.passo_tickY_EIA = self.n_rotuloY_EIA = self.minY_EIA = self.maxY_EIA = None
		self.titulo_graph_desv = self.titulo_axe_y_desv = self.titulo_axe_x_desv = self.passo_tickX_desv = self.n_rotuloX_desv = self.passo_tickY_desv = self.n_rotuloY_desv = self.minX_desv = self.maxX_desv = self.passo_tickY_desv = self.n_rotuloY_desv = self.minY_desv = self.maxY_desv = self.legendas_desvio = None
		self.titulo_axe_y_rot = self.titulo_axe_x_rot = self.passo_tickX_rot = self.n_rotuloX_rot = self.minX_rot = self.maxX_rot = self.passo_tickY_rot = self.n_rotuloY_rot = self.minY_rot = self.maxY_rot = None

		self.titulo_bar_model_map = self.titulo_bar_indv = self.titulo_bar_setor = self.titulo_bar_EIA = "VTEC"

		
		self.rfont_titulo_bar_model_map = self.rfont_titulo_graph_indv = self.rfont_titulo_axe_y_indv = self.rfont_titulo_axe_x_indv = self.rfont_titulo_bar_indv = self.rfont_titulo_graph_setor = self.rfont_titulo_axe_y_setor = self.rfont_titulo_axe_x_setor = self.rfont_titulo_bar_setor = self.rfont_titulo_graph_desv = self.rfont_titulo_axe_y_desv = self.rfont_titulo_axe_x_desv = self.rfont_titulo_axe_y_rot = self.rfont_titulo_axe_x_rot = self.rfont_titulo_graph_rot = self.rfont_titulo_graph_EIA = self.rfont_titulo_axe_y_EIA = self.rfont_titulo_axe_x_EIA = self.rfont_titulo_bar_EIA = {'family': '@MS Gothic', 'size': 28, 'weight': 'bold'}

		self.min_ori_Y = self.max_ori_Y = self.min_ori_X = self.max_ori_X = None
		self.Dado_config = DadoIdioma()
		self.current_plot = self.linha_eq_mag = self.list_id = None
		self.Data_Entry = StringVar(janelaprincipal)

		self.Data_Entry.set("11/09/2017")


		self.Data_linha_eqm = date.today().year
		self.inf = None;self.vm = 50;self.Menu = None
		self.tela_graf_old_state = 'zoomed'
		self.janelaprincipal = janelaprincipal
		self.uti = Utilitarios()
		self.uti.Teste()
		self.tela_graf = Toplevel(janelaprincipal)
		self.tela_graf.iconbitmap(self.uti.resource_path('icone.ico'))
		self.tela_graf.lift()
		self.tela_graf.withdraw()
		self.popup_graf = Menu(self.tela_graf, tearoff=0)
		self.frameprincipal1=VerticalScrolledFrame(self.janelaprincipal,relief='ridge',bd=2,bg='gray')
		Label(self.frameprincipal1.interior, text = self.Dado_config.idioma(171) ).pack(side='bottom',fill='y')
		self.principal=Menu(janelaprincipal)
		ferramentas=Menu(self.principal,tearoff=0)
		ferramentas.add_command(label=self.Dado_config.idioma(4),command=lambda id=1:self.xama(id))
		ferramentas.add_command(label=self.Dado_config.idioma(5),command=lambda id=3:self.xama(id))
		ferramentas.add_command(label=self.Dado_config.idioma(6),command=lambda id=4:self.xama(id))
		ferramentas.add_command(label=self.Dado_config.idioma(149),command=lambda id=5:self.xama(id))
		programas=Menu(self.principal,tearoff=0)
		programas.add_cascade(label=self.Dado_config.idioma(8),menu=ferramentas,state="disabled")
		idioma=Menu(self.principal,tearoff=0)
		idioma.add_command(label=self.Dado_config.idioma(9),command=lambda id=0:self.setarIDI(id))
		idioma.add_command(label=self.Dado_config.idioma(10),command=lambda id=1:self.setarIDI(id))
		config=Menu(self.principal,tearoff=0)
		config.add_cascade(label=self.Dado_config.idioma(11),menu=idioma)
		root.configure(menu=self.principal)
		self.principal.add_cascade(label=self.Dado_config.idioma(12),menu=programas)
		self.principal.add_cascade(label=self.Dado_config.idioma(13),menu=config)
		self.accept = True
		newpath = os.path.expanduser('~/Documents/UTECDA')
		try:
			self.uti.teste_licença()
			programas.entryconfig(self.Dado_config.idioma(8),state="normal")
			self.frameprincipal1.pack(  # CONVERT_PACKside='left',fill=BOTH)
		except (IOError,IndexError):
			self.accept = False
			
			
			self.principal.add_command(label=self.Dado_config.idioma(15),command=lambda j=janelaprincipal:getli(janelaprincipal))
		if not os.path.exists(("%s/OBS.dat")%(newpath)):
			self.uti.setOBS(newpath)
		if not os.path.exists(("%s/LOCS.dat")%(newpath)):
			self.uti.setLOCS(newpath)
		try:
			with open((('%s/LOCS.dat')%(newpath)) , 'r',encoding="UTF-8") as locs:
				linhas_loc = locs.readlines()
				self.lista_loc = [loc.replace("\n","").split("\t") for loc in linhas_loc]
		except (IOError,IndexError,ValueError,PermissionError):
			messagebox.showerror(self.Dado_config.idioma(49),self.Dado_config.idioma(55),parent=self.janelaprincipal)
			quit()
		self.frame_prop_inbut = Frame(self.tela_graf,bg='gray')
		self.frame_prop_inbut.pack(  # CONVERT_PACKside='top',fill='both')
		self.varsave = BooleanVar(self.janelaprincipal)
		self.varmatriz = BooleanVar(self.janelaprincipal)
		self.popup_graf.add_command(label=self.Dado_config.idioma(139), command=self.atua_grid_Y)
		self.popup_graf.add_command(label=self.Dado_config.idioma(141), command=self.atua_grid_X)
		self.popup_graf.add_checkbutton(label=self.Dado_config.idioma(25),variable=self.varsave,command=self.save_png)
		self.popup_graf.add_checkbutton(label=self.Dado_config.idioma(91),variable=self.varmatriz,command=self.save_matriz)
		self.popup_graf.add_separator()
		self.popup_graf.add_command(label=self.Dado_config.idioma(26), command=self.refreshCanvas)
		self.tela_graf.bind("<Configure>", self.state_refresh )  # CONVERT_BIND
		self.tela_graf.bind("<Button-3>", self.do_popup)  # CONVERT_BIND
		self.tela_graf.protocol("WM_DELETE_WINDOW",self.quit_graf)
		

		self.img, self.img_axes = plt.subplots()
		self.canvas_img = FigureCanvasTkAgg(self.img,self.tela_graf)
		self.toolbar = NavigationToolbar2Tk(self.canvas_img, self.tela_graf)
		self.canvas_img.get_tk_widget().pack(side="bottom", fill="both", expand=True)
		self.canvas_img._tkcanvas.pack(  # CONVERT_PACKside="top", fill="both", expand=True)

		self.filedir = None

		self.frame_loc = Frame(self.frameprincipal1.interior)
		self.frame_loc.pack(  # CONVERT_PACKside='top',fill='both')
		Label(self.frame_loc,width = 25, text = self.Dado_config.idioma(157),relief='ridge').pack(side='top',fill=X)
		self.cbg_loc_value = ""
		mp = self.Dado_config.getMapa()
		if mp == "None":
			mp = self.lista_loc[0][0]
		self.cbg_loc_value.set(mp)
		self.n_lista_loc = [ll[0] for ll in self.lista_loc]
		self.cbg_loc = ttk.Combobox(self.frame_loc,state='readonly',exportselection=False,textvariable=self.cbg_loc_value,values=self.n_lista_loc)
		self.cbg_loc.bind("<<ComboboxSelected>>",self.Set_map)  # CONVERT_BIND
		self.cbg_loc.pack(  # CONVERT_PACKside='top',fill='x')
		self.dirstd = Button(self.frameprincipal1.interior, text=self.Dado_config.idioma(18),command=self.selecionar,relief='ridge')
		self.dirstd.pack(  # CONVERT_PACKside='top',fill='x')
		self.dir_string = StringVar(self.janelaprincipal)
		self.lbl_dir = Label(self.frameprincipal1.interior,width = 25 ,anchor=E,textvariable = self.dir_string ,relief='ridge')
		self.lbl_dir.pack(  # CONVERT_PACKfill='x')
		self.frame_filter = Frame(self.frameprincipal1.interior,relief='ridge',bd=2)
		self.frame_filter.pack(  # CONVERT_PACKside='top',fill='both',expand=True)
		self.check_filter_v = BooleanVar(self.janelaprincipal)
		self.check_filter_v.set(True)
		Label(self.frame_filter,text=self.Dado_config.idioma(166)).pack(side='left',fill='both',expand=True)
		self.check_filter = Checkbutton(self.frame_filter,variable=self.check_filter_v,relief='ridge',bd=2,width=5,command=self.check_fill)
		self.check_filter.pack(  # CONVERT_PACK)
		self.frame_list = Frame(self.frameprincipal1.interior)
		self.frame_list.pack(  # CONVERT_PACKside='top',fill='both')
		self.listaobs = Listbox(self.frame_list,exportselection=False,bd=2,relief='ridge',width=25,highlightthickness=0,selectmode="single",justify=RIGHT)
		
		self.listaobs.pack(  # CONVERT_PACKside=LEFT,fill='both',expand=True)

		
		
		self.listaobs.bind("<<ListboxSelect>>",self.sel_map)  # CONVERT_BIND
		self.sb = Scrollbar(self.frame_list)
		self.sb.pack(  # CONVERT_PACKside='right',fill=Y)
		self.sb.configure(command=self.listaobs.yview)
		self.listaobs.configure(yscrollcommand=self.sb.set)
		self.frame_select_obs = Frame(self.frameprincipal1.interior)
		self.frame_select_obs.pack(  # CONVERT_PACKfill=X)
		self.cont_est_select = StringVar(self.janelaprincipal)
		self.cont_est_select.set('0')
		Label(self.frame_select_obs,textvariable = self.cont_est_select,relief='ridge').pack(side=LEFT,fill=BOTH,expand=True)
		Button(self.frame_select_obs,text=self.Dado_config.idioma(113),relief='ridge',command=self.clear_list_and_plot).pack(side='right',fill=BOTH,expand=True)
		self.cbg_value = ""
		self.cbg = ttk.Combobox(self.frameprincipal1.interior,state='disabled',exportselection=False,textvariable=self.cbg_value,values=['Individual (STD)','Setor (STD)','EIA (STD)','Desvio (STD)','Mapa (CMN)','ROT (CMN)'])
		self.cbg.current(0)
		self.cbg.bind("<<ComboboxSelected>>",self.Set_menu_rap)  # CONVERT_BIND
		self.cbg.pack(  # CONVERT_PACKside='top',fill=X)
		self.frameprincipal2 = Frame(janelaprincipal)
		self.frameprincipal2.pack(  # CONVERT_PACKfill=BOTH,side='right',expand=True)

		

		self.Frame_prop_rap_INDV = Frame(self.frameprincipal1.interior,bd=3,bg='gray',relief=GROOVE)
		Label(self.Frame_prop_rap_INDV,text=self.Dado_config.idioma(53)).pack(fill=X)
		self.cal_INDV = DateEntry(self.Frame_prop_rap_INDV, textvariable = self.Data_Entry,background='darkblue',foreground='white', borderwidth=2)
		self.cal_INDV.bind('<<DateEntrySelected>>', self.atualizar_dip)  # CONVERT_BIND
		self.cal_INDV.pack(  # CONVERT_PACKfill='x')
		Label(self.Frame_prop_rap_INDV,text=self.Dado_config.idioma(54)).pack(fill='x')
		self.Data_Entry_INDV2 = StringVar(janelaprincipal)
		self.cal2_INDV = DateEntry(self.Frame_prop_rap_INDV,textvariable=self.Data_Entry_INDV2,background='darkblue',foreground='white', borderwidth=2)
		self.cal2_INDV.pack(  # CONVERT_PACKfill='x')
		Label(self.Frame_prop_rap_INDV,text=self.Dado_config.idioma(130),relief=GROOVE).pack(fill=X)
		self.DateFormat_INDV = IntVar(self.janelaprincipal)
		self.DateFormat_INDV.set(1)
		Radiobutton(self.Frame_prop_rap_INDV,variable=self.DateFormat_INDV,relief=GROOVE,command=self.refreshCanvas ,value=1,text=self.Dado_config.idioma(40)).pack(side='left',fill=X,expand=1)
		Radiobutton(self.Frame_prop_rap_INDV,variable=self.DateFormat_INDV,relief=GROOVE,command=self.refreshCanvas ,value=0,text=self.Dado_config.idioma(135)).pack(side='right',fill=X,expand=1)
		self.vargrid_X = BooleanVar(self.janelaprincipal)
		self.vargrid_Y = BooleanVar(self.janelaprincipal)


		self.Frame_prop_rap_SETOR = Frame(self.frameprincipal1.interior,bd=3,bg='gray',relief=GROOVE)
		self.Frame_prop_rap_SETOR_Entry = Frame(self.Frame_prop_rap_SETOR,bg='gray')
		self.Frame_prop_rap_SETOR_Entry.pack(  # CONVERT_PACKfill=X)
		Label(self.Frame_prop_rap_SETOR_Entry,text=self.Dado_config.idioma(107)).pack(fill=X)
		self.cal_SETOR = DateEntry(self.Frame_prop_rap_SETOR_Entry,textvariable = self.Data_Entry,background='darkblue',foreground='white', borderwidth=2)
		self.cal_SETOR.bind('<<DateEntrySelected>>',self.atualizar_dip)  # CONVERT_BIND
		self.cal_SETOR.pack(  # CONVERT_PACKfill=X)
		self.Frame_prop_rap_SETOR_Check = Frame(self.Frame_prop_rap_SETOR,bg='gray')
		self.Frame_prop_rap_SETOR_Check.pack(  # CONVERT_PACKfill=X)
		self.cal_SETOR_EIA_varest = BooleanVar(self.janelaprincipal)
		self.cal_SETOR_lblest = Label(self.Frame_prop_rap_SETOR_Check,text=self.Dado_config.idioma(109),relief=GROOVE)
		self.cal_SETOR_lblest.pack(  # CONVERT_PACKside='left',fill=BOTH,expand=True)
		self.cal_SETOR_checkest = Checkbutton(self.Frame_prop_rap_SETOR_Check,variable=self.cal_SETOR_EIA_varest,width=5,command=self.check_est_setor_EIA)
		self.cal_SETOR_checkest.pack(  # CONVERT_PACKside='right')
		self.Frame_prop_rap_SETOR_eixoY = Frame(self.Frame_prop_rap_SETOR,bg='gray',relief=GROOVE)
		self.Frame_prop_rap_SETOR_eixoY.pack(  # CONVERT_PACKfill=X)
		self.varaxixY = IntVar(self.janelaprincipal)
		self.varaxixY.set(1)
		Label(self.Frame_prop_rap_SETOR_eixoY,text=self.Dado_config.idioma(120),relief=GROOVE).pack(fill=X)
		Radiobutton(self.Frame_prop_rap_SETOR_eixoY,variable=self.varaxixY,value=0,text='Latitude',relief=GROOVE,command=self.radio_dip_setor_EIA).pack(side='right',fill=X,expand=1)
		Radiobutton(self.Frame_prop_rap_SETOR_eixoY,variable=self.varaxixY,value=1,text='Dip.Lat',relief=GROOVE,command=self.radio_dip_setor_EIA).pack(side='left',fill=X,expand=1)
		self.Frame_prop_rap_SETOR_btn = Frame(self.Frame_prop_rap_SETOR,bg='gray',relief=GROOVE)
		self.Frame_prop_rap_SETOR_btn.pack(  # CONVERT_PACKfill=X)
		Button(self.Frame_prop_rap_SETOR_btn,text=self.Dado_config.idioma(108),relief='ridge',command = self.plot).pack(fill=X)


		self.Frame_prop_rap_DESVIO = Frame(self.frameprincipal1.interior,bd=3,bg='gray',relief=GROOVE)
		self.Frame_prop_rap_DESVIO_Sel_Dias_Calmos = Frame(self.Frame_prop_rap_DESVIO,bd=3,relief=GROOVE)
		self.Frame_prop_rap_DESVIO_Sel_Dias_Calmos.pack(  # CONVERT_PACKfill='both')
		Label(self.Frame_prop_rap_DESVIO_Sel_Dias_Calmos,text=self.Dado_config.idioma(123)).pack(fill=X,side="top")
		self.Cal_Calm_days = Calendar(self.Frame_prop_rap_DESVIO_Sel_Dias_Calmos, width=10, font="Arial 10", selectmode='day',cursor="hand2",Locator=self.Dado_config.idioma(0),year = date.today().year,month=date.today().month)
		self.Cal_Calm_days.pack(  # CONVERT_PACKfill="both", expand=True)
		Label(self.Frame_prop_rap_DESVIO_Sel_Dias_Calmos,text=self.Dado_config.idioma(124),relief='ridge').pack(fill=X)
		Label(self.Frame_prop_rap_DESVIO_Sel_Dias_Calmos,text=self.Dado_config.idioma(53)).pack(fill=X)
		self.cal_in_DESVIO = DateEntry(self.Frame_prop_rap_DESVIO_Sel_Dias_Calmos,textvariable = self.Data_Entry, background='darkblue',foreground='white', borderwidth=1)
		self.cal_in_DESVIO.bind('<<DateEntrySelected>>',self.atualizar_dip)  # CONVERT_BIND
		self.cal_in_DESVIO.pack(  # CONVERT_PACKfill='both',expand = True)
		Label(self.Frame_prop_rap_DESVIO_Sel_Dias_Calmos,text=self.Dado_config.idioma(54)).pack(fill=X)
		self.Data_Entry_DESVIO2 = StringVar(janelaprincipal)
		self.cal_fi_DESVIO = DateEntry(self.Frame_prop_rap_DESVIO_Sel_Dias_Calmos,textvariable= self.Data_Entry_DESVIO2, background='darkblue',foreground='white', borderwidth=1)
		self.cal_fi_DESVIO.pack(  # CONVERT_PACKfill='both',expand = True)
		self.Frame_prop_rap_DESVIO_prop = Frame(self.Frame_prop_rap_DESVIO,bd=3,bg='gray',relief=GROOVE)
		self.Frame_prop_rap_DESVIO_prop.pack(  # CONVERT_PACKfill=X)
		self.frame_prop_it = []
		for rowit in range(4):
			self.frame_prop_it.append(Frame(self.Frame_prop_rap_DESVIO_prop,bd=3,relief=GROOVE))
			self.frame_prop_it[rowit].pack(fill=X)
		Label(self.frame_prop_it[0],text=self.Dado_config.idioma(130),relief=GROOVE).pack()
		self.DateFormat_DESVIO = IntVar(self.janelaprincipal)
		self.DateFormat_DESVIO.set(0)
		Radiobutton(self.frame_prop_it[1],variable=self.DateFormat_DESVIO,command=self.refresh_format_DESVIO,relief=GROOVE,value=1,text=self.Dado_config.idioma(40)).pack(side='left',fill=X,expand=1)
		'''
			variable=self.DateFormat,command=self.refreshCanvas ,
		'''
		Radiobutton(self.frame_prop_it[1],variable=self.DateFormat_DESVIO,command=self.refresh_format_DESVIO,relief=GROOVE,value=0,text=self.Dado_config.idioma(131)).pack(side='right',fill=X,expand=1)
		'''
			variable=self.DateFormat,command=self.refreshCanvas ,
		'''
		self.Legend = BooleanVar(self.janelaprincipal)
		Label(self.frame_prop_it[2], text=self.Dado_config.idioma(134),relief=GROOVE).pack(side="left")
		Checkbutton(self.frame_prop_it[2],variable=self.Legend,command=self.setar_legends).pack(fill=X,expand=1,side='left')
		Button(self.frame_prop_it[3],text=self.Dado_config.idioma(108),relief='ridge',command = self.plot).pack(fill=X)


		self.Frame_prop_rap_MAPA = Frame(self.frameprincipal1.interior,bd=3,bg='gray',relief=GROOVE)
		self.Frame_prop_rap_MAPA_Entry = Frame(self.Frame_prop_rap_MAPA,bg='gray')
		self.Frame_prop_rap_MAPA_Entry.pack(  # CONVERT_PACKfill=X)

		Label(self.Frame_prop_rap_MAPA_Entry,text=self.Dado_config.idioma(107)).pack(fill=X)
		self.cal_MAPA = DateEntry(self.Frame_prop_rap_MAPA_Entry,textvariable = self.Data_Entry,background='darkblue',foreground='white', borderwidth=2)
		self.cal_MAPA.bind('<<DateEntrySelected>>',self.atualizar_dip)  # CONVERT_BIND
		self.cal_MAPA.pack(  # CONVERT_PACKfill=X)


		self.Frame_prop_rap_MAPA_H_INICIO = Frame(self.Frame_prop_rap_MAPA,bg='gray')
		self.Frame_prop_rap_MAPA_H_INICIO.pack(  # CONVERT_PACKfill=X)
		Label(self.Frame_prop_rap_MAPA_H_INICIO,text=self.Dado_config.idioma(172),relief=GROOVE).pack(side='left',fill=BOTH,expand=True)
		vcmd = (self.janelaprincipal.register(self.uti.onValidatesigla),'%S', '%s','%d',2,4)
		self.MAPA_Time_INICIO = Entry(self.Frame_prop_rap_MAPA_H_INICIO,width=10,validate="key",validatecommand=vcmd,bd=2)
		self.MAPA_Time_INICIO.insert(END,'0')
		self.MAPA_Time_INICIO.pack(  # CONVERT_PACKside='right',fill='both')


		self.Frame_prop_rap_MAPA_H_FIM = Frame(self.Frame_prop_rap_MAPA,bg='gray')
		self.Frame_prop_rap_MAPA_H_FIM.pack(  # CONVERT_PACKfill=X)
		Label(self.Frame_prop_rap_MAPA_H_FIM,text=self.Dado_config.idioma(173),relief=GROOVE).pack(side='left',fill=BOTH,expand=True)
		vcmd = (self.janelaprincipal.register(self.uti.onValidatesigla),'%S', '%s','%d',2,4)
		self.MAPA_Time_FIM = Entry(self.Frame_prop_rap_MAPA_H_FIM,width=10,validate="key",validatecommand=vcmd,bd=2)
		self.MAPA_Time_FIM.insert(END,'24')
		self.MAPA_Time_FIM.pack(  # CONVERT_PACKside='right',fill='both')


		self.Frame_prop_rap_MAPA_D_TIME = Frame(self.Frame_prop_rap_MAPA,bg='gray')
		self.Frame_prop_rap_MAPA_D_TIME.pack(  # CONVERT_PACKfill=X)
		Label(self.Frame_prop_rap_MAPA_D_TIME,text=self.Dado_config.idioma(174),relief=GROOVE).pack(side='left',fill=BOTH,expand=True)
		vcmd = (self.janelaprincipal.register(self.uti.onValidatesigla),'%S', '%s','%d',2,4)
		self.MAPA_Delta_Time = Entry(self.Frame_prop_rap_MAPA_D_TIME,width=10,validate="key",validatecommand=vcmd,bd=2)
		self.MAPA_Delta_Time.insert(END,'1')
		self.MAPA_Delta_Time.pack(  # CONVERT_PACKside='right',fill='both')



		Button(self.Frame_prop_rap_MAPA,text=self.Dado_config.idioma(175),relief='ridge',command = self.modelo_mapa).pack(fill=X)

		Button(self.Frame_prop_rap_MAPA,text=self.Dado_config.idioma(108),relief='ridge',command = self.plot).pack(fill=X)





		self.Frame_prop_rap_ROT = Frame(self.frameprincipal1.interior,bd=3,bg='gray',relief=GROOVE)
		self.Frame_prop_rap_ROT_Entry = Frame(self.Frame_prop_rap_ROT,bg='gray')
		self.Frame_prop_rap_ROT_Entry.pack(  # CONVERT_PACKfill=X)
		Label(self.Frame_prop_rap_ROT_Entry,text=self.Dado_config.idioma(107)).pack(fill=X)
		self.cal_ROT = DateEntry(self.Frame_prop_rap_ROT_Entry,textvariable = self.Data_Entry,background='darkblue',foreground='white', borderwidth=2)
		self.cal_ROT.bind('<<DateEntrySelected>>',self.atualizar_dip)  # CONVERT_BIND
		self.cal_ROT.pack(  # CONVERT_PACKfill=X)
		self.Frame_prop_rap_ROT_Check = Frame(self.Frame_prop_rap_ROT,bg='gray')
		self.Frame_prop_rap_ROT_Check.pack(  # CONVERT_PACKfill=X)
		self.ROT_varest = BooleanVar(self.janelaprincipal)
		Label(self.Frame_prop_rap_ROT_Check,text=self.Dado_config.idioma(167),relief=GROOVE).pack(side='left',fill=BOTH,expand=True)
		Checkbutton(self.Frame_prop_rap_ROT_Check,relief=GROOVE,command = self.set_cores_ROT,variable=self.ROT_varest,width=5).pack(side='right')
		self.Frame_prop_rap_ROT_Check_Legend = Frame(self.Frame_prop_rap_ROT,bg='gray')
		self.Frame_prop_rap_ROT_Check_Legend.pack(  # CONVERT_PACKfill=X)
		Label(self.Frame_prop_rap_ROT_Check_Legend,text=self.Dado_config.idioma(134),relief=GROOVE).pack(side='left',fill=BOTH,expand=True)
		Checkbutton(self.Frame_prop_rap_ROT_Check_Legend,relief=GROOVE,command=self.setar_legends,variable=self.Legend,width=5).pack(side='right')
		self.Frame_prop_rap_ROT_D_TIME = Frame(self.Frame_prop_rap_ROT,bg='gray')
		self.Frame_prop_rap_ROT_D_TIME.pack(  # CONVERT_PACKfill=X)
		Label(self.Frame_prop_rap_ROT_D_TIME,text='ΔT (Min)',relief=GROOVE).pack(side='left',fill=BOTH,expand=True)
		vcmd = (self.janelaprincipal.register(self.uti.onValidatesigla),'%S', '%s','%d',2,4)
		self.ROT_Delta_Time = Entry(self.Frame_prop_rap_ROT_D_TIME,width=10,validate="key",validatecommand=vcmd)
		self.ROT_Delta_Time.insert(END,'1')
		self.ROT_Delta_Time.pack(  # CONVERT_PACKside='right')

		Button(self.Frame_prop_rap_ROT,text=self.Dado_config.idioma(108),relief='ridge',command = self.plot).pack(fill=X)
		


		self.Frame_prop_rap_EIA = Frame(self.frameprincipal1.interior,bd=3,bg='gray',relief=GROOVE)
		self.Frame_prop_rap_EIA_Entry = Frame(self.Frame_prop_rap_EIA,bg='gray')
		self.Frame_prop_rap_EIA_Entry.pack(  # CONVERT_PACKfill=X)
		Label(self.Frame_prop_rap_EIA,text=self.Dado_config.idioma(53)).pack(fill=X)
		self.cal_EIA = DateEntry(self.Frame_prop_rap_EIA, textvariable = self.Data_Entry,background='darkblue',foreground='white', borderwidth=2)
		self.cal_EIA.bind('<<DateEntrySelected>>', self.atualizar_dip)  # CONVERT_BIND
		self.cal_EIA.pack(  # CONVERT_PACKfill='x')
		Label(self.Frame_prop_rap_EIA,text=self.Dado_config.idioma(54)).pack(fill='x')
		self.Data_Entry_EIA2 = StringVar(janelaprincipal)
		self.cal2_EIA = DateEntry(self.Frame_prop_rap_EIA,textvariable=self.Data_Entry_EIA2,background='darkblue',foreground='white', borderwidth=2)
		self.cal2_EIA.pack(  # CONVERT_PACKfill='x')
		self.Frame_prop_rap_EIA_Check = Frame(self.Frame_prop_rap_EIA,bg='gray')
		self.Frame_prop_rap_EIA_Check.pack(  # CONVERT_PACKfill=X)
		self.cal_EIA_lblest = Label(self.Frame_prop_rap_EIA_Check,text=self.Dado_config.idioma(109),relief=GROOVE)
		self.cal_EIA_lblest.pack(  # CONVERT_PACKside='left',fill=BOTH,expand=True)
		self.cal_EIA_checkest = Checkbutton(self.Frame_prop_rap_EIA_Check,variable=self.cal_SETOR_EIA_varest,width=5,command=self.check_est_setor_EIA)
		self.cal_EIA_checkest.pack(  # CONVERT_PACKside='right')
		self.Frame_prop_rap_EIA_eixoY = Frame(self.Frame_prop_rap_EIA,bg='gray',relief=GROOVE)
		self.Frame_prop_rap_EIA_eixoY.pack(  # CONVERT_PACKfill=X)
		self.varaxixY = IntVar(self.janelaprincipal)
		self.varaxixY.set(1)
		Label(self.Frame_prop_rap_EIA_eixoY,text=self.Dado_config.idioma(120),relief=GROOVE).pack(fill=X)
		Radiobutton(self.Frame_prop_rap_EIA_eixoY,variable=self.varaxixY,value=0,text='Latitude',relief=GROOVE,command=self.radio_dip_setor_EIA).pack(side='right',fill=X,expand=1)
		Radiobutton(self.Frame_prop_rap_EIA_eixoY,variable=self.varaxixY,value=1,text='Dip.Lat',relief=GROOVE,command=self.radio_dip_setor_EIA).pack(side='left',fill=X,expand=1)
		self.Frame_prop_rap_EIA_btn = Frame(self.Frame_prop_rap_EIA,bg='gray',relief=GROOVE)
		self.Frame_prop_rap_EIA_btn.pack(  # CONVERT_PACKfill=X)
		Button(self.Frame_prop_rap_EIA_btn,text=self.Dado_config.idioma(108),relief='ridge',command = self.plot).pack(fill=X)

		
		
		
		





		
		
		
		
		
		
		
		
		
		
		
		
		
		
		

		
		
		
		
		


		self.fig_map, self.ax_map = plt.subplots()

		try:
			cbg_loc_g = self.lista_loc[self.n_lista_loc.index(self.cbg_loc_value.get())]
		except ValueError:
			cbg_loc_g = self.lista_loc[self.n_lista_loc.index(self.lista_loc[0][0])]
			self.cbg_loc_value.set(self.lista_loc[0][0])
			self.Dado_config.setMapa(self.lista_loc[0][0])

		self.la = cbg_loc_g[1].split(' ')
		self.lo = cbg_loc_g[2].split(' ')

		
		


		self.map = Basemap(projection='cyl',llcrnrlat=-90, urcrnrlat=90,llcrnrlon=-180, urcrnrlon=180, resolution='l')

		self.map.drawcoastlines(linewidth=1.1,zorder=3)
		self.map.drawcountries(linewidth=1.1,zorder=3)
		self.map.drawstates(linewidth=1.1,zorder=3)
		
		
		self.ax_map.set_ylim(int(self.la[0]),int(self.la[1]))
		self.ax_map.set_xlim(int(self.lo[0]),int(self.lo[1]))
		self.canvas_map = FigureCanvasTkAgg(self.fig_map,self.frameprincipal2)
		self.canvas_map.get_tk_widget().pack(side='right',expand=True, fill=BOTH)
		toolbar = NavigationToolbar2Tk(self.canvas_map, self.frameprincipal2)
		toolbar.update()
		self.canvas_map._tkcanvas.pack(  # CONVERT_PACKside=TOP,expand=True, fill=BOTH)

		self.fig_map.canvas.mpl_connect('pick_event', self.on_click_map)


		
		
		
		
		
		self.lista_plots = []
		self.lista_plots_text = []
		if self.accept:self.fig_map.canvas.mpl_connect('motion_notify_event', self.vis_info)

		
		

		self.fig_map.tight_layout(pad=0)
		

		






		Caminho =  self.Dado_config.getLocalSTD()
		if Caminho != "None" and self.accept:
			if os.path.exists(Caminho):
				self.selecionar(Caminho,dip=False)

		self.janelaprincipal.bind("<Return>",self.plot)  # CONVERT_BIND
		self.janelaprincipal.protocol("WM_DELETE_WINDOW", self.quit)
		self.janelaprincipal.mainloop()

	def set_cores_ROT(self,*event):
		self.plot()
		self.refreshCanvas()

	def state_refresh(self,event=None):
		if self.tela_graf_old_state != self.tela_graf.state():
			self.tela_graf_old_state = self.tela_graf.state()
			self.refreshCanvas()
			self.refreshCanvas()

	def quit(self):
		self.Dado_config.writeConfig()
		plt.close('all')
		self.canvas_img.get_tk_widget().destroy()
		self.canvas_map.get_tk_widget().destroy()
		self.tela_graf.destroy()
		self.janelaprincipal.destroy()


	def atualizar_dip(self,event):
		year = int(self.Data_Entry.get()[-4:])
		if year != self.Data_linha_eqm:
			back_list = self.listaobs.curselection()
			n_list,self.conteudo_lista = self.uti.Refresh_list_obs(self.filedir,year,True)
			self.Data_linha_eqm = year
			if self.conteudo_lista or n_list:
				self.listaobs.delete(0,'end')
				[self.listaobs.insert('end', item) for item in self.conteudo_lista]
				[self.listaobs.insert('end', item + " ("+ self.Dado_config.idioma(144) +")") for item in n_list]
			self.plot_linha_eq_mag(year)
			[self.listaobs.select_set(id) for id in back_list]
			self.Data_Entry_INDV2.set(self.Data_Entry.get())
			self.Data_Entry_DESVIO2.set(self.Data_Entry.get())
			self.Data_Entry_EIA2.set(self.Data_Entry.get())

	def radio_dip_setor_EIA(self):
		if len(self.listaobs.curselection())>1:self.plot()

	def check_fill(self):
		if self.filedir:
			try:
				self.selecionar(self.filedir)
			except FileNotFoundError :
				pass

	def check_est_setor_EIA(self):
		try:
			if self.cal_SETOR_EIA_varest.get():
				self.img_axes.yaxis.set_major_locator(ticker.FixedLocator(self.eixoG))
				self.img_axes.minorticks_off()
			else:
				self.img_axes.minorticks_on()
				if self.passo_tickY_setor:
					self.img_axes.yaxis.set_major_locator(ticker.IndexLocator(base=(self.passo_tickY_setor), offset=self.minY_setor))
				elif self.n_rotuloY_setor:
					self.img_axes.yaxis.set_major_locator(ticker.LinearLocator(round(self.n_rotuloY_setor)))
				else:
					self.img_axes.yaxis.set_major_locator(ticker.LinearLocator())
		except AttributeError:
			if self.passo_tickY_setor:
				self.img_axes.yaxis.set_major_locator(ticker.IndexLocator(base=(self.passo_tickY_setor), offset=self.minY_setor))
			elif self.n_rotuloY_setor:
				self.img_axes.yaxis.set_major_locator(ticker.LinearLocator(round(self.n_rotuloY_setor)))
			else:
				self.img_axes.yaxis.set_major_locator(ticker.LinearLocator())
		self.refreshCanvas()

	def drawstates(self,ax, shapefile='BRA_adm1'):
		shp = self.m.readshapefile(shapefile, 'states', drawbounds=True)
		for nshape, seg in enumerate(self.m.states):
			poly = Polygon(seg, facecolor='0.75', edgecolor='k')
			ax.add_patch(poly)

	def save_matriz(self):
		if self.varmatriz.get() == True:
			if self.cbg_value.get() == "Individual (STD)":
				self.save_matriz_ind()
			elif self.cbg_value.get() in ("Setor (STD)", "EIA (STD)"):
				self.save_matriz_SETOR_EIA()
			elif self.cbg_value.get() == "Desvio (STD)":
				self.save_matriz_desvio()
			elif self.cbg_value.get() == "Mapa (CMN)":
				
				pass
			elif self.cbg_value.get() == "ROT (CMN)":
				self.save_matriz_rot()

	def save_matriz_rot(self):
    	
		for sat in self.prn:
			with open(("%s\%2.2i-%2.2i-%i_%s_PRN%0.2i.ROT"%(self.filedir,self.data.day,self.data.month,self.data.year,self.sigla,sat)),'w') as arqTri:
				arqTri.write("Hora\tROT\n")
				for hora in np.arange(0,24,(.5/60)):
					try:
						ind = self.dados[str(sat)+".time"].index("%.6f"%hora)
						if np.isnan(self.dados[str(sat)+".rot"][ind]):
							arqTri.write("%06.3f\t-999,00\n"%hora)
						else:
							arqTri.write(("%06.3f\t%.2f\n"%(hora,self.dados[str(sat)+".rot"][ind])))
					except ValueError:
						arqTri.write("%06.3f\t-999,00\n"%hora)


	def save_matriz_desvio(self):
		for tec_n,sigla,med,desv in zip(self.tec_desv,[s[0]for s in self.siglas],self.med,self.desv):
			
			nome = ('%s-%s-%s(%s-%s)')%(sigla,self.Data_Entry.get()[6:],self.Data_Entry.get()[3:5],self.Data_Entry.get()[0:2],self.Data_Entry_DESVIO2.get()[0:2])
			self.matriz_linha((r"%s\%s.Std")%(self.filedir,nome),tec_n,med,desv)

	def matriz_linha(self,caminho,tec_n,med_calm,desv_calmo):
		try:
			with open(caminho,'w') as arqTri:
				arqTri.write("Média\tMed+Des\tMed-Des")
				for contd in range(self.delta):
					datafile = (datetime.strptime(self.Data_Entry.get(), '%d/%m/%Y') + timedelta(days=contd))
					arqTri.write(("\tHora\tTec %i")%(datafile.day))
				else:arqTri.write("\n")
				for t,tec_est,m,d in zip(self.temp,tec_n.T,med_calm,desv_calmo):
					arqTri.write(((("%.2f\t%.2f\t%.2f")%(m,(m+d),(m-d))).replace("nan","-999,0")).replace(".",","))
					for tec_dia in tec_est:arqTri.write(((("\t%.2f\t%.2f")%(t,tec_dia)).replace("nan","-999,0")).replace(".",","))
					else:arqTri.write("\n")
		except (IOError):
			pass

	def save_matriz_SETOR_EIA(self):
		try:
			with open(self.filedir+("\%s_%s_Matriz.Std"%([sgl[0] for sgl in self.siglas],self.titulo[:10])),'w') as arqTri:
				if self.varaxixY.get() == 0:arqTri.write("HORA\tLATITUDE\tVTEC\n")
				else:arqTri.write("HORA\tDIP LATITUDE\tVTEC\n")
				for (x,y,z) in list(self.estacao_select_matriz):
					arqTri.write(("%.2f\t%.2f\t%.2f\n"%(x,y,z)).replace('.',','))
		except (IOError):
			pass

	def save_matriz_ind(self):
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
				for tecN in matriz_tmp.flatten():
					if tecN < 0:
						Matriz_std+=("-----\t")
					else:
						Matriz_std+=(("%05.2f\t")%(tecN)).replace(".",",")
				tmp_media = [float(n) for n in matriz_tmp.flatten() if not np.isnan(n)]
				try:
					mediaTEC = sum(tmp_media)/float(len(tmp_media))
				except ZeroDivisionError:
					messagebox.showerror(self.Dado_config.idioma(49),self.Dado_config.idioma(94),parent=self.janelaprincipal)
					raise IOError
				des_std = np.std(tmp_media)
				Matriz_std+=(("%06.3f\t")%(mediaTEC)).replace(".",",")
				Matriz_std+=(("%06.3f\t")%(des_std)).replace(".",",")
				Matriz_std+=(("%06.3f\t")%(mediaTEC+des_std)).replace(".",",")
				Matriz_std+=(("%06.3f\n")%(mediaTEC-des_std)).replace(".",",")
			with open((self.filedir  + ("/%s_matriz.std")%(self.titulo)), 'w',encoding="UTF-8") as arquivoMat:
				arquivoMat.write(Matriz_std)
				arquivoMat.close()
		except PermissionError:
			messagebox.showerror(self.Dado_config.idioma(49),self.Dado_config.idioma(95),parent=self.janelaprincipal)

	def save_png(self):
		if self.varsave.get():
			if self.filedir and self.titulo:
				if self.cbg_value.get() == "Desvio (STD)":self.img.savefig(("%s\%s.png")%(self.filedir,self.titulo),facecolor=self.img.get_facecolor())
				else:self.img.savefig(("%s\%s.png")%(self.filedir,self.titulo))
					

	def do_popup(self,event):
		try:
			self.popup_graf.tk_popup(event.x_root, event.y_root, 0)
		finally:
			self.popup_graf.grab_release()

	def atua_grid_X(self,verifi=None,refresh=True):
		if not verifi:
			self.vargrid_X.set(not self.vargrid_X.get())
			if self.vargrid_X.get() == True:
				self.popup_graf.entryconfig(self.Dado_config.idioma(141),label=self.Dado_config.idioma(142))
			else:
				self.popup_graf.entryconfig(self.Dado_config.idioma(142),label=self.Dado_config.idioma(141))
		try:
			self.img_axes.xaxis.grid(  # CONVERT_GRIDself.vargrid_X.get())
		except (AttributeError,ValueError):
			for axe_i in np.array(self.img_axes).flatten():
				axe_i.xaxis.grid(  # CONVERT_GRIDself.vargrid_X.get())
				
		if refresh:self.refreshCanvas()

	def atua_grid_Y(self,verifi=None,refresh=True):
		if not verifi:
			self.vargrid_Y.set(not self.vargrid_Y.get())
			if self.vargrid_Y.get() == True:
				self.popup_graf.entryconfig(self.Dado_config.idioma(139),label=self.Dado_config.idioma(140))
			else:
				self.popup_graf.entryconfig(self.Dado_config.idioma(140),label=self.Dado_config.idioma(139))
		try:
			self.img_axes.yaxis.grid(  # CONVERT_GRIDself.vargrid_Y.get())
		except (AttributeError,ValueError):
			for axe_i in np.array(self.img_axes).flatten():
				axe_i.yaxis.grid(  # CONVERT_GRIDself.vargrid_Y.get())
		if refresh:self.refreshCanvas()

	def plot_linha_eq_mag(self,ano,img=None):
		eq_y = []
		eq_x = []
		for x in range(-180,181,1):
			inclinacao = self.uti.get_inclinacao(300,ano,0,0,x,0)
			diplat = -(math.degrees(math.atan(((math.tan(math.radians(float(inclinacao)))/2)))))
			eq_y.append(diplat)
			eq_x.append(x)
		if self.linha_eq_mag:
			self.background = self.fig_map.canvas.copy_from_bbox(self.fig_map.bbox)
			self.fig_map.canvas.restore_region(self.background)
			eq_x,eq_y = self.map(eq_x,eq_y)
			self.linha_eq_mag.set_data(eq_x,eq_y)
			self.ax_map.draw_artist(self.linha_eq_mag)
			self.fig_map.canvas.blit(self.fig_map.bbox)
			self.fig_map.canvas.draw()
		else:
			eq_x,eq_y = self.map(eq_x,eq_y)
			if img:
				self.linha_eq_mag = img.plot(eq_x,eq_y,'K',gid="line_ecuador_mag",picker=2)[0]
			else:
				self.linha_eq_mag = self.map.plot(eq_x,eq_y,'K',gid="line_ecuador_mag",picker=2)[0]

	def quit_graf(self):
		self.tela_graf.withdraw()

	def refreshCanvas(self,event=None):
		try:
			if self.cbg_value.get() == "Individual (STD)":
				self.img.tight_layout()
				self.img.canvas.draw()
				self.img.canvas.flush_events()
			elif self.cbg_value.get() in ("Setor (STD)","EIA (STD)"):
				self.img.tight_layout()
				self.img.canvas.draw()
				self.img.canvas.flush_events()
			elif self.cbg_value.get() == "Desvio (STD)":
				self.img.tight_layout(rect=[0, 0.03, 1, 0.95])
				self.img.subplots_adjust(wspace=0,hspace=0)
				self.img.canvas.draw()
				self.img.canvas.flush_events()
			elif self.cbg_value.get() == "Mapa (CMN)":
				self.img.tight_layout()
				self.img.canvas.draw()
				self.img.canvas.flush_events()
			elif self.cbg_value.get() == "ROT (CMN)":
				self.img.tight_layout()
				self.img.canvas.draw()
				self.img.canvas.flush_events()
			self.pick_axes()
		except (AttributeError, ValueError, TypeError):
			pass

	def sel_map(self,event):
		id = self.listaobs.curselection()
		self.cont_est_select.set(len(id))
		if self.filedir:
			self.inf = None
			new_id = []
			for item in id:
				if self.listaobs.get(item)[6:-1] == self.Dado_config.idioma(144):self.inf=True
				else:new_id.append(item)
			if self.cbg_value.get() in ("Individual (STD)","ROT (CMN)"):
				self.un_sel(self.current_plot)
				if not self.inf:
					self.current_plot = (self.lista_plots[self.uti.list_duplicates_of(self.lista_plots_label,self.listaobs.get(id)[:4])[0]])
					self.in_sel(self.current_plot)
				self.plot()
			elif self.cbg_value.get() in ("Setor (STD)", "Desvio (STD)", "EIA (STD)"):
				Delta_lista = list(set(self.list_id) - set(list(new_id)))
				if Delta_lista:
					self.un_sel(self.lista_plots[self.uti.list_duplicates_of(self.lista_plots_label,self.listaobs.get(Delta_lista)[:4])[0]])
				else:
					Delta_lista = list(set(list(new_id)) - set(self.list_id))
					self.in_sel(self.lista_plots[self.uti.list_duplicates_of(self.lista_plots_label,self.listaobs.get(Delta_lista)[:4])[0]])
				self.list_id = new_id
		else:
			messagebox.showerror(self.Dado_config.idioma(49),self.Dado_config.idioma(126),parent=self.janelaprincipal)

	def un_sel(self,*events):
		try:
			for event in events:
				event.set_color('red')
				self.update_scatter(event)
		except (AttributeError, ValueError, TypeError):
			pass

	def in_sel(self,event):
		try:
			event.set_color('green')
			self.update_scatter(event)
		except (AttributeError, ValueError, TypeError):
			pass
	def modelo_mapa(self,*event):
		self.la = self.ax_map.get_ylim()
		self.lo = self.ax_map.get_xlim()
		self.img.clf()
		self.img.set_facecolor('white')
		ax = self.img.add_subplot(111)
		eq_y = []
		eq_x = []
		ano = int(self.Data_Entry.get()[-4:])
		for x in range(-180,181,1):
			inclinacao = self.uti.get_inclinacao(300,ano,0,0,x,0)
			diplat = -(math.degrees(math.atan(((math.tan(math.radians(float(inclinacao)))/2)))))
			eq_y.append(diplat)
			eq_x.append(x)

		m =  Basemap(ax = ax, projection='cyl',resolution='l',llcrnrlat=self.la[0], urcrnrlat=self.la[1],llcrnrlon=self.lo[0], urcrnrlon=self.lo[1])
		m.drawcoastlines()
		m.drawcountries()
		m.drawstates()
		y = np.array([-90.0 ,90.0,-180.0, 180.0])
		x = np.array([-180,-180,180,180])
		z = np.array([10,20,30,40])
		passo = 1;level = np.arange(0,(self.vm+1),passo)
		xi,yi,GD1 = self.uti.Interpool_xyz(x,y,z)
		m.plot(eq_x,eq_y,'K',gid="line_ecuador_mag",picker=2)
		cmap = plt.cm.get_cmap("jet")
		cmap.set_under("white")
		cmap.set_over("darkred")

		font_default = {'family' : 'Arial','weight' : 'bold','size' : 18}

		self.cbar_model_map = self.img.colorbar(m.contourf(xi,yi,GD1, cmap = cmap,levels = level, vmin = 0, vmax = self.vm ,extend="both" ),ticks = np.arange(0,self.vm+1,5))
		self.cbar_model_map.ax.set_picker(5)
		self.cbar_model_map.ax.set_gid("tick_bar_graph_model_map")
		

		ax.set_title("00:0.00",**self.rfont_titulo_bar_model_map)

		self.cbar_model_map.ax.set_title(self.titulo_bar_model_map,**self.rfont_titulo_bar_model_map,picker=5,gid="label_bar_graph_model_map")
		if self.tela_graf.state() == "withdrawn" or self.tela_graf.state() == "iconic":
			self.tela_graf.deiconify()
		elif self.tela_graf.state() == "normal":
			self.tela_graf.focus_force()

		self.refreshCanvas()
		self.img.canvas.mpl_connect('pick_event', self.on_click_prop)
		self.janelaprincipal.wait_window(self.janelaprincipal)

	def plot(self,*event):
		if self.filedir:
			if len(self.listaobs.curselection()) != 0:
				if self.cbg_value.get() == "Individual (STD)":
					self.plot_INV(self.vm)
				elif self.cbg_value.get() == "Setor (STD)" and not self.inf:
					self.plot_SETOR(self.vm)
				elif self.cbg_value.get() == "EIA (STD)" and not self.inf:
					self.plot_EIA(self.vm)
				elif self.cbg_value.get() == "Desvio (STD)" and not self.inf:
					self.plot_DESVIO()
				elif self.cbg_value.get() == "ROT (CMN)" and not self.inf:
					self.plot_ROT()
				elif self.inf:messagebox.showerror(self.Dado_config.idioma(49),self.Dado_config.idioma(162),parent=self.janelaprincipal)
			elif self.cbg_value.get() == "Mapa (CMN)" and not self.inf:
				self.plot_MAPA(self.vm)
		else:
			messagebox.showerror(self.Dado_config.idioma(49),self.Dado_config.idioma(126),parent=self.janelaprincipal)

	def vis_info(self,event):
		temp_pth = ""
		for pth in self.lista_plots:
			if pth.contains(event)[0]:
				temp_pth = pth
				w,h = self.fig_map.get_size_inches()*self.fig_map.dpi
				ws = (event.x > w/2.)*-1 + (event.x <= w/2.)
				hs = (event.y > h/2.)*-1 + (event.y <= h/2.)
				self.ab.xybox = (self.xybox[0]*ws, self.xybox[1]*hs)
				self.ab.set_visible(True)
				data = temp_pth.get_offsets()[0]
				self.ab.xy =(data[0], data[1])
				self.txb.set_text(temp_pth.get_label())
				break
			else:
				self.ab.set_visible(False)
			self.fig_map.canvas.draw_idle()

	def on_click_map(self,event):
		if event.artist.get_gid() == "station":
			if self.cbg_value.get() in ("Individual (STD)","ROT (CMN)"):
				self.listaobs.selection_clear(0,END)
				self.listaobs.selection_set(self.check_index(event.artist.get_label()))
				self.listaobs.event_generate('<<ListboxSelect>>')
			elif self.cbg_value.get() in ("Setor (STD)" ,"EIA (STD)","Desvio (STD)"):
				id_check = self.check_index(event.artist.get_label())
				if self.listaobs.selection_includes(id_check):
					self.listaobs.selection_clear(id_check)
				else:
					self.listaobs.selection_set(id_check)
				self.listaobs.event_generate('<<ListboxSelect>>')
		elif event.artist.get_gid() == "line_ecuador_mag":
			
			
			pass

	def update_scatter(self,current):
		self.background = self.fig_map.canvas.copy_from_bbox(self.fig_map.bbox)
		self.fig_map.canvas.restore_region(self.background)
		self.ax_map.draw_artist(current)
		self.fig_map.canvas.blit(self.fig_map.bbox)

	def setar_legends(self,refresh=True):
		if self.cbg_value.get() == "Desvio (STD)":
			try:
				if self.Legend.get() == False:
					if type(self.legendas_desvio) == matplotlib.legend.Legend:
						if self.legendas_desvio:self.legendas_desvio.remove()
				elif self.Legend.get() == True:
					img_valida = None
					for l_lines in self.img_axes:
						for lines in l_lines:
							if len(lines.lines) == 2:
								img_valida = lines
								break
							elif len(lines.lines) == 1:
								img_valida = lines
					if img_valida:
						handles, labels = img_valida.get_legend_handles_labels()
						self.legendas_desvio = self.img.legend(handles, labels,facecolor="lightgrey" , loc='upper right', borderaxespad=0.)
						self.legendas_desvio.draggable(True)
			except (AttributeError,ValueError,TypeError):
				pass
		elif self.cbg_value.get() == "ROT (CMN)":
			if self.Legend.get() == False:
				self.img_axes.legend().remove()
			elif self.Legend.get() == True:
				self.img_axes.legend(bbox_to_anchor=(1.009, 0, .1, 1.9), loc=3,ncol=1, mode="expand", borderaxespad=0.).draggable(True)
		if refresh:self.refreshCanvas();self.refreshCanvas()

	def refresh_format_DESVIO(self):
		try:
			for AX,d_ax_X in zip(self.img_axes[0],self.datas):
				AX.set_title(d_ax_X[self.DateFormat_DESVIO.get()],**self.rfont_titulo_axe_y_desv)
			self.refreshCanvas()
		except (AttributeError,TypeError):
			pass

	def plot_DESVIO(self):
		if len(self.listaobs.curselection()) > 0:
			try:
				dataI = datetime.strptime(self.Data_Entry.get(), '%d/%m/%Y')
				dataF = datetime.strptime(self.Data_Entry_DESVIO2.get(), '%d/%m/%Y')
			except ValueError:
				messagebox.showerror(self.Dado_config.idioma(49),self.Dado_config.idioma(176),parent=self.janelaprincipal)
				return False

			self.siglas = []
			for iten_id in self.listaobs.curselection():
				item_line = ((self.listaobs.get(iten_id)).replace('(','')).replace(')','')
				item_line = item_line.split(",")
				N_L = item_line[0].split(' ')
				lat = (item_line[1].strip()).split(' ')
				self.siglas.append([N_L[0],N_L[1],N_L[2],lat[0],lat[1],item_line[2].strip()])
			self.siglas.sort(key=lambda x: float(x[5]),reverse=True)
			self.img,self.img_axes,self.titulo,self.tec_desv,self.desv,self.med,self.delta,self.temp,self.datas = COMP_DESVIO(self.img,self.filedir,self.siglas,self.Cal_Calm_days.selection_get(),dataI,dataF,self.DateFormat_DESVIO.get())._get_Matplotlib_grafico_att()
			[img_ax[0].yaxis.get_major_ticks()[-1].set_visible(False) for img_ax in self.img_axes[1:]]
			self.img.canvas.mpl_connect('pick_event', self.on_click_prop)
			self.min_ori_Y,self.max_ori_Y = self.img_axes[0][0].get_ylim()
			self.min_ori_X,self.max_ori_X = self.img_axes[0][0].get_xlim()
			if self.titulo_axe_y_desv:
				for ax in self.img_axes:
					ax[0].set_ylabel(self.titulo_axe_y_desv,**self.rfont_titulo_axe_y_desv)
			if self.titulo_graph_desv:
    				self.img.suptitle(self.titulo_graph_desv,**self.rfont_titulo_graph_desv,picker=5,gid="Sup_titulo_Desvio")
			if self.passo_tickX_desv:
				[img_ax.xaxis.get_major_ticks()[-1].set_visible(True) for img_ax in self.img_axes[-1][:-1]]
				delta_ult = 0
				for ax in self.img_axes[-1]:
					lisa_ticklb_X = np.arange(self.minX_desv,self.maxX_desv+self.passo_tickX_desv,self.passo_tickX_desv)
					delta_ult =  self.maxX_desv - lisa_ticklb_X[-1]
					ax.xaxis.set_major_locator(ticker.FixedLocator(lisa_ticklb_X))
				if delta_ult < 6.0:
					[img_ax.xaxis.get_major_ticks()[-1].set_visible(False) for img_ax in self.img_axes[-1][:-1]]
			elif self.n_rotuloX_desv:
				[img_ax.xaxis.get_major_ticks()[-1].set_visible(True) for img_ax in self.img_axes[-1][:-1]]
				[img_ax.xaxis.set_major_locator(ticker.LinearLocator(round(self.n_rotuloX_desv))) for img_ax in self.img_axes[-1]]
				[img_ax.xaxis.get_major_ticks()[-1].set_visible(False) for img_ax in self.img_axes[-1][:-1]]
			if self.minX_desv or self.maxX_desv:
				[img_ax.set_xlim(self.minX_desv,self.maxX_desv) for l_img_ax in self.img_axes for img_ax in l_img_ax]
			if self.passo_tickY_desv:
				[img_ax[0].yaxis.get_major_ticks()[-1].set_visible(True) for img_ax in self.img_axes[1:]]
				delta_ult = 0
				for ax in self.img_axes:
					lisa_ticklb_Y = np.arange(self.minY_desv,self.maxY_desv,self.passo_tickY_desv)
					delta_ult =  self.maxY_desv - lisa_ticklb_Y[-1]
					ax[0].yaxis.set_major_locator(ticker.FixedLocator(lisa_ticklb_Y))
				if delta_ult < 6.0:
					[img_ax[0].yaxis.get_major_ticks()[-1].set_visible(False) for img_ax in self.img_axes[1:]]
			elif self.n_rotuloY_desv:
				[img_ax[0].yaxis.get_major_ticks()[-1].set_visible(True) for img_ax in self.img_axes[1:]]
				[img_ax[0].yaxis.set_major_locator(ticker.LinearLocator(round(self.n_rotuloY_desv))) for img_ax in self.img_axes]
				[img_ax[0].yaxis.get_major_ticks()[-1].set_visible(False) for img_ax in self.img_axes[1:]]
			if self.minY_desv or self.maxY_desv:
				[img_ax.set_ylim(self.minY_desv,self.maxY_desv) for l_img_ax in self.img_axes for img_ax in l_img_ax]
			self.setar_legends(refresh=False)
			self.refresh_format_DESVIO()
			self.atua_grid_Y(verifi=True,refresh=False)
			self.atua_grid_X(verifi=True,refresh=False)
			self.save_matriz()
			self.save_png()
			self.pick_axes()
			if self.tela_graf.state() == "withdrawn" or self.tela_graf.state() == "iconic":
				self.tela_graf.deiconify()
			elif self.tela_graf.state() == "normal":
				try:
					self.tela_graf.focus_force()
				except TclError:
					pass
			self.refreshCanvas()
			self.janelaprincipal.wait_window(self.janelaprincipal)
			
			
			

	def plot_EIA(self,vm=50):
		if len(self.listaobs.curselection()) > 1:
			try:
				dataI = datetime.strptime(self.Data_Entry.get(), '%d/%m/%Y')
				dataF = datetime.strptime(self.Data_Entry_EIA2.get(), '%d/%m/%Y')
			except ValueError:
				messagebox.showerror(self.Dado_config.idioma(49),self.Dado_config.idioma(176),parent=self.janelaprincipal)
				return False

			self.siglas = []
			for iten_id in self.listaobs.curselection():
				item_line = ((self.listaobs.get(iten_id)).replace('(','')).replace(')','')
				item_line = item_line.split(",")
				N_L = item_line[0].split(' ')
				lat = (item_line[1].strip()).split(' ')
				self.siglas.append([N_L[0],N_L[1],N_L[2],lat[0],lat[1],item_line[2].strip()])
			self.vm = vm
			self.img ,self.img_axes ,self.img_cbar, self.titulo ,self.estacao_select_matriz,self.eixoG = COMP_EIA(self.img,self.siglas,self.filedir,dataI,dataF,self.vm,self.varaxixY.get(),self.cal_SETOR_EIA_varest).re_figura()
			self.img.canvas.mpl_connect('pick_event', self.on_click_prop)
			self.min_ori_Y,self.max_ori_Y = self.img_axes.get_ylim()
			self.min_ori_X,self.max_ori_X = self.img_axes.get_xlim()
			
			
			if self.titulo_axe_y_EIA and self.rfont_titulo_axe_y_EIA:
				self.img_axes.set_ylabel(self.titulo_axe_y_EIA,**self.rfont_titulo_axe_y_EIA)
			if self.titulo_axe_x_EIA and self.rfont_titulo_axe_x_EIA:
				self.img_axes.set_xlabel(self.titulo_axe_x_EIA,**self.rfont_titulo_axe_x_EIA)
			if self.titulo_bar_EIA and self.rfont_titulo_bar_EIA:
				try:
					self.img_cbar.ax.set_title(self.titulo_bar_EIA,**self.rfont_titulo_bar_EIA)
				except AttributeError:
					pass
			if self.passo_tickY_EIA:
				self.img_axes.yaxis.set_major_locator(ticker.IndexLocator(base=(self.passo_tickY_EIA), offset=self.minY_EIA))
			elif self.n_rotuloY_EIA:
				self.img_axes.yaxis.set_major_locator(ticker.LinearLocator(round(self.n_rotuloY_EIA)))
			if self.minY_EIA or self.maxY_EIA:
				self.img_axes.set_ylim(self.minY_EIA,self.maxY_EIA)
			if self.passo_tickX_EIA:
				self.img_axes.xaxis.set_major_locator(ticker.IndexLocator(base=(self.passo_tickX_EIA), offset=self.minX_EIA))
			elif self.n_rotuloX_EIA:
				self.img_axes.xaxis.set_major_locator(ticker.LinearLocator(round(self.n_rotuloX_EIA)))
			if self.minX_EIA or self.maxX_EIA:
				self.img_axes.set_xlim(self.minX_EIA,self.maxX_EIA)
			try:
				if self.cal_SETOR_EIA_varest.get():
					
					self.img_axes.yaxis.set_major_locator(ticker.FixedLocator(self.eixoG))
					self.img_axes.minorticks_off()
				
					
			except AttributeError:
				pass
			self.atua_grid_X(verifi=True,refresh=False)
			self.atua_grid_Y(verifi=True,refresh=False)
			self.save_matriz()
			self.save_png()
			self.pick_axes()
			if self.tela_graf.state() == "withdrawn" or self.tela_graf.state() == "iconic":
				self.tela_graf.deiconify()
			elif self.tela_graf.state() == "normal":
				self.tela_graf.focus_force()
			self.refreshCanvas()
			self.janelaprincipal.wait_window(self.janelaprincipal)
		else:
			messagebox.showerror(self.Dado_config.idioma(49),self.Dado_config.idioma(129),parent=self.janelaprincipal)

	def plot_SETOR(self,vm=50):
		if len(self.listaobs.curselection()) > 1:
			try:
				data = datetime.strptime(self.Data_Entry.get(), '%d/%m/%Y')
			except ValueError:
				messagebox.showerror(self.Dado_config.idioma(49),self.Dado_config.idioma(176),parent=self.janelaprincipal)
				return False

			self.siglas = []
			for iten_id in self.listaobs.curselection():
				item_line = ((self.listaobs.get(iten_id)).replace('(','')).replace(')','')
				item_line = item_line.split(",")
				N_L = item_line[0].split(' ')
				lat = (item_line[1].strip()).split(' ')
				self.siglas.append([N_L[0],N_L[1],N_L[2],lat[0],lat[1],item_line[2].strip()])
			self.vm = vm
			graf_Setor = COMP_SETOR(self.img,self.siglas,data,self.filedir,self.vm,self.varaxixY.get(),self.cal_SETOR_EIA_varest)
			graf_Setor._set_Matplotlib_grafico()
			self.img ,self.img_axes ,self.img_cbar ,self.titulo ,self.estacao_select_matriz,self.eixoG = graf_Setor._get_Matplotlib_grafico_att()
			if self.estacao_select_matriz:
				self.img.canvas.mpl_connect('pick_event', self.on_click_prop)
				self.min_ori_Y,self.max_ori_Y = self.img_axes.get_ylim()
				self.min_ori_X,self.max_ori_X = self.img_axes.get_xlim()
				
				
				if self.titulo_axe_y_setor and self.rfont_titulo_axe_y_setor:
					self.img_axes.set_ylabel(self.titulo_axe_y_setor,**self.rfont_titulo_axe_y_setor)
				if self.titulo_axe_x_setor and self.rfont_titulo_axe_x_setor:
					self.img_axes.set_xlabel(self.titulo_axe_x_setor,**self.rfont_titulo_axe_x_setor)
				if self.titulo_bar_setor and self.rfont_titulo_bar_setor:
					try:
						self.img_cbar.ax.set_title(self.titulo_bar_setor,**self.rfont_titulo_bar_setor)
					except AttributeError:
						pass
				if self.passo_tickY_setor:
					self.img_axes.yaxis.set_major_locator(ticker.IndexLocator(base=(self.passo_tickY_setor), offset=self.minY_setor))
				elif self.n_rotuloY_setor:
					self.img_axes.yaxis.set_major_locator(ticker.LinearLocator(round(self.n_rotuloY_setor)))
				if self.minY_setor or self.maxY_setor:
					self.img_axes.set_ylim(self.minY_setor,self.maxY_setor)
				if self.passo_tickX_setor:
					self.img_axes.xaxis.set_major_locator(ticker.IndexLocator(base=(self.passo_tickX_setor), offset=self.minX_setor))
				elif self.n_rotuloX_setor:
					self.img_axes.xaxis.set_major_locator(ticker.LinearLocator(round(self.n_rotuloX_setor)))
				if self.minX_setor or self.maxX_setor:
					self.img_axes.set_xlim(self.minX_setor,self.maxX_setor)
				try:
					if self.cal_SETOR_EIA_varest.get():
						
						self.img_axes.yaxis.set_major_locator(ticker.FixedLocator(self.eixoG))
						self.img_axes.minorticks_off()
					
						
				except AttributeError:
					pass
				self.atua_grid_X(verifi=True,refresh=False)
				self.atua_grid_Y(verifi=True,refresh=False)
				self.save_matriz()
				self.save_png()
				self.pick_axes()

			if self.tela_graf.state() == "withdrawn" or self.tela_graf.state() == "iconic":
				self.tela_graf.deiconify()
			elif self.tela_graf.state() == "normal":
				self.tela_graf.focus_force()
			self.refreshCanvas()
			self.janelaprincipal.wait_window(self.janelaprincipal)
		else:
			messagebox.showerror(self.Dado_config.idioma(49),self.Dado_config.idioma(129),parent=self.janelaprincipal)

	def plot_INV(self,vm=50):
		id = self.listaobs.curselection()
		sigla = self.listaobs.get(id)[:4]
		try:
			dataI = datetime.strptime(self.Data_Entry.get(), '%d/%m/%Y')
			dataF = datetime.strptime(self.Data_Entry_INDV2.get(), '%d/%m/%Y')
		except ValueError:
			messagebox.showerror(self.Dado_config.idioma(49),self.Dado_config.idioma(176),parent=self.janelaprincipal)
			return False

		self.vm = vm
		indv = COMP_INDV(self.img,sigla,dataI,dataF,self.filedir,self.DateFormat_INDV,self.vm)
		indv._set_Matplotlib_grafico()
		self.img,self.img_axes,self.img_cbar,self.titulo,self.TECdias,self.matrizstd,self.matrizdias_indv = indv._get_Matplotlib_grafico_att()
		
		if self.matrizstd.all():
			self.img.canvas.mpl_connect('pick_event', self.on_click_prop)
			self.min_ori_Y,self.max_ori_Y = self.img_axes.get_ylim()
			self.min_ori_Y /= 60 ;self.max_ori_Y /= 60
			
			self.min_ori_X,self.max_ori_X = self.img_axes.get_xlim()
			
			
			
			if self.rfont_titulo_graph_indv:
				self.img_axes.set_title(self.titulo,**self.rfont_titulo_graph_indv)
			if self.titulo_axe_y_indv and self.rfont_titulo_axe_y_indv:
				self.img_axes.set_ylabel(self.titulo_axe_y_indv,**self.rfont_titulo_axe_y_indv)
			if self.titulo_axe_x_indv and self.rfont_titulo_axe_x_indv:
				self.img_axes.set_xlabel(self.titulo_axe_x_indv,**self.rfont_titulo_axe_x_indv)
			if self.titulo_bar_indv and self.rfont_titulo_bar_indv:
				try:
					self.img_cbar.ax.set_title(self.titulo_bar_indv,**self.rfont_titulo_bar_indv)
				except AttributeError:
					pass
			
			if self.passo_tickX_indv:
				self.img_axes.xaxis.set_major_locator(ticker.IndexLocator(base=(self.passo_tickX_indv), offset=self.minX_indv))
			elif self.n_rotuloX_indv:
				self.img_axes.xaxis.set_major_locator(ticker.LinearLocator(round(self.n_rotuloX_indv)))

			
			
	
	
			if self.passo_tickY_indv:
				self.img_axes.yaxis.set_major_locator(ticker.IndexLocator(base=(self.passo_tickY_indv), offset=self.minY_indv))
			elif self.n_rotuloY_indv:
				self.img_axes.yaxis.set_major_locator(ticker.LinearLocator(round(self.n_rotuloY_indv)))
			
			if self.minY_indv or self.maxY_indv:
				self.img_axes.set_ylim(self.minY_indv,self.maxY_indv)

			self.atua_grid_X(verifi=True,refresh=False)
			self.atua_grid_Y(verifi=True,refresh=False)
			self.save_matriz()
			self.save_png()
			self.pick_axes()
		if self.tela_graf.state() == "withdrawn" or self.tela_graf.state() == "iconic":
			self.tela_graf.deiconify()
		elif self.tela_graf.state() == "normal":
			self.tela_graf.focus_force()
		self.refreshCanvas()
		self.janelaprincipal.wait_window(self.janelaprincipal)
		

	def plot_ROT(self):
		try:
			self.data = datetime.strptime(self.Data_Entry.get(), '%d/%m/%Y')
		except ValueError:
			messagebox.showerror(self.Dado_config.idioma(49),self.Dado_config.idioma(176),parent=self.janelaprincipal)
			return False

		id = self.listaobs.curselection()
		self.sigla = self.listaobs.get(id)[:4]
		d_T = self.ROT_Delta_Time.get()
		if d_T:d_T = float(self.ROT_Delta_Time.get().replace(',','.'))
		else:d_T=1
		self.img,self.img_axes,self.titulo,self.prn,self.dados = COMP_ROT(self.img,self.sigla,self.filedir,self.data,self.ROT_varest.get(),d_T).re_figura()
		if self.prn:
			self.img.canvas.mpl_connect('pick_event', self.on_click_prop)
			if self.titulo_axe_y_rot and self.rfont_titulo_axe_y_rot:
				self.img_axes.set_ylabel(self.titulo_axe_y_rot,**self.rfont_titulo_axe_y_rot)
			if self.titulo_axe_x_rot and self.rfont_titulo_axe_x_rot:
				self.img_axes.set_xlabel(self.titulo_axe_x_rot,**self.rfont_titulo_axe_x_rot)
			
				

			if self.passo_tickX_rot:self.img_axes.xaxis.set_major_locator(ticker.IndexLocator(base=(self.passo_tickX_rot), offset=self.minX_rot))
			elif self.n_rotuloX_rot:self.img_axes.xaxis.set_major_locator(ticker.LinearLocator(round(self.n_rotuloX_rot)))
			if self.minX_rot or self.maxX_rot:self.img_axes.set_xlim(self.minX_rot,self.maxX_rot)

			
			
			

			if self.passo_tickY_rot:self.img_axes.yaxis.set_major_locator(ticker.FixedLocator([(pr*10) for pr in np.arange(self.prn[0],self.prn[-1]+1,self.passo_tickY_rot)]))
			elif self.n_rotuloY_rot:self.img_axes.yaxis.set_major_locator(ticker.LinearLocator(round(self.n_rotuloY_rot)))
			
			if self.minY_rot or self.maxY_rot:self.img_axes.set_ylim(self.minY_rot,self.maxY_rot)
			self.setar_legends(refresh = False)
			self.atua_grid_X(verifi=True,refresh = False)
			self.atua_grid_Y(verifi=True,refresh = False)
			self.save_matriz()
			self.save_png()
			self.pick_axes()
			
		if self.tela_graf.state() == "withdrawn" or self.tela_graf.state() == "iconic":
			self.tela_graf.deiconify()
		elif self.tela_graf.state() == "normal":
			self.tela_graf.focus_force()
		self.refreshCanvas()
		if self.Legend.get():self.refreshCanvas()
		self.janelaprincipal.wait_window(self.janelaprincipal)


	def plot_MAPA(self,vm=50):
		try:
			self.data = datetime.strptime(self.Data_Entry.get(), '%d/%m/%Y')
		except ValueError:
			messagebox.showerror(self.Dado_config.idioma(49),self.Dado_config.idioma(176),parent=self.janelaprincipal)
			return False

		
		self.la = self.ax_map.get_ylim()
		self.lo = self.ax_map.get_xlim()
		
		self.var_barra_loading = DoubleVar()
		self.var_barra_loading_lbl = ""
		self.var_process = False
		self.var_process.set(False)
		

		thread_MAPA = thread_with_trace(target = COMP_MAPA, args = (self.filedir,self.data,vm,float(self.MAPA_Time_INICIO.get()),float(self.MAPA_Time_FIM.get()),float(self.MAPA_Delta_Time.get()),self.conteudo_lista,self.titulo_bar_model_map,self.rfont_titulo_bar_model_map,self.la[0],self.la[1],self.lo[0],self.lo[1],self.var_barra_loading,self.var_barra_loading_lbl, )) 
		thread_MAPA.start()

		
		
		


		qtSimpleDialog.Loading(self.janelaprincipal,'loading...',orient_u = HORIZONTAL,maximum_u = 100,length_u = 500, mode_u = 'determinate', icon=self.uti.resource_path('icone.ico'),progress_var = self.var_barra_loading,info_loading=self.var_barra_loading_lbl,_thread_name=thread_MAPA)



	
	
	
	

	def pick_axes(self):
		
		try:
			if 	self.cbg_value.get() == "Desvio (STD)":
				for img_ax in self.img_axes:
					for label in img_ax[0].get_xticklabels():
						label.set_picker(True)
						label.set_gid("ticks_x_Desvio")
				for label in img_ax[0].get_yticklabels():
					label.set_picker(True)
					label.set_gid("ticks_y_Desvio")
			else:
				for label in self.img_axes.get_xticklabels():
					label.set_picker(True)
					label.set_gid("ticks_x_"+self.cbg_value.get()[:-6].title())
				for label in self.img_axes.get_yticklabels():
					label.set_picker(True)
					label.set_gid("ticks_y_"+self.cbg_value.get()[:-6].title())
		except (TypeError, ValueError):
			pass

	def on_click_prop(self,event):


		"""
			Adaptar os títulos .... para o padrão inglês ou portuguesesadasd (:>)
			-=, subtracts a value from variable, setting the variable to the result
			*=, multiplies the variable and a value, making the outcome the variable
			/=, divides the variable by the value, making the outcome the variable
			%=, performs modulus on the variable, with the variable then being set to the result of it
		"""
		

		if event.artist.get_gid() == "y_label_graph_Desvio":
			titulo_atual = event.artist.get_text()
			self.titulo_axe_y_desv,self.rfont_titulo_axe_y_desv = askEntry(self.janelaprincipal,"LABEL Y",titulo_atual,self.rfont_titulo_axe_y_desv,self.tela_graf)
			if self.rfont_titulo_axe_y_desv:
				for ax in self.img_axes:
					ax[0].set_ylabel(self.titulo_axe_y_desv,**self.rfont_titulo_axe_y_desv)
			elif self.titulo_axe_y_desv != titulo_atual:
				for ax in self.img_axes:
					ax[0].set_ylabel(self.titulo_axe_y_desv)
			self.refresh_format_DESVIO()

		if event.artist.get_gid() == "Sup_titulo_Desvio":
			titulo_atual = event.artist.get_text()
			self.titulo_graph_desv,self.rfont_titulo_graph_desv = askEntry(self.janelaprincipal,"LABEL " + self.Dado_config.idioma(170),titulo_atual,self.rfont_titulo_graph_desv,self.tela_graf)

			if self.rfont_titulo_graph_desv:
				self.img.suptitle(self.titulo_graph_desv,picker=5,gid="Sup_titulo_Desvio",**self.rfont_titulo_graph_desv)
			elif self.titulo_graph_desv:
				self.img.suptitle(self.titulo_graph_desv,picker=5,gid="Sup_titulo_Desvio",**self.rfont_titulo_graph_desv)

		elif event.artist.get_gid() == "ticks_x_Desvio":
			self.minX_desv,self.maxX_desv = self.img_axes[0][0].get_xlim()
			tam_x,L_MJ_x,A_MJ_x,L_MN_x,A_MN_x,self.minX_desv,self.maxX_desv,self.passo_tickX_desv,self.n_rotuloX_desv = askEntrytick(self.janelaprincipal,'X',self.Dado_config.getSizeLabelsTick_X('Desvio'),self.Dado_config.getWidthTickMajor_X('Desvio'),self.Dado_config.getHeightTickMajor_X('Desvio'),self.Dado_config.getWidthTickMinor_X('Desvio'),self.Dado_config.getHeightTickMinor_X('Desvio'),self.minX_desv,self.maxX_desv,self.tela_graf)
			if not self.minX_desv: self.minX_desv = self.min_ori_X
			if not self.maxX_desv: self.maxX_desv = self.max_ori_X
			if self.passo_tickX_desv:
				[img_ax.xaxis.get_major_ticks()[-1].set_visible(True) for img_ax in self.img_axes[-1][:-1]]
				delta_ult = 0
				for ax in self.img_axes[-1]:
					lisa_ticklb_X = np.arange(self.minX_desv,self.maxX_desv+self.passo_tickX_desv,self.passo_tickX_desv)
					delta_ult =  self.maxX_desv - lisa_ticklb_X[-1]
					ax.xaxis.set_major_locator(ticker.FixedLocator(lisa_ticklb_X))
				if delta_ult < 6.0:
					[img_ax.xaxis.get_major_ticks()[-1].set_visible(False) for img_ax in self.img_axes[-1][:-1]]
			elif self.n_rotuloX_desv:
				[img_ax.xaxis.get_major_ticks()[-1].set_visible(True) for img_ax in self.img_axes[-1][:-1]]
				[img_ax.xaxis.set_major_locator(ticker.LinearLocator(round(self.n_rotuloX_desv))) for img_ax in self.img_axes[-1]]
				[img_ax.xaxis.get_major_ticks()[-1].set_visible(False) for img_ax in self.img_axes[-1][:-1]]
			[img_ax.set_xlim(self.minX_desv,self.maxX_desv) for l_img_ax in self.img_axes for img_ax in l_img_ax]
			[img_ax.tick_params(axis='x', which='major', width=float(L_MJ_x),size=float(A_MJ_x),labelsize=float(tam_x)) for l_img_ax in self.img_axes for img_ax in l_img_ax ]
			[img_ax.tick_params(axis='x', which='minor', width=float(L_MN_x),size=float(A_MN_x)) for l_img_ax in self.img_axes for img_ax in l_img_ax ]
			self.Dado_config.setConfig_tick_X('Desvio',[tam_x,L_MJ_x,A_MJ_x,L_MN_x,A_MN_x])
			self.pick_axes()

		elif event.artist.get_gid() == "ticks_y_Desvio":
			self.minY_desv,self.maxY_desv = self.img_axes[0][0].get_ylim()
			tam_y,L_MJ_y,A_MJ_y,L_MN_y,A_MN_y,self.minY_desv,self.maxY_desv,self.passo_tickY_desv,self.n_rotuloY_desv = askEntrytick(self.janelaprincipal,'Y',self.Dado_config.getSizeLabelsTick_Y('Desvio'),self.Dado_config.getWidthTickMajor_Y('Desvio'),self.Dado_config.getHeightTickMajor_Y('Desvio'),self.Dado_config.getWidthTickMinor_Y('Desvio'),self.Dado_config.getHeightTickMinor_Y('Desvio'),self.minY_desv,self.maxY_desv,self.tela_graf)
			if not self.minY_desv: self.minY_desv = self.min_ori_Y
			if not self.maxY_desv: self.maxY_desv = self.max_ori_Y
			if self.passo_tickY_desv:
				[img_ax[0].yaxis.get_major_ticks()[-1].set_visible(True) for img_ax in self.img_axes[1:]]
				delta_ult = 0
				for ax in self.img_axes:
					lisa_ticklb_Y = np.arange(self.minY_desv,self.maxY_desv,self.passo_tickY_desv)
					delta_ult =  self.maxY_desv - lisa_ticklb_Y[-1]
					ax[0].yaxis.set_major_locator(ticker.FixedLocator(lisa_ticklb_Y))
				if delta_ult < 6.0:
					[img_ax[0].yaxis.get_major_ticks()[-1].set_visible(False) for img_ax in self.img_axes[1:]]
			elif self.n_rotuloY_desv:
				[img_ax[0].yaxis.get_major_ticks()[-1].set_visible(True) for img_ax in self.img_axes[1:]]
				[img_ax[0].yaxis.set_major_locator(ticker.LinearLocator(round(self.n_rotuloY_desv))) for img_ax in self.img_axes]
				[img_ax[0].yaxis.get_major_ticks()[-1].set_visible(False) for img_ax in self.img_axes[1:]]
			[img_ax.set_ylim(self.minY_desv,self.maxY_desv) for l_img_ax in self.img_axes for img_ax in l_img_ax]
			[img_ax.tick_params(axis='y', which='major', width=float(L_MJ_y),size=float(A_MJ_y),labelsize=float(tam_y)) for l_img_ax in self.img_axes for img_ax in l_img_ax]
			[img_ax.tick_params(axis='y', which='minor', width=float(L_MN_y),size=float(A_MN_y)) for l_img_ax in self.img_axes for img_ax in l_img_ax]
			self.Dado_config.setConfig_tick_Y('Desvio',[tam_y,L_MJ_y,A_MJ_y,L_MN_y,A_MN_y])
			self.pick_axes()



		elif event.artist.get_gid() == "titulo_graph_Eia":
			titulo_atual = event.artist.get_text()
			self.titulo_graph_EIA,self.rfont_titulo_graph_EIA = askEntry(self.janelaprincipal,self.Dado_config.idioma(170),titulo_atual,self.rfont_titulo_graph_EIA,self.tela_graf)
			if self.rfont_titulo_graph_EIA:
				self.img_axes.set_title(self.titulo_graph_EIA,**self.rfont_titulo_graph_EIA)
			elif titulo_atual != self.titulo_graph_EIA:
				self.img_axes.set_title(self.titulo_graph_EIA)

		elif event.artist.get_gid() == "y_label_graph_Eia":
			titulo_atual = event.artist.get_text()
			self.titulo_axe_y_EIA,self.rfont_titulo_axe_y_EIA = askEntry(self.janelaprincipal,"LABEL Y",titulo_atual,self.rfont_titulo_axe_y_EIA,self.tela_graf)
			if self.rfont_titulo_axe_y_EIA:
				self.img_axes.set_ylabel(self.titulo_axe_y_EIA,**self.rfont_titulo_axe_y_EIA)
			elif titulo_atual != self.titulo_axe_y_EIA:
				self.img_axes.set_ylabel(self.titulo_axe_y_EIA)

		elif event.artist.get_gid() == "x_label_graph_Eia":
			titulo_atual = event.artist.get_text()
			self.titulo_axe_x_EIA,self.rfont_titulo_axe_x_EIA = askEntry(self.janelaprincipal,"LABEL X",titulo_atual,self.rfont_titulo_axe_x_EIA,self.tela_graf)
			if self.rfont_titulo_axe_x_EIA:
				self.img_axes.set_xlabel(self.titulo_axe_x_EIA,**self.rfont_titulo_axe_x_EIA)
			elif titulo_atual != self.titulo_axe_x_EIA:
				self.img_axes.set_xlabel(self.titulo_axe_x_EIA)

		elif event.artist.get_gid() == "label_bar_graph_Eia":
			titulo_atual = event.artist.get_text()
			self.titulo_bar_EIA,self.rfont_titulo_bar_EIA = askEntry(self.janelaprincipal,self.Dado_config.idioma(169),titulo_atual,self.rfont_titulo_bar_EIA,self.tela_graf)
			if self.rfont_titulo_bar_EIA:
				self.img_cbar.ax.set_title(self.titulo_bar_EIA,**self.rfont_titulo_bar_EIA)
			elif titulo_atual != self.titulo_bar_EIA:
				self.img_cbar.ax.set_title(self.titulo_bar_EIA)

		elif event.artist.get_gid() == "tick_bar_graph_Eia":
			tick_atual = self.img_cbar.vmax
			self.tick_bar_EIA = askEntry(self.janelaprincipal,"Max Vtec",tick_atual, self.rfont_titulo_bar_EIA, self.tela_graf,False)
			
			if self.tick_bar_EIA and tick_atual != self.tick_bar_EIA:
				self.tick_bar_EIA = (''.join(x for x in self.tick_bar_EIA if x.isdecimal() or x == "." or x== ",")).replace(",",".")
				self.vm = float(self.tick_bar_EIA)
				self.plot()

		elif event.artist.get_gid() == "ticks_y_Eia":
			self.minY_EIA,self.maxY_EIA = self.img_axes.get_ylim()
			tam_y,L_MJ_y,A_MJ_y,L_MN_y,A_MN_y,self.minY_EIA,self.maxY_EIA,self.passo_tickY_EIA,self.n_rotuloY_EIA = askEntrytick(self.janelaprincipal,'Y',self.Dado_config.getSizeLabelsTick_Y('Eia'),self.Dado_config.getWidthTickMajor_Y('Eia'),self.Dado_config.getHeightTickMajor_Y('Eia'),self.Dado_config.getWidthTickMinor_Y('Eia'),self.Dado_config.getHeightTickMinor_Y('Eia'),self.minY_EIA,self.maxY_EIA,self.tela_graf)
			if not self.minY_EIA: self.minY_EIA = self.min_ori_Y
			if not self.maxY_EIA: self.maxY_EIA = self.max_ori_Y
			if self.passo_tickY_EIA:
				self.img_axes.yaxis.set_major_locator(ticker.IndexLocator(base=(self.passo_tickY_EIA), offset=self.minY_EIA))
			elif self.n_rotuloY_EIA:
				self.img_axes.yaxis.set_major_locator(ticker.LinearLocator(round(self.n_rotuloY_EIA)))
			self.img_axes.set_ylim(self.minY_EIA,self.maxY_EIA)
			self.img_axes.tick_params(axis='y', which='major', width=float(L_MJ_y),size=float(A_MJ_y),labelsize=float(tam_y))
			self.img_axes.tick_params(axis='y', which='minor', width=float(L_MN_y),size=float(A_MN_y))
			self.Dado_config.setConfig_tick_Y('Eia',[tam_y,L_MJ_y,A_MJ_y,L_MN_y,A_MN_y])
			self.pick_axes()

		elif event.artist.get_gid() == "ticks_x_Eia":
			self.minX_EIA,self.maxX_EIA = self.img_axes.get_xlim()
			tam_x,L_MJ_x,A_MJ_x,L_MN_x,A_MN_x,self.minX_EIA,self.maxX_EIA,self.passo_tickX_EIA,self.n_rotuloX_EIA = askEntrytick(self.janelaprincipal,'X',self.Dado_config.getSizeLabelsTick_X('Eia'),self.Dado_config.getWidthTickMajor_X('Eia'),self.Dado_config.getHeightTickMajor_X('Eia'),self.Dado_config.getWidthTickMinor_X('Eia'),self.Dado_config.getHeightTickMinor_X('Eia'),self.minX_EIA,self.maxX_EIA,self.tela_graf)
			if not self.minX_EIA: self.minX_EIA = self.min_ori_X
			if not self.maxX_EIA: self.maxX_EIA = self.max_ori_X
			if self.passo_tickX_EIA:
				self.img_axes.xaxis.set_major_locator(ticker.IndexLocator(base=(self.passo_tickX_EIA), offset=self.minX_EIA))
			elif self.n_rotuloX_EIA:
				self.img_axes.xaxis.set_major_locator(ticker.LinearLocator(round(self.n_rotuloX_EIA)))
			self.img_axes.set_xlim(self.minX_EIA,self.maxX_EIA)
			self.img_axes.tick_params(axis='x', which='major', width=float(L_MJ_x),size=float(A_MJ_x),labelsize=float(tam_x))
			self.img_axes.tick_params(axis='x', which='minor', width=float(L_MN_x),size=float(A_MN_x))
			self.Dado_config.setConfig_tick_X('Eia',[tam_x,L_MJ_x,A_MJ_x,L_MN_x,A_MN_x])
			self.pick_axes()



		elif event.artist.get_gid() == "titulo_graph_Setor":
			titulo_atual = event.artist.get_text()
			self.titulo_graph_setor,self.rfont_titulo_graph_setor = askEntry(self.janelaprincipal,self.Dado_config.idioma(170),titulo_atual,self.rfont_titulo_graph_setor,self.tela_graf)

			if self.rfont_titulo_graph_setor:
				self.img_axes.set_title(self.titulo_graph_setor,**self.rfont_titulo_graph_setor)
			elif titulo_atual != self.titulo_graph_setor:
				self.img_axes.set_title(self.titulo_graph_setor)

		elif event.artist.get_gid() == "y_label_graph_Setor":
			titulo_atual = event.artist.get_text()
			self.titulo_axe_y_setor,self.rfont_titulo_axe_y_setor = askEntry(self.janelaprincipal,"LABEL Y",titulo_atual,self.rfont_titulo_axe_y_setor,self.tela_graf)
			if self.rfont_titulo_axe_y_setor:
				self.img_axes.set_ylabel(self.titulo_axe_y_setor,**self.rfont_titulo_axe_y_setor)
			elif titulo_atual != self.titulo_axe_y_setor:
				self.img_axes.set_ylabel(self.titulo_axe_y_setor)

		elif event.artist.get_gid() == "x_label_graph_Setor":
			titulo_atual = event.artist.get_text()
			self.titulo_axe_x_setor,self.rfont_titulo_axe_x_setor = askEntry(self.janelaprincipal,"LABEL X",titulo_atual,self.rfont_titulo_axe_x_setor,self.tela_graf)
			if self.rfont_titulo_axe_x_setor:
				self.img_axes.set_xlabel(self.titulo_axe_x_setor,**self.rfont_titulo_axe_x_setor)
			elif titulo_atual != self.titulo_axe_x_setor:
				self.img_axes.set_xlabel(self.titulo_axe_x_setor)

		elif event.artist.get_gid() == "label_bar_graph_Setor":
			titulo_atual = event.artist.get_text()
			self.titulo_bar_setor,self.rfont_titulo_bar_setor = askEntry(self.janelaprincipal,self.Dado_config.idioma(169),titulo_atual,self.rfont_titulo_bar_setor,self.tela_graf)
			if self.rfont_titulo_bar_setor:
				self.img_cbar.ax.set_title(self.titulo_bar_setor,**self.rfont_titulo_bar_setor)
			elif titulo_atual != self.titulo_bar_setor:
				self.img_cbar.ax.set_title(self.titulo_bar_setor)

		elif event.artist.get_gid() == "tick_bar_graph_Setor":
			tick_atual = self.img_cbar.vmax
			self.tick_bar_setor = askEntry(self.janelaprincipal,"Max Vtec",tick_atual, self.rfont_titulo_bar_setor, self.tela_graf,False)
			
			if self.tick_bar_setor and tick_atual != self.tick_bar_setor:
				self.tick_bar_setor = (''.join(x for x in self.tick_bar_setor if x.isdecimal() or x == "." or x== ",")).replace(",",".")
				self.vm = float(self.tick_bar_setor)
				self.plot()

		elif event.artist.get_gid() == "ticks_y_Setor":
			self.minY_setor,self.maxY_setor = self.img_axes.get_ylim()
			tam_y,L_MJ_y,A_MJ_y,L_MN_y,A_MN_y,self.minY_setor,self.maxY_setor,self.passo_tickY_setor,self.n_rotuloY_setor = askEntrytick(self.janelaprincipal,'Y',self.Dado_config.getSizeLabelsTick_Y('Setor'),self.Dado_config.getWidthTickMajor_Y('Setor'),self.Dado_config.getHeightTickMajor_Y('Setor'),self.Dado_config.getWidthTickMinor_Y('Setor'),self.Dado_config.getHeightTickMinor_Y('Setor'),self.minY_setor,self.maxY_setor,self.tela_graf)
			if not self.minY_setor: self.minY_setor = self.min_ori_Y
			if not self.maxY_setor: self.maxY_setor = self.max_ori_Y
			if self.passo_tickY_setor:
				self.img_axes.yaxis.set_major_locator(ticker.IndexLocator(base=(self.passo_tickY_setor), offset=self.minY_setor))
			elif self.n_rotuloY_setor:
				self.img_axes.yaxis.set_major_locator(ticker.LinearLocator(round(self.n_rotuloY_setor)))
			self.img_axes.set_ylim(self.minY_setor,self.maxY_setor)
			self.img_axes.tick_params(axis='y', which='major', width=float(L_MJ_y),size=float(A_MJ_y),labelsize=float(tam_y))
			self.img_axes.tick_params(axis='y', which='minor', width=float(L_MN_y),size=float(A_MN_y))
			self.Dado_config.setConfig_tick_Y('Setor',[tam_y,L_MJ_y,A_MJ_y,L_MN_y,A_MN_y])
			self.pick_axes()

		elif event.artist.get_gid() == "ticks_x_Setor":
			self.minX_setor,self.maxX_setor = self.img_axes.get_xlim()
			tam_x,L_MJ_x,A_MJ_x,L_MN_x,A_MN_x,self.minX_setor,self.maxX_setor,self.passo_tickX_setor,self.n_rotuloX_setor = askEntrytick(self.janelaprincipal,'X',self.Dado_config.getSizeLabelsTick_X('Setor'),self.Dado_config.getWidthTickMajor_X('Setor'),self.Dado_config.getHeightTickMajor_X('Setor'),self.Dado_config.getWidthTickMinor_X('Setor'),self.Dado_config.getHeightTickMinor_X('Setor'),self.minX_setor,self.maxX_setor,self.tela_graf)
			if not self.minX_setor: self.minX_setor = self.min_ori_X
			if not self.maxX_setor: self.maxX_setor = self.max_ori_X
			if self.passo_tickX_setor:
				self.img_axes.xaxis.set_major_locator(ticker.IndexLocator(base=(self.passo_tickX_setor), offset=self.minX_setor))
			elif self.n_rotuloX_setor:
				self.img_axes.xaxis.set_major_locator(ticker.LinearLocator(round(self.n_rotuloX_setor)))
			self.img_axes.set_xlim(self.minX_setor,self.maxX_setor)
			self.img_axes.tick_params(axis='x', which='major', width=float(L_MJ_x),size=float(A_MJ_x),labelsize=float(tam_x))
			self.img_axes.tick_params(axis='x', which='minor', width=float(L_MN_x),size=float(A_MN_x))
			self.Dado_config.setConfig_tick_X('Setor',[tam_x,L_MJ_x,A_MJ_x,L_MN_x,A_MN_x])
			self.pick_axes()




		elif event.artist.get_gid() == "titulo_graph_Individual":
			titulo_atual = event.artist.get_text()
			self.titulo_graph_indv,self.rfont_titulo_graph_indv = askEntry(self.janelaprincipal,self.Dado_config.idioma(170),titulo_atual,self.rfont_titulo_graph_indv,self.tela_graf)
			if self.rfont_titulo_graph_indv:
				self.img_axes.set_title(self.titulo_graph_indv,**self.rfont_titulo_graph_indv)
			elif titulo_atual != self.titulo_graph_indv:
				self.img_axes.set_title(self.titulo_graph_indv)

		elif event.artist.get_gid() == "y_label_graph_Individual":
			titulo_atual = event.artist.get_text()
			self.titulo_axe_y_indv,self.rfont_titulo_axe_y_indv = askEntry(self.janelaprincipal,"LABEL Y",titulo_atual,self.rfont_titulo_axe_y_indv,self.tela_graf)
			if self.rfont_titulo_axe_y_indv:
				self.img_axes.set_ylabel(self.titulo_axe_y_indv,**self.rfont_titulo_axe_y_indv)
			elif titulo_atual != self.titulo_axe_y_indv:
				self.img_axes.set_ylabel(self.titulo_axe_y_indv)

		elif event.artist.get_gid() == "x_label_graph_Individual":
			titulo_atual = event.artist.get_text()
			self.titulo_axe_x_indv,self.rfont_titulo_axe_x_indv = askEntry(self.janelaprincipal,"LABEL X",titulo_atual,self.rfont_titulo_axe_x_indv,self.tela_graf)
			if self.rfont_titulo_axe_x_indv:
				self.img_axes.set_xlabel(self.titulo_axe_x_indv,**self.rfont_titulo_axe_x_indv)
			elif titulo_atual != self.titulo_axe_x_indv:
				self.img_axes.set_xlabel(self.titulo_axe_x_indv)

		elif event.artist.get_gid() == "label_bar_graph_Individual":
			titulo_atual = event.artist.get_text()
			self.titulo_bar_indv,self.rfont_titulo_bar_indv = askEntry(self.janelaprincipal,self.Dado_config.idioma(169),titulo_atual,self.rfont_titulo_bar_indv,self.tela_graf)
			if self.rfont_titulo_bar_indv:
				self.img_cbar.ax.set_title(self.titulo_bar_indv,**self.rfont_titulo_bar_indv)
			elif titulo_atual != self.titulo_bar_indv:
				self.img_cbar.ax.set_title(self.titulo_bar_indv)

		elif event.artist.get_gid() == "tick_bar_graph_Individual":
			tick_atual = self.img_cbar.vmax
			self.tick_bar_indv = askEntry(self.janelaprincipal,"Max Vtec",tick_atual,self.rfont_titulo_bar_indv,self.tela_graf,False)
			if self.tick_bar_indv and tick_atual != self.tick_bar_indv:
				self.tick_bar_indv = (''.join(x for x in self.tick_bar_indv if x.isdecimal() or x == "." or x== ",")).replace(",",".")
				self.vm = float(self.tick_bar_indv)
				self.plot()

		elif event.artist.get_gid() == "ticks_x_Individual":
			self.minX_indv,self.maxX_indv = self.img_axes.get_xlim()
			try:
				if self.minX_indv < 0:minX_indv_dia = self.minX_indv + int(self.matrizdias_indv[0][1])
				else:minX_indv_dia = int(self.matrizdias_indv[int(self.minX_indv)][1])
			except IndexError:
				minX_indv_dia = int(self.minX_indv) + int(self.matrizdias_indv[0][1])
			try:
				maxX_indv_dia = int(self.matrizdias_indv[int(self.maxX_indv)][1])
			except IndexError:
				maxX_indv_dia = int(self.maxX_indv) + int(self.matrizdias_indv[0][1])

			tam_x,L_MJ_x,A_MJ_x,L_MN_x,A_MN_x,self.minX_indv,self.maxX_indv,self.passo_tickX_indv,self.n_rotuloX_indv = askEntrytick(self.janelaprincipal,'X',self.Dado_config.getSizeLabelsTick_X('Individual'),self.Dado_config.getWidthTickMajor_X('Individual'),self.Dado_config.getHeightTickMajor_X('Individual'),self.Dado_config.getWidthTickMinor_X('Individual'),self.Dado_config.getHeightTickMinor_X('Individual'),minX_indv_dia,maxX_indv_dia,self.tela_graf)
			self.minX_indv-=int(self.matrizdias_indv[0][1]);self.maxX_indv-=int(self.matrizdias_indv[0][1])
			if not self.minX_indv: self.minX_indv = self.min_ori_X
			if not self.maxX_indv: self.maxX_indv = self.max_ori_X
			if self.passo_tickX_indv:
				self.img_axes.xaxis.set_major_locator(ticker.IndexLocator(base=(self.passo_tickX_indv), offset=self.minX_indv))
			elif self.n_rotuloX_indv:
				self.img_axes.xaxis.set_major_locator(ticker.LinearLocator(round(self.n_rotuloX_indv)))
			
			self.img_axes.set_xlim(self.minX_indv,self.maxX_indv)
			
			self.img_axes.tick_params(axis='x', which='major', width=float(L_MJ_x),size=float(A_MJ_x),labelsize=float(tam_x))
			self.img_axes.tick_params(axis='x', which='minor', width=float(L_MN_x),size=float(A_MN_x))


			self.Dado_config.setConfig_tick_X('Individual',[tam_x,L_MJ_x,A_MJ_x,L_MN_x,A_MN_x])
			self.pick_axes()

		elif event.artist.get_gid() == "ticks_y_Individual":
			self.minY_indv,self.maxY_indv = self.img_axes.get_ylim()
			self.minY_indv /=60;self.maxY_indv /= 60
			tam_y,L_MJ_y,A_MJ_y,L_MN_y,A_MN_y,self.minY_indv,self.maxY_indv,self.passo_tickY_indv,self.n_rotuloY_indv = askEntrytick(self.janelaprincipal,'Y',self.Dado_config.getSizeLabelsTick_Y('Individual'),self.Dado_config.getWidthTickMajor_Y('Individual'),self.Dado_config.getHeightTickMajor_Y('Individual'),self.Dado_config.getWidthTickMinor_Y('Individual'),self.Dado_config.getHeightTickMinor_Y('Individual'),self.minY_indv,self.maxY_indv,self.tela_graf)
			if not self.minY_indv: self.minY_indv = self.min_ori_Y
			if not self.maxY_indv: self.maxY_indv = self.max_ori_Y
			self.minY_indv*=60;self.maxY_indv*=60
			if self.passo_tickY_indv:
				self.passo_tickY_indv*=60
				self.img_axes.yaxis.set_major_locator(ticker.IndexLocator(base=(self.passo_tickY_indv), offset=self.minY_indv))
			elif self.n_rotuloY_indv:
				self.img_axes.yaxis.set_major_locator(ticker.LinearLocator(round(self.n_rotuloY_indv)))
			self.img_axes.set_ylim(self.minY_indv,self.maxY_indv)
			self.img_axes.tick_params(axis='y', which='major', width=float(L_MJ_y),size=float(A_MJ_y),labelsize=float(tam_y))
			self.img_axes.tick_params(axis='y', which='minor', width=float(L_MN_y),size=float(A_MN_y))
			self.img_cbar.ax.tick_params(axis='y', which='major', width=float(L_MJ_y),size=float(A_MJ_y),labelsize=float(tam_y))

			self.Dado_config.setConfig_tick_Y('Individual',[tam_y,L_MJ_y,A_MJ_y,L_MN_y,A_MN_y])
			self.pick_axes()



		elif event.artist.get_gid() == "titulo_graph_Rot":
			titulo_atual = event.artist.get_text()
			self.titulo_graph_rot,self.rfont_titulo_graph_rot = askEntry(self.janelaprincipal,self.Dado_config.idioma(170),titulo_atual,self.rfont_titulo_graph_rot,self.tela_graf)
			if self.rfont_titulo_graph_rot:
				self.img_axes.set_title(self.titulo_graph_rot,**self.rfont_titulo_graph_rot)
			elif titulo_atual != self.titulo_graph_rot:
				self.img_axes.set_title(self.titulo_graph_rot)
		elif event.artist.get_gid() == "y_label_graph_Rot":

			titulo_atual = event.artist.get_text()
			self.titulo_axe_y_rot,self.rfont_titulo_axe_y_rot = askEntry(self.janelaprincipal,"LABEL Y",titulo_atual,self.rfont_titulo_axe_y_rot,self.tela_graf)
			if self.rfont_titulo_axe_y_rot:
   				self.img_axes.set_ylabel(self.titulo_axe_y_rot,**self.rfont_titulo_axe_y_rot)
			elif self.titulo_axe_y_rot != titulo_atual:
				self.img_axes.set_ylabel(self.titulo_axe_y_rot)

			
			
			
			
			
			

		elif event.artist.get_gid() == "x_label_graph_Rot":
			titulo_atual = event.artist.get_text()
			self.titulo_axe_x_rot,self.rfont_titulo_axe_x_rot = askEntry(self.janelaprincipal,"LABEL X",titulo_atual,self.rfont_titulo_axe_x_rot,self.tela_graf)
			if self.rfont_titulo_axe_x_rot:
				self.img_axes.set_xlabel(self.titulo_axe_x_rot,**self.rfont_titulo_axe_x_rot)
			elif titulo_atual != self.titulo_axe_x_rot:
				self.img_axes.set_xlabel(self.titulo_axe_x_rot)

		elif event.artist.get_gid() == "ticks_x_Rot":
			self.minX_rot,self.maxX_rot = self.img_axes.get_xlim()
			tam_x,L_MJ_x,A_MJ_x,L_MN_x,A_MN_x,self.minX_rot,self.maxX_rot,self.passo_tickX_rot,self.n_rotuloX_rot = askEntrytick(self.janelaprincipal,'X',self.Dado_config.getSizeLabelsTick_X('Rot'),self.Dado_config.getWidthTickMajor_X('Rot'),self.Dado_config.getHeightTickMajor_X('Rot'),self.Dado_config.getWidthTickMinor_X('Rot'),self.Dado_config.getHeightTickMinor_X('Rot'),self.minX_rot,self.maxX_rot,self.tela_graf)
			if self.minX_rot == None: self.minX_rot = self.min_ori_X
			if self.maxX_rot == None: self.maxX_rot = self.max_ori_X
			if self.passo_tickX_rot:
				self.img_axes.xaxis.set_major_locator(ticker.IndexLocator(base=(self.passo_tickX_rot), offset=self.minX_rot))
			elif self.n_rotuloX_rot:
				self.img_axes.xaxis.set_major_locator(ticker.LinearLocator(round(self.n_rotuloX_rot)))
			self.img_axes.set_xlim(self.minX_rot,self.maxX_rot)
			self.img_axes.tick_params(axis='x', which='major', width=float(L_MJ_x),size=float(A_MJ_x),labelsize=float(tam_x))
			self.img_axes.tick_params(axis='x', which='minor', width=float(L_MN_x),size=float(A_MN_x))
			self.Dado_config.setConfig_tick_X('Rot',[tam_x,L_MJ_x,A_MJ_x,L_MN_x,A_MN_x])
			self.pick_axes()

		elif event.artist.get_gid() == "ticks_y_Rot":
			self.minY_rot,self.maxY_rot = self.img_axes.get_ylim()
			self.minY_rot /= 10; self.maxY_rot /= 10
			tam_y,L_MJ_y,A_MJ_y,L_MN_y,A_MN_y,self.minY_rot,self.maxY_rot,self.passo_tickY_rot,self.n_rotuloY_rot = askEntrytick(self.janelaprincipal,'Y',self.Dado_config.getSizeLabelsTick_Y('Rot'),self.Dado_config.getWidthTickMajor_Y('Rot'),self.Dado_config.getHeightTickMajor_Y('Rot'),self.Dado_config.getWidthTickMinor_Y('Rot'),self.Dado_config.getHeightTickMinor_Y('Rot'),self.minY_rot,self.maxY_rot,self.tela_graf)
			if self.minY_rot == None:
				self.minY_rot = self.min_ori_Y
			if self.maxY_rot == None:
				self.maxY_rot = self.max_ori_Y
			self.minY_rot *= 10; self.maxY_rot *= 10
			if self.passo_tickY_rot:
				
				self.img_axes.yaxis.set_major_locator(ticker.FixedLocator([(pr * 10) for pr in np.arange(self.prn[0],((self.prn[-1]) + 1),self.passo_tickY_rot)]))
			elif self.n_rotuloY_rot:
				self.img_axes.yaxis.set_major_locator(ticker.LinearLocator(round(self.n_rotuloY_rot)))

			self.img_axes.set_ylim(self.minY_rot,self.maxY_rot)
			self.img_axes.tick_params(axis='y', which='major', width=float(L_MJ_y),size=float(A_MJ_y),labelsize=float(tam_y))
			self.img_axes.tick_params(axis='y', which='minor', width=float(L_MN_y),size=float(A_MN_y))
			self.Dado_config.setConfig_tick_Y('Rot',[tam_y,L_MJ_y,A_MJ_y,L_MN_y,A_MN_y])
			self.pick_axes()


		elif event.artist.get_gid() == "tick_bar_graph_model_map":
			tick_atual = self.cbar_model_map.vmax
			self.tick_bar_model_map = askEntry(self.janelaprincipal,"Max Vtec",tick_atual,self.rfont_titulo_bar_model_map,self.tela_graf,False)
			if self.tick_bar_model_map and tick_atual != self.tick_bar_model_map:
				self.tick_bar_model_map = (''.join(x for x in self.tick_bar_model_map if x.isdecimal() or x == "." or x== ",")).replace(",",".")
				self.vm = float(self.tick_bar_model_map)
				self.modelo_mapa()

		elif event.artist.get_gid() == "label_bar_graph_model_map":
			titulo_atual = event.artist.get_text()
			self.titulo_bar_model_map, self.rfont_titulo_bar_model_map = askEntry(self.janelaprincipal,self.Dado_config.idioma(169),titulo_atual,self.rfont_titulo_bar_model_map,self.tela_graf)
			if self.rfont_titulo_bar_model_map:
				self.cbar_model_map.ax.set_title(self.titulo_bar_model_map,**self.rfont_titulo_bar_model_map)
			elif titulo_atual != self.titulo_bar_model_map:
				self.cbar_model_map.ax.set_title(self.titulo_bar_model_map)

		self.Dado_config.writeConfig()
		self.refreshCanvas()


	def check_index(self,element):
		try:
			index = [iten[:4] for iten in self.listaobs.get(0, "end")].index(element)
			return index
		except ValueError:
			index = -1 
			return index

	def Set_map(self,*event):

		cbg_loc_g = self.lista_loc[self.n_lista_loc.index(self.cbg_loc_value.get())]
		la = cbg_loc_g[1].split(' ')
		lo = cbg_loc_g[2].split(' ')
		self.ax_map.set_ylim(int(la[0]),int(la[1]))
		self.ax_map.set_xlim(int(lo[0]),int(lo[1]))
		plt.tight_layout(pad=0)
		self.fig_map.canvas.mpl_connect('pick_event', self.on_click_map)
		self.Dado_config.setMapa(self.cbg_loc_value.get())
		self.fig_map.canvas.draw()

		
		
		
		
		
		

	def Set_menu_rap(self,*event):

		
		

    		
		self.Menu = True
		
		self.Frame_prop_rap_INDV.pack_forget()
		self.Frame_prop_rap_SETOR.pack_forget()
		self.Frame_prop_rap_EIA.pack_forget()
		self.Frame_prop_rap_DESVIO.pack_forget()
		self.Frame_prop_rap_MAPA.pack_forget()
		self.Frame_prop_rap_ROT.pack_forget()

		if self.cbg_value.get() == "Individual (STD)":
			self.clear_list_and_plot()
			self.Frame_prop_rap_INDV.pack(  # CONVERT_PACKfill='x')
			self.listaobs.config(selectmode="single")

		elif self.cbg_value.get() == "Setor (STD)":
			
			self.Frame_prop_rap_SETOR.pack(  # CONVERT_PACKfill='x')
			self.listaobs.configure(selectmode="multiple")

		elif self.cbg_value.get() == "EIA (STD)":
			
			self.Frame_prop_rap_EIA.pack(  # CONVERT_PACKfill='x')
			self.listaobs.configure(selectmode="multiple")

		elif self.cbg_value.get() == "Desvio (STD)":
			
			self.Frame_prop_rap_DESVIO.pack(  # CONVERT_PACKfill='x')
			self.listaobs.configure(selectmode="multiple")

		elif self.cbg_value.get() == "Mapa (CMN)":
			self.clear_list_and_plot()
			self.listaobs.configure(selectmode="single")
			self.Frame_prop_rap_MAPA.pack(  # CONVERT_PACKfill='x')


		elif self.cbg_value.get() == "ROT (CMN)":
			self.clear_list_and_plot()
			self.Frame_prop_rap_ROT.pack(  # CONVERT_PACKfill='x')
			self.listaobs.config(selectmode="single")

		if len(self.listaobs.get(0).split(',')) == 2 and self.cbg_value.get():
			self.clear_list_and_plot()
			try:
				nt_lista,self.conteudo_lista = self.uti.Refresh_list_obs(self.filedir,int(self.Data_Entry.get()[-4:]),self.check_filter_v.get(),True)
			except (ValueError, TypeError, IndexError):
				self.conteudo_lista = self.uti.Refresh_list_obs(self.filedir,int(self.Data_Entry.get()[-4:]),self.check_filter_v.get(),True)[0]
				nt_lista = []
			
			self.listaobs.delete(0,END)
			self.cont_est_select.set(0)
			[self.listaobs.insert(END, item) for item in self.conteudo_lista]
			[self.listaobs.insert(END, item + " ("+ self.Dado_config.idioma(144) +")") for item in nt_lista]
			
			
			
			
			
			
			
			
			
			self.plot_linha_eq_mag(int(self.Data_Entry.get()[-4:]))
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			self.fig_map.canvas.draw()


	def clear_list_and_plot(self):
		self.un_sel(self.current_plot)
		self.listaobs.select_clear(0, 'end')
		self.cont_est_select.set(0)
		try:
			for item_id in list(self.list_id):
				self.un_sel(self.lista_plots[self.uti.list_duplicates_of(self.lista_plots_label,self.listaobs.get(item_id)[:4])[0]])
		except (AttributeError,TypeError):
			pass
		self.current_plot = ""
		self.list_id = []

	
	
	

	def selecionar(self, file = None, dip = None):
		if not file:file = askdirectory(initialdir="c:/",title = self.Dado_config.idioma(40),parent=self.janelaprincipal)
		if file:
			self.clear_list_and_plot()
			self.filedir = file
			
			if self.Menu: dip = True
			nt_lista = []
			
			if self.check_filter_v.get(): nt_lista,self.conteudo_lista = self.uti.Refresh_list_obs(self.filedir,int(self.Data_Entry.get()[-4:]),self.check_filter_v.get(),dip)
			
			else:self.conteudo_lista = self.uti.Refresh_list_obs(self.filedir,int(self.Data_Entry.get()[-4:]),self.check_filter_v.get(),dip)[0]
			
			self.dir_string.set(self.filedir)

			ToolTip.createToolTip(self.lbl_dir,self.filedir)

			self.lbl_dir.config(bg="white")
			
			self.listaobs.delete(0,END)
			self.cont_est_select.set(0)
			[self.listaobs.insert(END, item) for item in self.conteudo_lista]
			[self.listaobs.insert(END, item + " ("+ self.Dado_config.idioma(144) +")") for item in nt_lista]
			try:
				for plot,text in zip(self.lista_plots,self.lista_plots_text):
					plot.remove()
					text.remove()
			except (AttributeError,ValueError):
				pass
			if self.conteudo_lista:
				self.lista_plots = []
				self.lista_plots_label = []
				self.lista_plots_text = []


				
				

				for conteudo_obs in self.conteudo_lista:
					inf = (conteudo_obs.replace('(','')).replace(')','')
					item_line = inf.split(",")
					N_L = item_line[0].split(' ')
					lat = (item_line[1].strip()).split(' ')
					Lat_c = self.uti.DMDDEC(int(lat[0]),int(lat[1]))
					Long_c = self.uti.DMDDEC(int(N_L[1]),int(N_L[2]))
					Lat_c,Long_c = self.map(Lat_c,Long_c)
					sct = self.map.scatter(Lat_c,Long_c,color='red',picker=2,s=20,norm=1,gid="station",label=N_L[0],zorder=3)
					self.lista_plots.append(sct)
					self.lista_plots_text.append(plt.text(Lat_c, Long_c,N_L[0],fontsize=7, color='K'))
					self.lista_plots_label.append(self.lista_plots[-1].get_label())
				self.cbg.config(values=['Individual (STD)','Setor (STD)','EIA (STD)','Desvio (STD)','Mapa (CMN)','ROT (CMN)'])
				self.cbg.config(state='readonly')
				self.Set_menu_rap()
				cort_list = [item[5:] for item in self.conteudo_lista]
				itens_rep = self.uti.FindDuplicates(cort_list)
				if itens_rep:
					info = ['-'*88]
					for rp in itens_rep:
						rp_pos = self.uti.list_duplicates_of(cort_list,rp)
						for pos in rp_pos:
							info.append((self.conteudo_lista[pos]))
						info.append('-'*88)
					qtSimpleDialog.Dialog(self.janelaprincipal,self.Dado_config.idioma(145)+": "+self.Dado_config.idioma(146),info,self.uti.resource_path('icone.ico'))
			else:
				self.Frame_prop_rap_INDV.pack_forget()
				self.Frame_prop_rap_SETOR.pack_forget()
				self.Frame_prop_rap_DESVIO.pack_forget()
				self.cbg.config(values=['Individual (STD)'])
				self.cbg.config(state='readonly')
				self.cbg_value.set("")
			self.janelaprincipal.bind("<Up>",lambda e: self.uti.up_lista(self.listaobs))  # CONVERT_BIND
			self.janelaprincipal.bind("<Down>",lambda e: self.uti.down_lista(self.listaobs))  # CONVERT_BIND
			self.Dado_config.setLocalSTD(self.filedir)
			self.fig_map.canvas.draw()

	def restart_program(self):
		"""Restarts the current program.
		Note: this function does not return. Any cleanup action (like
		saving data) must be done before calling this function."""
		os.execl(sys.executable, 'python', __file__, *sys.argv)

	def setarIDI(self,id):
		if messagebox.askokcancel(self.Dado_config.idioma(145),self.Dado_config.idioma(147),parent=self.janelaprincipal):
			self.Dado_config.setIdioma(id)
			self.Dado_config.writeConfig()
			os.execl(sys.executable, sys.executable, *sys.argv)

	def xama(self,id):
		root.withdraw()
		if id == 1:
			frm = Ordena(root)
		elif id == 3:
			frm = Geradordeinclinacao(root)
		elif id == 4:
			frm = CadObs(root)
		elif id == 5:
			self.lista_loc,self.n_lista_loc = askLOC(root,self.cbg_loc)



if __name__ == "__main__":
	try:
		root = Tk()
		root.geometry('800x600')
		root.state('zoomed')
		root.iconbitmap(Utilitarios().resource_path('icone.ico'))
		root.title(DadoIdioma().idioma(16))
		Principal(root)
		root.mainloop()
	except (Exception) as  e:
		messagebox.showerror("ERRO", "Erro gravado (ERRO.txt)")
		erro = open('ERRO.txt','w+')
		erro.write(str(e)+"\n")
		[erro.write(str(tb)) for tb in  traceback.format_tb(sys.exc_info()[2])]
		erro.close()
