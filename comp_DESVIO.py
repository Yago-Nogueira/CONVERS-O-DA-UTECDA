from datetime import timedelta, datetime, date
from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import Qt
import numpy as np
from util import Utilitarios, DadoIdioma
from shared_utils import (
	apply_tick_params, configure_axis_locator, ensure_date_order,
	build_std_filepath,
)
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import warnings
from matplotlib.offsetbox import AnchoredText
from matplotlib.ticker import FormatStrFormatter


class COMP_DESVIO(QDialog):
	def __init__(self, matplotlib_figure, diretorio_dados, siglas_estacao, dias_calmos, data_inicial, data_final, formato_data, dado_config):
		self._matplotlib_figure = matplotlib_figure
		self._diretorio_dados = diretorio_dados
		self._siglas_estacao = siglas_estacao
		self._dias_calmos = dias_calmos
		self._data_inicial = data_inicial
		self._data_final = data_final
		self._formato_data = formato_data	
		self._dado_config = dado_config

	def _set_Matplotlib_grafico(self):
		plt.tick_params(axis='both',direction='inout', which='major',top=True)
		plt.tick_params(axis='both',direction='inout', which='minor' ,top=True,right=True)

		self._matplotlib_figure.clf()
		self.temp = np.array([x for x in np.arange(0,24,(1/60))])					
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
		self.delta_days = self.delta.days+1
		len_est = len(self._siglas_estacao)

		
		
		
		self.axes = self._matplotlib_figure.subplots(len_est,int(self.delta_days),sharex='col', sharey='row')#, squeeze=True)
		# self._matplotlib_figure.subplots_adjust(wspace=0,hspace=0)
		self._matplotlib_figure.suptitle(self._dado_config.idioma(122), picker=5,gid="Sup_titulo:Desvio",**font)
		self.C_dip_lat = []
		self.C_desvio = []
		self.C_sigla = []
		self.C_media = []
		self.C_tec = []
		for est_s in self._siglas_estacao:
			self.matrizstd = []
			for dia_select in self._dias_calmos:
				caminho_arquivo = build_std_filepath(self._diretorio_dados, est_s[0], dia_select)
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
			for contd in range(self.delta_days):
				datafile = (self._data_inicial + timedelta(days=contd))
				self.datas_axes_X.append([datafile.date(),datafile.day])
				caminho_arquivo_p = build_std_filepath(self._diretorio_dados, est_s[0], datafile)
				self.matriz_tec_p.append(self.uti.Leitura_trip(caminho_arquivo_p))
			self.matriz_tec_p = np.array(self.matriz_tec_p).reshape(self.delta_days,1440)
			self.C_sigla.append(est_s[0])
			self.C_dip_lat.append(est_s[3])
			self.C_media.append(self.media_calmo)					
			self.C_desvio.append(self.desvio_calmo)
			self.C_tec.append(self.matriz_tec_p)

		max_G = np.nanmax(self.C_tec)
		if np.isnan(max_G):max_G=1

		if len_est == 1 and self.delta_days > 1:
			self.axes = [self.axes]
		elif len_est == 1 and self.delta_days == 1:
			self.axes = [[self.axes]]
		elif len_est > 1 and self.delta_days == 1:
			self.axes = [[axes_c] for axes_c in self.axes]
		self.legendas = []
		#self.axes=np.flip(self.axes)
		ziper=zip(self.C_dip_lat,self.axes,self.C_media,self.C_desvio,self.C_tec,self.C_sigla)
		#print(self.axes)
		#ziper=np.flip(ziper)
		#print(ziper)
		#for (dip_lat,axes,media,desvio,tec,sigla) in zip(self.C_dip_lat,self.axes,self.C_media,self.C_desvio,self.C_tec,self.C_sigla):
		for (dip_lat,axes,media,desvio,tec,sigla) in ziper:
			for AX,tec_d in zip(axes,tec):
				with warnings.catch_warnings():
					warnings.simplefilter("ignore", category=RuntimeWarning)
					if np.isnan(np.nanmax(tec)) or np.nanmax(tec) < 0:
						AX.text(.5,.5, self._dado_config.idioma(94))#,ha="center", va="center" )
					else:		
						if self._dias_calmos:
							y1 = (media+desvio)
							y2 = (media-desvio)
							AX.fill_between(self.temp,y1,y2,color = 'gray',label=self._dado_config.idioma(125))
							AX.plot(self.temp,media, color ='black',label=self._dado_config.idioma(138),linewidth=3.0)
						AX.plot(self.temp,[np.nan if x <0 else x for x in tec_d], color='r',label='Tec',linewidth=2.5)
				AX.set_facecolor("lightgrey")
				AX.set_gid("DESVIO")
				try:AX.set_xlim(self._dado_config.Settings["DESVIO"]["fValueMin_Axes_X_temp"],self._dado_config.Settings["DESVIO"]["fValueMax_Axes_X_temp"])
				except KeyError:AX.set_xlim(0,24)
				try:AX.set_ylim(self._dado_config.Settings["DESVIO"]["fValueMin_Axes_Y_temp"],self._dado_config.Settings["DESVIO"]["fValueMax_Axes_Y_temp"])
				except KeyError:AX.set_ylim(0,round(max_G+(max_G *(.05*len(sigla)))))
				AX.minorticks_on()
				AX.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
				AX.tick_params(axis='both',direction='inout', which='major',top=True,right=True)#, width=float(self.largtick.get()),size=float(self.alttick.get()),labelsize=float(self.sizetick.get()))
				AX.tick_params(axis='both',direction='inout', which='minor' ,top=True,right=True)#,width=float(self.largtickMinor.get()) ,size=float(self.alttickMinor.get()))
				apply_tick_params(AX, self._dado_config.Settings, "DESVIO")
			else:
				at = AnchoredText("%s(dip latitude %s)"%(sigla,dip_lat), prop=font_anchored, frameon=False, loc='upper left', borderpad=0)
				axes[0].add_artist(at)
				axes[0].set_ylabel(self.tituloy,picker=5,gid="y_label_graph:Desvio",**font)
				configure_axis_locator(axes[0].yaxis, self._dado_config.Settings, "DESVIO", "Y", ticker.LinearLocator(4))
				axes[0].yaxis.get_major_ticks()[-1].set_visible(False)
				for label in axes[0].get_yticklabels():
					label.set_picker(True)
					label.set_gid("ticks_y:Desvio")
		else:
			for AX,d_ax_X in zip(self.axes[0],self.datas_axes_X):AX.set_title(d_ax_X[self._formato_data],picker=5, gid="Data_Y:Desvio",**font)
			else:self.axes[0][0].yaxis.get_major_ticks()[-1].set_visible(True)
			for AX in self.axes[-1]:
				configure_axis_locator(AX.xaxis, self._dado_config.Settings, "DESVIO", "X", ticker.LinearLocator(7))
				labels_AX_X = AX.get_xticklabels()
				plt.setp(labels_AX_X[-1], visible=False)
				for label in AX.get_xticklabels():
					label.set_picker(True)
					label.set_gid("ticks_x:Desvio")
			else:
				configure_axis_locator(AX.xaxis, self._dado_config.Settings, "DESVIO", "X", ticker.LinearLocator(7))
				plt.setp(labels_AX_X, visible=True)

		self._matplotlib_figure.set_facecolor('lightgrey')

	def _get_Matplotlib_grafico_att(self):
		return self._matplotlib_figure,self.axes,self.titulo,self.C_tec,self.C_desvio,self.C_media,self.delta_days,self.temp,self.datas_axes_X

