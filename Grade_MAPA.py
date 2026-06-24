import numpy as np
import pandas as pd
from util import Utilitarios
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, date
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from scipy.interpolate import griddata
import os,math
import matplotlib as mpl
import copy

# mpl.use('Agg')




############################################################################################
######################|TESTES GRADES|#######################################################
# from datetime import datetime, timedelta, date
# import pandas as pd

# start = '01/09/2017 00:00:00'
# end = '01/09/2017 12:00:00'

# start = datetime.strptime(start, "%d/%m/%Y %H:%M:%S")
# end = datetime.strptime(end, "%d/%m/%Y %H:%M:%S")

# for xx in range(100,2000,10):
#     date = pd.date_range(start = start, end = end, freq='%iS'%xx)
#     print(len(date))
#     print(date)

# quit()
######################|TESTES GRADES|#######################################################
############################################################################################








# def on_press(event):
#     print('press', event.key)
#     if event.key == 'x':
#         FIG.savefig(camff,dpi=FIG.dpi)


# base = datetime.today()
# date_list = [base - timedelta(days=x) for x in range(7)]

# print(date_list)



# start = datetime.strptime("07/09/2017", '%d/%m/%Y ')
# end = datetime.strptime("08/09/2017", '%d/%m/%Y ')

_filedir = r"D:\IP&D\Dados\CMN\2017"

# _h_i = 0
# _h_f = 24
_h_interval = .5 #minutos
_h_interval/=60
intervalo_LEITURA_CMN = 30
intervalo_LEITURA_CMN/=3600

plt.rc('font', weight='bold')
plt.rc('axes',linewidth=2)


_rfont_titulo_bar = {'family' : 'Arial','weight' : 'bold','size'   : 38}
_rfont_time_map = {'family' : 'Arial','weight' : 'bold','size'   : 11}

#######################|VTEC|###############################
# _titulo_bar = "VTEC"
#######################|ROTI|###############################
_titulo_bar = "ROTI"


start = '08/09/2017 14:00:00'
end = '08/09/2017 22:45:00'

start = datetime.strptime(start, "%d/%m/%Y %H:%M:%S")
end = datetime.strptime(end, "%d/%m/%Y %H:%M:%S")


datas = pd.date_range(start = start, end = end, freq='900S')
print(datas)
ncols = 6
nrows = 6

"""
Alias   /   Description
   B        /   business day frequency
   C        /   custom business day frequency
   D        /   calendar day frequency
   W        /   weekly frequency
   M        /   month end frequency
   SM       /   semi-month end frequency (15th and end of month)
   BM       /   business month end frequency
   CBM      /   custom business month end frequency
   MS       /   month start frequency
   SMS      /   semi-month start frequency (1st and 15th)
   BMS      /   business month start frequency
   CBMS     /   custom business month start frequency
   Q        /   quarter end frequency
   BQ       /   business quarter end frequency
   QS       /   quarter start frequency
   BQS      /   business quarter start frequency
   A, Y     /   year end frequency
   BA, BY   /   business year end frequency
   AS, YS   /   year start frequency
   BAS, BYS /   business year start frequency
   BH       /   business hour frequency
   H        /   hourly frequency
   T, min   /   minutely frequency
   S        /   secondly frequency
   L, ms    /   milliseconds
   U, us    /   microseconds
   N        /   nanoseconds
"""

date_dias = pd.date_range(start = start.date(), end = end.date(), freq='D')

# print(len(datas))
print(datas)
# print(date_dias)

#######################|LEITURA DADOS|###############################
uti = Utilitarios()

# _extend_LAT_LONG = [-77, -32, -35, 7];mapa = 'Brasil'
# _siglas = [["ALAR",-9.73,-36.65,-14.92],["AMBC",0.97,-62.92,8.55],["AMCO",-4.87,-65.33,4.17],["AMHU",-7.50,-63.03,1.03],["AMMU",-3.40,-57.72,2.47],["AMPR",-2.63,-56.73,2.69],["AMTA",-4.22,-69.93,6.00],["AMTE",-3.35,-64.70,5.32],["AMUA",-3.10,-60.02,3.76],["APLJ",0.82,-52.50,3.68],["APS1",0.07,-51.17,2.30],["APSA",0.05,-51.17,2.28],["BABJ",-13.27,-43.55,-13.90],["BABR",-12.15,-44.98,-12.10],["BAIL",-14.80,-39.17,-17.83],["BAIR",-11.30,-41.87,-13.22],["BAIT",-12.52,-40.28,-15.22],["BATF",-17.55,-39.75,-19.72],["BAVC",-14.88,-40.80,-16.91],["BELE",-1.40,-48.45,-0.51],["BEPA",-1.45,-48.43,-0.56],["BOAV",2.83,-60.70,9.35],["BOMJ",-13.25,-43.42,-13.97],["BRAZ",-15.95,-47.88,-13.62],["BRAZ",-15.93,-47.87,-13.61],["BRFT",-3.87,-38.42,-8.45],["BRFT",-3.88,-38.43,-8.45],["CEEU",-3.87,-38.42,-8.45],["CEFE",-20.32,-40.32,-21.52],["CEFT",-3.70,-38.47,-8.26],["CESB",-3.68,-40.33,-7.20],["CHPI",-22.68,-44.98,-20.56],["CHPI",-22.68,-44.98,-20.56],["COAM",-4.08,-63.13,4.12],["CORU",-19.00,-57.63,-11.15],["CRAT",36.80,-116.57,42.95],["CRAT",-7.23,-39.40,-11.04],["CRUZ",-7.60,-72.67,3.41],["CUIB",-15.55,-56.07,-8.96],["EESC",-22.00,-47.90,-18.42],["FORT",-3.87,-38.42,-8.45],["GOGY",-16.67,-49.25,-13.44],["GOJA",-17.88,-51.73,-13.09],["GOUR",-14.52,-49.15,-11.70],["GVA1",-18.85,-41.95,-19.43],["GVAL",-18.85,-41.95,-19.43],["IFSC",-27.60,-48.55,-22.10],["ILHA",-20.43,-51.35,-15.34],["IMBT",-28.23,-48.65,-22.47],["IMPZ",-5.48,-47.48,-4.76],["ITAI",-25.42,-54.58,-17.60],["ITAM",-3.13,-58.43,3.03],["JAMG",-15.35,-43.77,-15.52],["MABA",-5.35,-49.12,-3.71],["MABB",-4.23,-44.82,-5.15],["MABS",-7.53,-46.03,-7.43],["MANA",12.15,-86.25,22.42],["MANA",-3.10,-60.05,3.77],["MAPA",0.08,-51.10,2.28],["MCL1",-16.72,-43.88,-16.58],["MCLA",-22.75,-70.25,-10.57],["MCLA",-16.72,-43.88,-16.58],["MGBH",-19.93,-43.92,-19.10],["MGIN",-22.32,-46.33,-19.53],["MGMC",-16.72,-43.85,-16.60],["MGMT",-18.72,-47.52,-16.07],["MGRP",-19.22,-46.13,-17.26],["MGUB",-18.92,-48.25,-15.82],["MGV1",-21.55,-45.43,-19.46],["MGVA",-21.55,-45.43,-19.46],["MSAQ",-20.45,-55.67,-13.22],["MSCB",-18.98,-56.62,-11.58],["MSCG",-20.43,-54.53,-13.74],["MSCG",34.03,-116.65,40.11],["MSCO",-19.00,-57.63,-11.15],["MSDO",-22.22,-54.80,-15.04],["MSDR",-22.20,-54.93,-14.96],["MSPP",-22.62,-55.62,-14.98],["MTBA",-15.88,-52.25,-11.16],["MTCN",-13.55,-52.27,-9.17],["MTCO",-10.80,-55.45,-5.16],["MTGA",-15.88,-52.32,-11.12],["MTJI",-11.43,-58.72,-4.19],["MTJU",-11.42,-58.77,-4.15],["MTNX",-14.70,-52.35,-10.11],["MTSF",-11.62,-50.67,-8.38],["MTSR",-12.55,-55.73,-6.54],["MTVB",-15.00,-59.95,-6.77],["NAUS",-3.02,-60.05,3.85],["NAUS",-77.52,167.15,-72.42],["NEIA",-25.02,-47.92,-20.63],["ONRJ",-22.90,-43.22,-21.73],["OURI",-22.95,-49.90,-18.05],["PAAT",-3.20,-52.17,-0.12],["PAIT",-4.28,-56.03,0.88],["PARA",-25.43,-49.22,-20.24],["PASM",-2.43,-54.73,1.89],["PAST",-2.50,-54.72,1.83],["PBCG",-7.20,-35.90,-13.01],["PBJP",-7.13,-34.87,-13.52],["PEAF",-7.77,-37.63,-12.55],["PEPE",-9.38,-40.50,-12.34],["PICR",-10.43,-45.17,-10.50],["PIFL",-6.78,-43.03,-8.50],["PISR",-9.03,-42.70,-10.72],["PITN",-5.10,-42.80,-7.10],["POAL",-30.07,-51.12,-22.48],["POLI",-23.55,-46.73,-20.21],["POVE",-8.72,-63.90,0.25],["PPTE",-22.12,-51.42,-16.63],["PRCV",-24.97,-53.47,-17.78],["PRGU",-25.38,-51.48,-19.05],["PRMA",-23.42,-51.93,-17.36],["RECF",-8.05,-34.97,-14.33],["RECF",-8.05,-34.95,-14.34],["RIOB",-9.97,-67.80,0.29],["RIOD",-22.82,-43.30,-21.62],["RJCG",-21.75,-41.32,-22.00],["RNMO",-5.20,-37.33,-10.32],["RNNA",-5.83,-35.20,-12.10],["RNPF",-6.13,-38.20,-10.71],["ROCD",-13.12,-60.55,-4.89],["ROGM",-10.78,-65.33,-1.13],["ROJI",-10.87,-61.97,-2.36],["ROSA",-22.52,-52.95,-16.16],["RSAL",-29.78,-55.77,-20.25],["RSCL",-28.15,-54.75,-19.52],["RSPE",-31.80,-52.42,-23.01],["RSPF",-28.23,-52.38,-20.65],["SAGA",0.15,-67.05,9.20],["SALU",-2.60,-44.22,-3.98],["SALU",-2.60,-44.22,-3.98],["SALV",-13.00,-38.50,-16.70],["SAVO",-12.93,-38.43,-16.69],["SAVO",-12.93,-38.43,-16.69],["SCAQ",-26.38,-48.73,-21.16],["SCCH",-27.13,-52.58,-19.78],["SCFL",-27.60,-48.52,-22.11],["SCLA",-27.80,-50.30,-21.35],["SEAJ",-10.92,-37.10,-15.72],["SJRP",-20.78,-49.37,-16.68],["SJSP",-23.20,-45.87,-20.44],["SMAR",-29.72,-53.72,-21.07],["SPAR",-21.18,-50.43,-16.42],["SPBO",-22.85,-48.43,-18.76],["SPBP",-22.98,-46.53,-19.91],["SPC1",-22.82,-47.07,-19.49],["SPCA",-22.80,-47.05,-19.49],["SPDR",-21.45,-51.55,-16.04],["SPFE",-20.27,-50.23,-15.80],["SPFR",-20.52,-47.38,-17.57],["SPJA",-21.23,-48.28,-17.62],["SPLI",-21.67,-49.73,-17.16],["SPPI",-22.70,-47.62,-19.10],["SPS1",-23.48,-47.42,-19.79],["SPSO",-23.48,-47.42,-19.79],["SPTU",-21.93,-50.50,-16.96],["SSA1",-12.98,-38.52,-16.68],["TOGU",-11.73,-49.03,-9.39],["TOPL",-10.17,-48.33,-8.43],["UBA1",-23.50,-45.12,-21.08],["UBAT",-23.50,-45.12,-21.08],["UBE1",-18.88,-48.32,-15.76],["UBER",-18.88,-48.32,-15.76],["UEPP",-22.12,-51.40,-16.64],["UFPR",-25.45,-49.23,-20.24],["UFPR",-25.43,-49.22,-20.24],["VARG",-21.53,-45.43,-19.45],["VICO",-20.77,-42.87,-20.36]]

_extend_LAT_LONG = [-27, 61, -35, 46];mapa = 'Africa'
_siglas = ['SULP', 'ZECK', 'ISBA', 'GRAS', 'NAST', 'ONSA', 'HUEG', 'BSHM', 'BUCU', 'MADR', 'TASH', 'KMTR', 'SEAJ', 'IENG', 'SEY2', 'IRKM', 'EBRE', 'MORP', 'RABT', 'TUBI', 'CEFT', 'PTBB', 'MTDK', 'PBJP', 'NKLG', 'ZIMM', 'OBE4', 'MBEY', 'SUMK', 'KATC', 'BHR4', 'MEDI', 'OPMT', 'GRAC', 'YEBE', 'CEBR', 'ONS1', 'SUTV', 'KITG', 'WIND', 'KOS1', 'ALAR', 'MERS', 'GANP', 'PADO', 'LEIJ', 'MAYG', 'BHR3', 'BJCO', 'FFMJ', 'ISTA', 'MAT1', 'ARUC', 'MAUA', 'SUTH', 'RNMO', 'MTVE', 'BZRG', 'NICO', 'ABOO', 'CRAO', 'LCK3', 'MOBJ', 'HALY', 'METG', 'HERS', 'BAKU', 'STHL', 'MARS', 'SEYG', 'KUWT', 'BIK0', 'KFNY', 'PENC', 'ZIM2', 'PRE4', 'GOPE', 'MOBN', 'MFKG', 'M0SE', 'DAKR', 'PODG', 'IRKJ', 'MET3', 'TETN', 'RBAY', 'YIBL', 'OAK2', 'SGOC', 'OAK1', 'LHAZ', 'DEAR', 'DGAR', 'GRAZ', 'TIT2', 'RASH', 'JIR2', 'CPVG', 'SFER', 'VILL', 'SEKC', 'HAMD', 'CHUM', 'LAMA', 'SNGC', 'HYDE', 'GRHI', 'SASS', 'TEHN', 'MELI', 'MOBK', 'RNPF', 'ASCG', 'HERT', 'IZMI', 'JMSM', 'TDOU', 'VACS', 'SVTL', 'GLSV', 'ZOMB', 'KLCK', 'NOVM', 'POLV', 'KIT3', 'PRE3', 'LMJG', 'TLSG', 'REUN', 'MUET', 'YKRO', 'CEEU', 'SYBC', 'BRFT', 'SNDL', 'LUZZ', 'POL2', 'POTS', 'MAL2', 'RECF', 'ADIS', 'NVSK', 'PEAF', 'MBAR', 'RAMO', 'ZAMB', 'ANKR', 'KRS1', 'SABD', 'METS', 'GANJ', 'RIGA', 'OLO7', 'IISC', 'ORID', 'RNNA', 'DRAG', 'KHAR', 'KKN4', 'MATE', 'REDU', 'TNDC', 'DODM', 'SOFI', 'HARB', 'MDVJ', 'ROAP', 'LPAL', 'ZIMJ', 'LROC', 'PBCG', 'NEFT', 'OUCA', 'SPT0', 'ULDI', 'TALA', 'NOT1', 'MIKL', 'FUNC', 'TLSE', 'DYNG', 'JOZ2', 'HNUS', 'KRTV', 'FLRS', 'NPGJ', 'SUTM', 'NEGE', 'NTUS', 'IFR1', 'JOZE', 'VOIM', 'DJIG', 'MBBC', 'PDEL', 'PIRS', 'HRAC', 'RAEG', 'RMJT', 'MAS1', 'JOG2', 'MAD2', 'LCK4', 'OLO3', 'HRAO', 'SBOK', 'MATL', 'GENO', 'PBRI', 'KAZA', 'AJAC']


_elevacao = 30.0

MEAN_PONTOS_MAPA = []

dados_organizados = {}


day_list_prn = []
day_nome_est = []
for day in date_dias:
    indi_day = day.date()
    list_prn = []
    nome_est = []
    dia_ano = day.timetuple().tm_yday
    dados_organizados[indi_day] = {}
    for es in _siglas:
        # es = es[0].lower()
        es = es.lower()
        caminho = (("%s\\%s%.3i-%s-%.2i-%.2i.Cmn") % (_filedir,es,dia_ano,day.year,day.month,day.day))
        prns_cmn,dado_cmn = uti.Leitura_CMN_DICT(destino = caminho, ele = _elevacao)
        if prns_cmn and dado_cmn:
            nome_est.append(es)
            list_prn.append(prns_cmn)
            dados_organizados[indi_day][es] = {}
            for prn in prns_cmn:
                str_prn = str(prn)
                dados_organizados[indi_day][es][str_prn] = {}
                for hora in dado_cmn[str_prn + ".time"]:
                    dados_organizados[indi_day][es][str_prn][hora] = {}
                    ind = dado_cmn[str_prn + ".time"].index(hora)
                    dados_organizados[indi_day][es][str_prn][hora]['lon'] = dado_cmn[str_prn + ".lon"][ind]
                    dados_organizados[indi_day][es][str_prn][hora]['lat'] = dado_cmn[str_prn + ".lat"][ind]
                    dados_organizados[indi_day][es][str_prn][hora]['vtec'] = dado_cmn[str_prn + ".vtec"][ind]
    day_list_prn.append(list_prn)
    day_nome_est.append(nome_est)


dados_organizados_plot = {}
for day,nome_est,list_prn in zip(date_dias,day_nome_est,day_list_prn):
    indi_day = day.date()
    dados_organizados_plot[indi_day] = {}
    for _est,_prn in zip(nome_est,list_prn):
        for prn in _prn:
            str_prn = str(prn)
            #######################|ROTI|###############################
            dados_organizados[indi_day][_est][str_prn] = uti.get_ROT(dados_organizados[indi_day][_est][str_prn], delta_time_rot = 60, intervalo_LEITURA_CMN = 30)
            dados_organizados[indi_day][_est][str_prn] = uti.get_ROTI(dados_organizados[indi_day][_est][str_prn], delta_time_roti = 300, intervalo_LEITURA_CMN = 30)
            #######################|ROTI|###############################
            for hora in dados_organizados[indi_day][_est][str_prn].keys():  
                f_hora = hora
                #######################|ROTI|###############################
                if not np.isnan(dados_organizados[indi_day][_est][str_prn][f_hora]['roti']):
                #######################|ROTI|###############################
                #######################|VTEC|###############################
                # if not np.isnan(dados_organizados[indi_day][_est][str_prn][f_hora]['vtec']):
                #######################|VTEC|###############################
                    try:
                        dados_organizados_plot[indi_day][f_hora+".lat"].append(dados_organizados[indi_day][_est][str_prn][f_hora]['lat'])
                    except KeyError:
                        dados_organizados_plot[indi_day][f_hora+".lat"] = []
                        dados_organizados_plot[indi_day][f_hora+".lat"].append(dados_organizados[indi_day][_est][str_prn][f_hora]['lat'])
                    try:
                        dados_organizados_plot[indi_day][f_hora+".lon"].append(dados_organizados[indi_day][_est][str_prn][f_hora]['lon'])
                    except KeyError:
                        dados_organizados_plot[indi_day][f_hora+".lon"] = []
                        dados_organizados_plot[indi_day][f_hora+".lon"].append(dados_organizados[indi_day][_est][str_prn][f_hora]['lon'])
                    #######################|ROTI|###############################
                    try:
                        dados_organizados_plot[indi_day][f_hora+".roti"].append(dados_organizados[indi_day][_est][str_prn][f_hora]['roti'])
                    except KeyError:
                        dados_organizados_plot[indi_day][f_hora+".roti"] = []
                        dados_organizados_plot[indi_day][f_hora+".roti"].append(dados_organizados[indi_day][_est][str_prn][f_hora]['roti'])
                    #######################|ROTI|###############################
                    #######################|VTEC|###############################
                    # try:
                    #     dados_organizados_plot[indi_day][f_hora+".vtec"].append(dados_organizados[indi_day][_est][str_prn][f_hora]['vtec'])
                    # except KeyError:
                    #     dados_organizados_plot[indi_day][f_hora+".vtec"] = []
                    #     dados_organizados_plot[indi_day][f_hora+".vtec"].append(dados_organizados[indi_day][_est][str_prn][f_hora]['vtec'])
                    #######################|VTEC|###############################

#######################|LEITURA DADOS|###############################
###########################|VTEC|####################################
# _vm = 35
# level = np.arange(0,(_vm+1),1)
###########################|VTEC|####################################
#######################|LEITURA DADOS|###############################
cmap = copy.copy(mpl.cm.get_cmap("jet"))
cmap.set_under("white")
cmap.set_over("darkred")
###########################|ROTI|####################################
_vm = 0.9
_ticks_cbar = 10
_ticks_divisao = 4
passo = _vm/(_ticks_cbar*_ticks_divisao)
bounds = np.arange(.1,_vm+passo,passo)
ticks = np.arange(0-passo,_vm+2*passo,passo)
ticks_colorbar =  np.arange(0,_vm+passo,0.1)
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
nmap = mpl.cm.ScalarMappable(norm=norm, cmap=cmap)
###########################|ROTI|####################################


numcols, numrows = 100,100
# numcols, numrows = 40,40


eq_y = []
eq_x = []
for x in range(-180,181,1):
    inclinacao = uti.get_inclinacao(300,start.year,0,0,x,0)
    diplat = -(math.degrees(math.atan(((math.tan(math.radians(float(inclinacao)))/2)))))
    eq_y.append(diplat)
    eq_x.append(x)

FIG,List_AXs = plt.subplots(ncols=ncols,nrows=nrows,subplot_kw={'projection': ccrs.PlateCarree()})

# FIG.canvas.mpl_connect('key_press_event', on_press)
#######################|BRASIL|############################
######################|5x5;6x6;6x5|###############################   
# x_text_hora =-50 
# y_text_hora = -36
#######################|5x5;6x6;6x5|###############################   
#######################|7x5|###############################
# x_text_hora =-54 
# y_text_hora = -36
#######################|7x5|###############################
#######################|AFRICA|############################
# x_text_hora = 26 
# y_text_hora = -42
#######################|AFRICA  pc nasa|############################
# x_text_hora = 16 
x_text_hora = 13 
y_text_hora = -42

FIG.subplots_adjust(
#######################|BRASIL|############################
#######################|5x5;6x6;6x5|#######################
    # top=0.975,
    # bottom=0.015,
    # left=0.258,
    # right=0.757,
    # hspace=0.0,
    # wspace=0.0
#######################|5x5;6x6;6x5|###############################
#######################|7x5|###############################
    # top=0.975,
    # bottom=0.015,
    # left=0.4,
    # right=0.757,
    # hspace=0.0,
    # wspace=0.0
#######################|7x5|###############################
#######################|AFRICA|############################
#######################|6x5|###############################
    # top=0.965,
    # bottom=0.015,
    # left=0.398,
    # right=0.757,
    # hspace=0.0,
    # wspace=0.0
#######################|6x5|###############################
#######################|5x5|###############################
    # top=0.965,
    # bottom=0.015,
    # left=0.323,
    # right=0.757,
    # hspace=0.0,
    # wspace=0.0
#######################|5x5|###############################
#######################|5x5 - pc - lab|####################
    # top=0.965,
    # bottom=0.1,
    # left=0.323,
    # right=0.757,
    # hspace=0.0,
    # wspace=0.0
    top=1.0,
    bottom=0.005,
    left=0.257,
    right=0.745,
    hspace=0.0,
    wspace=0.0
#######################|5x5|###############################
)





cont_pos_time = 0
for Ax_cols in List_AXs:
    for Ax_line in Ax_cols:
        # try:
        time = datas[cont_pos_time]
        ut = time.hour + (time.minute/60) + (time.second/3600)
        str_ut = ("%.6f"%ut)[:-1]
        Ax_line.set_extent(_extend_LAT_LONG)
        Ax_line.add_feature(cfeature.BORDERS)
        Ax_line.add_feature(cfeature.COASTLINE)
        # Ax_line.text(-49.9,3, date[cont_pos_time].time())
        Ax_line.text(x_text_hora,y_text_hora, datas[cont_pos_time].time(),**_rfont_time_map)
        [i.set_visible(False) for i in Ax_line.xaxis.get_major_ticks()]
        [i.set_visible(False) for i in Ax_line.yaxis.get_major_ticks()]
        #######################|ROTI|###############################
        x, y, z = np.array(dados_organizados_plot[time.date()][str_ut+'.lon']), np.array(dados_organizados_plot[time.date()][str_ut+'.lat']), np.array(dados_organizados_plot[time.date()][str_ut+'.roti']) 
        #######################|ROTI|###############################
        #######################|VTEC|###############################
        # x, y, z = np.array(dados_organizados_plot[time.date()][str_ut+'.lon']), np.array(dados_organizados_plot[time.date()][str_ut+'.lat']), np.array(dados_organizados_plot[time.date()][str_ut+'.vtec']) 
        MEAN_PONTOS_MAPA.append(len(z))
        # print(len(z))
        # # quit()
        # # print(z)
        # # print(len([z for xxx in z if not np.isnan(z)]))
        #######################|VTEC|###############################
        scx,scy = x, y
        xi = np.linspace(x.min(), x.max(), numcols)
        yi = np.linspace(y.min(), y.max(), numrows)
        xi, yi = np.meshgrid(xi, yi)
        zi = griddata((x, y), z,(xi, yi), method = 'linear')
        x = np.arange(0, zi.shape[1])
        y = np.arange(0, zi.shape[0])
        zi = np.ma.masked_invalid(zi)
        x1 = xi[~zi.mask]
        y1 = yi[~zi.mask]
        newarr = zi[~zi.mask]
        GD1 = griddata((x1, y1), newarr.ravel(),(xi, yi),method='linear')
        Ax_line.plot(eq_x,eq_y,'k')
        # Ax_line.scatter(scx, scy, marker='.',c='red')#, s=10)
        ###########################|VTEC|####################################
        # im = Ax_line.contourf(xi,yi,GD1, cmap = cmap,levels = level, vmin = 0, vmax = _vm ,extend="both",transform=ccrs.PlateCarree())
        ###########################|VTEC|####################################
        ###########################|ROTI|####################################
        Ax_line.contourf(
            xi,yi,GD1,
            cmap = cmap, 
            extend='both',
            levels = bounds,
            transform=ccrs.PlateCarree()
        )
        ###########################|ROTI|####################################
    # except (Exception) as e: 
        # print(e)
        # pass
        cont_pos_time+=1




cbar_ax = FIG.add_axes([0.85, 0.15, 0.0205, 0.7])
###########################|VTEC|####################################
# cbar_mapa = FIG.colorbar(im,ticks = np.arange(0,_vm+1,5) ,cax=cbar_ax) 
###########################|VTEC|####################################
###########################|ROTI|####################################
cbar_mapa = FIG.colorbar(
    nmap,
    cax=cbar_ax,
    boundaries=ticks,
    extend='both',
    spacing='proportional',
    ticks=ticks_colorbar
)
###########################|ROTI|####################################
cbar_mapa.ax.set_title(_titulo_bar,**_rfont_titulo_bar)
cbar_mapa.ax.tick_params(axis='y', which='major', width=2.0,size=10.0,labelsize=23.0)

camff = (("%s\\GRADE_MAPA_Contorno_%s_(%s_%s).png")%(_filedir,_titulo_bar,start.date(),end.date()))
FIG.set_size_inches(20.0, 10.0)
FIG.set_facecolor('lightgrey')

# figManager = plt.get_current_fig_manager()
# figManager.window.showMaximized()
figManager = plt.get_current_fig_manager()
figManager.window.state('zoomed')


FIG.savefig(camff,dpi=FIG.dpi)
print("MAX = %i"%np.max(MEAN_PONTOS_MAPA))
print("MIN = %i"%np.min(MEAN_PONTOS_MAPA))
print("MED = %.2f"%np.mean(MEAN_PONTOS_MAPA))

plt.show()
