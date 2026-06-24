# import os


# import shapefile
# from matplotlib.patches import Path, PathPatch, Polygon
# # import matplotlib.patches as patches
# from matplotlib.collections import PatchCollection
# import pandas as pd
# from scipy.interpolate import griddata
# import shapefile
# import matplotlib.pyplot as plt
# from mpl_toolkits.basemap import Basemap
# import numpy as np
# from util import Utilitarios
# from numpy import linspace
# import matplotlib.mlab as mlab
# # from matplotlib.patches import Polygon
# from numpy import meshgrid
# import scipy.interpolate
# from mpl_toolkits.basemap import maskoceans



# # caminho = r"C:\Users\Mateus_Pillat\Google Drive\Estágio\Dados\CMN"
# caminho = r"C:\Users\Mateus-Not\Google Drive\Estágio\Dados\CMN"
# caminho_itens = [x for x in list(set([(os.path.join(caminho, nome).split('\\')[-1][:4]).upper() for nome in os.listdir(caminho)])) if x != "DESK"]
# caminho_itens.sort()


# # print(caminho_itens)
# list_vtec = []
# list_time = []
# list_lat = []
# list_lon = []
# for cmn in caminho_itens:
# 	file = (caminho+r"\%s018-2015-01-18.Cmn"%(cmn))
# 	arquivo = open(file)
	

# 	for line in arquivo.readlines()[5:]:
# 		list_line = line.split('\t')
# 		if float(list_line[1]) == 3.000000:

# 			list_vtec.append(float(list_line[8]))
# 			list_lat.append(float(list_line[5]))
# 			list_lon.append(float(list_line[6]))


# 	arquivo.close()




# # ls = list(zip(list_vtec,list_lat,list_lon))
# # ls.sort()
# # list_vtec,list_lat,list_lon =zip(*ls)

# # quit()

# m = Basemap(projection='cyl',llcrnrlat=-34, urcrnrlat=6,llcrnrlon=-77, urcrnrlon=-33, resolution='l')
# shapefile=r'shape\BRA_adm0'
# shp = m.readshapefile(shapefile, 'pais', drawbounds= True, linewidth=1)
# vmax = 40
# passo = 1
# level=np.arange(0,(vmax+1),passo)
# numcols, numrows = 100, 100


# list_lat = np.array(list_lat)
# list_lon = np.array(list_lon)
# list_vtec = np.array(list_vtec)

# x, y, z = list_lon, list_lat, list_vtec 
# xi,yi = np.linspace(x.min(),x.max(),100),np.linspace(y.min(),y.max(),100)
# xi,yi = np.meshgrid(xi,yi)


# # xt, yt = map(x,y)
# rbf = scipy.interpolate.Rbf(x, y, z, function = "linear")
# zi = rbf(xi, yi)

# cmap = plt.cm.get_cmap("jet")
# cmap.set_under("white")
# cmap.set_over("darkred")

# ny = zi.shape[0]; nx = zi.shape[1]
# lons, lats = m.makegrid(nx, ny) # get lat/lons of ny by nx evenly space grid.
# x, y = m(lons, lats)

# ax_map = plt.gca()
# m.contourf(x,y,zi, cmap = cmap,levels= level, vmin = 0, vmax = vmax ,extend="both" )
# #m.contourf(x,y,zi,extend="both" )


# # plt.contourf(zi,cmap = cmap)





# x0,x1 = ax_map.get_xlim()
# y0,y1 = ax_map.get_ylim()
# map_edges = np.array([[x0,y0],[x1,y0],[x1,y1],[x0,y1]])

# polys = [map_edges] + m.pais

# codes = [[Path.MOVETO] + [Path.LINETO for p in p[1:]]for p in polys]
# polys_lin = [v for p in polys for v in p]
# codes_lin = [c for cs in codes for c in cs]
# path = Path(polys_lin, codes_lin)

# #Important - Set Zorder greater than Contour and less than Map borders
# patch = PathPatch(path,facecolor='white', lw=.5, zorder =2)

# ##masking the data:
# ax_map.add_patch(patch)
# ############################################################################################
# # m.scatter(lista_lat_county)
# m.colorbar(ticks = np.arange(0,vmax+1,5))#passo))




# # xi = np.linspace(list_lon.min(), list_lon.max(), numcols)
# # yi = np.linspace(list_lat.min(), list_lat.max(), numrows)
# # xi, yi = np.meshgrid(xi, yi)
# # cmap = plt.cm.get_cmap("jet")
# # cmap.set_under("white")
# # cmap.set_over("darkred")
# # x, y, z = list_lon, list_lat, list_vtec 
# # zi = griddata((x, y), z,(xi, yi), method = 'cubic')
# # from scipy import interpolate
# # x = np.arange(0, zi.shape[1])
# # y = np.arange(0, zi.shape[0])
# # zi = np.ma.masked_invalid(zi)
# # # print(zi)
# # # x = np.arange(0, zi.shape[1])
# # # y = np.arange(0, zi.shape[0])
# # # xx, yy = np.meshgrid(x, y)
# # x1 = xi[~zi.mask]
# # y1 = yi[~zi.mask]
# # newarr = zi[~zi.mask]
# # GD1 = interpolate.griddata((x1, y1), newarr.ravel(),(xi, yi),method='linear')
# # plt.clf()
# # # hora = hora.split('.')
# # # hora = (("%02i:%02i")%(int(hora[0])  ,  (int(hora[1])*0.06)))
# # plt.title('hora')
# # ax_map = plt.gca()
# # cs = m.contourf(xi, yi, zi, cmap = cmap,levels= level, vmin = 0, vmax = vmax ,extend="both" )



# plt.show()



import os


import shapefile
from matplotlib.patches import Path, PathPatch, Polygon
# import matplotlib.patches as patches
from matplotlib.collections import PatchCollection
from scipy import interpolate
import pandas as pd
from scipy.interpolate import griddata
import shapefile
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
from util import Utilitarios
from numpy import linspace
import matplotlib.mlab as mlab
# from matplotlib.patches import Polygon
from numpy import meshgrid
# import scipy.interpolate
from mpl_toolkits.basemap import maskoceans

dias = ['248-2017-09-05']
caminhos = ['2017-09-05_AFRICA']
savecam = ['5 MAPA AFRICA']



for dia,save,cams in zip(dias,savecam,caminhos):
	# print(dia,save,cams)
	
	caminho = r"C:\Users\Mateus_Pillat\Desktop\CMN\%s"%cams
	# print(caminho)
	# caminho = r"C:\Users\Mateus_Pillat\Google Drive\Estágio\Dados\CMN\2013-01-17"
	# caminho = r"C:\Users\Mateus-Not\Google Drive\Estágio\Dados\CMN"
	caminho_itens = [x for x in list(set([(os.path.join(caminho, nome).split('\\')[-1][:4]).upper() for nome in os.listdir(caminho)])) if x != "DESK"]
	# print(len(caminho_itens))
	fig = plt.figure()
	
	for hora in np.arange(12,14.25,(.5/60)):
		# plt.clf()
		list_vtec = []
		list_time = []
		list_lat = []
		list_lon = []


		for cmn in caminho_itens:
			file = (caminho+r"\%s%s.Cmn"%(cmn,dia))
			arquivo = open(file)
			for line in arquivo.readlines()[5:]:
				list_line = line.split('\t')
				if float(list_line[1]) == -24.0:
					 list_line[1] = '0.000000'

					 
				if list_line[1] == ("%.6f"%(hora)) and float(list_line[4]) >= 30:#3.000000:
					vtec = float(list_line[8])
					if vtec < 0:vtec = np.nan
					list_vtec.append(vtec)
					list_lat.append(float(list_line[5]))
					list_lon.append(float(list_line[6]))#-360)
			arquivo.close()
		m = Basemap(projection='cyl',resolution='l',llcrnrlat=-35, urcrnrlat=46,llcrnrlon=-27, urcrnrlon=61)
		# m = Basemap(projection='cyl',llcrnrlat=-90, urcrnrlat=90,llcrnrlon=-180, urcrnrlon=180, resolution='l')
		m.drawcoastlines()#linewidth=1.1,zorder=1)
		# m.drawcountries()#linewidth=1.1,zorder=1)
		# m.drawstates()#linewidth=1.1,zorder=1)
		# shapefile=r'shape\BRA_adm0'
		# shp = m.readshapefile(shapefile, 'pais', drawbounds= True, linewidth=1)

		vmax = 35
		passo = 1
		level = np.arange(0,(vmax+1),passo)
		# numcols, numrows = 400, 400
		numcols, numrows = 40,40
		list_lon = np.array(list_lon)
		list_lat = np.array(list_lat)
		list_vtec = np.array(list_vtec)

		try:	
			print("||--------------------------------------------------------------------------------------------------------------------------------------------||")
			x, y, z = list_lon, list_lat, list_vtec 
			print(x, y, z)
			# xi = np.linspace(x.min(),x.max(),100)
			# yi = np.linspace(y.min(),y.max(),100)
			# xi,yi = np.meshgrid(xi,yi)
			# rbf = scipy.interpolate.Rbf(x, y, z, function = "linear")
			# zi = rbf(xi, yi)
			# ny = zi.shape[0]
			# nx = zi.shape[1]
			# lons, lats = m.makegrid(nx, ny)
			# x, y = m(lons, lats)
			xi = np.linspace(list_lon.min(), list_lon.max(), numcols)
			yi = np.linspace(list_lat.min(), list_lat.max(), numrows)
			xi, yi = np.meshgrid(xi, yi)
			zi = griddata((x, y), z,(xi, yi), method = 'linear')

		#################################################################################|INTERPOLAÇÃO|#######################################################################################
			from scipy import interpolate
			x = np.arange(0, zi.shape[1])
			y = np.arange(0, zi.shape[0])
			zi = np.ma.masked_invalid(zi)
			# x = np.arange(0, zi.shape[1])
			# y = np.arange(0, zi.shape[0])
			# xx, yy = np.meshgrid(x, y)
			x1 = xi[~zi.mask]
			y1 = yi[~zi.mask]
			newarr = zi[~zi.mask]
			GD1 = interpolate.griddata((x1, y1), newarr.ravel(),(xi, yi),method='linear')
		#################################################################################|INTERPOLAÇÃO|#######################################################################################
			ax_map = plt.gca()
			hora = str(hora).split('.')
			minu = float('0.%s'%(hora[1]))*60  
			hora = ("%.02i:%.02f"%(int(hora[0]),minu))
			plt.title(dia+"  "+hora)
			cmap = plt.cm.get_cmap("jet")
			cmap.set_under("white")
			cmap.set_over("darkred")
			m.contourf(xi,yi,GD1, cmap = cmap,levels= level, vmin = 0, vmax = vmax ,extend="both" )
			# m.tricontour(list_lon,list_lat,list_vtec)
			# m.plot(list_lon,list_lat,marker='o',linewidth=0,c = "r", markersize=1)
			# m.tricontour(x,y,z)
			# m.contourf(xi,yi,GD1, cmap = cmap,levels= level, vmin = 0, vmax = vmax ,extend="both" )
			# ('o', 'v', '^', '<', '>', '8', 's', 'p', '*', 'h', 'H', 'D', 'd', 'P', 'X')
			# m.scatter(xi,yi,c=GD1,marker='o',cmap = cmap, vmin = 0, vmax = vmax )
			# m.scatter(list_lon,list_lat,c=list_vtec,cmap = cmap, vmin = 0, vmax = vmax)#, extend="both"  )
			# m.contourf(x,y,z, cmap = cmap,levels= level, vmin = 0, vmax = vmax ,extend="both" )
			# m.contourf(list_lon,list_lat,list_vtec)









			############################################|							|################################################
			############################################|		Contorno SHAPE		|################################################
			############################################|							|################################################
			# x0,x1 = ax_map.get_xlim()
			# y0,y1 = ax_map.get_ylim()
			# map_edges = np.array([[x0,y0],[x1,y0],[x1,y1],[x0,y1]])
			# polys = [map_edges] + m.pais
			# codes = [[Path.MOVETO] + [Path.LINETO for p in p[1:]]for p in polys]
			# polys_lin = [v for p in polys for v in p]
			# codes_lin = [c for cs in codes for c in cs]
			# path = Path(polys_lin, codes_lin)
			# #Important - Set Zorder greater than Contour and less than Map borders
			# patch = PathPatch(path,facecolor='white', lw=.5, zorder =2)
			# ##masking the data:
			# ax_map.add_patch(patch)
			############################################|							|################################################
			############################################|		Contorno SHAPE		|################################################
			############################################|							|################################################








			############################################################################################
			# m.scatter(lista_lat_county)
			# m.colorbar(ticks = np.arange(0,vmax+1,5))#passo))
			m.colorbar(ticks = np.arange(0,vmax+1,5))#passo))
			# m.scatter(x,y,c=zi)
			# m.scatter(x,y, c = zi)
			# m.scatter(x,y,c = zi)
			# caminho = r"C:\Users\Mateus_Pillat\Google Drive\Estágio\Dados\CMN"

			
			# plt.savefig((r"C:\Users\Mateus_Pillat\Google Drive\Estágio\Dados\MAPA_CMN_2013_JAN_18\CMN_TESTE\%s.png")%(hora).replace(':',"-"))
			
			cms = r"C:\Users\Mateus_Pillat\Google Drive\Estágio\Dados\MAPA_CMN_2017_SET_5_6\%s"%(save)

			plt.savefig(("%s\%s.png")%(cms,hora.replace(':',"-")),dpi=fig.dpi)#,format='svg' )
			

			# plt.savefig((r"C:\Users\Mateus_Pillat\Google Drive\Estágio\Dados\MAPA_CMN_2013_JAN_18\CMN_TESTE_FILTRO_3_MIN\%s-b%i.png")%((hora).),dpi=fig.dpi)#,format='svg' )
			# fig.savefig('temp',format='png', dpi=fig.dpi)



			print("Figura (fig-%s.png) - GERADA\nqtd-TEC's= %i"%(hora,len(list_vtec)))
			print("||--------------------------------------------------------------------------------------------------------------------------------------------||")
				

			# plt.show()
			# quit()

		except ValueError as e:
			print("||--------------------------------------------------------------------------------------------------------------------------------------------||")
			print("%s - Error - %s"%(hora,e))
			print("||--------------------------------------------------------------------------------------------------------------------------------------------||")
			pass

	print("||----------------------------------------------------------------------FIM----------------------------------------------------------------------||")










