
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



Dados = {}
caminho = r"C:\Users\Mateus_Pillat\Desktop\CMN\2017-09-05"

caminho_itens = [x for x in list(set([(os.path.join(caminho, nome).split('\\')[-1][:4]).upper() for nome in os.listdir(caminho)])) if x != "DESK"]
dia = '248-2017-09-05'
Dados['Ele'] = []
Dados['Lat'] = []
Dados['Lon'] = []
for cam_itens in caminho_itens:
	file = (caminho+r"\%s%s.Cmn"%(cam_itens,dia))
	arquivo = open(file)
	for line in arquivo.readlines()[5:]:
		list_line = line.split('\t')
		
		try:
			Dados[list_line[1]].append(list_line[8])
		except KeyError:
			Dados[list_line[1]] = [list_line[8]]

		Dados['Ele'].append(list_line[4])
		Dados['Lat'].append(list_line[5])
		Dados['Lon'].append(list_line[6])
	arquivo.close()

print(Dados)


