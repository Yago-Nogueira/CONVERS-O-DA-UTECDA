

from matplotlib.backends.backend_qt6agg import NavigationToolbar2QT as NavigationToolbar
from util import DadoIdioma, Utilitarios, VerticalScrolledFrame, thread_with_trace, TopNavigationToolbar
from matplotlib.backends.backend_qt6agg import FigureCanvasQTAgg as FigureCanvas
from EntryBox import askEntry, askEntrytick, askEntryBoxColorBar
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.font_manager import FontProperties
from matplotlib.backend_bases import MouseButton
from matplotlib.textpath import TextPath
from matplotlib.patches import PathPatch
import matplotlib.ticker as mticker
from datetime import datetime,timedelta,date
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
from PIL import Image
from PyQt6.QtGui import QPixmap as PhotoImage
from threading import Thread
import cartopy.crs as ccrs
from matplotlib import cm
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox, QFileDialog
import pandas as pd
import numpy as np

import qtSimpleDialog
import simplekml
import cartopy
import math
import copy
import os
import sys

from comp_GRADE_MAPA import COMP_GRADE_MAPA
from gerardoric import Geradordeinclinacao
from tkcalendar_Days import Calendar
from maskedentry import MaskedWidget
from comp_DESVIO import COMP_DESVIO
from comp_ONDAS import COMP_ONDAS

from qt_calendar import DateEntry
from Balloon_info import ToolTip
from comp_INDV import COMP_INDV
from cadastrarOBS import CadObs
from comp_MAPA import COMP_MAPA
from comp_ROT import COMP_ROT
from comp_EIA import COMP_EIA
from ordena import Ordena
from licença import getli






plt.rc('axes', linewidth=2)
plt.rc('font', weight='bold')




class Main_UTECDA(QWidget):
    def __init__(self, master):
        QWidget.__init__(self, master)


        self.uti = Utilitarios()
        self.uti.center_to_two_monitor(self.master)


        self.master.protocol("WM_DELETE_WINDOW", self.Quit_Program)

        self.GRAFICO_Desvio = None
        self.GRAFICO_Eia = None
        self.GRAFICO_Setor = None
        self.GRAFICO_Individual = None
        self.GRAFICO_Mapa = None
        self.GRAFICO_Rot = None
        self.ID_Connection_MPL_CANVAS_MAPA_TOPLEVEL_ROT_LINHAS = None
        self.plot_ATIVO = None

        self.MAPA = None

        self.habilitar_DIP_lista_estacoes = tk.BooleanVar(self)
        self.habilitar_DIP_lista_estacoes.set(False)
        self.Listas_Estacoes_Cadastradas = []
        self.Lista_Estacoes_NAO_Cadastradas = []
        self.Listas_String_Estacoes_Cadastradas = []
        self.List_Scatter_OBS_Station = []
        self.List_Annotate_OBS_Station = []
        self.List_Selection_Listbx_OBS_Station = []
        self.Linha_Equador_Magnetico_MAPA_PRINCIPAL = None
        self.Menu_de_Propriedades_dos_Graficos_atual = None
        self.ID_Connection_MPL_CANVAS_MAPA_PRINCIPAL = None
        self.data_Inicial_GRAFICO_JANELA_TOPLEVEL_GRAFICO_EIA = None
        self.data_Final_GRAFICO_JANELA_TOPLEVEL_GRAFICO_EIA = None
        self.Value_Mostrar_Estacoes_MAPA_PRINCIPAL = tk.BooleanVar(self)
        self.Value_Mostrar_Estacoes_MAPA_PRINCIPAL.set(True)
        self.stop_thread_MAPA = tk.BooleanVar(self)
        self.stop_thread_PAINEL_MAPA = tk.BooleanVar(self)
        self.Value_Salvar_Figura_JANELA_TOPLEVEL_GRAFICO = tk.BooleanVar(self)
        self.Value_Salvar_Matriz_JANELA_TOPLEVEL_GRAFICO = tk.BooleanVar(self)
        self.filedir = tk.StringVar(self)
        self.Value_Check_Filter = tk.BooleanVar(self)
        self.Value_Check_VIDEO_MAPA = tk.BooleanVar(self)
        self.Value_cb_Local_MAPA = tk.StringVar(self)
        self.Value_DATA_entry_main_inicio = tk.StringVar(self)
        self.Value_DATA_entry_main_fim = tk.StringVar(self)
        self.Value_DATA_entry_main_inicio.set("03/07/2021")
        self.Value_grid_axes_X = tk.BooleanVar(self)
        self.Value_grid_axes_Y = tk.BooleanVar(self)
        self.Value_Line_Cores = tk.BooleanVar(self)
        self.Cont_Line_Horas_JANELA_TOPLEVEL_GRAFICO = 0
        self.Value_Line_Horas_JANELA_TOPLEVEL_GRAFICO = tk.BooleanVar(self)
        self.Value_Lat_Dip_axes_Y = tk.IntVar(self)
        self.Value_Lat_Dip_axes_Y.set(1)
        self.Value_station_on_TICK = tk.BooleanVar(self)
        self.Value_Formato_DATA_Grafico = tk.IntVar(self)
        self.Value_Formato_DATA_Grafico.set(1)
        self.Value_State_Legenda = tk.BooleanVar(self)
        self.Value_State_Legenda.set(0)
        self.String_Label_dir = tk.StringVar(self)
        Value_Caminho_Dir = tk.BooleanVar(self)
        Value_Caminho_Dir.set(False)
        self.dir_documents = os.path.expanduser('~/UTECDA')
        self.License_val = tk.BooleanVar(self)
        self.License_val.set(True)
        self.Cont_Station_Selecionadas_Lista = tk.IntVar(self)
        self.Cont_Station_Selecionadas_Lista.set(0)
        self.varx = tk.IntVar(self)
        self.varx.set(0)
        self.vary = tk.IntVar(self)
        self.vary.set(0)
        self.varabs = tk.IntVar(self)
        self.varabs.set(1)
        self.rots = tk.IntVar(self)
        self.rots.set(1)
        

        cartopy.config['data_dir'] = self.uti.resource_path('cartopy')

        self.master.geometry('800x600')
        self.master.state('zoomed')
        self.master.iconbitmap(self.uti.resource_path('img\icone.ico'))
        self.Dado_config = DadoIdioma()
        self.master.title(self.Dado_config.idioma(16))
        vcmd_get_number = (self.master.register(self.uti.onValidatesigla),'%S', '%s','%d',2,4)
        self.texto=""
        self.texto.set(self.Dado_config.idioma(113))



        self.JANELA_TOPLEVEL_GRAFICO = QDialog(master = self.master)
        self.JANELA_TOPLEVEL_GRAFICO.geometry('800x600')
        self.JANELA_TOPLEVEL_GRAFICO.withdraw()
        self.Popup_TopLevel_Grafico = QMenu(self.JANELA_TOPLEVEL_GRAFICO, tearoff = False)
        self.Popup_TopLevel_Grafico.add_command(label = self.Dado_config.idioma(188), command = self.INSERIR_LINHA_VERTICAL_GRAFICO_JANELA_TOPLEVEL_GRAFICO)
        self.Popup_TopLevel_Grafico.add_command(label = self.Dado_config.idioma(139), command = self.Atualizar_grid_Y_JANELA_TOPLEVEL_GRAFICO)
        self.Popup_TopLevel_Grafico.add_command(label = self.Dado_config.idioma(141), command = self.Atualizar_grid_X_JANELA_TOPLEVEL_GRAFICO)
        self.Popup_TopLevel_Grafico.add_checkbutton(label = self.Dado_config.idioma(25), variable = self.Value_Salvar_Figura_JANELA_TOPLEVEL_GRAFICO, command = self.SALVAR_IMAGEM_DADOS_GRAFICO_JANELA_TOPLEVEL_GRAFICO)
        self.Popup_TopLevel_Grafico.add_checkbutton(label = self.Dado_config.idioma(91), variable = self.Value_Salvar_Matriz_JANELA_TOPLEVEL_GRAFICO, command = self.SALVAR_MATRIZ_DADOS_GRAFICO_JANELA_TOPLEVEL_GRAFICO)
        self.Popup_TopLevel_Grafico.add_separator()
        
        self.Popup_TopLevel_Grafico.add_command(label = self.Dado_config.idioma(26), command = self.AJUSTAR_CANVAS_JANELA_TOPLEVEL_GRAFICO)
        

        self.JANELA_TOPLEVEL_GRAFICO.iconbitmap(self.uti.resource_path('img\icone.ico'))
        self.JANELA_TOPLEVEL_GRAFICO.bind("<Button-3>", self.Do_popup_TopLevel_Grafico)  # CONVERT_BIND
        self.JANELA_TOPLEVEL_GRAFICO.protocol("WM_DELETE_WINDOW", self.close_JANELA_TOPLEVEL_GRAFICO )
        self.FIGURA_TOPLEVEL_GRAFICO, self.AXES_TOPLEVEL_GRAFICO = plt.subplots()
        self.FIGURA_TOPLEVEL_GRAFICO.canvas.mpl_connect('pick_event', self.Thread_Pick_Event_PROPRIEDADES_JANELA_TOPLEVEL_GRAFICO)
        self.CANVAS_JANELA_TOPLEVEL_GRAFICO = FigureCanvas(self.FIGURA_TOPLEVEL_GRAFICO, self.JANELA_TOPLEVEL_GRAFICO)
        self.CANVAS_JANELA_TOPLEVEL_GRAFICO.get_tk_widget().pack(side="bottom", fill="both", expand = True)
        self.NAVIGATIONTOOLBAR_TOPLEVEL_GRAFICO = NavigationToolbar(self.CANVAS_JANELA_TOPLEVEL_GRAFICO, self.JANELA_TOPLEVEL_GRAFICO)
        self.CANVAS_JANELA_TOPLEVEL_GRAFICO._tkcanvas.pack(side="top", fill="both", expand = True)  # CONVERT_PACK


        self.Left_Frame = VerticalScrolledFrame(self, relief="ridge", bd = 2, bg = 'gray')
        QLabel(self.Left_Frame.interior, text = self.Dado_config.idioma(171) ).pack(side="bottom", fill="y")


        principal = QMenu(self)
        menu_ferramentas = QMenu(principal, tearoff = 0)
        menu_ferramentas.add_command(label = self.Dado_config.idioma(4), command = lambda id = 'ordena': self.call_windows(id))
        menu_ferramentas.add_command(label = self.Dado_config.idioma(5), command = lambda id = 'igrf12': self.call_windows(id))
        menu_ferramentas.add_command(label = self.Dado_config.idioma(6), command = lambda id = 'registro_est': self.call_windows(id))
        
        menu_programas = QMenu(principal, tearoff = 0)
        menu_programas.add_cascade(label = self.Dado_config.idioma(8), menu = menu_ferramentas, state = "disabled")
        menu_idioma = QMenu(principal, tearoff = 0)
        menu_idioma.add_command(label = self.Dado_config.idioma(9),command = lambda id = 0:self.setarIDI(id))
        menu_idioma.add_command(label = self.Dado_config.idioma(10),command = lambda id = 1:self.setarIDI(id))
        menu_config = QMenu(principal,tearoff = 0)
        menu_config.add_cascade(label = self.Dado_config.idioma(11), menu = menu_idioma)
        menu_map = QMenu(principal,tearoff = 0)
        
        menu_map.add_checkbutton(label = self.Dado_config.idioma(183), variable = self.Value_Mostrar_Estacoes_MAPA_PRINCIPAL, command = self.start_siglas_mapa)
        menu_map.add_command(label = self.Dado_config.idioma(184),command = self.start_gerar_GOOGLE_KMZ)
        
        self.master.config(menu = principal)
        principal.add_cascade(label = self.Dado_config.idioma(12), menu = menu_programas)
        principal.add_cascade(label = self.Dado_config.idioma(13), menu = menu_config)
        principal.add_cascade(label = self.Dado_config.idioma(182), menu = menu_map)


        try:
            self.uti.teste_licença()
            menu_programas.entryconfig(self.Dado_config.idioma(8), state = "normal")
            self.Left_Frame.pack(  # CONVERT_PACKside="left", fill="both")
            Value_Caminho_Dir.set(True)
        except (IOError,IndexError):
            self.License_val.set(False)
            principal.add_command(label = self.Dado_config.idioma(15), command = lambda j = self.master: getli(self.master))


        if not os.path.exists(("%s/OBS.dat") % (self.dir_documents)): self.uti.setOBS()


        self.Frame_Local_MAPA = QWidget(self.Left_Frame.interior)
        self.Frame_Local_MAPA.pack(  # CONVERT_PACKside="top", fill="both")

        QLabel(self.Frame_Local_MAPA, width = 25, text = self.Dado_config.idioma(157), relief="ridge").pack(side="top", fill="x")

        self.set_VARS_LOCS_MAPA_PRINCIPAL()
        self.MAPA = self.Dado_config.Settings["INTERFACE"]["sMap"]
        if not self.MAPA:self.MAPA = self.Lista_Nomes_Locais[0]
        self.Value_cb_Local_MAPA.set(self.MAPA)

        self.cb_Local_Mapa = tk.ttk.Combobox(self.Frame_Local_MAPA, state = 'readonly', exportselection = False, textvariable = self.Value_cb_Local_MAPA, values = self.Lista_Nomes_Locais)
        self.cb_Local_Mapa.bind("<<ComboboxSelected>>", self.Set_Local_MAPA)  # CONVERT_BIND
        self.cb_Local_Mapa.pack(  # CONVERT_PACKside="top", fill="x")

        QPushButton(self.Left_Frame.interior, text = self.Dado_config.idioma(18), command = self.Selecionar_Dir_Data, relief="ridge").pack(side="top", fill="x")

        self.Label_String_dir = QLabel(self.Left_Frame.interior, width = 40 , anchor="e", textvariable = self.String_Label_dir, relief="ridge")
        self.Label_String_dir.pack(  # CONVERT_PACKfill="x")

        self.frame_filter = QWidget(self.Left_Frame.interior, relief="ridge", bd = 2)
        self.frame_filter.pack(  # CONVERT_PACKside="top", fill="both", expand = True)

        QLabel(self.frame_filter, text = self.Dado_config.idioma(166)).pack(side="left", fill="both", expand = True)
        QCheckBox(self.frame_filter, variable = self.Value_Check_Filter, relief="ridge", bd = 2, width = 5, command = self.Aplicar_Filtro_Dir_station_OBS).pack()
        self.Value_Check_Filter.set(self.Dado_config.Settings["INTERFACE"]["iFiltro"])

        self.Frame_Listbx_Stations_OBS = QWidget(self.Left_Frame.interior)
        self.Frame_Listbx_Stations_OBS.pack(  # CONVERT_PACKside="top", fill="both")

        self.Listbx_Stations_OBS = QListWidget(self.Frame_Listbx_Stations_OBS, exportselection = False, bd = 2, relief="ridge", width = 25, highlightthickness = 0, selectmode = "single", font = tk.font.Font(size = 10))
        self.Listbx_Stations_OBS.pack(  # CONVERT_PACKside="left", fill="both", expand = True)
        self.scroll_bar_Listbx_Stations_OBS = QScrollBar(self.Frame_Listbx_Stations_OBS, bd = 2, relief="raised")
        self.scroll_bar_Listbx_Stations_OBS.pack(  # CONVERT_PACKside="right", fill="y")
        self.scroll_bar_Listbx_Stations_OBS.configure(command = self.Listbx_Stations_OBS.yview)
        self.Listbx_Stations_OBS.configure(yscrollcommand = self.scroll_bar_Listbx_Stations_OBS.set)

        self.Frame_Select_Station_obs = QWidget(self.Left_Frame.interior)
        self.Frame_Select_Station_obs.pack(  # CONVERT_PACKfill="x")

        QLabel(self.Frame_Select_Station_obs,textvariable = self.Cont_Station_Selecionadas_Lista, relief="ridge").pack(side="left", fill="both", expand = True)
        
        QPushButton(self.Frame_Select_Station_obs, textvariable = self.texto,relief="ridge", command = self.Clear_SELECTION_Plot_SCATTER_and_Listbx).pack(side="right", fill="both", expand = True)
        QPushButton(self.Frame_Select_Station_obs, text = "Save est",relief="ridge", command = self.Save_SELECTION_Plot_SCATTER_and_Listbx).pack(side="right", fill="both", expand = True)

        self.Value_cb_Modelo_Grafico = tk.StringVar(self)
        style=tk.ttk.Style()
        style.theme_create('person',parent='alt',settings={'TCombobox':{'configure':{'selectforeground':'black','selectbackground':'white','fieldforeground':'black','fieldbackground':'yellow','background':'yellow'}}})
        style.theme_use('person')
        
        self.cb_modelo_grafico = tk.ttk.Combobox(self.Left_Frame.interior, state = "disabled", exportselection = False, textvariable = self.Value_cb_Modelo_Grafico, values = ['Individual (STD)', 'EIA (STD)', 'Desvio (STD)', 'Mapa VTEC/ROTI (CMN)', 'Painel Mapa VTEC/ROTI (CMN)', 'ROT/VTEC (CMN)', 'ONDAS (STD)'])
        self.cb_modelo_grafico.bind("<<ComboboxSelected>>", self.Exibir_Menu_de_Propriedades_dos_Graficos)  # CONVERT_BIND
        self.cb_modelo_grafico.pack(  # CONVERT_PACKside="top", fill="x")


        self.Frame_propriedades_modelo_INDIVIDUAL = QWidget(self.Left_Frame.interior, bd = 3, bg = 'gray', relief="groove")
        self.Frame_propriedades_modelo_INDIVIDUAL_Calendario = QWidget(self.Frame_propriedades_modelo_INDIVIDUAL, bd = 1, bg = 'gray', relief="groove")
        self.Frame_propriedades_modelo_INDIVIDUAL_Calendario.pack(  # CONVERT_PACKfill="x")
        QLabel(self.Frame_propriedades_modelo_INDIVIDUAL_Calendario, text = self.Dado_config.idioma(53)).pack(fill="x")
        self.calendario_modelo_grafico_INDIVIDUAL = DateEntry(self.Frame_propriedades_modelo_INDIVIDUAL_Calendario, locale = "pt_BR", date_pattern ="dd/mm/yyyy", textvariable = self.Value_DATA_entry_main_inicio, bg = 'darkblue', fg = 'white', borderwidth = 2)
        
        
        self.calendario_modelo_grafico_INDIVIDUAL.bind('<<DateEntrySelected>>', self.Atualizar_DIP_Listabx_Station_OBS)  # CONVERT_BIND
        self.calendario_modelo_grafico_INDIVIDUAL.pack(  # CONVERT_PACKfill="x")
        QLabel(self.Frame_propriedades_modelo_INDIVIDUAL_Calendario, text = self.Dado_config.idioma(54)).pack(fill="x")
        DateEntry(self.Frame_propriedades_modelo_INDIVIDUAL_Calendario, locale = "pt_BR", date_pattern ="dd/mm/yyyy", textvariable = self.Value_DATA_entry_main_fim, bg = 'darkblue', fg = 'white', borderwidth = 2).pack(fill="x")
        
        
        
        self.Frame_propriedades_modelo_INDIVIDUAL_FORMATO_DIA = QWidget(self.Frame_propriedades_modelo_INDIVIDUAL, bd = 1, bg = 'gray', relief="groove")
        self.Frame_propriedades_modelo_INDIVIDUAL_FORMATO_DIA.pack(  # CONVERT_PACKfill="x")
        QLabel(self.Frame_propriedades_modelo_INDIVIDUAL_FORMATO_DIA, text = self.Dado_config.idioma(130), relief="groove").pack(fill="x")
        QRadioButton(self.Frame_propriedades_modelo_INDIVIDUAL_FORMATO_DIA, variable = self.Value_Formato_DATA_Grafico, relief="groove", value = 1, text = self.Dado_config.idioma(40)).pack(side="left", fill="x", expand = True)
        QRadioButton(self.Frame_propriedades_modelo_INDIVIDUAL_FORMATO_DIA, variable = self.Value_Formato_DATA_Grafico, relief="groove", value = 0, text = self.Dado_config.idioma(135)).pack(side="right", fill="x", expand = True)
        self.Frame_propriedades_modelo_INDIVIDUAL_btn = QWidget(self.Frame_propriedades_modelo_INDIVIDUAL, bg = 'gray', relief="groove")
        self.Frame_propriedades_modelo_INDIVIDUAL_btn.pack(  # CONVERT_PACKfill="x", side="bottom")
        QPushButton(self.Frame_propriedades_modelo_INDIVIDUAL_btn, text = self.Dado_config.idioma(108), relief="ridge", command = self.THREAD_PLOTAR_GRAFICO_JANELA_TOPLEVEL_GRAFICO).pack(fill="x")


        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        


        self.Frame_propriedades_modelo_DESVIO = QWidget(self.Left_Frame.interior, bd = 3, bg = 'gray', relief="groove")
        self.Frame_propriedades_modelo_DESVIO_Dias_Calmos = QWidget(self.Frame_propriedades_modelo_DESVIO, bd = 3, relief="groove")
        self.Frame_propriedades_modelo_DESVIO_Dias_Calmos.pack(  # CONVERT_PACKfill="both")
        QLabel(self.Frame_propriedades_modelo_DESVIO_Dias_Calmos, text = self.Dado_config.idioma(123)).pack(fill="x", side="top")
        self.Calendario_Dias_Calmos = Calendar(self.Frame_propriedades_modelo_DESVIO_Dias_Calmos, width = 10, font = "Arial 10", selectmode = 'day', cursor = "hand2", Locator = self.Dado_config.idioma(0), textvariable = self.Value_DATA_entry_main_inicio)
        
        
        self.Calendario_Dias_Calmos.pack(  # CONVERT_PACKfill="both", expand = True)
        QLabel(self.Frame_propriedades_modelo_DESVIO_Dias_Calmos, text = self.Dado_config.idioma(124), relief="ridge").pack(fill="x")
        QLabel(self.Frame_propriedades_modelo_DESVIO_Dias_Calmos, text = self.Dado_config.idioma(53)).pack(fill="x")
        self.Calendario_Data_DESVIO_Inicial = DateEntry(self.Frame_propriedades_modelo_DESVIO_Dias_Calmos, locale = "pt_BR", date_pattern ="dd/mm/yyyy", textvariable = self.Value_DATA_entry_main_inicio, bg = 'darkblue', fg = 'white', borderwidth = 1)
        self.Calendario_Data_DESVIO_Inicial.bind('<<DateEntrySelected>>', self.Atualizar_DIP_Listabx_Station_OBS)  # CONVERT_BIND
        self.Calendario_Data_DESVIO_Inicial.pack(  # CONVERT_PACKfill="both", expand = True)
        QLabel(self.Frame_propriedades_modelo_DESVIO_Dias_Calmos , text = self.Dado_config.idioma(54)).pack(fill="x")
        DateEntry(self.Frame_propriedades_modelo_DESVIO_Dias_Calmos, locale = "pt_BR", date_pattern ="dd/mm/yyyy", textvariable = self.Value_DATA_entry_main_fim, bg = 'darkblue', fg = 'white', borderwidth = 1).pack(fill="both", expand = True)
        self.Frame_propriedades_modelo_DESVIO_Recursos = QWidget(self.Frame_propriedades_modelo_DESVIO, bd = 3, bg = 'gray', relief="groove")
        self.Frame_propriedades_modelo_DESVIO_Recursos.pack(  # CONVERT_PACKfill="x")
        self.Frame_propriedades_modelo_DESVIO_Recursos_Formato_dia = QWidget(self.Frame_propriedades_modelo_DESVIO, bd = 3, bg = 'gray', relief="groove")
        self.Frame_propriedades_modelo_DESVIO_Recursos_Formato_dia.pack(  # CONVERT_PACKfill="x")
        self.Frame_propriedades_modelo_DESVIO_Recursos_Legendas = QWidget(self.Frame_propriedades_modelo_DESVIO, bd = 3, bg = 'gray', relief="groove")
        self.Frame_propriedades_modelo_DESVIO_Recursos_Legendas.pack(  # CONVERT_PACKfill="x")
        self.Frame_propriedades_modelo_DESVIO_Recursos_PLOT = QWidget(self.Frame_propriedades_modelo_DESVIO, bd = 3, bg = 'gray', relief="groove")
        self.Frame_propriedades_modelo_DESVIO_Recursos_PLOT.pack(  # CONVERT_PACKfill="x")
        QLabel(self.Frame_propriedades_modelo_DESVIO_Recursos_Formato_dia, text = self.Dado_config.idioma(130), relief="groove").pack(side="top", fill="x")
        QRadioButton(self.Frame_propriedades_modelo_DESVIO_Recursos_Formato_dia, variable = self.Value_Formato_DATA_Grafico, relief="groove", value = 1, text = self.Dado_config.idioma(40)).pack(side="left", fill="x", expand = True)
        QRadioButton(self.Frame_propriedades_modelo_DESVIO_Recursos_Formato_dia, variable = self.Value_Formato_DATA_Grafico, relief="groove", value = 0, text = self.Dado_config.idioma(131)).pack(side="right", fill="x", expand = True)
        QLabel(self.Frame_propriedades_modelo_DESVIO_Recursos_Legendas, text = self.Dado_config.idioma(134), relief="groove").pack(side="left", fill="both")
        QCheckBox(self.Frame_propriedades_modelo_DESVIO_Recursos_Legendas, variable = self.Value_State_Legenda).pack(fill="x", expand = True, side="left")
        QPushButton(self.Frame_propriedades_modelo_DESVIO_Recursos_PLOT, text = self.Dado_config.idioma(108), relief="ridge", command = self.THREAD_PLOTAR_GRAFICO_JANELA_TOPLEVEL_GRAFICO).pack(fill="x")


        self.Frame_propriedades_modelo_MAPA = QWidget(self.Left_Frame.interior, bd = 3, bg = 'gray', relief="groove")
        self.Frame_propriedades_modelo_MAPA_Entry_inicio = QWidget(self.Frame_propriedades_modelo_MAPA, bg = 'gray')
        self.Frame_propriedades_modelo_MAPA_Entry_inicio.pack(  # CONVERT_PACKfill="x")
        QLabel(self.Frame_propriedades_modelo_MAPA_Entry_inicio, text = self.Dado_config.idioma(53)).pack(fill="x")
        self.Calendario_Data_MAPA_Inicial = DateEntry(self.Frame_propriedades_modelo_MAPA_Entry_inicio, locale = "pt_BR", date_pattern ="dd/mm/yyyy", textvariable = self.Value_DATA_entry_main_inicio, bg = 'darkblue', fg = 'white', borderwidth = 2)  
        
        
        
        self.Calendario_Data_MAPA_Inicial.bind('<<DateEntrySelected>>', self.Atualizar_DIP_Listabx_Station_OBS)  # CONVERT_BIND
        self.Calendario_Data_MAPA_Inicial.pack(  # CONVERT_PACKfill="x")
        self.Frame_propriedades_modelo_MAPA_H_INICIO = QWidget(self.Frame_propriedades_modelo_MAPA, bg = 'gray')
        self.Frame_propriedades_modelo_MAPA_H_INICIO.pack(  # CONVERT_PACKfill="x")
        QLabel(self.Frame_propriedades_modelo_MAPA_H_INICIO, text = self.Dado_config.idioma(172), relief="groove").pack(side="left", fill="both", expand = True)       
        self.MAPA_Time_INICIO = MaskedWidget(self.Frame_propriedades_modelo_MAPA_H_INICIO, 'fixed', mask='99:99:99', width = 10)
        self.MAPA_Time_INICIO.insert(0, '000000')
        self.MAPA_Time_INICIO.pack(  # CONVERT_PACKside="right", fill="both")
        self.Frame_propriedades_modelo_MAPA_Entry_fim = QWidget(self.Frame_propriedades_modelo_MAPA, bg = 'gray')
        self.Frame_propriedades_modelo_MAPA_Entry_fim.pack(  # CONVERT_PACKfill="x")
        QLabel(self.Frame_propriedades_modelo_MAPA_Entry_fim, text = self.Dado_config.idioma(54)).pack(fill="x")
        self.Calendario_Data_MAPA_Final = DateEntry(self.Frame_propriedades_modelo_MAPA_Entry_fim, locale = "pt_BR", date_pattern ="dd/mm/yyyy", textvariable = self.Value_DATA_entry_main_fim , bg = 'darkblue', fg = 'white', borderwidth = 2)  
        self.Calendario_Data_MAPA_Final.pack(  # CONVERT_PACKfill="x")
        self.Frame_propriedades_modelo_MAPA_H_FIM = QWidget(self.Frame_propriedades_modelo_MAPA, bg = 'gray')
        self.Frame_propriedades_modelo_MAPA_H_FIM.pack(  # CONVERT_PACKfill="x")
        QLabel(self.Frame_propriedades_modelo_MAPA_H_FIM, text = self.Dado_config.idioma(173), relief="groove").pack(side="left", fill="both", expand = True)
        self.MAPA_Time_FIM = MaskedWidget(self.Frame_propriedades_modelo_MAPA_H_FIM, 'fixed', mask='99:99:99', width = 10)
        self.MAPA_Time_FIM.insert(0, '240000')
        self.MAPA_Time_FIM.pack(  # CONVERT_PACKside="right", fill="both")
        self.Frame_propriedades_modelo_MAPA_ELE = QWidget(self.Frame_propriedades_modelo_MAPA, bg = 'gray')
        self.Frame_propriedades_modelo_MAPA_ELE.pack(  # CONVERT_PACKfill="x")
        QLabel(self.Frame_propriedades_modelo_MAPA_ELE, text = self.Dado_config.idioma(181), relief="groove").pack(side="left", fill="both", expand = True)
        self.Entry_MAPA_Filter_ELE = QLineEdit(self.Frame_propriedades_modelo_MAPA_ELE, width = 10, validate = "key", validatecommand = vcmd_get_number)
        self.Entry_MAPA_Filter_ELE.insert(END,self.Dado_config.Settings["MAPA"]["fElevation_Filter"])
        self.Entry_MAPA_Filter_ELE.pack(  # CONVERT_PACKside="right")
        self.Frame_propriedades_modelo_MAPA_D_TIME = QWidget(self.Frame_propriedades_modelo_MAPA, bg = 'gray')
        self.Frame_propriedades_modelo_MAPA_D_TIME.pack(  # CONVERT_PACKfill="x")
        QLabel(self.Frame_propriedades_modelo_MAPA_D_TIME, text = self.Dado_config.idioma(174), relief="groove").pack(side="left", fill="both", expand = True)
        self.MAPA_Delta_Time = QLineEdit(self.Frame_propriedades_modelo_MAPA_D_TIME, width = 8, validate = "key", validatecommand = vcmd_get_number, bd = 2)
        self.MAPA_Delta_Time.insert(END, '1')
        self.MAPA_Delta_Time.pack(  # CONVERT_PACKside="right", fill="both")
        self.Frame_propriedades_modelo_MAPA_VTEC_ROTI = QWidget(self.Frame_propriedades_modelo_MAPA, bg = 'gray')
        self.Frame_propriedades_modelo_MAPA_VTEC_ROTI.pack(  # CONVERT_PACKfill="x")        
        QLabel(self.Frame_propriedades_modelo_MAPA_VTEC_ROTI, text = self.Dado_config.idioma(185), relief="groove").pack(side="left", fill="both", expand = True)
        self.CB_DADOS_MAPA_VTEC_ROTI = tk.ttk.Combobox(self.Frame_propriedades_modelo_MAPA_VTEC_ROTI, width = 10, state = 'readonly', exportselection = False, values = ["VTEC", "ROT", "ROTI"])
        self.CB_DADOS_MAPA_VTEC_ROTI.bind("<<ComboboxSelected>>", self.Set_Dados_MAPA_VTEC_ROTI)  # CONVERT_BIND
        self.CB_DADOS_MAPA_VTEC_ROTI.pack(  # CONVERT_PACKside="right", fill="x")

        self.Frame_propriedades_MAPA_VTEC_ROTI = QWidget(self.Frame_propriedades_modelo_MAPA, bg = 'gray')
        self.Frame_propriedades_MAPA_VTEC_ROTI.pack(  # CONVERT_PACKfill="x")









        self.Frame_propriedades_MAPA_ROT = QWidget(self.Frame_propriedades_MAPA_VTEC_ROTI, bg = 'gray')
        self.Frame_propriedades_MAPA_ROT_Delta_Time = QWidget(self.Frame_propriedades_MAPA_ROT, bg = 'gray')
        self.Frame_propriedades_MAPA_ROT_Delta_Time.pack(  # CONVERT_PACKfill="x")
        QLabel(self.Frame_propriedades_MAPA_ROT_Delta_Time, text = 'ΔT (s) (ROT)', relief="groove").pack(side="left", fill="both", expand = True)
        self.Entry_Delta_Time_MAPA_ROT = QLineEdit(self.Frame_propriedades_MAPA_ROT_Delta_Time, width = 10, validate = "key", validatecommand = vcmd_get_number)
        self.Entry_Delta_Time_MAPA_ROT.insert(END, self.Dado_config.Settings["MAPA"]["fValueDelta_ROT"])
        self.Entry_Delta_Time_MAPA_ROT.pack(  # CONVERT_PACKside="right")

        self.Frame_propriedades_MAPA_ROTI = QWidget(self.Frame_propriedades_MAPA_VTEC_ROTI, bg = 'gray')
        self.Frame_propriedades_MAPA_ROTI_ROT_Delta_Time_ROT = QWidget(self.Frame_propriedades_MAPA_ROTI, bg = 'gray')
        self.Frame_propriedades_MAPA_ROTI_ROT_Delta_Time_ROT.pack(  # CONVERT_PACKfill="x")
        QLabel(self.Frame_propriedades_MAPA_ROTI_ROT_Delta_Time_ROT, text = 'ΔT (s) (ROT)', relief="groove").pack(side="left", fill="both", expand = True)
        self.Entry_ROT_Delta_Time_MAPA_ROT = QLineEdit(self.Frame_propriedades_MAPA_ROTI_ROT_Delta_Time_ROT, width = 10, validate = "key", validatecommand = vcmd_get_number)
        self.Entry_ROT_Delta_Time_MAPA_ROT.insert(END, self.Dado_config.Settings["MAPA"]["fValueDelta_ROT"])
        self.Entry_ROT_Delta_Time_MAPA_ROT.pack(  # CONVERT_PACKside="right")
        self.Frame_propriedades_MAPA_ROTI_ROT_Delta_Time_ROTI = QWidget(self.Frame_propriedades_MAPA_ROTI, bg = 'gray')
        self.Frame_propriedades_MAPA_ROTI_ROT_Delta_Time_ROTI.pack(  # CONVERT_PACKfill="x")
        QLabel(self.Frame_propriedades_MAPA_ROTI_ROT_Delta_Time_ROTI, text = 'ΔT (s) (ROTI)', relief="groove").pack(side="left", fill="both", expand = True)
        self.Entry_ROTI_Delta_Time_MAPA_ROTI = QLineEdit(self.Frame_propriedades_MAPA_ROTI_ROT_Delta_Time_ROTI, width = 10, validate = "key", validatecommand = vcmd_get_number)
        self.Entry_ROTI_Delta_Time_MAPA_ROTI.insert(END, str(self.Dado_config.Settings["MAPA"]["fValueDelta_ROTI"]))
        self.Entry_ROTI_Delta_Time_MAPA_ROTI.pack(  # CONVERT_PACKside="right")


        self.Frame_propriedades_modelo_MAPA_Xtick = QWidget(self.Frame_propriedades_modelo_MAPA, bg = 'gray')
        self.Frame_propriedades_modelo_MAPA_Xtick.pack(  # CONVERT_PACKfill="x")
        QCheckBox(self.Frame_propriedades_modelo_MAPA_Xtick, text = "Manual Ticks X",variable=self.varx,onvalue=1,offvalue=0).pack(side="left", fill="both", expand = True)
        self.Entry_MAPA_Xtick = QLineEdit(self.Frame_propriedades_modelo_MAPA_Xtick, width = 20, validate = "key")
        self.Entry_MAPA_Xtick.insert(END,"-70,-50")
        self.Entry_MAPA_Xtick.pack(  # CONVERT_PACKside="right")

        self.Frame_propriedades_modelo_MAPA_Ytick = QWidget(self.Frame_propriedades_modelo_MAPA, bg = 'gray')
        self.Frame_propriedades_modelo_MAPA_Ytick.pack(  # CONVERT_PACKfill="x")
        QCheckBox(self.Frame_propriedades_modelo_MAPA_Ytick, text = "Manual Ticks Y",variable=self.vary,onvalue=1,offvalue=0).pack(side="left", fill="both", expand = True)
        self.Entry_MAPA_Ytick = QLineEdit(self.Frame_propriedades_modelo_MAPA_Ytick, width = 20, validate = "key")
        self.Entry_MAPA_Ytick.insert(END,"-60,-30,-0,30,60")
        self.Entry_MAPA_Ytick.pack(  # CONVERT_PACKside="right")

        self.Frame_propriedades_modelo_MAPA_Abs = QWidget(self.Frame_propriedades_modelo_MAPA, bg = 'gray')
        self.Frame_propriedades_modelo_MAPA_Abs.pack(  # CONVERT_PACKfill="x")
        QCheckBox(self.Frame_propriedades_modelo_MAPA_Abs, text = "abs(ROT)",variable=self.varabs,onvalue=1,offvalue=0).pack(side="left", fill="both", expand = True)
        
        self.Frame_propriedades_MAPA_VIDEO = QWidget(self.Frame_propriedades_modelo_MAPA, bg = 'gray')
        self.Frame_propriedades_MAPA_VIDEO.pack(  # CONVERT_PACKfill="x")
        QLabel(self.Frame_propriedades_MAPA_VIDEO, text = self.Dado_config.idioma(191), relief="groove").pack(side="left", fill="both", expand = True)
        QCheckBox(self.Frame_propriedades_MAPA_VIDEO, variable = self.Value_Check_VIDEO_MAPA, relief="ridge", bd = 2, width = 5).pack(side="right")
        QPushButton(self.Frame_propriedades_modelo_MAPA, text = self.Dado_config.idioma(175), relief="ridge", command = self.PLOTAR_GRAFICO_JANELA_TOPLEVEL_MODELO_GRAFICO_MAPA).pack(fill="x")
        QPushButton(self.Frame_propriedades_modelo_MAPA, text = self.Dado_config.idioma(108), relief="ridge", command = self.THREAD_PLOTAR_GRAFICO_JANELA_TOPLEVEL_GRAFICO).pack(fill="x")


        self.Frame_propriedades_modelo_PAINEL_MAPA = QWidget(self.Left_Frame.interior, bd = 3, bg = 'gray', relief="groove")
        self.Frame_propriedades_modelo_PAINEL_MAPA_DATA_INICIO = QWidget(self.Frame_propriedades_modelo_PAINEL_MAPA, bg = 'gray')
        self.Frame_propriedades_modelo_PAINEL_MAPA_DATA_INICIO.pack(  # CONVERT_PACKfill="x")
        QLabel(self.Frame_propriedades_modelo_PAINEL_MAPA_DATA_INICIO, text = self.Dado_config.idioma(53)).pack(fill="x")
        self.Calendario_Data_PAINEL_MAPA_Inicial = DateEntry(self.Frame_propriedades_modelo_PAINEL_MAPA_DATA_INICIO, locale = "pt_BR", date_pattern ="dd/mm/yyyy", textvariable = self.Value_DATA_entry_main_inicio, bg = 'darkblue', fg = 'white', borderwidth = 2)  
        self.Calendario_Data_PAINEL_MAPA_Inicial.bind('<<DateEntrySelected>>', self.Atualizar_DIP_Listabx_Station_OBS)  # CONVERT_BIND
        self.Calendario_Data_PAINEL_MAPA_Inicial.pack(  # CONVERT_PACKfill="x")
        self.Frame_propriedades_modelo_PAINEL_MAPA_H_INICIO = QWidget(self.Frame_propriedades_modelo_PAINEL_MAPA, bg = 'gray')
        self.Frame_propriedades_modelo_PAINEL_MAPA_H_INICIO.pack(  # CONVERT_PACKfill="x")
        QLabel(self.Frame_propriedades_modelo_PAINEL_MAPA_H_INICIO, text = self.Dado_config.idioma(172), relief="groove").pack(side="left", fill="both", expand = True)
        self.PAINEL_MAPA_Time_INICIO = MaskedWidget(self.Frame_propriedades_modelo_PAINEL_MAPA_H_INICIO, 'fixed', mask='99:99:99', width = 10)
        self.PAINEL_MAPA_Time_INICIO.insert(0, '000000')
        self.PAINEL_MAPA_Time_INICIO.pack(  # CONVERT_PACKside="right", fill="both")
        self.Frame_propriedades_modelo_PAINEL_MAPA_DATA_FIM = QWidget(self.Frame_propriedades_modelo_PAINEL_MAPA, bg = 'gray')
        self.Frame_propriedades_modelo_PAINEL_MAPA_DATA_FIM.pack(  # CONVERT_PACKfill="x")
        QLabel(self.Frame_propriedades_modelo_PAINEL_MAPA_DATA_FIM, text = self.Dado_config.idioma(54)).pack(fill="x")
        self.Calendario_Data_PAINEL_MAPA_Final = DateEntry(self.Frame_propriedades_modelo_PAINEL_MAPA_DATA_FIM, locale = "pt_BR", date_pattern ="dd/mm/yyyy", textvariable = self.Value_DATA_entry_main_fim, bg = 'darkblue', fg = 'white', borderwidth = 2)  
        self.Calendario_Data_PAINEL_MAPA_Final.pack(  # CONVERT_PACKfill="x")
        self.Frame_propriedades_modelo_PAINEL_MAPA_H_FIM = QWidget(self.Frame_propriedades_modelo_PAINEL_MAPA, bg = 'gray')
        self.Frame_propriedades_modelo_PAINEL_MAPA_H_FIM.pack(  # CONVERT_PACKfill="x")
        QLabel(self.Frame_propriedades_modelo_PAINEL_MAPA_H_FIM, text = self.Dado_config.idioma(173), relief="groove").pack(side="left", fill="both", expand = True)
        self.PAINEL_MAPA_Time_FIM = MaskedWidget(self.Frame_propriedades_modelo_PAINEL_MAPA_H_FIM, 'fixed', mask='99:99:99', width = 10)
        self.PAINEL_MAPA_Time_FIM.insert(0, '240000')
        self.PAINEL_MAPA_Time_FIM.pack(  # CONVERT_PACKside="right", fill="both")
        self.Frame_propriedades_modelo_PAINEL_MAPA_ELE = QWidget(self.Frame_propriedades_modelo_PAINEL_MAPA, bg = 'gray')
        self.Frame_propriedades_modelo_PAINEL_MAPA_ELE.pack(  # CONVERT_PACKfill="x")
        QLabel(self.Frame_propriedades_modelo_PAINEL_MAPA_ELE, text = self.Dado_config.idioma(181), relief="groove").pack(side="left", fill="both", expand = True)
        self.Entry_PAINEL_MAPA_Filter_ELE = QLineEdit(self.Frame_propriedades_modelo_PAINEL_MAPA_ELE, width = 10, validate = "key", validatecommand = vcmd_get_number)
        self.Entry_PAINEL_MAPA_Filter_ELE.insert(END,self.Dado_config.Settings["PAINEL MAPA"]["fElevation_Filter"])
        self.Entry_PAINEL_MAPA_Filter_ELE.pack(  # CONVERT_PACKside="right")
        self.Frame_propriedades_modelo_PAINEL_MAPA_GRADE = QWidget(self.Frame_propriedades_modelo_PAINEL_MAPA, bg = 'gray')
        self.Frame_propriedades_modelo_PAINEL_MAPA_GRADE.pack(  # CONVERT_PACKfill="x")
        QLabel(self.Frame_propriedades_modelo_PAINEL_MAPA_GRADE, text = self.Dado_config.idioma(186), relief="groove").pack(side="left", fill="both", expand = True)
        self.Frame_propriedades_modelo_PAINEL_MAPA_GRADE_COLUNA_LINHA = QWidget(self.Frame_propriedades_modelo_PAINEL_MAPA_GRADE, bg = 'gray')
        self.Frame_propriedades_modelo_PAINEL_MAPA_GRADE_COLUNA_LINHA.pack(  # CONVERT_PACKside="right", fill="both")
        self.PAINEL_MAPA_GRADE_LINHA = QLineEdit(self.Frame_propriedades_modelo_PAINEL_MAPA_GRADE_COLUNA_LINHA, width=5,validate = "key", validatecommand = vcmd_get_number,bd = 2)
        self.PAINEL_MAPA_GRADE_LINHA.insert(END, '5')
        self.PAINEL_MAPA_GRADE_LINHA.pack(  # CONVERT_PACKside="left", fill="both")
        QLabel(self.Frame_propriedades_modelo_PAINEL_MAPA_GRADE_COLUNA_LINHA, text = "X", relief="groove").pack(side="left", fill="both", expand = True)
        self.PAINEL_MAPA_GRADE_COLUNA = QLineEdit(self.Frame_propriedades_modelo_PAINEL_MAPA_GRADE_COLUNA_LINHA,width=5,validate = "key", validatecommand = vcmd_get_number,bd = 2)
        self.PAINEL_MAPA_GRADE_COLUNA.insert(END, '6')
        self.PAINEL_MAPA_GRADE_COLUNA.pack(  # CONVERT_PACKside="right", fill="both")
        self.Frame_propriedades_modelo_PAINEL_MAPA_VTEC_ROTI = QWidget(self.Frame_propriedades_modelo_PAINEL_MAPA, bg = 'gray')
        self.Frame_propriedades_modelo_PAINEL_MAPA_VTEC_ROTI.pack(  # CONVERT_PACKfill="x")
        QLabel(self.Frame_propriedades_modelo_PAINEL_MAPA_VTEC_ROTI, text = self.Dado_config.idioma(185), relief="groove").pack(side="left", fill="both", expand = True)
        self.CB_DADOS_PAINEL_MAPA_VTEC_ROTI = tk.ttk.Combobox(self.Frame_propriedades_modelo_PAINEL_MAPA_VTEC_ROTI, width = 10, state = 'readonly', exportselection = False, values = ["VTEC","ROT","ROTI"])
        self.CB_DADOS_PAINEL_MAPA_VTEC_ROTI.bind("<<ComboboxSelected>>", self.Set_Dados_PAINEL_MAPA_VTEC_ROTI)  # CONVERT_BIND
        self.CB_DADOS_PAINEL_MAPA_VTEC_ROTI.pack(  # CONVERT_PACKside="right", fill="x")

        self.Frame_propriedades_PAINEL_MAPA_VTEC_ROTI = QWidget(self.Frame_propriedades_modelo_PAINEL_MAPA, bg = 'gray')
        self.Frame_propriedades_PAINEL_MAPA_VTEC_ROTI.pack(  # CONVERT_PACKfill="x")

        
        
        
        
        
        
        

        self.Frame_propriedades_PAINEL_MAPA_ROT = QWidget(self.Frame_propriedades_PAINEL_MAPA_VTEC_ROTI, bg = 'gray')
        self.Frame_propriedades_PAINEL_MAPA_ROT_Delta_Time_ROT = QWidget(self.Frame_propriedades_PAINEL_MAPA_ROT, bg = 'gray')
        self.Frame_propriedades_PAINEL_MAPA_ROT_Delta_Time_ROT.pack(  # CONVERT_PACKfill="x")
        QLabel(self.Frame_propriedades_PAINEL_MAPA_ROT_Delta_Time_ROT, text = 'ΔT (s) (ROT)', relief="groove").pack(side="left", fill="both", expand = True)
        self.Entry_Delta_Time_PAINEL_MAPA_ROT = QLineEdit(self.Frame_propriedades_PAINEL_MAPA_ROT_Delta_Time_ROT, width = 10, validate = "key", validatecommand = vcmd_get_number)
        self.Entry_Delta_Time_PAINEL_MAPA_ROT.insert(END, self.Dado_config.Settings["PAINEL MAPA"]["fValueDelta_ROT"])
        self.Entry_Delta_Time_PAINEL_MAPA_ROT.pack(  # CONVERT_PACKside="right")

        self.Frame_propriedades_PAINEL_MAPA_ROTI = QWidget(self.Frame_propriedades_PAINEL_MAPA_VTEC_ROTI, bg = 'gray')
        self.Frame_propriedades_PAINEL_MAPA_ROTI_ROT_Delta_Time_ROT = QWidget(self.Frame_propriedades_PAINEL_MAPA_ROTI, bg = 'gray')
        self.Frame_propriedades_PAINEL_MAPA_ROTI_ROT_Delta_Time_ROT.pack(  # CONVERT_PACKfill="x")
        QLabel(self.Frame_propriedades_PAINEL_MAPA_ROTI_ROT_Delta_Time_ROT, text = 'ΔT (s) (ROT)', relief="groove").pack(side="left", fill="both", expand = True)
        self.Entry_ROT_Delta_Time_PAINEL_MAPA_ROT = QLineEdit(self.Frame_propriedades_PAINEL_MAPA_ROTI_ROT_Delta_Time_ROT, width = 10, validate = "key", validatecommand = vcmd_get_number)
        self.Entry_ROT_Delta_Time_PAINEL_MAPA_ROT.insert(END, self.Dado_config.Settings["PAINEL MAPA"]["fValueDelta_ROT"])
        self.Entry_ROT_Delta_Time_PAINEL_MAPA_ROT.pack(  # CONVERT_PACKside="right")
        self.Frame_propriedades_PAINEL_MAPA_ROTI_ROT_Delta_Time_ROTI = QWidget(self.Frame_propriedades_PAINEL_MAPA_ROTI, bg = 'gray')
        self.Frame_propriedades_PAINEL_MAPA_ROTI_ROT_Delta_Time_ROTI.pack(  # CONVERT_PACKfill="x")
        QLabel(self.Frame_propriedades_PAINEL_MAPA_ROTI_ROT_Delta_Time_ROTI, text = 'ΔT (s) (ROTI)', relief="groove").pack(side="left", fill="both", expand = True)
        self.Entry_ROTI_Delta_Time_PAINEL_MAPA_ROTI = QLineEdit(self.Frame_propriedades_PAINEL_MAPA_ROTI_ROT_Delta_Time_ROTI, width = 10, validate = "key", validatecommand = vcmd_get_number)
        self.Entry_ROTI_Delta_Time_PAINEL_MAPA_ROTI.insert(END, str(self.Dado_config.Settings["PAINEL MAPA"]["fValueDelta_ROTI"]))
        self.Entry_ROTI_Delta_Time_PAINEL_MAPA_ROTI.pack(  # CONVERT_PACKside="right")

        QPushButton(self.Frame_propriedades_modelo_PAINEL_MAPA, text = self.Dado_config.idioma(175), relief="ridge", command = self.PLOTAR_GRAFICO_JANELA_TOPLEVEL_MODELO_GRAFICO_PAINEL_MAPA).pack(fill="x")
        QPushButton(self.Frame_propriedades_modelo_PAINEL_MAPA, text = self.Dado_config.idioma(108), relief="ridge", command = self.THREAD_PLOTAR_GRAFICO_JANELA_TOPLEVEL_GRAFICO).pack(fill="x")


        self.Frame_propriedades_modelo_ROT = QWidget(self.Left_Frame.interior, bd = 3, bg = 'gray', relief="groove")
        self.Frame_propriedades_modelo_ROT_Entry = QWidget(self.Frame_propriedades_modelo_ROT, bg = 'gray', relief="groove")
        self.Frame_propriedades_modelo_ROT_Entry.pack(  # CONVERT_PACKfill="x")
        QLabel(self.Frame_propriedades_modelo_ROT_Entry, text = self.Dado_config.idioma(107)).pack(fill="x")
        self.Calendario_Data_ROT_Inicial = DateEntry(self.Frame_propriedades_modelo_ROT_Entry, locale = "pt_BR", date_pattern ="dd/mm/yyyy", textvariable = self.Value_DATA_entry_main_inicio, bg = 'darkblue', fg = 'white', borderwidth = 2)
        self.Calendario_Data_ROT_Inicial.bind('<<DateEntrySelected>>', self.Atualizar_DIP_Listabx_Station_OBS)  # CONVERT_BIND
        self.Calendario_Data_ROT_Inicial.pack(  # CONVERT_PACKfill="x")
        self.Frame_propriedades_modelo_ROT_Check = QWidget(self.Frame_propriedades_modelo_ROT, bg = 'gray')
        self.Frame_propriedades_modelo_ROT_Check.pack(  # CONVERT_PACKfill="x")
        QLabel(self.Frame_propriedades_modelo_ROT_Check, text = self.Dado_config.idioma(167), relief="groove").pack(side="left", fill="both", expand = True)
        QCheckBox(self.Frame_propriedades_modelo_ROT_Check, relief="groove", variable = self.Value_Line_Cores, width = 5,command=self.activateROTLegend).pack(side="right")
        self.Frame_propriedades_modelo_ROT_Check_Legenda_LOCAL = QWidget(self.Frame_propriedades_modelo_ROT, bg = 'gray')
        self.Frame_propriedades_modelo_ROT_Check_Legenda_LOCAL.pack(  # CONVERT_PACKfill="x")
        self.Frame_propriedades_modelo_ROT_Check_Legenda = QWidget(self.Frame_propriedades_modelo_ROT_Check_Legenda_LOCAL, bg = 'gray')
        QLabel(self.Frame_propriedades_modelo_ROT_Check_Legenda, text = self.Dado_config.idioma(134), relief="groove").pack(side="left", fill="both", expand = True)
        QCheckBox(self.Frame_propriedades_modelo_ROT_Check_Legenda, relief="groove", variable = self.Value_State_Legenda, width = 5).pack(side="right")
        self.Frame_propriedades_modelo_ROT_D_TIME = QWidget(self.Frame_propriedades_modelo_ROT, bg = 'gray')
        self.Frame_propriedades_modelo_ROT_D_TIME.pack(  # CONVERT_PACKfill="x")
        QLabel(self.Frame_propriedades_modelo_ROT_D_TIME, text = 'ΔT (s) ROT', relief="groove").pack(side="left", fill="both", expand = True)
        self.Entry_ROT_Delta_Time_ROT = QLineEdit(self.Frame_propriedades_modelo_ROT_D_TIME, width = 10, validate = "key", validatecommand = vcmd_get_number)
        self.Entry_ROT_Delta_Time_ROT.insert(END, self.Dado_config.Settings["ROT"]["fValueDelta_ROT"])
        self.Entry_ROT_Delta_Time_ROT.pack(  # CONVERT_PACKside="right")

        
        self.Frame_propriedades_modelo_ROTI_D_TIME = QWidget(self.Frame_propriedades_modelo_ROT, bg = 'gray')
        self.Frame_propriedades_modelo_ROTI_D_TIME.pack(  # CONVERT_PACKfill="x")
        QLabel(self.Frame_propriedades_modelo_ROTI_D_TIME, text = 'ΔT (s) ROTI', relief="groove").pack(side="left", fill="both", expand = True)
        self.Entry_ROT_Delta_Time_ROTI = QLineEdit(self.Frame_propriedades_modelo_ROTI_D_TIME, width = 10, validate = "key", validatecommand = vcmd_get_number)
        self.Entry_ROT_Delta_Time_ROTI.insert(END, self.Dado_config.Settings["ROT"]["fValueDelta_ROTI"])
        self.Entry_ROT_Delta_Time_ROTI.pack(  # CONVERT_PACKside="right")
        
        self.Frame_propriedades_modelo_ROT_ELE = QWidget(self.Frame_propriedades_modelo_ROT, bg = 'gray')
        self.Frame_propriedades_modelo_ROT_ELE.pack(  # CONVERT_PACKfill="x")
        QLabel(self.Frame_propriedades_modelo_ROT_ELE, text = self.Dado_config.idioma(181), relief="groove").pack(side="left", fill="both", expand = True)
        self.Entry_ROT_Filter_ELE = QLineEdit(self.Frame_propriedades_modelo_ROT_ELE, width = 10, validate = "key", validatecommand = vcmd_get_number)
        self.Entry_ROT_Filter_ELE.insert(END, self.Dado_config.Settings["ROT"]["fElevation_Filter"])
        self.Entry_ROT_Filter_ELE.pack(  # CONVERT_PACKside="right")
        self.Frame_propriedades_modelo_ROT_FATOR_MULTIPLICACAO = QWidget(self.Frame_propriedades_modelo_ROT, bg = 'gray')
        self.Frame_propriedades_modelo_ROT_FATOR_MULTIPLICACAO.pack(  # CONVERT_PACKfill="x")
        QLabel(self.Frame_propriedades_modelo_ROT_FATOR_MULTIPLICACAO, text = self.Dado_config.idioma(187), relief="groove").pack(side="left", fill="both", expand = True)
        self.Entry_ROT_Filter_FATOR_MULTIPLICACAO = QLineEdit(self.Frame_propriedades_modelo_ROT_FATOR_MULTIPLICACAO, width = 10, validate = "key", validatecommand = vcmd_get_number)
        self.Entry_ROT_Filter_FATOR_MULTIPLICACAO.insert(END, self.Dado_config.Settings["ROT"]["fValueMultFactor_ROT"])
        self.Entry_ROT_Filter_FATOR_MULTIPLICACAO.pack(  # CONVERT_PACKside="right")
        



        self.Frame_propriedades_modelo_ROT_TIPO = QWidget(self.Frame_propriedades_modelo_ROT, bg = 'gray')
        QLabel(self.Frame_propriedades_modelo_ROT_TIPO, text = self.Dado_config.idioma(185), relief="groove").pack(side="left", fill="both", expand = True)
        self.CB_DADOS_ROT = tk.ttk.Combobox(self.Frame_propriedades_modelo_ROT_TIPO, width = 10, state = 'readonly', exportselection = False, values = ["VTEC","ROT","ROTI"])
        self.CB_DADOS_ROT.bind("<<ComboboxSelected>>", self.Set_Dados_ROT)  # CONVERT_BIND
        self.CB_DADOS_ROT.pack(  # CONVERT_PACKside="right", fill="x")
        self.Frame_propriedades_modelo_ROT_TIPO.pack(  # CONVERT_PACKfill="x")

        self.Frame_propriedades_modelo_ROT_SF = QWidget(self.Frame_propriedades_modelo_ROT, bg = 'gray')
        self.Frame_propriedades_modelo_ROT_SF.pack(  # CONVERT_PACKfill="x")
        QCheckBox(self.Frame_propriedades_modelo_ROT_SF, text = "ROT spread",variable=self.rots,onvalue=1,offvalue=0).pack(side="left", fill="both", expand = True)

        self.Frame_propriedades_modelo_ROT_XMinortick = QWidget(self.Frame_propriedades_modelo_ROT, bg = 'gray')
        self.Frame_propriedades_modelo_ROT_XMinortick.pack(  # CONVERT_PACKfill="x")
        QLabel(self.Frame_propriedades_modelo_ROT_XMinortick, text = "Qtde_Xminor", relief="groove").pack(side="left", fill="both", expand = True)
        self.Entry_ROT_XMinor = QLineEdit(self.Frame_propriedades_modelo_ROT_XMinortick, width = 10, validate = "key", validatecommand = vcmd_get_number)
        self.Entry_ROT_XMinor.insert(END,"4")
        self.Entry_ROT_XMinor.pack(  # CONVERT_PACKside="right")

        self.Frame_propriedades_modelo_ROT_YMinortick = QWidget(self.Frame_propriedades_modelo_ROT, bg = 'gray')
        self.Frame_propriedades_modelo_ROT_YMinortick.pack(  # CONVERT_PACKfill="x")
        QLabel(self.Frame_propriedades_modelo_ROT_YMinortick, text = "Qtde_Yminor", relief="groove").pack(side="left", fill="both", expand = True)
        self.Entry_ROT_YMinor = QLineEdit(self.Frame_propriedades_modelo_ROT_YMinortick, width = 10, validate = "key", validatecommand = vcmd_get_number)
        self.Entry_ROT_YMinor.insert(END,"4")
        self.Entry_ROT_YMinor.pack(  # CONVERT_PACKside="right")
        

        QPushButton(self.Frame_propriedades_modelo_ROT, text = self.Dado_config.idioma(108), relief = 'ridge', command = self.THREAD_PLOTAR_GRAFICO_JANELA_TOPLEVEL_GRAFICO).pack(fill="both", expand = True)


        self.Frame_propriedades_modelo_EIA = QWidget(self.Left_Frame.interior, bd = 3, bg = 'gray', relief="groove")
        self.Frame_propriedades_modelo_EIA_Entry = QWidget(self.Frame_propriedades_modelo_EIA, bg = 'gray')
        self.Frame_propriedades_modelo_EIA_Entry.pack(  # CONVERT_PACKfill="x")
        QLabel(self.Frame_propriedades_modelo_EIA, text = self.Dado_config.idioma(53)).pack(fill="x")
        self.Calendario_Data_EIA_Inicial = DateEntry(self.Frame_propriedades_modelo_EIA, locale = "pt_BR", date_pattern ="dd/mm/yyyy", textvariable = self.Value_DATA_entry_main_inicio, bg = 'darkblue', fg = 'white', borderwidth = 2)
        self.Calendario_Data_EIA_Inicial.bind('<<DateEntrySelected>>', self.Atualizar_DIP_Listabx_Station_OBS)  # CONVERT_BIND
        self.Calendario_Data_EIA_Inicial.pack(  # CONVERT_PACKfill="x")
        QLabel(self.Frame_propriedades_modelo_EIA, text = self.Dado_config.idioma(54)).pack(fill="x")
        DateEntry(self.Frame_propriedades_modelo_EIA, locale = "pt_BR", date_pattern ="dd/mm/yyyy", textvariable = self.Value_DATA_entry_main_fim, bg = 'darkblue', fg = 'white', borderwidth = 2).pack(fill="x")
        self.Frame_propriedades_modelo_EIA_Check = QWidget(self.Frame_propriedades_modelo_EIA, bg = 'gray')
        self.Frame_propriedades_modelo_EIA_Check.pack(  # CONVERT_PACKfill="x")
        QLabel(self.Frame_propriedades_modelo_EIA_Check, text = self.Dado_config.idioma(109), relief="groove").pack(side="left", fill="both", expand = True)
        QCheckBox(self.Frame_propriedades_modelo_EIA_Check, variable = self.Value_station_on_TICK, width = 5 ).pack(side="right")
        self.Frame_propriedades_modelo_EIA_eixoY = QWidget(self.Frame_propriedades_modelo_EIA, bg = 'gray', relief="groove")
        self.Frame_propriedades_modelo_EIA_eixoY.pack(  # CONVERT_PACKfill="x")
        QLabel(self.Frame_propriedades_modelo_EIA_eixoY, text = self.Dado_config.idioma(120), relief="groove").pack(fill="x")
        QRadioButton(self.Frame_propriedades_modelo_EIA_eixoY, variable = self.Value_Lat_Dip_axes_Y, value = 0, text = 'Latitude', relief="groove").pack(side="right", fill="x", expand = True)
        QRadioButton(self.Frame_propriedades_modelo_EIA_eixoY, variable = self.Value_Lat_Dip_axes_Y, value = 1, text = 'Dip.Lat', relief="groove").pack(side="left", fill="x", expand = True)
        self.Frame_propriedades_modelo_EIA_btn = QWidget(self.Frame_propriedades_modelo_EIA, bg = 'gray', relief="groove")
        self.Frame_propriedades_modelo_EIA_btn.pack(  # CONVERT_PACKfill="x")
        QPushButton(self.Frame_propriedades_modelo_EIA_btn, text = self.Dado_config.idioma(108), relief="ridge", command = self.THREAD_PLOTAR_GRAFICO_JANELA_TOPLEVEL_GRAFICO).pack(fill="x")


        self.Frame_propriedades_modelo_ONDAS = QWidget(self.Left_Frame.interior, bd = 3, bg = 'gray', relief="groove")
        
        QLabel(self.Frame_propriedades_modelo_ONDAS, text = self.Dado_config.idioma(53)).pack(fill="x")
        self.Calendario_Data_ONDAS_Inicial = DateEntry(self.Frame_propriedades_modelo_ONDAS, locale = "pt_BR", date_pattern ="dd/mm/yyyy", textvariable = self.Value_DATA_entry_main_inicio, bg = 'darkblue', fg = 'white', borderwidth = 1)
        self.Calendario_Data_ONDAS_Inicial.bind('<<DateEntrySelected>>', self.Atualizar_DIP_Listabx_Station_OBS)  # CONVERT_BIND
        self.Calendario_Data_ONDAS_Inicial.pack(  # CONVERT_PACKfill="both", expand = True)
        QLabel(self.Frame_propriedades_modelo_ONDAS , text = self.Dado_config.idioma(54)).pack(fill="x")
        DateEntry(self.Frame_propriedades_modelo_ONDAS, locale = "pt_BR", date_pattern ="dd/mm/yyyy", textvariable = self.Value_DATA_entry_main_fim, bg = 'darkblue', fg = 'white', borderwidth = 1).pack(fill="both", expand = True)
        self.Frame_propriedades_modelo_ONDAS_Recursos = QWidget(self.Frame_propriedades_modelo_ONDAS, bd = 3, bg = 'gray', relief="groove")
        self.Frame_propriedades_modelo_ONDAS_Recursos.pack(  # CONVERT_PACKfill="x")
        self.Frame_propriedades_modelo_ONDAS_Recursos_Formato_dia = QWidget(self.Frame_propriedades_modelo_ONDAS, bd = 3, bg = 'gray', relief="groove")
        self.Frame_propriedades_modelo_ONDAS_Recursos_Formato_dia.pack(  # CONVERT_PACKfill="x")
        self.Frame_propriedades_modelo_ONDAS_Recursos_Legendas = QWidget(self.Frame_propriedades_modelo_ONDAS, bd = 3, bg = 'gray', relief="groove")
        self.Frame_propriedades_modelo_ONDAS_Recursos_Legendas.pack(  # CONVERT_PACKfill="x")
        self.Frame_propriedades_modelo_ONDAS_Recursos_PLOT = QWidget(self.Frame_propriedades_modelo_ONDAS, bd = 3, bg = 'gray', relief="groove")
        self.Frame_propriedades_modelo_ONDAS_Recursos_PLOT.pack(  # CONVERT_PACKfill="x")
        QLabel(self.Frame_propriedades_modelo_ONDAS_Recursos_Formato_dia, text = self.Dado_config.idioma(130), relief="groove").pack(side="top", fill="x")
        QRadioButton(self.Frame_propriedades_modelo_ONDAS_Recursos_Formato_dia, variable = self.Value_Formato_DATA_Grafico, relief="groove", value = 1, text = self.Dado_config.idioma(40)).pack(side="left", fill="x", expand = True)
        QRadioButton(self.Frame_propriedades_modelo_ONDAS_Recursos_Formato_dia, variable = self.Value_Formato_DATA_Grafico, relief="groove", value = 0, text = self.Dado_config.idioma(131)).pack(side="right", fill="x", expand = True)
        QLabel(self.Frame_propriedades_modelo_ONDAS_Recursos_Legendas, text = self.Dado_config.idioma(134), relief="groove").pack(side="left", fill="both")
        QCheckBox(self.Frame_propriedades_modelo_ONDAS_Recursos_Legendas, variable = self.Value_State_Legenda).pack(fill="x", expand = True, side="left")
        self.Frame_propriedades_modelo_ONDAS_CORTE = QWidget(self.Frame_propriedades_modelo_ONDAS_Recursos, bg = 'gray')
        self.Frame_propriedades_modelo_ONDAS_CORTE.pack(  # CONVERT_PACKfill="x")
        QLabel(self.Frame_propriedades_modelo_ONDAS_CORTE, text = "Time", relief="groove").pack(side="left", fill="both", expand = True)
        self.Entry_ONDAS_CORTE = QLineEdit(self.Frame_propriedades_modelo_ONDAS_CORTE, width = 10, validate = "key", validatecommand = vcmd_get_number)
        self.Entry_ONDAS_CORTE.insert(END,"18")
        self.Entry_ONDAS_CORTE.pack(  # CONVERT_PACKside="right")
        QPushButton(self.Frame_propriedades_modelo_ONDAS_Recursos_PLOT, text = self.Dado_config.idioma(108), relief="ridge", command = self.THREAD_PLOTAR_GRAFICO_JANELA_TOPLEVEL_GRAFICO).pack(fill="x")



        self.Right_Frame = QWidget(self, relief="ridge", bg = 'gray')
        self.Right_Frame.pack(  # CONVERT_PACKfill="both", expand = True)


        self.FIGURA_MAPA_PRINCIPAL = plt.figure()
        self.AXES_MAPA_PRINCIPAL = plt.axes(projection = ccrs.PlateCarree())
        self.AXES_MAPA_PRINCIPAL.add_feature(cfeature.NaturalEarthFeature('cultural', 'admin_1_states_provinces_lines', '50m', edgecolor = 'gray', facecolor = 'none'))
        self.AXES_MAPA_PRINCIPAL.add_feature(cfeature.LAND)
        self.AXES_MAPA_PRINCIPAL.add_feature(cfeature.OCEAN)
        self.AXES_MAPA_PRINCIPAL.add_feature(cfeature.STATES)
        self.AXES_MAPA_PRINCIPAL.add_feature(cfeature.COASTLINE)
        self.AXES_MAPA_PRINCIPAL.add_feature(cfeature.BORDERS)
        self.AXES_MAPA_PRINCIPAL.add_feature(cfeature.LAKES, alpha = 0.5)
        self.AXES_MAPA_PRINCIPAL.add_feature(cfeature.RIVERS)
        self.CANVAS_MAPA_PRINCIPAL = FigureCanvas(self.FIGURA_MAPA_PRINCIPAL, self.Right_Frame)
        self.CANVAS_MAPA_PRINCIPAL.get_tk_widget().pack(fill="both", expand = True)
        
        self.FIGURA_MAPA_PRINCIPAL.subplots_adjust(top=1,right=1)
        self.FIGURA_MAPA_PRINCIPAL.tight_layout(pad = .1)
        self.CANVAS_MAPA_PRINCIPAL._tkcanvas.pack(  # CONVERT_PACKside="bottom", fill="both", expand = True)
        if not self.License_val.get():
            img = Image.open(self.uti.resource_path('img\icone.ico')).rotate(0)
            self.AXES_MAPA_PRINCIPAL.imshow(img, extent = (-50, 50, -50, 50))
            logo_path = TextPath((-35,-65), 'UTECDA', size = 20 , prop = FontProperties(family = 'Calibri'))
            patch = PathPatch(logo_path, facecolor = 'black' ,edgecolor = 'black', transform = ccrs.PlateCarree())
            self.AXES_MAPA_PRINCIPAL.add_patch(patch)
            logo_path = TextPath((-78,-75), '(Univap Total Eletronic Content Data Analysis)', size = 8 , prop = FontProperties(family = 'Calibri'))
            patch = PathPatch(logo_path, facecolor = 'black' ,edgecolor = 'black', transform = ccrs.PlateCarree())
            self.AXES_MAPA_PRINCIPAL.add_patch(patch)
            self.AXES_MAPA_PRINCIPAL.set_extent([-180, 180, -90, 90],crs=ccrs.PlateCarree())
        else:
            
            
            self.TOOLBAR_MAPA_PRINCIPAL = TopNavigationToolbar(self.CANVAS_MAPA_PRINCIPAL, self.Right_Frame)
            self.TOOLBAR_MAPA_PRINCIPAL.update()
            self.TOOLBAR_MAPA_PRINCIPAL.pack(  # CONVERT_PACKside="top", fill="x")
            self.IMAGE_GOOGLE_KMZ= PhotoImage.from_pil(self, (Image.open(self.uti.resource_path("img/earth.png"))).resize((25,25), Image.LANCZOS))
            BUTTON_KML_TOOLBAR_MAPA_PRINCIPAL = QPushButton(master=self.TOOLBAR_MAPA_PRINCIPAL,image = self.IMAGE_GOOGLE_KMZ,command= self.start_gerar_GOOGLE_KMZ)
            BUTTON_KML_TOOLBAR_MAPA_PRINCIPAL.pack(  # CONVERT_PACKside="left")
            ToolTip.createToolTip(BUTTON_KML_TOOLBAR_MAPA_PRINCIPAL, "Generate kml from map")
            self.IMAGE_SIGLAS_MAPA= PhotoImage.from_pil(self, (Image.open(self.uti.resource_path("img/est.png"))).resize((25,25), Image.LANCZOS))
            BUTTON_SIGLAS_MAPA_MAPA_PRINCIPAL = QPushButton(master=self.TOOLBAR_MAPA_PRINCIPAL,image = self.IMAGE_SIGLAS_MAPA,command= self.tool_start_siglas_mapa)
            BUTTON_SIGLAS_MAPA_MAPA_PRINCIPAL.pack(  # CONVERT_PACKside="left")
            ToolTip.createToolTip(BUTTON_SIGLAS_MAPA_MAPA_PRINCIPAL, "Show/Hide Acronyms on Map")
            self.IMAGE_SAVE_MAPA= PhotoImage.from_pil(self, (Image.open(self.uti.resource_path("img/mapa.png"))).resize((25,25), Image.LANCZOS))
            BUTTON_SAVE_TOOLBAR_MAPA_PRINCIPAL = QPushButton(master=self.TOOLBAR_MAPA_PRINCIPAL,image = self.IMAGE_SAVE_MAPA,command= self.save_extends_MAPA_PRINCIPAL)
            BUTTON_SAVE_TOOLBAR_MAPA_PRINCIPAL.pack(  # CONVERT_PACKside="left")
            ToolTip.createToolTip(BUTTON_SAVE_TOOLBAR_MAPA_PRINCIPAL, "Map Registration")
            self.IMAGE_DEL_MAPA= PhotoImage.from_pil(self, (Image.open(self.uti.resource_path("img/mapa-del.png"))).resize((25,25), Image.LANCZOS))
            BUTTON_DEL_TOOLBAR_MAPA_PRINCIPAL = QPushButton(master=self.TOOLBAR_MAPA_PRINCIPAL,image = self.IMAGE_DEL_MAPA,command= self.del_extends_MAPA_PRINCIPAL)
            BUTTON_DEL_TOOLBAR_MAPA_PRINCIPAL.pack(  # CONVERT_PACKside="left")
            ToolTip.createToolTip(BUTTON_DEL_TOOLBAR_MAPA_PRINCIPAL, "Del Registered Map")



            self.Set_Local_MAPA(self.MAPA)
        Caminho =  self.Dado_config.Settings["INTERFACE"]["sDir_DATA"]
        if not Caminho == "None" and Value_Caminho_Dir.get():
            if os.path.exists(Caminho):
                self.Selecionar_Dir_Data(Caminho)
        self.Listbx_Stations_OBS.configure(state = "disabled")


    def Do_popup_TopLevel_Grafico(self, event):
        try:
            self.Popup_TopLevel_Grafico.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.Popup_TopLevel_Grafico.grab_release()



    def Exibir_Menu_de_Propriedades_dos_Graficos(self,*event):
        try:
            self.Menu_de_Propriedades_dos_Graficos_atual.pack_forget()
            self.AXES_MAPA_PRINCIPAL.figure.canvas.mpl_disconnect(self.ID_Connection_MPL_CANVAS_MAPA_PRINCIPAL)
        except AttributeError:
            print("MENUUUUUUUUUUUUUUUU")
            self.Listbx_Stations_OBS.configure(state = "normal")
            self.plotar_linha_ecuador_magnetico()
            self.Atualizar_DIP_Listabx_Station_OBS(True)
        if self.Value_cb_Modelo_Grafico.get() == "Individual (STD)":
            self.Clear_SELECTION_Plot_SCATTER_and_Listbx()
            self.Listbx_Stations_OBS.configure(selectmode = "single", state = "normal")
            self.ID_Connection_MPL_CANVAS_MAPA_PRINCIPAL = self.AXES_MAPA_PRINCIPAL.figure.canvas.mpl_connect("pick_event", self.Pick_Event_MAPA_PRINCIPAL_SINGLE)
            self.Listbx_Stations_OBS.bind("<<ListboxSelect>>", self.Selecionar_Station_MAPA_SINGLE)  # CONVERT_BIND
            self.Frame_propriedades_modelo_INDIVIDUAL.pack(  # CONVERT_PACKfill="x")
            self.Menu_de_Propriedades_dos_Graficos_atual = self.Frame_propriedades_modelo_INDIVIDUAL
        elif self.Value_cb_Modelo_Grafico.get() == "EIA (STD)":
            self.Listbx_Stations_OBS.configure(selectmode = "multiple", state = "normal")
            self.ID_Connection_MPL_CANVAS_MAPA_PRINCIPAL = self.AXES_MAPA_PRINCIPAL.figure.canvas.mpl_connect("pick_event", self.Pick_Event_MAPA_PRINCIPAL_MULTIPLE)
            self.Listbx_Stations_OBS.bind("<<ListboxSelect>>", self.Selecionar_Station_MAPA_MULTIPLE)  # CONVERT_BIND
            self.Frame_propriedades_modelo_EIA.pack(  # CONVERT_PACKfill="x")
            self.Menu_de_Propriedades_dos_Graficos_atual = self.Frame_propriedades_modelo_EIA
        elif self.Value_cb_Modelo_Grafico.get() == "Desvio (STD)":
            self.Listbx_Stations_OBS.configure(selectmode = "multiple", state = "normal")
            self.ID_Connection_MPL_CANVAS_MAPA_PRINCIPAL = self.AXES_MAPA_PRINCIPAL.figure.canvas.mpl_connect("pick_event", self.Pick_Event_MAPA_PRINCIPAL_MULTIPLE)
            self.Listbx_Stations_OBS.bind("<<ListboxSelect>>", self.Selecionar_Station_MAPA_MULTIPLE)  # CONVERT_BIND
            self.Frame_propriedades_modelo_DESVIO.pack(  # CONVERT_PACKfill="x")
            self.Menu_de_Propriedades_dos_Graficos_atual = self.Frame_propriedades_modelo_DESVIO
        elif self.Value_cb_Modelo_Grafico.get() == "Mapa VTEC/ROTI (CMN)":
            self.Listbx_Stations_OBS.configure(selectmode = "multiple", state = "normal")
            self.ID_Connection_MPL_CANVAS_MAPA_PRINCIPAL = self.AXES_MAPA_PRINCIPAL.figure.canvas.mpl_connect("pick_event", self.Pick_Event_MAPA_PRINCIPAL_MULTIPLE)
            self.Listbx_Stations_OBS.bind("<<ListboxSelect>>", self.Selecionar_Station_MAPA_MULTIPLE)  # CONVERT_BIND
            self.Frame_propriedades_modelo_MAPA.pack(  # CONVERT_PACKfill="x")
            self.Menu_de_Propriedades_dos_Graficos_atual = self.Frame_propriedades_modelo_MAPA
        elif self.Value_cb_Modelo_Grafico.get() == "Painel Mapa VTEC/ROTI (CMN)":
            self.Clear_SELECTION_Plot_SCATTER_and_Listbx()
            self.Listbx_Stations_OBS.configure(selectmode = "multiple", state = "normal")
            self.ID_Connection_MPL_CANVAS_MAPA_PRINCIPAL = self.AXES_MAPA_PRINCIPAL.figure.canvas.mpl_connect("pick_event", self.Pick_Event_MAPA_PRINCIPAL_SINGLE)
            self.Listbx_Stations_OBS.bind("<<ListboxSelect>>", self.Selecionar_Station_MAPA_SINGLE)  # CONVERT_BIND
            self.Frame_propriedades_modelo_PAINEL_MAPA.pack(  # CONVERT_PACKfill="x")
            self.Menu_de_Propriedades_dos_Graficos_atual = self.Frame_propriedades_modelo_PAINEL_MAPA
        elif self.Value_cb_Modelo_Grafico.get() == "ROT/VTEC (CMN)":
            self.Clear_SELECTION_Plot_SCATTER_and_Listbx()
            self.Listbx_Stations_OBS.configure(selectmode = "single", state = "normal")
            self.ID_Connection_MPL_CANVAS_MAPA_PRINCIPAL = self.AXES_MAPA_PRINCIPAL.figure.canvas.mpl_connect("pick_event", self.Pick_Event_MAPA_PRINCIPAL_SINGLE)
            self.Listbx_Stations_OBS.bind("<<ListboxSelect>>", self.Selecionar_Station_MAPA_SINGLE)  # CONVERT_BIND
            self.Frame_propriedades_modelo_ROT.pack(  # CONVERT_PACKfill="x")
            self.Menu_de_Propriedades_dos_Graficos_atual = self.Frame_propriedades_modelo_ROT
        elif self.Value_cb_Modelo_Grafico.get() == "ONDAS (STD)":
            self.Listbx_Stations_OBS.configure(selectmode = "single", state = "normal")
            self.ID_Connection_MPL_CANVAS_MAPA_PRINCIPAL = self.AXES_MAPA_PRINCIPAL.figure.canvas.mpl_connect("pick_event", self.Pick_Event_MAPA_PRINCIPAL_SINGLE)
            self.Listbx_Stations_OBS.bind("<<ListboxSelect>>", self.Selecionar_Station_MAPA_SINGLE)  # CONVERT_BIND
            self.Frame_propriedades_modelo_ONDAS.pack(  # CONVERT_PACKfill="x")
            self.Menu_de_Propriedades_dos_Graficos_atual = self.Frame_propriedades_modelo_ONDAS

    def MAPA_Get_extent_with_zoom(self):
        la = self.AXES_MAPA_PRINCIPAL.get_ylim()
        lo = self.AXES_MAPA_PRINCIPAL.get_xlim()
        return [lo[0],lo[1],la[0],la[1]]

    def MAPA_Get_extent(self, Mapa=None):
        try:
            if Mapa:
                Local_MAPA = self.Lista_Locais_MAPA[self.Lista_Nomes_Locais.index(Mapa)]
            else:
                print(self.Value_cb_Local_MAPA.get())    
                Local_MAPA = self.Lista_Locais_MAPA[self.Lista_Nomes_Locais.index(self.Value_cb_Local_MAPA.get())]
        except ValueError:Local_MAPA = ""
        return Local_MAPA

    def Set_Dados_MAPA_VTEC_ROTI(self, *event, Mapa=None):
        valor_combo_mapa_VTEC_ROTI = self.CB_DADOS_MAPA_VTEC_ROTI.get()
        if valor_combo_mapa_VTEC_ROTI:
            self.Frame_propriedades_MAPA_VTEC.pack_forget()
            self.Frame_propriedades_MAPA_ROTI.pack_forget()
            self.Frame_propriedades_MAPA_ROT.pack_forget()
            if valor_combo_mapa_VTEC_ROTI == "VTEC":self.Frame_propriedades_MAPA_VTEC.pack(  # CONVERT_PACKfill="x")
            elif valor_combo_mapa_VTEC_ROTI == "ROT":self.Frame_propriedades_MAPA_ROT.pack(  # CONVERT_PACKfill="x")
            elif valor_combo_mapa_VTEC_ROTI == "ROTI":self.Frame_propriedades_MAPA_ROTI.pack(  # CONVERT_PACKfill="x")
    
    def Set_Dados_PAINEL_MAPA_VTEC_ROTI(self, *event, Mapa=None):
        valor_combo_painel_mapa_VTEC_ROTI = self.CB_DADOS_PAINEL_MAPA_VTEC_ROTI.get()
        if valor_combo_painel_mapa_VTEC_ROTI:
            self.Frame_propriedades_PAINEL_MAPA_ROT.pack_forget()
            self.Frame_propriedades_PAINEL_MAPA_ROTI.pack_forget()
            if valor_combo_painel_mapa_VTEC_ROTI == "ROT":self.Frame_propriedades_PAINEL_MAPA_ROT.pack(  # CONVERT_PACKfill="x")
            elif valor_combo_painel_mapa_VTEC_ROTI == "ROTI":self.Frame_propriedades_PAINEL_MAPA_ROTI.pack(  # CONVERT_PACKfill="x")
    def Set_Dados_ROT(self, *event, Mapa=None):
        valor_combo_painel_mapa_VTEC_ROTI = self.CB_DADOS_ROT.get()





    def Set_Local_MAPA(self, *event, Mapa=None):
        if self.Lista_Locais_MAPA:
            
            self.AXES_MAPA_PRINCIPAL.set_extent(self.MAPA_Get_extent(Mapa),crs=ccrs.PlateCarree())	
            self.CANVAS_MAPA_PRINCIPAL.draw()
            self.Dado_config.Settings["INTERFACE"]["sMap"] = self.Value_cb_Local_MAPA.get()

    def Pick_Event_MAPA_PRINCIPAL_SINGLE(self, event):
        id_Station = int(event.artist.get_label())
        if (event.artist.get_facecolors() == [[1, 0, 0, 1]]).all():
            try:
                self.List_Scatter_OBS_Station[self.List_Selection_Listbx_OBS_Station[0]].set_facecolors('red')
                self.UPDATE_Artist(self.List_Scatter_OBS_Station[self.List_Selection_Listbx_OBS_Station[0]])
                self.Unsel_Listbx_Stations_OBS(self.List_Selection_Listbx_OBS_Station[0])
                event.artist.set_facecolors('green')
                self.Sel_Listbx_Stations_OBS(id_Station)
            except IndexError:
                event.artist.set_facecolors('green')
                self.Sel_Listbx_Stations_OBS(id_Station)
        else:
            self.Unsel_Listbx_Stations_OBS(id_Station)
            event.artist.set_facecolors('red')
        self.UPDATE_Artist(event.artist)
    
    def Pick_Event_MAPA_PRINCIPAL_MULTIPLE(self, event):
        id_Station = int(event.artist.get_label())
        if (event.artist.get_facecolors() == [[1, 0, 0, 1]]).all():
            event.artist.set_facecolors('green')
            self.Sel_Listbx_Stations_OBS(id_Station)
        else:
            event.artist.set_facecolors('red')
            self.Unsel_Listbx_Stations_OBS(id_Station)
        self.UPDATE_Artist(event.artist)

    def Selecionar_Station_MAPA_MULTIPLE(self, *event):
        Indice_Last_selection = list(set(self.Listbx_Stations_OBS.curselection()) - set(self.List_Selection_Listbx_OBS_Station))
        if Indice_Last_selection:
            try:
                self.List_Selection_Listbx_OBS_Station = list(self.Listbx_Stations_OBS.curselection())
                self.List_Scatter_OBS_Station[Indice_Last_selection[0]].set_facecolors('green')
            except IndexError:pass
            self.Cont_Station_Selecionadas_Lista.set(self.Cont_Station_Selecionadas_Lista.get()+1)
        else:
            Indice_Last_selection = list(set(self.List_Selection_Listbx_OBS_Station) -  set(self.Listbx_Stations_OBS.curselection()))
            try:
                self.List_Selection_Listbx_OBS_Station = list(self.Listbx_Stations_OBS.curselection())
                self.List_Scatter_OBS_Station[Indice_Last_selection[0]].set_facecolors('red')
            except IndexError:pass
            self.Cont_Station_Selecionadas_Lista.set(self.Cont_Station_Selecionadas_Lista.get()-1)
        try:self.UPDATE_Artist(self.List_Scatter_OBS_Station[Indice_Last_selection[0]])
        except IndexError:pass
    
    def Selecionar_Station_MAPA_SINGLE(self, *event):
        try:
            self.List_Scatter_OBS_Station[self.List_Selection_Listbx_OBS_Station[0]].set_facecolors('red')
            self.UPDATE_Artist(self.List_Scatter_OBS_Station[self.List_Selection_Listbx_OBS_Station[0]])
        except IndexError:pass
        self.List_Selection_Listbx_OBS_Station = list(self.Listbx_Stations_OBS.curselection())
        try:
            self.List_Scatter_OBS_Station[self.List_Selection_Listbx_OBS_Station[0]].set_facecolors('green')
            self.UPDATE_Artist(self.List_Scatter_OBS_Station[self.List_Selection_Listbx_OBS_Station[0]])
        except IndexError:pass
        self.Cont_Station_Selecionadas_Lista.set(1)

    def Sel_Listbx_Stations_OBS(self,id_Station):
        self.Listbx_Stations_OBS.select_set(id_Station)
        self.List_Selection_Listbx_OBS_Station.append(id_Station)
        self.Cont_Station_Selecionadas_Lista.set(self.Cont_Station_Selecionadas_Lista.get()+1)

    def Unsel_Listbx_Stations_OBS(self,id_Station):
        self.Listbx_Stations_OBS.select_clear(id_Station)
        del(self.List_Selection_Listbx_OBS_Station[self.List_Selection_Listbx_OBS_Station.index(id_Station)])
        self.Cont_Station_Selecionadas_Lista.set(self.Cont_Station_Selecionadas_Lista.get()-1)

    def UPDATE_Line_Ecuador(self, current, new_x, new_y, New_ANO_DIP):
        self.background = self.FIGURA_MAPA_PRINCIPAL.canvas.copy_from_bbox(self.FIGURA_MAPA_PRINCIPAL.bbox)
        self.FIGURA_MAPA_PRINCIPAL.canvas.restore_region(self.background)
        current.set_data(new_x,new_y)
        current.set_label(New_ANO_DIP)
        self.AXES_MAPA_PRINCIPAL.draw_artist(self.Linha_Equador_Magnetico_MAPA_PRINCIPAL)
        self.FIGURA_MAPA_PRINCIPAL.canvas.blit(self.FIGURA_MAPA_PRINCIPAL.bbox)
        self.CANVAS_MAPA_PRINCIPAL.draw()

    def UPDATE_Artist(self, current):
        self.background = self.FIGURA_MAPA_PRINCIPAL.canvas.copy_from_bbox(self.FIGURA_MAPA_PRINCIPAL.bbox)
        self.FIGURA_MAPA_PRINCIPAL.canvas.restore_region(self.background)
        self.AXES_MAPA_PRINCIPAL.draw_artist(current)
        self.FIGURA_MAPA_PRINCIPAL.canvas.blit(self.FIGURA_MAPA_PRINCIPAL.bbox)

    def plotar_linha_ecuador_magnetico(self, Ano_FOR_DIP = None):
        try:
            if not Ano_FOR_DIP:Ano_FOR_DIP = int(self.Value_DATA_entry_main_inicio.get()[-4:])
            self.Coordenadas_equador_Magnetico_X = []
            self.Coordenadas_equador_Magnetico_Y = []
            
            for x in np.arange(-180,181,1):
                inclinacao = self.uti.get_inclinacao(300, Ano_FOR_DIP, 0, 0, x, 0)
                diplat = -(math.degrees(math.atan(((math.tan(math.radians(float(inclinacao)))/2)))))
                self.Coordenadas_equador_Magnetico_X.append(x)
                self.Coordenadas_equador_Magnetico_Y.append(diplat)
                
                
                
            
            self.UPDATE_Line_Ecuador(self.Linha_Equador_Magnetico_MAPA_PRINCIPAL, self.Coordenadas_equador_Magnetico_X, self.Coordenadas_equador_Magnetico_Y, Ano_FOR_DIP)
        except AttributeError:			
            self.habilitar_DIP_lista_estacoes.set(True)
            self.Linha_Equador_Magnetico_MAPA_PRINCIPAL = self.AXES_MAPA_PRINCIPAL.plot(self.Coordenadas_equador_Magnetico_X, self.Coordenadas_equador_Magnetico_Y, 'k', gid = "Line_Ecuador_mag", label = Ano_FOR_DIP)[0]
            self.UPDATE_Artist(self.Linha_Equador_Magnetico_MAPA_PRINCIPAL)
            
            

    def activateROTLegend(self):
        if self.Value_Line_Cores.get():self.Frame_propriedades_modelo_ROT_Check_Legenda.pack(  # CONVERT_PACKfill="x")
        else:self.Frame_propriedades_modelo_ROT_Check_Legenda.pack_forget()

    def call_windows(self, UI_id):
        self.master.withdraw()
        if UI_id == 'ordena': Ordena(self.master)
        if UI_id == 'igrf12': Geradordeinclinacao(self.master)
        if UI_id == 'registro_est': CadObs(self.master)
        

    def Clear_SELECTION_Plot_SCATTER_and_Listbx(self):
        for Index_Selection_Listbx_OBS_Station in self.List_Selection_Listbx_OBS_Station:
            try:
                self.List_Scatter_OBS_Station[Index_Selection_Listbx_OBS_Station].set_facecolors('red')
                self.UPDATE_Artist(self.List_Scatter_OBS_Station[Index_Selection_Listbx_OBS_Station])
            except IndexError:pass
        self.List_Selection_Listbx_OBS_Station = []
        self.Cont_Station_Selecionadas_Lista.set(0)
        self.Listbx_Stations_OBS.select_clear(0, END)
        
    def Save_SELECTION_Plot_SCATTER_and_Listbx(self):
        with open((self.filedir.get()  + ("/Estacoes_usadas.txt")), 'w', encoding = "UTF-8") as arquivoEst:
            for Index_Selection_Listbx_OBS_Station in range(len(self.List_Selection_Listbx_OBS_Station)):
                arquivoEst.write(self.Listbx_Stations_OBS.get(self.List_Selection_Listbx_OBS_Station[Index_Selection_Listbx_OBS_Station])+'\n')
                

    def Clear_Listbx_OBS_and_Plot_SCATTER(self):
        for (Scatter_OBS_Station,Annotate_OBS_Station) in zip(self.List_Scatter_OBS_Station,self.List_Annotate_OBS_Station):
            Scatter_OBS_Station.remove()
            Annotate_OBS_Station.remove()
        self.List_Selection_Listbx_OBS_Station = []
        self.List_Scatter_OBS_Station = []
        self.List_Annotate_OBS_Station = []
        self.Listbx_Stations_OBS.select_clear(0, END)
        self.Listbx_Stations_OBS.delete(0,'end')
        self.Cont_Station_Selecionadas_Lista.set(0)

    def Aplicar_Filtro_Dir_station_OBS(self):
        if self.Value_Check_Filter.get():self.Dado_config.Settings["INTERFACE"]["iFiltro"] = 1
        else:self.Dado_config.Settings["INTERFACE"]["iFiltro"] = 0
        if self.filedir.get():
            try:
                self.Clear_Listbx_OBS_and_Plot_SCATTER()
                if self.Value_Check_Filter.get():
                    self.Lista_Estacoes_NAO_Cadastradas, self.Listas_String_Estacoes_Cadastradas, self.Listas_Estacoes_Cadastradas = self.uti.Refresh_list_obs(self.filedir.get(), int(self.Value_DATA_entry_main_inicio.get()[-4:]), self.Value_Check_Filter.get(), self.habilitar_DIP_lista_estacoes.get(), True)
                    self.Listas_Estacoes_Cadastradas.sort();self.Listas_String_Estacoes_Cadastradas.sort()
                    [self.Listbx_Stations_OBS.insert(END, item) for item in self.Listas_String_Estacoes_Cadastradas]
                    [self.Listbx_Stations_OBS.insert(END, item + " ("+ self.Dado_config.idioma(144) +")") for item in self.Lista_Estacoes_NAO_Cadastradas]
                    self.texto.set(self.Dado_config.idioma(113)+" ["+str(len(self.Listas_String_Estacoes_Cadastradas))+"]")
                else:
                    self.Listas_String_Estacoes_Cadastradas, self.Listas_Estacoes_Cadastradas = self.uti.Refresh_list_obs(self.filedir.get(), int(self.Value_DATA_entry_main_inicio.get()[-4:]), self.Value_Check_Filter.get(), self.habilitar_DIP_lista_estacoes.get(), True)
                    self.Listas_Estacoes_Cadastradas.sort();self.Listas_String_Estacoes_Cadastradas.sort()
                    [self.Listbx_Stations_OBS.insert(END, item) for item in self.Listas_String_Estacoes_Cadastradas]
                    self.texto.set(self.Dado_config.idioma(113)+" ["+str(len(self.Listas_String_Estacoes_Cadastradas))+"]")
                for id_Station, lista in enumerate(self.Listas_Estacoes_Cadastradas):
                    Lat_Station = float(lista[1])
                    Lon_Station = float(lista[2])
                    self.List_Scatter_OBS_Station.append(self.AXES_MAPA_PRINCIPAL.scatter(Lon_Station, Lat_Station, facecolor = 'red', picker = 2, s = 20, norm = 1, gid = "Station", zorder = 3, label = id_Station))
                    self.List_Annotate_OBS_Station.append(self.AXES_MAPA_PRINCIPAL.annotate(lista[0], (Lon_Station+.15, Lat_Station)))
                self.CANVAS_MAPA_PRINCIPAL.draw()
            except FileNotFoundError :
                pass

    def Atualizar_DIP_Listabx_Station_OBS(self, Fano=False, *event):
        ANO_DIP_STATIONS_OBS = self.calendario_modelo_grafico_INDIVIDUAL.get_date().year
        print(ANO_DIP_STATIONS_OBS,int(self.Linha_Equador_Magnetico_MAPA_PRINCIPAL.get_label()),self.filedir.get(),Fano)
        if ((not int(self.Linha_Equador_Magnetico_MAPA_PRINCIPAL.get_label()) == ANO_DIP_STATIONS_OBS and self.filedir.get())) or (Fano == True):
            back_list = self.Listbx_Stations_OBS.curselection()
            self.Listbx_Stations_OBS.delete(0, END)
            if self.Value_Check_Filter.get():
                self.Lista_Estacoes_NAO_Cadastradas, self.Listas_String_Estacoes_Cadastradas, self.Listas_Estacoes_Cadastradas = self.uti.Refresh_list_obs(self.filedir.get(), ANO_DIP_STATIONS_OBS,self.Value_Check_Filter.get(), True, True)
                self.Listas_Estacoes_Cadastradas.sort(); self.Listas_String_Estacoes_Cadastradas.sort()
                [self.Listbx_Stations_OBS.insert(END, item) for item in self.Listas_String_Estacoes_Cadastradas]
                [self.Listbx_Stations_OBS.insert(END, item + " ("+ self.Dado_config.idioma(144) +")") for item in self.Lista_Estacoes_NAO_Cadastradas]
                self.texto.set(self.Dado_config.idioma(113)+" ["+str(len(self.Listas_String_Estacoes_Cadastradas))+"]")
            else:
                self.Listas_String_Estacoes_Cadastradas, self.Listas_Estacoes_Cadastradas = self.uti.Refresh_list_obs(self.filedir.get(), ANO_DIP_STATIONS_OBS,self.Value_Check_Filter.get(), True, True)
                self.Listas_Estacoes_Cadastradas.sort();  self.Listas_String_Estacoes_Cadastradas.sort()
                [self.Listbx_Stations_OBS.insert(END, item) for item in self.Listas_String_Estacoes_Cadastradas]
                self.texto.set(self.Dado_config.idioma(113)+" ["+str(len(self.Listas_String_Estacoes_Cadastradas))+"]")
            self.plotar_linha_ecuador_magnetico()
            self.Value_DATA_entry_main_fim.set(self.Value_DATA_entry_main_inicio.get())
            [self.Listbx_Stations_OBS.select_set(ids) for ids in back_list]
            Fano=False

    def Selecionar_Dir_Data(self, File_dir = None):
        if not File_dir:File_dir = tk.filedialog.askdirectory(initialdir = "c:/", title = self.Dado_config.idioma(40), parent = self.master)
        if (File_dir and not File_dir == self.filedir.get()) or (File_dir and self.habilitar_DIP_lista_estacoes.get()):
            self.filedir.set(File_dir)
            Listbx_Stations_OBS_desabilitada = False
            a=(list(set([arquivos.upper() for arquivos in os.listdir(File_dir)if (arquivos.lower().endswith("cmn") or arquivos.lower().endswith("std"))])))
            x=a[0]
            ano=x[8:12]; mes=x[13:15];dia=x[16:18]
            dt=date(int(ano),int(mes),int(dia))
            
            
            
            
            self.Value_DATA_entry_main_inicio.set((dia)+"/"+(mes)+"/"+(ano))
            self.Value_DATA_entry_main_fim.set((dia)+"/"+(mes)+"/"+(ano))
            
            if self.Listbx_Stations_OBS["state"] == "disabled":
                Listbx_Stations_OBS_desabilitada = True
                self.Listbx_Stations_OBS.config(state = "normal")
            self.Clear_Listbx_OBS_and_Plot_SCATTER()
            if self.Value_Check_Filter.get():
                self.Lista_Estacoes_NAO_Cadastradas, self.Listas_String_Estacoes_Cadastradas, self.Listas_Estacoes_Cadastradas = self.uti.Refresh_list_obs(self.filedir.get(), int(self.Value_DATA_entry_main_inicio.get()[-4:]), self.Value_Check_Filter.get(), self.habilitar_DIP_lista_estacoes.get(), True)
                self.Listas_Estacoes_Cadastradas.sort(); self.Listas_String_Estacoes_Cadastradas.sort()
                self.texto.set(self.Dado_config.idioma(113)+" ["+str(len(self.Listas_String_Estacoes_Cadastradas))+"]")
                [self.Listbx_Stations_OBS.insert(END, item) for item in self.Listas_String_Estacoes_Cadastradas]
                [self.Listbx_Stations_OBS.insert(END, item + " ("+ self.Dado_config.idioma(144) +")") for item in self.Lista_Estacoes_NAO_Cadastradas]
            else:
                self.Listas_String_Estacoes_Cadastradas, self.Listas_Estacoes_Cadastradas = self.uti.Refresh_list_obs(self.filedir.get(), int(self.Value_DATA_entry_main_inicio.get()[-4:]), self.Value_Check_Filter.get(), self.habilitar_DIP_lista_estacoes.get(), True)
                self.Listas_Estacoes_Cadastradas.sort();self.Listas_String_Estacoes_Cadastradas.sort()
                [self.Listbx_Stations_OBS.insert(END, item) for item in self.Listas_String_Estacoes_Cadastradas]
                self.texto.set(self.Dado_config.idioma(113)+" ["+str(len(self.Listas_String_Estacoes_Cadastradas))+"]")
            ToolTip.createToolTip(self.Label_String_dir, self.filedir.get())
            for id_Station, lista in enumerate(self.Listas_Estacoes_Cadastradas):
                Lat_Station = float(lista[1])
                Lon_Station = float(lista[2])
                self.List_Scatter_OBS_Station.append(self.AXES_MAPA_PRINCIPAL.scatter(Lon_Station, Lat_Station, facecolor = 'red', picker = 2, s = 20, norm = 1, gid = "Station", zorder = 3, label = id_Station))
                self.List_Annotate_OBS_Station.append(self.AXES_MAPA_PRINCIPAL.annotate(lista[0], (Lon_Station+.15, Lat_Station)))
            self.Value_Mostrar_Estacoes_MAPA_PRINCIPAL.set(True)
            self.String_Label_dir.set(self.filedir.get())
            self.Label_String_dir.config(bg = "white")
            self.cb_modelo_grafico.config(state = 'readonly')
            if Listbx_Stations_OBS_desabilitada:
                self.Listbx_Stations_OBS.config(state = "disabled")
                Listbx_Stations_OBS_desabilitada = False
            self.Dado_config.Settings["INTERFACE"]["sDir_DATA"] = self.filedir.get()
            self.CANVAS_MAPA_PRINCIPAL.draw()

    def AJUSTAR_CANVAS_JANELA_TOPLEVEL_GRAFICO(self, *event):
        self.FIGURA_TOPLEVEL_GRAFICO.tight_layout()
        self.FIGURA_TOPLEVEL_GRAFICO.subplots_adjust(hspace=0,wspace=0)
        self.CANVAS_JANELA_TOPLEVEL_GRAFICO.draw()
        self.Dado_config.Settings[self.plot_ATIVO]["fTop"]=self.FIGURA_TOPLEVEL_GRAFICO.subplotpars.top
        self.Dado_config.Settings[self.plot_ATIVO]["fBottom"]=self.FIGURA_TOPLEVEL_GRAFICO.subplotpars.bottom
        self.Dado_config.Settings[self.plot_ATIVO]["fLeft"]=self.FIGURA_TOPLEVEL_GRAFICO.subplotpars.left
        self.Dado_config.Settings[self.plot_ATIVO]["fRight"]=self.FIGURA_TOPLEVEL_GRAFICO.subplotpars.right
        self.Dado_config.Settings[self.plot_ATIVO]["fHspace"]=self.FIGURA_TOPLEVEL_GRAFICO.subplotpars.hspace
        self.Dado_config.Settings[self.plot_ATIVO]["fWspace"]=self.FIGURA_TOPLEVEL_GRAFICO.subplotpars.wspace
        size_inches_fig_width,size_inches_fig_height=self.FIGURA_TOPLEVEL_GRAFICO.get_size_inches()
        self.Dado_config.Settings[self.plot_ATIVO]["fSize_inches_fig_width"]=size_inches_fig_width
        self.Dado_config.Settings[self.plot_ATIVO]["fSize_inches_fig_height"]=size_inches_fig_height

    def ATUALIZAR_CANVAS_JANELA_TOPLEVEL_GRAFICO(self, *event):
        try:
            print("|setando tamanho|")
            print(self.plot_ATIVO)
            print("self.Dado_config.Settings[self.plot_ATIVO][fTop]")
            print(self.Dado_config.Settings[self.plot_ATIVO]["fTop"])
            if ((self.Dado_config.Settings[self.plot_ATIVO]["fTop"] == None) and (self.Dado_config.Settings[self.plot_ATIVO]["fBottom"] == None) and (self.Dado_config.Settings[self.plot_ATIVO]["fLeft"] == None) and (self.Dado_config.Settings[self.plot_ATIVO]["fRight"] == None) and (self.Dado_config.Settings[self.plot_ATIVO]["fHspace"] == None) and (self.Dado_config.Settings[self.plot_ATIVO]["fWspace"] == None)):
                self.FIGURA_TOPLEVEL_GRAFICO.tight_layout()
                self.FIGURA_TOPLEVEL_GRAFICO.subplots_adjust(hspace=0,wspace=0)
                self.Dado_config.Settings[self.plot_ATIVO]["fTop"]=self.FIGURA_TOPLEVEL_GRAFICO.subplotpars.top
                self.Dado_config.Settings[self.plot_ATIVO]["fBottom"]=self.FIGURA_TOPLEVEL_GRAFICO.subplotpars.bottom
                self.Dado_config.Settings[self.plot_ATIVO]["fLeft"]=self.FIGURA_TOPLEVEL_GRAFICO.subplotpars.left
                self.Dado_config.Settings[self.plot_ATIVO]["fRight"]=self.FIGURA_TOPLEVEL_GRAFICO.subplotpars.right
                self.Dado_config.Settings[self.plot_ATIVO]["fHspace"]=self.FIGURA_TOPLEVEL_GRAFICO.subplotpars.hspace
                self.Dado_config.Settings[self.plot_ATIVO]["fWspace"]=self.FIGURA_TOPLEVEL_GRAFICO.subplotpars.wspace
                size_inches_fig_width,size_inches_fig_height=self.FIGURA_TOPLEVEL_GRAFICO.get_size_inches()
                self.Dado_config.Settings[self.plot_ATIVO]["fSize_inches_fig_width"]=size_inches_fig_width
                self.Dado_config.Settings[self.plot_ATIVO]["fSize_inches_fig_height"]=size_inches_fig_height
            else:
                self.FIGURA_TOPLEVEL_GRAFICO.subplots_adjust(
                    top=self.Dado_config.Settings[self.plot_ATIVO]["fTop"],
                    bottom=self.Dado_config.Settings[self.plot_ATIVO]["fBottom"],
                    left=self.Dado_config.Settings[self.plot_ATIVO]["fLeft"],
                    right=self.Dado_config.Settings[self.plot_ATIVO]["fRight"],
                    hspace=self.Dado_config.Settings[self.plot_ATIVO]["fHspace"],
                    wspace=self.Dado_config.Settings[self.plot_ATIVO]["fWspace"]
                )
            self.CANVAS_JANELA_TOPLEVEL_GRAFICO.draw()
            print("|setando tamanho|")
        except Exception as e:
            print(e)

    def THREAD_PLOTAR_GRAFICO_JANELA_TOPLEVEL_GRAFICO(self, graph = None, *event):
        self.PLOTAR_GRAFICO_JANELA_TOPLEVEL_GRAFICO(graph, event)

        
        pass

    def PLOTAR_GRAFICO_JANELA_TOPLEVEL_GRAFICO(self, graph = None, *event):
        if not graph:graph = self.Value_cb_Modelo_Grafico.get()
        if self.filedir.get():
            if len(self.Listbx_Stations_OBS.curselection()) > 0 or graph in ("Mapa VTEC/ROTI (CMN)", "MAPA") or graph in ("Painel Mapa VTEC/ROTI (CMN)","PAINEL MAPA"):
                if graph in ("Individual (STD)","INDIVIDUAL"):self.PLOTAR_GRAFICO_JANELA_TOPLEVEL_GRAFICO_INDIVIDUAL()
                elif graph in ("EIA (STD)" ,"EIA"):self.PLOTAR_GRAFICO_JANELA_TOPLEVEL_GRAFICO_EIA()
                elif graph in ("Desvio (STD)" ,"DESVIO"):self.PLOTAR_GRAFICO_JANELA_TOPLEVEL_GRAFICO_DESVIO()
                elif graph in ("Mapa VTEC/ROTI (CMN)" ,"MAPA"):self.PLOTAR_GRAFICO_JANELA_TOPLEVEL_GRAFICO_MAPA()
                elif graph in ("Painel Mapa VTEC/ROTI (CMN)","PAINEL MAPA"):self.PLOTAR_GRAFICO_JANELA_TOPLEVEL_GRAFICO_PAINEL_MAPA()
                elif graph in ("ROT/VTEC (CMN)" ,"ROT"):self.PLOTAR_GRAFICO_JANELA_TOPLEVEL_GRAFICO_ROT()
                elif graph in ("ONDAS (STD)" ,"ONDAS"):self.PLOTAR_GRAFICO_JANELA_TOPLEVEL_GRAFICO_ONDAS()
        else:tk.messagebox.showerror(self.Dado_config.idioma(49),self.Dado_config.idioma(126), parent = self.master)

    def PLOTAR_GRAFICO_JANELA_TOPLEVEL_GRAFICO_INDIVIDUAL(self):
        IDS_JANELA_TOPLEVEL_GRAFICO_INDIVIDUAL = self.Listbx_Stations_OBS.curselection()
        if IDS_JANELA_TOPLEVEL_GRAFICO_INDIVIDUAL:
            SIGLA_ESTACAO_FIGURA_TOPLEVEL_GRAFICO_INDIVIDUAL = self.Listbx_Stations_OBS.get(IDS_JANELA_TOPLEVEL_GRAFICO_INDIVIDUAL)[:4]
            try:
                data_Inicial_GRAFICO_JANELA_TOPLEVEL_GRAFICO_INDIVIDUAL = datetime.strptime(self.Value_DATA_entry_main_inicio.get(), '%d/%m/%Y')
                data_Final_GRAFICO_JANELA_TOPLEVEL_GRAFICO_INDIVIDUAL = datetime.strptime(self.Value_DATA_entry_main_fim.get(), '%d/%m/%Y')
            except ValueError:
                tk.messagebox.showerror(self.Dado_config.idioma(49), self.Dado_config.idioma(176), parent = self.master)
                return False
            self.GRAFICO_Individual = COMP_INDV(self.FIGURA_TOPLEVEL_GRAFICO, SIGLA_ESTACAO_FIGURA_TOPLEVEL_GRAFICO_INDIVIDUAL, data_Inicial_GRAFICO_JANELA_TOPLEVEL_GRAFICO_INDIVIDUAL, data_Final_GRAFICO_JANELA_TOPLEVEL_GRAFICO_INDIVIDUAL, self.filedir.get(), self.Value_Formato_DATA_Grafico,self.Dado_config)
            self.GRAFICO_Individual._set_Matplotlib_grafico()
            self.FIGURA_TOPLEVEL_GRAFICO,self.AXES_TOPLEVEL_GRAFICO,self.COLORBAR_TOPLEVEL_GRAFICO,self.TITULO_TOPLEVEL_GRAFICO,self.DIAS_TEC_JANELA_TOPLEVEL_GRAFICO_INDIVIDUAL,self.Matriz_STD_DADOS_JANELA_TOPLEVEL_GRAFICO_INDIVIDUAL,self.matrizdias_indv = self.GRAFICO_Individual._get_Matplotlib_grafico_att()
            self.Cont_Line_Horas_JANELA_TOPLEVEL_GRAFICO = 0
            self.plot_ATIVO = "INDIVIDUAL"
            self.SALVAR_MATRIZ_DADOS_GRAFICO_JANELA_TOPLEVEL_GRAFICO()
            self.Exibir_Toplevel_GRAFICO()            
            
            self.ATUALIZAR_CANVAS_JANELA_TOPLEVEL_GRAFICO()
    
    def PLOTAR_GRAFICO_JANELA_TOPLEVEL_GRAFICO_EIA(self):
        IDS_JANELA_TOPLEVEL_GRAFICO_EIA = self.Listbx_Stations_OBS.curselection()
        if len(IDS_JANELA_TOPLEVEL_GRAFICO_EIA) > 1:
            try:
                self.data_Inicial_GRAFICO_JANELA_TOPLEVEL_GRAFICO_EIA = datetime.strptime(self.Value_DATA_entry_main_inicio.get(), '%d/%m/%Y')
                self.data_Final_GRAFICO_JANELA_TOPLEVEL_GRAFICO_EIA = datetime.strptime(self.Value_DATA_entry_main_fim.get(), '%d/%m/%Y')
            except ValueError:
                tk.messagebox.showerror(self.Dado_config.idioma(49), self.Dado_config.idioma(176), parent = self.master)
                return False
            self.SIGLAS_GRAFICO_JANELA_TOPLEVEL_GRAFICO_EIA = []
            for iten_id in IDS_JANELA_TOPLEVEL_GRAFICO_EIA:
                item_line = self.Listbx_Stations_OBS.get(iten_id).replace('(','').replace(')','').replace('\n','').replace(',','')
                item_line = item_line.split(' ')
                try:self.SIGLAS_GRAFICO_JANELA_TOPLEVEL_GRAFICO_EIA.append([item_line[0],float(item_line[1]),float(item_line[2]),float(item_line[3])])
                except ValueError:pass
            self.GRAFICO_Eia = COMP_EIA(self.FIGURA_TOPLEVEL_GRAFICO,self.SIGLAS_GRAFICO_JANELA_TOPLEVEL_GRAFICO_EIA,self.filedir.get(),self.data_Inicial_GRAFICO_JANELA_TOPLEVEL_GRAFICO_EIA,self.data_Final_GRAFICO_JANELA_TOPLEVEL_GRAFICO_EIA,self.Value_Lat_Dip_axes_Y.get(), self.Value_station_on_TICK.get(),self.Dado_config)
            self.GRAFICO_Eia._set_Matplotlib_grafico()
            self.FIGURA_TOPLEVEL_GRAFICO, self.AXES_TOPLEVEL_GRAFICO ,self.COLORBAR_TOPLEVEL_GRAFICO, self.TITULO_TOPLEVEL_GRAFICO ,self.Matriz_STD_DADOS_JANELA_TOPLEVEL_GRAFICO_EIA, self.EIXOG_JANELA_TOPLEVEL_GRAFICO_EIA = self.GRAFICO_Eia._get_Matplotlib_grafico_att()
            self.plot_ATIVO = "EIA"
            self.SALVAR_MATRIZ_DADOS_GRAFICO_JANELA_TOPLEVEL_GRAFICO()     
            self.SALVAR_IMAGEM_DADOS_GRAFICO_JANELA_TOPLEVEL_GRAFICO()
            self.Exibir_Toplevel_GRAFICO()
            self.ATUALIZAR_CANVAS_JANELA_TOPLEVEL_GRAFICO()

    def PLOTAR_GRAFICO_JANELA_TOPLEVEL_GRAFICO_DESVIO(self):
        IDS_JANELA_TOPLEVEL_GRAFICO_DESVIO = self.Listbx_Stations_OBS.curselection()
        try:
            data_Inicial_GRAFICO_JANELA_TOPLEVEL_GRAFICO_DESVIO = datetime.strptime(self.Value_DATA_entry_main_inicio.get(), '%d/%m/%Y')
            data_Final_GRAFICO_JANELA_TOPLEVEL_GRAFICO_DESVIO = datetime.strptime(self.Value_DATA_entry_main_fim.get(), '%d/%m/%Y')
        except ValueError:
            tk.messagebox.showerror(self.Dado_config.idioma(49), self.Dado_config.idioma(176), parent = self.master)
            return False

        self.SIGLAS_GRAFICO_JANELA_TOPLEVEL_GRAFICO_DESVIO = []	
        for iten_id in IDS_JANELA_TOPLEVEL_GRAFICO_DESVIO:
            item_line = ((self.Listbx_Stations_OBS.get(iten_id)).replace('(','')).replace(')','')
            item_line = item_line.split(",")
            est_lat = item_line[0].split(' ')
            estacao = est_lat[0]
            lati = est_lat[1]
            long = item_line[1]
            dip = item_line[2]
            self.SIGLAS_GRAFICO_JANELA_TOPLEVEL_GRAFICO_DESVIO.append([estacao.strip(),lati.strip(),long.strip(),dip.strip()])
        
        self.SIGLAS_GRAFICO_JANELA_TOPLEVEL_GRAFICO_DESVIO.sort(key=lambda x: float(x[3]),reverse=True)

        self.GRAFICO_Desvio = COMP_DESVIO(self.FIGURA_TOPLEVEL_GRAFICO,self.filedir.get(),self.SIGLAS_GRAFICO_JANELA_TOPLEVEL_GRAFICO_DESVIO,self.Calendario_Dias_Calmos.selection_get(),data_Inicial_GRAFICO_JANELA_TOPLEVEL_GRAFICO_DESVIO,data_Final_GRAFICO_JANELA_TOPLEVEL_GRAFICO_DESVIO,self.Value_Formato_DATA_Grafico.get(),self.Dado_config)
        self.GRAFICO_Desvio._set_Matplotlib_grafico()
        self.FIGURA_TOPLEVEL_GRAFICO,self.AXES_TOPLEVEL_GRAFICO,self.TITULO_TOPLEVEL_GRAFICO,self.Matriz_STD_DADOS_JANELA_TOPLEVEL_GRAFICO_DESVIO,self.LISTA_DESVIOPD_TEC,self.LISTA_MEDIA_TEC,self.DELTA_DAYS_DESVIO,self.LISTA_HORAS_DEVIO,self.DATAS_EIXO_X_GRAFICO_DESVIO = self.GRAFICO_Desvio._get_Matplotlib_grafico_att()
        self.Cont_Line_Horas_JANELA_TOPLEVEL_GRAFICO = 0

        self.plot_ATIVO = "DESVIO"
        self.ID_Connection_MPL_CANVAS_MAPA_TOPLEVEL_ROT_LINHAS=self.FIGURA_TOPLEVEL_GRAFICO.canvas.mpl_connect('button_press_event', self.Thread_LINHAS_UT_GRAFICO_JANELA_TOPLEVEL_GRAFICO)
        self.SALVAR_MATRIZ_DADOS_GRAFICO_JANELA_TOPLEVEL_GRAFICO()
        self.Exibir_Toplevel_GRAFICO()
        self.ATUALIZAR_CANVAS_JANELA_TOPLEVEL_GRAFICO()
        
    def PLOTAR_GRAFICO_JANELA_TOPLEVEL_GRAFICO_ONDAS(self):
        IDS_JANELA_TOPLEVEL_GRAFICO_ONDAS = self.Listbx_Stations_OBS.curselection()
        try:
            data_Inicial_GRAFICO_JANELA_TOPLEVEL_GRAFICO_ONDAS = datetime.strptime(self.Value_DATA_entry_main_inicio.get(), '%d/%m/%Y')
            data_Final_GRAFICO_JANELA_TOPLEVEL_GRAFICO_ONDAS = datetime.strptime(self.Value_DATA_entry_main_fim.get(), '%d/%m/%Y')
        except ValueError:
            tk.messagebox.showerror(self.Dado_config.idioma(49), self.Dado_config.idioma(176), parent = self.master)
            return False

        self.SIGLAS_GRAFICO_JANELA_TOPLEVEL_GRAFICO_ONDAS = []	
        for iten_id in IDS_JANELA_TOPLEVEL_GRAFICO_ONDAS:
            item_line = ((self.Listbx_Stations_OBS.get(iten_id)).replace('(','')).replace(')','')
            item_line = item_line.split(",")
            est_lat = item_line[0].split(' ')
            estacao = est_lat[0]
            lati = est_lat[1]
            long = item_line[1]
            dip = item_line[2]
            self.SIGLAS_GRAFICO_JANELA_TOPLEVEL_GRAFICO_ONDAS.append([estacao.strip(),lati.strip(),long.strip(),dip.strip()])
        
        self.SIGLAS_GRAFICO_JANELA_TOPLEVEL_GRAFICO_ONDAS.sort(key=lambda x: float(x[3]),reverse=True)

        self.GRAFICO_ONDAS = COMP_ONDAS(self.FIGURA_TOPLEVEL_GRAFICO,self.filedir.get(),self.SIGLAS_GRAFICO_JANELA_TOPLEVEL_GRAFICO_ONDAS,data_Inicial_GRAFICO_JANELA_TOPLEVEL_GRAFICO_ONDAS,data_Final_GRAFICO_JANELA_TOPLEVEL_GRAFICO_ONDAS,self.Value_Formato_DATA_Grafico.get(),self.Entry_ONDAS_CORTE.get(),self.Dado_config)
        self.GRAFICO_ONDAS._set_Matplotlib_grafico()
        self.FIGURA_TOPLEVEL_GRAFICO,self.AXES_TOPLEVEL_GRAFICO,self.TITULO_TOPLEVEL_GRAFICO,self.Matriz_STD_DADOS_JANELA_TOPLEVEL_GRAFICO_ONDAS,self.DELTA_DAYS_ONDAS,self.LISTA_HORAS_ONDAS,self.DATAS_EIXO_X_GRAFICO_ONDAS = self.GRAFICO_ONDAS._get_Matplotlib_grafico_att()
        self.Cont_Line_Horas_JANELA_TOPLEVEL_GRAFICO = 0

        self.plot_ATIVO = "DESVIO"
        self.ID_Connection_MPL_CANVAS_MAPA_TOPLEVEL_ROT_LINHAS=self.FIGURA_TOPLEVEL_GRAFICO.canvas.mpl_connect('button_press_event', self.Thread_LINHAS_UT_GRAFICO_JANELA_TOPLEVEL_GRAFICO)
        self.SALVAR_MATRIZ_DADOS_GRAFICO_JANELA_TOPLEVEL_GRAFICO()
        self.Exibir_Toplevel_GRAFICO()
        self.ATUALIZAR_CANVAS_JANELA_TOPLEVEL_GRAFICO()


    def PLOTAR_GRAFICO_JANELA_TOPLEVEL_MODELO_GRAFICO_PAINEL_MAPA(self,*event):
        tipo_dado_DADOS_PAINEL_MAPA_VTEC_ROTI = self.CB_DADOS_PAINEL_MAPA_VTEC_ROTI.get()
        if tipo_dado_DADOS_PAINEL_MAPA_VTEC_ROTI:
            hora_inicio = self.PAINEL_MAPA_Time_INICIO.get()
            hora_fim = self.PAINEL_MAPA_Time_FIM.get()
            if hora_inicio == "24:00:00":hora_inicio = "23:59:59"    
            if hora_fim == "24:00:00":hora_fim = "23:59:59"    
            font = self.Dado_config.get_font_Settings("PAINEL MAPA")
            _extend_LAT_LONG = self.MAPA_Get_extent_with_zoom()
            colunas = int(self.PAINEL_MAPA_GRADE_COLUNA.get())
            linhas = int(self.PAINEL_MAPA_GRADE_LINHA.get())
            Periodo = colunas * linhas
            start = datetime.strptime("%s %s"%(self.Value_DATA_entry_main_inicio.get(),hora_inicio), '%d/%m/%Y %H:%M:%S')
            end = datetime.strptime("%s %s"%(self.Value_DATA_entry_main_fim.get(),hora_fim), '%d/%m/%Y %H:%M:%S')
            
            
            date = pd.date_range(start = start, end = end, periods = Periodo)
            xlist = np.linspace(_extend_LAT_LONG[0], _extend_LAT_LONG[1], 100)
            ylist = np.linspace(_extend_LAT_LONG[2], _extend_LAT_LONG[3], 100)
            xi, yi = np.meshgrid(xlist, ylist)
            GD1 = np.sqrt(xi**2 + yi**2)
            self.FIGURA_TOPLEVEL_GRAFICO.clf()
            _ticks_cbar = self.Dado_config.Settings["PAINEL MAPA"]["iTicksCbar_%s"%tipo_dado_DADOS_PAINEL_MAPA_VTEC_ROTI]
            _ticks_divisao = self.Dado_config.Settings["PAINEL MAPA"]["iDivTicks_%s"%tipo_dado_DADOS_PAINEL_MAPA_VTEC_ROTI]
            _vm_max = self.Dado_config.Settings["PAINEL MAPA"]["fValueMax_B_%s"%tipo_dado_DADOS_PAINEL_MAPA_VTEC_ROTI]
            _vm_min = self.Dado_config.Settings["PAINEL MAPA"]["fValueMin_B_%s"%tipo_dado_DADOS_PAINEL_MAPA_VTEC_ROTI]
            levels = np.linspace(_vm_min,_vm_max,int(_ticks_cbar + ((_ticks_cbar-1)*(_ticks_divisao-1))))
            
            ticks = np.linspace(_vm_min,_vm_max,int(_ticks_cbar))
            
            CMAP_MODELO_GRAFICO_PAINEL_MAPA = copy.copy(cm.get_cmap("jet"))
            CMAP_MODELO_GRAFICO_PAINEL_MAPA.set_under("white")
            CMAP_MODELO_GRAFICO_PAINEL_MAPA.set_over("darkred")
            
            AX_MODELO_GRAFICO_PAINEL_MAPA = self.FIGURA_TOPLEVEL_GRAFICO.subplots(ncols=colunas,nrows=linhas,subplot_kw={'projection': ccrs.PlateCarree()}).flat
            cbar_ax = self.FIGURA_TOPLEVEL_GRAFICO.add_axes([0.85, 0.15, 0.0205, 0.7])
            contL=0;contC=0
            for Data,AX_MODELO_GRAFICO_PAINEL_MAPA_N in zip(date,AX_MODELO_GRAFICO_PAINEL_MAPA):
                COLOR_SET = AX_MODELO_GRAFICO_PAINEL_MAPA_N.contourf( xi,yi,GD1, cmap = CMAP_MODELO_GRAFICO_PAINEL_MAPA,  extend='both', levels = levels, transform=ccrs.PlateCarree()                )
                AX_MODELO_GRAFICO_PAINEL_MAPA_N.set_extent(_extend_LAT_LONG, crs=ccrs.PlateCarree())	
                AX_MODELO_GRAFICO_PAINEL_MAPA_N.add_feature(cfeature.BORDERS)
                AX_MODELO_GRAFICO_PAINEL_MAPA_N.add_feature(cfeature.COASTLINE)
                AX_MODELO_GRAFICO_PAINEL_MAPA_N.plot(self.Coordenadas_equador_Magnetico_X,self.Coordenadas_equador_Magnetico_Y,'k')
                
                
                gl = AX_MODELO_GRAFICO_PAINEL_MAPA_N.gridlines(crs=ccrs.PlateCarree(),draw_labels=True)
                gl.xlabels_bottom=True
                gl.xlabels_left=True




                gl.xlabels_top=False
                gl.ylabels_right=False
                
                
                
                AX_MODELO_GRAFICO_PAINEL_MAPA_N.grid(  # CONVERT_GRID'on')
                transform = ccrs.PlateCarree()._as_mpl_transform(AX_MODELO_GRAFICO_PAINEL_MAPA_N)
                AX_MODELO_GRAFICO_PAINEL_MAPA_N.annotate(str(Data.time())[:8], xy=(_extend_LAT_LONG[0], _extend_LAT_LONG[2]), xycoords=transform, color='black', ha='left', va='bottom')
                contL=contL+1;contC=contC+1
            self.CBAR_MODELO_GRAFICO_PAINEL_MAPA = self.FIGURA_TOPLEVEL_GRAFICO.colorbar(COLOR_SET, cax=cbar_ax, boundaries=ticks, extend='both', ticks=ticks)
            self.CBAR_MODELO_GRAFICO_PAINEL_MAPA.ax.set_picker(5)
            
            self.CBAR_MODELO_GRAFICO_PAINEL_MAPA.ax.set_gid("tick_bar_graph_model:PAINEL MAPA:%s"%tipo_dado_DADOS_PAINEL_MAPA_VTEC_ROTI)
            self.CBAR_MODELO_GRAFICO_PAINEL_MAPA.ax.set_title(self.Dado_config.Settings["PAINEL MAPA"]["sTitle_B_%s"%tipo_dado_DADOS_PAINEL_MAPA_VTEC_ROTI],picker=5,gid="label_bar_graph_model:PAINEL MAPA:%s"%tipo_dado_DADOS_PAINEL_MAPA_VTEC_ROTI,pad = 30,**font)
            self.plot_ATIVO = "PAINEL MAPA"
            self.Exibir_Toplevel_GRAFICO()
            self.ATUALIZAR_CANVAS_JANELA_TOPLEVEL_GRAFICO()

    def PLOTAR_GRAFICO_JANELA_TOPLEVEL_GRAFICO_PAINEL_MAPA(self,*event):
        tipo_dado_DADOS_PAINEL_MAPA_VTEC_ROTI = self.CB_DADOS_PAINEL_MAPA_VTEC_ROTI.get()
        if tipo_dado_DADOS_PAINEL_MAPA_VTEC_ROTI:
            hora_inicio = self.PAINEL_MAPA_Time_INICIO.get()
            hora_fim = self.PAINEL_MAPA_Time_FIM.get()
            if hora_inicio == "24:00:00":hora_inicio = "23:59:59"    
            if hora_fim == "24:00:00":hora_fim = "23:59:59"
            colunas = int(self.PAINEL_MAPA_GRADE_COLUNA.get())
            linhas = int(self.PAINEL_MAPA_GRADE_LINHA.get())
            try:
                data_GRAFICO_JANELA_TOPLEVEL_GRAFICO_PAINEL_MAPA_Inicio = datetime.strptime("%s %s"%(self.Value_DATA_entry_main_inicio.get(),hora_inicio), '%d/%m/%Y %H:%M:%S')
                data_GRAFICO_JANELA_TOPLEVEL_GRAFICO_PAINEL_MAPA_Fim = datetime.strptime("%s %s"%(self.Value_DATA_entry_main_fim.get(),hora_fim), '%d/%m/%Y %H:%M:%S')
            except ValueError:
                tk.messagebox.showerror(self.Dado_config.idioma(49), self.Dado_config.idioma(176), parent = self.master)
                return False
            self.VAR_BARRA_LOADING_GRAFICO_PAINEL_MAPA = tk.DoubleVar(self)
            self.VAR_BARRA_LOADING_LABEL_GRAFICO_PAINEL_MAPA = tk.StringVar(self)
            self.VAR_PROCESSO_GRAFICO_PAINEL_MAPA = tk.BooleanVar(self)
            self.VAR_PROCESSO_GRAFICO_PAINEL_MAPA.set(False)

            if float(self.Entry_PAINEL_MAPA_Filter_ELE.get().replace(',','.')) != self.Dado_config.Settings["PAINEL MAPA"]["fElevation_Filter"]:self.Dado_config.Settings["PAINEL MAPA"]["fElevation_Filter"] = float(self.Entry_PAINEL_MAPA_Filter_ELE.get().replace(',','.'))
            if float(self.Entry_Delta_Time_PAINEL_MAPA_ROT.get().replace(',','.')) != self.Dado_config.Settings["PAINEL MAPA"]["fValueDelta_ROT"]:self.Dado_config.Settings["PAINEL MAPA"]["fValueDelta_ROT"] = float(self.Entry_Delta_Time_PAINEL_MAPA_ROT.get().replace(',','.'))
            if float(self.Entry_ROTI_Delta_Time_PAINEL_MAPA_ROTI.get().replace(',','.')) != self.Dado_config.Settings["PAINEL MAPA"]["fValueDelta_ROTI"]:self.Dado_config.Settings["PAINEL MAPA"]["fValueDelta_ROTI"] = float(self.Entry_ROTI_Delta_Time_PAINEL_MAPA_ROTI.get().replace(',','.'))
            limites_estacoes = self.MAPA_Get_extent_with_zoom()
            Listas_Estacoes_Cadastradas_lim = []
            IDS_JANELA_TOPLEVEL_GRAFICO_PAINEL_MAPA = self.Listbx_Stations_OBS.curselection()
            if(len(IDS_JANELA_TOPLEVEL_GRAFICO_PAINEL_MAPA) > 1):
                for iten_id in IDS_JANELA_TOPLEVEL_GRAFICO_PAINEL_MAPA:Listas_Estacoes_Cadastradas_lim.append(self.Listbx_Stations_OBS.get(iten_id)[:4])
            else:
                for estacao in self.Listas_Estacoes_Cadastradas:
                    X = float(estacao[2])
                    Y = float(estacao[1])
                    min_X,max_X,min_Y,max_Y = limites_estacoes
                    if ((X >= (min_X-20)) and (X <= (max_X+20)) and (Y >= (min_Y-20)) and (Y <= (max_Y+20))):Listas_Estacoes_Cadastradas_lim.append(estacao[0])
            self.stop_thread_PAINEL_MAPA.set(False)
            self.GRAFICO_PAINEL_MAPA = COMP_GRADE_MAPA(
                self.filedir.get(),
                data_GRAFICO_JANELA_TOPLEVEL_GRAFICO_PAINEL_MAPA_Inicio,
                data_GRAFICO_JANELA_TOPLEVEL_GRAFICO_PAINEL_MAPA_Fim,
                colunas,
                linhas,
                Listas_Estacoes_Cadastradas_lim,
                limites_estacoes,
                self.VAR_BARRA_LOADING_GRAFICO_PAINEL_MAPA,
                self.VAR_BARRA_LOADING_LABEL_GRAFICO_PAINEL_MAPA,
                self.Dado_config,
                self.Coordenadas_equador_Magnetico_X,
                self.Coordenadas_equador_Magnetico_Y,
                self.stop_thread_PAINEL_MAPA
            )
            if tipo_dado_DADOS_PAINEL_MAPA_VTEC_ROTI == "VTEC":
                thread_PAINEL_MAPA = thread_with_trace(target = self.GRAFICO_PAINEL_MAPA._set_Matplotlib_grafico_grade_VTEC)
                thread_PAINEL_MAPA.setDaemon(True)
                thread_PAINEL_MAPA.start()
            elif tipo_dado_DADOS_PAINEL_MAPA_VTEC_ROTI == "ROT":
                thread_PAINEL_MAPA = thread_with_trace(target = self.GRAFICO_PAINEL_MAPA._set_Matplotlib_grafico_grade_ROT) 
                thread_PAINEL_MAPA.setDaemon(True)
                thread_PAINEL_MAPA.start()
            elif tipo_dado_DADOS_PAINEL_MAPA_VTEC_ROTI == "ROTI":
                thread_PAINEL_MAPA = thread_with_trace(target = self.GRAFICO_PAINEL_MAPA._set_Matplotlib_grafico_grade_ROTI) 
                thread_PAINEL_MAPA.setDaemon(True)
                thread_PAINEL_MAPA.start()
            qtSimpleDialog.Loading(self.master,'PAINEL MAPA',orient_u = Qt.Orientation.Horizontal,maximum_u = 100,length_u = 500,mode_u = 'determinate',icon=self.uti.resource_path('img\icone.ico'),progress_var = self.VAR_BARRA_LOADING_GRAFICO_PAINEL_MAPA,info_loading=self.VAR_BARRA_LOADING_LABEL_GRAFICO_PAINEL_MAPA,uti = self.uti,Dado_config=self.Dado_config,stop_thread = self.stop_thread_PAINEL_MAPA,threads = thread_PAINEL_MAPA)
            self.plot_ATIVO = "PAINEL MAPA"
            
            
            

    def PLOTAR_GRAFICO_JANELA_TOPLEVEL_MODELO_GRAFICO_MAPA(self,*event):
        tipo_dado_DADOS_MAPA_VTEC_ROTI = self.CB_DADOS_MAPA_VTEC_ROTI.get()
        if tipo_dado_DADOS_MAPA_VTEC_ROTI:
            self.FIGURA_TOPLEVEL_GRAFICO.clf()
            self.FIGURA_TOPLEVEL_GRAFICO.set_facecolor('white')
            font = self.Dado_config.get_font_Settings("MAPA")
            _extend_LAT_LONG = self.MAPA_Get_extent_with_zoom()
            AX_MODELO_GRAFICO_MAPA = self.FIGURA_TOPLEVEL_GRAFICO.add_subplot(111, projection = ccrs.PlateCarree())
            ylist = np.linspace(-90.0, 90.0, 100)
            xlist = np.linspace(-180.0, 180.0, 100)
            xi, yi = np.meshgrid(xlist, ylist)
            GD1 = np.sqrt(xi**2 + yi**2)
            AX_MODELO_GRAFICO_MAPA.plot(self.Coordenadas_equador_Magnetico_X,self.Coordenadas_equador_Magnetico_Y,'k',gid="line_ecuador_mag",picker=2)
            _ticks_cbar = self.Dado_config.Settings["MAPA"]["iTicksCbar_%s"%tipo_dado_DADOS_MAPA_VTEC_ROTI]
            _ticks_divisao = self.Dado_config.Settings["MAPA"]["iDivTicks_%s"%tipo_dado_DADOS_MAPA_VTEC_ROTI]
            _vm_max = self.Dado_config.Settings["MAPA"]["fValueMax_B_%s"%tipo_dado_DADOS_MAPA_VTEC_ROTI]
            _vm_min = self.Dado_config.Settings["MAPA"]["fValueMin_B_%s"%tipo_dado_DADOS_MAPA_VTEC_ROTI]
            levels = np.linspace(_vm_min,_vm_max,int(_ticks_cbar + ((_ticks_cbar-1)*(_ticks_divisao-1))))
            
            gl = AX_MODELO_GRAFICO_MAPA.gridlines(crs=ccrs.PlateCarree(),draw_labels=True)
            gl.xlabels_top=False
            gl.ylabels_right=False
            if self.varx.get()==1:
                t=self.Entry_MAPA_Xtick.get()
                x=t.split(",")
                for i in range(len(x)):
                    x[i]=int(x[i])
                gl.xlocator = mticker.FixedLocator(x)
            if self.vary.get()==1:
                t=self.Entry_MAPA_Ytick.get()
                y=t.split(",")
                for i in range(len(y)):
                    y[i]=int(y[i])
                gl.ylocator = mticker.FixedLocator(y)
            AX_MODELO_GRAFICO_MAPA.grid(  # CONVERT_GRID'on')
            
            ticks = np.linspace(_vm_min,_vm_max,int(_ticks_cbar))
            
            CMAP_MODELO_GRAFICO_MAPA = copy.copy(cm.get_cmap("jet"))
            CMAP_MODELO_GRAFICO_MAPA.set_under("white")
            CMAP_MODELO_GRAFICO_MAPA.set_over("darkred")
            
            
            
            
            
            COLOR_SET = AX_MODELO_GRAFICO_MAPA.contourf(
                xi,yi,GD1,
                cmap = CMAP_MODELO_GRAFICO_MAPA, 
                extend='both',
                levels = levels,
                transform=ccrs.PlateCarree()
            )
            self.CBAR_MODELO_GRAFICO_MAPA = self.FIGURA_TOPLEVEL_GRAFICO.colorbar(
                COLOR_SET,
                extend='both',
                ticks=ticks
            )
            AX_MODELO_GRAFICO_MAPA.set_extent(_extend_LAT_LONG,crs=ccrs.PlateCarree())	
            AX_MODELO_GRAFICO_MAPA.add_feature(cfeature.BORDERS, linewidth=2.0)
            AX_MODELO_GRAFICO_MAPA.add_feature(cfeature.COASTLINE, linewidth=2.0)
            AX_MODELO_GRAFICO_MAPA.set_title("00:00:00",**font)
            self.CBAR_MODELO_GRAFICO_MAPA.ax.set_picker(5)
            self.CBAR_MODELO_GRAFICO_MAPA.ax.set_gid("tick_bar_graph_model:MAPA:%s"%tipo_dado_DADOS_MAPA_VTEC_ROTI)
            self.CBAR_MODELO_GRAFICO_MAPA.ax.set_title(self.Dado_config.Settings["MAPA"]["sTitle_B_%s"%tipo_dado_DADOS_MAPA_VTEC_ROTI],picker=5,gid="label_bar_graph_model:MAPA:%s"%tipo_dado_DADOS_MAPA_VTEC_ROTI,**font,pad=30)
            self.plot_ATIVO = "MAPA"
            self.Exibir_Toplevel_GRAFICO()
            self.ATUALIZAR_CANVAS_JANELA_TOPLEVEL_GRAFICO()
         
    def PLOTAR_GRAFICO_JANELA_TOPLEVEL_GRAFICO_MAPA(self):
        dados = self.CB_DADOS_MAPA_VTEC_ROTI.get()
        if dados:    
            hora_inicio = self.MAPA_Time_INICIO.get()
            hora_fim = self.MAPA_Time_FIM.get()
            if hora_inicio == "24:00:00":hora_inicio = "23:59:59"    
            if hora_fim == "24:00:00":hora_fim = "23:59:59"    
            try:
                data_GRAFICO_JANELA_TOPLEVEL_GRAFICO_MAPA_Inicio = datetime.strptime("%s %s"%(self.Value_DATA_entry_main_inicio.get(),hora_inicio), '%d/%m/%Y %H:%M:%S')
                data_GRAFICO_JANELA_TOPLEVEL_GRAFICO_MAPA_Fim = datetime.strptime("%s %s"%(self.Value_DATA_entry_main_fim.get(),hora_fim), '%d/%m/%Y %H:%M:%S')
            except ValueError:
                tk.messagebox.showerror(self.Dado_config.idioma(49), self.Dado_config.idioma(176), parent = self.master)
                return False
            self.VAR_BARRA_LOADING_GRAFICO_MAPA = tk.DoubleVar(self)
            self.VAR_BARRA_LOADING_LABEL_GRAFICO_MAPA = tk.StringVar(self)

            intervalo_MAPA = self.MAPA_Delta_Time.get().replace(',','.')
            if float(self.Entry_MAPA_Filter_ELE.get().replace(',','.')) != self.Dado_config.Settings["MAPA"]["fElevation_Filter"]:
                self.Dado_config.Settings["MAPA"]["fElevation_Filter"] = float(self.Entry_MAPA_Filter_ELE.get().replace(',','.'))
            if float(self.Entry_ROT_Delta_Time_MAPA_ROT.get().replace(',','.')) != self.Dado_config.Settings["MAPA"]["fValueDelta_ROT"]:
                self.Dado_config.Settings["MAPA"]["fValueDelta_ROT"] = float(self.Entry_ROT_Delta_Time_MAPA_ROT.get().replace(',','.'))
            if float(self.Entry_ROTI_Delta_Time_MAPA_ROTI.get().replace(',','.')) != self.Dado_config.Settings["MAPA"]["fValueDelta_ROTI"]:
                self.Dado_config.Settings["MAPA"]["fValueDelta_ROTI"] = float(self.Entry_ROTI_Delta_Time_MAPA_ROTI.get().replace(',','.'))
            limites_estacoes = self.MAPA_Get_extent_with_zoom()
            Listas_Estacoes_Cadastradas_lim = []
            IDS_JANELA_TOPLEVEL_GRAFICO_MAPA = self.Listbx_Stations_OBS.curselection()
            
            if(len(IDS_JANELA_TOPLEVEL_GRAFICO_MAPA) > 1):
                for iten_id in IDS_JANELA_TOPLEVEL_GRAFICO_MAPA:Listas_Estacoes_Cadastradas_lim.append(self.Listbx_Stations_OBS.get(iten_id)[:4])
            else:
                for estacao in self.Listas_Estacoes_Cadastradas:
                    X = float(estacao[2])
                    Y = float(estacao[1])
                    min_X,max_X,min_Y,max_Y = limites_estacoes
                    if ((X >= (min_X-20)) and (X <= (max_X+20)) and (Y >= (min_Y-20)) and (Y <= (max_Y+20))):Listas_Estacoes_Cadastradas_lim.append(estacao[0])
            self.stop_thread_MAPA.set(False)
            self.GRAFICO_Mapa = COMP_MAPA(
                self.filedir.get(),
                data_GRAFICO_JANELA_TOPLEVEL_GRAFICO_MAPA_Inicio,
                data_GRAFICO_JANELA_TOPLEVEL_GRAFICO_MAPA_Fim,
                intervalo_MAPA,
                Listas_Estacoes_Cadastradas_lim,
                limites_estacoes,
                self.VAR_BARRA_LOADING_GRAFICO_MAPA,
                self.VAR_BARRA_LOADING_LABEL_GRAFICO_MAPA,
                self.Dado_config,
                self.Coordenadas_equador_Magnetico_X,
                self.Coordenadas_equador_Magnetico_Y,
                self.Value_Check_VIDEO_MAPA.get(),
                self.stop_thread_MAPA,
                self.varx,
                self.Entry_MAPA_Xtick,
                self.vary,
                self.Entry_MAPA_Ytick,
                self.varabs
            )
            if dados == "VTEC":
                thread_MAPA = thread_with_trace(target = self.GRAFICO_Mapa._set_Matplotlib_grafico_VTEC) 
                thread_MAPA.setDaemon(True)
                thread_MAPA.start()
            elif dados == "ROTI":
                thread_MAPA = thread_with_trace(target = self.GRAFICO_Mapa._set_Matplotlib_grafico_ROTI) 
                thread_MAPA.setDaemon(True)
                thread_MAPA.start()
            elif dados == "ROT":
                thread_MAPA = thread_with_trace(target = self.GRAFICO_Mapa._set_Matplotlib_grafico_ROT) 
                thread_MAPA.setDaemon(True)
                thread_MAPA.start()
            qtSimpleDialog.Loading(self.master,'MAPA',orient_u = Qt.Orientation.Horizontal,maximum_u = 100,length_u = 500, mode_u = 'determinate', icon=self.uti.resource_path('img\icone.ico'),progress_var = self.VAR_BARRA_LOADING_GRAFICO_MAPA,info_loading=self.VAR_BARRA_LOADING_LABEL_GRAFICO_MAPA,uti = self.uti, Dado_config=self.Dado_config, stop_thread = self.stop_thread_MAPA, threads = thread_MAPA)
            self.plot_ATIVO = "MAPA"


    def PLOTAR_GRAFICO_JANELA_TOPLEVEL_GRAFICO_ROT(self):
        ids = self.Listbx_Stations_OBS.curselection()
        if ids:
            dados= self.CB_DADOS_ROT.get()
            try:self.data_Inicial_GRAFICO_JANELA_TOPLEVEL_GRAFICO_ROT = datetime.strptime(self.Value_DATA_entry_main_inicio.get(), '%d/%m/%Y')
            except ValueError:
                tk.messagebox.showerror(self.Dado_config.idioma(49),self.Dado_config.idioma(176), parent = self.master)
                return False
            self.SIGLAS_GRAFICO_JANELA_TOPLEVEL_GRAFICO_ROT = self.Listbx_Stations_OBS.get(ids).replace("(","").replace(",","").split(" ")
            if float(self.Entry_ROT_Filter_ELE.get().replace(',','.')) != self.Dado_config.Settings["ROT"]["fElevation_Filter"]:self.Dado_config.Settings["ROT"]["fElevation_Filter"] = float(self.Entry_ROT_Filter_ELE.get().replace(',','.'))
            if float(self.Entry_ROT_Delta_Time_ROT.get().replace(',','.')) != self.Dado_config.Settings["ROT"]["fValueDelta_ROT"]:self.Dado_config.Settings["ROT"]["fValueDelta_ROT"] = float(self.Entry_ROT_Delta_Time_ROT.get().replace(',','.'))
            if float(self.Entry_ROT_Delta_Time_ROTI.get().replace(',','.')) != self.Dado_config.Settings["ROT"]["fValueDelta_ROTI"]:self.Dado_config.Settings["ROT"]["fValueDelta_ROTI"] = float(self.Entry_ROT_Delta_Time_ROTI.get().replace(',','.'))
            if float(self.Entry_ROT_Filter_FATOR_MULTIPLICACAO.get().replace(',','.')) != self.Dado_config.Settings["ROT"]["fValueMultFactor_ROT"]:self.Dado_config.Settings["ROT"]["fValueMultFactor_ROT"] = float(self.Entry_ROT_Filter_FATOR_MULTIPLICACAO.get().replace(',','.'))
            
            self.GRAFICO_Rot = COMP_ROT(self.FIGURA_TOPLEVEL_GRAFICO, self.SIGLAS_GRAFICO_JANELA_TOPLEVEL_GRAFICO_ROT,self.filedir.get(), self.data_Inicial_GRAFICO_JANELA_TOPLEVEL_GRAFICO_ROT, self.Value_Line_Cores.get(),self.Value_State_Legenda.get(),self.Dado_config, dados,self.Entry_ROT_XMinor.get(),self.Entry_ROT_YMinor.get(), self.rots)
            self.GRAFICO_Rot._set_Matplotlib_grafico()
            self.FIGURA_TOPLEVEL_GRAFICO, self.AXES_TOPLEVEL_GRAFICO, self.TITULO_TOPLEVEL_GRAFICO, self.List_PRN, self.DADOS = self.GRAFICO_Rot._get_Matplotlib_grafico_att()
            self.Cont_Line_Horas_JANELA_TOPLEVEL_GRAFICO = 0
            self.plot_ATIVO = "ROT"
            self.ID_Connection_MPL_CANVAS_MAPA_TOPLEVEL_ROT_LINHAS=self.FIGURA_TOPLEVEL_GRAFICO.canvas.mpl_connect('button_press_event', self.Thread_LINHAS_UT_GRAFICO_JANELA_TOPLEVEL_GRAFICO)
            self.SALVAR_MATRIZ_DADOS_GRAFICO_JANELA_TOPLEVEL_GRAFICO()
            self.Exibir_Toplevel_GRAFICO()
            self.ATUALIZAR_CANVAS_JANELA_TOPLEVEL_GRAFICO()

    def PLOTAR_GRAFICO_JANELA_TOPLEVEL_GRAFICO_ROTI(self):pass

    def SALVAR_IMAGEM_DADOS_GRAFICO_JANELA_TOPLEVEL_GRAFICO(self):
        if self.Value_Salvar_Figura_JANELA_TOPLEVEL_GRAFICO.get():
            if self.filedir.get() and self.TITULO_TOPLEVEL_GRAFICO:
                self.FIGURA_TOPLEVEL_GRAFICO.set_size_inches(self.Dado_config.Settings["MAPA"]["fSize_inches_fig_width"], self.Dado_config.Settings["MAPA"]["fSize_inches_fig_height"])
                if self.Value_cb_Modelo_Grafico.get() == "Desvio (STD)":self.FIGURA_TOPLEVEL_GRAFICO.savefig((r"%s\%s.png")%(self.filedir.get(), self.TITULO_TOPLEVEL_GRAFICO), facecolor = self.FIGURA_TOPLEVEL_GRAFICO.get_facecolor())
                else:self.FIGURA_TOPLEVEL_GRAFICO.savefig((r"%s\%s.png")%(self.filedir.get(), self.TITULO_TOPLEVEL_GRAFICO))

    
    
    
    
    
    
    



    def SALVAR_MATRIZ_DADOS_GRAFICO_JANELA_TOPLEVEL_GRAFICO(self):
        if self.Value_Salvar_Matriz_JANELA_TOPLEVEL_GRAFICO.get():
            if self.Value_cb_Modelo_Grafico.get() == "Individual (STD)":self.SALVAR_MATRIZ_DADOS_GRAFICO_JANELA_TOPLEVEL_GRAFICO_INDIVIDUAL()
            elif self.Value_cb_Modelo_Grafico.get() in "EIA (STD)":self.SALVAR_MATRIZ_DADOS_GRAFICO_JANELA_TOPLEVEL_GRAFICO_EIA()
            elif self.Value_cb_Modelo_Grafico.get() == "Desvio (STD)":self.SALVAR_MATRIZ_DADOS_GRAFICO_JANELA_TOPLEVEL_GRAFICO_DESVIO()
            
            
            elif self.Value_cb_Modelo_Grafico.get() == "ROT/VTEC (CMN)":self.SALVAR_MATRIZ_DADOS_GRAFICO_JANELA_TOPLEVEL_GRAFICO_ROT()
            elif self.Value_cb_Modelo_Grafico.get() == "ONDAS (STD)":self.SALVAR_MATRIZ_DADOS_GRAFICO_JANELA_TOPLEVEL_GRAFICO_ONDAS()
                
    def SALVAR_MATRIZ_DADOS_GRAFICO_JANELA_TOPLEVEL_GRAFICO_INDIVIDUAL(self):
        try:
            Matriz_std = "Hora"
            barra_std = "------"
            for diaTEC in self.DIAS_TEC_JANELA_TOPLEVEL_GRAFICO_INDIVIDUAL:
                Matriz_std+=(("\tTEC%.2i")%(diaTEC))
                barra_std+=("\t-----")
            Matriz_std+=(("\tMEDIA\tDESV\tM+DES\tM-DES\n%s\t------\t------\t------\t------\n")%barra_std)
            Horas = 0
            for matriz_tmp in self.Matriz_STD_DADOS_JANELA_TOPLEVEL_GRAFICO_INDIVIDUAL:
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
                    tk.messagebox.showerror(self.Dado_config.idioma(49), self.Dado_config.idioma(94), parent = self.master)
                    raise IOError
                des_std = np.std(tmp_media)
                Matriz_std+=(("%06.3f\t")%(mediaTEC)).replace(".",",")
                Matriz_std+=(("%06.3f\t")%(des_std)).replace(".",",")
                Matriz_std+=(("%06.3f\t")%(mediaTEC+des_std)).replace(".",",")
                Matriz_std+=(("%06.3f\n")%(mediaTEC-des_std)).replace(".",",")
            with open((self.filedir.get()  + ("/%s_matriz.txt")%(self.TITULO_TOPLEVEL_GRAFICO)), 'w', encoding = "UTF-8") as arquivoMat:
                arquivoMat.write(Matriz_std)
        except PermissionError:
            tk.messagebox.showerror(self.Dado_config.idioma(49), self.Dado_config.idioma(95), parent = self.master)
    
    def SALVAR_MATRIZ_DADOS_GRAFICO_JANELA_TOPLEVEL_GRAFICO_EIA(self):
        
        
        
        try:
            if len(self.SIGLAS_GRAFICO_JANELA_TOPLEVEL_GRAFICO_EIA)<10:
                est=[sgl[0] for sgl in self.SIGLAS_GRAFICO_JANELA_TOPLEVEL_GRAFICO_EIA]
            else:
                est=[self.SIGLAS_GRAFICO_JANELA_TOPLEVEL_GRAFICO_EIA[sgl][0] for sgl in range(10)]
            arquivo=self.filedir.get()+"\\"+self.TITULO_TOPLEVEL_GRAFICO+"_"+str(est)+"_Matriz.txt"

            
            
            with open(arquivo,'w') as arqTri:
                if self.Value_Lat_Dip_axes_Y.get() == 0:arqTri.write("HORA\tLATITUDE\tVTEC\n")
                else:arqTri.write("HORA\tDIP LATITUDE\tVTEC\n")
                for x,y,z in self.Matriz_STD_DADOS_JANELA_TOPLEVEL_GRAFICO_EIA:
                    arqTri.write(("%.2f\t%.2f\t%.2f\n"%(x,y,z)).replace('.',','))
        except (IOError):
            pass

    def SALVAR_MATRIZ_DADOS_GRAFICO_JANELA_TOPLEVEL_GRAFICO_DESVIO(self):
        
        
        
        
        
        
        
        
        
        for tec_n,sigla,med,desv in zip(self.Matriz_STD_DADOS_JANELA_TOPLEVEL_GRAFICO_DESVIO,[s[0]for s in self.SIGLAS_GRAFICO_JANELA_TOPLEVEL_GRAFICO_DESVIO],self.LISTA_MEDIA_TEC,self.LISTA_DESVIOPD_TEC):
            
            nome = ('%s-%s-%s(%s-%s)')%(sigla,self.Value_DATA_entry_main_inicio.get()[6:],self.Value_DATA_entry_main_inicio.get()[3:5],self.Value_DATA_entry_main_inicio.get()[0:2],self.Value_DATA_entry_main_fim.get()[0:2])
            
            self.matriz_linha((r"%s\%s.txt")%(self.filedir.get(),nome),tec_n,med,desv)

    def matriz_linha(self,caminho,tec_n,med_calm,desv_calmo):
        try:
            with open(caminho,'w') as arqTri:
                arqTri.write("Média\tMed+Des\tMed-Des")
                for contd in range(self.DELTA_DAYS_DESVIO):
                    datafile = (datetime.strptime(self.Value_DATA_entry_main_inicio.get(), '%d/%m/%Y') + timedelta(days=contd))
                    arqTri.write(("\tHora\tTec %i")%(datafile.day))
                else:arqTri.write("\n")
                for t,tec_est,m,d in zip(self.LISTA_HORAS_DEVIO,tec_n.T,med_calm,desv_calmo):
                    arqTri.write(((("%.2f\t%.2f\t%.2f")%(m,(m+d),(m-d))).replace("nan","-999,0")).replace(".",","))
                    for tec_dia in tec_est:arqTri.write(((("\t%.2f\t%.2f")%(t,tec_dia)).replace("nan","-999,0")).replace(".",","))
                    else:arqTri.write("\n")
        except (IOError):
            pass

    def SALVAR_MATRIZ_DADOS_GRAFICO_JANELA_TOPLEVEL_GRAFICO_ONDAS(self):
        
        
        
        
        
        
        
        
        
        for tec_n,sigla in zip(self.Matriz_STD_DADOS_JANELA_TOPLEVEL_GRAFICO_ONDAS,[s[0]for s in self.SIGLAS_GRAFICO_JANELA_TOPLEVEL_GRAFICO_ONDAS]):
            
            nome = ('%s-%s-%s(%s-%s)')%(sigla,self.Value_DATA_entry_main_inicio.get()[6:],self.Value_DATA_entry_main_inicio.get()[3:5],self.Value_DATA_entry_main_inicio.get()[0:2],self.Value_DATA_entry_main_fim.get()[0:2])
            print((r"%s\%s.txt")%(self.filedir.get(),nome))
            
        
        
        with open((r"%s\%s.txt")%(self.filedir.get(),nome),'w') as arqTri:
            for i in range(len(tec_n)):
                arqTri.write(str(self.LISTA_HORAS_ONDAS[i])+'\t'+str(tec_n[i])+'\n')
                

    def matriz_linha1(self,caminho,tec_n):
        try:
            with open(caminho,'w') as arqTri:
                for contd in range(self.DELTA_DAYS_ONDAS):
                    datafile = (datetime.strptime(self.Value_DATA_entry_main_inicio.get(), '%d/%m/%Y') + timedelta(days=contd))
                    arqTri.write(("\tHora\tTec %i")%(datafile.day))
                else:arqTri.write("\n")
                for t,tec_est in zip(self.LISTA_HORAS_ONDAS,tec_n.T):
                    for tec_dia in tec_est:arqTri.write(((("\t%.2f\t%.2f")%(t,tec_dia)).replace("nan","-999,0")).replace(".",","))
                    else:arqTri.write("\n")
        except (IOError):
            pass
    def SALVAR_MATRIZ_DADOS_GRAFICO_JANELA_TOPLEVEL_GRAFICO_MAPA(self):pass

    def SALVAR_MATRIZ_DADOS_GRAFICO_JANELA_TOPLEVEL_GRAFICO_ROT(self):
        
        
        
        
        
        
        if self.CB_DADOS_ROT.get() == "ROT":
            ext="ROT"
        elif self.CB_DADOS_ROT.get() == "ROTI":
            ext="ROTI"
        elif self.CB_DADOS_ROT.get() == "VTEC":
            ext="VTEC"

        for sat in self.List_PRN:
            
            with open(("%s\%2.2i-%2.2i-%i_%s_PRN%0.2i.%s"%(self.filedir.get(),self.data_Inicial_GRAFICO_JANELA_TOPLEVEL_GRAFICO_ROT.day,self.data_Inicial_GRAFICO_JANELA_TOPLEVEL_GRAFICO_ROT.month,self.data_Inicial_GRAFICO_JANELA_TOPLEVEL_GRAFICO_ROT.year,self.SIGLAS_GRAFICO_JANELA_TOPLEVEL_GRAFICO_ROT,sat,ext)),'w') as arqTri:
                arqTri.write("Hora\t"+ext+"\n")
                
                
                for hora in np.arange(0,24,(30/3600)):
                    try:
                        
                        h=int(hora*100000)/100000
                        hs=str(h)
                        if hs[len(hs)-2:]=="99":
                            h=int(hora*1000000)/1000000
                        else:h=int(hora*100000)/100000
                        if self.CB_DADOS_ROT.get() == "ROT":
                            rot_time = self.DADOS[str(sat)]["%.5f"%float(h)]['rot']
                        elif self.CB_DADOS_ROT.get() == "VTEC":
                            rot_time = self.DADOS[str(sat)]["%.5f"%float(h)]['vtec']
                        elif self.CB_DADOS_ROT.get() == "ROTI":
                            rot_time = self.DADOS[str(sat)]["%.5f"%float(h)]['roti']
                        
                        arqTri.write(("%09.5f\t%.2f\n"%(h,rot_time)))
                        
                    except KeyError:
                        
                        h=int(hora*100000)/100000
                        arqTri.write("%09.5f\t-999,00\n"%h)
                        
                    
                    
                    
                    
                    
                    
                    
                
        with open(("%s\%2.2i-%2.2i-%i_%s_all.%s"%(self.filedir.get(),self.data_Inicial_GRAFICO_JANELA_TOPLEVEL_GRAFICO_ROT.day,self.data_Inicial_GRAFICO_JANELA_TOPLEVEL_GRAFICO_ROT.month,self.data_Inicial_GRAFICO_JANELA_TOPLEVEL_GRAFICO_ROT.year,self.SIGLAS_GRAFICO_JANELA_TOPLEVEL_GRAFICO_ROT,ext)),'w') as arqTri:
                linha="Time(UT)\t"
                for i in np.arange(1,max(self.List_PRN)+1):
                    linha=linha+"PRN"+str("%02i\t"%i)
                arqTri.write(linha[:-1]+"\n")    
                linha=""
                for hora in np.arange(0,24,(30/3600)):
                    if linha!= "":
                        arqTri.write(linha[:-1]+"\n")
                        linha=""
                    for sat in np.arange(1,max(self.List_PRN)+1):
                        try:
                            
                            h=int(hora*100000)/100000
                            hs=str(h)
                            if hs[len(hs)-2:]=="99":
                                h=int(hora*1000000)/1000000
                            else:h=int(hora*100000)/100000
                            if linha=="":
                                linha=("%09.5f\t"%(h))
                            if self.CB_DADOS_ROT.get() == "ROT":
                                rot_time = self.DADOS[str(sat)]["%.5f"%float(h)]['rot']
                            elif self.CB_DADOS_ROT.get() == "VTEC":
                                rot_time = self.DADOS[str(sat)]["%.5f"%float(h)]['vtec']
                            elif self.CB_DADOS_ROT.get() == "ROTI":
                                rot_time = self.DADOS[str(sat)]["%.5f"%float(h)]['roti']
                            linha=linha+("%.2f\t"%(rot_time))
                            
                        except KeyError:
                            
                            h=int(hora*100000)/100000
                            linha=linha+"-999,00\t"
                arqTri.write(linha[:-1]+"\n")
    

    def INSERIR_LINHA_VERTICAL_GRAFICO_JANELA_TOPLEVEL_GRAFICO(self):
        self.Value_Line_Horas_JANELA_TOPLEVEL_GRAFICO.set(not self.Value_Line_Horas_JANELA_TOPLEVEL_GRAFICO.get())
        
        if self.Value_Line_Horas_JANELA_TOPLEVEL_GRAFICO.get():self.Popup_TopLevel_Grafico.entryconfig(self.Dado_config.idioma(188), label = self.Dado_config.idioma(189))
        else:self.Popup_TopLevel_Grafico.entryconfig(self.Dado_config.idioma(189), label = self.Dado_config.idioma(188))

    def Atualizar_grid_X_JANELA_TOPLEVEL_GRAFICO(self, Atualizar_Popup_TopLevel_Grafico = True):
        if Atualizar_Popup_TopLevel_Grafico:
            self.Value_grid_axes_X.set(not self.Value_grid_axes_X.get())
            if self.Value_grid_axes_X.get():self.Popup_TopLevel_Grafico.entryconfig(self.Dado_config.idioma(141), label = self.Dado_config.idioma(142))
            else:self.Popup_TopLevel_Grafico.entryconfig(self.Dado_config.idioma(142), label = self.Dado_config.idioma(141))
            try:self.AXES_TOPLEVEL_GRAFICO.xaxis.grid(  # CONVERT_GRIDself.Value_grid_axes_X.get())
            except (AttributeError,ValueError):
                for axe_i in np.array(self.AXES_TOPLEVEL_GRAFICO).flatten():axe_i.xaxis.grid(  # CONVERT_GRIDself.Value_grid_axes_X.get())

    def Atualizar_grid_Y_JANELA_TOPLEVEL_GRAFICO(self, Atualizar_Popup_TopLevel_Grafico = True):
        if Atualizar_Popup_TopLevel_Grafico:
            self.Value_grid_axes_Y.set(not self.Value_grid_axes_Y.get())
            if self.Value_grid_axes_Y.get():self.Popup_TopLevel_Grafico.entryconfig(self.Dado_config.idioma(139), label = self.Dado_config.idioma(140))
            else:self.Popup_TopLevel_Grafico.entryconfig(self.Dado_config.idioma(140), label = self.Dado_config.idioma(139))
            try:self.AXES_TOPLEVEL_GRAFICO.yaxis.grid(  # CONVERT_GRIDself.Value_grid_axes_Y.get())
            except (AttributeError,ValueError):
                for axe_i in np.array(self.AXES_TOPLEVEL_GRAFICO).flatten():axe_i.yaxis.grid(  # CONVERT_GRIDself.Value_grid_axes_Y.get())
    
    def Thread_Pick_Event_PROPRIEDADES_JANELA_TOPLEVEL_GRAFICO(self,event):
        
        self.Pick_Event_PROPRIEDADES_JANELA_TOPLEVEL_GRAFICO(event)
        


    def Pick_Event_PROPRIEDADES_JANELA_TOPLEVEL_GRAFICO(self,event):

        """
            Adaptar os títulos .... para o padrão inglês ou portuguesesadasd (:>)
            -=, subtracts a value from variable, setting the variable to the result
            *=, multiplies the variable and a value, making the outcome the variable
            /=, divides the variable by the value, making the outcome the variable
            %=, performs modulus on the variable, with the variable then being set to the result of it
        """

        
        try:GID_EVENT = event.artist.get_gid().split(":")
        except AttributeError:return

        Evento = GID_EVENT[0]
        INTERFACE = GID_EVENT[1].upper()
        print(GID_EVENT)
        print(Evento)
        print(INTERFACE)



        
        

        
                
        
        
        

                    
                    
                    
        
        

                    
                    
                    
                    
                    
        
        

                    
                    
                    
                    
                    
        
        





        if Evento == "Sup_titulo":
            titulo_atual = event.artist.get_text()
            font_old =  self.Dado_config.get_font_Settings(INTERFACE)
            self.titulo_graph,font_new = askEntry(self.master,titulo = "LABEL " + self.Dado_config.idioma(170),valor = titulo_atual,font_u = font_old,window = self.JANELA_TOPLEVEL_GRAFICO)
            if font_new:
                self.Dado_config.set_font_Settings(INTERFACE,font_new)
                
                    
                        
                            
                                
                self.FIGURA_TOPLEVEL_GRAFICO.suptitle(self.titulo_graph, picker=5,gid="Sup_titulo:"+INTERFACE,**font_new)

            elif self.titulo_graph:
                
                    
                        
                            
                
                
                self.FIGURA_TOPLEVEL_GRAFICO.suptitle(self.titulo_graph, picker=5,gid="Sup_titulo:"+INTERFACE)


        elif Evento == "titulo_graph":
            titulo_atual = event.artist.get_text()
            font_old =  self.Dado_config.get_font_Settings(INTERFACE)
            titulo_graph_new, font_new = askEntry(self.master,titulo = self.Dado_config.idioma(170), valor = titulo_atual,font_u = font_old, window = self.JANELA_TOPLEVEL_GRAFICO, uti = self.uti, Dado_config = self.Dado_config)
            if font_new:
                self.Dado_config.set_font_Settings(INTERFACE,font_new)
                self.AXES_TOPLEVEL_GRAFICO.set_title(titulo_graph_new,**font_new)
            elif titulo_graph_new != titulo_atual:
                self.AXES_TOPLEVEL_GRAFICO.set_title(titulo_graph_new)


        elif Evento == "y_label_graph":
            titulo_atual = event.artist.get_text()
            font_old =  self.Dado_config.get_font_Settings(INTERFACE)
            titulo_axe_y_new,font_new = askEntry(self.master,titulo = "LABEL Y",valor = titulo_atual,font_u = font_old, window = self.JANELA_TOPLEVEL_GRAFICO, uti = self.uti, Dado_config = self.Dado_config )
            if font_new:
                self.Dado_config.set_font_Settings(INTERFACE,font_new)
                self.Dado_config.Settings[INTERFACE]["sTitle_Y"] = titulo_axe_y_new
                self.AXES_TOPLEVEL_GRAFICO.set_ylabel(titulo_axe_y_new,**font_new)
            elif titulo_atual != titulo_axe_y_new:
                self.Dado_config.Settings[INTERFACE]["sTitle_Y"] = titulo_axe_y_new
                self.AXES_TOPLEVEL_GRAFICO.set_ylabel(titulo_axe_y_new)

        elif Evento == "x_label_graph":
            titulo_atual = event.artist.get_text()
            font_old =  self.Dado_config.get_font_Settings(INTERFACE)
            titulo_axe_x_new, font_new = askEntry(self.master,titulo = "LABEL X",valor = titulo_atual,font_u = font_old,window = self.JANELA_TOPLEVEL_GRAFICO, uti = self.uti, Dado_config = self.Dado_config )
            if font_new:
                self.Dado_config.set_font_Settings(INTERFACE,font_new)
                self.Dado_config.Settings[INTERFACE]["sTitle_X"] = titulo_axe_x_new
                self.AXES_TOPLEVEL_GRAFICO.set_xlabel(titulo_axe_x_new,**font_new)
            elif titulo_atual != titulo_axe_x_new:
                self.Dado_config.Settings[INTERFACE]["sTitle_X"] = titulo_axe_x_new
                self.AXES_TOPLEVEL_GRAFICO.set_xlabel(titulo_axe_x_new)
        
        elif Evento == "label_bar_graph":
            titulo_atual = event.artist.get_text()
            font_old =  self.Dado_config.get_font_Settings(INTERFACE)
            titulo_bar_new,font_new = askEntry(self.master,titulo = self.Dado_config.idioma(169),valor = titulo_atual,font_u = font_old,window = self.JANELA_TOPLEVEL_GRAFICO, uti = self.uti, Dado_config = self.Dado_config )
            if font_new:
                self.Dado_config.set_font_Settings(INTERFACE,font_new)
                self.Dado_config.Settings[INTERFACE]["sTitle_B"] = titulo_bar_new
                self.COLORBAR_TOPLEVEL_GRAFICO.ax.set_title(titulo_bar_new,**font_new)
            elif titulo_atual != titulo_bar_new:
                self.Dado_config.Settings[INTERFACE]["sTitle_B"] = titulo_bar_new
                self.COLORBAR_TOPLEVEL_GRAFICO.ax.set_title(titulo_bar_new)
                
        elif Evento == "tick_bar_graph":
            
            tick_bar_atual_vmax = self.COLORBAR_TOPLEVEL_GRAFICO.vmax
            tick_bar_atual_vmin = self.COLORBAR_TOPLEVEL_GRAFICO.vmin
            tick_bar_novo_vmax = askEntry(self.master,titulo = "Max Vtec",valor = tick_bar_atual_vmax, window = self.JANELA_TOPLEVEL_GRAFICO, font_c = False, uti = self.uti, Dado_config = self.Dado_config, Numeric = True)
            tick_bar_novo_vmin = askEntry(self.master,titulo = "Min Vtec",valor = tick_bar_atual_vmin, window = self.JANELA_TOPLEVEL_GRAFICO, font_c = False, uti = self.uti, Dado_config = self.Dado_config, Numeric = True)
            try:
                tick_bar_novo_vmax = float(tick_bar_novo_vmax)
                tick_bar_novo_vmin = float(tick_bar_novo_vmin)
                if (tick_bar_atual_vmax != tick_bar_novo_vmax) or (tick_bar_atual_vmin != tick_bar_novo_vmin):
                    self.Dado_config.Settings[INTERFACE]["fValueMax_B_VTEC"] = float(tick_bar_novo_vmax)
                    self.Dado_config.Settings[INTERFACE]["fValueMin_B_VTEC"] = float(tick_bar_novo_vmin)
                    self.THREAD_PLOTAR_GRAFICO_JANELA_TOPLEVEL_GRAFICO(INTERFACE)
            except ValueError:pass

        elif Evento == "tick_bar_graph_model":
            old_MAX_VALUE_BAR = self.Dado_config.Settings[self.plot_ATIVO]["fValueMax_B_%s"%GID_EVENT[2]]
            old_MIN_VALUE_BAR = self.Dado_config.Settings[self.plot_ATIVO]["fValueMin_B_%s"%GID_EVENT[2]]
            old_VALUE_TicksCbar = self.Dado_config.Settings[self.plot_ATIVO]["iTicksCbar_%s"%GID_EVENT[2]]
            old_VALUE_DivTicks = self.Dado_config.Settings[self.plot_ATIVO]["iDivTicks_%s"%GID_EVENT[2]]
            new_VALUES_BAR = askEntryBoxColorBar(
                self.master,
                valorMax = old_MAX_VALUE_BAR,
                valorMin = old_MIN_VALUE_BAR,
                vTicksCbar = old_VALUE_TicksCbar,
                vDivTicks = old_VALUE_DivTicks,
                window = self.JANELA_TOPLEVEL_GRAFICO,
                uti = self.uti,
                Dado_config = self.Dado_config 
            )
            new_MAX_VALUE_BAR, new_MIN_VALUE_BAR, new_VALUE_TicksCbar, new_VALUE_DivTicks = new_VALUES_BAR
            if old_MAX_VALUE_BAR != new_MAX_VALUE_BAR:self.Dado_config.Settings[self.plot_ATIVO]["fValueMax_B_%s"%GID_EVENT[2]] = new_MAX_VALUE_BAR
            if old_MIN_VALUE_BAR != new_MIN_VALUE_BAR:self.Dado_config.Settings[self.plot_ATIVO]["fValueMin_B_%s"%GID_EVENT[2]] = new_MIN_VALUE_BAR
            if old_VALUE_TicksCbar != new_VALUE_TicksCbar:self.Dado_config.Settings[self.plot_ATIVO]["iTicksCbar_%s"%GID_EVENT[2]] = new_VALUE_TicksCbar
            if old_VALUE_DivTicks != new_VALUE_DivTicks:self.Dado_config.Settings[self.plot_ATIVO]["iDivTicks_%s"%GID_EVENT[2]] = new_VALUE_DivTicks
            if self.plot_ATIVO == "PAINEL MAPA":self.PLOTAR_GRAFICO_JANELA_TOPLEVEL_MODELO_GRAFICO_PAINEL_MAPA()
            elif self.plot_ATIVO == "MAPA":self.PLOTAR_GRAFICO_JANELA_TOPLEVEL_MODELO_GRAFICO_MAPA()

        elif Evento == "label_bar_graph_model":
            titulo_atual = self.Dado_config.Settings[INTERFACE]["sTitle_B_%s"%GID_EVENT[2]]
            old_font = self.Dado_config.get_font_Settings(INTERFACE)
            titulo_bar_model_map, font = askEntry(self.master,titulo = self.Dado_config.idioma(169),valor = titulo_atual,font_u = old_font,window = self.JANELA_TOPLEVEL_GRAFICO,uti = self.uti,Dado_config = self.Dado_config)
            if font:
                self.Dado_config.set_font_Settings(INTERFACE,font)
                self.Dado_config.Settings[INTERFACE]["sTitle_B_%s"%GID_EVENT[2]] = titulo_bar_model_map
                event.artist.axes.set_title(titulo_bar_model_map,**font)
            elif titulo_atual != titulo_bar_model_map:
                event.artist.axes.set_title(titulo_bar_model_map)
                self.Dado_config.Settings[INTERFACE]["sTitle_B_%s"%GID_EVENT[2]] = titulo_bar_model_map

        elif Evento == "ticks_x":
            print('---X')
            try:self.Dado_config.Settings[INTERFACE]["fValueMin_Axes_X_temp"], self.Dado_config.Settings[INTERFACE]["fValueMax_Axes_X_temp"] = self.AXES_TOPLEVEL_GRAFICO.get_xlim()
            except AttributeError:self.Dado_config.Settings[INTERFACE]["fValueMin_Axes_X_temp"], self.Dado_config.Settings[INTERFACE]["fValueMax_Axes_X_temp"] = self.AXES_TOPLEVEL_GRAFICO[0][0].get_xlim()
            
            
            
                
            askEntrytick(
                titulo = 'X',
                interface = INTERFACE,
                window = self.JANELA_TOPLEVEL_GRAFICO,
                uti = self.uti,
                Dado_config = self.Dado_config 
            )
            self.THREAD_PLOTAR_GRAFICO_JANELA_TOPLEVEL_GRAFICO(INTERFACE)

        elif Evento == "ticks_y":
            print('---Y')
            try:self.Dado_config.Settings[INTERFACE]["fValueMin_Axes_Y_temp"], self.Dado_config.Settings[INTERFACE]["fValueMax_Axes_Y_temp"] = self.AXES_TOPLEVEL_GRAFICO.get_ylim()
            except AttributeError:self.Dado_config.Settings[INTERFACE]["fValueMin_Axes_Y_temp"], self.Dado_config.Settings[INTERFACE]["fValueMax_Axes_Y_temp"] = self.AXES_TOPLEVEL_GRAFICO[0][0].get_ylim()
            if INTERFACE == "INDIVIDUAL":
                self.Dado_config.Settings[INTERFACE]["fValueMin_Axes_Y_temp"]/=60
                self.Dado_config.Settings[INTERFACE]["fValueMax_Axes_Y_temp"]/=60
            elif INTERFACE == "ROT":
                self.Dado_config.Settings[INTERFACE]["fValueMin_Axes_Y_temp"]*=2
                self.Dado_config.Settings[INTERFACE]["fValueMax_Axes_Y_temp"]*=2
            askEntrytick(
                titulo = 'Y',
                interface = INTERFACE,
                window = self.JANELA_TOPLEVEL_GRAFICO,
                uti = self.uti,
                Dado_config = self.Dado_config 
            )
            self.THREAD_PLOTAR_GRAFICO_JANELA_TOPLEVEL_GRAFICO(INTERFACE)

        self.ATUALIZAR_CANVAS_JANELA_TOPLEVEL_GRAFICO()

    def event_key_Left_INTERFACE_PRINCIPAL(self, event):
        print("event_key_Left_INTERFACE_PRINCIPAL")

    def event_key_Right_INTERFACE_PRINCIPAL(self, event):
        print(event)
        print("event_key_Right_INTERFACE_PRINCIPAL")

    def event_key_press(self, event):
        sys.stdout.flush()
        if event.key == 'left':self.event_button_mouse_press(self.AXES_TOPLEVEL_GRAFICO,0)
        elif event.key == 'right':self.event_button_mouse_press(self.AXES_TOPLEVEL_GRAFICO,24)

    def Thread_LINHAS_UT_GRAFICO_JANELA_TOPLEVEL_GRAFICO(self, line, pos = None, interface = None):
        
        Thread(target = self.LINHAS_UT_GRAFICO_JANELA_TOPLEVEL_GRAFICO, args = (line, pos, interface,), daemon = True).start()

    def LINHAS_UT_GRAFICO_JANELA_TOPLEVEL_GRAFICO(self, line, pos = None, interface = None):
        
        if self.Value_Line_Horas_JANELA_TOPLEVEL_GRAFICO.get():
            try:event_button_mouse = line.button
            except AttributeError:event_button_mouse = MouseButton.LEFT
            if event_button_mouse is MouseButton.LEFT:
                try:
                    if pos != None:
                        time = pos
                        ax = line
                    else:
                        time = line.xdata
                        ax = line.inaxes
                    hours = int(time)
                    minutes = (time*60) % 60
                    seconds = (time*3600) % 60
                    s3 = "%s %d:%02d:%02d" % (self.Dado_config.idioma(41),hours, minutes, seconds)
                    if self.plot_ATIVO == "DESVIO":
                        for COL_AXE_TOPLEVEL_GRAFICO in self.AXES_TOPLEVEL_GRAFICO:
                            for LINE_AXE_TOPLEVEL_GRAFICO in COL_AXE_TOPLEVEL_GRAFICO:
                                LINE_AXE_TOPLEVEL_GRAFICO.axvline(time, 0, 1, c="b")
                                
                                    
                                
                                LINE_AXE_TOPLEVEL_GRAFICO.text(time+.05,(ax.get_ylim()[1])*self.Cont_Line_Horas_JANELA_TOPLEVEL_GRAFICO,s3,rotation=00,**self.Dado_config.get_font_Settings(ax.get_gid()))
                                
                    self.Cont_Line_Horas_JANELA_TOPLEVEL_GRAFICO+=.1
                    self.FIGURA_TOPLEVEL_GRAFICO.canvas.draw()                
                except (TypeError,AttributeError) as e:print(e)
    
    def set_VARS_LOCS_MAPA_PRINCIPAL(self):
        self.Lista_Nomes_Locais = self.Dado_config.Settings["MAPAS"]["lNameMAP"]
        self.Lista_Locais_MAPA = []
        strNomes = ""
        for maps in self.Lista_Nomes_Locais:strNomes+=maps
        if strNomes:
            self.Lista_Locais_MAPA = self.Dado_config.Settings["MAPAS"]["lLocs"]
            self.Lista_Locais_MAPA = [[float(pp)for pp in self.Lista_Locais_MAPA[x:x+4]] for x in range(0, len(self.Lista_Locais_MAPA), 4)]
        else:self.Dado_config.Settings["INTERFACE"]["sMap"] = " "
    
    def del_extends_MAPA_PRINCIPAL(self):


        if tk.messagebox.askokcancel(self.Dado_config.idioma(145),self.Dado_config.idioma(194)+' "'+self.Value_cb_Local_MAPA.get()+'"?',parent=self.master):
            cont = 0
            for del_map in self.uti.list_duplicates_of(self.Dado_config.Settings["MAPAS"]["lNameMAP"],self.Value_cb_Local_MAPA.get()):
                del(self.Dado_config.Settings["MAPAS"]["lNameMAP"][del_map-cont])
                pos_del=del_map*4
                del(self.Dado_config.Settings["MAPAS"]["lLocs"][pos_del:pos_del+4])
                cont+=1
            self.cb_Local_Mapa.config(values = self.Lista_Nomes_Locais)
            self.MAPA = self.Dado_config.Settings["MAPAS"]["lNameMAP"][0]
            self.Value_cb_Local_MAPA.set(self.MAPA)
            self.Set_Local_MAPA(self.MAPA)
            self.set_VARS_LOCS_MAPA_PRINCIPAL()


    def save_extends_MAPA_PRINCIPAL(self):
        name_MAPA = askEntry(self.master,titulo = self.Dado_config.idioma(152),valor = "MAP", font_c = False, window = self.master, uti = self.uti, Dado_config = self.Dado_config )
        self.MAPA = name_MAPA
        self.Dado_config.Settings["MAPAS"]["lNameMAP"].append(name_MAPA)
        [self.Dado_config.Settings["MAPAS"]["lLocs"].append(p) for p in self.MAPA_Get_extent_with_zoom()]
        self.cb_Local_Mapa.config(values = self.Lista_Nomes_Locais)
        self.Value_cb_Local_MAPA.set(self.MAPA)
        self.set_VARS_LOCS_MAPA_PRINCIPAL()
    
    def tool_start_siglas_mapa(self):
        self.Value_Mostrar_Estacoes_MAPA_PRINCIPAL.set(not self.Value_Mostrar_Estacoes_MAPA_PRINCIPAL.get())
        self.start_siglas_mapa()
        
    def start_siglas_mapa(self):
        if self.Value_Mostrar_Estacoes_MAPA_PRINCIPAL.get():
            for obj_Annotate in self.List_Annotate_OBS_Station:obj_Annotate.set_visible(True)
        else:
            for obj_Annotate in self.List_Annotate_OBS_Station:obj_Annotate.set_visible(False)
        self.FIGURA_MAPA_PRINCIPAL.canvas.draw()
        self.FIGURA_MAPA_PRINCIPAL.canvas.flush_events()

    def start_gerar_GOOGLE_KMZ(self):
        thread_GOOGLE_KMZ = thread_with_trace(target = self.gerar_GOOGLE_KMZ) 
        thread_GOOGLE_KMZ.start()

    def gerar_GOOGLE_KMZ(self):
        List_Stations_OBS_select = []
        if self.Listbx_Stations_OBS.curselection():
            for estacoes in self.Listbx_Stations_OBS.curselection():
                string_estacao = self.Listbx_Stations_OBS.get(estacoes).replace(",","").replace("(","").replace(")","").split()
                XLT_EST = float(string_estacao[1])
                XLN_EST = float(string_estacao[2])
                DIP_EST = float(string_estacao[3])
                NOME_EST = string_estacao[0]
                List_Stations_OBS_select.append([NOME_EST,XLT_EST,XLN_EST,DIP_EST])
        kml=simplekml.Kml()
        eq_y = []
        eq_x = []
        ano = int(self.Value_DATA_entry_main_inicio.get()[-4:])
        for x in np.arange(-180,181, .1):
            inclinacao = self.uti.get_inclinacao(300,ano,0,0,x,0)
            diplat = -(math.degrees(math.atan(((math.tan(math.radians(float(inclinacao)))/2)))))
            eq_y.append(diplat)
            eq_x.append(x)
        for x,y in zip(eq_y,eq_x):
            a = kml.newpoint(coords=[(y,x)])
            a.style.iconstyle.scale = 1
            a.style.iconstyle.color = simplekml.Color.black
        for x in np.arange(-180,181,.1):
            a = kml.newpoint(coords=[(x,0)])
            a.style.iconstyle.scale = .8
            a.style.iconstyle.color = simplekml.Color.yellow
        for nome,latitude,longitude,dip in List_Stations_OBS_select:
            a = kml.newpoint(name=("%s (%.2f)"%(nome,dip)),coords=[(longitude,latitude)])
            a.style.iconstyle.scale = 5
            a.style.labelstyle.scale = 5
            a.style.iconstyle.color = simplekml.Color.yellow	
        kml.save(("%s/UTECDA_GOOGLE_EARTH_%s.kml"%(self.filedir.get(),ano)))
        tk.messagebox.showinfo(self.Dado_config.idioma(145), self.Dado_config.idioma(190), parent = self.master)
        
        return

    def close_JANELA_TOPLEVEL_GRAFICO(self, *event):
        if self.plot_ATIVO == "INDIVIDUAL":pass
        elif self.plot_ATIVO == "EIA":pass
        elif self.plot_ATIVO == "MAPA":pass
        elif self.plot_ATIVO == "DESVIO":pass
        elif self.plot_ATIVO == "PAINEL MAPA":pass
        elif self.plot_ATIVO == "ROT":self.FIGURA_TOPLEVEL_GRAFICO.canvas.mpl_disconnect(self.ID_Connection_MPL_CANVAS_MAPA_TOPLEVEL_ROT_LINHAS)

        print("|salvando tamanho|")
        self.Dado_config.Settings[self.plot_ATIVO]["fTop"]=self.FIGURA_TOPLEVEL_GRAFICO.subplotpars.top
        self.Dado_config.Settings[self.plot_ATIVO]["fBottom"]=self.FIGURA_TOPLEVEL_GRAFICO.subplotpars.bottom
        self.Dado_config.Settings[self.plot_ATIVO]["fLeft"]=self.FIGURA_TOPLEVEL_GRAFICO.subplotpars.left
        self.Dado_config.Settings[self.plot_ATIVO]["fRight"]=self.FIGURA_TOPLEVEL_GRAFICO.subplotpars.right
        self.Dado_config.Settings[self.plot_ATIVO]["fHspace"]=self.FIGURA_TOPLEVEL_GRAFICO.subplotpars.hspace
        self.Dado_config.Settings[self.plot_ATIVO]["fWspace"]=self.FIGURA_TOPLEVEL_GRAFICO.subplotpars.wspace
        size_inches_fig_width,size_inches_fig_height=self.FIGURA_TOPLEVEL_GRAFICO.get_size_inches()
        self.Dado_config.Settings[self.plot_ATIVO]["fSize_inches_fig_width"]=size_inches_fig_width
        self.Dado_config.Settings[self.plot_ATIVO]["fSize_inches_fig_height"]=size_inches_fig_height
        print("|salvando tamanho|")
        self.JANELA_TOPLEVEL_GRAFICO.withdraw()

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        


    def Exibir_Toplevel_GRAFICO(self):
        if self.JANELA_TOPLEVEL_GRAFICO.state() == "withdrawn" or self.JANELA_TOPLEVEL_GRAFICO.state() == "iconic":
            self.uti.center_to_two_monitor(self.JANELA_TOPLEVEL_GRAFICO)
            self.JANELA_TOPLEVEL_GRAFICO.deiconify()
            
            self.JANELA_TOPLEVEL_GRAFICO.state("zoomed")

        elif self.JANELA_TOPLEVEL_GRAFICO.state() == "normal":
            self.JANELA_TOPLEVEL_GRAFICO.focus_force()

    def setarIDI(self,id):
        if self.Dado_config.Settings["INTERFACE"]["iLanguage"] != id:
            if tk.messagebox.askokcancel(self.Dado_config.idioma(145),self.Dado_config.idioma(147),parent=self.master):
                self.Dado_config.Settings["INTERFACE"]["iLanguage"] = id
                self.Dado_config.writeConfig()
                self.Restart_Program()

    def Restart_Program(self):
        os.execl(sys.executable, sys.executable, *sys.argv)

    def Quit_Program(self):
        self.Dado_config.writeConfig()




        try:
            plt.close('all')
            self.master.destroy()
        except (AttributeError, RuntimeError):
            print('Não iniciou thread')
            self.master.destroy()



if __name__ == "__main__":
    try:
        root = tk.Tk()
        
        Main_UTECDA(root).pack(side="top", fill="both", expand = True)
        root.mainloop()
    except (Exception) as exp:
        Utilitarios().gravar_erro(exp)




