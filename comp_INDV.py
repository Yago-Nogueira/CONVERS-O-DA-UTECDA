from datetime import timedelta, datetime, date
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QFileDialog, QMessageBox
from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QFont
import matplotlib.ticker as ticker
from qtfontchooser import askfont
import matplotlib.pyplot as plt
from util import Utilitarios 
import numpy as np
import logging
import warnings

class COMP_INDV(QDialog):	
	def __init__(self, matplotlib_figure, sigla_estacao, data_inicial, data_final, diretorio_dados, formato_data, dado_config):
		self._matplotlib_figure = matplotlib_figure
		self._sigla_estacao = sigla_estacao
		self._data_inicial = data_inicial
		self._data_final = data_final
		self._diretorio_dados = diretorio_dados
		self._formato_data = formato_data
		self._dado_config = dado_config
		self._vtec_max = self._dado_config.Settings["INDIVIDUAL"]["fValueMax_B_VTEC"]
		self._vtec_min = self._dado_config.Settings["INDIVIDUAL"]["fValueMin_B_VTEC"]

		# self._sFamily = self._dado_config.Settings["INDIVIDUAL"]["sFamily"]
		# self._sWeight = self._dado_config.Settings["INDIVIDUAL"]["sWeight"]
		# self._fSize = self._dado_config.Settings["INDIVIDUAL"]["fSize"]
		# self._sTitle_X = self._dado_config.Settings["INDIVIDUAL"]["sTitle_X"]
		# self._sTitle_Y = self._dado_config.Settings["INDIVIDUAL"]["sTitle_Y"]
		# self._sTitle_B = self._dado_config.Settings["INDIVIDUAL"]["sTitle_B"]
		# self._fSizeLabelsTick_X = self._dado_config.Settings["INDIVIDUAL"]["fSizeLabelsTick_X"]
		# self._fWidthTickMajor_X = self._dado_config.Settings["INDIVIDUAL"]["fWidthTickMajor_X"]
		# self._fHeightTickMajor_X = self._dado_config.Settings["INDIVIDUAL"]["fHeightTickMajor_X"]
		# self._fWidthTickMinor_X = self._dado_config.Settings["INDIVIDUAL"]["fWidthTickMinor_X"]
		# self._fHeightTickMinor_X = self._dado_config.Settings["INDIVIDUAL"]["fHeightTickMinor_X"]
		# self._fSizeLabelsTick_Y = self._dado_config.Settings["INDIVIDUAL"]["fSizeLabelsTick_Y"]
		# self._fWidthTickMajor_Y = self._dado_config.Settings["INDIVIDUAL"]["fWidthTickMajor_Y"]
		# self._fHeightTickMajor_Y = self._dado_config.Settings["INDIVIDUAL"]["fHeightTickMajor_Y"]
		# self._fWidthTickMinor_Y = self._dado_config.Settings["INDIVIDUAL"]["fWidthTickMinor_Y"]
		# self._fHeightTickMinor_Y = self._dado_config.Settings["INDIVIDUAL"]["fHeightTickMinor_Y"]

		# self._titulo_graph_indv = None
		# self._titulo_axe_y_indv = None
		# self._titulo_axe_x_indv = None
		# self._tick_bar_indv = None
		# self._passo_tick_x_indv = None
		# self._n_rotulo_x_indv = None
		# self._min_x_indv = None
		# self._max_x_indv = None
		# self._passo_tick_y_indv = None
		# self._n_rotulo_y_indv = None
		# self._min_y_indv = None
		# self._max_y_indv = None
		# self.titulo_bar_indv = "VTEC"
		# self.rfont_titulo_graph_indv = self.rfont_titulo_axe_y_indv = self.rfont_titulo_axe_x_indv = self.rfont_titulo_bar_indv = {'family': '@MS Gothic', 'size': 28, 'weight': 'bold'}
		
		# plt.rc('font', weight='bold')
		# plt.rc('axes',linewidth=2)
	# def __init__(self,fi = None,sigla=None,dataI=None,dataF=None,self._diretorio_dados=None,DateFormat=None,vm=None):

	def _set_Matplotlib_grafico(self):
		self._tec_dias = []
		self._matriz_dias = []
		self._cbar = None
		_matrizstd = []
		nfile=''
		uti = Utilitarios()
		font = self._dado_config.get_font_Settings("INDIVIDUAL")
		self._matplotlib_figure.set_facecolor('white')	
		if self._data_inicial > self._data_final:backdata = self._data_inicial;self._data_inicial = self._data_final;self._data_final = backdata
		delta = self._data_final - self._data_inicial
		# self._titulo =(("%s-%s-%.2i") % (self._sigla_estacao.lower(),self._data_inicial.year,self._data_inicial.month)) 
		self._titulo =(("%s") % (self._sigla_estacao.upper())) 
		delta_days = delta.days + 1
		if delta_days == 1:delta_days+=1
		for contd in range(delta_days):
			datafile = (self._data_inicial + timedelta(days=contd))
			self._tec_dias.append(datafile.day)
			dia_ano = datafile.timetuple().tm_yday
			self._matriz_dias.append([('%s/%s')%(datafile.day,datafile.month),('%s')%(datafile.day)])
			nfile = ("/%s%.3i-%i-%.2i-%.2i.Std") % (self._sigla_estacao.lower(),dia_ano,datafile.year,datafile.month,datafile.day)
			destino = self._diretorio_dados + nfile
			_matrizstd.append(uti.Leitura_trip(destino))
		
		_matrizstd = np.array(_matrizstd).transpose()	
		# '''
		# 	arrumando matriz...fix
		# '''
		self._tec_fix = []
		for x in [a for s in _matrizstd for a in s]:
			self._tec_fix.append(x)
		self._tec_fix = np.array(self._tec_fix)
		self._matplotlib_figure.clf()
		self._axes = self._matplotlib_figure.subplots()
		
		with warnings.catch_warnings():
			warnings.simplefilter("ignore", category=RuntimeWarning)
			if  np.isnan(np.nanmean(np.array([np.nanmean(tecx) for tecx in self._tec_fix]))):
				self._matplotlib_figure.text(.5,.5, self._dado_config.idioma(94),ha="center", va="center" )
			else:
				passo = self._vtec_max/15
				level = np.arange(self._vtec_min,(self._vtec_max+1),passo)
				self._axes.set_gid("INDIVIDUAL")
				self._axes.set_title(self._titulo,picker=5,gid="titulo_graph:INDIVIDUAL",**font)
				self._axes.set_ylabel(self._dado_config.Settings["INDIVIDUAL"]["sTitle_Y"], picker=5, gid="y_label_graph:INDIVIDUAL",**font)
				self._axes.set_xlabel(self._dado_config.Settings["INDIVIDUAL"]["sTitle_X"], picker=5, gid="x_label_graph:INDIVIDUAL",**font)
				self._axes.set_ylim(0,1440)

				try:
					if self._dado_config.Settings["INDIVIDUAL"]["fValue_Passo_Ticks_Y_temp"]:self._axes.yaxis.set_major_locator(ticker.MultipleLocator(self._dado_config.Settings["INDIVIDUAL"]["fValue_Passo_Ticks_Y_temp"]*60))
					elif self._dado_config.Settings["INDIVIDUAL"]["iValue_Num_Ticks_Y_temp"]:self._axes.yaxis.set_major_locator(ticker.LinearLocator(self._dado_config.Settings["INDIVIDUAL"]["iValue_Num_Ticks_Y_temp"]))
					else:self._axes.yaxis.set_major_locator(ticker.LinearLocator(24))
				except KeyError:self._axes.yaxis.set_major_locator(ticker.LinearLocator(24))
				try:
					if self._dado_config.Settings["INDIVIDUAL"]["fValue_Passo_Ticks_X_temp"]:self._axes.xaxis.set_major_locator(ticker.MultipleLocator(self._dado_config.Settings["INDIVIDUAL"]["fValue_Passo_Ticks_X_temp"]))
					elif self._dado_config.Settings["INDIVIDUAL"]["iValue_Num_Ticks_X_temp"]:self._axes.xaxis.set_major_locator(ticker.LinearLocator(self._dado_config.Settings["INDIVIDUAL"]["iValue_Num_Ticks_X_temp"]))
					else:self._axes.xaxis.set_major_locator(ticker.MultipleLocator(2))
				except KeyError:self._axes.xaxis.set_major_locator(ticker.MultipleLocator(2))
				
				try:self._axes.set_xlim(self._dado_config.Settings["INDIVIDUAL"]["fValueMin_Axes_X_temp"],self._dado_config.Settings["INDIVIDUAL"]["fValueMax_Axes_X_temp"])
				except KeyError:
					logging.debug("INDIVIDUAL: X-axis temp limits not configured, using defaults")
				try:self._axes.set_ylim(self._dado_config.Settings["INDIVIDUAL"]["fValueMin_Axes_Y_temp"]*60,self._dado_config.Settings["INDIVIDUAL"]["fValueMax_Axes_Y_temp"]*60)
				except KeyError:
					logging.debug("INDIVIDUAL: Y-axis temp limits not configured, using defaults")


				self._axes.yaxis.set_major_formatter(ticker.FuncFormatter(self.major_formatterhora))
				self._axes.xaxis.set_major_formatter(ticker.FuncFormatter(self.major_formatterdia))
				self._axes.minorticks_on()
				self.passo_ctick = 10
				self.cmap = plt.cm.get_cmap("jet").copy()
				self.cmap.set_under("white")
				self.cmap.set_over("darkred")
				self.plot_current=self._axes.contourf(self._tec_fix,levels=level,cmap=self.cmap,vmin = self._vtec_min, vmax=self._vtec_max,extend="both")
				self._cbar = self._matplotlib_figure.colorbar(self.plot_current,ax = self._axes,ticks = np.arange(self._vtec_min,self._vtec_max+1,self.passo_ctick),)
				for label in self._axes.get_xticklabels():
					label.set_picker(True)
					label.set_gid("ticks_x:INDIVIDUAL")
				for label in self._axes.get_yticklabels():
					label.set_picker(True)
					label.set_gid("ticks_y:INDIVIDUAL")
				self._cbar.ax.set_picker(5)
				self._cbar.ax.set_gid("tick_bar_graph:INDIVIDUAL")
				self._cbar.ax.set_title(self._dado_config.Settings["INDIVIDUAL"]["sTitle_B"],**font,picker=5,pad=30,gid="label_bar_graph:INDIVIDUAL")
				self._cbar.ax.tick_params(axis='y', which='major',
				width=self._dado_config.Settings["INDIVIDUAL"]["fWidthTickMajor_Y"],
				size=self._dado_config.Settings["INDIVIDUAL"]["fHeightTickMajor_Y"],
				labelsize=self._dado_config.Settings["INDIVIDUAL"]["fSizeLabelsTick_Y"])
		
		self._axes.tick_params(axis='x', which='minor', width=self._dado_config.Settings["INDIVIDUAL"]["fWidthTickMinor_X"],size=self._dado_config.Settings["INDIVIDUAL"]["fHeightTickMinor_X"])#,labelsize=tam_x))
		self._axes.tick_params(axis='x', which='major', width=self._dado_config.Settings["INDIVIDUAL"]["fWidthTickMajor_X"],size=self._dado_config.Settings["INDIVIDUAL"]["fHeightTickMajor_X"],labelsize=self._dado_config.Settings["INDIVIDUAL"]["fSizeLabelsTick_X"])
		self._axes.tick_params(axis='y', which='minor', width=self._dado_config.Settings["INDIVIDUAL"]["fWidthTickMinor_Y"],size=self._dado_config.Settings["INDIVIDUAL"]["fHeightTickMinor_Y"])#,labelsize=tam_y))
		self._axes.tick_params(axis='y', which='major', width=self._dado_config.Settings["INDIVIDUAL"]["fWidthTickMajor_Y"],size=self._dado_config.Settings["INDIVIDUAL"]["fHeightTickMajor_Y"],labelsize=self._dado_config.Settings["INDIVIDUAL"]["fSizeLabelsTick_Y"])
		
		# self._axes.tick_params(axis='x', which='minor', width=Larg_minor_X_INDIVIDUAL,size=Alt_minor_X_INDIVIDUAL)#,labelsize=tam_x))
		# self._axes.tick_params(axis='x', which='major', width=Larg_major_X_INDIVIDUAL,size=Alt_major_X_INDIVIDUAL,labelsize=Tam_label_X_INDIVIDUAL)
		# self._axes.tick_params(axis='y', which='minor', width=Larg_minor_Y_INDIVIDUAL,size=Alt_minor_Y_INDIVIDUAL)#,labelsize=tam_y))
		# self._axes.tick_params(axis='y', which='major', width=Larg_major_Y_INDIVIDUAL,size=Alt_major_Y_INDIVIDUAL,labelsize=Tam_label_Y_INDIVIDUAL)


	def _get_Matplotlib_grafico_att(self):
		# return self._cbar,self._titulo,self._tec_dias,self._tec_fix,self._matriz_dias#,_matrizstd
		return self._matplotlib_figure,self._axes,self._cbar,self._titulo,self._tec_dias,self._tec_fix,self._matriz_dias
		# self.plot_current
		#,_matrizstd

	def major_formatterhora(self,x, pos):
		try:
			return "%.f" % (x/60)
		except IndexError:
			pass
	def major_formatterdia(self,x, pos):
		try:
			return (self._matriz_dias[int(x)][self._formato_data.get()])
		except IndexError:
			pass
			
		# return (("%s") % (self._matriz_dias[(int(x))]))

	










if __name__ == "__main__":
	
	root = Tk()

	teste = Frame(root,bg='green')
	teste.pack(fill=BOTH,expand=True)
	im = plt.subplots()


	COMP_INDV(self.im,'ALAR')

	# ttk.Button(root, text='DateEntry', command=example2).pack(padx=10, pady=10)

	root.mainloop()
