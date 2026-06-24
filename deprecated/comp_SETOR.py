from qt_ui import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.ticker import LinearLocator , FuncFormatter,IndexLocator
from datetime import datetime, timedelta, date
from qt_ui import ttk, messagebox, Toplevel
from qt_ui.filedialog import askdirectory
# import matplotlib.animation as manimation
import matplotlib,os,calendar,math,io
import matplotlib.ticker as ticker
from qtfontchooser import askfont
from qt_calendar import DateEntry
# from matplotlib import animation
import matplotlib.pyplot as plt
from util import Utilitarios,VerticalScrolledFrame,DadoIdioma
# from Calcigrf import IGRF12 
# matplotlib.use("TkAgg")
import matplotlib

from qt_ui import * 
from scipy.interpolate import griddata
from scipy import interpolate
import qt_ui as tk
import numpy as np

class COMP_SETOR(tk.Toplevel):
	def __init__(self, matplotlib_figure, siglas_estacao, data, diretorio_dados, vtec_max,var_axix_y,var_estacao):
		self._matplotlib_figure = matplotlib_figure
		self._siglas_estacao = siglas_estacao
		self._data = data
		self._diretorio_dados = diretorio_dados
		self._vtec_max = vtec_max
		self._var_axix_y = var_axix_y
		self._var_estacao = var_estacao
		self.titulo_graph_setor = None
		self.y_min_est_setor = None
		self.y_max_est_setor = None
		self.titulo_axe_y_setor = None
		self.titulo_axe_x_setor = None
		self.tick_bar_setor = None
		self.passo_tickX_setor = None
		self.n_rotuloX_setor = None
		self.minX_setor = None
		self.maxX_setor = None
		self.passo_tickY_setor = None
		self.n_rotuloY_setor = None
		self.minY_setor = None
		self.maxY_setor = None
		self.titulo_bar_setor = "VTEC"
		
		self.rfont_titulo_graph_setor = self.rfont_titulo_axe_y_setor = self.rfont_titulo_axe_x_setor = self.rfont_titulo_bar_setor =  {'family': '@MS Gothic', 'size': 28, 'weight': 'bold'}

	def _set_Matplotlib_grafico(self):
		plt.rc('font', weight='bold')
		plt.rc('axes',linewidth=2)
		self._matplotlib_figure.clf()
		self.cbar = None
		self.resp_matriz = None
		self.uti = Utilitarios()
		Dado_config = DadoIdioma()
		self.axes = self._matplotlib_figure.subplots()
		self.eixoG = []
		self.font_default = {'family': 'DejaVu Sans', 'size': 28, 'weight': 'bold'}
		# self.font_default = {'family' : 'Arial','weight' : 'bold','size'   : 18}
		# self.DateFormat = DateFormat 
		dia_ano = self._data.timetuple().tm_yday
		self.estacao_select = []
		for sigla in self._siglas_estacao:
			Lat = self.uti.DMDDEC(int(sigla[1]),int(sigla[2]))
			Lon = self.uti.DMDDEC(int(sigla[3]),int(sigla[4]))
			print(sigla)
			self.estacao_select.append([sigla[0],Lat,Lon,float(sigla[5])])
		if self._var_axix_y == 0:
			self.tituloy = Dado_config.idioma(63)
			self.estacao_select.sort(key=lambda x: x[1])
			self.eixoG = [lat[1] for lat in self.estacao_select]
			self.eixoG_sigla = [item[0] for item in self.estacao_select]
			self.min_y = int(float(self.estacao_select[-1][1]))
			self.max_y = int(float(self.estacao_select[0][1]))
			self.titulo = ("%s-Latitude-%s"%(self._data.date(),self.eixoG_sigla))
		else:
			self.tituloy = "Dip Latitude"
			self.estacao_select.sort(key=lambda x: x[3])
			self.eixoG = [dip[3] for dip in self.estacao_select]
			self.eixoG_sigla = [item[0] for item in self.estacao_select]
			self.min_y = int(float(self.estacao_select[-1][3]))
			self.max_y = int(float(self.estacao_select[0][3]))
			self.titulo = ("%s-Dip_Latitude-%s"%(self._data.date(),self.eixoG_sigla))
		vtec = [];lat = [];dip = []
		list_hora = [np.arange(0,24,(1/60))] * len(self.estacao_select)
		for c,item in enumerate(self.estacao_select):
			nfile = (("\%s%.3i-%s-%.2i-%.2i.Std") % (item[0].lower(),dia_ano,self._data.year,self._data.month,self._data.day))						
			# nome.append(item[0])
			lat.append([float(item[1])] * 1440)
			dip.append([float(item[3])] * 1440)
			tec = self.uti.Leitura_trip(self._diretorio_dados+nfile)[0]
			vtec.append(tec)
			self.estacao_select[c].append(tec)
		vtec = np.array(vtec)
		vtec = vtec.flatten()
		if np.isnan(np.nanmean(vtec)):
			self._matplotlib_figure.text(.5, .5, Dado_config.idioma(94), ha = "center", va = "center")
		else:
			lat = np.array(lat);lat = lat.flatten()
			dip = np.array(dip);dip = dip.flatten()
			# nome = np.array(nome);nome = nome.flatten()
			list_hora = np.array(list_hora);list_hora = list_hora.flatten()
			numcols, numrows = 100,100
			ord_Y = [lat,dip]
			x, y, z = list_hora,ord_Y[self._var_axix_y],vtec
			self.resp_matriz = x, y, z
			# self.resp_matriz = zip(x, y, z)
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
			GD1 = interpolate.griddata((x1, y1), newarr.ravel(),(xi, yi), method = 'linear')
			self.titulox = Dado_config.idioma(41)
			self.titulob = "VTEC"
			self.axes.set_title(self.titulo[:10], picker = 5, gid = "titulo_graph_Setor",**self.font_default)
			self.axes.set_ylabel(self.tituloy, picker = 5, gid = "y_label_graph_Setor",**self.font_default)
			self.axes.set_xlabel(self.titulox, picker = 5, gid = "x_label_graph_Setor",**self.font_default)
			passo = self._vtec_max/15
			level=np.arange(0,(self._vtec_max+1),passo)
			self.cmap = plt.cm.get_cmap("jet")
			self.cmap.set_under("white")
			self.cmap.set_over("darkred")	
			# self.cbar = self._matplotlib_figure.colorbar(self.axes.contourf(self.tec_fix,levels=level,cmap=self.cmap,vmin = 0,vmax=vmax,extend="both"),ax = self.axes,ticks = np.arange(0,vmax+1,self.passo_ctick))
			self.cbar = self._matplotlib_figure.colorbar(self.axes.contourf(xi,yi,GD1,levels=level,cmap=self.cmap,vmin = 0,vmax=self._vtec_max,extend="both") , ax = self.axes,ticks = np.arange(0,self._vtec_max+1,10) )
			self.cbar.ax.set_picker(5)
			self.cbar.ax.set_gid("tick_bar_graph_Setor")
			self.cbar.ax.set_title("VTEC",**self.font_default,picker=5,gid="label_bar_graph_Setor")
			self.cbar.ax.tick_params(axis='y', which='major', width=Dado_config.getWidthTickMajor_Y('Setor'),size=Dado_config.getHeightTickMajor_Y('Setor'),labelsize=Dado_config.getSizeLabelsTick_Y('Setor'))

			
			for label in self.axes.get_xticklabels():  # make the xtick labels pickable
				label.set_picker(True)
				label.set_gid("ticks_x_Setor")
			for label in self.axes.get_yticklabels():  # make the xtick labels pickable
				label.set_picker(True)
				label.set_gid("ticks_y_Setor")
			self.axes.minorticks_on()
			self.axes.tick_params(axis='x', which='minor', width=Dado_config.getWidthTickMinor_X('Setor'),size=Dado_config.getHeightTickMinor_X('Setor'))#,labelsize=tam_x))
			self.axes.tick_params(axis='x', which='major', width=Dado_config.getWidthTickMajor_X('Setor'),size=Dado_config.getHeightTickMajor_X('Setor'),labelsize=Dado_config.getSizeLabelsTick_X('Setor'))
			self.axes.tick_params(axis='y', which='minor', width=Dado_config.getWidthTickMinor_Y('Setor'),size=Dado_config.getHeightTickMinor_Y('Setor'))#,labelsize=tam_y))
			self.axes.tick_params(axis='y', which='major', width=Dado_config.getWidthTickMajor_Y('Setor'),size=Dado_config.getHeightTickMajor_Y('Setor'),labelsize=Dado_config.getSizeLabelsTick_Y('Setor'))
			self.axes.set_xlim(0,24)
			self.axes.yaxis.set_major_locator(ticker.LinearLocator())
			self.axes.xaxis.set_major_locator(ticker.LinearLocator())
			self.axes.yaxis.set_major_formatter(ticker.FuncFormatter(self.major_formatterest))
			self.axes.xaxis.set_major_formatter(ticker.FuncFormatter(self.major_formatterhora))


	def major_formatterhora(self,x, pos):
		return ("%.1i" % (x))
###########################|Formatação dos EIXOS Y|##############################################################################################################################################################
	# def fix_major_formatterest(self,x, pos):
	# 	if x % 1 == 0:resp = (("%.2f")%(x+(self.min_lat)))
	# 	else:resp = ""
	# 	return resp
	def major_formatterest(self,x, pos):
		if self._var_estacao.get(): #and int(x) % 1 == 0:
			# self.axes.yaxis.set_major_locator(ticker.IndexLocator(base=(1), offset=0))
			# resp = (("%s →%s")%((x+(self.min_lat)),self.eixoG[int(x)])) # ("%s ► %s") % (self.estacao_select[int(x)][0],self.estacao_select[int(x)][1])
			lista_dup = self.uti.list_duplicates_of(self.eixoG,x)
			if lista_dup:
				txt_est = ''
				for ind in lista_dup:
					txt_est+= "%s,"%(self.estacao_select[ind][0])
				else:
					txt_est = txt_est[:-1]
					txt_est+= ' → %.2f'% x
				# resp = ("%s → %.2f"%(self.estacao_select[lista_dup[0]][0],x))	
				resp = txt_est	
			else:
				resp = ("%.2f"%(x))	
		else:
			# self.axes.yaxis.set_major_locator(ticker.LinearLocator())            
			# resp = (("%.2f")%(x+(self.min_lat)))	
			resp = ("%.2f"%(x))	

		return resp

	def _get_Matplotlib_grafico_att(self):
		return self._matplotlib_figure,self.axes,self.cbar,self.titulo,self.resp_matriz,self.eixoG_sigla#self.max_y,self.min_y




if __name__ == "__main__":
	tela_graf = Toplevel()
	filedir = r"C:\Users\Mateus_Pillat\Google Drive\Estágio\Dados\STD"
	siglas = [['AMBC', '-00', '58', '-62', '55', '8.58'], ['AMCO', '-4', '52', '-65', '20', '4.20'], ['AMMU', '-03', '24', '-57', '43', '2.51'], ['AMPR', '-02', '38', '-56', '44', '2.74'], ['AMTA', '-04', '13', '-69', '56', '6.03'], ['AMTE', '-03', '21', '-64', '42', '5.36'], ['AMUA', '-03', '06', '-60', '01', '3.80'], ['APLJ', '-00', '49', '-52', '30', '3.73'], ['APS1', '-00', '04', '-51', '10', '2.35']] 
	data = datetime(2017,9,1)

	img,img_axes = plt.subplots()

	varest = BooleanVar(tela_graf)
	varest.set(True)

	img,img_axes,img_cbar,titulo,estacao_select,eixoGs = COMP_SETOR(img,siglas,data,filedir,50,1,varest).re_figura()
	# img,img_axes = COMP_SETOR(img,siglas,data,filedir,50,3,False).re_figura()
	plt.show()
	tela_graf.mainloop()