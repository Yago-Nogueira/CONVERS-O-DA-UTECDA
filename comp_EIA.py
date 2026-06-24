from datetime import datetime, timedelta, date
from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import Qt
from util import Utilitarios, DadoIdioma
from matplotlib import colors as mcolors
from scipy.interpolate import griddata
from scipy import interpolate
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import numpy as np
import matplotlib

class COMP_EIA(QDialog):	
	def __init__(self,matplotlib_figure ,siglas_estacao,diretorio_dados,data_inicial,data_final,varaxix_y,var_estacao,dado_config):
		self._matplotlib_figure = matplotlib_figure
		self._estacao_select = siglas_estacao
		self._diretorio_dados = diretorio_dados
		self._data_inicial = data_inicial
		self._data_final = data_final
		self._varaxix_y = varaxix_y
		self._var_estacao = var_estacao
		self._dado_config = dado_config
		self._vtec_max = self._dado_config.Settings["EIA"]["fValueMax_B_VTEC"]
		self.titulox = self._dado_config.Settings["EIA"]["sTitle_X"]
		self.titulob = self._dado_config.Settings["EIA"]["sTitle_B"]
		
		# self.titulo_graph_EIA = None
		# self.y_min_est_EIA = None
		# self.y_max_est_EIA = None
		# self.titulo_axe_y_EIA = None
		# self.titulo_axe_x_EIA = None
		# self.tick_bar_EIA = None
		# self.passo_tickX_EIA = None
		# self.n_rotuloX_EIA = None
		# self.minX_EIA = None
		# self.maxX_EIA = None
		# self.passo_tickY_EIA = None
		# self.n_rotuloY_EIA = None
		# self.minY_EIA = None
		# self.maxY_EIA = None
		# self.titulo_bar_EIA = "VTEC"

		# self.rfont_titulo_graph_EIA = self.rfont_titulo_axe_y_EIA = self.rfont_titulo_axe_x_EIA = self.rfont_titulo_bar_EIA = {'family': 'DejaVu Sans', 'size': 28, 'weight': 'bold'}


	def _set_Matplotlib_grafico(self):
		# plt.rc('font', weight='bold')
		# plt.rc('axes',linewidth=2)

		self._matplotlib_figure.clf()
		self.resp_matriz = None
		self.cbar = None
		self.estacao_select_dips_e_lats = []
		
		
		# font_default = {'family': 'DejaVu Sans', 'size': 28, 'weight': 'bold'}
		font = self._dado_config.get_font_Settings("EIA")
		self.uti = Utilitarios()
		
		self.axes = self._matplotlib_figure.subplots()
		self.estacao_select_dips_e_lats.append([lat[1] for lat in self._estacao_select])
		self.estacao_select_dips_e_lats.append([dip[3] for dip in self._estacao_select])
		if self._varaxix_y == 0:
			self.titulo_y = self._dado_config.Settings["EIA"]["sTitle_Y_LATITUDE"]#self._dado_config.idioma(63)
			self._estacao_select.sort(key=lambda x: x[1])
			self.eixoG = [lat[1] for lat in self._estacao_select]
			self.min_y = int(self._estacao_select[-1][1])
			self.max_y = int(self._estacao_select[0][1])
		else:
			self.titulo_y = self._dado_config.Settings["EIA"]["sTitle_Y_DIP"]
			self._estacao_select.sort(key=lambda x: x[3])
			self.eixoG = [dip[3] for dip in self._estacao_select]
			self.min_y = int(self._estacao_select[-1][3])
			self.max_y = int(self._estacao_select[0][3])
		if self._data_inicial > self._data_final:
			backdata = self._data_inicial
			self._data_inicial = self._data_final
			self._data_final = backdata
		delta = self._data_final - self._data_inicial
		delta_days = delta.days + 1
		Matriz_DADOS = [];lat_y = [];dip_y = [];list_hora = [np.arange(0,24,(1/60))] * len(self._estacao_select)
		for sigla,lat,_,dip in self._estacao_select:
			Matriz_DADOS_day = []
			lat_y.append([lat] * 1440)
			dip_y.append([dip] * 1440)
			for contd in range(delta_days):
				data = (self._data_inicial + timedelta(days=contd))
				dia_ano = data.timetuple().tm_yday
				nfile = ("/%s%.3i-%i-%.2i-%.2i.Std") % (sigla.lower(),dia_ano,data.year,data.month,data.day)
				Matriz_DADOS_day.append(self.uti.Leitura_trip(self._diretorio_dados + nfile)[0])
				# DADOS[sigla+'.'+str(data.day)+'.'+"VTEC"] = self.uti.Leitura_trip(filedir + nfile)[0]
			Matriz_DADOS.append(Matriz_DADOS_day)

		self.matriz_mean = []
		for list_day in Matriz_DADOS:
			mean_mes = []		
			for hor in np.array(list_day).T:
				mean_mes.append(np.mean(hor))
			self.matriz_mean.append(mean_mes)

		if self._data_inicial.date() == self._data_final.date():self.titulo = ("%s(%s)")%(self._dado_config.idioma(122),self._data_inicial.date())
		else:self.titulo = ("%s(%s)(%s)")%(self._dado_config.idioma(122),self._data_inicial.date(),self._data_final.date())

		vtec = np.array(self.matriz_mean)
		vtec = vtec.flatten()
		if np.isnan(np.nanmean(vtec)):
			self._matplotlib_figure.text(.5,.5, self._dado_config.idioma(94),ha="center", va="center" )
		else:
			lat_y = np.array(lat_y);lat_y = lat_y.flatten()
			dip_y = np.array(dip_y);dip_y = dip_y.flatten()
			list_hora = np.array(list_hora);list_hora = list_hora.flatten()
			numcols, numrows = 100,100
			ord_Y = [lat_y,dip_y]
			x, y, z = list_hora,ord_Y[self._varaxix_y],vtec

			self.resp_matriz = list(zip(x, y, z))
			
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
			GD1 = interpolate.griddata((x1, y1), newarr.ravel(),(xi, yi),method='linear')

			

			self.axes.set_gid("EIA")
			self.axes.set_title(self.titulo,picker=5,gid="titulo_graph:EIA",**font)
			self.axes.set_ylabel(self.titulo_y, picker=5, gid="y_label_graph:EIA",**font)
			self.axes.set_xlabel(self.titulox, picker=5, gid="x_label_graph:EIA",**font)

			passo = self._vtec_max/15
			level=np.arange(0,(self._vtec_max+1),passo)
			
			self.cmap = plt.cm.get_cmap("jet").copy()
			self.cmap.set_under("white")
			self.cmap.set_over("darkred")


			self.cbar = self._matplotlib_figure.colorbar(self.axes.contourf(xi,yi,GD1,levels=level,cmap=self.cmap,vmin = 0,vmax=self._vtec_max,extend="both") , ax = self.axes,ticks = np.arange(0,self._vtec_max+1,10) )
			self.cbar.ax.set_picker(5)
			self.cbar.ax.set_gid("tick_bar_graph:EIA")

			self.cbar.ax.set_title(self.titulob,**font,picker=5,pad=30,gid="label_bar_graph:EIA")
			
			for label in self.axes.get_xticklabels():  # make the xtick labels pickable
				label.set_picker(True)
				label.set_gid("ticks_x:EIA")
			for label in self.axes.get_yticklabels():  # make the xtick labels pickable
				label.set_picker(True)
				label.set_gid("ticks_y:EIA")

			self.axes.minorticks_on()
			self.axes.tick_params(axis='x', which='minor', width=self._dado_config.Settings["EIA"]["fWidthTickMinor_X"],size=self._dado_config.Settings["EIA"]["fHeightTickMinor_X"])#,labelsize=tam_x))
			self.axes.tick_params(axis='x', which='major', width=self._dado_config.Settings["EIA"]["fWidthTickMajor_X"],size=self._dado_config.Settings["EIA"]["fHeightTickMajor_X"],labelsize=self._dado_config.Settings["EIA"]["fSizeLabelsTick_X"])
			self.axes.tick_params(axis='y', which='minor', width=self._dado_config.Settings["EIA"]["fWidthTickMinor_Y"],size=self._dado_config.Settings["EIA"]["fHeightTickMinor_Y"])#,labelsize=tam_y))
			self.axes.tick_params(axis='y', which='major', width=self._dado_config.Settings["EIA"]["fWidthTickMajor_Y"],size=self._dado_config.Settings["EIA"]["fHeightTickMajor_Y"],labelsize=self._dado_config.Settings["EIA"]["fSizeLabelsTick_Y"])
			self.axes.set_xlim(0,24)
			
			
			if self._var_estacao:
				self.axes.yaxis.set_major_locator(ticker.FixedLocator(self.estacao_select_dips_e_lats[self._varaxix_y]))
			else:
				try:
					if self._dado_config.Settings["EIA"]["fValue_Passo_Ticks_Y_temp"]:self.axes.yaxis.set_major_locator(ticker.MultipleLocator(self._dado_config.Settings["EIA"]["fValue_Passo_Ticks_Y_temp"]))
					elif self._dado_config.Settings["EIA"]["iValue_Num_Ticks_Y_temp"]:self.axes.yaxis.set_major_locator(ticker.LinearLocator(self._dado_config.Settings["EIA"]["iValue_Num_Ticks_Y_temp"]))
					else:self.axes.yaxis.set_major_locator(ticker.LinearLocator())
				except KeyError:self.axes.yaxis.set_major_locator(ticker.LinearLocator())
			
			try:
				if self._dado_config.Settings["EIA"]["fValue_Passo_Ticks_X_temp"]:self.axes.xaxis.set_major_locator(ticker.MultipleLocator(self._dado_config.Settings["EIA"]["fValue_Passo_Ticks_X_temp"]))
				elif self._dado_config.Settings["EIA"]["iValue_Num_Ticks_X_temp"]:self.axes.xaxis.set_major_locator(ticker.LinearLocator(self._dado_config.Settings["EIA"]["iValue_Num_Ticks_X_temp"]))
				else:self.axes.xaxis.set_major_locator(ticker.LinearLocator())
			except KeyError:self.axes.xaxis.set_major_locator(ticker.LinearLocator())

			try:self.axes.set_xlim(self._dado_config.Settings["EIA"]["fValueMin_Axes_X_temp"],self._dado_config.Settings["EIA"]["fValueMax_Axes_X_temp"])
			except KeyError:pass
			try:self.axes.set_ylim(self._dado_config.Settings["EIA"]["fValueMin_Axes_Y_temp"],self._dado_config.Settings["EIA"]["fValueMax_Axes_Y_temp"])
			except KeyError:pass
			

			self.axes.yaxis.set_major_formatter(ticker.FuncFormatter(self.major_formatterest))
			self.axes.xaxis.set_major_formatter(ticker.FuncFormatter(self.major_formatterhora))

	def _get_Matplotlib_grafico_att(self):
		return self._matplotlib_figure,self.axes,self.cbar,self.titulo,self.resp_matriz,self.eixoG


	def major_formatterhora(self,x, pos):
		return ("%.1i" % (x))
###########################|Formatação dos EIXOS Y|##############################################################################################################################################################
	# def fix_major_formatterest(self,x, pos):
	# 	if x % 1 == 0:resp = (("%.2f")%(x+(self.min_lat)))
	# 	else:resp = ""
	# 	return resp
	def major_formatterest(self,x, pos):
		if self._var_estacao: #and int(x) % 1 == 0:
			if x in self.estacao_select_dips_e_lats[self._varaxix_y]:
				# self.axes.yaxis.set_major_locator(ticker.IndexLocator(base=(1), offset=0))
				# resp = (("%s →%s")%((x+(self.min_lat)),self.eixoG[int(x)])) # ("%s ► %s") % (self._estacao_select[int(x)][0],self._estacao_select[int(x)][1])
				lista_dup = self.uti.list_duplicates_of(self.eixoG,x)
				if lista_dup:
					txt_est = ''
					for ind in lista_dup:
						txt_est+= "%s,"%(self._estacao_select[ind][0])
					else:
						txt_est = txt_est[:-1]
						txt_est+= ' → %.2f'% x
					# resp = ("%s → %.2f"%(self._estacao_select[lista_dup[0]][0],x))	
					resp = txt_est	
				else:
					resp = ("%.2f"%(x))	
			else:resp = ""
		else:
			# self.axes.yaxis.set_major_locator(ticker.LinearLocator())            
			# resp = (("%.2f")%(x+(self.min_lat)))	
			resp = ("%.2f"%(x))	

		return resp



	
if __name__ == "__main__":
	# print(np.mean([16.89,15.4,15.18,15.73,11.51,17.47,9.11,10.29,24.13,10.8,12.29,10.65,8.67,11.57,15.63,13.08,13.55,12.86,16.02,13.21,15.9,13.71,13.76,12.6,13.83,11.48,16.77,25.29,18.54,14.7]))
	# print(np.mean([16.84,15.38,15.13,15.69,11.47,17.44,9.09,10.21,24.07,10.78,12.29,10.64,8.66,11.52,15.6,13.05,13.57,12.84,15.98,13.19,15.87,13.7,13.76,12.58,13.83,11.47,16.73,25.31,18.61,14.72]))

	tela_graf = Toplevel()
	filedir = r"C:\Users\Mateus_Pillat\Google Drive\Estágio\Dados\STD"
	siglas = [['AMBC', '-00', '58', '-62', '55', '8.58'], ['AMCO', '-4', '52', '-65', '20', '4.20'], ['AMMU', '-03', '24', '-57', '43', '2.51'], ['AMPR', '-02', '38', '-56', '44', '2.74'], ['AMTA', '-04', '13', '-69', '56', '6.03'], ['AMTE', '-03', '21', '-64', '42', '5.36'], ['AMUA', '-03', '06', '-60', '01', '3.80'], ['APLJ', '-00', '49', '-52', '30', '3.73'], ['APS1', '-00', '04', '-51', '10', '2.35']] 
	data_i = datetime(2017,9,1)
	data_f = datetime(2017,9,30)

	varest = BooleanVar(tela_graf)
	varest.set(True)

	img,img_axes = plt.subplots()
	# img,img_axes,img_cbar = COMP_EIA(img,siglas,filedir,data_i,data_f,50).re_figura()
	img,img_axes,img_cbar,titulo,est,eixo = COMP_EIA(img,siglas,filedir,data_i,data_f,50,1,varest).re_figura()
	# quit()
	# img.show()
	tela_graf.mainloop()
