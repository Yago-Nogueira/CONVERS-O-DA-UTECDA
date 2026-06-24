from util import Utilitarios
from datetime import datetime
# from threading import Thread
from pyqt_utils import Toplevel
import pyqt_utils as ui
import numpy as np
from scipy.interpolate import griddata

import os,copy#,math,_thread
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import matplotlib as mpl
import cartopy.feature as cfeature
from pyqt_utils import messagebox
import pandas as pd

class COMP_MAPA(ui.Toplevel):	
	def __init__(self, filedir, data_inicio, data_fim , h_interval, siglas, extend_LAT_LONG, var_barra_progess, var_barra_progess_label, dado_config,Coordenadas_equador_Magnetico_X,Coordenadas_equador_Magnetico_Y):
		self._filedir = filedir
		self._data_inicio = data_inicio
		self._data_fim = data_fim
		self._h_interval = h_interval
		self._siglas = siglas
		self._extend_LAT_LONG = extend_LAT_LONG
		self._var_barra_progess_label = var_barra_progess_label
		self._var_barra_progess = var_barra_progess
		self._dado_config = dado_config

		self._elevacao = self._dado_config.Settings["MAPA"]["fElevation_Filter"]

		self._Coordenadas_equador_Magnetico_X = Coordenadas_equador_Magnetico_X
		self._Coordenadas_equador_Magnetico_Y = Coordenadas_equador_Magnetico_Y
		self.uti = Utilitarios()
		

		self._PERIODO_MAPA = pd.date_range(start = self._data_inicio, end = self._data_fim, freq=('%sT'%self._h_interval))
		self._PERIODO_MAPA_dias = pd.date_range(start = self._data_inicio.date(), end = self._data_fim.date(), freq='D')

		
		# self._var_barra_progess_label.set(self._dado_config.idioma(177))
		# Processando todos os dados (*.CMN) encontrados --> pos 177

		# self._var_barra_progess_label.set(self._dado_config.idioma(178) +str(self._data.year))
		# Gerando equador magnético para o ano de  --> pos 178

		# self._var_barra_progess_label.set(self._dado_config.idioma(179))
		# Iniciando plot das figuras --> pos 179

		# self._var_barra_progess_label.set("Figura - "+camff+" gerada")

		# self._var_barra_progess_label.set(self._dado_config.idioma(180))
		# Trabalho finalizado --> pos 180


	def _set_Matplotlib_grafico_ROTI(self):
		_titulo_bar = self._dado_config.Settings["MAPA"]["sTitle_B_ROTI"]
		font = {'family' : self._dado_config.Settings["MAPA"]["sFamily"] , 'weight' : self._dado_config.Settings["MAPA"]["sWeight"],'size' : self._dado_config.Settings["MAPA"]["fSize"]}
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
		dados_organizados = {}
		list_prn = {}
		nome_est = {}
		coef_loop_leitura = ((100)/(3*len(self._siglas)*len(self._PERIODO_MAPA_dias)))
		for MAPA_dia in self._PERIODO_MAPA_dias:
			MAPA_dia_date = MAPA_dia.date()
			dia_ano = MAPA_dia.timetuple().tm_yday
			dados_organizados[MAPA_dia_date] = {}
			list_prn[MAPA_dia_date] = []
			nome_est[MAPA_dia_date] = []
			for es in self._siglas:
				es = es[0]
				caminho = (("%s\\%s%.3i-%s-%.2i-%.2i.Cmn") % (self._filedir,es.lower(),dia_ano,MAPA_dia_date.year,MAPA_dia_date.month,MAPA_dia_date.day))
				prns_cmn,dado_cmn = self.uti.Leitura_CMN_DICT(destino = caminho, ele = self._elevacao)
				if prns_cmn and dado_cmn:
					_es = es.lower()
					nome_est[MAPA_dia_date].append(_es)
					list_prn[MAPA_dia_date].append(prns_cmn)
					dados_organizados[MAPA_dia_date][_es] = {}
					for prn in prns_cmn:
						str_prn = str(prn)
						dados_organizados[MAPA_dia_date][_es][str_prn] = {}
						for hora in dado_cmn[str_prn + ".time"]:
							dados_organizados[MAPA_dia_date][_es][str_prn][hora] = {}
							ind = dado_cmn[str_prn + ".time"].index(hora)
							dados_organizados[MAPA_dia_date][_es][str_prn][hora]['lon'] = dado_cmn[str_prn + ".lon"][ind]
							dados_organizados[MAPA_dia_date][_es][str_prn][hora]['lat'] = dado_cmn[str_prn + ".lat"][ind]
							dados_organizados[MAPA_dia_date][_es][str_prn][hora]['vtec'] = dado_cmn[str_prn + ".vtec"][ind]
				self._var_barra_progess.set(self._var_barra_progess.get() + coef_loop_leitura)
#'____________________________________________________________________________________________________________________________'
		self._var_barra_progess_label.set(self._dado_config.idioma(178))
#'____________________________________________________________________________________________________________________________'
		pasta = {}
		dados_organizados_plot = {}
		coef_loop_processamento = ((100)/(3*len(self._siglas)*len(self._PERIODO_MAPA_dias)))
		for MAPA_dia in self._PERIODO_MAPA_dias:
			MAPA_dia_date = MAPA_dia.date()
			if nome_est[MAPA_dia_date]:
				dados_organizados_plot[MAPA_dia_date] = {}
				for _est,_prn in zip(nome_est[MAPA_dia_date],list_prn[MAPA_dia_date]):
					for prn in _prn:
						str_prn = str(prn)
						dados_organizados[MAPA_dia_date][_est][str_prn] = self.uti.get_ROT(dados_organizados[MAPA_dia_date][_est][str_prn], delta_time_rot = self._dado_config.Settings["MAPA"]["fValueDelta_ROT"], intervalo_LEITURA_CMN = 30)
						dados_organizados[MAPA_dia_date][_est][str_prn] = self.uti.get_ROTI(dados_organizados[MAPA_dia_date][_est][str_prn], delta_time_roti = self._dado_config.Settings["MAPA"]["fValueDelta_ROTI"], intervalo_LEITURA_CMN = 30)
						for hora in dados_organizados[MAPA_dia_date][_est][str_prn].keys():  
							f_hora = hora
							if not np.isnan(dados_organizados[MAPA_dia_date][_est][str_prn][f_hora]['roti']):
								try:
									dados_organizados_plot[MAPA_dia_date][f_hora+".lat"].append(dados_organizados[MAPA_dia_date][_est][str_prn][f_hora]['lat'])
								except KeyError:
									dados_organizados_plot[MAPA_dia_date][f_hora+".lat"] = []
									dados_organizados_plot[MAPA_dia_date][f_hora+".lat"].append(dados_organizados[MAPA_dia_date][_est][str_prn][f_hora]['lat'])
								try:
									dados_organizados_plot[MAPA_dia_date][f_hora+".lon"].append(dados_organizados[MAPA_dia_date][_est][str_prn][f_hora]['lon'])
								except KeyError:
									dados_organizados_plot[MAPA_dia_date][f_hora+".lon"] = []
									dados_organizados_plot[MAPA_dia_date][f_hora+".lon"].append(dados_organizados[MAPA_dia_date][_est][str_prn][f_hora]['lon'])
								try:
									dados_organizados_plot[MAPA_dia_date][f_hora+".roti"].append(dados_organizados[MAPA_dia_date][_est][str_prn][f_hora]['roti'])
								except KeyError:
									dados_organizados_plot[MAPA_dia_date][f_hora+".roti"] = []
									dados_organizados_plot[MAPA_dia_date][f_hora+".roti"].append(dados_organizados[MAPA_dia_date][_est][str_prn][f_hora]['roti'])
					self._var_barra_progess.set(self._var_barra_progess.get() + coef_loop_processamento)				
				try:
					pasta[MAPA_dia_date] = ("Contorno_ROTI_%s-%.2i-%.2i"%(MAPA_dia_date.year,MAPA_dia_date.month,MAPA_dia_date.day))
					os.makedirs(self._filedir+"\\"+pasta[MAPA_dia_date])
				except FileExistsError:
					pass

		numcols, numrows = 100,100
		_vm = self._dado_config.Settings["MAPA"]["fValueMax_B_ROTI"]
		# level = np.arange(0,(_vm+1),1)
		cmap = copy.copy(mpl.cm.get_cmap("jet"))
		cmap.set_under("white")
		cmap.set_over("darkred")
		_ticks_cbar = 10
		_ticks_divisao = 4
		passo = _vm/(_ticks_cbar*_ticks_divisao)
		bounds = np.arange(.1,_vm+passo,passo)
		ticks = np.arange(0-passo,_vm+2*passo,passo)
		ticks_colorbar =  np.arange(0,_vm+passo,0.1)
		norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
		nmap = mpl.cm.ScalarMappable(norm=norm, cmap=cmap)
		#'____________________________________________________________________________________________________________________________'
		self._var_barra_progess_label.set(self._dado_config.idioma(179))
		#'____________________________________________________________________________________________________________________________'
		coef_loop_plot = ((100)/(3*len(self._PERIODO_MAPA)))
		for PERIODO_DATA_MAPA in self._PERIODO_MAPA:
			try:
				self.fig.clf()
				axes = self.fig.add_subplot(111, projection = ccrs.PlateCarree())
				# hora+=0.00001
				# horas = int(hora)
				# minutos = (hora*60) % 60
				# segundos = (hora*3600) % 60
				# hora_HMS =  ("%02d:%02d:%02d" % (horas, minutos, segundos))
				hora_HMS = str(PERIODO_DATA_MAPA.time())
				# hora-=0.00001
				hora_decimal = (PERIODO_DATA_MAPA.hour) + (PERIODO_DATA_MAPA.minute/60) + (PERIODO_DATA_MAPA.second/3600)
				f_hora = ("%.6f"%float(hora_decimal))[:-1]
				axes.set_title(("%s\n%s"%(str(PERIODO_DATA_MAPA.date()),hora_HMS)),**font)
				# axes.set_title(("%s\n%s"%(str(self._data)[:-9],hora_HMS)),**font)
				axes.set_extent(self._extend_LAT_LONG)
				axes.add_feature(cfeature.BORDERS)
				axes.add_feature(cfeature.COASTLINE)
				x, y, z = np.array(dados_organizados_plot[PERIODO_DATA_MAPA.date()][f_hora+'.lon']), np.array(dados_organizados_plot[PERIODO_DATA_MAPA.date()][f_hora+'.lat']), np.array(dados_organizados_plot[PERIODO_DATA_MAPA.date()][f_hora+'.roti']) 
				# scx,scy = x, y
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
				axes.plot(self._Coordenadas_equador_Magnetico_X,self._Coordenadas_equador_Magnetico_Y,'k')
				# cbar_mapa = self.fig.colorbar(axes.contourf(xi,yi,GD1, cmap = cmap,levels = level, vmin = 0, vmax = _vm ,extend="both",transform=ccrs.PlateCarree()),ticks = np.arange(0,_vm+1,4))
				axes.contourf(
					xi,yi,GD1,
					cmap = cmap, 
					extend='both',
					levels = bounds,
					transform=ccrs.PlateCarree()
				)
				cbar_mapa = self.fig.colorbar(
					nmap,
					boundaries=ticks,
					extend='both',
					spacing='proportional',
					ticks=ticks_colorbar
				)
				# xs = [_sigla[2]for _sigla in _siglas]
				# ys = [_sigla[1]for _sigla in _siglas]
				# axes.scatter(xs, ys, marker='.',c='blue')#, s=10)
				# axes.scatter(scx, scy, marker='.',c='red')#, s=10)
				cbar_mapa.ax.set_title(_titulo_bar,**font)
				camff = (("%s\\%s\\%s.png")%(self._filedir,pasta[PERIODO_DATA_MAPA.date()],hora_HMS.replace(':',"-")))
				# fig.set_size_inches(20.0, 10.0)
				self.fig.savefig(camff,dpi=self.fig.dpi)
				self._var_barra_progess_label.set("Figura - "+camff+" gerada")
			except (Exception) as e: 
				print(e)
				pass
			self._var_barra_progess.set(self._var_barra_progess.get() + coef_loop_plot)
		# self._var_barra_progess_label.set(self._dado_config.idioma(94))
		self._var_barra_progess.set(100)
		self._var_barra_progess_label.set(self._dado_config.idioma(180))
		plt.close()
		return None#

	def _set_Matplotlib_grafico_VTEC(self):
		import time
		start_time = time.time()
		
		_titulo_bar = self._dado_config.Settings["MAPA"]["sTitle_B_VTEC"]
		font = {'family' : self._dado_config.Settings["MAPA"]["sFamily"] , 'weight' : self._dado_config.Settings["MAPA"]["sWeight"],'size' : self._dado_config.Settings["MAPA"]["fSize"]}
		""" 
			Realizando a leitura de todos os dados encontrados (*.CMN) encontrados --> pos 177
			Realizando o processamento do dado --> pos 178
			Iniciando plot das figuras --> pos 179
			Trabalho finalizado --> pos 180
			# Processando todos os dados (*.CMN) encontrados --> pos 177
		"""
#'____________________________________________________________________________________________________________________________'
		self._var_barra_progess_label.set(self._dado_config.idioma(177))
		self._var_barra_progess.set(0)
#'____________________________________________________________________________________________________________________________'
		self.fig,self.axes = plt.subplots()
		self.fig.set_facecolor('white')
		dados_organizados = {}
		list_prn = {}
		nome_est = {}
		coef_loop_leitura = ((100)/(3*len(self._siglas)*len(self._PERIODO_MAPA_dias)))
		for MAPA_dia in self._PERIODO_MAPA_dias:
			MAPA_dia_date = MAPA_dia.date()
			dia_ano = MAPA_dia.timetuple().tm_yday
			dados_organizados[MAPA_dia_date] = {}
			list_prn[MAPA_dia_date] = []
			nome_est[MAPA_dia_date] = []
			for es in self._siglas:
				es = es[0]
				caminho = (("%s\\%s%.3i-%s-%.2i-%.2i.Cmn") % (self._filedir,es.lower(),dia_ano,MAPA_dia_date.year,MAPA_dia_date.month,MAPA_dia_date.day))
				prns_cmn,dado_cmn = self.uti.Leitura_CMN_DICT(destino = caminho, ele = self._elevacao)
				if prns_cmn and dado_cmn:
					_es = es.lower()
					nome_est[MAPA_dia_date].append(_es)
					list_prn[MAPA_dia_date].append(prns_cmn)
					dados_organizados[MAPA_dia_date][_es] = {}
					for prn in prns_cmn:
						str_prn = str(prn)
						dados_organizados[MAPA_dia_date][_es][str_prn] = {}
						for hora in dado_cmn[str_prn + ".time"]:
							dados_organizados[MAPA_dia_date][_es][str_prn][hora] = {}
							ind = dado_cmn[str_prn + ".time"].index(hora)
							dados_organizados[MAPA_dia_date][_es][str_prn][hora]['lon'] = dado_cmn[str_prn + ".lon"][ind]
							dados_organizados[MAPA_dia_date][_es][str_prn][hora]['lat'] = dado_cmn[str_prn + ".lat"][ind]
							dados_organizados[MAPA_dia_date][_es][str_prn][hora]['vtec'] = dado_cmn[str_prn + ".vtec"][ind]
				self._var_barra_progess.set(self._var_barra_progess.get() + coef_loop_leitura)
#'____________________________________________________________________________________________________________________________'
		self._var_barra_progess_label.set(self._dado_config.idioma(178))
#'____________________________________________________________________________________________________________________________'
		pasta = {}
		dados_organizados_plot = {}
		coef_loop_processamento = ((100)/(3*len(self._siglas)*len(self._PERIODO_MAPA_dias)))
		for MAPA_dia in self._PERIODO_MAPA_dias:
			MAPA_dia_date = MAPA_dia.date()
			if nome_est[MAPA_dia_date]:		
				dados_organizados_plot[MAPA_dia_date] = {}
				for _est,_prn in zip(nome_est[MAPA_dia_date],list_prn[MAPA_dia_date]):
					for prn in _prn:
						str_prn = str(prn)
						for hora in dados_organizados[MAPA_dia_date][_est][str_prn].keys():  
							f_hora = hora
							if not np.isnan(dados_organizados[MAPA_dia_date][_est][str_prn][f_hora]['vtec']):
								try:
									dados_organizados_plot[MAPA_dia_date][f_hora+".lat"].append(dados_organizados[MAPA_dia_date][_est][str_prn][f_hora]['lat'])
								except KeyError:
									dados_organizados_plot[MAPA_dia_date][f_hora+".lat"] = []
									dados_organizados_plot[MAPA_dia_date][f_hora+".lat"].append(dados_organizados[MAPA_dia_date][_est][str_prn][f_hora]['lat'])
								try:
									dados_organizados_plot[MAPA_dia_date][f_hora+".lon"].append(dados_organizados[MAPA_dia_date][_est][str_prn][f_hora]['lon'])
								except KeyError:
									dados_organizados_plot[MAPA_dia_date][f_hora+".lon"] = []
									dados_organizados_plot[MAPA_dia_date][f_hora+".lon"].append(dados_organizados[MAPA_dia_date][_est][str_prn][f_hora]['lon'])
								try:
									dados_organizados_plot[MAPA_dia_date][f_hora+".vtec"].append(dados_organizados[MAPA_dia_date][_est][str_prn][f_hora]['vtec'])
								except KeyError:
									dados_organizados_plot[MAPA_dia_date][f_hora+".vtec"] = []
									dados_organizados_plot[MAPA_dia_date][f_hora+".vtec"].append(dados_organizados[MAPA_dia_date][_est][str_prn][f_hora]['vtec'])
					self._var_barra_progess.set(self._var_barra_progess.get() + coef_loop_processamento)
				try:
					pasta[MAPA_dia_date] = ("Contorno_VTEC_%s-%.2i-%.2i"%(MAPA_dia_date.year,MAPA_dia_date.month,MAPA_dia_date.day))
					os.makedirs(self._filedir+"\\"+pasta[MAPA_dia_date])
				except FileExistsError:
					pass

		numcols, numrows = 100,100
		_vm = self._dado_config.Settings["MAPA"]["fValueMax_B_VTEC"]
		level = np.arange(0,(_vm+1),1)
		cmap = copy.copy(mpl.cm.get_cmap("jet"))
		cmap.set_under("white")
		cmap.set_over("darkred")
		#'____________________________________________________________________________________________________________________________'
		self._var_barra_progess_label.set(self._dado_config.idioma(179))
		#'____________________________________________________________________________________________________________________________'
		coef_loop_plot = ((100)/(3*len(self._PERIODO_MAPA)))
		for PERIODO_DATA_MAPA in self._PERIODO_MAPA:
			try:
				self.fig.clf()
				axes = self.fig.add_subplot(111, projection = ccrs.PlateCarree())
				# hora+=0.00001
				# horas = int(hora)
				# minutos = (hora*60) % 60
				# segundos = (hora*3600) % 60
				# hora_HMS =  ("%02d:%02d:%02d" % (horas, minutos, segundos))
				hora_HMS = str(PERIODO_DATA_MAPA.time())
				# hora-=0.00001
				hora_decimal = (PERIODO_DATA_MAPA.hour) + (PERIODO_DATA_MAPA.minute/60) + (PERIODO_DATA_MAPA.second/3600)
				f_hora = ("%.6f"%float(hora_decimal))[:-1]
				# f_hora = ("%.6f"%hora)[:-1]
				axes.set_title(("%s\n%s"%(str(PERIODO_DATA_MAPA.date()),hora_HMS)),**font)
				axes.set_extent(self._extend_LAT_LONG)
				axes.add_feature(cfeature.BORDERS)
				axes.add_feature(cfeature.COASTLINE)
				x, y, z = np.array(dados_organizados_plot[PERIODO_DATA_MAPA.date()][f_hora+'.lon']), np.array(dados_organizados_plot[PERIODO_DATA_MAPA.date()][f_hora+'.lat']), np.array(dados_organizados_plot[PERIODO_DATA_MAPA.date()][f_hora+'.vtec']) 
				# scx,scy = x, y
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
				axes.plot(self._Coordenadas_equador_Magnetico_X,self._Coordenadas_equador_Magnetico_Y,'k')
				cbar_mapa = self.fig.colorbar(axes.contourf(xi,yi,GD1, cmap = cmap,levels = level, vmin = 0, vmax = _vm ,extend="both",transform=ccrs.PlateCarree()),ticks = np.arange(0,_vm+1,4))
				# axes.contourf(
				#     xi,yi,GD1,
				#     cmap = cmap, 
				#     extend='both',
				#     levels = bounds,
				#     transform=ccrs.PlateCarree()
				# )
				# cbar_mapa = self.fig.colorbar(
				#     nmap,
				#     boundaries=ticks,
				#     extend='both',
				#     spacing='proportional',
				#     ticks=ticks_colorbar
				# )
				# xs = [_sigla[2]for _sigla in _siglas]
				# ys = [_sigla[1]for _sigla in _siglas]
				# axes.scatter(xs, ys, marker='.',c='blue')#, s=10)
				# axes.scatter(scx, scy, marker='.',c='red')#, s=10)
				cbar_mapa.ax.set_title(_titulo_bar,**font)
				camff = (("%s\\%s\\%s.png")%(self._filedir,pasta[PERIODO_DATA_MAPA.date()],hora_HMS.replace(':',"-")))
				# print(camff)
				# fig.set_size_inches(20.0, 10.0)
				self.fig.savefig(camff,dpi=self.fig.dpi)
				self._var_barra_progess_label.set("Figura - "+camff+" gerada")
			except (Exception) as e: 
				print(e)
				pass
			self._var_barra_progess.set(self._var_barra_progess.get() + coef_loop_plot)

		# self._var_barra_progess_label.set(self._dado_config.idioma(94))
		self._var_barra_progess.set(100)
		self._var_barra_progess_label.set(self._dado_config.idioma(180))

		# messagebox.showinfo(self._dado_config.idioma(182), self._dado_config.idioma(180), parent = self)
		plt.close()
		print("--- %s seconds ---" % (time.time() - start_time))
		return None#

	#'____________________________________________________________________________________________________________________________'
	#'____________________________________________________________________________________________________________________________'
	#'____________________________________________________________________________________________________________________________'
	#'____________________________________________________________________________________________________________________________'
	#'____________________________________________________________________________________________________________________________'
	#'____________________________________________________________________________________________________________________________'
	#'____________________________________________________________________________________________________________________________'
	#'____________________________________________________________________________________________________________________________'
	#'____________________________________________________________________________________________________________________________'
	#'____________________________________________________________________________________________________________________________'
	#'____________________________________________________________________________________________________________________________'



	# def stop_process(self,end):
	# 	while True:
	# 		print(end.get())
	# 		if end.get():
	# 			return False
				# self.thread_fim_map.join()
				# raise SystemError('Fim_Thread_MAPA!')
				# break


		# siglas = []
		# for iten_id in self.listaobs.curselection():
		# 	item_line = ((self.listaobs.get(iten_id)).replace('(','')).replace(')','')
		# 	item_line = item_line.split(",")
		# 	N_L = item_line[0].split(' ')
		# 	lat = (item_line[1].strip()).split(' ')
		# 	siglas.append([N_L[0],N_L[1],N_L[2],lat[0],lat[1],item_line[2].strip()])
		# cmnc = r"C:\Users\Mateus_Pillat\Desktop\CMN\2017-09-06"



		# # caminho_itens = [x for x in list(set([(os.path.join(caminho, nome).split('\\')[-1][:4]).upper() for nome in os.listdir(caminho)])) if x != "DESK"]
		# self.dados = {}
		# list_prn = []
		# for es in siglas:
		# 	caminho = cmnc+r"\%s249-2017-09-06.Cmn"%es[0].lower()
		# 	self.list_prn,self.dados = self.uti.Leitura_CMN(caminho,delta_time=delta_time)
		# 	print(self.dados)
		# 	quit()
		# 	try:
		# 		arquivo = open(caminho)
		# 		for line in arquivo.readlines()[5:]:
		# 			linha = line.replace('\n','').split('\t')
		# 			time = float(linha[1]);prn = (linha[2]).replace(' ','');elevation = float(linha[4]);vtec = float(linha[8])
		# 			if elevation > 30:
		# 				if time == -24.0: time = 0.0
		# 				list_prn.append(int(prn))

		# 				try:
		# 					dados[es[0]+prn+".time"].append(time)
		# 				except KeyError:
		# 					dados[es[0]+prn+".time"] = []
		# 					dados[es[0]+prn+".time"].append(time)

		# 				try:
		# 					dados[es[0]+prn+".elevation"].append(elevation)
		# 				except KeyError:
		# 					dados[es[0]+prn+".elevation"] = []
		# 					dados[es[0]+prn+".elevation"].append(elevation)

		# 				try:
		# 					dados[es[0]+prn+".vtec"].append(vtec)
		# 				except KeyError:
		# 					dados[es[0]+prn+".vtec"] = []
		# 					dados[es[0]+prn+".vtec"].append(vtec)

		# 	print(Dados)
		# 	data = datetime.strptime(self.cal_MAPA.get(), '%d/%m/%Y')
		# 	if self.tela_graf.state() == "withdrawn" or self.tela_graf.state() == "iconic":
		# 		self.tela_graf.deiconify()
		# 	elif self.tela_graf.state() == "normal":
		# 		self.tela_graf.focus_force()
		# 	self.janelaprincipal.wait_window(self.janelaprincipal)
		# 	self.img.tight_layout()



		# 	for hora in np.arange(0.0,24.0+(.5/60),(.5/60)):
		# 		list_vtec = []
		# 		list_time = []
		# 		list_lat = []
		# 		list_lon = []
		# 		for cmn in caminho_itens:
		# 			file = (caminho+r"\%s249-2017-09-06.Cmn"%(cmn))
		# 			arquivo = open(file)
		# 			for line in arquivo.readlines()[5:]:
		# 				list_line = line.split('\t')
		# 				if float(list_line[1]) == -24.0:
		# 					list_line[1] = '0.000000'
		# 				if list_line[1] == ("%.6f"%(hora)) and float(list_line[4]) >= 30:#3.000000:
		# 					vtec = float(list_line[8])
		# 					if vtec < 0:vtec = np.nan
		# 					list_vtec.append(vtec)
		# 					list_lat.append(float(list_line[5]))
		# 					list_lon.append(float(list_line[6]))#-360)
		# 			arquivo.close()
		# 		# m = Basemap(projection='cyl',resolution='l',llcrnrlat=-35, urcrnrlat=46,llcrnrlon=-27, urcrnrlon=61)
		# 		# m.drawcoastlines()#linewidth=1.1,zorder=1)
		# 		# vmax = 35
		# 		# passo = 1
		# 		# level = np.arange(0,(vmax+1),passo)
		# 		# # numcols, numrows = 400, 400
		# 		# numcols, numrows = 40,40
		# 		list_lon = np.array(list_lon)
		# 		list_lat = np.array(list_lat)
		# 		list_vtec = np.array(list_vtec)
		# 		Dados.append([list_lon,list_lat,list_vtec])
		# 		print(dados)
		# 		try:	
		# 			print("||--------------------------------------------------------------------------------------------------------------------------------------------||")
		# 			x, y, z = list_lon, list_lat, list_vtec 
		# 			# xi = np.linspace(x.min(),x.max(),100)
		# 			# yi = np.linspace(y.min(),y.max(),100)
		# 			# xi,yi = np.meshgrid(xi,yi)
		# 			# rbf = scipy.interpolate.Rbf(x, y, z, function = "linear")
		# 			# zi = rbf(xi, yi)
		# 			# ny = zi.shape[0]
		# 			# nx = zi.shape[1]
		# 			# lons, lats = m.makegrid(nx, ny)
		# 			# x, y = m(lons, lats)
		# 			xi = np.linspace(list_lon.min(), list_lon.max(), numcols)
		# 			yi = np.linspace(list_lat.min(), list_lat.max(), numrows)
		# 			xi, yi = np.meshgrid(xi, yi)
		# 			zi = griddata((x, y), z,(xi, yi), method = 'linear')

		# 		#################################################################################|INTERPOLAÇÃO|#######################################################################################
					
		# 			x = np.arange(0, zi.shape[1])
		# 			y = np.arange(0, zi.shape[0])
		# 			zi = np.ma.masked_invalid(zi)
		# 			# x = np.arange(0, zi.shape[1])
		# 			# y = np.arange(0, zi.shape[0])
		# 			# xx, yy = np.meshgrid(x, y)
		# 			x1 = xi[~zi.mask]
		# 			y1 = yi[~zi.mask]
		# 			newarr = zi[~zi.mask]
		# 			GD1 = interpolate.griddata((x1, y1), newarr.ravel(),(xi, yi),method='linear')
					
		# 		#################################################################################|INTERPOLAÇÃO|#######################################################################################
		# 			ax_map = plt.gca()
		# 			hora = str(hora).split('.')
		# 			minu = float('0.%s'%(hora[1]))*60  
		# 			hora = ("%.02i:%.02f"%(int(hora[0]),minu))
		# 			plt.title(dia+"  "+hora)
		# 			cmap = plt.cm.get_cmap("jet")
		# 			cmap.set_under("white")
		# 			cmap.set_over("darkred")
					
		# 				# m.contourf(xi,yi,GD1, cmap = cmap,levels= level, vmin = 0, vmax = vmax ,extend="both" )
					
		# 			# m.tricontour(list_lon,list_lat,list_vtec)
		# 			# m.plot(list_lon,list_lat,marker='o',linewidth=0,c = "r", markersize=1)
		# 			# m.tricontour(x,y,z)
		# 			# m.contourf(xi,yi,GD1, cmap = cmap,levels= level, vmin = 0, vmax = vmax ,extend="both" )
		# 			# ('o', 'v', '^', '<', '>', '8', 's', 'p', '*', 'h', 'H', 'D', 'd', 'P', 'X')
		# 			# m.scatter(xi,yi,c=GD1,marker='o',cmap = cmap, vmin = 0, vmax = vmax )
		# 			# m.scatter(list_lon,list_lat,c=list_vtec,cmap = cmap, vmin = 0, vmax = vmax)#, extend="both"  )
		# 			# m.contourf(x,y,z, cmap = cmap,levels= level, vmin = 0, vmax = vmax ,extend="both" )
		# 			# m.contourf(list_lon,list_lat,list_vtec)

		# 			############################################|							|################################################
		# 			############################################|		Contorno SHAPE		|################################################
		# 			############################################|							|################################################
		# 			# x0,x1 = ax_map.get_xlim()
		# 			# y0,y1 = ax_map.get_ylim()
		# 			# map_edges = np.array([[x0,y0],[x1,y0],[x1,y1],[x0,y1]])
		# 			# polys = [map_edges] + m.pais
		# 			# codes = [[Path.MOVETO] + [Path.LINETO for p in p[1:]]for p in polys]
		# 			# polys_lin = [v for p in polys for v in p]
		# 			# codes_lin = [c for cs in codes for c in cs]
		# 			# path = Path(polys_lin, codes_lin)
		# 			# #Important - Set Zorder greater than Contour and less than Map borders
		# 			# patch = PathPatch(path,facecolor='white', lw=.5, zorder =2)
		# 			# ##masking the data:
		# 			# ax_map.add_patch(patch)
		# 			############################################|							|################################################
		# 			############################################|		Contorno SHAPE		|################################################
		# 			############################################|							|################################################
		# 			############################################################################################
		# 			# m.scatter(lista_lat_county)
		# 			# m.colorbar(ticks = np.arange(0,vmax+1,5))#passo))
		# 			m.colorbar(ticks = np.arange(0,vmax+1,5))#passo))
		# 			# m.scatter(x,y,c=zi)
		# 			# m.scatter(x,y, c = zi)
		# 			# m.scatter(x,y,c = zi)
		# 			# caminho = r"C:\Users\Mateus_Pillat\Google Drive\Estágio\Dados\CMN"
		# 			# plt.savefig((r"C:\Users\Mateus_Pillat\Google Drive\Estágio\Dados\MAPA_CMN_2013_JAN_18\CMN_TESTE\%s.png")%(hora).replace(':',"-"))
		# 			print(hora)
		# 			plt.savefig((r"C:\Users\Mateus_Pillat\Desktop\%s.png")%(hora).replace(':',"-"))
		# 			# cms = r"C:\Users\Mateus_Pillat\Google Drive\Estágio\Dados\MAPA_CMN_2017_SET_5_6\%s"%(save)
		# 			# plt.savefig(("%s\%s.png")%(cms,hora.replace(':',"-")),dpi=fig.dpi)#,format='svg' )
		# 			print("Figura (fig-%s.png) - GERADA\nqtd-TEC's= %i"%(hora,len(list_vtec)))
		# 			print("||--------------------------------------------------------------------------------------------------------------------------------------------||")
					
		# 		except ValueError as e:
		# 			print("||--------------------------------------------------------------------------------------------------------------------------------------------||")
		# 			print("%s - Error - %s"%(hora,e))
		# 			print("||--------------------------------------------------------------------------------------------------------------------------------------------||")
		# 			pass

		# 	except FileNotFoundError as e:
		# 		print(e)
		# 		# break
		# print("||----------------------------------------------------------------------FIM----------------------------------------------------------------------||")
		# pass

if __name__ == "__main__":
	tela_graf = Toplevel()
	self._filedir = r"C:\Users\Mateus_Pillat\Desktop\MAPA CMN\CMN\2017-09-05"
	
	# siglas = [['AMBC', '-00', '58', '-62', '55', '8.58'], ['AMCO', '-4', '52', '-65', '20', '4.20'], ['AMMU', '-03', '24', '-57', '43', '2.51'], ['AMPR', '-02', '38', '-56', '44', '2.74'], ['AMTA', '-04', '13', '-69', '56', '6.03'], ['AMTE', '-03', '21', '-64', '42', '5.36'], ['AMUA', '-03', '06', '-60', '01', '3.80'], ['APLJ', '-00', '49', '-52', '30', '3.73'], ['APS1', '-00', '04', '-51', '10', '2.35']] 
	siglas = ['ALAR (-9 44, -36 39 , -14.86)', 'AMBC (-00 58, -62 55 , 8.58)', 'AMCO (-4 52, -65 20 , 4.20)', 'AMHA (-07 31, -63 02 , 1.05)', 'AMMU (-03 24, -57 43 , 2.51)', 'AMPR (-02 38, -56 44 , 2.74)', 'AMTA (-04 13, -69 56 , 6.03)', 'AMTE (-03 21, -64 42 , 5.36)', 'AMUA (-03 06, -60 01 , 3.80)', 'ANKR (39 53, 32 45 , 37.78)', 'APLJ (-00 49, -52 30 , 3.73)', 'APS1 (-00 04, -51 10 , 2.35)', 'APSA (-0 3, -51 10 , 2.33)', 'BABJ (-13 16, -43 33 , -13.84)', 'BABR (-12 9, -44 59 , -12.04)', 'BAIL (-14 48, -39 10 , -17.77)', 'BAIR (-11 18, -41 52 , -13.16)', 'BAIT (-12 31, -40 17 , -15.16)', 'BATF (-17 33, -39 45 , -19.66)', 'BAVC (-14 53, -40 48 , -16.86)', 'BELE (-1 24, -48 27 , -0.45)', 'BEPA (-01 27, -48 26 , -0.51)', 'BOAV (2 50, -60 42 , 9.38)', 'BOMJ (-13 15, -43 25 , -13.91)', 'BRAZ (-15 56, -47 52 , -13.55)', 'BRFT (-3 52, -38 25 , -8.39)', 'CEEU (-3 52, -38 25 , -8.39)', 'CEFE (-20 19, -40 19 , -21.47)', 'CEFT (-3 42, -38 28 , -8.20)', 'CESB (-03 41, -40 20 , -7.14)', 'CHPI (-22 41, -44 59 , -20.50)', 'COAM (-04 5, -63 08 , 4.15)', 'CORU (-19 00, -57 38 , -11.09)', 'CRAO (44 24, 33 59 , 43.08)', 'CRAT (-7 14, -39 24 , -10.98)', 'CRUZ (-7 36, -72 40 , 3.43)', 'CUIB (-15 33, -56 4 , -8.91)', 'DEAR (-30 39, 23 59 , -44.64)', 'DJIG (11 31, 42 50 , 4.89)', 'EESC (-22 0, -47 54 , -18.36)', 'GLSV (50 21, 30 29 , 49.31)', 'GOGY (-16 40, -49 15 , -13.38)', 'GOJA (-17 53, -51 44 , -13.03)', 'GOUR (-14 31, -49 09 , -11.64)', 'GVA1 (-18 51, -41 57 , -19.37)', 'HARB (-25 53, 27 42 , -41.84)', 'HNUS (-34 25, 19 13 , -45.89)', 'IFSC (-27 36, -48 33 , -22.04)', 'ILHA (-20 26, -51 21 , -15.29)', 'IMBT (-28 14, -48 39 , -22.42)', 'IMPZ (-5 29, -47 29 , -4.70)', 'ITAI (-25 25, -54 35 , -17.55)', 'ITAM (-03 08, -58 26 , 3.08)', 'JAMG (-15 21, -43 46 , -15.46)', 'KIRU (67 51, 20 57 , 65.76)', 'MABA (-5 21, -49 7 , -3.66)', 'MABB (-04 14, -44 49 , -5.09)', 'MABS (-7 32, -46 2 , -7.37)', 'MAL2 (-3 1, 40 10 , -13.28)', 'MAPA (0 05, -51 06 , 2.33)', 'MCL1 (-16 43, -43 53 , -16.52)', 'MET3 (60 13, 24 23 , 58.84)', 'MGBH (-19 56, -43 55 , -19.05)', 'MGIN (-22 19, -46 20 , -19.47)', 'MGMC (-16 43, -43 51 , -16.54)', 'MGMT (-18 43, -47 31 , -16.01)', 'MGRP (-19 13, -46 08 , -17.20)', 'MGUB (-18 55, -48 15 , -15.76)', 'MGV1 (-21 33, -45 26 , -19.40)', 'MIKL (46 58, 31 58 , 45.76)', 'MSAQ (-20 27, -55 40 , -13.17)', 'MSCB (-18 59, -56 37 , -11.53)', 'MSCG (-20 26, -54 32 , -13.69)', 'MSCO (-19 00, -57 38 , -11.09)', 'MSDR (-22 12, -54 56 , -14.91)', 'MSPP (-22 37, -55 37 , -14.92)', 'MTBA (-15 53, -52 15 , -11.10)', 'MTCN (-13 33, -52 16 , -9.11)', 'MTCO (-10 48, -55 27 , -5.11)', 'MTGA (-15 53, -52 19 , -11.06)', 'MTJI (-11 26, -58 43 , -4.14)', 'MTNX (-14 42, -52 21 , -10.05)', 'MTSF (-11 37, -50 40 , -8.32)', 'MTSR (-12 33, -55 44 , -6.49)', 'MTVB (-15 00, -59 57 , -6.72)', 'NAUS (-3 1, -60 3 , 3.89)', 'NEIA (-25 1, -47 55 , -20.57)', 'NICO (35 8, 33 23 , 32.23)', 'ONRJ (-22 54, -43 13 , -21.67)', 'OURI (-22 57, -49 54 , -18.00)', 'PAAT (-3 12, -52 10 , -0.07)', 'PAIT (-4 17, -56 2 , 0.93)', 'PASM (-02 26, -54 44 , 1.94)', 'PAST (-2 30, -54 43 , 1.87)', 'PBCG (-7 12, -35 54 , -12.96)', 'PBJP (-07 08, -34 52 , -13.47)', 'PEAF (-07 46, -37 38 , -12.49)', 'PEPE (-9 23, -40 30 , -12.28)', 'PICR (-10 26, -45 10 , -10.44)', 'PIFL (-06 47, -43 02 , -8.44)', 'PISR (-9 02, -42 42 , -10.66)', 'PITN (-05 06, -42 48 , -7.04)', 'POAL (-30 4, -51 7 , -22.43)', 'POLI (-23 33, -46 44 , -20.15)', 'POVE (-8 43, -63 54 , 0.28)', 'PPTE (-22 7, -51 25 , -16.57)', 'PRCV (-24 58, -53 28 , -17.72)', 'PRGU (-25 23, -51 29 , -18.99)', 'PRMA (-23 25, -51 56 , -17.30)', 'RAMO (30 35, 34 46 , 26.90)', 'RECF (-8 3, -34 58 , -14.28)', 'RIGA (56 56, 24 3 , 55.59)', 'RIOB (-9 58, -67 48 , 0.32)', 'RIOD (-22 49, -43 18 , -21.57)', 'RJCG (-21 45, -41 19 , -21.94)', 'RNMO (-5 12, -37 20 , -10.26)', 'RNNA (-5 50, -35 12 , -12.05)', 'RNPF (-06 08, -38 12 , -10.65)', 'ROCD (-13 7, -60 33 , -4.85)', 'ROGM (-10 47, -65 20 , -1.09)', 'ROJI (-10 52, -61 58 , -2.32)', 'ROSA (-22 31, -52 57 , -16.11)', 'RSAL (-29 47, -55 46 , -20.20)', 'RSCL (-28 09, -54 45 , -19.47)', 'RSPE (-31 48, -52 25 , -22.96)', 'RSPF (-28 14, -52 23 , -20.59)', 'SAGA (-0 09, -67 3 , 9.23)', 'SALU (-2 36, -44 13 , -3.93)', 'SAVO (-12 56, -38 26 , -16.63)', 'SCAQ (-26 23, -48 44 , -21.11)', 'SCCH (-27 8, -52 35 , -19.73)', 'SCFL (-27 36, -48 31 , -22.06)', 'SCLA (-27 48, -50 18 , -21.29)', 'SEAJ (-10 55, -37 06 , -15.66)', 'SJRP (-20 47, -49 22 , -16.62)', 'SJSP (-23 12, -45 52 , -20.38)', 'SMAR (-29 43, -53 43 , -21.01)', 'SPAR (-21 11, -50 26 , -16.36)', 'SPBO (-22 51, -48 26 , -18.71)', 'SPBP (-22 59, -46 32 , -19.85)', 'SPC1 (-22 49, -47 04 , -19.43)', 'SPDR (-21 27, -51 33 , -15.98)', 'SPFE (-20 16, -50 14 , -15.74)', 'SPFR (-20 31, -47 23 , -17.51)', 'SPJA (-21 14, -48 17 , -17.56)', 'SPLI (-21 40, -49 44 , -17.10)', 'SPPI (-22 42, -47 37 , -19.04)', 'SPS1 (-23 29, -47 25 , -19.73)', 'SPSO (-23 29, -47 25 , -19.73)', 'SPTU (-21 56, -50 30 , -16.90)', 'SSA1 (-12 59, -38 31 , -16.63)', 'TDOU (-23 4, 30 23 , -39.12)', 'TOGU (-11 44, -49 2 , -9.33)', 'TOPL (-10 10, -48 20 , -8.37)', 'UBA1 (-23 30, -45 7 , -21.02)', 'UBE1 (-18 53, -48 19 , -15.70)', 'UFPR (-25 26, -49 13 , -20.18)', 'VICO (-20 46, -42 52 , -20.30)']
	data = datetime(2017,9,5)

	# img,img_axes = plt.subplots()
	COMP_MAPA(self._filedir,data,50,0,24,480,siglas,-35,7,-77,-32)#.re_figura()

	print('--')
	tela_graf.mainloop()