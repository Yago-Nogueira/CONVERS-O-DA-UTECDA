import copy
import math
import os
from datetime import date, datetime, timedelta

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.interpolate import griddata
from util import DadoIdioma, Utilitarios

from pyqt_utils import *

root = Tk()
root.mainloop()

dado_config = DadoIdioma()
uti = Utilitarios()

_rfont_titulo_bar = {'family' : 'Arial','weight' : 'bold','size'   : 28}
_rfont_time_map = {'family' : 'Arial','weight' : 'bold','size'   : 11}
_titulo_bar = "ROTI"

plt.rc('font', weight='bold')
plt.rc('axes',linewidth=2)

start = '07/09/2017 23:00:00'
end = '08/09/2017 06:00:00'

start = datetime.strptime(start, "%d/%m/%Y %H:%M:%S")
end = datetime.strptime(end, "%d/%m/%Y %H:%M:%S")

date = pd.date_range(start = start, end = end, freq='720S')

ncols = 5
nrows = 5


_extend_LAT_LONG = [-27, 61, -35, 46];mapa = 'Africa'
# _extend_LAT_LONG = [-77, -32, -35, 7];mapa = 'Brasil'

###########################|VTEC|####################################
# _vm = 100
# level = np.arange(0,(_vm+1),10)
###########################|VTEC|####################################
cmap = copy.copy(mpl.cm.get_cmap("jet"))
cmap.set_under("white")
cmap.set_over("darkred")
###########################|ROTI|####################################
_vm = 0.9
_ticks_cbar = 10
_ticks_divisao = 4
passo = _vm/(_ticks_cbar*_ticks_divisao)
bounds = np.arange(.1,_vm+passo,passo)
ticks = np.arange(0-passo,_vm+2*passo,passo)
ticks_colorbar =  np.arange(0,_vm+passo,0.1)
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
nmap = mpl.cm.ScalarMappable(norm=norm, cmap=cmap)
###########################|ROTI|####################################
fig, axes = plt.subplots(ncols=ncols,nrows=nrows,subplot_kw={'projection': ccrs.PlateCarree()})
fig.subplots_adjust(
    top=1.0,
    bottom=0.005,
    left=0.257,
    right=0.745,
    hspace=0.0,
    wspace=0.0
    )

x_text_hora = 13 
y_text_hora = -42

eq_y = []
eq_x = []
# for x in range(-180,181,1):
#     inclinacao = uti.get_inclinacao(300,start.year,0,0,x,0)
#     diplat = -(math.degrees(math.atan(((math.tan(math.radians(float(inclinacao)))/2)))))
#     eq_y.append(diplat)
#     eq_x.append(x)

cont_pos_time = 0
for ax,d in zip(axes.flat,date):
    ###########################|VTEC|####################################
    # im = ax.contourf(np.random.random((10,10)), cmap = cmap, vmin=0, vmax=100, levels = level,extend="both", transform=ccrs.PlateCarree())
    ###########################|VTEC|####################################
    ###########################|ROTI|####################################
    # ax.contourf(
    #     np.random.random((10,10)),
    #     cmap = cmap, 
    #     extend='both',
    #     levels = bounds,
    #     transform=ccrs.PlateCarree()
    # )
    ###########################|ROTI|####################################
    ax.plot(eq_x,eq_y,'k')
    ax.set_extent(_extend_LAT_LONG)
    ax.add_feature(cfeature.BORDERS)
    ax.add_feature(cfeature.COASTLINE)
    ax.text(x_text_hora,y_text_hora, date[cont_pos_time].time(),**_rfont_time_map)

    cont_pos_time+=1

cbar_ax = fig.add_axes([0.85, 0.15, 0.0205, 0.7])
###########################|VTEC|####################################
# cbar_mapa = fig.colorbar(im,ticks = np.arange(0,_vm+1,10) ,cax=cbar_ax) 
###########################|VTEC|####################################
###########################|ROTI|####################################
cbar_mapa = fig.colorbar(
    nmap,
    cax=cbar_ax,
    boundaries=ticks,
    extend='both',
    spacing='proportional',
    ticks=ticks_colorbar
)
###########################|ROTI|####################################

cbar_mapa.ax.set_title(_titulo_bar,**_rfont_titulo_bar)
cbar_mapa.ax.tick_params(axis='y', which='major', width=2.0,size=10.0,labelsize=23.0)
fig.set_size_inches(20.0, 10.0)
# mng = plt.get_current_fig_manager()
# mng.window.state('zoomed') #works fine on Windows!

fig.savefig("teste.png",dpi=fig.dpi)
plt.subplot_tool()
plt.show()


