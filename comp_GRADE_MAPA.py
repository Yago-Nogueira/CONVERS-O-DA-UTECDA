
from matplotlib.colors import LinearSegmentedColormap
from util import Utilitarios
from shared_utils import (
	create_jet_colormap, interpolate_grid, dict_list_append,
	organize_cmn_data, collect_plot_data_vtec,
	compute_colorbar_levels, cleanup_matplotlib,
)
import os, copy, queue
import matplotlib.pyplot as plt
from cartopy.crs import PlateCarree
from matplotlib import cm,colors
import cartopy.feature as cfeature
from threading import Thread
from pandas import date_range

from scipy.interpolate import griddata
import cartopy.crs as ccrs

from datetime import date, datetime, timedelta

import numpy as np
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox, QFileDialog



class COMP_GRADE_MAPA(QDialog):	
	def __init__(self,
		filedir,
		data_inicio,
		data_fim ,
		colunas,
		linhas,
		siglas,
		extend_LAT_LONG,
		var_barra_progess,
		var_barra_progess_label,
		dado_config,
		Coordenadas_equador_Magnetico_X,
		Coordenadas_equador_Magnetico_Y,
		stop_thread_PAINEL_MAPA
	):

		# self._matplotlib_figure = matplotlib_figure


		self._filedir = filedir
		self._data_inicio = data_inicio
		self._data_fim = data_fim
		self._colunas = colunas
		self._linhas = linhas
		self._siglas = siglas
		self._extend_LAT_LONG = extend_LAT_LONG
		self._var_barra_progess_label = var_barra_progess_label
		self._var_barra_progess = var_barra_progess
		self._dado_config = dado_config
		self._elevacao = self._dado_config.Settings["PAINEL MAPA"]["fElevation_Filter"]
		self._Coordenadas_equador_Magnetico_X = Coordenadas_equador_Magnetico_X
		self._Coordenadas_equador_Magnetico_Y = Coordenadas_equador_Magnetico_Y
		
		self._stop_thread_PAINEL_MAPA = stop_thread_PAINEL_MAPA
		self.uti = Utilitarios()

		self.numcols, self.numrows = 100,100
		# self.cmap = copy.copy(cm.get_cmap("jet"))
		# self.cmap.set_under("white")
		# self.cmap.set_over("darkred")
		self._PERIODO_PAINEL_MAPA = date_range(start=self._data_inicio, end=self._data_fim, periods=(self._colunas * self._linhas))
		self._PERIODO_PAINEL_MAPA_dias = date_range(start = self._data_inicio.date(), end = self._data_fim.date(), freq='D')






	
	
	
	
	def _start_thread_siglas_VTEC(self, siglas, dia_ano, MAPA_dia_date, max = 10):
		total_task = len(siglas)
		q = queue.Queue(maxsize=0)
		num_theads = min(max, total_task)
		for i in range(total_task):
			q.put((i,siglas[i]))
		for i in range(num_theads):
			Thread(target=self._thread_siglas_VTEC, args=(q,dia_ano, MAPA_dia_date,), daemon = True).start()
		q.join()

	def _thread_siglas_VTEC(self, q, dia_ano, MAPA_dia_date):
		while not q.empty():
			work = q.get()
			if self._stop_thread_PAINEL_MAPA.get():
				q.task_done()
				continue
			es = work[1]
			caminho = (("%s\\%s%.3i-%s-%.2i-%.2i.Cmn") % (self._filedir, es.lower(), dia_ano, MAPA_dia_date.year, MAPA_dia_date.month, MAPA_dia_date.day))
			prns_cmn,dado_cmn = self.uti.Leitura_CMN_DICT(destino = caminho, ele = self._elevacao)
			if prns_cmn and dado_cmn:
				_es = es.lower()
				self.nome_est[MAPA_dia_date].append(_es)
				self.list_prn[MAPA_dia_date].append(prns_cmn)
				organize_cmn_data(dado_cmn, prns_cmn, self.dados_organizados, MAPA_dia_date, _es)
			self._var_barra_progess.set(self._var_barra_progess.get() + self.coef_loop_leitura)
			q.task_done()
		return

	def _start_thread_organizar_dados_VTEC(self, zip_list, MAPA_dia_date, max = 10):
		total_task = len(zip_list)
		q = queue.Queue(maxsize=0)
		num_theads = min(max, total_task)
		
		for i in range(total_task):
			q.put((i,zip_list[i]))
		for i in range(num_theads):
			Thread(target=self._thread_organizar_dados_VTEC, args=(q,MAPA_dia_date,), daemon = True).start()
		q.join()

	def _thread_organizar_dados_VTEC(self,q, MAPA_dia_date):
		while not q.empty():
			work = q.get()
			if self._stop_thread_PAINEL_MAPA.get():
				q.task_done()
				continue
			_est,_prn =  work[1]
			collect_plot_data_vtec(self.dados_organizados, self.dados_organizados_plot, MAPA_dia_date, _est, _prn)
			self._var_barra_progess.set(self._var_barra_progess.get() + self.coef_loop_processamento)
			q.task_done()
		return
			
	def _set_Matplotlib_grafico_grade_VTEC(self):
		_titulo_bar = self._dado_config.Settings["PAINEL MAPA"]["sTitle_B_VTEC"]
		font = self._dado_config.get_font_Settings("PAINEL MAPA")

		""" 
			Realizando a leitura de todos os dados encontrados (*.CMN) encontrados --> pos 177
			Realizando o processamento do dado --> pos 178
			Iniciando plot das figuras --> pos 179
			Trabalho finalizado --> pos 180
			# Processando todos os dados (*.CMN) encontrados --> pos 177
		"""



		self._var_barra_progess_label.set(self._dado_config.idioma(177))
		self._var_barra_progess.set(0)
		

		self.dados_organizados = {}
		self.list_prn = {}
		self.nome_est = {}
		self.coef_loop_leitura = ((100)/(3*len(self._siglas)*len(self._PERIODO_PAINEL_MAPA_dias)))

		for MAPA_dia in self._PERIODO_PAINEL_MAPA_dias:
			MAPA_dia_date = MAPA_dia.date()
			dia_ano = MAPA_dia.timetuple().tm_yday
			self.dados_organizados[MAPA_dia_date] = {}
			self.list_prn[MAPA_dia_date] = []
			self.nome_est[MAPA_dia_date] = []
			self._start_thread_siglas_VTEC(self._siglas, dia_ano, MAPA_dia_date,20)	

		
		self._var_barra_progess.set(33.33)
		self._var_barra_progess_label.set(self._dado_config.idioma(178))

		CMAP_GRAFICO_MAPA_VTEC = create_jet_colormap()

		levels, ticks, _vm_min, _vm_max = compute_colorbar_levels(self._dado_config.Settings, "PAINEL MAPA", "VTEC")


		

		self.pasta = {}
		self.dados_organizados_plot = {}
		self.coef_loop_processamento = ((100)/(3*len(self._siglas)*len(self._PERIODO_PAINEL_MAPA_dias)))
		for MAPA_dia in self._PERIODO_PAINEL_MAPA_dias:
			MAPA_dia_date = MAPA_dia.date()
			if self.nome_est[MAPA_dia_date]:		
				self.dados_organizados_plot[MAPA_dia_date] = {}
				self._start_thread_organizar_dados_VTEC(list(zip(self.nome_est[MAPA_dia_date],self.list_prn[MAPA_dia_date])),MAPA_dia_date,20)
				try:
					self.pasta[MAPA_dia_date] = ("(VMAX %.2f_%.2f) PAINEL_Contorno_VTEC_%s"%(_vm_min,_vm_max,MAPA_dia_date.year))
					os.makedirs(self._filedir+"\\"+self.pasta[MAPA_dia_date])
				except FileExistsError:
					pass


		#'____________________________________________________________________________________________________________________________'
		self._var_barra_progess.set(66.66)
		self._var_barra_progess_label.set(self._dado_config.idioma(179))
		#'____________________________________________________________________________________________________________________________'
		self.coef_loop_plot = ((100)/(3*len(self._PERIODO_PAINEL_MAPA)))

		# self.numcols
		# self.numrows

		# self._matplotlib_figure.clf()
		# self._axes = self._matplotlib_figure.subplots(ncols=self._colunas,nrows=self._linhas, subplot_kw={'projection': PlateCarree()})
		self.fig, self.axes = plt.subplots(ncols=self._colunas,nrows=self._linhas, subplot_kw={'projection': PlateCarree()}, squeeze=True)
		
		self.fig.subplots_adjust(
			top=self._dado_config.Settings["PAINEL MAPA"]["fTop"],
			bottom=self._dado_config.Settings["PAINEL MAPA"]["fBottom"],
			left=self._dado_config.Settings["PAINEL MAPA"]["fLeft"],
			right=self._dado_config.Settings["PAINEL MAPA"]["fRight"],
			hspace=self._dado_config.Settings["PAINEL MAPA"]["fHspace"],
			wspace=self._dado_config.Settings["PAINEL MAPA"]["fWspace"]
		)
		cbar_ax = self.fig.add_axes([0.85, 0.15, 0.0205, 0.7])

		for AXE,data in zip(self.axes.flat,self._PERIODO_PAINEL_MAPA):
			try:
				# hora_HMS = str(data.time())
				hora_decimal = (data.hour) + (data.minute/60) + (data.second/3600)
				f_hora = ("%.6f"%float(hora_decimal))[:-1]
				# AXE.set_title(("%s\n%s"%(str(data.date()),hora_HMS)),**font)
				AXE.set_extent(self._extend_LAT_LONG, crs=PlateCarree())
				AXE.add_feature(cfeature.BORDERS)
				AXE.add_feature(cfeature.COASTLINE)
				transform = PlateCarree()._as_mpl_transform(AXE)
				AXE.annotate(str(data.time())[:8], xy=(self._extend_LAT_LONG[0], self._extend_LAT_LONG[2]), xycoords=transform, color='red', ha='left', va='bottom', fontsize=15)
				#AXE.annotate(str(data.time())[:8], xy=(self._extend_LAT_LONG[0], self._extend_LAT_LONG[2]), xycoords=transform, color='red', ha='left', va='bottom', fontsize=15)
				AXE.plot(self._Coordenadas_equador_Magnetico_X,self._Coordenadas_equador_Magnetico_Y,'k')
				#AXE.xaxis.grid(True,zorder=0)
				#AXE.yaxis.grid(True,zorder=0)
				#Inserir lat/lon
				gl = AXE.gridlines(crs=ccrs.PlateCarree(),draw_labels=True)				
				gl.xlabels_top=False
				gl.ylabels_right=False
				AXE.grid('on')
				#Fim 
				x, y, z = np.array(self.dados_organizados_plot[data.date()][f_hora+'.lon']), np.array(self.dados_organizados_plot[data.date()][f_hora+'.lat']), np.array(self.dados_organizados_plot[data.date()][f_hora+'.vtec']) 
				xi, yi, GD1 = interpolate_grid(x, y, z, self.numcols, self.numrows)
				COLOR_SET = AXE.contourf(
					xi,yi,GD1,
					cmap = CMAP_GRAFICO_MAPA_VTEC, 
					extend='both',
					levels = levels,
					transform=PlateCarree()
				)
				self._var_barra_progess.set(self._var_barra_progess.get() + self.coef_loop_plot)

			except (Exception) as e: 
				print(e)
				pass

		cbar_mapa = self.fig.colorbar(COLOR_SET,cax=cbar_ax,extend='both',ticks=ticks)
		cbar_mapa.ax.set_title(_titulo_bar,pad = 30,**font)
		
		# hora_inicio = str(self._data_inicio.time()).replace(":","-")
		# hora_fim = str(self._data_fim.time()).replace(":","-")
		data_inicio = str(self._PERIODO_PAINEL_MAPA[0]).replace(":","-").replace(" ","_")
		data_fim = str(self._PERIODO_PAINEL_MAPA[-1]).replace(":","-").replace(" ","_")
		camff = (("%s\\%s\\PAINEL_VTEC_(%s_%s).png")%(self._filedir,self.pasta[data.date()],data_inicio,data_fim))
		# PAINEL_VTEC_DIAS_(2021-11-03 20-00-00_2021-11-04 00-00-00)_HORARIO_(20-00-00_00-00-00)

		# figManager = plt.get_current_fig_manager()
		# figManager.window.state('zoomed')
		# FIG.set_facecolor('lightgrey')
		# self.fig.savefig(camff, bbox_inches='tight')
		# self.fig.savefig(camff, dpi=self.fig.dpi)
		# plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, wspace = 0)
		# self.fig.savefig(camff, bbox_inches = 'tight', pad_inches = 0)
		# self.fig.set_size_inches(20.0, 10.0)
		# self.fig.set_size_inches(19.20, 9.77)
		# self.fig.savefig(camff, bbox_inches = 'tight', pad_inches = 0)
		self.fig.set_size_inches(self._dado_config.Settings["PAINEL MAPA"]["fSize_inches_fig_width"], self._dado_config.Settings["PAINEL MAPA"]["fSize_inches_fig_height"])
		self.fig.savefig(camff, dpi=self.fig.dpi)
		cleanup_matplotlib()
		self._var_barra_progess_label.set("Figura - "+camff+" gerada")
		self._var_barra_progess.set(self._var_barra_progess.get() + self.coef_loop_plot)
		self._var_barra_progess.set(100)
		self._var_barra_progess_label.set(self._dado_config.idioma(180))
		del self.dados_organizados
		del self.list_prn
		del self.nome_est
		del self.pasta
		del self.dados_organizados_plot
		del self.fig
		del self.axes
		return True#



	def _start_thread_siglas_ROT(self, siglas, dia_ano, MAPA_dia_date, max = 10):
		q = queue.Queue(maxsize=0)
		num_theads = min(max, len(siglas))
		for i in range(len(siglas)):
			q.put((i,siglas[i]))
		for i in range(num_theads):
			Thread(target=self._thread_siglas_ROT, args=(q,dia_ano, MAPA_dia_date,), daemon = True).start()
		q.join()
		
	def _thread_siglas_ROT(self, q, dia_ano, MAPA_dia_date):
		while not q.empty():
			work = q.get()
			if self._stop_thread_PAINEL_MAPA.get():
				q.task_done()
				continue
			es = work[1]
			caminho = (("%s\\%s%.3i-%s-%.2i-%.2i.Cmn") % (self._filedir, es.lower(), dia_ano,MAPA_dia_date.year, MAPA_dia_date.month, MAPA_dia_date.day))
			prns_cmn,dado_cmn = self.uti.Leitura_CMN_DICT(destino = caminho, ele = self._elevacao)
			if prns_cmn and dado_cmn:
				_es = es.lower()
				self.nome_est[MAPA_dia_date].append(_es)
				self.list_prn[MAPA_dia_date].append(prns_cmn)
				organize_cmn_data(dado_cmn, prns_cmn, self.dados_organizados, MAPA_dia_date, _es)
			self._var_barra_progess.set(self._var_barra_progess.get() + self.coef_loop_leitura)
			q.task_done()
		return 

	def _start_thread_organizar_dados_ROT(self, zip_list, MAPA_dia_date, max = 10):
		total_task = len(zip_list)
		q = queue.Queue(maxsize=0)
		num_theads = min(max, total_task)
		for i in range(total_task):
			q.put((i,zip_list[i]))
		for i in range(num_theads):
			Thread(target=self._thread_organizar_dados_ROT, args=(q,MAPA_dia_date,), daemon = True).start()
		q.join()

	def _thread_organizar_dados_ROT(self,q, MAPA_dia_date):
		while not q.empty():
			work = q.get()
			if self._stop_thread_PAINEL_MAPA.get():
				q.task_done()
				continue
			_est,_prn = work[1]
			for prn in _prn:
				str_prn = str(prn)
				self.dados_organizados[MAPA_dia_date][_est][str_prn] = self.uti.get_ROT(self.dados_organizados[MAPA_dia_date][_est][str_prn], delta_time_rot = self._dado_config.Settings["PAINEL MAPA"]["fValueDelta_ROT"], intervalo_LEITURA_CMN = 30)
				for hora in self.dados_organizados[MAPA_dia_date][_est][str_prn].keys():  
					f_hora = hora
					if not np.isnan(self.dados_organizados[MAPA_dia_date][_est][str_prn][f_hora]['rot']):
						entry = self.dados_organizados[MAPA_dia_date][_est][str_prn][f_hora]
						dict_list_append(self.dados_organizados_plot[MAPA_dia_date], f_hora+".lat", entry['lat'])
						dict_list_append(self.dados_organizados_plot[MAPA_dia_date], f_hora+".lon", entry['lon'])
						dict_list_append(self.dados_organizados_plot[MAPA_dia_date], f_hora+".rot", abs(entry['rot']))
			self._var_barra_progess.set(self._var_barra_progess.get() + self.coef_loop_processamento)
			q.task_done()
		return 

	def _set_Matplotlib_grafico_grade_ROT(self):
		_titulo_bar = self._dado_config.Settings["PAINEL MAPA"]["sTitle_B_ROT"]
		font = self._dado_config.get_font_Settings("PAINEL MAPA")
		""" 
			Realizando a leitura de todos os dados encontrados (*.CMN) encontrados --> pos 177
			Realizando o processamento do dado --> pos 178
			Iniciando plot das figuras --> pos 179
			Trabalho finalizado --> pos 180
		"""
#'____________________________________________________________________________________________________________________________'
		self._var_barra_progess_label.set(self._dado_config.idioma(177))
		self._var_barra_progess.set(0)
#'____________________________________________________________________________________________________________________________'
		self.fig,self.axes = plt.subplots()
		self.fig.set_facecolor('white')
		self.dados_organizados = {}
		self.list_prn = {}
		self.nome_est = {}
		self.coef_loop_leitura = ((100)/(3*len(self._siglas)*len(self._PERIODO_PAINEL_MAPA_dias)))
		
		for MAPA_dia in self._PERIODO_PAINEL_MAPA_dias:
			MAPA_dia_date = MAPA_dia.date()
			dia_ano = MAPA_dia.timetuple().tm_yday
			self.dados_organizados[MAPA_dia_date] = {}
			self.list_prn[MAPA_dia_date] = []
			self.nome_est[MAPA_dia_date] = []
			self._start_thread_siglas_ROT(self._siglas, dia_ano, MAPA_dia_date,20)
			# for es in self._siglas:
		# print("--------------")
#'____________________________________________________________________________________________________________________________'
		self._var_barra_progess.set(33.33)
		self._var_barra_progess_label.set(self._dado_config.idioma(178))
#'____________________________________________________________________________________________________________________________'
		CMAP_GRAFICO_MAPA_ROT = LinearSegmentedColormap.from_list("my_list", ['darkred', 'red', 'yellow', 'limegreen', "blue", 'blue', 'limegreen', 'yellow', 'red', 'darkred'], N=100)
		# CMAP_GRAFICO_MAPA_ROT.set_under("darkred")
		# CMAP_GRAFICO_MAPA_ROT.set_over("darkred")
		
		levels, ticks, _vm_min, _vm_max = compute_colorbar_levels(self._dado_config.Settings, "PAINEL MAPA", "ROT")




		self.pasta = {}
		self.dados_organizados_plot = {}
		self.coef_loop_processamento = ((100)/(3*len(self._siglas)*len(self._PERIODO_PAINEL_MAPA_dias)))
		for MAPA_dia in self._PERIODO_PAINEL_MAPA_dias:
			MAPA_dia_date = MAPA_dia.date()
			if self.nome_est[MAPA_dia_date]:
				self.dados_organizados_plot[MAPA_dia_date] = {}
				# for _est,_prn in zip(self.nome_est[MAPA_dia_date],self.list_prn[MAPA_dia_date]):
				self._start_thread_organizar_dados_ROT(list(zip(self.nome_est[MAPA_dia_date],self.list_prn[MAPA_dia_date])),MAPA_dia_date,20)
				try:
					# self.pasta[MAPA_dia_date] = ("(VMAX %.2f_%.2f) Contorno_ROT_%s-%.2i-%.2i"%(_vm_min,_vm_max,MAPA_dia_date.year,MAPA_dia_date.month,MAPA_dia_date.day))
					self.pasta[MAPA_dia_date] = ("(VMAX %.2f_%.2f) PAINEL_Contorno_ROT_%s"%(_vm_min,_vm_max,MAPA_dia_date.year))
					os.makedirs(self._filedir+"\\"+self.pasta[MAPA_dia_date])
				except FileExistsError:
					pass


#'____________________________________________________________________________________________________________________________'
		self._var_barra_progess.set(66.66)
		self._var_barra_progess_label.set(self._dado_config.idioma(179))
		#'____________________________________________________________________________________________________________________________'
		self.coef_loop_plot = ((100)/(3*len(self._PERIODO_PAINEL_MAPA)))


		self.fig, self.axes = plt.subplots(ncols=self._colunas,nrows=self._linhas, subplot_kw={'projection': PlateCarree()}, squeeze=True)
		self.fig.subplots_adjust(
			top=self._dado_config.Settings["PAINEL MAPA"]["fTop"],
			bottom=self._dado_config.Settings["PAINEL MAPA"]["fBottom"],
			left=self._dado_config.Settings["PAINEL MAPA"]["fLeft"],
			right=self._dado_config.Settings["PAINEL MAPA"]["fRight"],
			hspace=self._dado_config.Settings["PAINEL MAPA"]["fHspace"],
			wspace=self._dado_config.Settings["PAINEL MAPA"]["fWspace"]
		)
		cbar_ax = self.fig.add_axes([0.85, 0.15, 0.0205, 0.7])
		for AXE,data in zip(self.axes.flat,self._PERIODO_PAINEL_MAPA):
			try:
				# hora_HMS = str(data.time())
				hora_decimal = (data.hour) + (data.minute/60) + (data.second/3600)
				f_hora = ("%.6f"%float(hora_decimal))[:-1]
				AXE.set_extent(self._extend_LAT_LONG, crs=PlateCarree())
				AXE.add_feature(cfeature.BORDERS)
				AXE.add_feature(cfeature.COASTLINE)
				transform = PlateCarree()._as_mpl_transform(AXE)
				#AXE.annotate(str(data.time())[:8], xy=(self._extend_LAT_LONG[0], self._extend_LAT_LONG[2]), xycoords=transform, color='red', ha='left', va='bottom')
				AXE.annotate(str(data.time())[:8], xy=(self._extend_LAT_LONG[0], self._extend_LAT_LONG[2]), xycoords=transform, color='red', ha='left', va='bottom', fontsize=15)
				AXE.plot(self._Coordenadas_equador_Magnetico_X,self._Coordenadas_equador_Magnetico_Y,'k')
				#Inserir lat/lon
				gl = AXE.gridlines(crs=ccrs.PlateCarree(),draw_labels=True)				
				gl.xlabels_top=False
				gl.ylabels_right=False
				AXE.grid('on')
				#Fim 
				x, y, z = np.array(self.dados_organizados_plot[data.date()][f_hora+'.lon']), np.array(self.dados_organizados_plot[data.date()][f_hora+'.lat']), np.array(self.dados_organizados_plot[data.date()][f_hora+'.rot']) 
				xi, yi, GD1 = interpolate_grid(x, y, z, self.numcols, self.numrows)
				COLOR_SET = AXE.contourf(
					xi,yi,GD1,
					cmap = CMAP_GRAFICO_MAPA_ROT, 
					extend='both',
					levels = levels,
					transform=PlateCarree()
				)
				self._var_barra_progess.set(self._var_barra_progess.get() + self.coef_loop_plot)

			except (Exception) as e: 
				print(e)
				pass
		#AXE.tick_params(axis='both',direction='inout',wich='minor',length=6,width=2,bottom=True,top=True)
		cbar_mapa = self.fig.colorbar(
			COLOR_SET,
			cax=cbar_ax,
			extend='both',
			ticks=ticks
		)
		cbar_mapa.ax.set_title(_titulo_bar, pad = 30, **font)
		
		# hora_inicio = str(self._data_inicio.time()).replace(":","-")
		# hora_fim = str(self._data_fim.time()).replace(":","-")
		data_inicio = str(self._PERIODO_PAINEL_MAPA[0]).replace(":","-").replace(" ","_")
		data_fim = str(self._PERIODO_PAINEL_MAPA[-1]).replace(":","-").replace(" ","_")
		camff = (("%s\\%s\\PAINEL_ROT_(%s_%s).png")%(self._filedir,self.pasta[data.date()],data_inicio,data_fim))
		self.fig.set_size_inches(self._dado_config.Settings["PAINEL MAPA"]["fSize_inches_fig_width"], self._dado_config.Settings["PAINEL MAPA"]["fSize_inches_fig_height"])
		self.fig.savefig(camff, dpi=self.fig.dpi)
		cleanup_matplotlib()
		self._var_barra_progess_label.set("Figura - "+camff+" gerada")
		self._var_barra_progess.set(self._var_barra_progess.get() + self.coef_loop_plot)
		self._var_barra_progess.set(100)
		self._var_barra_progess_label.set(self._dado_config.idioma(180))
		del self.dados_organizados
		del self.list_prn
		del self.nome_est
		del self.pasta
		del self.dados_organizados_plot
		del self.fig
		del self.axes
		return True#




	def _start_thread_siglas_ROTI(self, siglas, dia_ano, MAPA_dia_date, max = 10):
		q = queue.Queue(maxsize=0)
		num_theads = min(max, len(siglas))
		for i in range(len(siglas)):
			q.put((i,siglas[i]))
		for i in range(num_theads):
			Thread(target=self._thread_siglas_ROTI, args=(q,dia_ano, MAPA_dia_date,), daemon = True).start()
		q.join()
		
	def _thread_siglas_ROTI(self, q, dia_ano, MAPA_dia_date):
		while not q.empty():
			work = q.get()
			if self._stop_thread_PAINEL_MAPA.get():
				q.task_done()
				continue
			es = work[1]
			caminho = (("%s\\%s%.3i-%s-%.2i-%.2i.Cmn") % (self._filedir, es.lower(), dia_ano,MAPA_dia_date.year, MAPA_dia_date.month, MAPA_dia_date.day))
			prns_cmn,dado_cmn = self.uti.Leitura_CMN_DICT(destino = caminho, ele = self._elevacao)
			if prns_cmn and dado_cmn:
				_es = es.lower()
				self.nome_est[MAPA_dia_date].append(_es)
				self.list_prn[MAPA_dia_date].append(prns_cmn)
				organize_cmn_data(dado_cmn, prns_cmn, self.dados_organizados, MAPA_dia_date, _es)
			self._var_barra_progess.set(self._var_barra_progess.get() + self.coef_loop_leitura)
			q.task_done()
		return 


	def _start_thread_organizar_dados_ROTI(self, zip_list, MAPA_dia_date, max = 10):
		total_task = len(zip_list)
		q = queue.Queue(maxsize=0)
		num_theads = min(max, total_task)
		for i in range(total_task):
			q.put((i,zip_list[i]))
		for i in range(num_theads):
			Thread(target=self._thread_organizar_dados_ROTI, args=(q,MAPA_dia_date,), daemon = True).start()
		q.join()
	def _thread_organizar_dados_ROTI(self,q, MAPA_dia_date):
		while not q.empty():
			work = q.get()
			if self._stop_thread_PAINEL_MAPA.get():
				q.task_done()
				continue
			_est,_prn = work[1]
			for prn in _prn:
				str_prn = str(prn)
				self.dados_organizados[MAPA_dia_date][_est][str_prn] = self.uti.get_ROT(self.dados_organizados[MAPA_dia_date][_est][str_prn], delta_time_rot = self._dado_config.Settings["PAINEL MAPA"]["fValueDelta_ROT"], intervalo_LEITURA_CMN = 30)
				self.dados_organizados[MAPA_dia_date][_est][str_prn] = self.uti.get_ROTI(self.dados_organizados[MAPA_dia_date][_est][str_prn], delta_time_roti = self._dado_config.Settings["PAINEL MAPA"]["fValueDelta_ROTI"], intervalo_LEITURA_CMN = 30)
				for hora in self.dados_organizados[MAPA_dia_date][_est][str_prn].keys():  
					f_hora = hora
					if not np.isnan(self.dados_organizados[MAPA_dia_date][_est][str_prn][f_hora]['roti']):
						entry = self.dados_organizados[MAPA_dia_date][_est][str_prn][f_hora]
						dict_list_append(self.dados_organizados_plot[MAPA_dia_date], f_hora+".lat", entry['lat'])
						dict_list_append(self.dados_organizados_plot[MAPA_dia_date], f_hora+".lon", entry['lon'])
						dict_list_append(self.dados_organizados_plot[MAPA_dia_date], f_hora+".roti", entry['roti'])
			self._var_barra_progess.set(self._var_barra_progess.get() + self.coef_loop_processamento)
			q.task_done()
		return 

	def _set_Matplotlib_grafico_grade_ROTI(self):
		_titulo_bar = self._dado_config.Settings["PAINEL MAPA"]["sTitle_B_ROTI"]
		font = self._dado_config.get_font_Settings("PAINEL MAPA")
		""" 
			Realizando a leitura de todos os dados encontrados (*.CMN) encontrados --> pos 177
			Realizando o processamento do dado --> pos 178
			Iniciando plot das figuras --> pos 179
			Trabalho finalizado --> pos 180
		"""
#'____________________________________________________________________________________________________________________________'
		self._var_barra_progess_label.set(self._dado_config.idioma(177))
		self._var_barra_progess.set(0)
#'____________________________________________________________________________________________________________________________'
		self.dados_organizados = {}
		self.list_prn = {}
		self.nome_est = {}
		self.coef_loop_leitura = ((100)/(3*len(self._siglas)*len(self._PERIODO_PAINEL_MAPA_dias)))
		
		for MAPA_dia in self._PERIODO_PAINEL_MAPA_dias:
			MAPA_dia_date = MAPA_dia.date()
			dia_ano = MAPA_dia.timetuple().tm_yday
			self.dados_organizados[MAPA_dia_date] = {}
			self.list_prn[MAPA_dia_date] = []
			self.nome_est[MAPA_dia_date] = []
			self._start_thread_siglas_ROTI(self._siglas, dia_ano, MAPA_dia_date,20)
			# for es in self._siglas:
		print("--------------")
#'____________________________________________________________________________________________________________________________'
		self._var_barra_progess.set(33.33)
		self._var_barra_progess_label.set(self._dado_config.idioma(178))
#'____________________________________________________________________________________________________________________________'
		
		# CMAP_GRAFICO_MAPA_ROTI = LinearSegmentedColormap.from_list("my_list", ['white','blue','aqua','yellow','red','darkred'], N=100)

		CMAP_GRAFICO_MAPA_ROTI = create_jet_colormap()

		levels, ticks, _vm_min, _vm_max = compute_colorbar_levels(self._dado_config.Settings, "PAINEL MAPA", "ROTI")



		self.pasta = {}
		self.dados_organizados_plot = {}
		self.coef_loop_processamento = ((100)/(3*len(self._siglas)*len(self._PERIODO_PAINEL_MAPA_dias)))
		for MAPA_dia in self._PERIODO_PAINEL_MAPA_dias:
			MAPA_dia_date = MAPA_dia.date()
			if self.nome_est[MAPA_dia_date]:
				self.dados_organizados_plot[MAPA_dia_date] = {}
				# for _est,_prn in zip(self.nome_est[MAPA_dia_date],self.list_prn[MAPA_dia_date]):
				self._start_thread_organizar_dados_ROTI(list(zip(self.nome_est[MAPA_dia_date],self.list_prn[MAPA_dia_date])),MAPA_dia_date,20)
				try:
					self.pasta[MAPA_dia_date] = ("(VMAX %.2f_%.2f) PAINEL_Contorno_ROTI_%s"%(_vm_min,_vm_max,MAPA_dia_date.year))
					os.makedirs(self._filedir+"\\"+self.pasta[MAPA_dia_date])
				except FileExistsError:
					pass

	
		#'____________________________________________________________________________________________________________________________'
		self._var_barra_progess.set(66.66)
		self._var_barra_progess_label.set(self._dado_config.idioma(179))
		#'____________________________________________________________________________________________________________________________'
		self.coef_loop_plot = ((100)/(3*len(self._PERIODO_PAINEL_MAPA)))
		self.fig, self.axes = plt.subplots(ncols=self._colunas,nrows=self._linhas, subplot_kw={'projection': PlateCarree()}, squeeze=True)
		self.fig.subplots_adjust(
			top=self._dado_config.Settings["PAINEL MAPA"]["fTop"],
			bottom=self._dado_config.Settings["PAINEL MAPA"]["fBottom"],
			left=self._dado_config.Settings["PAINEL MAPA"]["fLeft"],
			right=self._dado_config.Settings["PAINEL MAPA"]["fRight"],
			hspace=self._dado_config.Settings["PAINEL MAPA"]["fHspace"],
			wspace=self._dado_config.Settings["PAINEL MAPA"]["fWspace"]
		)
		cbar_ax = self.fig.add_axes([0.85, 0.15, 0.0205, 0.7])
		for AXE,data in zip(self.axes.flat,self._PERIODO_PAINEL_MAPA):
			try:
				# hora_HMS = str(data.time())
				hora_decimal = (data.hour) + (data.minute/60) + (data.second/3600)
				f_hora = ("%.6f"%float(hora_decimal))[:-1]
				AXE.set_extent(self._extend_LAT_LONG, crs=PlateCarree())
				AXE.add_feature(cfeature.BORDERS)
				AXE.add_feature(cfeature.COASTLINE)
				transform = PlateCarree()._as_mpl_transform(AXE)
				#AXE.annotate(str(data.time())[:8], xy=(self._extend_LAT_LONG[0], self._extend_LAT_LONG[2]), xycoords=transform, color='white', ha='left', va='bottom')
				AXE.annotate(str(data.time())[:8], xy=(self._extend_LAT_LONG[0], self._extend_LAT_LONG[2]), xycoords=transform, color='red', ha='left', va='bottom', fontsize=15)
				AXE.plot(self._Coordenadas_equador_Magnetico_X,self._Coordenadas_equador_Magnetico_Y,'k')
				#Inserir lat/lon
				gl = AXE.gridlines(crs=ccrs.PlateCarree(),draw_labels=True)				
				gl.xlabels_top=False
				gl.ylabels_right=False
				AXE.grid('on')
				#Fim 
				x, y, z = np.array(self.dados_organizados_plot[data.date()][f_hora+'.lon']), np.array(self.dados_organizados_plot[data.date()][f_hora+'.lat']), np.array(self.dados_organizados_plot[data.date()][f_hora+'.roti']) 
				xi, yi, GD1 = interpolate_grid(x, y, z, self.numcols, self.numrows)
				COLOR_SET = AXE.contourf(
					xi,yi,GD1,
					cmap = CMAP_GRAFICO_MAPA_ROTI, 
					extend='both',
					levels = levels,
					transform=PlateCarree()
				)
				self._var_barra_progess.set(self._var_barra_progess.get() + self.coef_loop_plot)
			except (Exception) as e: 
				print(e)
				pass
		cbar_mapa = self.fig.colorbar(COLOR_SET, cax=cbar_ax, extend='both', ticks=ticks)
		cbar_mapa.ax.set_title(_titulo_bar, pad = 30, **font)

		# hora_inicio = str(self._data_inicio.time()).replace(":","-")
		# hora_fim = str(self._data_fim.time()).replace(":","-")
		data_inicio = str(self._PERIODO_PAINEL_MAPA[0]).replace(":","-").replace(" ","_")
		data_fim = str(self._PERIODO_PAINEL_MAPA[-1]).replace(":","-").replace(" ","_")
		camff = (("%s\\%s\\PAINEL_ROTI_(%s_%s).png")%(self._filedir,self.pasta[data.date()],data_inicio,data_fim))
		self.fig.set_size_inches(self._dado_config.Settings["PAINEL MAPA"]["fSize_inches_fig_width"], self._dado_config.Settings["PAINEL MAPA"]["fSize_inches_fig_height"])
		self.fig.savefig(camff, dpi=self.fig.dpi)
		cleanup_matplotlib()

		self._var_barra_progess_label.set("Figura - "+camff+" gerada")
		self._var_barra_progess.set(self._var_barra_progess.get() + self.coef_loop_plot)
		self._var_barra_progess.set(100)
		self._var_barra_progess_label.set(self._dado_config.idioma(180))
		del self.dados_organizados
		del self.list_prn
		del self.nome_est
		del self.pasta
		del self.dados_organizados_plot
		del self.fig
		del self.axes
		return True#
