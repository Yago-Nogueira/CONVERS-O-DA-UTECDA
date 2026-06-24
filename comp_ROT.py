from matplotlib.offsetbox import AnnotationBbox, TextArea
from matplotlib.backend_bases import MouseButton
from matplotlib.offsetbox import AnchoredText
from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import Qt
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
from util import Utilitarios
from shared_utils import (
    apply_tick_params, configure_axis_locator, apply_axes_limits,
    setup_tick_label_pickers, build_cmn_filepath,
)
import numpy as np
import threading
from matplotlib.ticker import AutoMinorLocator

class COMP_ROT(QDialog):	
    def __init__(self,matplotlib_figure,estacao_info,filedir,datafile,color,legenda,dado_config, dados,Xminor,Yminor,rots):
        self._matplotlib_figure = matplotlib_figure
        self._sigla_estacao = estacao_info[0].lower()
        try:self._dip_estacao = estacao_info[3]
        except IndexError:self._dip_estacao = estacao_info[1] + " " + estacao_info[2]
        self._filedir = filedir
        self._datafile = datafile
        self._color = color
        self._legenda = legenda
        self._dado_config = dado_config
        self.uti = Utilitarios()
        self.dados=dados#adicionado para inserir vtec
        self.Xminor=Xminor
        self.Yminor=Yminor
        self.rots=rots
        self.font = self._dado_config.get_font_Settings("ROT")
        self._titulo = (("%s-%.2i-%.2i-%i") % (self._sigla_estacao,self._datafile.day,self._datafile.month,self._datafile.year)) 
        self.contador_linhas = 0
        self._coe_rot = .5
        self.list_scatter = []
        self.txb_PRN_ROT = TextArea("", minimumdescent=False)
        self.xybox_PRN_ROT=(50., 50.)
        self.ab_PRN_ROT = AnnotationBbox(self.txb_PRN_ROT, (0,0), xybox=self.xybox_PRN_ROT, xycoords='data', boxcoords="offset points",  pad=0.3,  arrowprops=dict(arrowstyle="->"))
        self.ab_PRN_ROT.set_visible(False)

        # plt.rc('axes',linewidth=2)
        # plt.rc('font', weight='bold')
        # self.titulo_axe_y_rot = None
        # self.titulo_axe_x_rot = None
        # self.passo_tickX_rot = None
        # self.n_rotuloX_rot = None
        # self.minX_rot = None
        # self.maxX_rot = None
        # self.passo_tickY_rot = None
        # self.n_rotuloY_rot = None
        # self.minY_rot = None
        # self.maxY_rot = None
        # self.sigla_estacao = sigla.lower()
        # self.rfont_titulo_axe_y_rot = self.rfont_titulo_axe_x_rot = self.rfont_titulo_graph_rot = font_default = {'family' : 'Arial', 'weight' : 'bold','size'   : 18}


    def _set_Matplotlib_grafico(self):
        if self.dados=="ROT":
            self._dado_config.Settings["ROT"]["sTitle_Y"] = "ROT (PRN)"
        elif self.dados=="ROTI":
            self._dado_config.Settings["ROT"]["sTitle_Y"] = "ROTi (PRN)"
        else:
            self._dado_config.Settings["ROT"]["sTitle_Y"] = "VTEC (PRN)"
        _titulox = self._dado_config.Settings["ROT"]["sTitle_X"]
        _tituloy = self._dado_config.Settings["ROT"]["sTitle_Y"]

        intervalo_LEITURA_CMN = 30# segundos
        intervalo_LEITURA_CMN/=3600
        dia_ano = self._datafile.timetuple().tm_yday
        caminho = build_cmn_filepath(self._filedir, self._sigla_estacao, self._datafile)
        self.list_prn,dado_cmn = self.uti.Leitura_CMN_DICT(destino = caminho, ele = self._dado_config.Settings["ROT"]["fElevation_Filter"])
        #print ('**********************************',self.dados,self._dado_config.Settings["ROT"]["sTitle_Y"], self._dado_config.Settings["ROT"]["fValueMultFactor_ROT"], self._coe_rot)
        self.dados_organizados = {};
        if self.list_prn and dado_cmn:
            for prn in self.list_prn:
                str_prn = str(prn)
                self.dados_organizados[str_prn] = {}
                for hora in dado_cmn[str_prn + ".time"]:
                    self.dados_organizados[str_prn][hora] = {}
                    ind = dado_cmn[str_prn + ".time"].index(hora)
                    self.dados_organizados[str_prn][hora]['vtec'] = dado_cmn[str_prn + ".vtec"][ind]

            self.dados_organizados_plot = {}
            for prn in self.list_prn:
                str_prn = str(prn)
                self.dados_organizados_plot[str_prn] = {}
                self.dados_organizados_plot[str_prn]['time'] = []
                if self.dados=="ROT":
                    self.dados_organizados[str_prn] = self.uti.get_ROT(self.dados_organizados[str_prn], delta_time_rot = self._dado_config.Settings["ROT"]["fValueDelta_ROT"], intervalo_LEITURA_CMN = 30, Fator_multplicacao = self._dado_config.Settings["ROT"]["fValueMultFactor_ROT"])
                    self.dados_organizados_plot[str_prn]['rot'] = []
                elif self.dados=="VTEC":
                    self.dados_organizados_plot[str_prn]['vtec'] = []
                elif self.dados=="ROTI":
                    self.dados_organizados[str_prn] = self.uti.get_ROT(self.dados_organizados[str_prn], delta_time_rot = self._dado_config.Settings["ROT"]["fValueDelta_ROT"], intervalo_LEITURA_CMN = 30, Fator_multplicacao = self._dado_config.Settings["ROT"]["fValueMultFactor_ROT"])
                    self.dados_organizados[str_prn] = self.uti.get_ROTI(self.dados_organizados[str_prn], delta_time_roti = self._dado_config.Settings["ROT"]["fValueDelta_ROTI"], intervalo_LEITURA_CMN = 30)
                    self.dados_organizados_plot[str_prn]['roti'] = []
                for hora in self.dados_organizados[str_prn].keys():
                    self.dados_organizados_plot[str_prn]['time'].append(float(hora))
                    if self.dados=="ROT":
                        if self.rots.get()==1:
                            self.dados_organizados_plot[str_prn]['rot'].append(self.dados_organizados[str_prn][hora]['rot']+(prn*self._coe_rot))
                        else:
                            self.dados_organizados_plot[str_prn]['rot'].append(self.dados_organizados[str_prn][hora]['rot']*self._coe_rot)
                    elif self.dados=="VTEC":
                        self.dados_organizados_plot[str_prn]['vtec'].append(self.dados_organizados[str_prn][hora]['vtec']*self._coe_rot)
                    elif self.dados=="ROTI":
                        if self.rots.get()==1:
                            self.dados_organizados_plot[str_prn]['roti'].append(self.dados_organizados[str_prn][hora]['roti']+(prn*self._coe_rot))
                        else:
                            self.dados_organizados_plot[str_prn]['roti'].append(self.dados_organizados[str_prn][hora]['roti']*self._coe_rot)

            self._matplotlib_figure.clf()
            self._matplotlib_figure.set_facecolor('lightgrey')
            self._axes = self._matplotlib_figure.subplots()
            self._axes.set_facecolor("lightgrey")
            self._axes.yaxis.set_major_formatter(ticker.FuncFormatter(self.major_formatteY))
            # self._axes.yaxis.set_major_formatter(ticker.FuncFormatter(self.major_formatteY))
            self._axes.set_xlim(0,24)
            self._axes.set_ylim(0,17)

            configure_axis_locator(self._axes.yaxis, self._dado_config.Settings, "ROT", "Y", ticker.LinearLocator(6))
            configure_axis_locator(self._axes.xaxis, self._dado_config.Settings, "ROT", "X", ticker.LinearLocator(8))
            apply_axes_limits(self._axes, self._dado_config.Settings, "ROT", y_scale=0.5)



            
            
            AncoredText_DIP = AnchoredText("%s(dip latitude %s"% (self._sigla_estacao.upper(),self._dip_estacao),borderpad=0, loc='upper left', prop=self.font,frameon=False)
            self._axes.add_artist(AncoredText_DIP)
            self._axes.set_gid("ROT")
            self._axes.set_title(self._titulo,picker=5,gid="titulo_graph:ROT",**self.font)
            self._axes.set_ylabel(_tituloy, picker=5, gid="y_label_graph:ROT",**self.font)
            self._axes.set_xlabel(_titulox, picker=5, gid="x_label_graph:ROT",**self.font)
            self._axes.minorticks_on()
            self._axes.yaxis.set_minor_locator(AutoMinorLocator(int(self.Yminor)))
            self._axes.xaxis.set_minor_locator(AutoMinorLocator(int(self.Xminor)))
            if self._color:		
                NUM_COLORS = len(self.list_prn)
                cm = plt.get_cmap('jet')
                self._axes.set_prop_cycle('color', [cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])
                #arq=open("vgp.txt","w")
                for prn in self.list_prn:
                    str_prn = str(prn)
                    if self.dados=="ROT":
                        self._axes.scatter(self.dados_organizados_plot[str_prn]['time'],self.dados_organizados_plot[str_prn]['rot'],linewidths = .1,label = ("PRN (%s)"%(prn)), marker = '.')#, picker=on_picker)
                        #arq.write(str(str_prn)+'\t'+str(self.dados_organizados_plot[str_prn]['time'])+ '\t'+str(self.dados_organizados_plot[str_prn]['rot'])+'\n')
                    elif self.dados=="ROT":
                        self._axes.scatter(self.dados_organizados_plot[str_prn]['time'],self.dados_organizados_plot[str_prn]['vtec'],linewidths = .1,label = ("PRN (%s)"%(prn)), marker = '.')#, picker=on_picker)
                        #arq.write(str(str_prn)+'\t'+str(self.dados_organizados_plot[str_prn]['time'])+ '\t'+str(self.dados_organizados_plot[str_prn]['vtec'])+'\n')
                    elif self.dados=="ROTI":
                        self._axes.scatter(self.dados_organizados_plot[str_prn]['time'],self.dados_organizados_plot[str_prn]['roti'],linewidths = .1,label = ("PRN (%s)"%(prn)), marker = '.')#, picker=on_picker)
                #arq.close()
                if self._legenda:
                    handles, labels = self._axes.get_legend_handles_labels()
                    # prop=self.font
                    self._axes.legend(handles, labels, bbox_to_anchor=(1.009, 0, .1, 1.9),loc=3,ncol=1, mode="expand", borderaxespad=0.,facecolor='lightgrey',prop= dict(weight='bold',size=12))
            else:
                for prn in self.list_prn:
                    str_prn = str(prn)
                    if self.dados=="ROT":
                        sc = self._axes.scatter(self.dados_organizados_plot[str_prn]['time'],self.dados_organizados_plot[str_prn]['rot'],linewidths = .1,label = ("PRN (%s)"%(prn)),c='blue',marker = '.')#, picker=on_picker)
                    elif self.dados=="VTEC":
                        sc = self._axes.scatter(self.dados_organizados_plot[str_prn]['time'],self.dados_organizados_plot[str_prn]['vtec'],linewidths = .1,label = ("PRN (%s)"%(prn)),c='blue',marker = '.')#, picker=on_picker)
                    elif self.dados=="ROTI":
                        sc = self._axes.scatter(self.dados_organizados_plot[str_prn]['time'],self.dados_organizados_plot[str_prn]['roti'],linewidths = .1,label = ("PRN (%s)"%(prn)),c='blue',marker = '.')#, picker=on_picker)
                    self.list_scatter.append(sc)
                    # self._axes.scatter(dados_organizados_plot[str_prn]['time'],dados_organizados_plot[str_prn]['rot'],linewidths = .1,label = ("PRN (%s)"%(prn)),c='blue',marker = '.')#, picker=on_picker)

            setup_tick_label_pickers(self._axes, "ROT")
            
            # self._matplotlib_figure.canvas.mpl_connect('button_press_event', self.Func_event_button_mouse_press)
            # self._matplotlib_figure.canvas.mpl_connect('key_press_event', self.Func_event_key_press)

            self._matplotlib_figure.canvas.mpl_connect('motion_notify_event', self.thread_vis_info)
            # self._matplotlib_figure.canvas.mpl_connect('motion_notify_event', self.vis_info)
            apply_tick_params(self._axes, self._dado_config.Settings, "ROT")
            self._axes.add_artist(self.ab_PRN_ROT)
        else:
            self._axes = None
            self._matplotlib_figure.text(.5,.5, self._dado_config.idioma(94), ha="center", va="center" )
            
    def thread_vis_info(self,event):
        threading.Thread(target=self.vis_info, args = (event,), daemon = True).start()

    def vis_info(self,event):
        temp_pth = ""
        for pth in self.list_scatter:
            if pth.contains(event)[0]:

                temp_pth = pth
                w,h = self._matplotlib_figure.get_size_inches()*self._matplotlib_figure.dpi
                
                ws = (event.x > w/2.)*-1 + (event.x <= w/2.)
                hs = (event.y > h/2.)*-1 + (event.y <= h/2.)

                self.ab_PRN_ROT.xybox = (ws, self.xybox_PRN_ROT[1]*hs)
                # self.ab_PRN_ROT.xybox = (self.xybox_PRN_ROT[0]*ws, self.xybox_PRN_ROT[1]*hs)
                data = temp_pth.get_offsets()[0]
                self.ab_PRN_ROT.xy =(event.xdata, data[1])
                # self.ab_PRN_ROT.xy =(data[0], data[1])
                PRN_ = int(temp_pth.get_label().replace("PRN (","").replace(")",""))
                ROT_ = (event.ydata) - (PRN_*self._coe_rot)
                self.txb_PRN_ROT.set_text(temp_pth.get_label() + " ROT: %.2f"%ROT_)
                self.ab_PRN_ROT.set_visible(True)
                break
            else:
                self.ab_PRN_ROT.set_visible(False)
                self.ab_PRN_ROT.set_visible(False)

            self._matplotlib_figure.canvas.draw_idle()
            
    # def event_key_press(self, event):
    #     sys.stdout.flush()
    #     if event.key == 'left':
    #         self.event_button_mouse_press(self._axes,0)
    #     elif event.key == 'right':
    #         self.event_button_mouse_press(self._axes,24)

    # def event_button_mouse_press(self, line, pos = None):
    #     try:   
    #         event_button_mouse = line.button
    #     except AttributeError:
    #         event_button_mouse = MouseButton.LEFT    

    #     if event_button_mouse is MouseButton.LEFT:
    #         try:
    #             if pos != None:
    #                 time = pos
    #                 ax = line
    #             else:
    #                 time = line.xdata
    #                 ax = line.inaxes
    #             hours = int(time)   
    #             minutes = (time*60) % 60
    #             seconds = (time*3600) % 60
    #             s3 = "%s %d:%02d:%02d" % (self._dado_config.idioma(41),hours, minutes, seconds)
    #             self._axes.axvline(time, 0, 1, c="b")
    #             # if time > 12:
    #                 # self._axes.text(time,(ax.get_ylim()[1]/2)*self.contador_linhas,s3,rotation=90,**self.font)
    #             # else:
    #             self._axes.text(time,(ax.get_ylim()[1]/2)*self.contador_linhas,s3,rotation=90,**self.font)
    #             # picker=5,gid="texto_line:ROT",
    #             self.contador_linhas+=.1
    #             self._matplotlib_figure.canvas.draw()
    #         except TypeError:
    #             pass

    def major_formatteY(self,y, pos):
        if self.dados=="ROTI":
            return "%.2f" % (y/self._coe_rot)
        elif self.rots.get()==0 and self.dados=="ROT":
            return "%.2f" % (y/self._coe_rot)
        else:
            return "%i" % (y/self._coe_rot)

    def _get_Matplotlib_grafico_att(self):
        return self._matplotlib_figure,self._axes,self._titulo,self.list_prn,self.dados_organizados
