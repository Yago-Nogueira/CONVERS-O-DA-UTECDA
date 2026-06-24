from datetime import timedelta, datetime, date
from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import Qt
import numpy as np
from util import Utilitarios, DadoIdioma
from shared_utils import (
	apply_tick_params, ensure_date_order, build_std_filepath,
)
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import warnings
from matplotlib.offsetbox import AnchoredText
from matplotlib.ticker import FormatStrFormatter


class COMP_ONDAS(QDialog):
	def __init__(self, matplotlib_figure, diretorio_dados, siglas_estacao, data_inicial, data_final, formato_data, corte, dado_config):
		self._matplotlib_figure = matplotlib_figure
		self._diretorio_dados = diretorio_dados
		self._siglas_estacao = siglas_estacao
		self._data_inicial = data_inicial
		self._data_final = data_final
		self._formato_data = formato_data
		self._corte=corte
		self._dado_config = dado_config

	def _set_Matplotlib_grafico(self):
		plt.tick_params(axis='both',direction='inout', which='major',top=True)
		plt.tick_params(axis='both',direction='inout', which='minor' ,top=True,right=True)

		self._matplotlib_figure.clf()
##		self.temp = np.array([x for x in np.arange(0,24,(1/60))])					
		self.titulox = self._dado_config.Settings["DESVIO"]["sTitle_X"]
		self.tituloy = self._dado_config.Settings["DESVIO"]["sTitle_Y"]
		self.titulo = ('%s-%s-%s(%s-%s)')%([sigla[0] for sigla in self._siglas_estacao ],self._data_inicial.year,self._data_inicial.month,self._data_inicial.day,self._data_final.day)

		self.cbar = None
		self.matriz_tec = []
		self.uti = Utilitarios()
		font = self._dado_config.get_font_Settings("DESVIO")
		font_anchored = font
		del(font_anchored['family'])
		self._data_inicial, self._data_final = ensure_date_order(self._data_inicial, self._data_final)
		self.delta = self._data_final - self._data_inicial
		#print(self.delta,self._data_final,self._data_inicial)
		self.delta_days = self.delta.days+1
		#self.temp = np.array([x for x in np.arange(self._data_inicial.day+0,self._data_final.day+1,(1/(24*60)))])
		self.temp = np.arange(self._data_inicial,self._data_final+timedelta(days=1),timedelta(minutes=1))
		#self.temp = np.array([x for x in np.arange(0,24*self.delta_days,(1/60))])
		len_est = len(self._siglas_estacao)
		est_s=self._siglas_estacao[0]
		
		#self._axes = self._matplotlib_figure.subplots(len_est,int(self.delta_days),sharex='col', sharey='row')#, squeeze=True)
		self._axes = self._matplotlib_figure.subplots(2,sharex='col', sharey='row')#, squeeze=True)
		# self._matplotlib_figure.subplots_adjust(wspace=0,hspace=0)
		#self._matplotlib_figure.suptitle(self._dado_config.idioma(122), picker=5,gid="Sup_titulo:Desvio",**font)
		self._matplotlib_figure.suptitle(est_s[0], picker=5,gid="Sup_titulo:Desvio",**font)
		self.C_dip_lat = []
		self.C_sigla = []
		self.C_tec = []
		#for est_s in self._siglas_estacao:
		self.matriz_tec_p = []
		self.datas_axes_X = []
		#print((self._data_inicial+timedelta(seconds=i)))
		for contd in range(self.delta_days):
			datafile = (self._data_inicial + timedelta(days=contd))
			self.datas_axes_X.append([datafile.date(),datafile.day])
			caminho_arquivo_p = build_std_filepath(self._diretorio_dados, est_s[0], datafile)
			self.matriz_tec_p.append(self.uti.Leitura_trip(caminho_arquivo_p))
		self.matriz_tec_p2 = np.array(self.matriz_tec_p).reshape(self.delta_days,1440)
		self.matriz_tec_p = np.array(self.matriz_tec_p).reshape(self.delta_days*1440)
		self.C_sigla.append(est_s[0])
		self.C_dip_lat.append(est_s[3])
		self.C_tec.append(self.matriz_tec_p)
		L=[];h=int(self._corte)
		for i in range(self.delta_days):
			#L.append([(self._data_inicial.day+i)+(h/24),self.matriz_tec_p[h*60+(i*1440)]])
                        L.append([self._data_inicial+timedelta(days=i)+timedelta(hours=h),self.matriz_tec_p[h*60+(i*1440)]])
			#print((self._data_inicial.day+i)+(h/24),h*60+(i*1440))#calcular com 1440.
			#print((self._data_inicial+timedelta(seconds=i+(h/24))),h*60+(i*1440))#calcular com 1440.
		print(L)
		L=np.array(L)

		max_G = np.nanmax(self.C_tec)
		if np.isnan(max_G):max_G=1
		print(len(self.matriz_tec_p),self.matriz_tec_p2.shape,self.matriz_tec_p.shape, max_G, self.temp.shape)
		
		#self._axes.scatter(self.temp,self.matriz_tec_p,linewidths = .1,c='blue',marker = '.')
		#self._axes.plot(self.temp,[np.nan if x <0 else x for x in self.matriz_tec_p], color='r',label='Tec',linewidth=2.5)
		self._axes[1].plot(self.temp,self.matriz_tec_p, color='b',label='Tec',linewidth=2.5)
		self._axes[1].plot(L[:,0],L[:,1], '*r')
		self._axes[1].set_facecolor("lightgrey")
		self._axes[1].set_gid("DESVIO")
		#try:self._axes.set_xlim(self._dado_config.Settings["DESVIO"]["fValueMin_Axes_X_temp"],self._dado_config.Settings["DESVIO"]["fValueMax_Axes_X_temp"])
		#except KeyError:self._axes.set_xlim(0,24)
		try:self._axes[1].set_ylim(self._dado_config.Settings["DESVIO"]["fValueMin_Axes_Y_temp"],self._dado_config.Settings["DESVIO"]["fValueMax_Axes_Y_temp"])
		except KeyError:self._axes[1].set_ylim(0,round(max_G+(max_G *(.05*len(est_s[0])))))
		self._axes[1].minorticks_on()
		self._axes[1].yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
		self._axes[1].tick_params(axis='both',direction='inout', which='major',top=True,right=True)
		self._axes[1].tick_params(axis='both',direction='inout', which='minor' ,top=True,right=True)
		apply_tick_params(self._axes[1], self._dado_config.Settings, "DESVIO")
		self._axes[1].tick_params(axis='x',labelrotation=30)
		self._axes[1].set_ylabel(self.tituloy,picker=5,gid="y_label_graph:Desvio",**font)
		self._axes[1].set_xlabel(self.titulox,picker=5,gid="x_label_graph:Desvio",**font)
		
		self._axes[0].minorticks_on()		
		self._axes[0].plot(L[:,0],L[:,1], color='b',linewidth=2.5)
		self._axes[0].plot(L[:,0],L[:,1], '*r')
		self._axes[0].set_facecolor("lightgrey")
		self._axes[0].yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
		self._axes[0].tick_params(axis='both',direction='inout', which='major',top=True,right=True)
		self._axes[0].tick_params(axis='both',direction='inout', which='minor' ,top=True,right=True)
		apply_tick_params(self._axes[0], self._dado_config.Settings, "DESVIO")
		self._axes[0].set_ylabel(self.tituloy,picker=5,gid="y_label_graph:Desvio",**font)
		for label in self._axes[1].get_yticklabels():
                        label.set_picker(True)
                        label.set_gid("ticks_y:Desvio")
		



##		h=18
##		for (dip_lat,axes,tec,sigla) in ziper:
##			for AX,tec_d in zip(axes,tec):
##				with warnings.catch_warnings():
##					warnings.simplefilter("ignore", category=RuntimeWarning)
##					if np.isnan(np.nanmax(tec)) or np.nanmax(tec) < 0:
##						AX.text(.5,.5, self._dado_config.idioma(94))#,ha="center", va="center" )
##					else:
##						#for x in range(len(tec_d)):
##							
##						AX.plot(self.temp,[np.nan if x <0 else x for x in tec_d], color='r',label='Tec',linewidth=2.5)
##				AX.set_facecolor("lightgrey")
##				AX.set_gid("DESVIO")
##				try:AX.set_xlim(self._dado_config.Settings["DESVIO"]["fValueMin_Axes_X_temp"],self._dado_config.Settings["DESVIO"]["fValueMax_Axes_X_temp"])
##				except KeyError:AX.set_xlim(0,24)
##				try:AX.set_ylim(self._dado_config.Settings["DESVIO"]["fValueMin_Axes_Y_temp"],self._dado_config.Settings["DESVIO"]["fValueMax_Axes_Y_temp"])
##				except KeyError:AX.set_ylim(0,round(max_G+(max_G *(.05*len(sigla)))))
##				AX.minorticks_on()
##				AX.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
##				AX.tick_params(axis='both',direction='inout', which='major',top=True,right=True)
##				AX.tick_params(axis='both',direction='inout', which='minor' ,top=True,right=True)
##				AX.tick_params(axis='x', which='minor', width=self._dado_config.Settings["DESVIO"]["fWidthTickMinor_X"],size=self._dado_config.Settings["DESVIO"]["fHeightTickMinor_X"])
##				AX.tick_params(axis='x', which='major', width=self._dado_config.Settings["DESVIO"]["fWidthTickMajor_X"],size=self._dado_config.Settings["DESVIO"]["fHeightTickMajor_X"],labelsize=self._dado_config.Settings["DESVIO"]["fSizeLabelsTick_X"])
##				AX.tick_params(axis='y', which='minor', width=self._dado_config.Settings["DESVIO"]["fWidthTickMinor_Y"],size=self._dado_config.Settings["DESVIO"]["fHeightTickMinor_Y"])
##				AX.tick_params(axis='y', which='major', width=self._dado_config.Settings["DESVIO"]["fWidthTickMajor_Y"],size=self._dado_config.Settings["DESVIO"]["fHeightTickMajor_Y"],labelsize=self._dado_config.Settings["DESVIO"]["fSizeLabelsTick_Y"])
##			else:
##				at = AnchoredText("%s(dip latitude %s)"%(sigla,dip_lat), prop=font_anchored, frameon=False, loc='upper left', borderpad=0)
##				axes[0].add_artist(at)
##				axes[0].set_ylabel(self.tituloy,picker=5,gid="y_label_graph:Desvio",**font)
##				try:
##					if self._dado_config.Settings["DESVIO"]["fValue_Passo_Ticks_Y_temp"]:axes[0].yaxis.set_major_locator(ticker.MultipleLocator(self._dado_config.Settings["DESVIO"]["fValue_Passo_Ticks_Y_temp"]))
##					elif self._dado_config.Settings["DESVIO"]["iValue_Num_Ticks_Y_temp"]:axes[0].yaxis.set_major_locator(ticker.LinearLocator(self._dado_config.Settings["DESVIO"]["iValue_Num_Ticks_Y_temp"]))
##					else:axes[0].yaxis.set_major_locator(ticker.LinearLocator(4))
##				except KeyError:axes[0].yaxis.set_major_locator(ticker.LinearLocator(4))
##				axes[0].yaxis.get_major_ticks()[-1].set_visible(False)
##				for label in axes[0].get_yticklabels():
##					label.set_picker(True)
##					label.set_gid("ticks_y:Desvio")
##		else:
##			for AX,d_ax_X in zip(self.axes[0],self.datas_axes_X):AX.set_title(d_ax_X[self._formato_data],picker=5, gid="Data_Y:Desvio",**font)
##			else:self.axes[0][0].yaxis.get_major_ticks()[-1].set_visible(True)
##			for AX in self.axes[-1]:
##				try:
##					if self._dado_config.Settings["DESVIO"]["fValue_Passo_Ticks_X_temp"]:AX.xaxis.set_major_locator(ticker.MultipleLocator(self._dado_config.Settings["DESVIO"]["fValue_Passo_Ticks_X_temp"]))
##					elif self._dado_config.Settings["DESVIO"]["iValue_Num_Ticks_X_temp"]:AX.xaxis.set_major_locator(ticker.LinearLocator(self._dado_config.Settings["DESVIO"]["iValue_Num_Ticks_X_temp"]))
##					else:AX.xaxis.set_major_locator(ticker.LinearLocator(7))
##				except KeyError:AX.xaxis.set_major_locator(ticker.LinearLocator(7))
##				labels_AX_X = AX.get_xticklabels()
##				plt.setp(labels_AX_X[-1], visible=False)
##				for label in AX.get_xticklabels():
##					label.set_picker(True)
##					label.set_gid("ticks_x:Desvio")
##			else:
##				try:
##					if self._dado_config.Settings["DESVIO"]["fValue_Passo_Ticks_X_temp"]:AX.xaxis.set_major_locator(ticker.MultipleLocator(self._dado_config.Settings["DESVIO"]["fValue_Passo_Ticks_X_temp"]))
##					elif self._dado_config.Settings["DESVIO"]["iValue_Num_Ticks_X_temp"]:AX.xaxis.set_major_locator(ticker.LinearLocator(self._dado_config.Settings["DESVIO"]["iValue_Num_Ticks_X_temp"]))
##					else:AX.xaxis.set_major_locator(ticker.LinearLocator(7))
##				except KeyError:
##					AX.xaxis.set_major_locator(ticker.LinearLocator(7))
##				plt.setp(labels_AX_X, visible=True)
##
		self._matplotlib_figure.set_facecolor('lightgrey')

	def _get_Matplotlib_grafico_att(self):
		return self._matplotlib_figure,self._axes,self.titulo,self.C_tec,self.delta_days,self.temp,self.datas_axes_X

