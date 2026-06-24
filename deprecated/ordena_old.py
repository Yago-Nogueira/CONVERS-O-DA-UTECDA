#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pyqt_utils.filedialog import askdirectory  
from pyqt_utils import messagebox,ttk
from util import Utilitarios
from pyqt_utils import *
import pyqt_utils as ui
import datetime
import shutil
import os
class Ordena:
	def formularioordena(self,root):
		self.janelaordena = Tk()
		self.janelaordena.title(Utilitarios().idioma(42))
		self.frame = Frame(self.janelaordena, bd=3, highlightbackground ="red" , width=200, height=200 , relief=SUNKEN)
		self.frame.pack( fill=X, side = TOP )
		self.frameb = Frame(self.janelaordena,bd=3, highlightbackground ="red" , width=200, height=200 , relief=SUNKEN)
		self.btnselect = Button(self.frame, text=Utilitarios().idioma(18))
		self.btnselect.pack()
		self.framec = Frame(self.janelaordena,bd=3,width=200, height=200 , relief=SUNKEN )
		self.framec.pack(fill=X)
		self.btnselectdest = Button(self.framec, text=Utilitarios().idioma(43)) 
		self.btnselectdest.pack()
		self.lbldestino = Label(self.framec, text="")
		self.lbldestino.pack()
		self.btnorganizar = Button(self.janelaordena, text=Utilitarios().idioma(44), command=self.organizar)
		self.btnorganizar.pack(side = "bottom")
		self.frameb.pack( fill=X, side = "bottom" )


		self.txt = Entry(self.frameb,width=20)
		self.txt.pack(side = "bottom",fill="y")
		


		self.lblpasta = Label(self.janelaordena, text="")
		self.lblpasta.pack()
		self.lblcaminho = Label(self.frame, text="")
		self.lblcaminho.pack()
		self.btnselect.bind("<Button-1>",lambda id=1:self.selecionar(self.lblcaminho,self.frame,1))
		self.btnselectdest.bind('<Button-1>',lambda id=0:self.selecionar(self.lbldestino,self.framec,0))
		self.lbl = Label(self.frameb, text=Utilitarios().idioma(45))
		self.lbl.pack()
		self.janelaordena.title(Utilitarios().idioma(46))
		self.janelaordena.geometry("300x220")
		self.janelaordena.resizable(False, False)
		self.janelaordena.iconbitmap(r'icone.ico')
		self.janelaordena.protocol("WM_DELETE_WINDOW",lambda tk=root:self.fechamento(tk,self.janelaordena))#lambda troca=1:troca(troca))
		self.janelaordena.mainloop()
	def fechamento(self,root,tk):
		global execc
		uti = Utilitarios()
		if execc == True:
			if messagebox.askokcancel(Utilitarios().idioma(47),Utilitarios().idioma(48)):	 
				execc = False
				#raise NameError
				uti.troca(root,tk)
		else:
			execc = False
			uti.troca(root,tk)

	def mes(self,dia,ano):
		data = int(str(datetime.date(ano, 1, 1) + datetime.timedelta(dia - 1))[5:7])
		return "%.3i"%(data)
	def selecionar(self,lblcaminho,frame,id):
		global filename;global filenamedestino
		file = askdirectory(initialdir = "C:/",title = Utilitarios().idioma(39))
		lblcaminho.configure(text=file)
		if file.strip() != "": 
			frame.configure(bg="gray")
		else: 
			frame.configure(bg='SystemButtonFace')
		if id == 1:
			filename = file
		elif id == 0:
			filenamedestino = file

	def organizar(self):
		ye = self.txt.get()
		#try:
		global filename ; global filenamedestino ; global execc  
		if filenamedestino != None and filenamedestino != "" and filename != None and filename != "" and len(ye) == 4 :
			self.btnselect.config(state='disabled')
			self.btnselectdest.config(state='disabled')				
			self.btnorganizar.config(state='disabled')
			self.txt.config(state='disabled')
			caminhos = [os.path.join(filename, nome) for nome in os.listdir(filename)]
			self.janelaordena.configure(cursor = "watch")
			contfiles=0
			barra =""
			for o in range(len(caminhos)):
				try:
					arquivos = os.listdir(caminhos[o])
					self.lblpasta.configure(text =caminhos[o] + " Nº:" + str(len(arquivos)))
					self.lblpasta.update_idletasks()
					for i in arquivos :
						if not filenamedestino.lower().endswith('/') :
							barra = '/'
						destino = filenamedestino + barra + "GPS/"+ye+"/"
						if i.lower().endswith(".zip") or i.lower().endswith(".z"):
							# print('oi')
							final =  destino + self.mes(int(i[4:7]),int(ye)) + "/" + i[:4]
							if(os.path.exists(final) == False):
								os.makedirs(final)
							local = caminhos[o] + "/" + i
							shutil.copy(local,final)
							self.janelaordena.update()
					contfiles+=1
					execc = True
				except (NotADirectoryError,PermissionError):
					messagebox.showerror(Utilitarios().idioma(49),Utilitarios().idioma(50))
					break
			self.janelaordena.configure(cursor = "arrow") 
			self.lblpasta.configure(text = "%s%d" %(Utilitarios().idioma(51),contfiles))
			execc = False
		else:
			messagebox.showerror(Utilitarios().idioma(49),Utilitarios().idioma(52))
		# except ValueError:
			# messagebox.showerror(Utilitarios().idioma(53),'Verifique o formato do ANO (9999)')
		# except AttributeError:
			# messagebox.showerror(Utilitarios().idioma(53),'Seleione o DIRETÓRIO')
		self.btnselect.config(state='normal')
		self.btnselectdest.config(state='normal')
		self.btnorganizar.config(state='normal')
		self.txt.config(state='normal')	
filenamedestino = None
filename = None
execc = False
parada =  False
