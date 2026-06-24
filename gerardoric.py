#!/usr/bin/env python
# -*- coding: utf-8 -*-
from qt_ui.filedialog import askdirectory
from qt_ui import messagebox,ttk
from util import Utilitarios,DadoIdioma
import qt_ui as tk 
from qt_ui import * 
import math,os
# import numpy as np


class Geradordeinclinacao(tk.Tk):
	def __init__(self,root):
		tk.Tk.__init__(self)
		self.geometry('800x600')
		self.uti = Utilitarios()
		self.Dado_config = DadoIdioma()
		self.title(self.Dado_config.idioma(83))
		self.frameGs=[]
		for rowGS in range(4):
			self.frameGs.append(Frame(self,bd=3,bg='gray',relief=GROOVE))
		self.frameGs[0].pack(fill='x')
		self.frameGs[1].pack(fill='x')
		self.frameGs[2].pack(fill='y',expand=1)
		self.frameGs[3].pack(fill='x',side='bottom')
		Label(self.frameGs[0],text=self.Dado_config.idioma(84),font=("Courier", 22)).pack(fill=X)
		self.frameCenter = Frame(self.frameGs[1])
		self.frameCenter.pack()
		Label(self.frameCenter,text=self.Dado_config.idioma(85),relief='groove',width=6).pack(side='left',fill=Y,expand=True)

		vcmd = (self.register(self.uti.onValidatesigla),'%S', '%s','%d',2,4)
		self.txtano = Entry(self.frameCenter,validate="key",validatecommand=vcmd)
		self.txtano.pack(side='left',fill=Y,expand=True)
		Label(self.frameCenter,text=self.Dado_config.idioma(86),relief='groove').pack(side='left',fill=Y,expand=True)
		vcmd = (self.register(self.uti.onValidatesigla),'%S', '%s','%d',2)
		self.txtlat = Entry(self.frameCenter,validate="key",validatecommand=vcmd)
		self.txtlat.insert('end','300')
		self.txtlat.pack(side='left',fill=Y,expand=True)
		self.txtano.focus_set()
		
		self.dataCols = (self.Dado_config.idioma(59),self.Dado_config.idioma(60),self.Dado_config.idioma(61),self.Dado_config.idioma(63),self.Dado_config.idioma(62),self.Dado_config.idioma(88),'Dip Lat',self.Dado_config.idioma(101))
		self.grade_igrf_dip = ttk.Treeview(self.frameGs[2],columns=self.dataCols,show='headings')
		self.grade_igrf_dip.pack(side="left",fill='both',expand=1)
		self.ysb = ttk.Scrollbar(self.frameGs[2],orient=tk.VERTICAL, command=self.grade_igrf_dip.yview)
		self.grade_igrf_dip['yscroll'] = self.ysb.set
		self.ysb.pack(side='right',fill=Y)
		for c in self.dataCols:
			self.grade_igrf_dip.heading(c, text=c, command=lambda _c=c:self.uti.treeview_sort_column(self.grade_igrf_dip, _c, False))
		self.grade_igrf_dip.column(self.Dado_config.idioma(59),minwidth=0,width=200, stretch=NO)
		self.grade_igrf_dip.column(self.Dado_config.idioma(60),minwidth=0,width=100, stretch=NO)
		self.grade_igrf_dip.column(self.Dado_config.idioma(61),minwidth=0,width=160, stretch=NO)
		self.grade_igrf_dip.column(self.Dado_config.idioma(63),minwidth=0,width=160, stretch=NO)
		self.grade_igrf_dip.column(self.Dado_config.idioma(62),minwidth=0,width=160, stretch=NO)
		self.grade_igrf_dip.column(self.Dado_config.idioma(88),minwidth=0,width=160, stretch=NO)
		self.grade_igrf_dip.column("Dip Lat",minwidth=0,width=160, stretch=NO)
		self.grade_igrf_dip.column(self.Dado_config.idioma(101),minwidth=0,width=160, stretch=NO)

		try:	
			with open((('%s/OBS.dat')%(os.path.expanduser('~/UTECDA'))) , 'r',encoding='utf-8') as arquivoOBS:
				line = arquivoOBS.readlines()
				del(line[0])
				for obs in line:
					tmpobs = obs.replace("\n","").split("\t")
					LAT = tmpobs[3].split(' ')
					LON = tmpobs[4].split(' ')
					self.grade_igrf_dip.insert('','end',values=(tmpobs[0],tmpobs[1],tmpobs[2],LAT,LON,self.Dado_config.idioma(163),self.Dado_config.idioma(163),self.Dado_config.idioma(163)))	
					# self.grade_igrf_dip.insert('','end',values=(tmpobs[0],tmpobs[1],tmpobs[2],LTD+" "+LTM,LND+" "+LNM,self.Dado_config.idioma(163),self.Dado_config.idioma(163),self.Dado_config.idioma(163)))	
				#(tmpobs[0] + "\t" + tmpobs[1] + "\t" + tmpobs[2] + "\t" + LTD + " " + LTM + "\t" + LND + " " + LNM + "\t" + inclinacao  + '\t' + '\n' )
				arquivoOBS.close()
		except IOError:
			messagebox.showerror(self.Dado_config.idioma(49),self.Dado_config.idioma(55),parent=self)

		self.state('zoomed')
		self.bind('<Return>', self.gerarincGRADE)
		self.btngerar = Button(self.frameCenter,text=self.Dado_config.idioma(87),relief="groove",command=self.gerarincGRADE)
		self.btngerar.pack(fill=X)
		self.btnsave = Button(self.frameGs[3],text=self.Dado_config.idioma(90),relief="groove",command=self.salvarGRADE)
		self.btnsave.pack(fill=X)
		self.protocol("WM_DELETE_WINDOW",lambda tk=root:self.uti.troca(tk,self))
		self.iconbitmap(self.uti.resource_path('img\icone.ico'))
	
	def salvarGRADE(self):
		self.destino = askdirectory(title = self.Dado_config.idioma(39),parent=self)
		if self.destino:
			self.destino+= '/Obs_igrf_'+ str(int(self.ano)) +'_'+ str(int(self.lat)) +'.dat'
			New_obs = [('%s\t%10s\t%10s\t%10s\t%10s\t%10s\tDip Latitude\n')%(self.Dado_config.idioma(59).ljust(60),self.Dado_config.idioma(60),self.Dado_config.idioma(61),self.Dado_config.idioma(63),self.Dado_config.idioma(62),self.Dado_config.idioma(88))]
			for items in self.grade_igrf_dip.get_children():
				Newtmp_obs = self.grade_igrf_dip.item(items)['values']
				# print(Newtmp_obs)
				New_obs.append("%s\t%10s\t%10s\t%10s\t%10s\t%10s\t%10s\t\n" % (Newtmp_obs[0].ljust(60),Newtmp_obs[1],Newtmp_obs[2],Newtmp_obs[3],Newtmp_obs[4],Newtmp_obs[5],Newtmp_obs[6]))
			try:
				with open(self.destino, 'w') as arquivoOBS:
					arquivoOBS.writelines(New_obs)    
					arquivoOBS.close()
					messagebox.showinfo(self.Dado_config.idioma(68), self.Dado_config.idioma(89)+self.destino,parent=self)
			except PermissionError:
				messagebox.showerror(self.Dado_config.idioma(49), self.Dado_config.idioma(95),parent=self)
			except IOError:
				messagebox.showerror(self.Dado_config.idioma(49), self.Dado_config.idioma(55),parent=self)
		
	def gerarincGRADE(self,*event):
		if self.txtlat.get() and self.txtano.get():
			self.configure(cursor = "watch")
			self.lat = float(self.txtlat.get().strip(' ').replace(',','.'))
			self.ano = float(self.txtano.get().strip(' ').replace(',','.'))
			for items in self.grade_igrf_dip.get_children():
				Newtmp_obs = self.grade_igrf_dip.item(items)['values']
				self.grade_igrf_dip.delete(items)
				LAT = Newtmp_obs[3]
				LON = Newtmp_obs[4]
				inclinacao = float(("%.3f")%(self.uti.get_inclinacao_D(float(self.lat),int(self.ano),float(LAT),float(LON))))
				diplat = float(("%.3f")%(math.degrees(math.atan(((math.tan(math.radians(inclinacao))/2))))))
				pos=""
				if diplat >= 20 or diplat <=-20:
					pos = self.Dado_config.idioma(102)
				elif diplat > -5 and diplat < 5:
					pos = self.Dado_config.idioma(103)
				elif diplat <=- 5 and diplat >= -20:
					pos = self.Dado_config.idioma(104)
				elif diplat >= 5 and diplat < 20:
					pos = self.Dado_config.idioma(105)
				self.grade_igrf_dip.insert('','end',values=(Newtmp_obs[0],Newtmp_obs[1],Newtmp_obs[2],LAT,LON,inclinacao,diplat,pos))	
			self.configure(cursor = "arrow") 
		else:
			messagebox.showerror(self.Dado_config.idioma(49),self.Dado_config.idioma(106),parent=self)

if __name__ == "__main__":
	root = Tk()
	Geradordeinclinacao(root)
	root.mainloop()