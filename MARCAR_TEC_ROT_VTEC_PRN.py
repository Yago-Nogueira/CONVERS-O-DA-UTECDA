from util import Utilitarios,DadoIdioma
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime#, timedelta, date
import math, os, sys
import matplotlib.ticker as ticker
from matplotlib.offsetbox import AnchoredText
import matplotlib


Dado_config = DadoIdioma()

def major_formatteY(x, pos):
    # return "%i" % (x)
    return "%i" % (x/coe_rot)

_filedir = r"D:\IP&D\Dados\CMN\2021"

# _data = datetime.strptime("03/07/2021", '%d/%m/%Y')
_data = datetime.strptime("28/10/2021", '%d/%m/%Y')

_dia_ano = _data.timetuple().tm_yday

# _siglas = [["NKLG",-23.07,30.38,-13.94]]
# _siglas = [["BOAV",-23.07,30.38,8.622]]


# _siglas = [["BELE",-23.07,30.38,-1.383]]
# _siglas = [["SAGA",-23.07,30.38,8.603]]
# _siglas = [["TOPL",-23.07,30.38,-9.358]]
# _siglas = [["SALU",-23.07,30.38,-4.876]]


# _siglas = [["YKRO",-23.07,30.38,-5.883]]
# _siglas = [["GODE",-23.07,30.38,47.354]]
# _siglas = [["STHL",-23.07,30.38,-35.184]]
_siglas = [["HARB",-23.07,30.38,-41.359]]





coe_rot = .5
coe_roti = .15

_elevacao = 30.0
delta_time_rot = 300
Delta_T_ROT = delta_time_rot/3600 # segundos - > horas 
intervalo_LEITURA_CMN = 30# segundos
intervalo_LEITURA_CMN/=3600

horas = np.arange(0, 24, intervalo_LEITURA_CMN)

_titulo_bar = "vtec"
# _titulo_bar = "rot"

_rfont_titulo = {'family' : 'Arial','weight' : 'bold','size'   : 20}

uti = Utilitarios()

contttt = 0

lista_String_INFO_TEXT = []

def on_press2(line=None):
    dirpasta = r"%s\PONTOS_ESTACOES"% _filedir
    nom = "%s%s_%s"%(_siglas[0][0],_data.strftime("(%d-%m-%Y)"),_titulo_bar.upper())
    if not os.path.exists(dirpasta):
        os.makedirs(dirpasta)    
    plt.savefig(r"%s\%s.png"%(dirpasta,nom))


def on_pressauto(event):
    sys.stdout.flush()
    if event.key == 'left':
        on_press(AXs,0)
    elif event.key == 'right':
        on_press(AXs,24)

def on_press(line, pos = None):
    global contttt
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
        # print("-----------------------------------------------")
        s1 = "Estação: %s"%_siglas[0][0]
        s2 = "Dip: %s"%_siglas[0][3]
        s3 = "Hora: %d:%02d:%02d" % (hours, minutes, seconds)
        s4 = _data.strftime("%d/%m/%Y")
        s5 = "-----------------------------------------------"
        print(s1)
        print(s2)
        print(s3)
        print(s4)
        print(s5)
        lista_String_INFO_TEXT.append(s1)
        lista_String_INFO_TEXT.append(s2)
        lista_String_INFO_TEXT.append(s3)
        lista_String_INFO_TEXT.append(s4)
        lista_String_INFO_TEXT.append(s5)

        plt.axvline(time, 0, 1, c="b")
        if time > 12:
            # plt.text(time-3,-2,s3,**_rfont_titulo)
            plt.text(time-3,(ax.get_ylim()[1]/2)*contttt,s3,**_rfont_titulo)
        else:
            # plt.text(time,-2,s3,**_rfont_titulo)
            plt.text(time,(ax.get_ylim()[1]/2)*contttt,s3,**_rfont_titulo)
        
        contttt+=.1
        FIGs.canvas.draw()

        # FIGs.canvas.draw()
        # FIGs.canvas.flush_events()


    except TypeError:
        pass



nome_est = []
list_prn = []
dados_organizados = {}
for es in _siglas:
    es = es[0]
    caminho = (("%s\\%s%.3i-%s-%.2i-%.2i.Cmn") % (_filedir,es.lower(),_dia_ano,_data.year,_data.month,_data.day))
    prns_cmn,dado_cmn = uti.Leitura_CMN_DICT(destino = caminho, ele = _elevacao)
    if prns_cmn and dado_cmn:
        _es = es.lower()
        nome_est.append(_es)
        list_prn.append(prns_cmn)
        dados_organizados[_es] = {}
        for prn in prns_cmn:
            str_prn = str(prn)
            dados_organizados[_es][str_prn] = {}
            for hora in dado_cmn[str_prn + ".time"]:
                dados_organizados[_es][str_prn][hora] = {}
                ind = dado_cmn[str_prn + ".time"].index(hora)
                # dados_organizados[_es][str_prn][hora]['lon'] = dado_cmn[str_prn + ".lon"][ind]
                # dados_organizados[_es][str_prn][hora]['lat'] = dado_cmn[str_prn + ".lat"][ind]
                dados_organizados[_es][str_prn][hora]['vtec'] = dado_cmn[str_prn + ".vtec"][ind]
    else:
        quit()



dados_organizados_plot = {}
for _est,_prn in zip(nome_est,list_prn):
    dados_organizados_plot[_est] = {}

    for prn in _prn:
        str_prn = str(prn)
        # dados_organizados[_est][str_prn] = uti.get_ROT(dados_organizados[_est][str_prn], delta_time_rot = 60, intervalo_LEITURA_CMN = 30)
        # dados_organizados[_est][str_prn] = uti.get_ROTI(dados_organizados[_est][str_prn], delta_time_roti = 300, intervalo_LEITURA_CMN = 30)
        dados_organizados_plot[_est][str_prn] = {}
        dados_organizados_plot[_est][str_prn]['time'] = []
        dados_organizados_plot[_est][str_prn]['vtec'] = []
        # dados_organizados_plot[_est][str_prn]['rot'] = []
        # dados_organizados_plot[_est][str_prn]['roti'] = []

        for hora in dados_organizados[_est][str_prn].keys():
            dados_organizados_plot[_est][str_prn]['time'].append(float(hora))
            dados_organizados_plot[_est][str_prn]['vtec'].append(dados_organizados[_est][str_prn][hora]['vtec'])
            # dados_organizados_plot[_est][str_prn]['rot'].append(dados_organizados[_est][str_prn][hora]['rot']+(prn*coe_rot))
            # dados_organizados_plot[_est][str_prn]['roti'].append(dados_organizados[_est][str_prn][hora]['roti']+(prn*coe_roti))


plt.rc('font', weight='bold')
plt.rc('axes',linewidth=2)
FIGs,AXs = plt.subplots(len(_siglas),1)
FIGs.subplots_adjust(wspace=0,hspace=0)
FIGs.suptitle(("%s-%.2i-%.2i"%(_data.year,_data.month,_data.day)),fontsize=20,fontweight='bold',y=.91)
FIGs.canvas.mpl_connect('button_press_event', on_press)
FIGs.canvas.mpl_connect('key_press_event', on_pressauto)
FIGs.canvas.mpl_connect('close_event', on_press2)



for (AX,es,prns) in zip([AXs],_siglas,list_prn):
    sigla_es = es[0].lower()

    AX.tick_params(axis='x', which='minor', width=Dado_config.Settings["ROT"]["fWidthTickMinor_X"],size=Dado_config.Settings["ROT"]["fHeightTickMinor_X"])#,labelsize=tam_x))
    AX.tick_params(axis='x', which='major', width=Dado_config.Settings["ROT"]["fWidthTickMajor_X"],size=Dado_config.Settings["ROT"]["fHeightTickMajor_X"],labelsize=Dado_config.Settings["ROT"]["fSizeLabelsTick_X"])
    AX.tick_params(axis='y', which='minor', width=Dado_config.Settings["ROT"]["fWidthTickMinor_Y"],size=Dado_config.Settings["ROT"]["fHeightTickMinor_Y"])#,labelsize=tam_y))
    AX.tick_params(axis='y', which='major', width=Dado_config.Settings["ROT"]["fWidthTickMajor_Y"],size=Dado_config.Settings["ROT"]["fHeightTickMajor_Y"],labelsize=Dado_config.Settings["ROT"]["fSizeLabelsTick_Y"])


    AX.minorticks_on()
    AX.set_ylabel(("%s (PRN)"%_titulo_bar.upper()),fontsize = 20,fontweight='bold')
    # AX.set_facecolor("lightgrey")

    
    # VTEC
    
    AX.set_xlim(11,17)
    AX.xaxis.set_major_locator(ticker.FixedLocator(np.arange(11,18,1)))
    # AX.set_xlim(0,24)
    # AX.xaxis.set_major_locator(ticker.FixedLocator(np.arange(0,25,4)))
    AX.set_ylim(0,55)
    AX.yaxis.set_major_locator(ticker.FixedLocator(np.arange(0,56,5)))
    
    # ROT
    
    # AX.set_ylim(0, 17.009)
    # AX.yaxis.set_major_formatter(ticker.FuncFormatter(major_formatteY))
    # AX.set_xlim(11,17)
    # AX.xaxis.set_major_locator(ticker.FixedLocator(np.arange(11,18,1)))
    # # AX.set_xlim(11,17)
    # # AX.xaxis.set_major_locator(ticker.FixedLocator(np.arange(0,25,4)))
    # # AX.set_xlim(-1,25)
    # # AX.set_ylim(-0.3490000000000024, 17.009)
       

    
    # AX.yaxis.set_major_locator(ticker.FixedLocator([0,10*coe_rot,20*coe_rot,30*coe_rot]))
    [i.set_visible(False) for i in AX.xaxis.get_major_ticks()]

    # FIGs.set_facecolor('lightgrey')
    for prn in prns:
        str_prn = str(prn)
        # AX.plot(dados_organizados_plot[sigla_es][str_prn]['time'],(dados_organizados_plot[sigla_es][str_prn][_titulo_bar]),label ='PRN '+str_prn)
        AX.scatter(dados_organizados_plot[sigla_es][str_prn]['time'],dados_organizados_plot[sigla_es][str_prn][_titulo_bar],linewidths = .1,label ='PRN '+str_prn, marker = '.')#, picker=on_picker)
    
    
    AncoredText_DIP = AnchoredText( "%s(dip latitude %s)"%(sigla_es.upper(),es[-1]),borderpad=0, loc=2, prop=dict(fontweight="bold",fontsize=20),frameon=False)
    AX.add_artist(AncoredText_DIP)
    
else:
    [i.set_visible(True) for i in AX.xaxis.get_major_ticks()]
    AX.set_xlabel("UT",fontweight='bold',fontsize = 20)


# plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,ncol=1, mode="expand", borderaxespad=0.)
# plt.legend(bbox_to_anchor=(1.009, 0, .1, 1.9), loc=3,ncol=1, mode="expand", borderaxespad=0.,facecolor='lightgrey')
# plt.grid()
# FIG.savefig(r"C:\Users\Mateus_Pillat\Desktop\Gráficos Fagundes\PRN-POVE-2015-03-20.png")

# mng = plt.get_current_fig_manager()
# mng.frame.Maximize(True)
# FIGs.canvas.manager.window.showMaximized()

figManager = plt.get_current_fig_manager()
figManager.window.showMaximized()

# mng = plt.get_current_fig_manager()
# mng.resize(*mng.window.maxsize())
plt.show()