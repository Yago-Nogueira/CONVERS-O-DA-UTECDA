#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pyqt_utils.filedialog import askdirectory
from pyqt_utils import Toplevel, messagebox


from uuid import getnode as get_mac

# import psutil


from util import DadoIdioma,Utilitarios
from pyqt_utils import *
import pyqt_utils as ui
import getpass
class Licença(Toplevel):
	def __init__(self, master):
		Toplevel.__init__(self, master)
		self.res = ""
		self.uti = Utilitarios()
		self.Dado_config = DadoIdioma()
		self.title(self.Dado_config.idioma(96))
		#self.geometry('800x600')( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°)
		self.resizable(False, False)
		self.protocol("WM_DELETE_WINDOW", self.quit)
		self.frameL=[]
		for rowL in range(4):
			self.frameL.append(Frame(self,bd=3,bg='blue',relief=RIDGE))
			self.frameL[rowL].grid(column=0,row=rowL+1,sticky=E+W)
		Label(self.frameL[0],text=self.Dado_config.idioma(97),font=("Courier", 44)).pack()
		Label(self.frameL[1],text=self.Dado_config.idioma(98),width=10,font="Arial\ Black 10 bold roman").pack(side="left")
		self.nomec = Entry(self.frameL[1],width=25)
		self.nomec.pack(side="right")
		Label(self.frameL[2],text=self.Dado_config.idioma(99),width=10,font="Arial\ Black 10 bold roman").pack(side="left")
		self.inst = Entry(self.frameL[2],width=25)
		self.inst.pack(side="right")		
		Button(self.frameL[3],text=self.Dado_config.idioma(96),command=self.gerararquivo).pack(fill="x")
		self.iconbitmap(self.uti.resource_path('icone.ico'))
		self.wait_visibility(self)
		self.focus_set()
		self.grab_set()
		self.lift()


	# import socket
	# def get_ip_addresses(family):
	# 	for interface, snics in psutil.net_if_addrs().items():
	# 		for snic in snics:
	# 			if snic.family == family:
	# 				yield (interface, (snic.address, snic.netmask))
	

	# ipv4s = dict(get_ip_addresses(socket.AF_INET))
	# macs = dict(get_ip_addresses(psutil.AF_LINK))
	# mac2ipv4 = {macs[k][0]: ipv4s[k] for k in set(macs) & set(ipv4s)}

	# print (mac2ipv4)


	# macs = list(get_ip_addresses(psutil.AF_LINK))
	# print (macs)

	def gerararquivo(self):
		nome = self.nomec.get()
		instP = self.inst.get()
		if nome and instP:
			destino = askdirectory(initialdir = "C:/",title =self.Dado_config.idioma(39),parent=self)
			if destino:
				try:
					# print(self.getHwAddr('enp0s8'))
					# print(get_mac())
					mac = ':'.join(("%012X" % get_mac())[i:i+2] for i in range(0, 12, 2))
					usu = getpass.getuser()
					arquivo = open(destino + r'\request_license.utc','w',encoding="UTF-8")
					arquivo.write('Instituição: ' + instP + "\n")
					arquivo.write('Usuário: ' + usu + "\n")
					arquivo.write('Nome: ' + nome + "\n")
					arquivo.write('ID: ' + mac)
					arquivo.close()
					self.res = True
					messagebox.showinfo(self.Dado_config.idioma(68),self.Dado_config.idioma(100),parent=self)
					self.quit()
				except PermissionError:
					messagebox.showerror(self.Dado_config.idioma(49),self.Dado_config.idioma(95),parent=self)
	def get_res(self):
		return self.res
	def quit(self):
		self.destroy()
def getli(master=None):
	lisc =  Licença(master)
	lisc.wait_window(lisc)
	return lisc.get_res()
#-----------------------------------------------------TESTE-------------------------------------------------
if __name__ == "__main__":
	from pyqt_utils import Tk
	from sys import platform
	janelateste = Tk()
	def callback():
		teste = getli(janelateste)
		if teste:
			print(teste)
	Button(janelateste, text='Teste',command=callback).pack(padx=10, pady=(4, 10))
	janelateste.mainloop()

