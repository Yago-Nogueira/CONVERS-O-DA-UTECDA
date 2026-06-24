import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from util import Utilitarios
uti = Utilitarios()


from matplotlib.colors import LinearSegmentedColormap







CMAP_MODELO_GRAFICO_MAPA = LinearSegmentedColormap.from_list("my_list", ['white','blue','aqua','yellow','red','darkred'], N=100)











y = np.array([-90.0 ,90.0,-180.0, 180.0])
x = np.array([-180,-180,180,180])
z = np.array([10,20,30,40])

xi,yi,GD1 = uti.Interpool_xyz(x,y,z)


_ticks_divisao = 5
_ticks_cbar = 10
_vm_max = 0.9
_vm_min = 0.0
levels = np.linspace(_vm_min,_vm_max,int(_ticks_cbar + ((_ticks_cbar-1)*(_ticks_divisao-1))))
ticks = np.linspace(_vm_min,_vm_max,int(_ticks_cbar))


fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()})


ax.coastlines()

contorno = ax.contourf(
    xi,yi,GD1,
    
    cmap = CMAP_MODELO_GRAFICO_MAPA, 
    extend='both',
    levels = levels,
    transform=ccrs.PlateCarree()
)



CBAR_MODELO_GRAFICO_MAPA = plt.colorbar(
    contorno,
    
    extend='both',
    
    ticks=ticks
)




plt.show()