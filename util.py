#!/usr/bin/env python
# -*- coding: utf-8 -*-
from matplotlib.backend_bases import NavigationToolbar2 as NavigationToolbar
from geopy.geocoders import Nominatim
from PyQt6.QtWidgets import QMessageBox, QWidget, QVBoxLayout, QScrollArea, QFrame, QLabel
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont
from scipy import interpolate
from bs4 import BeautifulSoup
from typing import Union      
import numpy as np
import screeninfo
import threading
import traceback
import datetime
import requests
import psutil
import math
import igrf
import sys
import os


class thread_with_trace(threading.Thread): 
    def __init__(self, *args, **keywords): 
        threading.Thread.__init__(self, *args, **keywords) 
        self.killed = False

    def start(self): 
        self.__run_backup = self.run 
        self.run = self.__run	 
        threading.Thread.start(self) 

    def __run(self): 
        sys.settrace(self.globaltrace) 
        self.__run_backup() 
        self.run = self.__run_backup 
    def globaltrace(self, frame, event, arg): 
        if event == 'call':return self.localtrace 
        else:return None

    def localtrace(self, frame, event, arg): 
        if self.killed: 
            if event == 'line':raise SystemExit() 
            return self.localtrace 

    def kill(self):self.killed = True

class TopNavigationToolbar(NavigationToolbar):
   def __init__(self, canvas, window):
      super().__init__(canvas, window, pack_toolbar=False)

   def _Button(self, text, image_file, toggle, command):
      return super()._Button(text, image_file, toggle, command)

   # override _Spacer() to create vertical separator
#    def _Spacer(self):
#       s = Frame(self, width=26, relief="ridge", bg="DarkGray", padx=2)
#       s.pack(side="left", pady=5)
#       return s

   # disable showing mouse position in toolbar
   def set_message(self, s):
      pass
class VerticalScrolledFrame(QWidget):
    def __init__(self, parent=None, *args, **kw):
        super().__init__(parent)
        
        vscrollbar = QScrollArea()
        vscrollbar.setWidgetResizable(True)
        
        self.interior = QFrame(vscrollbar)
        vscrollbar.setWidget(self.interior)
        
        layout = QVBoxLayout(self)
        layout.addWidget(vscrollbar)
        self.setLayout(layout)


class DadoIdioma(object):
    def __init__(self):
        self.Settings = {}
        try:
            with open((('%s/Settings.cfg')%(os.path.expanduser('~/UTECDA'))) , 'r',encoding="UTF-8") as conf:
                interfaces = conf.read().split("[=]");interfaces.pop(0)
                for interface in interfaces:
                    propriedades = list(filter(None, interface.split("\n")))
                    indice = propriedades[0].replace("[","").replace("]","")
                    self.Settings[indice] = {}
                    for propriedade in propriedades[1:]:
                        ind,prop = propriedade.split("=")
                        ind = ind.replace(" ","")
                        prop = prop.strip()
                        if prop == "None":self.Settings[indice][ind]=None
                        elif ind[0] == "s":self.Settings[indice][ind]=prop  
                        elif ind[0] == "i":self.Settings[indice][ind]=int(prop)  
                        elif ind[0] == "f":self.Settings[indice][ind]=float(prop)
                        elif ind[0] == "l":
                            prop = prop.replace("'", "").replace(",", "").replace("[", "").replace("]", "")
                            self.Settings[indice][ind]=prop.split(" ")
            # print(self.Settings)
            if not self.Settings:raise ValueError
        except (IOError,IndexError,ValueError,PermissionError) as e:
            print(e)
            ####################################
            #  alterar para gerar executavel   #
            ####################################
            self.Settings={'INTERFACE': {'iLanguage': 0, 'sDir_DATA': 'C:/Users/mateu/Desktop/DADOS_TEC_PARA_TESTE', 'sMap': 'AMERICAS', 'iFiltro': 1}, 'MAPAS': {'lNameMAP': ['All', 'Brasil', 'Africa', 'EURO-ORIENTE-AFRICA', 'AMERICAS', 'MAP'], 'lLocs': ['-180.0', '180.0', '-90.0', '90.0', '-77.0', '-32.0', '-35.0', '7.0', '-24.98168994304885', '54.25017875206461', '-38.87683109480383', '50.998124439951766', '-23.248291005001192', '75.47732833130513', '-49.78743598787921', '82.27134944692196', '-168.47049235130987', '-12.208006692123917', '-90.0', '83.96985472582617', '-168.4704923513099', '-12.208006692123917', '-90.0', '88.28697257974105']}, 'INDIVIDUAL': {'sFamily': 'Arial', 'sWeight': 'bold', 'fSize': 18.0, 'sTitle_X': 'Dias', 'sTitle_Y': 'Hora(UT)', 'sTitle_B': 'VTEC', 'fValueMax_B_VTEC': 30.0, 'fValueMin_B_VTEC': 0.0, 'iTicksCbar_VTEC': 10, 'iDivTicks_VTEC': 4, 'fSizeLabelsTick_X': 25.9, 'fWidthTickMajor_X': 2.0, 'fHeightTickMajor_X': 10.0, 'fWidthTickMinor_X': 2.0, 'fHeightTickMinor_X': 5.0, 'fSizeLabelsTick_Y': 23.0, 'fWidthTickMajor_Y': 2.0, 'fHeightTickMajor_Y': 10.0, 'fWidthTickMinor_Y': 2.0, 'fHeightTickMinor_Y': 5.0, 'fTop': 1.0, 'fBottom': 0.005, 'fLeft': 0.258, 'fRight': 0.757, 'fHspace': 0.0, 'fWspace': 0.0, 'fSize_inches_fig_width': 14.4, 'fSize_inches_fig_height': 8.05}, 'EIA': {'sFamily': 'Arial', 'sWeight': 'bold', 'fSize': 18.0, 'sTitle_X': 'Hora', 'sTitle_Y_DIP': 'DIP LATITUDE', 'sTitle_Y_LATITUDE': 'LATITUDE', 'sTitle_B': 'VTEC', 'fValueMax_B_VTEC': 28.0, 'fValueMin_B_VTEC': 0.0, 'iTicksCbar_VTEC': 10, 'iDivTicks_VTEC': 4, 'fSizeLabelsTick_X': 23.0, 'fWidthTickMajor_X': 2.0, 'fHeightTickMajor_X': 10.0, 'fWidthTickMinor_X': 2.0, 'fHeightTickMinor_X': 5.0, 'fSizeLabelsTick_Y': 23.0, 'fWidthTickMajor_Y': 2.0, 'fHeightTickMajor_Y': 10.0, 'fWidthTickMinor_Y': 2.0, 'fHeightTickMinor_Y': 5.0, 'fTop': 1.0, 'fBottom': 0.005, 'fLeft': 0.258, 'fRight': 0.757, 'fHspace': 0.0, 'fWspace': 0.0, 'fSize_inches_fig_width': 14.4, 'fSize_inches_fig_height': 8.05}, 'MAPA': {'sFamily': 'Arial', 'sWeight': 'bold', 'fSize': 18.0, 'sTitle_B_VTEC': 'VTEC', 'fValueMax_B_VTEC': 50.0, 'fValueMin_B_VTEC': 0.0, 'iTicksCbar_VTEC': 10, 'iDivTicks_VTEC': 4, 'sTitle_B_ROT': 'ROT', 'fValueMax_B_ROT': 0.13, 'fValueMin_B_ROT': -0.25, 'iTicksCbar_ROT': 6, 'iDivTicks_ROT': 10, 'fValueDelta_ROT': 60.0, 'sTitle_B_ROTI': 'ROTI', 'fValueMax_B_ROTI': 1.0, 'fValueMin_B_ROTI': 0.0, 'iTicksCbar_ROTI': 10, 'iDivTicks_ROTI': 4, 'fValueDelta_ROTI': 300.0, 'fElevation_Filter': 30.0, 'fTop': 0.9690476190476192, 'fBottom': 0.005, 'fLeft': 0.2571428571428572, 'fRight': 0.8404761904761904, 'fHspace': 0.0, 'fWspace': 0.0, 'fSize_inches_fig_width': 14.4, 'fSize_inches_fig_height': 8.05}, 'DESVIO': {'sFamily': 'Arial', 'sWeight': 'bold', 'fSize': 18.0, 'sTitle_X': 'UT', 'sTitle_Y': 'VTEC', 'fValueMax_B_VTEC': 28.0, 'fValueMin_B_VTEC': 0.0, 'fSizeLabelsTick_X': 23.0, 'fWidthTickMajor_X': 2.0, 'fHeightTickMajor_X': 10.0, 'fWidthTickMinor_X': 2.0, 'fHeightTickMinor_X': 5.0, 'fSizeLabelsTick_Y': 23.0, 'fWidthTickMajor_Y': 2.0, 'fHeightTickMajor_Y': 10.0, 'fWidthTickMinor_Y': 2.0, 'fHeightTickMinor_Y': 5.0, 'fTop': 1.0, 'fBottom': 0.005, 'fLeft': 0.258, 'fRight': 0.757, 'fHspace': 0.0, 'fWspace': 0.0, 'fSize_inches_fig_width': 14.4, 'fSize_inches_fig_height': 8.05}, 'PAINEL MAPA': {'sFamily': 'Arial', 'sWeight': 'bold', 'fSize': 18.0, 'sTitle_B_VTEC': 'VTEC', 'fValueMax_B_VTEC': 30.0, 'fValueMin_B_VTEC': 0.0, 'iTicksCbar_VTEC': 10, 'iDivTicks_VTEC': 4, 'sTitle_B_ROT': 'ROT', 'fValueMax_B_ROT': 0.13, 'fValueMin_B_ROT': -0.25, 'iTicksCbar_ROT': 6, 'iDivTicks_ROT': 10, 'fValueDelta_ROT': 60.0, 'sTitle_B_ROTI': 'ROTI', 'fValueMax_B_ROTI': 1.0, 'fValueMin_B_ROTI': 0.0, 'iTicksCbar_ROTI': 10, 'iDivTicks_ROTI': 4, 'fValueDelta_ROTI': 300.0, 'fElevation_Filter': 30.0, 'fTop': 0.9857142857142858, 'fBottom': 0.00952380952380949, 'fLeft': 0.15714285714285714, 'fRight': 0.7238095238095239, 'fHspace': 0.0, 'fWspace': 0.0, 'fSize_inches_fig_width': 14.4, 'fSize_inches_fig_height': 8.05}, 'ROT': {'sFamily': 'Arial', 'sWeight': 'bold', 'fSize': 18.0, 'fElevation_Filter': 30.0, 'fValueDelta_ROT': 60.0,'fValueDelta_ROTI': 300.0, 'fValueMultFactor_ROT': 1.0, 'sTitle_X': 'UT', 'sTitle_Y': 'ROT (PRN)', 'fSizeLabelsTick_X': 23.0, 'fWidthTickMajor_X': 2.0, 'fHeightTickMajor_X': 10.0, 'fWidthTickMinor_X': 2.0, 'fHeightTickMinor_X': 5.0, 'fSizeLabelsTick_Y': 23.0, 'fWidthTickMajor_Y': 2.0, 'fHeightTickMajor_Y': 10.0, 'fWidthTickMinor_Y': 2.0, 'fHeightTickMinor_Y': 5.0, 'fTop': 1.0, 'fBottom': 0.005, 'fLeft': 0.258, 'fRight': 0.757, 'fHspace': 0.0, 'fWspace': 0.0, 'fSize_inches_fig_width': 14.4, 'fSize_inches_fig_height': 8.05}}
            
            
            if not os.path.exists(os.path.expanduser('~/UTECDA')):os.mkdir(os.path.expanduser('~/UTECDA'))
            Utilitarios().setSETTING(self.Settings)
    
    def set_font_Settings(self,interface,dic_font):
        self.Settings[interface]["sFamily"] = dic_font["family"]
        self.Settings[interface]["sWeight"] = dic_font["weight"]
        self.Settings[interface]["fSize"] = float(dic_font["size"])

    def get_font_Settings(self,interface):
        font = {'family' : self.Settings[interface]["sFamily"] , 'weight' : self.Settings[interface]["sWeight"],'size' : self.Settings[interface]["fSize"]}
        return font

    def writeConfig(self):
        newpath = os.path.expanduser('~/UTECDA')
        if not os.path.exists(newpath):os.mkdir(newpath)
        with open((('%s/Settings.cfg')%(newpath)) , 'w+',encoding="UTF-8") as conf:
            for interface in self.Settings:
                conf.write("[=]\n[%s]\n"%interface)
                for propriedades in self.Settings[interface]:
                    if not propriedades[-4:] == "temp":conf.write("%s = %s\n"%(propriedades,str(self.Settings[interface][propriedades])))         

    def idioma(self,pos,*arg):
        ling = self.Settings["INTERFACE"]["iLanguage"]
        matriz_ling=[
            ["pt-BR","en-US"],
            ["Matriz","Matrix"],
            ["Individual","Individual"],
            ["Contorno","Contour"],
            ["Ordena"," Sort"],
            ["IGRF","IGRF"],
            ["Registro de estações","Station registration"],
            ["Gráfico","Graph"],
            ["Ferramentas","Tools"],
            ["Português","Portuguese"],
            ["Inglês","English"],
            ["Idioma","Language"],
            ["Programas","Programs"],
            ["Configurações","Settings"],
            ["Licença incompativel","Incompatible license"],
            ["CRIAR SOLICITAÇÃO DE LICENÇA","CREATE LICENSE REQUEST"],
            ["UTECDA - Univap Conteúdo Eletronico Total Analise de Dados - Projetos FAPESP: 2016/22634-0 & 2017/21741-0","Univap Total Electron Content Data Analysis - FAPESP Project: 2016/22634-0 & 2017/21741-0"],
            ["Propriedades","Properties"],
            ["Escolher Diretório","Choose Directory"],
            ["Min X","Min X"],
            ["Max X","Max X"],
            ["Min Y","Min Y"],
            ["Max Y","Max Y"],
            ["Max (VTEC)","Max (VTEC)"],
            ["Grade","Grid"],
            ["Salvar PNG","Save PNG"],
            ["Ajustar Gráfico","Adjust Graph"],
            ["PROPRIEDADES","PROPERTIES"],
            ["Passo X","Step X"],
            ["Passo ","Step "],
            ["Nº de Rótulos X","Num Of Labels X"],
            ["Nº de Rótulos ","Num Of Labels "],
            ["Título (Eixo X)","Title (Axis X)"],
            ["Título (Eixo Y)","Title (Axis Y)"],
            ["Título (Gráfico)","Title (Graph)"],
            ["Título (Barra de cores)","Title (Colorbar)"],
            ["FONTE","FONT"],
            ["Escolher Fonte","Choose Font"],
            ["Distribuição TEC","TEC Distribution"],
            ["ESCOLHER DIRETÓRIO","CHOOSE DIRECTORY"],
            ["Dia","Day"],
            ["Hora (UT)","Hour (UT)"],
            ["Ordena","Sort"],
            ["Escolher Diretório Destino","Choose Destination Directory"],
            ["Organizar","Organize"],
            ["Digite o ano","Enter year"],
            ["Ordenar Dados","Sort Data"],
            ["Programa em execução","Running program"],
            ["Deseja abandonar o processo?","Do you want to abandon the process?"],
            ["Erro","Error"],
            ["Verifique se o DIRETÓRIO encontram-se os pastas com arquivos(.zip)","Verify that the DIRECTORY are folders with files (.zip)"],
            ["Processo Concluído Pastas: ","Process Completed Folders: "],
            ["Verifique o formato do ANO (9999) e os DIRETÓRIOS","Check YEAR format (9999) and DIRECTORY"],
            ["Data Inicial","Initial Date"],
            ["Data Final","Final Date"],
            ["Arquivo OBS.dat ausente","File OBS.dat absent"],
            ["Ficha de Estações","Stations Sheet"],
            ["Cadastro de Estações","Station Registration"],
            ["Adicionar Estação","Add Station"],
            ["Cidade","City"],
            ["UF","UF"],
            ["Sigla","Initials"],
            ["Longitude","Longitude"],
            ["Latitude","Latitude"],
            ["Estações: ","Stations: "],
            ["Cadastrar Estação","Register Station"],
            ["Exclusão de item","Item Deletion"],
            ["Deseja realmente excluir as estações selecionadas?","Do you really want to delete the selected stations?"],
            ["Ação concluída","Action completed"],
            ["Estação deletado com sucesso","Successfully deleted Station"],
            ["Preencha todos os dados","Fill in all the data"],
            ["Estação cadastrado com sucesso","Station successfully registered"],
            ["Editar Estação","Edit Station"],
            ["Alterar","Change"],
            ["Gerador de chave","Key generator"],
            ["Abrir","Open"],
            ["Escolher Destino","Choose destination"],
            ["Destino da chave","Destination of the key"],
            ["Gerar Chave","Generate Key"],
            ["ARQUIVO INVÁLIDO","INVALID FILE"],
            ["Chave cadastrada","Registered Key"],
            ["Chave salva em: ","Key saved in: "],
            ["Gerador de chave","Key generator"],
            ["Calculo da Inclinação Magnética e Dip Latitude","Magnetic Inclination and Latitude Dip Calculator"],
            ["Inclinação magnética","Magnetic slope"],
            ["ANO","YEAR"],
            ["Altitude (Km)","Altitude (Km)"],
            ["Gerar","Generate"],
            ["Inclinação","Inclination"],
            ["Arquivo salvo em: ","File saved in: "],
            ["Salvar","To save"],
            ["Salvar Matriz","Save Matrix"],
            ["Divisão por zero","division by zero"],
            ["Formatos Incorretos","Incorrect Formats"],
            ["Não foram encontrados dados neste periodo \n e estação selecionados","No data were found\n for this selected period and station"],
            ["Acesso ao diretório foi negado","Directory access denied"],
            ["Gerar pedido de licença","Generate License Request"],
            ["Licença","License"],
            ["Nome","Name"],
            ["Instituição","Institution"],
            ["Pedido de licença gerado com sucesso","Successfully generated license request"],
            ["Posição","Position"],
            ["ALEM EIA","ALEM EIA"],
            ["EQ","EQ"],
            ["BLS","LLS"],
            ["BLN","LLN"],
            ["Insira ano e latitude","Enter year and latitude"],
            ["Dia para visualização","Day to view"],
            ["Plotar","Plot"],
            ["Estações","Station"],
            ["Add gráfico para .mp4","add graphic to movie"],
            ["Gerar vídeo","Generate video"],
            ["Deletar ultimo gráfico da seleção","Delete last selection graph"],
            ["Limpar seleção","Clear selection"],
            ["Criação de vídeo","Video Creation"],
            ["Tamanho LabelsTick X e Y","Size LabelTick X and Y"],
            ["Largura Tick X e Y (Major)","Width Tick X and Y (Major)"],
            ["Altura Tick X e Y (Major)","Height Tick X and Y (Major)"],
            ["Largura Tick X e Y (Minor)","Width Tick X and Y (Minor)"],
            ["Altura Tick X e Y (Minor)","Height Tick X and Y (Minor)"],
            ["Eixo Y","Axis Y"],
            ["Sem dados...","No data..."],
            ["Setor","Sector"],
            ["Dias calmos","Calm days"],
            ["Período pertubado","Disturbed period"],
            ["Desvio","Detour"],
            ["Primeiramente escolha um diretório com os arquivos (.STD)","First choose a directory with the files (.STD)"],
            ["Escolha uma estação da lista","Choose a station from the list"],
            ["Escolha os dias calmos para a visualização","Choose calm days for viewing"],
            ["Escolha mais de uma estação para a visualização","Choose more than one station for viewing "],
            ["Formato dia","Day Format"],
            ["Data","Date"],
            ["Mínimo Y","Maximun Y"],
            ["Máximo Y","Minimun Y"],
            ["Legenda","Legend"],
            ["Dia / Mês","Day / Month"],
            ["Sub Plots","Sub Plots"],
            ["Setor","Sector"],
            ['Média','Average'],
            ['Inserir grade horizontal','Insert horizontal grid'],
            ['Remover grade horizontal','Remove horizontal grid'],
            ['Inserir grade vertical','Insert vertical grid'],
            ['Remover grade vertical','Remove vertical grid'],
            ['Equador Magnético','Magnetic Equador'],
            ['Não cadastrada','Not registered'],
            ['Atenção','Attention'],
            ['As seguintes estações possuem as mesmas coordenadas geográficas:\n\n','The following stations have the same geographical coordinates:\n\n'],
            ['Para aplicar as alterações o programa sera reiniciado','To apply the changes the program will be restarted'],
            ['Adicionar Mapa','Add Map'],
            ['Registro de Mapas','Map Registration'],
            ['Mapas: ','Maps: '],
            ['Editar mapa','Edit map'],
            ['Cadastrar mapa','Enter map'],
            ['Mapa cadastrado com sucesso','Map registered successfully'],
            ['Arquivo LOC.data ausente','LOC.dat file missing'],
            ['Deseja realmente excluir os mapas selecionadas?','Do you really want to delete the selected maps?'],
            ['Mapa deletado com sucesso','Map deleted successfully'],
            ['Mapa','Map'],
            ['Nenhum mapa selecionado','No map selected'],
            ['É permitida apenas uma edição por vez','Edit one map at a time'],
            ['Deletar','Delete'],
            ['Editar','Edit'],
            ['A seleção para setor ou desvio não podem possuir estações não cadastradas','The selection for sector or detour can not have stations not registered'],
            ['Vazio','Empty'],
            ['Nenhuma estação selecionada','No station selected'],
            ['Não há espaço no disco','No space left on disk '],
            ['Filtro de estações','Station filter'],
            ['Cores PRN','PRN Colors'],
            ['Erro ao acessar o arquivo LOCS.dat','--'],
            ['Título barra de cores','Color bar title'],
            ['TÍTULO','TITLE'],
            ['Desenvolvido por:\nValdir Gil Pillat \n Mateus de Oliveira Arcanjo','Developed by:\n Valdir Gil Pillat \n Mateus de Oliveira Arcanjo'],
            ['Hora de início','Start time'],
            ['Hora final','End time'],
            ['Intervalo (Min)','Interval (Min)'],
            ['Modelo do mapa','Map Template'],
            ['A data inserida não corresponde ao formato %d/%m/%Y','date does not match format %d/%m/%Y'],
            ['Realizando a leitura de todos os dados encontrados (*.CMN) encontrados','Reading all the data (*.CMN) found'],
            ['Realizando o processamento dos dados','Performing data processing the data'],
            ['Iniciando plot das figuras','Starting plot of figures'],
            ['Trabalho finalizado','Work finished'],
            ['Filtro de elevação º','Lifting filter º'],
            ['Mapa','Map'],
            ['Mostrar/Ocultar siglas no mapa','Show/Hide Acronyms on Map'],
            ['Gerar KML','Generate KML'],
            ['Dados','Data'],
            ['Grade (LxC)','Grid (RxC)'],
            ['Multiplicar ROT)','ROT Multiplication'],
            ['Ativar clique-linha vertical','Enable vertical line click'],
            ['Desativar clique-linha vertical','Disable vertical click-line'],
            ['arquivo kml gerado','kml file generated'],
            ['Criar video','Create video'],
            ['Criando video','Creating video'],
            ['Estação não encontrada','station not found'],
            ['Deletar','Delete']

            # ['Erro ao acessar o arquivo LOCS.dat','--']
            # ['Erro ao acessar o arquivo LOCS.dat','--']
        ]
        for objt in arg:
            for x in range(len(matriz_ling)):print(("%s --> pos %i") % ((matriz_ling[x][0]),x))
        try:ret = matriz_ling[pos][ling]
        except IndexError:ret = matriz_ling[pos][0]
        return ret


# class Utilitarios(Frame):
    # def __init__(self, master):
        # super().__init__(master)
        # print(self.master)
        # print(master)
        # print(self)
        
class Utilitarios:

    def get_ip_addresses(self,family):
        for interface, snics in psutil.net_if_addrs().items():
            for snic in snics:
                if snic.family == family:yield (interface, (snic.address, snic.netmask))

    def teste_licença(self):
        ID_macs = list(self.get_ip_addresses(psutil.AF_LINK))
        valkey = []
        idlic = ""
        try:
            with open('license_UTECDA.utc', 'r',encoding="UTF-8") as f:
                tudo=f.read()
                line = tudo[:-1].split("\n")
                valkey = line[25][:-2].split(':')
                for k in range(0,len(valkey),2):valkey[k] = chr(int(int(valkey[k])/2469))
                for k in range(0,len(valkey),2):idlic+=(valkey[k])
                if len(line)!= 51 or len(tudo[:-2].split(':')) != 1734:raise IOError(DadoIdioma().idioma(14))
                else:
                    verify = False
                    for ID_mac in ID_macs:
                        try:
                            if ID_mac[1][0].replace("-",":") == idlic:verify = True
                        except IndexError: pass
                    if not verify: raise IOError(DadoIdioma().idioma(14))
        except (Exception) as  e:raise IOError(DadoIdioma().idioma(14))
    
    def gravar_erro(self,exp):
        erro = open('ERRO.txt','w+')
        erro.write(str(exp)+"\n")
        [erro.write(str(tb)) for tb in  traceback.format_tb(sys.exc_info()[2])]
        erro.close()

    def resource_path(object, relative_path):
        try:base_path = sys._MEIPASS
        except AttributeError:base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def setOBS(self):
        try:
            with open((('%s/OBS.dat')%(os.path.expanduser('~/UTECDA'))) , 'w+',encoding="UTF-8") as conf:
                conf.write(("%s\t%s\t%s\tLAT\tLONG")%(DadoIdioma().idioma(59),DadoIdioma().idioma(60),DadoIdioma().idioma(61)))
                conf.close()
        except (IOError,IndexError,ValueError,PermissionError) as e:self.gravar_erro(e)

    def setSETTING(self, Settings = None):
        with open(( ('%s/Settings.cfg')%(os.path.expanduser('~/UTECDA') )) , 'w+',encoding="UTF-8") as conf:
            for interface in Settings:
                conf.write("[=]\n[%s]\n"%interface)
                for propriedades in Settings[interface]:
                    conf.write("%s = %s\n"%(propriedades,Settings[interface][propriedades]))
      
    def troca(self,abre,fecha,*args):
        abre.deiconify()
        abre.state('zoomed')
        fecha.destroy()
        for objt in args:
            try:objt.close('all')
            except AttributeError:objt.destroy()

    def chunks(self,l, n):
        for i in range(0, len(l), n):yield l[i:i + n]

    def list_duplicates_of(self,seq,item):
        locs = [i for i, x in enumerate(seq) if x == item]
        return locs

    def onValidatesigla(self, S, s, d,char=0,max=None):
        retorno = True
        if d == '1':
            if char == '1':
                if S.isdigit():retorno = False    
            elif char == '2':
                if len(S)>1:
                    for ch in S:
                        if ch != "," and ch != "." and ch != "-":
                            if not ch.isdigit():retorno = False
                else:
                    if S != "," and S != "." and S != "-":
                        if not S.isdigit():retorno = False

            if max != None:
                if len(s) > (int(max)-1):retorno = False
        return retorno

    def treeview_sort_column(self,tv, col, reverse):
        # print(col)
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(reverse=reverse)
        for index, (val, k) in enumerate(l):tv.move(k, '', index)
        tv.heading(col, command=lambda: self.treeview_sort_column(tv, col, not reverse))    


    def up_lista(self,listab):
        try:
            cur_sel = listab.curselection()
            if cur_sel:i = cur_sel[0]
            else:i = -1
            listab.selection_clear(0, "end")
            if i <= 0:i = listab.size()
            listab.see(i - 1)
            listab.select_set(i-1)
        except Exception:
            listab.selection_clear(0, "end")
            i = listab.size()
            listab.see(i - 1)
            listab.select_set(i - 1)
        listab.event_generate('<<ListboxSelect>>')

    def down_lista(self,listab):
        try:
            cur_sel = listab.curselection()
            if cur_sel:i = cur_sel[0]
            else:i = -1
            listab.selection_clear(0, "end")
            if i >= listab.size()-1:i = -1
            listab.see(i + 1)
            listab.select_set(i+1)
        except Exception:
            listab.selection_clear(0, "end")
            listab.see(0)
            listab.select_set(0)
        listab.event_generate('<<ListboxSelect>>')

    def DMDDEC(self, I, M):
        DE = I
        EM = M
        if str(I)[0] == "-":EM = -EM
        X = DE + EM/60.0
        return X
        
    def get_inclinacao(self,Alt,Ano,LTD,LTM,LND,LNM):
        XLT = self.DMDDEC(LTD,LTM)
        XLN = self.DMDDEC(LND,LNM)
        dt = datetime.datetime(Ano,1,1)
        xarray_Resp = igrf.igrf(dt,XLT,XLN,Alt)
        return float(xarray_Resp['incl'])

    def get_inclinacao_D(self,Alt,Ano,XLT,XLN):
        dt = datetime.datetime(Ano,1,1)
        xarray_Resp = igrf.igrf(dt,XLT,XLN,Alt)
        return float(xarray_Resp['incl'])
    
    def center_to_two_monitor(self, window):
        sw = window.width()
        sh = window.height()
        if len(screeninfo.get_monitors()) > 1:
            window.setGeometry(sw, 0, sw, sh)

    def center(self, root, window, width=None, height=None):
        if hasattr(window, 'parent') and window.parent():
            self.center_on_parent(root, window, width, height)
        else:
            self.center_on_screen(window, width, height)
    
    def center_on_screen(self, window, width=None, height=None):
        if not width:
            width = window.width()
        if not height:
            height = window.height()
        x_coordinate = int(window.screen().geometry().width() / 2 - width / 2)
        y_coordinate = int(window.screen().geometry().height() / 2 - height / 2)
        window.setGeometry(x_coordinate, y_coordinate, width, height)

    def center_on_parent(self, root, window, width=None, height=None):
        if not width:
            width = window.width()
        if not height:
            height = window.height()
        parent = root
        x_coordinate = int(parent.x() + (parent.width() / 2 - width / 2))
        y_coordinate = int(parent.y() + (parent.height() / 2 - height / 2))
        window.setGeometry(x_coordinate, y_coordinate, width, height)


    
    # thread_PAINEL_MAPA = thread_with_trace(target = self.GRAFICO_PAINEL_MAPA._set_Matplotlib_grafico_grade_VTEC)
    # thread_PAINEL_MAPA.setDaemon(True)
    # thread_PAINEL_MAPA.start()

    # self.VAR_BARRA_LOADING_GRAFICO_PAINEL_MAPA = DoubleVar(self)
    # self.VAR_BARRA_LOADING_LABEL_GRAFICO_PAINEL_MAPA = StringVar(self)
    # self.VAR_PROCESSO_GRAFICO_PAINEL_MAPA = BooleanVar(self)
    # self.VAR_PROCESSO_GRAFICO_PAINEL_MAPA.set(False)


    def BuscarEstacoes(self, siglas):
        # self.stop_thread_Busca_Siglas = BooleanVar(self)
        # self.VAR_BARRA_LOADING_GRAFICO_Busca_Siglas = DoubleVar(self)
        # self.VAR_BARRA_LOADING_LABEL_GRAFICO_Busca_Siglas = StringVar(self)
        # self.stop_thread_Busca_Siglas.set(False)

        # qtSimpleDialog.Loading(self.master,'Busca Siglas',orient_u = HORIZONTAL,maximum_u = 100,length_u = 500,mode_u = 'determinate',icon=self.resource_path('img\icone.ico'),progress_var = self.VAR_BARRA_LOADING_GRAFICO_Busca_Siglas,info_loading=self.VAR_BARRA_LOADING_LABEL_GRAFICO_Busca_Siglas,uti = self, Dado_config = DadoIdioma(), stop_thread = self.stop_thread_Busca_Siglas, cancelable = False)#, threads = thread_Busca_Siglas)


        # thread_with_trace(function = Progressbar, args = (self, orient='horizontal', mode='determinate', length=100,)).start()


        geolocator = Nominatim(user_agent="geoapiExercises")
        lista_info_estacoes_econtradas = []
        lista_info_estacoes_n_encontradas = []
        lista_info_estacoes_econtradas_OBS = []
        
        coef_loop_siglas = ((100)/(len(siglas)))
        
        # self.VAR_BARRA_LOADING_GRAFICO_Busca_Siglas.set(0)
        # self.VAR_BARRA_LOADING_LABEL_GRAFICO_Busca_Siglas.set("Buscando estações")
        
        for estacao in siglas:
            # self.VAR_BARRA_LOADING_LABEL_GRAFICO_Busca_Siglas.set("Baixando %s"%estacao)

            link = "http://geodesy.unr.edu/NGLStationPages/stations/%s.sta"%estacao
            html = requests.get(link).content
            soup = BeautifulSoup(html, 'html.parser')
            # strcoord = str(soup)
            h4 = soup.find_all("h4")

            if h4:
                Latitude = float((str(h4[0]).split(":")[1].replace(" degrees</h4>","")))
                Longitude = float((str(h4[1]).split(":")[1].replace(" degrees</h4>","")))
                coord = f"{Latitude}, {Longitude}"
                location = geolocator.reverse(coord, exactly_one=True)
                address = location.raw['address']
                
                city = address.get('city', '')
                state = address.get('state', '')
                country = address.get('country', '')

                str_local = ""
                if city:str_local+=city+" - "
                if state:str_local+=state+" - "
                if country:str_local+=state
                if not str_local: str_local = DadoIdioma().idioma(193)
                lista_info_estacoes_econtradas_OBS.append("\n%s\tNG\t%s\t%.3f\t%.3f"%(str_local,estacao,Latitude,Longitude))
                lista_info_estacoes_econtradas.append([estacao,Latitude,Longitude])
                print("%s Encontrada"%estacao)
                # self.VAR_BARRA_LOADING_LABEL_GRAFICO_Busca_Siglas.set("%s Encontrada"%estacao)
            else:
                lista_info_estacoes_n_encontradas.append(estacao)
                # self.VAR_BARRA_LOADING_LABEL_GRAFICO_Busca_Siglas.set("%s Não encontrada"%estacao)
                print("%s Não encontrada"%estacao)

            
            # self.VAR_BARRA_LOADING_GRAFICO_Busca_Siglas.set(self.VAR_BARRA_LOADING_GRAFICO_Busca_Siglas.get() + coef_loop_siglas)
            # self.VAR_BARRA_LOADING_LABEL_GRAFICO_Busca_Siglas.set("Busca concluida")
        
        # self.VAR_BARRA_LOADING_GRAFICO_Busca_Siglas.set(100)
        if lista_info_estacoes_econtradas_OBS:
            try:
                with open((('%s/OBS.dat')%(os.path.expanduser('~/UTECDA'))),'a',encoding='utf-8') as arquivoOBS:
                    for info_linhas in lista_info_estacoes_econtradas_OBS:arquivoOBS.write(info_linhas)
            except(IOError,IndexError) as e:print(e)
        return [lista_info_estacoes_econtradas,lista_info_estacoes_n_encontradas]
            

    def Ler_OBS(self):
        try:
            with open((('%s/OBS.dat')%(os.path.expanduser('~/UTECDA'))),'r',encoding='utf-8') as arquivoOBS:
                line_total = arquivoOBS.readlines()
                del(line_total[0])
                lista_info_estacoes = []
                for station in line_total:
                    station = station.replace("\n","").split('\t')
                    nome_station = station[2]
                    latitude_grau = station[3]
                    longitude_grau = station[4]
                    lista_info_estacoes.append([nome_station,latitude_grau,longitude_grau])
                return lista_info_estacoes
                
        except(IOError,IndexError) as e:
            QMessageBox.critical(None, DadoIdioma().idioma(49), DadoIdioma().idioma(55))
            return []

    def Listar_OBS(self,dir,fill=False):
        lista_total_estruturada_com_inf = self.Ler_OBS()
        lista_total_estruturada_com_SIGLA = [estacao[0] for estacao in lista_total_estruturada_com_inf]
        if fill:
            caminho_itens = list(set([arquivos[:4].upper() for arquivos in os.listdir(dir)if (arquivos.lower().endswith("cmn") or arquivos.lower().endswith("std"))]))
            n_cadastrada = []
            s_cadastrada = []

            for iten in caminho_itens:
                try:
                    indx = lista_total_estruturada_com_SIGLA.index(iten)
                    s_cadastrada.append(lista_total_estruturada_com_inf[indx])
                except ValueError:n_cadastrada.append(iten)
        
            ##########################
            # verificar Busca SIGLAS #
            ##########################
    
            # thread_Busca_Siglas = thread_with_trace(target = self.BuscarEstacoes, args=(n_cadastrada,))
            # thread_Busca_Siglas.setDaemon(True)
            # thread_Busca_Siglas.start()
            # thread_Busca_Siglas.join()

            
            # s_cadastrada_novas, n_cadastrada = self.BuscarEstacoes(n_cadastrada)
            # [s_cadastrada.append(novas) for novas in s_cadastrada_novas]
            # s_cadastrada.sort(key=lambda srt: srt[0])
            # n_cadastrada.sort(key=lambda srt: srt[0])

            return_list = [s_cadastrada,n_cadastrada]
        else:
            return_list = lista_total_estruturada_com_inf
            return_list.sort(key=lambda srt: srt[0])
        return return_list
        

    def Refresh_list_obs(self, dir, ano, fill = False, dip = True, return_lista_siglas = False):
        list_return = []
        if fill:
            lista_siglas,lista_n_cad = self.Listar_OBS(dir,fill)
            list_return.append(lista_n_cad)
        else:lista_siglas = self.Listar_OBS(dir)
        lista_OBS_INF = []
        for sigla in lista_siglas:
            if dip:
                inclinacao = self.get_inclinacao_D(300,int(ano),float(sigla[1]),float(sigla[2]))
                diplat = (math.degrees(math.atan(((math.tan(math.radians(float(inclinacao)))/2)))))
                #string = (("%s (%s, %s, %.2f)")%(sigla[0],sigla[1],sigla[2],diplat))
                string = (("%s (%.2f, %.2f, %.2f)")%(sigla[0],float(sigla[1]),float(sigla[2]),diplat))
            else:
                #string = (("%s (%s, %s)")%(sigla[0],sigla[1],sigla[2]))
                string = (("%s (%.2f, %.2f)")%(sigla[0],float(sigla[1]),float(sigla[2])))
            lista_OBS_INF.append(string)
        list_return.append(lista_OBS_INF)
        if return_lista_siglas:list_return.append(lista_siglas)
        return list_return
    
    
    def FindDuplicates(self,in_list):  
        duplicates = []
        unique = set(in_list)
        for each in unique:
            count = in_list.count(each)
            if count > 1:duplicates.append(each)
        return duplicates

    def controle_entry_calendar(self,cl1,cl2):
        cl2.set(cl1.get())

    def largTICK(self,vt,op,tick,plt):
        if op == '+':vt.set(('%.1f')%(float(vt.get())+.1))
        elif op == '-':vt.set(('%.1f')%(float(vt.get())-.1))
        plt.tick_params(axis='both', which=tick, width=float(vt.get()))

    def altTICK(self,vt,op,tick,plt):
        if op == '+':vt.set(('%.1f')%(float(vt.get())+.1))
        elif op == '-':vt.set(('%.1f')%(float(vt.get())-.1))
        plt.tick_params(axis='both', which=tick, size=float(vt.get()))

    def sizeTICK(self,vt,op,plt):
        if op == '+':vt.set(int(vt.get())+1)
        elif op == '-':vt.set(int(vt.get())-1)
        plt.tick_params(axis='both', labelsize=int(vt.get()))#width=1.5 ,size=4)

    def Interpool_xyz(self,x=None,y=None,z=None,numcols=100,numrows=100):
        xi = np.linspace(x.min(), x.max(), numcols)
        yi = np.linspace(y.min(), y.max(), numrows)
        xi, yi = np.meshgrid(xi, yi)
        zi = interpolate.griddata((x, y), z,(xi, yi), method = 'linear')
        x = np.arange(0, zi.shape[1])
        y = np.arange(0, zi.shape[0])
        zi = np.ma.masked_invalid(zi)
        x1 = xi[~zi.mask]
        y1 = yi[~zi.mask]
        newarr = zi[~zi.mask]
        GD1 = interpolate.griddata((x1, y1), newarr.ravel(),(xi, yi),method='linear')
        return xi,yi,GD1


    # def verificar_alteracao_temp_ticks(self, axes, interface, eixo, dadoConfig):

    #     if self.Dado_config.Settings["INDIVIDUAL"]["fValue_Passo_Ticks_Y_temp"]:
    #         self._axes.yaxis.set_major_locator(ticker.IndexLocator(self.Dado_config.Settings["INDIVIDUAL"]["fValue_Passo_Ticks_Y_temp"]))
    #         return True
    #     elif self.Dado_config.Settings["INDIVIDUAL"]["fValue_Num_Ticks_Y_temp"]:
    #         self._axes.yaxis.set_major_locator(ticker.LinearLocator(self.Dado_config.Settings["INDIVIDUAL"]["fValue_Num_Ticks_Y_temp"]))
    #         return True
    #     return False


    def get_ROT(self, dados = [], delta_time_rot = 60, intervalo_LEITURA_CMN = 30, Fator_multplicacao = 1):
        delta_time_rot/=3600
        intervalo_LEITURA_CMN/=3600
        for hora in dados.keys():
            float_hora = float(hora)
            t1 = hora
            t2 = (("%.6f") % (float_hora + delta_time_rot))[:-1]
            TEC1 = dados[t1]['vtec']
            try:TEC2 = dados[t2]['vtec']
            except (KeyError) as e:
                t2 = (("%.6f") % (0.00001 + float_hora + delta_time_rot))[:-1]
                try:TEC2 = dados[t2]['vtec']
                except (KeyError) as e:TEC2 = np.nan
            ROT = ((TEC2-TEC1)/(delta_time_rot*60))
            dados[t1]['rot'] = ROT * Fator_multplicacao
        return dados

    def get_ROTI(self, dados = [], delta_time_roti = 300, intervalo_LEITURA_CMN = 30):
        delta_time_roti/=3600
        intervalo_LEITURA_CMN/=3600
        for hora in dados.keys():
            float_hora = float(hora)
            t1 = hora
            # t2 = (("%.6f") % (float_hora + delta_time_roti))[:-1]
            lista_rot = []
            for hora_std_roti in np.arange(float_hora,float_hora + delta_time_roti,  intervalo_LEITURA_CMN):
                try:lista_rot.append(dados[(("%.6f") % (hora_std_roti))[:-1]]['rot'])
                except (KeyError) as e:
                    try:lista_rot.append(dados[(("%.6f") % (0.00001 + hora_std_roti))[:-1]]['rot'])
                    except (KeyError) as e:lista_rot.append(np.nan)
            ROTI = np.nanstd(lista_rot)
            dados[t1]['roti'] = ROTI
        return dados
                
    def Leitura_CMN_DICT(self,destino = None, ele = 30):#filtro_horas = []):
    # def Leitura_CMN(self,destino = None, ele = 30):
        list_prn = []
        dados = {}
        try:
            # with open(destino,'r',encoding="UTF-8") as arquivo:
            ajuste_hora=np.arange(0,24,(30/3600))
            for i in range(len(ajuste_hora)):
                h=int(ajuste_hora[i]*100000)/100000
                hs=str(h)
                if hs[len(hs)-2:]=="99":
                    h=int(ajuste_hora[i]*1000000)/1000000
                else:h=int(ajuste_hora[i]*100000)/100000
                ajuste_hora[i]=("%.5f"%float(h))
            with open(destino,'r') as arquivo:
                for line in arquivo.readlines()[5:]:
                    linha = line.replace('\n','').split('\t')
                    time = linha[1][:-1]
                    #time = ("%.5f"%float(linha[1]))[:-1]
                    # if filtro_horas:
                        # if (time in filtro_horas):
                    prn = (linha[2]).replace(' ','')
                    elevation = float(linha[4])
                    lat = float(linha[5])
                    lon = float(linha[6])
                    vtec = float(linha[8])
                    if lon > 180.0:lon-=360
                    # lon-=360
                    if ((elevation >= ele) and (vtec > 0)):
                        if time == '-24.00000': time = '0.00000'
                        #Adaptação para ajustar hora errado no cmn
                        if not(float(time) in ajuste_hora):
                            #print(prn,time)
                            time1=time
                            time="%.5f"%(float(time1)-0.00416)
                            if not(float(time) in ajuste_hora):
                                time="%.5f"%(float(time1)-0.00417)
                                #if not(float(time) in ajuste_hora):
                                #    print("Não funcionou2", time)
                        list_prn.append(int(prn))
                        try:dados[prn+".time"].append(time)
                        except KeyError:
                            dados[prn+".time"] = []
                            dados[prn+".time"].append(time)
                        try:dados[prn+".vtec"].append(vtec)
                        except KeyError:
                            dados[prn+".vtec"] = []
                            dados[prn+".vtec"].append(vtec)
                        try:dados[prn+".lat"].append(lat)
                        except KeyError:
                            dados[prn+".lat"] = []
                            dados[prn+".lat"].append(lat)
                        try:dados[prn+".lon"].append(lon)
                        except KeyError:
                            dados[prn+".lon"] = []
                            dados[prn+".lon"].append(lon)
            list_prn = list(set(list_prn))
            result = (list_prn,dados)
        except (IOError,IndexError,FileNotFoundError) as e:result = ([],[])
            # print(e)
        return result



    def Leitura_CMN(self,destino = None, rot = False, roti = False, delta_time_rot = 300,delta_time_roti = 300, ele = 30):
    # def Leitura_CMN(self,destino = None, ele = 30):
        print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ")
        list_prn = []
        dados = {}
        try:
            with open(destino,'r') as arquivo:
                for line in arquivo.readlines()[5:]:
                    linha = line.replace('\n','').split('\t')
                    # time = ("%.6f"%float(linha[1]))
                    time = linha[1]
                    prn = (linha[2]).replace(' ','')
                    elevation = float(linha[4])
                    lat = float(linha[5])
                    lon = float(linha[6])
                    vtec = float(linha[8])
                    
                    if lon > 180.0:lon-=360
                    # lon-=360

                    if ((elevation >= ele) and (vtec > 0)):
                        if time == '-24.000000': time = '0.000000'
                        list_prn.append(int(prn))
                        try:dados[prn+".time"].append(time)
                        except KeyError:
                            dados[prn+".time"] = []
                            dados[prn+".time"].append(time)
                        try:dados[prn+".vtec"].append(vtec)
                        except KeyError:
                            dados[prn+".vtec"] = []
                            dados[prn+".vtec"].append(vtec)
                        try:dados[prn+".lat"].append(lat)
                        except KeyError:
                            dados[prn+".lat"] = []
                            dados[prn+".lat"].append(lat)
                        try:dados[prn+".lon"].append(lon)
                        except KeyError:
                            dados[prn+".lon"] = []
                            dados[prn+".lon"].append(lon)
            list_prn = list(set(list_prn))
            result = (list_prn,dados)
        except (IOError,IndexError,FileNotFoundError) as e:result = ([],[])
            # print("indicando erro.. linha 885 util.py",e)
        return result

    
    def Leitura_trip(self,destino):
        matrizstd = []
        try:
            with open(destino,'r',encoding="UTF-8") as arqDiaStd:
                tmpStd=[]
                tudin = arqDiaStd.readlines()
                for tmpline in tudin:
                    VTEC = ((tmpline.split('\t')[1]).replace(",",".").strip())
                    if VTEC == "-" or float(VTEC) < 0:tmpStd.append(np.nan)
                    else:tmpStd.append(float(VTEC))
                tmp_len = len(tudin)
                if  tmp_len < 1440:
                    tmp_delt = (1440 - tmp_len)
                    for inter_tmp in range(tmp_delt):tmpStd.append(np.nan)
                elif tmp_len > 1440:del(tmpStd[-1])
                matrizstd.append(tmpStd)
                arqDiaStd.close()
        except (IOError,IndexError):matrizstd.append([np.nan]*1440)
        
        return matrizstd

    def Teste(self):
        print("Loading…\n█▒▒▒▒▒▒▒▒▒\n10%\n███▒▒▒▒▒▒▒\n30%\n█████▒▒▒▒▒\n50%\n███████▒▒▒\n100%\n██████████\n")
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n@@@@@@@@@@@@@@@@@&#((((#%@@@@@@@@@@@@@@@@\n@@@@@@@@@@@@@/,,,,,,,,,,,,,,/&@@@@@@@@@@@\n@@@@@@@@@@(,,,,,,,,,/@@@@@@(,,,#@@@@@@@@@\n@@@@@@@@&*,,,,,,,,,,/@@@@@*,,,,,,&@@@@@@@\n@@@@@@@@,,,,,,,,,,,,%@@@@#,,,,,,,,%@@@@@@\n@@@&,,,&@@&#/(((&@@@,,,,,@&###%&@@@,,,,,&\n@@@/,,(@@@@(,&@*,/@(/(%,/@@(,#@&,/@(,,,*@\n@@@,,,%@@@%,,#/*%@&*&%*/&@%,/@@@*,&%,,,&@\n@@#,,,#@@@*,%@@@@@&&*&&#@@*,@@@/,%@#,,#@@\n@@*,,,/@@%,*@@@@@@,,,,,@@(,*@&**&@@/,,@@@\n@#,,,,,#&&&&&&&&&(****/@@@@@&&&&&&&**/@@@\n@@@@@@@@*,,,,,,,*@@@@@*,,,,,,,,,,/@@@@@@@\n@@@@@@@@@&,,,,,*@@@@@%,,,,,,,,,,#@@@@@@@@\n@@@@@@@@@@@&/%%%%%%%%%%%/,,,,,&@@@@@@@@@@\n@@@@@@@@@@@@@@#,,,,,,,,,,,,/@@@@@@@@@@@@@\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n")
        print("                             `..-::::::::--.``                            \n                        `.:+syhhhhdddddddhhhys+:.`                        \n                     `:+yhddddddddddddddddddddddhyo:.                     \n                  `-+ydddddddddh+///:::::::::::::///::-`                  \n                 -shddddddddddddhyys/`          -+syhhhs:`                \n               -ohddddddddddddddddddh-         /hddddddddy:`              \n             `/hddddddddddddddddddddy`        .hddddddddddh+`             \n            `odddddddddddddddddddddd/        `sdddddddddddddy.            \n           `ohdddddddddddddddddddddh.        :hhdddddddddddddy-`          \n    `/sssss:------:::::::::--------osssssssso:-----------------osssssssss:\n    .hdddds      `-+yyyo+oso/.    -hdddddddds` .:oooo+++/:.`   /ddddddddy.\n    +ddddh-       `+ddy- `oddh-  `+ddhyyhddh:   `sddy.`.oddy:  `yddddddd/ \n   `hdddds`       .hdd/  `oddh:  -hd/:y./dds`   :hdd/    sddd-  +ddddddy` \n   +dddddo`       oddy` `/ddh+` `odh -+/ydd-   `sddy.    /dddo  :dddddd/  \n  .hddddd+       -ddds/+sys/.   .yoo.`oy:oo    /ddh:     +ddd+  -dddddy`  \n  +dddddd+      `sdds`          .`/do`.+sh-   `hdds     .hddh.  :ddddd:   \n .ydddddds`     /ddh:          -/`.+s/.`//`   +ddh.    .sdds-   /dddds`   \n /dddddddh.    .ydds`         `odhyyhdhys-   -hddo   `/hdy:`    sdddh:    \n.yddddddddo  .:ossso:.        :hddddddddo` -/syyhs//+o+:.      :ddddo     \n/dddddddddd-                 `sddddddddh-  ``````````         .sdddd-     \n.-----------syyyyyyyyyyyyyyyyo.........+yyyyyyyyyyyyyyyyyyyyys:.....      \n            -yddddddddddddddd:        `yddddddddddddddddddddd/            \n             .sdddddddddddddo         /ddddddddddddddddddddy:             \n              `/yddddddddddy.        `sddddddddddddddddddh+.              \n                .+hddddddh+.          /ydddddddddddddddhs-                \n                  .+ys:::-.............-:::sdddddddddh+-`                 \n                    `-+yhhhhhhhhhhhhhhhhhhhdddddddho:.                    \n                       `-/oyhddddddddddddddddhys+:`                       \n                           `.-:/+oossssoo+/:-.``                          \n")
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&&##(((((((((##%&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n@@@@@@@@@@@@@@@@@@@@@@@@@@@&#(*,,,,,,,,,,,,,,,,,,,,,*/(&@@@@@@@@@@@@@@@@@@@@@@@@@@\n@@@@@@@@@@@@@@@@@@@@@@@@@#/*,,,,,,,,,,,,,,,,,,,,,,,,,,,*/#&@@@@@@@@@@@@@@@@@@@@@@@\n@@@@@@@@@@@@@@@@@@@@@@&#/,,,,,,,,,,/#%%%%%%%%%%%%%%%%%%%%%%%&@@@@@@@@@@@@@@@@@@@@@\n@@@@@@@@@@@@@@@@@@@@(*,,,,,,,,,,,,,,,,,,/%@@@@@@@@@@@&(,,,,,,*#&@@@@@@@@@@@@@@@@@@\n@@@@@@@@@@@@@@@@@@&#,,,,,,,,,,,,,,,,,,,,*#@@@@@@@@@@%/,,,,,,,,,*#@@@@@@@@@@@@@@@@@\n@@@@@@@@@@@@@@@@&(*,,,,,,,,,,,,,,,,,,,,,/%@@@@@@@@@#*,,,,,,,,,,,,(&@@@@@@@@@@@@@@@\n@@@@@@@@@@@@@@@%/,,,,,,,,,,,,,,,,,,,,,,,(&@@@@@@@@&/,,,,,,,,,,,,,,/%@@@@@@@@@@@@@@\n@@@@@@@@@@@@@@&*,,,,,,,,,,,,,,,,,,,,,,,,&@@@@@@@@@(*,,,,,,,,,,,,,,,*(&@@@@@@@@@@@@\n@@@@@@@%(/////#&&&&&&&&&&&&&&&&&&&&&&&&%//////////%&&&&&&&&&&&&&&&&&%#//////////&@\n@@@@@@&(,,,,,/&@@@@@&%#(//(((((#&@@@@@@#,,,,,,,,,*@@&%######%%&&@@@@@%,,,,,,,,,*&@\n@@@@@@#*,,,,/%@@@@@@@@%*,*#@@@*,,*#@@@%/,,***,,,,(@@@@%,,,/&@%/,,(%@@@/,,,,,,,,(@@\n@@@@@&/,,,,,(&@@@@@@@&(,,/&@@@*,,,/@@&(*/#((%*,,/%@@@&(,,*#@@@&/,,/%@@(,,,,,,,*%@@\n@@@@@(*,,,,*#@@@@@@@&(*,,%@@@#,,*(&@@#*,&&###,,*#@@@@#*,*#@@@@@#*,,/&@#*,,,,,*#@@@\n@@@@@/,,,,,/%@@@@@@@%/,,,##(/**(%@@@&/*/&@%/*(/(&@@@%/,,/&@@@@@#*,,/&@%*,,,,,/&@@@\n@@@@&*,,,,,/%@@@@@@@(,,,/%%%%&@@@@@@%#%(#&&#((/%@@@&(*,*%@@@@@&/,,*#&@%*,,,,*#@@@@\n@@@@#,,,,,,*#@@@@@@&*,,/%@@@@@@@@@@&&@&#*(&@&/#@@@@#*,,#@@@@@%/,,/%@@@#*,,,*#@@@@@\n@@@&/,,,,,,*(&@@@@@%,,*#&@@@@@@@@@@(/(%%(//(%%@@@@%/,,,&@@@@%/,,*&@@@@(,,,,/%@@@@@\n@@&(*,,,,,,,*#@@&%(*,,*#&@@@@@@@@@&*,,,,,,,,,%@@@&*,,,*%%%(//(%&@@@@@@*,,,,%@@@@@@\n@@%/,,,,,,,,,(&@&&&&&&&&&@@@@@@@@@%,,,,,,,,,,&@@&%#####%%%%&@@@@@@@@@&,,,,*&@@@@@@\n@&#*,,,,,,,,,*#&&&&&&&&&&&&&&&&&&&(*********/&@@@@@@@@@&&&&&&&&&&&&&&#****/@@@@@@@\n@@@@@@@@@@@@@@@*,,,,,,,,,,,,,,,,,(&@@@@@@@@&(,,,,,,,,,,,,,,,,,,,,,,*#@@@@@@@@@@@@@\n@@@@@@@@@@@@@@@%*,,,,,,,,,,,,,,,*%@@@@@@@@@%*,,,,,,,,,,,,,,,,,,,,,/%@@@@@@@@@@@@@@\n@@@@@@@@@@@@@@@@@%/,,,,,,,,,,,,*#@@@@@@@@@%/,,,,,,,,,,,,,,,,,,,,,%@@@@@@@@@@@@@@@@\n@@@@@@@@@@@@@@@@@@&(,,,,,,,,,,*#@@@@@@@@@@%*,,,,,,,,,,,,,,,,,,,*#@@@@@@@@@@@@@@@@@\n@@@@@@@@@@@@@@@@@@@@(*,,,,,,,*%@@@@@@@@@@@&(*,,,,,,,,,,,,,,,,*(&@@@@@@@@@@@@@@@@@@\n@@@@@@@@@@@@@@@@@@@@@@&#/#%%%%%%%%%%%%%%%%%%%%%#/,,,,,,,,,,/&@@@@@@@@@@@@@@@@@@@@@\n@@@@@@@@@@@@@@@@@@@@@@@@@(*,,,,,,,,,,,,,,,,,,,,,,,,,,,,,*(%@@@@@@@@@@@@@@@@@@@@@@@\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&(/*,,,,,,,,,,,,,,,,,*/(#&@@@@@@@@@@@@@@@@@@@@@@@@@@@\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&%#((///////((#%%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n")


if __name__ == "__main__":
    # root = Tk()

    teste = Utilitarios()
    teste.Teste()
    teste = DadoIdioma()
    teste.idioma(2,1)
    
    # root.mainloop()

