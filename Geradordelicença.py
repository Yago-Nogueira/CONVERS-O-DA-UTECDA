#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pyqt_utils.filedialog import askdirectory, askopenfilename
from pyqt_utils import messagebox, Toplevel
from util import Utilitarios, DadoIdioma
from pyqt_utils import *
import pyqt_utils as ui
import random
import math
import os
class GeradorKey(Tk):
	def __init__(self, master=None):
		Tk.__init__(self,master)
		self.Dado_config = DadoIdioma()
		self.destino = "";self.licença = "";self.id_mac = "";self.frameG = []
		for rowG in range(5):
			self.frameG.append(Frame(self,bd=3,bg='blue',relief=RIDGE))
			self.frameG[rowG].grid(column=0,row=rowG+1,sticky=E+W)
		Label(self.frameG[0],text=self.Dado_config.idioma(74),font=("Courier", 20)).pack()
		self.frameG[1].config(bg='red')
		self.frameG[3].config(bg='red')
		Label(self.frameG[1],text="Arquivo Licença(.utc)",width=18).pack(side='left')
		Button(self.frameG[1],text=self.Dado_config.idioma(75),command=self.Selecionarlicença,width=17).pack(side='right')
		self.lbldados = Label(self.frameG[2],width=32,font="Arial 10 bold roman")
		Label(self.frameG[3],text=self.Dado_config.idioma(77),width=18).pack(side='left')
		Button(self.frameG[3],text=self.Dado_config.idioma(76),command=self.Selecionardestino,width=17).pack(side='right')
		Button(self.frameG[4],text=self.Dado_config.idioma(78),command=self.gerar,width=17).pack()
	def Selecionardestino(self):
		caminho = askdirectory(initialdir = "C:/",title = self.Dado_config.idioma(39),parent=self)
		if caminho:
			self.destino = caminho
			self.frameG[3].config(bg='blue')
		else:
			self.frameG[3].config(bg='red')
	def Selecionarlicença(self):
		filename = askopenfilename(filetypes=(("Licença UTECDA", "*.utc"),),parent=self)
		if filename:
			try:
				self.licença = filename
				arqLicença = open(self.licença, 'r',encoding="UTF-8")
				self.frameG[2].grid(column=0,row=3,sticky=E+W)
				self.frameG[2].config(bg='blue')
				self.frameG[1].config(bg='blue')
				inst = arqLicença.readline()
				self.usu  = arqLicença.readline()
				nome = arqLicença.readline()
				self.id_mac = arqLicença.readline()
				dados = "\n%s\n%s\n%s\n%s\n" % (nome,self.usu,inst,self.id_mac)
				if nome[:6] != "Nome: " or self.usu[:9] != "Usuário: " or inst[:13] != "Instituição: " or self.id_mac[:4] != "ID: ":
					dados=self.Dado_config.idioma(79)
					self.frameG[2].config(bg='red')
					self.frameG[1].config(bg='red')
				self.lbldados.config(text=dados)
				self.lbldados.pack()
				arqLicença.close()
			except IOError:
				messagebox.showerror(self.Dado_config.idioma(49),self.Dado_config.idioma(79),parent=self)
		else:
			self.frameG[1].config(bg='red')
			self.lbldados.config(text="")
			self.frameG[2].grid_forget()
	def gerar(self):
		secure_random = random.SystemRandom()
		self.id_crip = []
		self.id_crip2 = []
		self.id_crip3 = []
		for k in self.id_mac[4:]:
			self.id_crip.append(k)
		for k in range(len(self.id_crip)):
			self.id_crip[k]= ord(self.id_crip[k]) * 2469
		for k in self.id_crip:
			self.id_crip2.append(k)
			self.id_crip2.append(self.id_crip.count(k) * (secure_random.choice(self.id_crip)))	
		for	k in self.id_crip2:
			self.id_crip3.append(secure_random.choice(self.id_crip2))
		#self.usu[9:].replace('\n','')
		self.destino = self.destino + '/license_UTECDA.utc'

		try:
			arquivo = open(self.destino,'w',encoding="UTF-8")
			for k in range(50):
				if k == 25:
					for x in self.id_crip2:
						arquivo.write(str(x) + ':')
					arquivo.write("\n") 
				for f in self.id_crip3:
					arquivo.write(str(secure_random.choice(self.id_crip3))+ ':')
				arquivo.write("\n")
			messagebox.showinfo(self.Dado_config.idioma(80),(self.Dado_config.idioma(81) + self.destino),parent=self)
		except PermissionError:
			messagebox.showinfo(self.Dado_config.idioma(80),self.Dado_config.idioma(95),parent=self)	
		#arquivo.close()


if __name__ == "__main__":
	try:
		# root = Main()
		# root.config(cursor="hand1")
		# root.geometry('600x705')
		# root.iconbitmap(resource_path("Wwalczyszyn-Iwindows-Music-Library.ico"))
		# root.mainloop()
		root = GeradorKey()
		root.config(cursor="hand1")
		root.title(DadoIdioma().idioma(82))
		root.resizable(False, False)
		root.iconbitmap(Utilitarios().resource_path("img/icone.ico"))
		root.mainloop()
		# root = Tk()
		# GeradorKey(root)
		# root.title(DadoIdioma().idioma(82))
		# root.resizable(False, False)
		# root.iconbitmap(r'icone.ico')
		# root.mainloop()
	except (Exception) as  e:
		import sys,traceback
		messagebox.showerror("ERRO", "Erro gravado (ERRO.txt)")
		erro = open('ERRO.txt','w+')
		erro.write(str(e)+"\n")
		[erro.write(str(tb)) for tb in  traceback.format_tb(sys.exc_info()[2])]
		erro.close()

