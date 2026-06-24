

from util import Utilitarios,DadoIdioma
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime#, timedelta, date
import math
import matplotlib.ticker as ticker
import os

# def major_formatteY(x, pos):
#     return "%i" % (x/10)

#11.091667
plt.rc('axes', linewidth = 2)
plt.rc('font', weight = 'bold')
_filedir = os.path.join(os.path.expanduser('~'), 'UTECDA', 'DADOS_TEC')
# _filedir = r"C:\CMN_BRASIL"
#_filedir = r"D:\IP&D\Dados\CMN\2017"


_data = datetime.strptime("08/09/2017", '%d/%m/%Y')
# _data = datetime.strptime("01/03/2015", '%d/%m/%Y')



_vm = 1#100.0
_h_i = 0
_h_f = 24
_h_interval = 30.0 #segundoas
_siglas = [['TOPL']]
# _siglas = [['GOJA', '-9', '44', '-36', '39']]
_elevacao = 30.0
_titulo_bar = "ROT"
_rfont_titulo_bar = {'family' : 'Arial','weight' : 'bold','size'   : 18}
uti = Utilitarios()
dia_ano = _data.timetuple().tm_yday
delta_time_rot = 300
Delta_T_ROT = delta_time_rot/3600 # segundos - > horas 
intervalo_LEITURA_CMN = 30# segundos
intervalo_LEITURA_CMN/=3600

# horas = np.arange(0, (24+intervalo_LEITURA_CMN), intervalo_LEITURA_CMN)
horas = np.arange(0, 24, intervalo_LEITURA_CMN)

dados_organizados = {}
list_prn = []
nome_est = []

_elevacao = 30.0
_titulo_bar = "ROT"


_rfont_titulo_bar = {'family' : 'Arial','weight' : 'bold','size'   : 18}
fig,axes = plt.subplots()
fig.set_facecolor('lightgrey')
# fig.set_facecolor('white')
uti = Utilitarios()
Dado_config = DadoIdioma()
dia_ano = _data.timetuple().tm_yday


for es in _siglas:
    es = es[0]
    caminho = (("%s\\%s%.3i-%s-%.2i-%.2i.Cmn") % (_filedir,es.lower(),dia_ano,_data.year,_data.month,_data.day))
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
                dados_organizados[_es][str_prn][hora]['lon'] = dado_cmn[str_prn + ".lon"][ind]
                dados_organizados[_es][str_prn][hora]['lat'] = dado_cmn[str_prn + ".lat"][ind]
                dados_organizados[_es][str_prn][hora]['vtec'] = dado_cmn[str_prn + ".vtec"][ind]


dados_organizados_plot = {}
for _est,_prn in zip(nome_est,list_prn):
    # NUM_COLORS = len(_prn)
    # cm = plt.get_cmap('jet')
    # axes.set_prop_cycle('color', [cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])
    # fig.clf()
    fig.set_facecolor('lightgrey')

    for prn in _prn:
        str_prn = str(prn)
        dados_organizados[_est][str_prn] = uti.get_ROT(dados_organizados[_est][str_prn], delta_time_rot = 60, intervalo_LEITURA_CMN = 30)
        lista_ROT = []
        for hora in horas:
            hora = (("%.6f") % hora)[:-1]
            try:
                lista_ROT.append(dados_organizados[_est][str(prn)][hora]['rot'])
            except KeyError:
                lista_ROT.append(np.nan)
        
        # print(dados_organizados[_est][str_prn])
        # dados_organizados[_est][str_prn] = uti.get_ROTI(dados_organizados[_est][str_prn], delta_time_roti = 300, intervalo_LEITURA_CMN = 30)
        
        # axes.tick_params(axis='x', which='minor', width=Dado_config.getWidthTickMinor_X('Rot'),size=Dado_config.getHeightTickMinor_X('Rot'))#,labelsize=tam_x))
        # axes.tick_params(axis='x', which='major', width=Dado_config.getWidthTickMajor_X('Rot'),size=Dado_config.getHeightTickMajor_X('Rot'),labelsize=Dado_config.getSizeLabelsTick_X('Rot'))
        # axes.tick_params(axis='y', which='minor', width=Dado_config.getWidthTickMinor_Y('Rot'),size=Dado_config.getHeightTickMinor_Y('Rot'))#,labelsize=tam_y))
        # axes.tick_params(axis='y', which='major', width=Dado_config.getWidthTickMajor_Y('Rot'),size=Dado_config.getHeightTickMajor_Y('Rot'),labelsize=Dado_config.getSizeLabelsTick_Y('Rot'))
        axes.set_facecolor("lightgrey")
        
        plt.ylabel('ROT',**_rfont_titulo_bar)
        plt.xlabel('UT',**_rfont_titulo_bar)
        plt.title(("PRN %s"%str_prn),**_rfont_titulo_bar)
        plt.xlim(0,24)
        

        
       
        plt.plot(horas,lista_ROT, lw = 1, label = ("PRN (%s)"%(str_prn)))
        
        # axes.legend(bbox_to_anchor=(1.009, 0, .1, 1.9), loc=3,ncol=1, mode="expand", borderaxespad=0.,facecolor='lightgrey')#.draggable(True)#,facecolor='lightgrey')
        # axes.yaxis.set_major_formatter(ticker.FuncFormatter(major_formatteY))
        # axes.yaxis.set_major_locator(ticker.FixedLocator([pr * 10 for pr in np.arange(_prn[0],_prn[-1]+1)]))

        axes.set_xlim(0,24)
        axes.xaxis.set_major_locator(ticker.FixedLocator(np.arange(0,25,1)))
    plt.show()
        # quit()
plt.close() 



# for _est,_prn in zip(nome_est,list_prn):
    # for prn in _prn:
        # dados_organizados[_est][str(prn)] = uti.get_ROT(dados_organizados[_est][str(prn)], delta_time_rot = 300, intervalo_LEITURA_CMN = 30)
        
        

        









# print(dados)
# print(len(['11.000000', '11.008333', '11.016667', '11.025000', '11.033333', '11.041667', '11.050000', '11.058333', '11.066667', '11.075000', '11.083333', '11.091667', '11.100000', '11.108333', '11.116667', '11.125000', '11.133333', '11.141667', '11.150000', '11.158333', '11.166667', '11.175000', '11.183333', '11.191667', '11.200000', '11.208333', '11.216667', '11.225000', '11.233333', '11.241667', '11.250000', '11.258333', '11.266667', '11.275000', '11.283333', '11.291667', '11.300000', '11.308333', '11.316667', '11.325000', '11.333333', '11.341667', '11.350000', '11.358333', '11.366667', '11.375000', '11.383333', '11.391667', '11.400000', '11.408333', '11.416667', '11.425000', '11.433333', '11.441667', '11.450000', '11.458333', '11.466667', '11.475000', '11.483333', '11.491667', '11.500000', '11.508333', '11.516667', '11.525000', '11.533333', '11.541667', '11.550000', '11.558333', '11.566667', '11.575000', '11.583333', '11.591667', '11.600000', '11.608333', '11.616667', '11.625000', '11.633333', '11.641667', '11.650000', '11.658333', '11.666667', '11.675000', '11.683333', '11.691667', '11.700000', '11.708333', '11.716667', '11.725000', '11.733333', '11.741667', '11.750000', '11.758333', '11.766667', '11.775000', '11.783333', '11.791667', '11.800000', '11.808333', '11.816667', '11.825000', '11.833333', '11.841667', '11.850000', '11.858333', '11.866667', '11.875000', '11.883333', '11.891667', '11.900000', '11.908333', '11.916667', '11.925000', '11.933333', '11.941667', '11.950000', '11.958333', '11.966667', '11.975000', '11.983333', '11.991667', '12.000000', '12.008333', '12.016667', '12.025000', '12.033333', '12.041667', '12.050000', '12.058333', '12.066667', '12.075000', '12.083333', '12.091667', '12.100000', '12.108333', '12.116667', '12.125000', '12.133333', '12.141667', '12.150000', '12.158333', '12.166667', '12.175000', '12.183333', '12.191667', '12.200000', '12.208333', '12.216667', '12.225000', '12.233333', '12.241667', '12.250000', '12.258333', '12.266667', '12.275000', '12.283333', '12.291667', '12.300000', '12.308333', '12.316667', '12.325000', '12.333333', '12.341667', '12.350000', '12.358333', '12.366667', '12.375000', '12.383333', '12.391667', '12.400000', '12.408333', '12.416667', '12.425000', '12.433333', '12.441667', '12.450000', '12.458333', '12.466667', '12.475000', '12.483333', '12.491667', '12.500000', '12.508333', '12.516667', '12.525000', '12.533333', '12.541667', '12.550000', '12.558333', '12.566667', '12.575000', '12.583333', '12.591667', '12.600000', '12.608333', '12.616667', '12.625000', '12.633333', '12.641667', '12.650000', '12.658333', '12.666667', '12.675000', '12.683333', '12.691667', '12.700000', '12.708333', '12.716667', '12.725000', '12.733333', '12.741667']))
# 210

# for _est,_prn in zip(nome_est,list_prn):
#   for prn in _prn:
#       VTEC = []
#       for hora in horas:
#           # inds = uti.list_duplicates_of(dados[sigla_est][str(prn)+".time"],f_hora)
#           # dados_no_tempo[]
#           _hora = ("%.6f"%hora)
#           try:
#               VTEC.append(dados[_est][str(prn) + ".vtec"][dados[_est][str(prn) + ".time"].index(_hora)])
#           except ValueError:
#               VTEC.append(np.nan)



#       plt.xlabel('UT')
#       plt.ylabel('ROT')
#       plt.xlim(0,24)

#       plt.plot(horas,VTEC)
#   plt.show()


    # dado_cmn['1.time'].
    # dado_cmn['1.vtec']



# for horas in np.arange(0, (24+(intervalo_LEITURA_CMN/3600)), (intervalo_LEITURA_CMN/3600))
#   print(hora)


# dados_organizados = {}
# for hora in np.arange(_h_i,_h_f,(_h_interval/60)):
#   f_hora = ("%.6f"%hora)
#   dados_organizados[f_hora+".vtec"] = []
#   dados_organizados[f_hora+".lat"] = []
#   dados_organizados[f_hora+".lon"] = []
#   dados_organizados[f_hora+".rot"] = []
#   dados_organizados[f_hora+".roti"] = []
#   for sigla_est,_prn in zip(nome_est,list_prn):
#       for prn in _prn:
#           inds = uti.list_duplicates_of(dados[sigla_est][str(prn)+".time"],f_hora)
#           for ind in inds:
#               dados_organizados[f_hora+".vtec"].append(dados[sigla_est][str(prn)+'.vtec'][ind])
#               dados_organizados[f_hora+".lat"].append(dados[sigla_est][str(prn)+'.lat'][ind])
#               dados_organizados[f_hora+".lon"].append(dados[sigla_est][str(prn)+'.lon'][ind])
#               dados_organizados[f_hora+".rot"].append(dados[sigla_est][str(prn)+'.rot'][ind])
#               dados_organizados[f_hora+".roti"].append(dados[sigla_est][str(prn)+'.roti'][ind])

# print(dados_organizados)





