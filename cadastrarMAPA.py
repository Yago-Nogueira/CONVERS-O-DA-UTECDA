#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt6.QtWidgets import QDialog, QMessageBox, QTreeWidget, QTreeWidgetItem
from util import Utilitarios, DadoIdioma
import os


class CadMap(QDialog):
	def __init__(self, master, cbg = None):
		super().__init__(master)
		self.setGeometry(0, 0, 800, 600)
		self.cbg = cbg
		self.master = master
		self.uti = Utilitarios()
		self.Dado_config = DadoIdioma()
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
		Label(self.frameCs1,text=self.Dado_config.idioma(149),font=("Courier", 22)).pack(fill='both')
		self.btncad = Button(self.frameCs2,text=self.Dado_config.idioma(148), command=self.cad)
		self.btncad.pack(fill=X)	
		self.dataCols = (self.Dado_config.idioma(61),"Latitude","Longitude")
		self.grade = ttk.Treeview(self.frameCs3,columns=self.dataCols,show='headings')
		self.grade.pack(side='left', fill='both',expand=1)
		self.grade.bind('<Delete>', self.Delitem)
		self.grade.bind('<Double-Button-1>',self.Edititem)
		self.grade.bind('<Escape>',self.Unselect)
		ysb = ttk.Scrollbar(self.frameCs3,orient="vertical", command=self.grade.yview)
		self.grade['yscroll'] = ysb.set
		ysb.pack(side='right',fill='y')#grid(row=0, column=1, sticky="ns")
		for c in self.dataCols:
			self.grade.heading(c, text=c, command=lambda _c=c:self.uti.treeview_sort_column(self.grade, _c, False))


		try:
			with open((('%s/LOCS.dat')%(os.path.expanduser('~/Documents/UTECDA'))) , 'r',encoding="UTF-8") as locs:
				linhas_loc = locs.readlines()
				linhas_loc = [loc.replace("\n","").split("\t") for loc in linhas_loc]
				# print(linhas_loc)
				for datag in linhas_loc:
					self.grade.insert('','end',values=datag)
				self.contLOC()
		except (IOError,IndexError,ValueError,PermissionError)as e:
				self.uti.gravar_erro(e)



		self.popup_tre = Menu(self.grade, tearoff=0)
		self.popup_tre.add_command(label=self.Dado_config.idioma(160), command=self.Delitem)
		self.popup_tre.add_command(label=self.Dado_config.idioma(161), command=self.Edititem)
		self.popup_tre.add_command(label=self.Dado_config.idioma(113), command=self.Unselect)

		
		self.grade.bind("<Button-3>", self.do_popup)

		self.bind('<Return>', self.cad)
		self.protocol("WM_DELETE_WINDOW",self.quit)
		# self.bind('<Return>', self.teste)
		self.focus_set()
		#self.wait_visibility(master)
		self.lift()
		# self.state('zoomed')
		# self.resizable(False, False)
		self.state('zoomed')

		self.iconbitmap(self.uti.resource_path('icone.ico'))

		# self.geometry('372x366')
		self.mainloop()
	
	def do_popup(self,event):
		try:
			self.popup_tre.tk_popup(event.x_root, event.y_root, 0)
		finally:
			self.popup_tre.grab_release()

	def quit(self):
		self.list_loc = [self.grade.item(items)['values'] for items in self.grade.get_children()]
		self.n_list_loc = [ll[0] for ll in self.list_loc]
		self.cbg['values'] = self.n_list_loc
		self.uti.troca(self.master,self)
	def get_lista_loc(self):
		return self.list_loc,self.n_list_loc
	def contLOC(self):
		self.lblest.config(text=self.Dado_config.idioma(150) + str(len(self.grade.get_children())))
	

	def cad(self,*event):
		self.windowCad = Toplevel(self)
		self.frameDc = []
		for rowF in range(4):
			self.frameDc.append(Frame(self.windowCad,bd=3,bg='gray',relief='groove'))
			self.frameDc[rowF].pack(fill='both')

		# Label(self.frameDc[0])
		Label(self.frameDc[0],text=self.Dado_config.idioma(152),font=("Courier", 22)).pack(fill=X)
		Label(self.frameDc[1],text=self.Dado_config.idioma(61)).pack(side='left',fill=X)
		self.txtsigla = Entry(self.frameDc[1],width=47)
		self.txtsigla.pack(side='right')
		Label(self.frameDc[2],text=self.Dado_config.idioma(63),relief='groove').pack(side='left')
		vcmd = (self.register(self.uti.onValidatesigla),'%S', '%s','%d',2,4)
		self.txtlat1 = Entry(self.frameDc[2],width=8,validate="key",validatecommand=vcmd)
		self.txtlat1.pack(side='left',fill=X,expand=True)

		self.txtlat2 = Entry(self.frameDc[2],width=8,validate="key",validatecommand=vcmd)
		self.txtlat2.pack(side='left',fill=X,expand=True)
		Label(self.frameDc[2],text=self.Dado_config.idioma(62),relief='groove').pack(side='left')
		self.txtlong1 = Entry(self.frameDc[2],width=8,validate="key",validatecommand=vcmd)
		self.txtlong1.pack(side='left',fill=X,expand=True)
		self.txtlong2 = Entry(self.frameDc[2],width=8,validate="key",validatecommand=vcmd)
		self.txtlong2.pack(side='left',fill=X,expand=True)
		self.btncadastrar = Button(self.frameDc[3],text=self.Dado_config.idioma(152),command=self.Inseriritem)
		self.btncadastrar.pack(fill=X)
		self.windowCad.bind('<Return>', self.Inseriritem)
		self.windowCad.resizable(False, False)
		self.windowCad.grab_set()
		# self.windowCad.focus()
		self.windowCad.lift()
		self.txtsigla.focus()
		# self.windowCad.mainloop()
		# Label(self.frameDc[2],text="Latitude").pack(side='left',fill=X)
	def AtualizaArqLoc(self):
		New_loc = []
		for items in self.grade.get_children():
			Newtmp_loc = self.grade.item(items)['values']
			New_loc.append("%s\t%s\t%s\t\n" % (Newtmp_loc[0],Newtmp_loc[1],Newtmp_loc[2]))
		try:
			with open((('%s/LOCS.dat')%(os.path.expanduser('~/Documents/UTECDA'))) , 'w',encoding='utf-8') as arquivoLOC:
				arquivoLOC.writelines(New_loc)    
				arquivoLOC.close()
		except IOError:
			messagebox.showerror(self.Dado_config.idioma(49),self.Dado_config.idioma(153),parent=self)
		except PermissionError:
			messagebox.showerror(self.Dado_config.idioma(49),self.Dado_config.idioma(95),parent=self)
	def Delitem(self,*e):
		if len(self.grade.selection()) == 0:
			messagebox.showinfo(self.Dado_config.idioma(145),self.Dado_config.idioma(158),parent=self)
		else:
			if messagebox.askokcancel(self.Dado_config.idioma(66),self.Dado_config.idioma(155),parent=self):		
				for selec in self.grade.selection():
					self.grade.delete(selec)
				self.AtualizaArqLoc()		
				self.contLOC()
				messagebox.showinfo(self.Dado_config.idioma(68),self.Dado_config.idioma(156),parent=self)
	def Inseriritem(self,*event):
		if not self.txtsigla.get() or not self.txtlat1.get() or not self.txtlat2.get() or not self.txtlong1.get()  or not self.txtlong1.get():
			messagebox.showerror(self.Dado_config.idioma(68),self.Dado_config.idioma(70) ,parent=self)
		# elif self.txtlat1.get()  self.txtlat2.get() self.txtlong1.get() self.txtlong1.get() :
		else:
			self.grade.insert('','end',values=(self.txtsigla.get().upper().strip(),self.txtlat1.get()+' '+self.txtlat2.get(),self.txtlong1.get()+' '+self.txtlong2.get()))	
			self.uti.treeview_sort_column(self.grade, self.Dado_config.idioma(61), False)
			self.AtualizaArqLoc()
			self.txtsigla.delete(0, 'end')
			self.txtlat1.delete(0, 'end')
			self.txtlat2.delete(0, 'end')
			self.txtlong1.delete(0, 'end')
			self.txtlong2.delete(0, 'end')
			self.txtsigla.focus()
			messagebox.showinfo(self.Dado_config.idioma(68), self.Dado_config.idioma(153),parent=self)




	def Edititem(self,*a):
		curItem = self.grade.focus()
		if len(self.grade.selection()) == 0:
			messagebox.showinfo(self.Dado_config.idioma(145),self.Dado_config.idioma(158),parent=self)
		else:		
			if curItem and len(self.grade.selection()) == 1:
				dadosEDIT = self.grade.item(curItem)['values']
				self.windowEdit = Toplevel()
				self.frameEd = []
				for rowEd in range(4):
					self.frameEd.append(Frame(self.windowEdit,bd=3,bg='gray',relief=GROOVE))
					self.frameEd[rowEd].pack(fill='both')
					# self.frameEd[rowEd].grid(column=0,row=rowEd+1,sticky=W+E)
				
				Label(self.frameEd[0],text=self.Dado_config.idioma(151),font=("Courier", 22)).pack(fill=X)

				
				Label(self.frameEd[1],text=self.Dado_config.idioma(61),relief='groove').pack(side='left')
				self.txtsiglaEDIT = Entry(self.frameEd[1],font=(10))
				self.txtsiglaEDIT.insert(0,dadosEDIT[0].strip())
				self.txtsiglaEDIT.pack(fill='x',expand=True,side='left')

				vcmd = (self.register(self.uti.onValidatesigla),'%S', '%s','%d','',4)
				Label(self.frameEd[2],text=self.Dado_config.idioma(63),relief='groove').pack(side='left')
				self.txtlat1EDIT = Entry(self.frameEd[2],width=5,validate="key",validatecommand=vcmd)
				self.txtlat1EDIT.insert(0,dadosEDIT[1].split(' ')[0].strip())
				self.txtlat1EDIT.pack(side='left')
				self.txtlat2EDIT = Entry(self.frameEd[2],width=5,validate="key",validatecommand=vcmd)
				self.txtlat2EDIT.insert(0,dadosEDIT[1].split(' ')[1].strip())		
				self.txtlat2EDIT.pack(side='left')
				Label(self.frameEd[2],text=self.Dado_config.idioma(62),relief='groove').pack(side='left')
				# vcmd = (self.register(self.uti.onValidatesigla),'%S', '%s','%d',2,4)
				self.txtlong1EDIT = Entry(self.frameEd[2],width=5,validate="key",validatecommand=vcmd)
				self.txtlong1EDIT.insert(0,dadosEDIT[2].split(' ')[0].strip())
				self.txtlong1EDIT.pack(side='left')
				self.txtlong2EDIT = Entry(self.frameEd[2],width=5,validate="key",validatecommand=vcmd)
				self.txtlong2EDIT.insert(0,dadosEDIT[2].split(' ')[1].strip())
				self.txtlong2EDIT.pack(side='left')
				self.btncadastrarEDIT = Button(self.frameEd[3],text=self.Dado_config.idioma(151), command = self.Editaritem)
				self.btncadastrarEDIT.pack(fill=X)
				self.windowEdit.bind('<Return>', self.Editaritem)
				
				self.windowEdit.iconbitmap(self.uti.resource_path('icone.ico'))
				#self.windowEdit.wait_visibility(master)
				self.windowEdit.resizable(False, False)
				self.windowEdit.grab_set()
				# self.windowEdit.focus()
				self.windowEdit.lift()
				self.txtsiglaEDIT.focus()

				# self.windowEdit.mainloop()
			else:
				messagebox.showinfo(self.Dado_config.idioma(145),self.Dado_config.idioma(159),parent=self)

	def Editaritem(self,*event):
		selected_item = self.grade.selection()[0] 
		self.grade.item(selected_item, values=(self.txtsiglaEDIT.get().upper().strip(),self.txtlat1EDIT.get().strip()+' '+self.txtlat2EDIT.get().strip(),self.txtlong1EDIT.get().strip()+' '+self.txtlong2EDIT.get().strip()))
		self.windowEdit.destroy()
		self.AtualizaArqLoc()
		self.contLOC()	
	def Unselect(self,*event):
	#---Warning ----CurSelection não exlcuida...
		if len(self.grade.selection()) > 0:
			self.grade.selection_remove(self.grade.selection())

	# def teste(self,event):
		# print(self.geometry())
def askLOC(master=None,cbg = None):
	value = CadMap(master,cbg)
	# value.wait_window(value)
	return value.get_lista_loc()
	

if __name__ == "__main__":
	root = Tk()
	teste = askLOC(root)
	teste.mainloop()