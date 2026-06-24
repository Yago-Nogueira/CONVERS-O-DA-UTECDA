#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt6.QtWidgets import QDialog, QMessageBox, QTreeWidget, QTreeWidgetItem
from util import Utilitarios, DadoIdioma
import os

class CadObs(QDialog):
	def __init__(self, master):
		super().__init__(master)
		self.setGeometry(0, 0, 800, 600)
		self.uti = Utilitarios()
		self.Dado_config = DadoIdioma()
		self.title(self.Dado_config.idioma(56))
		self.frameCs1 = Frame(self,bd=3,bg='gray',relief=GROOVE)
		self.frameCs1.pack(fill='both')
		self.frameCs2 = Frame(self,bd=3,bg='gray',relief=GROOVE)
		self.frameCs2.pack(fill='both')
		self.frameCs3 = Frame(self,bd=3,bg='gray',relief=GROOVE)
		self.frameCs3.pack(fill='both',expand=1)
		self.frameCs4 = Frame(self,bd=3,bg='gray',relief=GROOVE)
		self.frameCs4.pack(fill='both')
		self.lblest = Label(self.frameCs4,font=("Courier", 12))
		self.lblest.pack(side='right')
		Label(self.frameCs1,text=self.Dado_config.idioma(57),font=("Courier", 22)).pack(fill='both')
		self.btncad = Button(self.frameCs2,text=self.Dado_config.idioma(58),command = self.cad)
		self.btncad.pack(fill=X)	
		#---------------------------------------------------------
		self.dataCols = (self.Dado_config.idioma(59),self.Dado_config.idioma(60),self.Dado_config.idioma(61),self.Dado_config.idioma(63),self.Dado_config.idioma(62))
		self.grade = ttk.Treeview(self.frameCs3,columns=self.dataCols,show='headings')
		self.grade.pack(side='left', fill='both',expand=1)
		self.grade.bind('<Delete>', self.Delitem)
		self.grade.bind('<Double-Button-1>',self.Edititem)
		self.grade.bind('<Escape>',lambda e:self.Unselect())
		ysb = ttk.Scrollbar(self.frameCs3,orient=tk.VERTICAL, command=self.grade.yview)
		self.grade['yscroll'] = ysb.set
		ysb.pack(side='right',fill='y')#grid(row=0, column=1, sticky=tk.N + tk.S)
		for c in self.dataCols:
			self.grade.heading(c, text=c, command=lambda _c=c:self.uti.treeview_sort_column(self.grade, _c, False))



		#for col in columns:
		#		treeview.heading(col, text=col, )
		#----leitura arq
		# arquivo = open('OBS.dat', 'r')
		# obs = arquivo.readlines()
		# #obs = sorted(obs, key=lambda tup: tup[0])
		# arquivo.close()
		try:
			with open((('%s/OBS.dat')%(os.path.expanduser('~/UTECDA'))), 'r',encoding='utf-8') as arquivoOBS:
				obs = arquivoOBS.readlines()
				del(obs[0])
				obs.sort()
				arquivoOBS.close()
				for tmpobsdata in obs:
					tmpobsdatasplt = tmpobsdata.split('\t')
					self.grade.insert('','end',values=(tmpobsdatasplt[0].strip(),tmpobsdatasplt[1].strip(),tmpobsdatasplt[2].strip(),tmpobsdatasplt[3].strip(),tmpobsdatasplt[4].strip()))	
				self.contEST()
		except IOError:
				messagebox.showerror(self.Dado_config.idioma(49),self.Dado_config.idioma(55),parent=self)
		
		#----leitura arq
		self.popup_tre = Menu(self.grade, tearoff=0)
		self.popup_tre.add_command(label=self.Dado_config.idioma(160), command=self.Delitem)
		self.popup_tre.add_command(label=self.Dado_config.idioma(161), command=self.Edititem)
		self.popup_tre.add_command(label=self.Dado_config.idioma(113), command=self.Unselect)
		
		self.grade.bind("<Button-3>", self.do_popup)
		self.protocol("WM_DELETE_WINDOW",lambda tk=master:self.uti.troca(tk,self))
		self.focus_set()
		#self.wait_visibility(master)
		self.lift()
		self.state('zoomed')
		#self.resizable(False, False)
		self.iconbitmap(self.uti.resource_path('img\icone.ico'))
		# self.mainloop()
	def do_popup(self,event):
		try:
			self.popup_tre.tk_popup(event.x_root, event.y_root, 0)
		finally:
			self.popup_tre.grab_release()
	def contEST(self):
		self.lblest.config(text=self.Dado_config.idioma(64) + str(len(self.grade.get_children())))
	def cad(self):
		self.windowCad = Toplevel()
		self.frameCDobs=[]
		for rowCDobs in range(4):
			self.frameCDobs.append(Frame(self.windowCad,bd=3,bg='gray',relief=GROOVE))
			self.frameCDobs[rowCDobs].grid(column=0,row=rowCDobs+1,sticky=W+E)
		Label(self.frameCDobs[0],text=self.Dado_config.idioma(65),font=("Courier", 22)).pack(fill=X)
		Label(self.frameCDobs[1],text=self.Dado_config.idioma(59),relief='groove',width=6).pack(side='left')
		self.txtcid = Entry(self.frameCDobs[1],width=47)
		self.txtcid.pack(side='left')
		Label(self.frameCDobs[1],text=self.Dado_config.idioma(60),width=4,relief='groove').pack(side='left')
		vcmd = (self.register(self.uti.onValidatesigla),'%S', '%s','%d',1,2)
		self.txtUf = Entry(self.frameCDobs[1],width=3,validate="key",validatecommand=vcmd)
		self.txtUf.pack(side='left',fill=X)
		Label(self.frameCDobs[2],text=self.Dado_config.idioma(61),relief='groove',width=13).pack(side='left')
		vcmd = (self.register(self.uti.onValidatesigla),'%S', '%s','%d','',4)
		self.txtsigla = Entry(self.frameCDobs[2],width=5,font=(10),validate="key",validatecommand=vcmd)
		self.txtsigla.pack(side='left')
		Label(self.frameCDobs[2],text=self.Dado_config.idioma(63),relief='groove').pack(side='left')
		vcmd = (self.register(self.uti.onValidatesigla),'%S', '%s','%d',2,4)
		self.txtlat1 = Entry(self.frameCDobs[2],width=5,validate="key",validatecommand=vcmd)
		self.txtlat1.pack(side='left')
		self.txtlat2 = Entry(self.frameCDobs[2],width=5,validate="key",validatecommand=vcmd)
		self.txtlat2.pack(side='left')
		Label(self.frameCDobs[2],text=self.Dado_config.idioma(62),relief='groove').pack(side='left')
		self.txtlong1 = Entry(self.frameCDobs[2],width=5,validate="key",validatecommand=vcmd)
		self.txtlong1.pack(side='left')
		self.txtlong2 = Entry(self.frameCDobs[2],width=5,validate="key",validatecommand=vcmd)
		self.txtlong2.pack(side='left')
		self.btncadastrar = Button(self.frameCDobs[3],text=self.Dado_config.idioma(65),command=lambda :self.Inseriritem())
		self.btncadastrar.pack(fill=X)
		self.windowCad.iconbitmap(self.uti.resource_path('icone.ico'))
		#self.windowCad.wait_visibility(master)
		self.windowCad.resizable(False, False)
		self.windowCad.grab_set()
		self.windowCad.focus()
		self.windowCad.lift()
		# self.windowCad.mainloop()
	def AtualizaArqObs(self):
		New_obs = []
		for items in self.grade.get_children():
			Newtmp_obs = self.grade.item(items)['values']
			New_obs.append("%s\t%s\t%s\t%s\t%s\t\n" % (Newtmp_obs[0],Newtmp_obs[1],Newtmp_obs[2],Newtmp_obs[3],Newtmp_obs[4]))
		try:
			with open((('%s/OBS.dat')%(os.path.expanduser('~/Documents/UTECDA'))) , 'w',encoding='utf-8') as arquivoOBS:
				arquivoOBS.write(("%s\t%s\t%s\tLAT LAT\tLONG LONG\t\n")%(DadoIdioma().idioma(59),DadoIdioma().idioma(60),DadoIdioma().idioma(61)))
				arquivoOBS.writelines(New_obs)    
				arquivoOBS.close()
		except IOError:
			messagebox.showerror(self.Dado_config.idioma(49),self.Dado_config.idioma(55),parent=self)
		except PermissionError:
			messagebox.showerror(self.Dado_config.idioma(49),self.Dado_config.idioma(95),parent=self)

	def Delitem(self,*e):
		if len(self.grade.selection()) == 0:
			messagebox.showinfo(self.Dado_config.idioma(145),self.Dado_config.idioma(164),parent=self)
		else:
			if messagebox.askokcancel(self.Dado_config.idioma(66),self.Dado_config.idioma(67),parent=self):		
				for selec in self.grade.selection():
					self.grade.delete(selec)
				self.AtualizaArqObs()	
				# self.contLOC()
				messagebox.showinfo(self.Dado_config.idioma(68),self.Dado_config.idioma(69),parent=self)
	def Inseriritem(self):		
		if not self.txtUf.get() or not self.txtcid.get() or not self.txtsigla.get() or not self.txtlat1.get() or not self.txtlat2.get() or not self.txtlong1.get()  or not self.txtlong1.get():
			messagebox.showerror(self.Dado_config.idioma(68),self.Dado_config.idioma(70) ,parent=self)
		else:
			self.grade.insert('','end',values=(self.txtcid.get().title(),self.txtUf.get().upper(),self.txtsigla.get().upper(),self.txtlat1.get()+' '+self.txtlat2.get(),self.txtlong1.get()+' '+self.txtlong2.get()))	
			self.uti.treeview_sort_column(self.grade, self.Dado_config.idioma(59), False)
			self.AtualizaArqObs()
			self.contEST()	
			self.txtUf.delete(0, 'end')
			self.txtcid.delete(0, 'end')
			self.txtsigla.delete(0, 'end')
			self.txtlat1.delete(0, 'end')
			self.txtlat2.delete(0, 'end')
			self.txtlong1.delete(0, 'end')
			self.txtlong2.delete(0, 'end')
			self.txtcid.focus()
			messagebox.showinfo(self.Dado_config.idioma(68), self.Dado_config.idioma(71),parent=self)
	
	def Edititem(self,*a):
		curItem = self.grade.focus()
		if len(self.grade.selection()) == 0:
			messagebox.showinfo(self.Dado_config.idioma(145),self.Dado_config.idioma(164),parent=self)
		else:
			if curItem and len(self.grade.selection()) == 1:
				dadosEDIT = self.grade.item(curItem)['values']
				self.windowEdit = Toplevel()
				self.frameEd = []
				for rowEd in range(4):
					self.frameEd.append(Frame(self.windowEdit,bd=3,bg='gray',relief=GROOVE))
					self.frameEd[rowEd].grid(column=0,row=rowEd+1,sticky=W+E)
				
				Label(self.frameEd[0],text=self.Dado_config.idioma(72),font=("Courier", 22)).pack(fill=X)
				Label(self.frameEd[1],text=self.Dado_config.idioma(59),relief='groove',width=6).pack(side='left')
				self.txtcidEDIT = Entry(self.frameEd[1],width=47)
				self.txtcidEDIT.insert(0,dadosEDIT[0].strip())
				self.txtcidEDIT.pack(side='left')
				Label(self.frameEd[1],text=self.Dado_config.idioma(60),width=3,relief='groove').pack(side='left')
				vcmd = (self.register(self.uti.onValidatesigla),'%S', '%s','%d',1,2)
				self.txtUfEDIT = Entry(self.frameEd[1],width=4,validate="key",validatecommand=vcmd)
				self.txtUfEDIT.insert(0,dadosEDIT[1].strip())
				self.txtUfEDIT.pack(side='left')
				Label(self.frameEd[2],text=self.Dado_config.idioma(61),relief='groove',width=13).pack(side='left')
				vcmd = (self.register(self.uti.onValidatesigla),'%S', '%s','%d','',4)
				self.txtsiglaEDIT = Entry(self.frameEd[2],width=5,font=(10),validate="key",validatecommand=vcmd)
				self.txtsiglaEDIT.insert(0,dadosEDIT[2].strip())
				self.txtsiglaEDIT.pack(side='left')
				Label(self.frameEd[2],text=self.Dado_config.idioma(63),relief='groove').pack(side='left')
				self.txtlat1EDIT = Entry(self.frameEd[2],width=5,validate="key",validatecommand=vcmd)
				self.txtlat1EDIT.insert(0,dadosEDIT[3].split(' ')[0].strip())
				self.txtlat1EDIT.pack(side='left')
				self.txtlat2EDIT = Entry(self.frameEd[2],width=5,validate="key",validatecommand=vcmd)
				self.txtlat2EDIT.insert(0,dadosEDIT[3].split(' ')[1].strip())		
				self.txtlat2EDIT.pack(side='left')
				Label(self.frameEd[2],text=self.Dado_config.idioma(62),relief='groove').pack(side='left')
				vcmd = (self.register(self.uti.onValidatesigla),'%S', '%s','%d',2,4)
				self.txtlong1EDIT = Entry(self.frameEd[2],width=5,validate="key",validatecommand=vcmd)
				self.txtlong1EDIT.insert(0,dadosEDIT[4].split(' ')[0].strip())
				self.txtlong1EDIT.pack(side='left')
				self.txtlong2EDIT = Entry(self.frameEd[2],width=5,validate="key",validatecommand=vcmd)
				self.txtlong2EDIT.insert(0,dadosEDIT[4].split(' ')[1].strip())
				self.txtlong2EDIT.pack(side='left')
				self.btncadastrarEDIT = Button(self.frameEd[3],text=self.Dado_config.idioma(73), command = self.Editaritem)
				self.btncadastrarEDIT.pack(fill=X)
				self.windowEdit.iconbitmap(self.uti.resource_path('icone.ico'))
				#self.windowEdit.wait_visibility(master)
				self.windowEdit.resizable(False, False)
				self.windowEdit.grab_set()
				self.windowEdit.focus()
				self.windowEdit.lift()
				# self.windowEdit.mainloop()

	def Editaritem(self):
		selected_item = self.grade.selection()[0] 
		self.grade.item(selected_item, values=(self.txtcidEDIT.get().title().strip(),self.txtUfEDIT.get().upper().strip(),self.txtsiglaEDIT.get().upper().strip(),self.txtlat1EDIT.get().strip()+' '+self.txtlat2EDIT.get().strip(),self.txtlong1EDIT.get().strip()+' '+self.txtlong2EDIT.get().strip()))
		self.windowEdit.destroy()
		self.AtualizaArqObs()
		self.contEST()	
	def Unselect(self,*event):
	#---Warning ----CurSelection não exlcuida...
		if len(self.grade.selection()) > 0:
			self.grade.selection_remove(self.grade.selection())
	

if __name__ == "__main__":
	root = Tk()
	teste = CadObs(root)
	teste.mainloop()
