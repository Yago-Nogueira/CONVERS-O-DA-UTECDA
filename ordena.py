


from pyqt_utils.filedialog import askdirectory  
from pyqt_utils import messagebox,ttk, Toplevel
from util import Utilitarios, DadoIdioma
# PyQt6 imports handled explicitly
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox, QFileDialog
import datetime
import shutil
import os
class Ordena(QDialog):
	def __init__(self,root):
		Toplevel.__init__(self,root)
		self.geometry("300x220")
		self.uti = Utilitarios()
		self.Dado_config = DadoIdioma()
		self.filenamedestino = None
		self.filename = None
		self.execc = False
		self.frame = Frame(self, bd=3, highlightbackground ="red" , width=200, height=200 , relief=SUNKEN)
		self.frame.pack( fill=X, side = TOP )
		self.frameb = Frame(self,bd=3, highlightbackground ="red" , width=200, height=200 , relief=SUNKEN)
		self.btnselect = Button(self.frame, text=self.Dado_config.idioma(18))
		self.btnselect.pack()
		self.framec = Frame(self,bd=3,width=200, height=200 , relief=SUNKEN )
		self.framec.pack(fill=X)
		self.btnselectdest = Button(self.framec, text=self.Dado_config.idioma(43)) 
		self.btnselectdest.pack()
		self.lbldestino = Label(self.framec, text="")
		self.lbldestino.pack()
		self.btnorganizar = Button(self, text=self.Dado_config.idioma(44), command=self.organizar)
		self.btnorganizar.pack(side = "bottom")
		self.frameb.pack( fill=X, side = "bottom" )
		vcmd = (self.register(self.uti.onValidatesigla),'%S', '%s','%d',2,4)
		self.txt = Entry(self.frameb,width=20,validate="key",validatecommand=vcmd)
		self.txt.pack(side = "bottom",fill="y")
		self.lblpasta = Label(self, text="")
		self.lblpasta.pack()
		self.lblcaminho = Label(self.frame, text="")
		self.lblcaminho.pack()
		self.btnselect.bind("<Button-1>",lambda id=1:self.selecionar(self.lblcaminho,self.frame,1))
		self.btnselectdest.bind('<Button-1>',lambda id=0:self.selecionar(self.lbldestino,self.framec,0))
		self.lbl = Label(self.frameb, text=self.Dado_config.idioma(45))
		self.lbl.pack()
		self.title(self.Dado_config.idioma(46))
		self.resizable(False, False)
		
		self.protocol("WM_DELETE_WINDOW",lambda parent=root: self.fechamento(parent))
		self.focus_force()
		

	def fechamento(self,root):
		if self.execc == True:
			if messagebox.askokcancel(self.Dado_config.idioma(47),self.Dado_config.idioma(48),parent=self):	 
				self.uti.troca(root,self)
		else:
			self.uti.troca(root,self)

	def mes(self,dia,ano):
		data = int(str(datetime.date(ano, 1, 1) + datetime.timedelta(dia - 1))[5:7])
		return "%.2i"%(data)
	def selecionar(self,lblcaminho,frame,id):
		file = askdirectory(initialdir = "C:/",title = self.Dado_config.idioma(39),parent=self)
		lblcaminho.configure(text=file)
		if file.strip() != "": 
			frame.configure(bg="gray")
		else: 
			frame.configure(bg='SystemButtonFace')
		if id == 1:
			self.filename = file
		elif id == 0:
			self.filenamedestino = file

	def organizar(self):
		
		self.execc = True
		ye = self.txt.get()
		
		if self.filenamedestino != None and self.filenamedestino != "" and self.filename != None and self.filename != "" and len(ye) == 4 :
			self.btnselect.config(state="disabled")
			self.btnselectdest.config(state="disabled")				
			self.btnorganizar.config(state="disabled")
			self.txt.config(state="disabled")
			caminhos = [os.path.join(self.filename, nome) for nome in os.listdir(self.filename)]
			self.configure(cursor = "watch")
			contfiles=0
			barra =""
			for o in range(len(caminhos)):
				try:
					arquivos = os.listdir(caminhos[o])
					self.lblpasta.configure(text =caminhos[o] + " Nº:" + str(len(arquivos)))
					self.lblpasta.update_idletasks()
					for i in arquivos :
						if not self.filenamedestino.lower().endswith('/') :
							barra = '/'
						destino = self.filenamedestino + barra + "GPS/"+ye+"/"
						if i.lower().endswith(".zip") or i.lower().endswith(".z"):
							
							final =  destino + self.mes(int(i[4:7]),int(ye)) + "/" + i[:4]
							if(os.path.exists(final) == False):
								os.makedirs(final)
							local = caminhos[o] + "/" + i
							shutil.copy(local,final)
							self.update()
					contfiles+=1
				except (NotADirectoryError,PermissionError):
					messagebox.showerror(self.Dado_config.idioma(49),self.Dado_config.idioma(50),parent=self)
					break
				except IOError:
					messagebox.showerror(self.Dado_config.idioma(49),self.Dado_config.idioma(165),parent=self)
					break
				except Exception:
					break



			self.configure(cursor = "arrow") 
			self.lblpasta.configure(text = "%s%d" %(self.Dado_config.idioma(51),contfiles))
		else:
			messagebox.showerror(self.Dado_config.idioma(49),self.Dado_config.idioma(52),parent=self)
		
			
		
			
		self.btnselect.config(state='normal')
		self.btnselectdest.config(state='normal')
		self.btnorganizar.config(state='normal')
		self.txt.config(state='normal')	
		self.execc = False
		
			


if __name__ == "__main__":
	root = Tk()
	teste = Ordena(root)
	
	root.mainloop()