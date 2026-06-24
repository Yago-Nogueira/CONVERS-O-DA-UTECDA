

import shapefile
from matplotlib.patches import Path, PathPatch, Polygon
# import matplotlib.patches as patches
from matplotlib.collections import PatchCollection
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
import scipy.interpolate
from mpl_toolkits.basemap import maskoceans


# # # def flattens(l):
# # #     for el in l:
# # #         if isinstance(el, collections.Iterable) and not isinstance(el, (str, bytes)):
# # #             yield from flatten(el)
# # #         else:
# # #             yield el


uti = Utilitarios()
# # # with open(((r"C:\Users\Mateus_Pillat\Desktop\JANEIRO_2013_DADOS_REDUZIDO\%s015-2013-01-15.Std")%(x[0].lower()) ), 'r',encoding="UTF-8") as a:
filedir = r"C:\Users\Mateus_Pillat\Desktop\JANEIRO_2013_DADOS_REDUZIDO"
filedir = r"C:\Users\Mateus_Pillat\Google Drive\Estágio\Dados\CMN\2017-09-06-std"
# # filedir = r"C:\Users\Mateus_Pillat\Desktop\Dados 17 e 18 janeiro 2013"
# filedir = r"C:\Users\Mateus_Pillat\Google Drive\Estágio\Dados\STD"

nt_lista,conteudo_lista = uti.Refresh_list_obs(filedir,int(2013),True)

print(conteudo_lista)


lista = [x.replace("(","").replace(")","").replace(",","").split(' ') for x in conteudo_lista]
lista_lat = ([uti.DMDDEC(float(x[1]),float(x[2])) for x in lista])
lista_long = ([uti.DMDDEC(float(x[3]),float(x[4])) for x in lista])
# print(lista_long)
lista_siglas = [x[0] for x in lista]

# # ##################################################################################################################################################################################################################
# # fig_map, ax_map = plt.subplots()
# # # list_poly = []
# # lista_lat_county = []
# # lista_long_county = []
# # repo = []
# # # from shapely.geometry import Point
# # # from shapely.geometry.polygon import Polygon



# # # m = Basemap(projection='cyl',llcrnrlat=-90, urcrnrlat=90,llcrnrlon=-180, urcrnrlon=180, resolution='l')
# m = Basemap(projection='cyl', llcrnrlat=-34, urcrnrlat=6,llcrnrlon=-77, urcrnrlon=-33, resolution='l')
# # # a = m.drawcountries()
m = Basemap(projection='cyl',resolution='l')#llcrnrlat=-35, urcrnrlat=46,llcrnrlon=-27, urcrnrlon=61, resolution='l')
# m = Basemap(projection='cyl',llcrnrlat=-90, urcrnrlat=90,llcrnrlon=-180, urcrnrlon=180, resolution='l')
m.drawcoastlines()#linewidth=1.1,zorder=1)
# # # m.drawmapboundary(color='red',linewidth=2.0)
# # # a = m.fillcontinents(color='blue', lake_color='red' )
# # # m.drawlsmask(land_color='brown',ocean_color='w')
# # # m.drawgreatcircle()
# # # m.drawcountries(linewidth=2, linestyle='solid', color='k', antialiased=0, ax=None, zorder=None)

# # # m.fillcontinents(color='white')
# # # m.drawcountries()


# # # print(a)
# 
# shapefile=r'shape1\BRA_adm1'
# shapefile=r'shape\BRA_adm0'


# shapefile=r'shape\BR_Localidades_2010_v1'
# shp = m.readshapefile(shapefile, 'pais', drawbounds= True, linewidth=1)
# print(shp)
# print(shp)
# print(shp)
##################################################################################################################################################################################################################
# print(m.states)
# patches   = []
# list_cord   = []
# list_patches = []
# for shape in m.pais:
# 	# print(shape)
# 	for xy in shape:
# 		# print(xy)
# 		# list_cord.append(xy)
# 		lista_lat_county.append(xy[0])
# 		lista_long_county.append(xy[1])
	# pol = Polygon(shape, edgecolor='k',fill=False)#,transform=ax_map.transAxes)
	# list_patches.append(pol)
	# print(pol)
	# ax_map.add_patch(pol)
	# for l_xy in pol.get_xy():
		# list_cord.append(l_xy)

		# lista_lat_county.append(l_xy[1])
		# lista_long_county.append(l_xy[0])
		# repo.append(0)


# for nshape, seg in enumerate(m.pais):
	# poly = Polygon(seg, facecolor='white', edgecolor='k')
	# list_poly.append(poly)

	# ax_map.add_patch(poly)#, edgecolor='k', linewidths=1.)


# ax_map.add_collection(PatchCollection(patches, edgecolor='k', linewidths=1.))

# 	for l_xy in poly.get_xy():
# 		lista_lat_county.append(l_xy[1])
# 		lista_long_county.append(l_xy[0])
		# repo.append(np.nan)

# lista_lat_county = np.array(lista_lat_county)
# lista_long_county = np.array(lista_long_county)
##################################################################################################################################################################################################################




vmax = 40
passo = 1
level=np.arange(0,(vmax+1),passo)
# numcols, numrows = 500, 500
numcols, numrows = 80, 80





# lista_lat_county = np.array(lista_lat_county)
# lista_long_county = np.array(lista_long_county)
# s = list(zip(lista_lat_county,lista_long_county))
# s.sort()
# lista_lat_county,lista_long_county = zip(*s)
# print(lista_lat_county)


lista_lat = np.array(lista_lat)
lista_long = np.array(lista_long)
# teste_x = lista_lat
# teste_y = lista_long
# lista_lat = np.append(lista_lat,lista_lat_county)
# lista_long = np.append(lista_long,lista_long_county)
# teste_x.flatten()
# teste_y.flatten()


# print(lista_lat_county.min())
# ml = 184

# print(lista_lat_county.min())
# print(lista_lat_county.max())
# print(lista_long_county.min())
# print(lista_long_county.max())




# y_min =-33.7470817565918 # lista_lat_county.min()
# y_max = 5.264877796173096 # lista_lat_county.max()
# x_min =-73.98970794677734 # lista_long_county.min()
# x_max =-28.84694480895996 # lista_long_county.max()
# lista_long = np.append(lista_long,[x_min]*46)
# lista_long = np.append(lista_long,np.arange(x_min,x_max,1))
# lista_long = np.append(lista_long,[x_max]*46)
# lista_long = np.append(lista_long,np.arange(x_max,x_min,-1))
# lista_lat = np.append(lista_lat,np.arange(y_min,y_max,0.8480860772340194))
# lista_lat = np.append(lista_lat,[y_max]*46)
# lista_lat = np.append(lista_lat,np.arange(y_max,y_min,-0.8480860772340194))
# lista_lat = np.append(lista_lat,[y_min]*46)



# lista_lat.flatten()
# lista_long.flatten()



xi = np.linspace(lista_long.min(), lista_long.max(), numcols)
yi = np.linspace(lista_lat.min(), lista_lat.max(), numrows)


# xi = np.linspace(lista_long.min(), lista_long.max(), numcols)
# yi = np.linspace(lista_lat.min(), lista_lat.max(), numrows)
xi, yi = np.meshgrid(xi, yi)

# cmap = plt.cm.get_cmap("hot")
cmap = plt.cm.get_cmap("jet")
# cmap = plt.cm.get_cmap("Pastel1")
	# # cmap.set_under("darkblue")
cmap.set_under("white")
cmap.set_over("darkred")

print('--')



# ax_map.add_collection(PatchCollection(poly))#, facecolor= 'brown', edgecolor='k', linewidths=1.))
# tec_hora = []
for i in range(0,1440,15):
	tec_hora = []
	for x in lista_siglas:
		try:
			lo = ""

			with open(((r"%s\%s249-2017-09-06.Std")%(filedir,x.lower()) ), 'r',encoding="UTF-8") as a:
			# with open(((r"%s\%s018-2013-01-18.Std")%(filedir,x.lower()) ), 'r',encoding="UTF-8") as a:
			# with open(((r"C:\Users\Mateus_Pillat\Desktop\JANEIRO_2013_DADOS_REDUZIDO\%s076-2015-03-17.Std")%(x[0].lower()) ), 'r',encoding="UTF-8") as a:
				lista = a.readlines()
				a.close()
				# print('entrei aqui')
				hora =(lista[i].split("\t")[0].strip())  
				lo = (lista[i].split("\t")[1].strip())
				# print(lo)
				if lo == "-":
					tec_hora.append(np.nan)
				else:
					tec_hora.append(float(lo))
		except (FileNotFoundError,IndexError):
			tec_hora.append(np.nan)

	tec_hora = np.array(tec_hora)
	# tec_hora = np.append(tec_hora,repo)
	# tec_hora = np.append(tec_hora,[np.nan]*184)
	# tec_hora.flatten()


	# xyz = list(zip(tec_hora,lista_lat,lista_long))
	# print(xyz)
	# xyz.sort()
	# print(xyz)
	# tec_hora,lista_lat,lista_long = list(zip(*xyz))

	# tec_hora = np.array(tec_hora)
	# print(tec_hora)

	# tec_hora = pd.DataFrame(tec_hora).interpolate().values.ravel().tolist()
	# from scipy import interpolate
	

	x, y, z = lista_long, lista_lat, tec_hora
	# print(x,y,z)
	# quit()
	print('aquie')
	zi = griddata((x, y), z,(xi, yi), method = 'linear')#,fill_value=np.nan)




	# nans    = np.array( np.where(  np.isnan(zi) ) ).T
	# notnans = np.array( np.where( ~np.isnan(zi) ) ).T
	# for p in nans:
	# 	zi[p[0],p[1]] = sum( zi[q[0],q[1]]*np.exp(-(sum((p-q)**2))/2) for q in notnans )	
	# zi = interpolate.interp2d(x,y,z, kind='linear')
	# zi = zi(l_i_x, l_i_y)

	# zi = zi(x,y)

	# np.set_printoptions(threshold=np.nan)

	# # interpolate.interp2d(x, y, z, kind='cubic')
	






	print(tec_hora)
#################################################################################|INTERPOLAÇÃO|#######################################################################################
#################################################################################|INTERPOLAÇÃO|#######################################################################################
#################################################################################|INTERPOLAÇÃO|#######################################################################################
#################################################################################|INTERPOLAÇÃO|#######################################################################################
#################################################################################|INTERPOLAÇÃO|#######################################################################################
	from scipy import interpolate
	x = np.arange(0, zi.shape[1])
	y = np.arange(0, zi.shape[0])
	zi = np.ma.masked_invalid(zi)
	# print(zi)
	# x = np.arange(0, zi.shape[1])
	# y = np.arange(0, zi.shape[0])
	# xx, yy = np.meshgrid(x, y)
	x1 = xi[~zi.mask]
	y1 = yi[~zi.mask]
	newarr = zi[~zi.mask]
	GD1 = interpolate.griddata((x1, y1), newarr.ravel(),(xi, yi),method='linear')
#################################################################################|INTERPOLAÇÃO|#######################################################################################
#################################################################################|INTERPOLAÇÃO|#######################################################################################
#################################################################################|INTERPOLAÇÃO|#######################################################################################
#################################################################################|INTERPOLAÇÃO|#######################################################################################
#################################################################################|INTERPOLAÇÃO|#######################################################################################


	# print(GD1)
	

	# for x in GD1:
		# print(x)


	# new_GD1 = []
	# for l_GD1 in GD1:
	# 	new_GD1.append(pd.DataFrame(l_GD1).interpolate().values.ravel().tolist())
	# print(new_GD1)








	# xi = np.linspace(lista_long.min(), lista_long.max(), numcols)
	# yi = np.linspace(lista_lat.min(), lista_lat.max(), numrows)
	# xi = np.linspace(lista_long.min(), lista_long.max(), numcols)
	# yi = np.linspace(lista_lat.min(), lista_lat.max(), numrows)
	# xi, yi = np.meshgrid(xi, yi)

	# cmap = plt.cm.get_cmap("jet")


	# m = Basemap(projection='cyl', llcrnrlat=-35, urcrnrlat=7,llcrnrlon=-77, urcrnrlon=-32, resolution='l')
	
	# mdata = maskoceans(xi, yi, zi, resolution = 'h', grid = 1.25, inlands=True)
	# fig_map.clf()
	print(hora)
	hora = hora.split('.')
	hora = (("%02i:%02i")%(int(hora[0]),  (int(hora[1])*0.06)))
	plt.title(hora)


	ax_map = plt.gca()




	# mdata = maskoceans(xi, yi, zi, resolution = 'h', grid = 1.25, inlands=True)

	# m.contourf(xi, yi, zi, cmap = cmap,levels= level,vmin = 0, vmax = vmax ,extend="both")#levels= level
	# m.contourf(xi, yi, mdata, cmap = cmap,levels= level, vmin = 0, vmax = vmax ,extend="both")
	# m.contourf(lista_long, lista_lat, tec_hora,tri = True, cmap = cmap,levels= level,vmin = 0, vmax = vmax ,extend="both")#levels= level
	
	# import pandas as pd
	
	# df = pd.DataFrame(GD1)
	# df = df.dropna(axis='columns', how='all')

	# df.fillna(method='ffill', axis='all')
	# from scipy.interpolate import SmoothBivariateSpline
	# f = SmoothBivariateSpline(x,y,z,kx=1,ky=1)
	# print(f)
	# znew=np.transpose(f(xi, yi))


	# print(GD1.shape)




	# cs = m.contourf(xi, yi, zi, cmap = cmap,levels= level, vmin = 0, vmax = vmax ,extend="both" )
	cs = m.contourf(xi, yi, GD1, cmap = cmap,levels= level, vmin = 0, vmax = vmax ,extend="both" )
	# m.imshow(GD1,vmin = 0,vmax = vmax,interpolation = 'none',cmap = "jet")

############################################################################################
	# import matplotlib.patches as mpatches
	# import matplotlib.path as mpath
	# poly_codes = [mpath.Path.MOVETO] + (len(list_cord) - 2) * [mpath.Path.LINETO] + [mpath.Path.CLOSEPOLY]
	# path = mpath.Path(list_cord, poly_codes)
	# patch = mpatches.PathPatch(path,visible=False, transform=ax_map.transData)
	# # patch = mpatches.PathPatch(path, visible=False)
	# # patch = mpatches.PathPatch(path, facecolor='none', edgecolor='k')
	# ax_map.add_patch(patch)
	# for col in cs.collections:
	# 	col.set_clip_path(patch)
############################################################################################
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
############################################################################################
	# m.scatter(lista_lat_county)
	# m.colorbar(ticks = np.arange(0,vmax+1,5))#passo))
	
	# pac=PatchCollection(list_patches,match_original = True)

	plt.tight_layout()
	# plt.savefig((r"C:\Users\Mateus_Pillat\Desktop\Teste\Teste\fig%i")%(i))
	# plt.savefig((r"C:\Users\Mateus_Pillat\Desktop\Teste\teste_map_interp\fig%i")%(i))
	

	# plt.show()
	# quit()
	
	plt.savefig((r"C:\Users\Mateus_Pillat\Google Drive\Estágio\Dados\MAPA_CMN_2017_SET_5_6\MAPA 6 STD\fig%i")%(i))



	# with open(((r"C:\Users\Mateus_Pillat\Desktop\Teste\teste_interp\fig%s_018-2013-01-1.Std")%(hora.replace(":","-"))), 'w',encoding="UTF-8") as a:
	# 	for xx, yy, zz in zip(lista_long, lista_lat, tec_hora):
	# 		a.write((("%07.3f\t%07.3f\t%07.3f\n")%(xx, yy, zz)).replace(".",",").replace("0000nan","-999,0"))
	# 	a.close()
		


	print(hora," Gerada")
	
print("FIM----------------------------------------------------------------------")

	# plt.show()



