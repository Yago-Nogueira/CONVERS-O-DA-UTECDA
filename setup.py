import sys,os
import os.path
from cx_Freeze import setup, Executable

base=None
# if sys.platform=='win32':
#     base="Win32GUI"
setup(
	name = "UTECDA",
	version = "2.0",
	author	= "IP&D - Instituto de Pesquisa e Desenvolvimento",
	description ="Univap Conteúdo Eletronico Total Analise de Dados" ,
	options = {
		"build_exe":{
			'packages':[
				"pkg_resources._vendor",
				"PyQt6",
				"matplotlib",
				"numpy",
				"sys",
				"xarray",
				"igrf12",
				"pandas",
				"datetime",
				"shutil",
				"scipy",
				"os",
				"uuid",
				"getpass",
				"math",
				"qt_ui",
				"qt_calendar",
				"qtSimpleDialog",
				"qtfontchooser",
			],
			'include_files': [
				r'vc_redist.x64.exe',
				r'vc_redist.x86.exe',
				r'icone.ico'
			],
			'excludes': ["scipy.spatial.cKDTree"],
			'include_msvcr': True
		}
	},
	executables = [
		Executable(
			"principal.py",
			shortcutName="UTECDA",
			shortcutDir="DesktopFolder",
			base=base,
			icon="icone.ico",
			targetName="UTECDA.exe"
			)
		]
	)
