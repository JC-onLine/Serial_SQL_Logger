# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

#####################################################################################
#
# 					Serial_SQL_Logger_GUI_MAIN.py
#
# Principe	:	Le but est de recevoir des logs depuis le port série,
#				et de les enregistrer dans une base de données sql.
#				Cette appli est un fork de 'Serie_vers_Afficheur_Uno_MAIN.py'
#
# Dépendance:	Interface graphique 'Serial_SQL_Logger_GUI_GUI.py'
#				GUI developpée avec 'wxFormBuilder v3.4.2 beta (unicode)'
#				Installation :
#				- python-2.7.6.amd64.msi
#				- wxPython3.0-win64-3.0.0.0-py27.exe
#				- wxFormBuilder_v3.4.2-beta.exe
#
# 2014-04-19:	Creation
# 2014-04-20:	Ajout menu <Port COM> + activation COM dispo dans menu
# 2014-04-21:	Ajout menu <Vitesse> + description menu status
#			 	Remplacement status Ctrtxt par StaticText
# 2014-04-22:	Ajout boite dialogue saisie manu port COM + err COM
# 2014-04-24:	Ajout menu <Gestionnaire de periphérique>
# 2014-04-24:	Ajout COM16 à COM20
# 2014-04-26:	Ajout menu [Fichier]/<Nouveau> 
#			 	+ mot COM dans menu [Vitesse COM]
#				+ différenciation des commentaires [menu] et <menuItem>
#				+ ré-indentation des commentaires du header de l'appli
# 2014-04-26a:	Correction bug menu [Port COM]/<Séléction manuelle> en wxITEM_RADIO
# 2014-05-04:	Ajout dev menu [Fichier] <Enregistrer>
# 							   [Fichier] <Enregistrer sous...>
# 							   [Fichier] <Ouvrir>
#				Correction bug menu [Port COM]/<Actualiser> en wxITEM_RADIO
#				Correction orthographe 'périphérique'+'Système' dans menu [Système]
#				Mise en commentaire fonction 'ActualiserCOM()' au démarrage appli
#	---------------------------------------------------------------------------------
# 2014-05-11:	Fork de Serie_vers_Afficheur_Uno_MAIN.py
#				Adaptation:
#					suppression des boutons, slider, progressbar etc
# 2014-05-17:	Ajout réception série dans le textCtrl (aide miniterm.py de pySerial)
#				Ajout Led ERR rouge/gris clignotant, si erreur definition port COM
# 2014-05-31:	Correction open-save-saveas car textCtrl nom différent
#				wxFB changement titre fenêtre appli
#				wxFB logTextCtrl enabled=true pour capture logs copier-coller
#				Ajout menu Port COM21 à COM25
#				Ajout RUN clignotant
#				Remplacement self.logTextCtrl.Value par self.logTextCtrl.WriteText
#				Modif self.repr_mode=1 pour gestion CRLF
#				Ajout arrêt clignotant pendant popup open/save/saveas
#				Essai ok: pc jc bluetooth COM20, avec VM prog08 WinCC Bac63 Ligne10 COM4
# 2014-06-01	GUI: Ajout CtrlTxt pour zone logs appli en plus de print
#				Ajout fonction MsgLog(self,"message") pour "logAppliTextCtrl"
# 2014-06-15	Remplacement disableBlinkGbl par enableBlinkGbl
# 2014-07-19	Remome wxFB nouveau/ouvrir/enreg/enreg en newLog/openLog/saveLog/saveAsLog
#				Ajout  wxFB newProfil/openProfil/saveProfil/saveAsProfil
# 2014-07-20	renome variable fichier en logFolderName/logFileName
#				création gestion profile avec module ConfigParser
# 2014-07-21	Gestion profile New/Open/Save/SaveAS
#				Fonctions CheckCOM() CheckVitesse() pour actu selection menu depuis profile
# 2014-07-22	Fin gestion profile conf port série, avec rappel dans titre appli
# 2014-07-26	wxFB: redimenssionnement GUI pour CubieTruck résol. 1024x768
#				Indication OS+architecture 32/64bits
# 2014-07-27	Actualisation port COM dans comboBox: w7+debian=ok				
# 2014-08-10	Création ToolBar, remplacement terme 'Actualisation port' par 'Rechercher port'
#				Suppression menu COM1..25 fonction EnableCOM() CheckCOM()
# 2014-09-07	Correction wxBitmapComboBox: compatibilité linux=ok
# 2014-09-08	Ajout AppliStart/AppliStop sur bouton Play/Stop toolbar test Linux Debian=ok
#				Etude bug graphique RUN clignotant bmp ON/OFF
#				le bug est du à la toolbar -> Déplacement du clignotant dans la toolbar
# 2014-09-19	Ajout de png spacer pour toolbar séparation des objets
# 2014-09-20	Ajout test MySQL MySQLdb 64bits http://www.codegood.com/archives/129
# 2014-09-21	Recherche MySQLdb
# 2014-09-23	Bouton MySQL INSERT fonctionne vers base serial_sql_logger Cubietruck
# 2014-09-24	Ajout MysqlInsert sur réception CR = ok
# 2014-09-28	Ajout chekBox pour extraction et séparation des données
# 2014-09-29	Ajout événements checkBox + Enable/Disable Txt et comboBox
# 2014-10-10	Modif GUI case à cocher décodage Horodatage/Catégorie/Priorité
# 2014-10-12	Ajout selections case à cocher dans le profile de réglage
#
#####################################################################################
# TODO:
#		[x] Marquer le nom du fichier en cours dans la barre de titre appli
#		[x] Raccourcie clavier Ctrl+N Ctrl+O Ctrl+S Ctrl+Shift+S Ctrl+Q
#		[ ] Mettre une icônes dans la barre de titre appli
#		[x] Voir si possible de mettre icônes dans menu Fichier/ouvrir etc
#		[x] Detecter OS pour compatibilité Windows/Linux
#		[x]	Gestion de profile de config COM pour utilisation différent PC
#		[ ]	Boot appli avec le dernier profile sélectionné
#		[ ] Faire apparaitre commentaire affect port COM ex: COM4 'Bluetooth' 
#			-> memoriser non machine et proposer la catalogue des ports COM
#		[ ] Ajouter zone saisie 'Terminal'
#		[ ] Ajouter animation sur bouton Play/Stop toolbar
#		[ ] Ajouter enregistrement SQL des logs
#		[ ] Ajouter logs des checkBox
#		[ ] Ajouter dossier 'Progile' pour enregistrement des Profile
#		[ ] Ajouter dossier 'Logs' pour enregistrement des Logs provenant port série
#####################################################################################

# importation la librairie wxWidget
import wx
# importation de la partie GUI
import Serial_SQL_Logger_GUI
# acces à la librairie du port série
import serial
# acces à la librairie de la gestion du temps
from time import sleep
# acces fonctions systeme
import os
import platform
# gestion des tâches
import threading
import sys
# gestion du temps
import time
# gestion de config/profile
import ConfigParser
# gestion base MySQL
import MySQLdb
# gestion date/heure
import time

# variables globales
global gSerialLog
global COMselectGbl
global COMvitesseGbl
global statusRunStopGbl
global compteurGbl
global erreurGbl
global erreurBlinkGbl
global runBlinkGbl
global enableBlinkGbl
global enableErrBlinkGbl
global bmpCirculaireIndexGbl
global gExtractHorodatageChk
global gExtractCategorieChk
global gExtractCategorieTxt
global gExtractPrioriteChk
global gExtractPrioriteInt
global gCaractereSeparateurTxt
global gCaractereSeparateurEnable

LF = serial.to_bytes([10])
CR = serial.to_bytes([13])
CRLF = serial.to_bytes([13, 10])
CONVERT_CRLF = 2
CONVERT_CR   = 1
CONVERT_LF   = 0
NEWLINE_CONVERISON_MAP = (LF, CR, CRLF)
LF_MODES = ('LF', 'CR', 'CR/LF')


class screenMain(Serial_SQL_Logger_GUI.FenetrePrincipaleClass):
	# constructor
	def __init__(self,parent):
		#self.Bind( wx.PyEventBinder(SERIALRX, 0), self.OnSerialRead)
		# initialize parent class
		Serial_SQL_Logger_GUI.FenetrePrincipaleClass.__init__(self,parent)
		# création objet portSerie depuis class Srérial de lib pySerial
		#self.portSerie = serial.Serial(str(COMselectGbl),int(COMvitesseGbl))
		self.portSerie = serial.Serial()
		#self.portSerie.timeout = 0.5   #make sure that the alive event can be checked from time to time
		self.thread = None
		self.alive = threading.Event()               
		# init titre de l'appli
		APP_TITRE = "Serial to SQL Logger"
        #self.SetTitle("Serial to SQL Logger")
		#screenHome.SetTitle('Serial to SQL Logger')
        #self.SetSize((546, 383))
		# init nom fichier+dossier
		self.logFileName = ""
		self.logFolderName = ""
		self.profileFileName   = ""
		self.profileFolderName = ""
        # Init des paramètres de COM
		self.echo = False
		self.repr_mode = 0
		self.convert_outgoing = CONVERT_CRLF
		self.newline = NEWLINE_CONVERISON_MAP[self.convert_outgoing]
		self.dtr_state = True
		self.rts_state = True
		self.break_state = False
		# init pointeur icones
		self.imageOsLinux   = wx.Bitmap(os.path.join(os.path.curdir,"Icons","OS","icon_linux.png"),wx.BITMAP_TYPE_ANY)
		self.imageOsWindows = wx.Bitmap(os.path.join(os.path.curdir,"Icons","OS","icon_windows.png"),wx.BITMAP_TYPE_ANY)
		self.imagePlay      = wx.Bitmap(os.path.join(os.path.curdir,"Icons","ToolBar","Oxygen","media-playback-start.png"),wx.BITMAP_TYPE_ANY)
		self.imagePause     = wx.Bitmap(os.path.join(os.path.curdir,"Icons","ToolBar","Oxygen","media-playback-pause.png"),wx.BITMAP_TYPE_ANY)
		self.imageLedStop   = wx.Bitmap(os.path.join(os.path.curdir,"Icons","LED","LedSTOP.png"   ),wx.BITMAP_TYPE_ANY)
		self.imageLedRunOn  = wx.Bitmap(os.path.join(os.path.curdir,"Icons","LED","LedRUN_ON.png" ),wx.BITMAP_TYPE_ANY)
		self.imageLedRunOff = wx.Bitmap(os.path.join(os.path.curdir,"Icons","LED","LedRUN_OFF.png"),wx.BITMAP_TYPE_ANY)
		self.imageLedErrOn  = wx.Bitmap(os.path.join(os.path.curdir,"Icons","LED","LedERR_ON.png" ),wx.BITMAP_TYPE_ANY)
		self.imageLedErrOff = wx.Bitmap(os.path.join(os.path.curdir,"Icons","LED","LedERR_OFF.png"),wx.BITMAP_TYPE_ANY)
		self.bmpCirculaireIndex1 = wx.Bitmap(os.path.join(os.path.curdir,"Icons","Loader","icon_loader_31x31_01.png"),  wx.BITMAP_TYPE_ANY)
		self.bmpCirculaireIndex2 = wx.Bitmap(os.path.join(os.path.curdir,"Icons","Loader","icon_loader_31x31_02.png"),  wx.BITMAP_TYPE_ANY)
		self.bmpCirculaireIndex3 = wx.Bitmap(os.path.join(os.path.curdir,"Icons","Loader","icon_loader_31x31_03.png"),  wx.BITMAP_TYPE_ANY)
		self.bmpCirculaireIndex4 = wx.Bitmap(os.path.join(os.path.curdir,"Icons","Loader","icon_loader_31x31_04.png"),  wx.BITMAP_TYPE_ANY)
		self.bmpCirculaireIndex5 = wx.Bitmap(os.path.join(os.path.curdir,"Icons","Loader","icon_loader_31x31_05.png"),  wx.BITMAP_TYPE_ANY)
		self.bmpCirculaireIndex6 = wx.Bitmap(os.path.join(os.path.curdir,"Icons","Loader","icon_loader_31x31_06.png"),  wx.BITMAP_TYPE_ANY)
		self.bmpCirculaireIndex7 = wx.Bitmap(os.path.join(os.path.curdir,"Icons","Loader","icon_loader_31x31_07.png"),  wx.BITMAP_TYPE_ANY)
		self.bmpCirculaireIndex8 = wx.Bitmap(os.path.join(os.path.curdir,"Icons","Loader","icon_loader_31x31_08.png"),  wx.BITMAP_TYPE_ANY)
		# affichage de l'OS + architecture 32/64bits
		global g_OSname
		global g_OSversion
		global g_OSdistrib
		global g_architectBits
		if (g_OSname == 'Linux'):
			self.m_bmpOS.SetBitmap(self.imageOsLinux)
			self.m_OSdetailsTxt.SetLabel(g_OSdistrib)
			MsgLog(self, "Systeme d'exploitation: " + g_OSname+'  '+g_OSdistrib+'  '+g_architectBits)
			self.m_gestPeriphMnu.Enable(False)
		else:
			self.m_bmpOS.SetBitmap(self.imageOsWindows)
			self.m_OSdetailsTxt.SetLabel(g_OSname+' '+g_OSversion)
			MsgLog(self, "Systeme d'exploitation: " + g_OSname+'  '+g_OSversion+'  '+g_architectBits)
		self.m_ArchBitsTxt.SetLabel(g_architectBits)
		# ListBox Caractères séparateurs de données
		self.m_separateurCbx.Clear()
		self.m_separateurCbx.Append("|")
		self.m_separateurCbx.Append(";")
		self.m_separateurCbx.Append("*")
		self.m_separateurCbx.Append("TAB")
			
		
	# capture de l'événement m_timer1
	def m_timer1Evt(self,event):
		global compteurGbl
		global erreurGbl
		global erreurBlinkGbl
		global statusRunStopGbl
		global runBlinkGbl
		global enableBlinkGbl
		global enableErrBlinkGbl
		global bmpCirculaireIndexGbl
		compteurGbl = compteurGbl + 1
		if compteurGbl >5:
			compteurGbl = 0
			enableErrBlinkGbl = not enableErrBlinkGbl
		self.m_compteurTxt.SetLabel(str(compteurGbl))
		# gestion Led clignotante RUN:
#		if (statusRunStopGbl and enableBlinkGbl):
#			if (not runBlinkGbl):
#				# animation led RUN clignotante ON
#				self.m_bmpRunStop.SetBitmap(self.imageLedRunOn)
#				runBlinkGbl = True
#			else:
#				# animation led RUN clignotante OFF
#				self.m_bmpRunStop.SetBitmap(self.imageLedRunOff)
#				runBlinkGbl = False
		# gestion Led clignotante Erreur:
		if (erreurGbl and enableErrBlinkGbl):
			if (not erreurBlinkGbl):
				# animation led ERR clignotante ON
				self.m_bmpRunStop.SetBitmap(self.imageLedErrOn)
				erreurBlinkGbl = True
			else:
				# animation led ERR clignotante OFF
				self.m_bmpRunStop.SetBitmap(self.imageLedErrOff)
				erreurBlinkGbl = False
		#gestion bmp circulaire 
		if (statusRunStopGbl and enableBlinkGbl):
			if bmpCirculaireIndexGbl==1:
				self.m_bmpCirculaire.SetBitmap(self.bmpCirculaireIndex1)
			elif bmpCirculaireIndexGbl==2:
				self.m_bmpCirculaire.SetBitmap(self.bmpCirculaireIndex2)
			elif bmpCirculaireIndexGbl==3:
				self.m_bmpCirculaire.SetBitmap(self.bmpCirculaireIndex3)
			elif bmpCirculaireIndexGbl==4:
				self.m_bmpCirculaire.SetBitmap(self.bmpCirculaireIndex4)
			elif bmpCirculaireIndexGbl==5:
				self.m_bmpCirculaire.SetBitmap(self.bmpCirculaireIndex5)
			elif bmpCirculaireIndexGbl==6:
				self.m_bmpCirculaire.SetBitmap(self.bmpCirculaireIndex6)
			elif bmpCirculaireIndexGbl==7:
				self.m_bmpCirculaire.SetBitmap(self.bmpCirculaireIndex7)
			elif bmpCirculaireIndexGbl==8:
				self.m_bmpCirculaire.SetBitmap(self.bmpCirculaireIndex8)
			bmpCirculaireIndexGbl=bmpCirculaireIndexGbl+1
			if bmpCirculaireIndexGbl > 8:
				bmpCirculaireIndexGbl = 1


	# capture de l'événement clic 'RUN'
	def m_bntRunEvt(self,event):
		self.AppliStart()

	# capture de l'événement clic 'STOP'
	def m_bntStopEvt(self,event):
		self.AppliStop()

	# capture de l'événement clic 'MySQL INSERT'
	def m_btn_mysqlInsertEvt(self,event):
		MysqlInsert(self,"Uno", "1", "Bouton Test")

	# capture de l'événement click checkBox 'Extraction Horodatage'
	def m_ExtractHorodateChkEvt(self,event):
		# mise à jour variable globale 'Extraction Horodatage'
		global gExtractHorodatageChk
		if event.IsChecked():
			gExtractHorodatageChk = True
		else:
			gExtractHorodatageChk = False
		print "gExtractHorodatageChk = " + str(gExtractHorodatageChk)
		SeparateurEnable(self)

	# capture de l'événement click checkBox 'Extraction Catégorie'
	def m_ExtractCategorieChkEvt(self,event):
		global gExtractCategorieChk
		# si la case 'Extraction Catégorie' est cochée
		if event.IsChecked():
			gExtractCategorieChk = True		# update image var globale
			#Désactivation saisie txt 'Catégorie'
			#car le nom de la catégorie sera extraite des logs
			self.m_CategorieTxt.Enable(False)
		else:
			gExtractCategorieChk = False	# update image var globale
			#Activation saisie txt 'catégorie'
			#pour saisir manuellement la catégorie pour SQL
			self.m_CategorieTxt.Enable(True)
		print "gExtractCategorieChk = " + str(gExtractCategorieChk)
		SeparateurEnable(self)

	# capture de l'événement Saisie Text 'Catégorie'
	def m_CategorieTxtEvt(self,event):
		global gExtractCategorieTxt
		gExtractCategorieTxt = self.m_CategorieTxt.GetValue()
		print "m_CategorieTxtEvt: " + gExtractCategorieTxt
	# capture de l'événement Saisie Text 'Catégorie'
	def m_CategorieTxtTextEnter(self,event):
		global gExtractCategorieTxt
		gExtractCategorieTxt = self.m_CategorieTxt.GetValue()
		print "m_CategorieTxtTextEnter: " + gExtractCategorieTxt

	# capture de l'événement click checkBox 'Extraction Priorité'
	def m_ExtractPrioriteChkEvt(self,event):
		global gExtractPrioriteChk
		# si la case 'Extraction Priorité' est cochée
		if event.IsChecked():
			gExtractPrioriteChk = True		# update image var globale
			#Désactivation saisie txt 'Priorité'
			#car le nom de la catégorie sera extraite des logs
			self.m_PrioriteInt.Enable(False)
		else:
			gExtractPrioriteChk = False		# update image var globale
			#Activation saisie txt 'Priorité'
			#pour saisir manuellement la  Priorité pour SQL
			self.m_PrioriteInt.Enable(True)
		print "gExtractPrioriteChk = " + str(gExtractPrioriteChk)
		SeparateurEnable(self)

	# capture de l'événement Saisie 'Priorité' OnSpinCtrl
	def m_PrioriteIntEvt(self,event):
		global gExtractPrioriteInt
		gExtractPrioriteInt = self.m_PrioriteInt.GetValue()
		print "gExtractPrioriteInt Evt = " + str(gExtractPrioriteInt)
	# capture de l'événement Saisie 'Priorité' OnSpinCtrlText
	def m_PrioriteIntEvtTxt(self,event):
		global gExtractPrioriteInt
		gExtractPrioriteInt = self.m_PrioriteInt.GetValue()
		print "gExtractPrioriteInt EvtTxt = " + str(gExtractPrioriteInt)
	# capture de l'événement Saisie 'Priorité' OnSpinCtrlEnter
	def m_PrioriteIntEvtEnter(self,event):
		global gExtractPrioriteInt
		gExtractPrioriteInt = self.m_PrioriteInt.GetValue()
		print "gExtractPrioriteInt EvtEnter = " + str(gExtractPrioriteInt)

	# capture de l'événement Sélection Cbo Evt 'Caractère séparateur'
	def m_separateurCbxEvt(self,event):
		global gCaractereSeparateurTxt
		gCaractereSeparateurTxt = self.m_separateurCbx.GetValue()
		print("gCaractereSeparateurTxt Evt = " + gCaractereSeparateurTxt)
	# capture de l'événement Sélection Cbo OnText 'Caractère séparateur'
	def m_separateurCbxOnText(self,event):
		global gCaractereSeparateurTxt
		gCaractereSeparateurTxt = self.m_separateurCbx.GetValue()
		print("gCaractereSeparateurTxt OnText= " + gCaractereSeparateurTxt)
	# capture de l'événement Sélection Cbo OnTextEnter 'Caractère séparateur'
	def m_separateurCbxOnTextEnter(self,event):
		global gCaractereSeparateurTxt
		gCaractereSeparateurTxt = self.m_separateurCbx.GetValue()
		print("gCaractereSeparateurTxt OnTextEnter = " + gCaractereSeparateurTxt)

	#####################################################
	# 					Fonction Appli_start(self)
	# Principe	:	Démarre la scrutation du port série
	# Dépandence:	Variables globales réglages appli
	# Appelé par:	bouton GUI
	# 2014-09-08:	Création
	#####################################################
	def AppliStart(self):
		global COMselectGbl
		global COMvitesseGbl
		global erreurGbl
		print("Capture evenement bouton RUN")
		# START si port série déjà pas ouvert
		if not self.portSerie.isOpen(): 
			# test si variable COMselectGbl pas definie
			if COMselectGbl == "Non select.":
				print('Port serie non selectionne')
				MsgLog(self,'Erreur: Port serie non selectionne')
				erreurGbl = True
				boxErr = wx.MessageDialog(None,'Port serie non selectionne', 'Erreur:', wx.OK)
				reponse= boxErr.ShowModal()
				boxErr.Destroy()
				# arret clignotant ERR
				erreurGbl = False
				self.m_bmpRunStop.SetBitmap(self.imageLedStop)
				self.m_RunStopTool.SetNormalBitmap(self.imagePause)
			# le port COM est defini, on continue
			else:
				#initialisation et ouverture du port série
				try:
					self.portSerie = serial.Serial(str(COMselectGbl),int(COMvitesseGbl))
				except Exception:
					print('Erreur avec le port serie '+COMselectGbl)
					MsgLog(self,'Erreur avec le port serie '+COMselectGbl)
					erreurGbl = True
					# appel popup erreur COM
					boxErr = wx.MessageDialog(None,'Erreur avec le port serie '+COMselectGbl, 'Erreur:', wx.OK)
					reponse=boxErr.ShowModal()
					boxErr.Destroy()
					# arret clignotant ERR
					erreurGbl = False
					#imageLedStop = wx.Bitmap("LedSTOP.png", wx.BITMAP_TYPE_ANY)
					self.m_bmpRunStop.SetBitmap(self.imageLedStop)
					self.m_RunStopTool.SetNormalBitmap(self.imagePause)
				else:
					# pas d'erreur, on continue:
					erreurGbl = False
					self.portSerie.timeout = 0.5   #make sure that the alive event can be checked from time to time
					# animation led run
					#imageLedRun  = wx.Bitmap("LedRUN_ON.png",  wx.BITMAP_TYPE_ANY)
					self.m_bmpRunStop.SetBitmap(self.imageLedRunOn)
					self.m_RunStopTool.SetNormalBitmap(self.imagePlay)
					print('Port serie '+COMselectGbl+' ouvert.')
					MsgLog(self,'Passage en RUN: Port serie '+COMselectGbl+' ouvert.')
					# flag appli en run
					global statusRunStopGbl
					statusRunStopGbl = 1
					# démarrage scrutation réception série
					self._start_reader()

	#####################################################
	# 					Fonction Appli_stop(self)
	# Principe	:	Arrête la scrutation du port série
	# Dépandence:	Variables globales réglages appli
	# Appelé par:	bouton GUI
	# 2014-09-08:	Création
	#####################################################
	def AppliStop(self):
		global COMselectGbl
		global erreurGbl
		print("Capture evenement bouton STOP")
		erreurGbl = False
		#imageLedStop = wx.Bitmap("LedSTOP.png", wx.BITMAP_TYPE_ANY)
		self.m_bmpRunStop.SetBitmap(self.imageLedStop)
		self.m_RunStopTool.SetNormalBitmap(self.imagePause)
		# STOP si port série déjà ouvert
		if self.portSerie.isOpen(): 
			# Arrêt de la scrutation réception série
			if self.alive and self._reader_alive:
				print('Arret de la scrutation reception serie.')
				MsgLog(self, 'Arret de la scrutation reception serie ' + COMselectGbl)
				self._stop_reader()
				#Fermeture du port série
				try:
					self.portSerie.close()
				except NameError:
					print('Erreur a la fermeture du Port serie '+COMselectGbl)
					MsgLog(self,'Erreur a la fermeture du Port serie '+COMselectGbl)
					erreurGbl = True
					boxErr = wx.MessageDialog(None,'Erreur a la fermeture du Port serie '+COMselectGbl, 'Erreur:', wx.OK)
					reponse=boxErr.ShowModal()
					boxErr.Destroy()
				else:
					# pas d'erreur, on continue:
					erreurGbl = False
					# Fermeture du port série
					print('Passage en STOP: Port serie '+COMselectGbl+' ferme.')
					MsgLog(self,'Port serie '+COMselectGbl+' ferme.')
					#imageLedStop = wx.Bitmap("LedSTOP.png", wx.BITMAP_TYPE_ANY)
					self.m_bmpRunStop.SetBitmap(self.imageLedStop)
					self.m_RunStopTool.SetNormalBitmap(self.imagePause)
					global statusRunStopGbl
					statusRunStopGbl = 0


	# START: regroupe les fonctions tâche Reception
	def _start_reader(self):
		"""Start reader thread"""
		self.alive = True
		self._reader_alive = True
		# start serial->console thread
		self.receiver_thread = threading.Thread(target=self.reader)
		self.receiver_thread.setDaemon(True)
		self.receiver_thread.start()

	# STOP: Arrêt tâche de Reception
	def _stop_reader(self):
		"""Stop reader thread only, wait for clean exit of thread"""
		self.receiver_thread._Thread__stop()
		self.alive = False
		self._reader_alive = False
		self.receiver_thread.join()


		
	# Lecture du port Série			
	def reader(self):
		# la liste texte est: logTextCtrl.Value = ""
		"""loop and copy serial->console"""
		try:
			global gSerialLog
			while self.alive and self._reader_alive:
				#desactive le RUN/STOP clignotant pour optimiser la réception
				enableBlinkGbl = False
				#data = character(self.serial.read(1))
				data = self.portSerie.read(1)
				if self.repr_mode == 9:
					# direct output, just have to care about newline setting
#					gSerialLog = gSerialLog + data
					self.logTextCtrl.WriteText(data)
				elif self.repr_mode == 0:
					# direct output, just have to care about newline setting
#					if data == '\r' and self.convert_outgoing == CONVERT_CR:
					# si reception CR
					if data == '\r':
						#sys.stdout.write('\n')
						self.logTextCtrl.WriteText('\n')
						MysqlInsert(self,"Uno", "1", gSerialLog)
						gSerialLog = ""
					else:
						#sys.stdout.write(data)
						self.logTextCtrl.WriteText(data)
						gSerialLog = gSerialLog + data
				elif self.repr_mode == 1:
					# escape non-printable, let pass newlines
					if self.convert_outgoing == CONVERT_CRLF and data in '\r\n':
						if data == '\n':
							self.logTextCtrl.WriteText('\n')
					elif data == '\r':
						pass
					elif data == '\n' and self.convert_outgoing == CONVERT_LF:
						self.logTextCtrl.WriteText('\n')
					elif data == '\r' and self.convert_outgoing == CONVERT_CR:
						self.logTextCtrl.WriteText('\n')
					else:
						self.logTextCtrl.WriteText(repr(data)[1:-1])
				elif self.repr_mode == 2:
					# escape all non-printable, including newline
					self.logTextCtrl.WriteText(repr(data)[1:-1])
				elif self.repr_mode == 3:
					# escape everything (hexdump)
					for c in data:
						sys.stdout.write("%s " % c.encode('hex'))
				sys.stdout.flush()
				enableBlinkGbl = True
		except serial.SerialException, e:
			self.alive = False
			# would be nice if the console reader could be interruptted at this
			# point...
			raise


	
	######## MENU [Fichier] ########
	# capture de l'événement selection menu <LogNew>
	def m_LogNewMnuEvt(self,event):
		print("Menu: Nouveau: Effacement des Logs")
		MsgLog(self,'Fichier Nouveau: Effacement des Logs')
		self.logTextCtrl.Value = ""
	# capture de l'événement selection menu <LogOpen>
	def m_LogOpenMnuEvt(self,event):
		global appliFolderName
		global logFileName
		global logFolderName
		global enableBlinkGbl
		print("Menu: Ouvrir Log")
		enableBlinkGbl = False
		# construction du chemin des Logs
#		logFolderName = os.path.join(appliFolderName, "Logs")
#						FileDialog(parent, message=FileSelectorPromptStr, defaultDir="", defaultFile="",
#										   wildcard=FileSelectorDefaultWildcardStr, style=FD_DEFAULT_STYLE,
#										   pos=DefaultPosition, size=DefaultSize, name=FileDialogNameStr)
		popupOpen = wx.FileDialog(self, "Ouvrir fichier log", self.logFolderName, self.logFileName,
										"Fichier texte (*.txt)|*.txt|All Files|*.*", wx.OPEN)
		if (popupOpen.ShowModal() == wx.ID_OK):
			self.logFileName = popupOpen.GetFilename()
			self.logFolderName = popupOpen.GetDirectory()
			try:
				# accès fichier en lecture
				pointeurFichier = file(os.path.join(self.logFolderName, self.logFileName), 'r')
				self.logTextCtrl.SetValue(pointeurFichier.read())
				pointeurFichier.close()
				MsgLog(self,'Fichier Ouvrir: ' + os.path.join(self.logFolderName, self.logFileName) + ' ouverture ok')
			except:
				MsgLog(self,'Erreur lecture du fichier: '+ os.path.join(self.logFolderName, self.logFileName))
				print('Erreur lecture du fichier: '+self.logFileName)
				boxErr = wx.MessageDialog(None,'Erreur lecture du fichier: '+self.logFileName, 'Erreur lecture fichier:', wx.OK)
				reponse=boxErr.ShowModal()
				boxErr.Destroy()
		popupOpen.Destroy()
		enableBlinkGbl = True
		
	# capture de l'événement selection menu <LogSave>
	def m_LogSaveMnuEvt(self,event):
		global enableBlinkGbl
		print("Menu: Enregistrer Logs")
		enableBlinkGbl = False
		# enregistre si fichier/dossier ont un nom
		if (self.logFileName !="") and (self.logFolderName != ""):
			try:
				# accès fichier en écriture
				pointeurFichier = file(os.path.join(self.logFolderName, self.logFileName), 'w')
				pointeurFichier.write(self.logTextCtrl.GetValue())
				MsgLog(self,'Fichier Enregistrer: ' + os.path.join(self.logFolderName, self.logFileName) + ' Sauvegarde ok')
				return True
			except:
				MsgLog(self,'Erreur ecriture du fichier: '+ os.path.join(self.logFolderName, self.logFileName))
				print('Erreur ecriture du fichier: '+self.logFileName)
				boxErr = wx.MessageDialog(None,'Erreur ecriture du fichier: '+self.logFileName, 'Erreur enregistrement fichier:', wx.OK)
				reponse=boxErr.ShowModal()
				boxErr.Destroy()
				return False
		# sinon popup <Enregistrer sous...>
		else:
			print('Fichier sans nom: go <Enregistrer sous...> ')
			self.m_LogSaveAsMnuEvt(self)
		enableBlinkGbl = True
		
	# capture de l'événement selection menu <LogSaveAs...>
	def m_LogSaveAsMnuEvt(self,event):
		global enableBlinkGbl
		print("Menu: Enregistrer Logs sous...")
		enableBlinkGbl = False
		popupSaveAs = wx.FileDialog(self, "Enregister fichier log sous...", self.logFolderName, self.logFileName,
						"Fichier texte (*.txt)|*.txt|All Files|*.*", wx.SAVE)
		if (popupSaveAs.ShowModal() == wx.ID_OK):
			self.logFileName = popupSaveAs.GetFilename()
			self.logFolderName = popupSaveAs.GetDirectory()
			# on réutilise la fonction d'enregistrement
			if self.m_LogSaveMnuEvt(self):
				#self.FenetrePrincipaleClass.SetTitle(self.APP_NAME + " - [" +self.logFileName+ "]")
				print("Serial SQL Logger - [" + self.logFileName + "]")
				MsgLog(self,'Fichier Enregistrer sous: ' + os.path.join(self.logFolderName, self.logFileName) + ' Sauvegarde ok')
		enableBlinkGbl = True

	# capture de l'événement selection menu <ProfileNew>
	def m_ProfileNewMnuEvt( self, event ):
		global AppliTitreGbl
		global ProfileNameGbl
		global COMselectGbl
		global COMvitesseGbl
		# Init partie fichier profile + titre appli
		ProfileNameGbl = "Aucun"
		self.profileFileName = ""
		self.profileFolderName = ""
		AppliTitreCreation()
		screenHome.SetTitle(AppliTitreGbl)
		# Init partie décodage
		self.m_ExtractHorodateChk.SetValue(False)
		self.m_ExtractCategorieChk.SetValue(False)
		self.m_CategorieTxt.Value = ""
		self.m_ExtractPrioriteChk.SetValue(False)
		self.m_PrioriteInt.Value = 0
		self.m_separateurCbx.SetValue("")
		self.m_separateurCbx.Enable(False)
		
	# capture de l'événement selection menu <ProfileOpen>
	def m_ProfileOpenMnuEvt( self, event ):
		global AppliTitreGbl
		global ProfileNameGbl
		global COMselectGbl
		global COMvitesseGbl
		global gExtractHorodatageChk
		global gExtractCategorieChk
		global gExtractCategorieTxt
		global gExtractPrioriteChk
		global gExtractPrioriteInt
		global gCaractereSeparateurTxt
		print("Menu: Ouvrir Profile")
		enableBlinkGbl = False
		popupOpen = wx.FileDialog(self, "Ouvrir fichier profile", self.profileFolderName, self.profileFileName,
										"Fichier profile (*.cfg)|*.cfg|All Files|*.*", wx.OPEN)
		if (popupOpen.ShowModal() == wx.ID_OK):
			self.profileFileName   = popupOpen.GetFilename()
			self.profileFolderName = popupOpen.GetDirectory()
			print('popupOpen: '+self.profileFolderName+' '+self.profileFileName)
			try:
				# accès fichier en lecture
				pointeurFichierProfile = file(os.path.join(self.profileFolderName, self.profileFileName), 'r')
			except Exception:
				MsgLog(self,'Erreur lecture du fichier: '+ os.path.join(self.profileFolderName, self.profileFileName))
				print('Erreur lecture du fichier: '+ os.path.join(self.profileFolderName, self.profileFileName))
				boxErr = wx.MessageDialog(None,'Erreur lecture du fichier: '+ os.path.join(self.profileFolderName,
										  self.profileFileName), 'Erreur lecture fichier:', wx.OK)
				reponse=boxErr.ShowModal()
				boxErr.Destroy()
			else:
				# pas d'erreur, le fichier est bien lu, on continue:
				# gestion du profile avec ConfigParser:
				profile = ConfigParser.ConfigParser()
				# lecture du profile selectionné par popupOpen
				profile.read(os.path.join(self.profileFolderName, self.profileFileName))
				COMselectGbl = profile.get   ('LiaisonSerie', 'portcom')
				COMvitesseGbl= profile.getint('LiaisonSerie', 'vitesse')
				gExtractHorodatageChk		= profile.getboolean('Decodage_Logs', 'Extract_Horodatage_Chk')
				gExtractCategorieChk		= profile.getboolean('Decodage_Logs', 'Extract_Categorie_Chk')
				gExtractCategorieTxt		= profile.get(       'Decodage_Logs', 'Extract_Categorie_Txt')
				gExtractPrioriteChk			= profile.getboolean('Decodage_Logs', 'Extract_Priorite_Chk')
				gExtractPrioriteInt			= profile.getint(    'Decodage_Logs', 'Extract_Priorite_Txt')
				gCaractereSeparateurTxt		= profile.get(       'Decodage_Logs', 'Caractere_Separateur_Txt')
				# test si le port série est bien sur la machine
				try:
					self.portSerie = serial.Serial(str(COMselectGbl),int(COMvitesseGbl))
				except Exception:
					print("Erreur: le port serie "+COMselectGbl+" n'est pas sur cette machine")
					MsgLog(self,"Erreur: le port serie "+COMselectGbl+" n'est pas sur cette machine")
					erreurGbl = True
					boxErr = wx.MessageDialog(None,"Erreur: le port serie "+COMselectGbl+" n'est pas sur cette machine", 'Erreur:', wx.OK)
					reponse=boxErr.ShowModal()
					boxErr.Destroy()
					COMselectGbl  = "Non select."
				else:
					# pas d'erreur, le port serie est sur la machine, on continue:
					erreurGbl = False
					CheckVitesse(COMvitesseGbl)		# coche la vitesse
					self.m_statusComTextStat.SetLabel("Port serie: " + COMselectGbl)
					self.m_statusActionTextStat.SetLabel("Pret.")
					MsgLog(self,"Port COM: "+COMselectGbl+"  Vitesse Port: "+ str(COMvitesseGbl))
					self.m_statusVitesseTextStat.SetLabel("Vitesse: "+str(COMvitesseGbl)+" bds")
					# memorisation du profile pour titre appli
					ProfileNameGbl = self.profileFileName
					#Fermeture du port série
					self.portSerie.close()
					# fermeture du fichier profile
					pointeurFichierProfile.close()
					DecodageRefresh(self)
					MsgLog(self,'Fichier Ouvrir: ' + os.path.join(self.profileFolderName, self.profileFileName) + ' ouverture ok')
			popupOpen.Destroy()
			enableBlinkGbl = True
			AppliTitreCreation()
			screenHome.SetTitle(AppliTitreGbl)

	# capture de l'événement selection menu <ProfileSave>
	def m_ProfileSaveMnuEvt( self, event ):
		global COMselectGbl
		global COMvitesseGbl
		global enableBlinkGbl
		global gExtractHorodatageChk
		global gExtractCategorieChk
		global gExtractCategorieTxt
		global gExtractPrioriteChk
		global gExtractPrioriteInt
		global gCaractereSeparateurTxt
		print("Menu: Enregistrer Profile")
		enableBlinkGbl = False
		# enregistre si fichier/dossier ont un nom
		if (self.profileFileName !="") and (self.profileFolderName != ""):
			try:
				# accès fichier en écriture
				pointeurFichierProfile = file(os.path.join(self.profileFolderName, self.profileFileName), 'w')
				profile = ConfigParser.ConfigParser()
				profile.add_section('LiaisonSerie')
				profile.set('LiaisonSerie', 'PortCOM', COMselectGbl)
				profile.set('LiaisonSerie', 'Vitesse', COMvitesseGbl)
				profile.add_section('Decodage_Logs')
				profile.set('Decodage_Logs', 'Extract_Horodatage_Chk',		str(gExtractHorodatageChk))
				profile.set('Decodage_Logs', 'Extract_Categorie_Chk',		str(gExtractCategorieChk))
				profile.set('Decodage_Logs', 'Extract_Categorie_Txt',		gExtractCategorieTxt)
				profile.set('Decodage_Logs', 'Extract_Priorite_Chk',		str(gExtractPrioriteChk))
				profile.set('Decodage_Logs', 'Extract_Priorite_Txt',		str(gExtractPrioriteInt))
				profile.set('Decodage_Logs', 'Caractere_Separateur_Txt',	gCaractereSeparateurTxt)
				print("Dossier = " + self.profileFolderName)
				print("Fichier = " + self.profileFileName)
				print("gExtractHorodatageChk      = " + str(gExtractHorodatageChk))
				print("gExtractCategorieChk       = " + str(gExtractCategorieChk))
				print("gExtractCategorieTxt       = " + gExtractCategorieTxt)
				print("gExtractPrioriteChk        = " + str(gExtractPrioriteChk))
				print("gExtractPrioriteInt        = " + str(gExtractPrioriteInt))
				print("gCaractereSeparateurTxt    = " + gCaractereSeparateurTxt)
				MsgLog(self,'Enregistrer profile: '+os.path.join(self.profileFolderName, self.profileFileName))
				profile.write(open(os.path.join(self.profileFolderName, self.profileFileName), 'w'))
				MsgLog(self,'Fichier Enregistrer: ' + os.path.join(self.profileFolderName, self.profileFileName) + ' Sauvegarde ok')
				return True
			except:
				MsgLog(self,'Erreur ecriture du fichier: '+ os.path.join(self.profileFolderName, self.profileFileName))
				print('Erreur ecriture du fichier: '+self.profileFileName)
				boxErr = wx.MessageDialog(None,'Erreur ecriture du fichier: '+self.profileFileName, 'Erreur enregistrement fichier:', wx.OK)
				reponse=boxErr.ShowModal()
				boxErr.Destroy()
				return False
		# sinon popup <Enregistrer sous...>
		else:
			print('Fichier sans nom: go <Enregistrer Profile sous...> ')
			self.m_ProfileSaveAsMnuEvt(self)
		enableBlinkGbl = True
		
		
	# capture de l'événement selection menu <ProfileSaveAs>
	def m_ProfileSaveAsMnuEvt( self, event ):
		global AppliTitreGbl
		global ProfileNameGbl
		global enableBlinkGbl
		print("Menu: Enregistrer Profile sous...")
		enableBlinkGbl = False
		popupSaveAs = wx.FileDialog(self, "Enregister fichier profile sous...", self.profileFolderName, self.profileFileName,
						"Fichier profile (*.cfg)|*.cfg|All Files|*.*", wx.SAVE)
		if (popupSaveAs.ShowModal() == wx.ID_OK):
			self.profileFileName = popupSaveAs.GetFilename()
			self.profileFolderName = popupSaveAs.GetDirectory()
			# on réutilise la fonction d'enregistrement
			if self.m_ProfileSaveMnuEvt(self):
				#self.FenetrePrincipaleClass.SetTitle(self.APP_NAME + " - [" +self.profileFileName+ "]")
				print("Serial SQL Logger - [" + self.profileFileName + "]")
				MsgLog(self,'Fichier Enregistrer sous: ' + os.path.join(self.profileFolderName, self.profileFileName) + ' Sauvegarde ok')
				# memorisation du profile
				ProfileNameGbl = self.profileFileName
		enableBlinkGbl = True
		AppliTitreCreation()
		screenHome.SetTitle(AppliTitreGbl)

	# capture de l'événement selection menu <Quiter>
	def m_quiterMnuEvt(self,event):
		print("Menu: Quiter")
		MsgLog(self,'Menu: Quiter')
		global statusRunStopGbl
		if (statusRunStopGbl == 1):
			self.portSerie.close()
			print('Fermeture Port serie '+COMselectGbl +' car reste ouvert...')
			MsgLog(self,'Fermeture Port serie '+COMselectGbl +' car reste ouvert...')
		# fermeture de l'appli
		#screenHome.StopThread()				#stop reader thread
		#screenHome.portSerie.close()			#cleanup
		#screenHome.Destroy()					#close windows, exit app
		screenHome.Close( True )

	######## MENU [Port COM] ########
	# menu <Actualiser>
	def m_COMactualiserMnuEvt(self,event):
		global COMselectGbl
		# scan port serie dispo:
		print("<Actualiser> ")
		MsgLog(self,'Recherche des Ports COM disponibles ...')
		self.m_statusActionTextStat.SetLabel("Recherche ports COM en cours...")
		FindCOM(self)
		print("<FIN> ")
		self.m_statusActionTextStat.SetLabel("Recherche terminer: choisissez un port serie")
	#  menu <Select.Manuelle>
	def m_COMmanuMnuEvt(self,event):
		global COMselectGbl
		# scan port serie dispo:
		print("<Select.Manuel> ")
		box = wx.TextEntryDialog(None, "Entrez le nom du port serie:\n  Exemple: COM4", "Port serie:", "COM4")
		if box.ShowModal()==wx.ID_OK:
			COMselectGbl=box.GetValue()
		print("Selection manuelle: "+ COMselectGbl)
		MsgLog(self,"Selection manuelle Port COM: "+ COMselectGbl)
		self.m_statusActionTextStat.SetLabel("Selection manuelle: "+ COMselectGbl)
		self.m_statusComTextStat.SetLabel("Port serie: " + COMselectGbl)
	# capture de l'événement selection menu COM non selectionné
	def m_COMnonSelectEvt(self,event):
		global COMselectGbl
		global COMvitesseGbl
		COMselectGbl = "Non select."
		COMvitesseGbl = 115200
		MsgLog(self,"Nouveau profile:    Port COM: "+COMselectGbl+"    Vitesse Port: "+ str(COMvitesseGbl))
		self.m_statusVitesseTextStat.SetLabel("Vitesse: "+str(COMvitesseGbl)+" bds")
		self.m_statusComTextStat.SetLabel("Port serie: "+COMselectGbl)

	# capture de l'événement selection ComboBox Port COM
	def m_portComCbxEvt( self, event ):
		global COMselectGbl
		bcb = event.GetEventObject()
		idx = event.GetInt()
		COMselectGbl  = bcb.GetString(idx)					# correction depuis wx2.8-examples
		print("COMselectGbl: " + COMselectGbl)
		MsgLog(self,"Selection Port COM: "+ COMselectGbl)
		self.m_statusComTextStat.SetLabel("Port serie: " + COMselectGbl)
		self.m_statusActionTextStat.SetLabel("Pret.")

	def m_portComCbxEvtOnText( self, event ):
		event.Skip()
	
	def m_portComCbxEvtOnTextEnter( self, event ):
		event.Skip()


	# capture de l'événement ComboBox Port COM Validation <Enter>
	def m_portComCbxEvtOnTextEnter( self, event ):
		global COMselectGbl
		COMselectGbl = event.GetString()
		print("COMselectGbl: " + COMselectGbl)
		MsgLog(self,"Selection Port COM: "+ COMselectGbl)
		self.m_statusComTextStat.SetLabel("Port serie: " + COMselectGbl)
		self.m_statusActionTextStat.SetLabel("Pret.")

	######## MENU [Vitesse COM] ########
	# capture de l'événement selection menu <115200 bds>
	def m_115200mnuEvt(self,event):
		global COMvitesseGbl
		COMvitesseGbl = 115200
		print("COMvitesseGbl: " + str(COMvitesseGbl))
		global COMselectGbl
		MsgLog(self,"Port COM: "+COMselectGbl+"  Vitesse: "+ str(COMvitesseGbl))
		self.m_statusVitesseTextStat.SetLabel("Vitesse: "+str(COMvitesseGbl)+" bds")
	# menu <57600 bds>
	def m_57600mnuEvt(self,event):
		global COMvitesseGbl
		COMvitesseGbl = 57600
		print("COMvitesseGbl: " + str(COMvitesseGbl))
		global COMselectGbl
		MsgLog(self,"Port COM: "+COMselectGbl+"  Vitesse: "+ str(COMvitesseGbl))
		self.m_statusVitesseTextStat.SetLabel("Vitesse: "+str(COMvitesseGbl)+" bds")
	# menu <19200 bds>
	def m_19200mnuEvt(self,event):
		global COMvitesseGbl
		COMvitesseGbl = 19200
		print("COMvitesseGbl: " + str(COMvitesseGbl))
		global COMselectGbl
		MsgLog(self,"Port COM: "+COMselectGbl+"  Vitesse: "+ str(COMvitesseGbl))
		self.m_statusVitesseTextStat.SetLabel("Vitesse: "+str(COMvitesseGbl)+" bds")
	# menu <9600 bds>
	def m_9600mnuEvt(self,event):
		global COMvitesseGbl
		COMvitesseGbl = 9600
		print("COMvitesseGbl: " + str(COMvitesseGbl))
		global COMselectGbl
		MsgLog(self,"Port COM: "+COMselectGbl+"  Vitesse: "+ str(COMvitesseGbl))
		self.m_statusVitesseTextStat.SetLabel("Vitesse: "+str(COMvitesseGbl)+" bds")
	# menu <4800 bds>
	def m_4800mnuEvt(self,event):
		global COMvitesseGbl
		COMvitesseGbl = 4800
		print("COMvitesseGbl: " + str(COMvitesseGbl))
		global COMselectGbl
		MsgLog(self,"Port COM: "+COMselectGbl+"  Vitesse: "+ str(COMvitesseGbl))
		self.m_statusVitesseTextStat.SetLabel("Vitesse: "+str(COMvitesseGbl)+" bds")
	# menu <2400 bds>
	def m_2400mnuEvt(self,event):
		global COMvitesseGbl
		COMvitesseGbl = 2400
		print("COMvitesseGbl: " + str(COMvitesseGbl))
		global COMselectGbl
		MsgLog(self,"Port COM: "+COMselectGbl+"  Vitesse: "+ str(COMvitesseGbl))
		self.m_statusVitesseTextStat.SetLabel("Vitesse: "+str(COMvitesseGbl)+" bds")
	# menu <1200 bds>
	def m_1200mnuEvt(self,event):
		global COMvitesseGbl
		COMvitesseGbl = 1200
		print("COMvitesseGbl: " + str(COMvitesseGbl))
		global COMselectGbl
		MsgLog(self,"Port COM: "+COMselectGbl+"  Vitesse: "+ str(COMvitesseGbl))
		self.m_statusVitesseTextStat.SetLabel("Vitesse: "+str(COMvitesseGbl)+" bds")

	######## MENU [Système] ########
	# menu <gestionnaire de periphérique>
	def m_gestPeriphMnuEvt(self,event):
		os.startfile('devmgmt.msc')
		MsgLog(self,"Menu Systeme: gestionnaire de peripherique")

	########==== ToolBar ====########
	# icone <Find Port>
	def m_findPortToolEvt( self, event ):
		# scan port serie dispo:
		print("<Actualiser> ")
		MsgLog(self,'Recherche des Ports COM disponibles ...')
		self.m_statusActionTextStat.SetLabel("Recherche ports COM en cours...")
		FindCOM(self)
		print("<FIN> ")
		self.m_statusActionTextStat.SetLabel("Recherche terminer: choisissez un port serie")

	# Icone <Run Stop>
	def m_RunStopToolEvt(self,event):
		global statusRunStopGbl
		if statusRunStopGbl == 0:
			self.AppliStart()
		else:
			self.AppliStop()

	# Icone <Quiter>
	def m_toolQuiterEvt(self,event):
		global COMselectGbl
		print("Menu: Quiter")
		MsgLog(self,'Menu: Quiter')
		global statusRunStopGbl
		if (statusRunStopGbl == 1):
			self.portSerie.close()
			print('Fermeture Port serie '+COMselectGbl +' car reste ouvert...')
			MsgLog(self,'Fermeture Port serie '+COMselectGbl +' car reste ouvert...')
		screenHome.Close( True )


#####################################################
# 					Fonction MsgLog(self,message)
# Principe	:	Retourne l'horodatage
#				Format: YYYY-MM-JJ HH:MM:SS espace
# Dépandence:	import time
# Appelé par:	Les fonctions action de l'appli
# 2014-06-01:	Création
#####################################################
def MsgLog(self,message):
	global ProfileNameGbl
	global COMselectGbl
	global COMvitesseGbl
	#self.logAppliTextCtrl.WriteText(1, 8, wx.TextAttr("RED", "YELLOW"))
	#self.logAppliTextCtrl.WriteText(wx.TextAttr("RED", "YELLOW"))
	self.logAppliTextCtrl.WriteText("\n" + time.strftime("%Y-%m-%d %H:%M:%S  " + message))
	#screenHome.SetTitle("Serial to SQL Logger - Profile="+ProfileNameGbl+" COM="+COMselectGbl+" Vitesse="+str(COMvitesseGbl)+" bds")

#####################################################
# 					Fonction AppliTitre(self)
# Principe	:	Retourne le titre de l'appli'
# Dépandence:	Variables globales réglages appli
# Appelé par:	menu ProfileOpen/ProfileSaveAS/COM/Vitesse
# 2014-07-22:	Création
#####################################################
def AppliTitreCreation():
	global AppliTitreGbl
	global ProfileNameGbl
	global COMselectGbl
	global COMvitesseGbl
	AppliTitreGbl = "Serial to SQL Logger - Profile: ["+ProfileNameGbl+"]  Port:"+COMselectGbl+"  Vitesse:"+str(COMvitesseGbl)+" bds"

#####################################################
# 					Fonction scan()
# Principe	:	Scan les ports COM disponibles
# Dépandence:	import serial
# Appelé par:	Fonction FindCOM()
# 2014-04-19:	Création
#####################################################
def scan():
	"""scan for available ports. return a list of tuples (num, name)"""
	available = []
	for i in range(100):
		try:
			s = serial.Serial(i)
			available.append( (i, s.portstr))
			s.close()   # explicit close 'cause of delayed GC in java
		except serial.SerialException:
			pass
	return available

#####################################################
# 					Fonction FindCOM()
# Principe	:	Désactive les ports dans le menu Port COM
# Dépandence:	import Serial_SQL_Logger_GUI
# Appelé par:	Fonction événement m_COMactualiserMnuEvt
# 2014-04-19:	Création
#####################################################
def FindCOM(self):
	# efface la liste dans ComboBox
	self.m_portComCbx.Clear()
	print "Ports dispo:"
	# scan port serie dispo:
	for n,s in scan():
		print "(%d) %s" % (n,s)
		MsgLog(self,"%s" % (s))
		# activation menu port serie en fonction des COM dispo
		#self.m_portComCbx.Append(s)
		self.m_portComCbx.Append(s)
		#AddMemnuPortCOM(s)

#####################################################
# 					Fonction AddMemnuPortCOM(COMname)
# Principe	:	Ajoute dynamiquement les ports COM
#				dans le menu Port COM
# Dépandence:	import Serial_SQL_Logger_GUI
# Appelé par:	Fonction FindCOM()
# 2014-07-26:	Création
#####################################################
def AddMemnuPortCOM(COMname):
	self.COMname = wx.MenuItem( self.m_portComMnu, wx.ID_ANY, COMname, wx.EmptyString, wx.ITEM_RADIO )
	self.m_portComMnu.AppendItem( self.m_COM1mnu )
	self.m_COM1mnu.Enable( True )
	self.Bind( wx.EVT_MENU, self.m_COM1mnuEvt, id = self.m_COM1mnu.GetId() )

###############################################################
# 					Fonction CheckVitesse(COMname)
# Principe	:	Selectionne la vitesse dans menu Vitesse COM
# Dépandence:	import Serial_SQL_Logger_GUI
# Appelé par:	LectureProfile
# 2014-07-21:	Création
###############################################################
def CheckVitesse(vitesse):
	if vitesse == 115200:
		screenHome.m_115200mnu.Check( True )
	if vitesse == 57600:
		screenHome.m_57600mnu.Check( True )
	if vitesse == 19200:
		screenHome.m_19200mnu.Check( True )
	if vitesse == 9600:
		screenHome.m_9600mnu.Check( True )
	if vitesse == 4800:
		screenHome.m_4800mnu.Check( True )
	if vitesse == 2400:
		screenHome.m_2400mnu.Check( True )
	if vitesse == 1200:
		screenHome.m_1200mnu.Check( True )

###############################################################
# 					Fonction SaveAs(self, folderName, fileName)
# Principe	:	generique Enregistrer sous
# Dépandence:	import wx
# Appelé par:	Fonction m_LogSaveMnuEvt()
#						 m_ProfileSaveMnuEvt()
# 2014-07-20:	Création
###############################################################
def Save(self, folderName, fileName):
	global COMselectGbl
	global COMvitesseGbl
	global enableBlinkGbl
	print("Menu: Enregistrer Logs")
	enableBlinkGbl = False
	# enregistre si fichier/dossier ont un nom
	if (self.logFileName !="") and (self.logFolderName != ""):
		try:
			# accès fichier en écriture
			pointeurFichier = file(os.path.join(folderName, fileName), 'w')
			# écriture du fichier
			pointeurFichier.write(COMselectGbl)
			MsgLog(self,'Fichier Enregistrer: ' + os.path.join(FolderName, FileName) + ' Sauvegarde ok')
			return True
		except:
			MsgLog(self,'Erreur ecriture du fichier: '+ os.path.join(self.logFolderName, self.logFileName))
			print('Erreur ecriture du fichier: '+self.logFileName)
			boxErr = wx.MessageDialog(None,'Erreur ecriture du fichier: '+self.logFileName, 'Erreur enregistrement fichier:', wx.OK)
			reponse=boxErr.ShowModal()
			boxErr.Destroy()
			return False
	# sinon popup <Enregistrer sous...>
	else:
		print('Fichier sans nom: go <Enregistrer sous...> ')
		self.m_LogSaveAsMnuEvt(self)
	enableBlinkGbl = True

#####################################################
# 					Fonction Separateur(self)
# Principe	:	Actualise Activation/Désactivation
#				de la selection caractère séparateur
# Dépandence:	Variables globales extractions
# Appelé par:	bouton checkBox GUI
# 2014-09-29:	Création
#####################################################
def SeparateurEnable(self):
	global gExtractHorodatageChk
	global gExtractCategorieChk
	global gExtractPrioriteChk
	if gExtractHorodatageChk or gExtractCategorieChk or gExtractPrioriteChk:
		gCaractereSeparateurEnable = True		# update image variable globale
		# Activation comboBox 'Caractère séparateur'
		self.m_separateurCbx.Enable(True)
	else:
		gCaractereSeparateurEnable = False		# update image variable globale
		# Désactivation comboBox 'Caractère séparateur'
		self.m_separateurCbx.Enable(False)
	#print "m_ExtractPrioriteChkEvt ",gExtractPrioriteChk

#####################################################
# 					Fonction DecodageRefresh(self)
# Principe	:	Actualise Activation/Désactivation
#				de la selection checkbox décodage
# Dépandence:	Variables globales extractions
# Appelé par:	bouton checkBox GUI
# 2014-10-11:	Création
#####################################################
def DecodageRefresh(self):
	global gExtractHorodatageChk
	global gExtractCategorieChk
	global gExtractCategorieTxt
	global gExtractPrioriteChk
	global gExtractPrioriteInt
	global gCaractereSeparateurTxt
	global gCaractereSeparateurEnable
	print('gExtractHorodatageChk=      ' + str(gExtractHorodatageChk))
	print('gExtractCategorieChk=       ' + str(gExtractCategorieChk))
	print('gExtractCategorieTxt=       ' + gExtractCategorieTxt)
	print('gExtractPrioriteChk=        ' + str(gExtractPrioriteChk))
	print('gExtractPrioriteInt=        ' + str(gExtractPrioriteInt))
	print('gCaractereSeparateurTxt=    ' + gCaractereSeparateurTxt)
	self.m_ExtractHorodateChk.SetValue(gExtractHorodatageChk)
	self.m_ExtractCategorieChk.SetValue(gExtractCategorieChk)
	self.m_CategorieTxt.Value = gExtractCategorieTxt
	self.m_ExtractPrioriteChk.SetValue(gExtractPrioriteChk)
	self.m_PrioriteInt.Value = gExtractPrioriteInt
	self.m_separateurCbx.SetValue(gCaractereSeparateurTxt)
	self.m_separateurCbx.Enable(gCaractereSeparateurEnable)
	SeparateurEnable(self)
	

#####################################################
# 					Fonction MysqlInsert(self)
# Principe	:	Enregistre les logs dans la base MySQL
# Dépandence:	Aucune
# Appelé par:	bouton GUI, fonction port série
# 2014-09-23:	Création
#####################################################
def MysqlInsert(self,categorie,niv_detail,message):
	try:
		#MysqlInsert: print "base MySQL ouverture..."
		db = MySQLdb.connect(host="192.168.1.150",user="root",passwd="mysql",db="serial_sql_logger")
	except Exception:
		# appel popup erreur connexion MySQL
		boxErr = wx.MessageDialog(None,'Erreur connexion MySQL vers 192.168.1.150', 'Erreur:', wx.OK)
		reponse=boxErr.ShowModal()
		boxErr.Destroy()
	else:
		#print "MysqlInsert: base MySQL ouverte"
		cur = db.cursor() 
		dateTime= (time.strftime("%Y-%m-%d ") + time.strftime("%H:%M:00"))
		requete=        "INSERT INTO arduino (horodatage,categorie,niv_detail,message) "
		requete=requete+"VALUES ('"+dateTime+"','"+categorie+"','"+niv_detail+"','"+message+"')"
		try:
			# execute la requete
			cur.execute(requete)
			#print "MysqlInsert: ...Mise a jour de la base"
			db.commit()
		except Exception:
			print "MysqlInsert: Erreur avec la Requete= " + requete
			print "MysqlInsert: ...Retour etat precedant de la base"
			db.rollback()
		else:
			#print "MysqlInsert: Requete executee avec:"
			#print requete
			db.close()
			#print "MysqlInsert: base fermee"
			print "MysqlInsert: ok"




#================ DEBUT APPLI ================
# Dossier de l'appli
appliFolderName = os.getcwd()
print "appliFolderName= " + appliFolderName
# detection de l'OS
print "Architecture systeme:"
print platform.architecture()
print "Systeme d'exploitation:"
print platform.platform()
plateformeComplete = platform.platform()
plateformeTab = plateformeComplete.split('-')
g_OSname    = plateformeTab[0]
g_OSversion = plateformeTab[1]
# detection detail distrib
if (g_OSname == 'Linux'):
	g_OSdistrib = plateformeTab[5]+' '+plateformeTab[6]
else:
	g_OSdistrib = plateformeTab[3]
# detection architecture 32/64 bits
g_archiTab     = platform.architecture()
g_architectBits = g_archiTab[0]+'s'
print('g_architectBits='+g_architectBits)

# start GUI
app = wx.App(False)
#wx.InitAllImageHandlers()
# creation de l'object screenHome depuis la class screenMain
screenHome = screenMain(None)
# scan port serie dispo:
#FindCOM()
compteurGbl 	= 0
erreurGbl		= False
erreurBlinkGbl 	= False
runBlinkGbl		= False
enableBlinkGbl	= True
enableErrBlinkGbl= True
bmpCirculaireIndexGbl=1
# init zones de status appli
AppliTitreGbl 	= "Serial SQL Logger"
ProfileNameGbl	= "Aucun"
COMselectGbl  	= "Non select."
COMvitesseGbl 	= 115200
statusRunStopGbl= 0
gSerialLog      = ""
gExtractHorodatageChk	  = False
gExtractCategorieChk	  = False
gExtractCategorieTxt	  = ""
gExtractPrioriteChk		  = False
gExtractPrioriteInt		  = 1
gCaractereSeparateurTxt	  = ""
gCaractereSeparateurEnable= False

screenHome.m_statusActionTextStat.SetLabel("Choisissez un port serie.")
screenHome.m_statusComTextStat.SetLabel("Port serie: "+COMselectGbl)
screenHome.m_statusVitesseTextStat.SetLabel("Vitesse: "+str(COMvitesseGbl)+" bds")
# affichage de l'écran principal
screenHome.Show(True)
# Démarrage de l'applications
app.MainLoop()

