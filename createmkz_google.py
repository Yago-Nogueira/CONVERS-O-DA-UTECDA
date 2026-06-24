import numpy as np
import simplekml ,datetime, math, igrf, os
from util import Utilitarios#, DadoIdioma

uti = Utilitarios()




# estacoes = [["XSAS" ,"Marsabit Sasura Girls School" ,2.286522 ,38.085304],  ["KYN6" ,"Sebit" ,1.39052868 ,35.34375836],  ["UGN3" ,"Nakasongola" ,1.315258 ,32.47317],  ["XLOY" ,"El Molo Bay" ,2.858734 ,36.700089],  ["XTBI" ,"Ileret Turkana" ,4.28582817 ,36.26217152],  ["A03G" ,"A03G" ,7.810839063 ,38.759367320],  ["KYN7" ,"Nakuru" ,-0.2732177 ,36.04422],  ["KYN1" ,"Nanyuki" ,-0.056460994 ,36.946606903],  ["XYAB" ,"Yabelo" ,4.882263 ,38.097276],  ["KYN5" ,"Egerton" ,0.48835755 ,35.92055391],  ["C01G" ,"Korbet Village" ,7.193445771 ,38.412473455],  ["SEME" ,"Semey" ,50.432694673 ,80.265910472],  ["ADTU" ,"Girmas House Adami Tullu" ,7.866915575 ,38.719128155],  ["KOST" ,"Kostanay" ,53.224557836 ,63.608102306],  ["UGN2" ,"Buyende" ,1.15704421 ,33.16077404],  ["KYN3" ,"Garba Tula" ,0.5347463 ,38.52656],  ["XMOY" ,"Moyale" ,3.545046 ,39.0399],  ["KYN2" ,"Isiolo" ,0.2713473 ,37.59219],  ["XLOK" ,"Lokichogio" ,4.206959 ,34.343753],  ["KYN4" ,"Maralal" ,1.21227766 ,36.55497967],  ["A12G" ,"Badassos House" ,7.745828820 ,38.799984575],  ["HAWA" ,"Hawassa University" ,7.051482039 ,38.499348122],  ["ALPL" ,"Aluto Power Station" ,7.788417264 ,38.794513425],  ["XJNK" ,"Jinka" ,5.755691 ,36.595037],  ["PIRG" ,"Pirguly" ,40.780214 ,48.595302],  ["XHOR" ,"North Horr" ,3.312443 ,37.059656],  ["QABL" ,"Gabala" ,40.957987 ,47.689548],  ["XTEL" ,"Teltele" ,5.030563 ,37.374737],  ["ATRU" ,"Atyrau" ,47.130880505 ,51.953765606],  ["MAR7" ,"Maartsbo" ,60.595052235 ,17.258439891],  ["MAR6" ,"Maartsbo" ,60.595141125 ,17.258521606],  ["XTRM" ,"Turmi" ,4.97485 ,36.479725],  ["OP71" ,"Observatoire de Paris" ,48.835905888 ,2.334974926],  ["C03G" ,"Borama Kabo" ,7.198248855 ,38.475703637],  ["CURG" ,"URJE" ,7.162713194 ,38.393638907],  ["CNHG" ,"CNHG" ,7.148957462 ,38.432129585],  ["UGN1" ,"Nabumali" ,0.98521347 ,34.21790497],  ["ASRG" ,"Southern Rim" ,7.779667687 ,38.766875162]] 

# for est in estacoes:
# 	lat_grauStr = str(est[2]).split(".")
	
# 	lat_grau = str(int(lat_grauStr[0]))
# 	lat_minitos = str(int(float("."+lat_grauStr[1])*60))


# 	lon_grauStr = str(est[3]).split(".")
# 	lon_grau = str(int(lon_grauStr[0]))
# 	lon_minitos = str(int(float("."+lon_grauStr[1])*60))
	

# 	print(est[1] +"\tAF\t"+ est[0]+"\t"+lat_grau+" "+lat_minitos+"\t"+lon_grau+" "+lon_minitos+"\t")




# quit()


lat = []
lon = []
est = []
diplat_list = []
linha_Texto = []

Ano = 2018
Alt = 300

nomearq = "MAPA_%i"%Ano

# mapa = 'Brasil'

# _siglas = ['AMCO', 'AMTG', 'BOGT', 'CN20', 'CN25', 'GOJA', 'GUAT', 'MANA', 'MTCA', 'MTGA', 'MTJI', 'MTSR', 'POAL', 'POVE', 'ROJI', 'SAGA', 'SCLA', 'SNLR', 'SPBP', 'SPDR', 'SPOR', 'UXAL', 'VERA', 'VORA','BAIL', 'BAIT', 'BOAV', 'CBMD', 'CN11', 'CN12', 'CN16', 'CN19', 'CN40', 'KOUG', 'MABB', 'MABS', 'PAAR', 'PASM', 'PICR', 'RDLT', 'SSA1', 'TTUW']
_siglas = ['ASCG', 'CEBR', 'CPVG', 'MAS1', 'OUCA', 'ROAG', 'STHL', 'YKRO','ABPO', 'ADTU', 'BHR4', 'CTPM', 'DEAR', 'DJIG', 'ISBA', 'MBAR', 'MTDK', 'OLO3', 'TDOU', 'VOIM', 'XTBI', 'YIBL']
# mapa = 'Africa'




try:	
	with open((('%s\\OBS.dat')%(os.path.expanduser('~\\UTECDA'))) , 'r',encoding='utf-8') as arquivoOBS:
		line = arquivoOBS.readlines()
		del(line[0])
		for obs in line:
			# print(obs)
			tmpobs = obs.replace("\n","").split("\t")
			cidade = tmpobs[0]
			eb = tmpobs[2]
			if eb in _siglas:
				XLT_EST = tmpobs[3]
				XLN_EST = tmpobs[4]
				inclinacao = uti.get_inclinacao_D(Alt,Ano,XLT_EST,XLN_EST)
				diplat = (math.degrees(math.atan(((math.tan(math.radians(float(inclinacao)))/2)))))
				# print(tmpobs[0]+"\t"+eb+"\tlat = %.2f\tlong = %.2f\tdip = %.2f"%(XLT_EST,XLN_EST,diplat))
				lat.append(XLT_EST)
				lon.append(XLN_EST)
				est.append(eb)
				diplat_list.append(diplat)
				linha_Texto.append([cidade,eb,XLT_EST,XLN_EST,diplat])
			
		arquivoOBS.close()
except IOError as e:
	print('IOError',e)
	# messagebox.showerror(self.Dado_config.idioma(49),self.Dado_config.idioma(55),parent=self)

# linha_Texto.sort(key=lambda x: float(x[4]),reverse=True)

# for c,e,la,lo,d  in linha_Texto:
	# print("[%s,%.2f,%.2f,%.2f]"%(e,la,lo,d))
# quit()

kml=simplekml.Kml()

eq_y = []
eq_x = []
for x in np.arange(-180,181, .1):
	inclinacao = uti.get_inclinacao(Alt,Ano,0,0,x,0)
	diplat = -(math.degrees(math.atan(((math.tan(math.radians(float(inclinacao)))/2)))))
	eq_y.append(diplat)
	eq_x.append(x)

for x,y in zip(eq_y,eq_x):
	a = kml.newpoint(coords=[(y,x)])
	a.style.iconstyle.scale = 1
	a.style.iconstyle.color = simplekml.Color.black
	a.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/target.png'
	# a = kml.newpoint(name="",coords=[(y,x)])
# #################|EQ|###########################################################################################################################
l = []
for x in np.arange(-180,181,.1):
	# a = kml.newpoint(name="",coords=[(x,0)])
	a = kml.newpoint(coords=[(x,0)])
	l.append(a)
	a.style.iconstyle.scale = .8
	a.style.iconstyle.color = simplekml.Color.yellow
	a.style.iconstyle.icon.href = r'point.png'
	# a.style.iconstyle.icon.href = 'point.png'
	# a.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/target.png'
else:
	# l[7].style.iconstyle.name="Equador"
	pass
# #################|EQ|###########################################################################################################################
for no,la,lo,dp in zip(est,lat,lon,diplat_list):
	if no in est:
		a = kml.newpoint(name=("%s"%no),coords=[(lo,la)])
		# a = kml.newpoint(name=("%s (%.2f)"%(no,dp)),coords=[(lo,la)])
		# a = kml.newpoint(name="",coords=[(lo,la)])
		a.style.iconstyle.scale = 5
		a.style.labelstyle.scale = 5
		a.style.iconstyle.color = simplekml.Color.yellow	
		# a.style.iconstyle.color = simplekml.Color.yellow	
		# a.style.iconstyle.color = simplekml.Color.red
		# a.style.iconstyle.color = simplekml.Color.lightgreen

kml.save(nomearq+'.kml')
import os
os.system(nomearq+'.kml')


