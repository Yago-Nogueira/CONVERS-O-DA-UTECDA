import shutil
import urllib.request as request
from contextlib import closing

class DownloadOBS():
	""" Clase para download dos arquivos no formato rinex da unvaco """
	def __init__(self, initano, initdias, initestacoes, initdirobs):
		""" 
			initano = ano (int)
			initdias = lsita com os dias DOY (list)(int)
			initestacoes = lista com as siglas das estações (list)(str)

		"""
		self.__anoDADOS = initano
		self.__diasDADOS = initdias
		self.__estacoesDADOS = initestacoes
		self.__diretorioOBS = initdirobs

	def __get__anoDADOS(self):
		return self.__anoDADOS

	def __get__diasDADOS(self):
		return self.__diasDADOS

	def __get__estacoesDADOS(self):
		return self.__estacoesDADOS

	def __get__diretorioOBS(self):
		return self.__diretorioOBS

	def __getOBS(self):
		for dia in self.__diasDADOS:
			for estacoes in self.__estacoesDADOS:
				rinex = "ftp://geoftp.ibge.gov.br/informacoes_sobre_posicionamento_geodesico/rbmc/dados"
				url_n = "%s/%i/%0.2i/%s%0.2i1.zip"%(rinex,self.__anoDADOS,dia,estacoes.lower(),dia)
				url_d = "%s/%i/%0.2i/%s%0.2i1.zip"%(rinex,self.__anoDADOS,dia,estacoes.lower(),dia)
				url_o = "%s/%i/%0.2i/%s%0.2i1.zip"%(rinex,self.__anoDADOS,dia,estacoes.lower(),dia)

				# rinex = "ftp://data-out.unavco.org/pub/rinex"
				# url_n = "%s/nav/%i/%i/%s%i0.15n.Z"%(rinex,self.__anoDADOS,dia,estacoes.lower(),dia)
				# url_d = "%s/obs/%i/%i/%s%i0.15d.Z"%(rinex,self.__anoDADOS,dia,estacoes.lower(),dia)
				# url_o = "%s/obs/%i/%i/%s%i0.15o.Z"%(rinex,self.__anoDADOS,dia,estacoes.lower(),dia)
				
				# print("Loading…\n█▒▒▒▒▒▒▒▒▒\n10%\n███▒▒▒▒▒▒▒\n30%\n█████▒▒▒▒▒\n50%\n███████▒▒▒\n100%\n██████████\n")
				
				print("Baixando… %s DOY: %d\n\n\n█▒▒▒▒▒▒▒▒▒\n"%(estacoes,dia))
				
				try:
					with closing(request.urlopen(url_d)) as r_d:
						with open(("%s//%s"%(self.__diretorioOBS,url_d[-14:])), 'wb') as f_d:
							shutil.copyfileobj(r_d, f_d)
				except Exception as e:
					print("Erro no: ",url_d)
					print(e)		

				print("█████▒▒▒▒▒  .D\n")
				
				try:
					with closing(request.urlopen(url_n)) as r_n:
						with open(("%s//%s"%(self.__diretorioOBS,url_n[-14:])), 'wb') as f_n:
							shutil.copyfileobj(r_n, f_n)
				except Exception as e:
					print("Erro no: ",url_n)
					print(e)

				print("███████▒▒▒  .N")

				try:
					with closing(request.urlopen(url_o)) as r_o:
						with open(("%s\\%s"%(self.__diretorioOBS,url_o[-14:])), 'wb') as f_o:
							shutil.copyfileobj(r_o, f_o)
				except Exception as e:
					print("Erro no: ",url_o)
					print(e)
				
				print("██████████  .O ")


		# print("método fortemente privado")




# est = ['shis','nege','mtdk','hrao','dakr','ykro','nklg','sutm']
# est = ['shis','nege']
est = ['alar','peaf']
# dias = [182,183,184,190,191]
dias = [182]
teste = DownloadOBS(initano=2015, initdias=dias, initestacoes=est, initdirobs=r"C:\Users\Mateus_Pillat\Desktop\Nova pasta")



# quit()
teste._DownloadOBS__getOBS()
# teste._DownloadOBS__primeiroMetodoFrotementePrivado()

# print(teste._DownloadOBS__anoDADOS)
