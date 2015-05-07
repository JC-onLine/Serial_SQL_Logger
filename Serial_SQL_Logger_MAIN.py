# -*- coding: utf8 -*-

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
#####################################################################################

#HIGH LOW INPUT INPUT_PULLUP OUTPUT DEC BIN HEX OCT bitRead bitWrite bitSet bitClear bit highByte lowByte analogReference analogRead analogWrite attachInterrupt detachInterrupt delay delayMicroseconds digitalWrite digitalRead interrupts millis micros noInterrupts noTone pinMode pulseIn shiftIn shiftOut tone yield Serial Serial1 Serial2 Serial3 SerialUSB begin end peek read print println available availableForWrite flush setTimeout find findUntil parseInt parseFloat readBytes readBytesUntil readString readStringUntil trim toUpperCase toLowerCase charAt compareTo concat endsWith startsWith equals equalsIgnoreCase getBytes indexOf lastIndexOf length replace setCharAt substring toCharArray toInt Keyboard Mouse press release releaseAll accept click move isPressed setup loop drawLine UTFT UTouch DueGUI InitTouch InitGUI UTouch SPI_Flash_init InitLCD clrScr fillScr setColorLong setBackColorLong setColor setBackColor drawPixel drawLine drawRect drawRoundRect fillRect fillRoundRect drawCircle fillCircle print printNumI printNumF setFont drawBitmap lcdOff lcdOn setContrast getDisplayXSize getDisplayYSize preserveColours restoreColours updatingScreen finishedUpdatingScreen withinBounds displayNumFormat calculate_x calculate_y drawAngledLine startTimer stopTimer restartTimer addButton addTextInput drawTextInputText drawTextInput updateTextInput addCheckBox drawCheckBox addCycleButton drawCycleButton drawButton checkButton checkAllButtons addPanel drawPanel addLabel drawLabel addShape drawShape addImage drawImage addAnalogueClock drawAnalogueClock addDigitalClock_Time drawDigitalClock_Time addDigitalClock_Date drawDigitalClock_Date drawHands drawAnalogueClock_dividers setObjectTime setObjectDate clearAllObjects redrawAllObjects redrawChangedObjects redrawObject clearRectObject makeObjectInvisible makeObjectVisible DueGUI_tickHandler KEYWORD2 clearObjectArea objectVisible drawSingleKey makePopUp clearPopUp returnBoolValue  returnIntValue returnStringValue findObjectByURN HandleShowButtons HandleShowLoop showCalibrate CTE50 CTE70 shutdown setScanLimit setIntensity clearDisplay setLed setRow setColumn setDigit setChar

from __future__ import unicode_literals
# importation la librairie wxWidget
import wx
# importation de la partie GUI
import Serial_SQL_Logger_GUI
# acces à la librairie du port série
import serial
import glob
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

# variables globales
# Série
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
# encodage
global gDecodeSerieTxt				# decodage série
global gDecodeSerieUTF8Chk
global gDecodeSerieWin1252Chk
global gDecodeSerieISO_8859_15Chk
global gDecodeSerieCP850Chk
global gEncodeSqlTxt				# encodage SQL
global gEncodeSqlUTF8Chk
global gEncodeSqlWin1252Chk
global gEncodeSqlISO_8859_15Chk
global gEncodeSqlCP850Chk
global gEncodeGuiTxt				# encodage GUI
global gEncodeGuilUTF8Chk
global gEncodeGuiWin1252Chk
global gEncodeGuiISO_8859_15Chk
global gEncodeGuiCP850Chk
# SQL
global gSQLenable
global gSQLcompleteLineTxt
global gExtractHorodatageChk
global gExtractCategorieChk
global gExtractCategorieTxt
global gExtractNivDetailChk
global gExtractNivDetailNum
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


# Gestion réception reprise de l'exemple wxTerminal.py de pyserial
# création événement 
#----------------------------------------------------------------------
# Create an own event type, so that GUI updates can be delegated
# this is required as on some platforms only the main thread can
# access the GUI without crashing. wxMutexGuiEnter/wxMutexGuiLeave
# could be used too, but an event is more elegant.
SERIALRX = wx.NewEventType()
# affecte l'événement à la réception du port série
EVT_SERIALRX = wx.PyEventBinder(SERIALRX, 0)

class SerialRxEvent(wx.PyCommandEvent):
	eventType = SERIALRX
	def __init__(self, windowID, data):
		wx.PyCommandEvent.__init__(self, self.eventType, windowID)
		self.data = data

class screenMain(Serial_SQL_Logger_GUI.FenetrePrincipaleClass):
	# constructor
	def __init__(self,parent):
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
		self.imageLedStop   = wx.Bitmap(os.path.join(os.path.curdir,"Icons","LED","LedSTOP.png"   ),wx.BITMAP_TYPE_ANY)
		self.imageLedRunOn  = wx.Bitmap(os.path.join(os.path.curdir,"Icons","LED","LedRUN_ON.png" ),wx.BITMAP_TYPE_ANY)
		self.imageLedRunOff = wx.Bitmap(os.path.join(os.path.curdir,"Icons","LED","LedRUN_OFF.png"),wx.BITMAP_TYPE_ANY)
		self.imageLedErrOn  = wx.Bitmap(os.path.join(os.path.curdir,"Icons","LED","LedERR_ON.png" ),wx.BITMAP_TYPE_ANY)
		self.imageLedErrOff = wx.Bitmap(os.path.join(os.path.curdir,"Icons","LED","LedERR_OFF.png"),wx.BITMAP_TYPE_ANY)
		self.imagePause     = wx.Bitmap(os.path.join(os.path.curdir,"Icons","ToolBar","Oxygen","media-playback-pause.png"),wx.BITMAP_TYPE_ANY)
		self.imagePlay      = wx.Bitmap(os.path.join(os.path.curdir,"Icons","ToolBar","Oxygen","media-playback-start.png"),wx.BITMAP_TYPE_ANY)
		self.imageSQLon     = wx.Bitmap(os.path.join(os.path.curdir,"Icons","ToolBar","data-enable_32x32.png"),wx.BITMAP_TYPE_ANY)
		self.imageSQLoff    = wx.Bitmap(os.path.join(os.path.curdir,"Icons","ToolBar","data-disable_32x32.png"),wx.BITMAP_TYPE_ANY)
		self.bmpCirculaireIndex1 = wx.Bitmap(os.path.join(os.path.curdir,"Icons","Loader","loader_32x32_01.png"),  wx.BITMAP_TYPE_ANY)
		self.bmpCirculaireIndex2 = wx.Bitmap(os.path.join(os.path.curdir,"Icons","Loader","loader_32x32_02.png"),  wx.BITMAP_TYPE_ANY)
		self.bmpCirculaireIndex3 = wx.Bitmap(os.path.join(os.path.curdir,"Icons","Loader","loader_32x32_03.png"),  wx.BITMAP_TYPE_ANY)
		self.bmpCirculaireIndex4 = wx.Bitmap(os.path.join(os.path.curdir,"Icons","Loader","loader_32x32_04.png"),  wx.BITMAP_TYPE_ANY)
		self.bmpCirculaireIndex5 = wx.Bitmap(os.path.join(os.path.curdir,"Icons","Loader","loader_32x32_05.png"),  wx.BITMAP_TYPE_ANY)
		self.bmpCirculaireIndex6 = wx.Bitmap(os.path.join(os.path.curdir,"Icons","Loader","loader_32x32_06.png"),  wx.BITMAP_TYPE_ANY)
		self.bmpCirculaireIndex7 = wx.Bitmap(os.path.join(os.path.curdir,"Icons","Loader","loader_32x32_07.png"),  wx.BITMAP_TYPE_ANY)
		self.bmpCirculaireIndex8 = wx.Bitmap(os.path.join(os.path.curdir,"Icons","Loader","loader_32x32_08.png"),  wx.BITMAP_TYPE_ANY)
		self.bmpCirculaireIndex9 = wx.Bitmap(os.path.join(os.path.curdir,"Icons","Loader","loader_32x32_09.png"),  wx.BITMAP_TYPE_ANY)
		self.bmpCirculaireIndex10 = wx.Bitmap(os.path.join(os.path.curdir,"Icons","Loader","loader_32x32_10.png"),  wx.BITMAP_TYPE_ANY)
		self.bmpCirculaireIndex11 = wx.Bitmap(os.path.join(os.path.curdir,"Icons","Loader","loader_32x32_11.png"),  wx.BITMAP_TYPE_ANY)
		self.bmpCirculaireIndex12 = wx.Bitmap(os.path.join(os.path.curdir,"Icons","Loader","loader_32x32_12.png"),  wx.BITMAP_TYPE_ANY)
		# affichage de l'OS + architecture 32/64bits
		global g_OSname
		global g_OSversion
		global g_OSdistrib
		global g_architectBits
		if (g_OSname == 'Linux'):
			self.m_bmpOS.SetBitmap(self.imageOsLinux)
			self.m_OSdetailsTxt.SetLabel(g_OSdistrib)
			MsgLog(self, u"Systeme d'exploitation: " + g_OSname+'  '+g_OSdistrib+'  '+g_architectBits)
			MsgLog(self, u"Python version: " + str(sys.version_info[0])+"."+str(sys.version_info[1])+str(sys.version_info[2])+" "+str(sys.version_info[3]))
			self.m_gestPeriphMnu.Enable(False)
		else:
			self.m_bmpOS.SetBitmap(self.imageOsWindows)
			self.m_OSdetailsTxt.SetLabel(g_OSname+' '+g_OSversion)
			MsgLog(self, u"Systeme d'exploitation: " + g_OSname+'  '+g_OSversion+'  '+g_architectBits)
		self.m_ArchBitsTxt.SetLabel(g_architectBits)
		# affichage version python
		self.m_PyVersionTxt.SetLabel(str(sys.version_info[0])+"."+str(sys.version_info[1])+str(sys.version_info[2])+" "+str(sys.version_info[3]))
		# ListBox Caractères séparateurs de données
		self.m_separateurCbx.Clear()
		self.m_separateurCbx.Append("|")
		self.m_separateurCbx.Append(";")
		self.m_separateurCbx.Append("*")
		self.m_separateurCbx.Append("TAB")
		# liaison événement pour réception du port série (cf exemple pyserial)
		self.Bind(EVT_SERIALRX, self.OnSerialRead)
	
	#####################################################
	# 					Fonction OnSerialRead(self, event)
	# Principe	:	Evénement de rafraichissement wxTextCtrl
	# Dépandence:	screenMain constructor
	# Appelé par:	Tâche de réception série
	# 2015-05-06:	Création
	#####################################################
	def OnSerialRead(self, event):
		"""Handle input from the serial port."""
		text = event.data
		self.logTextCtrl.AppendText(text)


	#####################################################
	# 			CAPTURE EVENEMENTS wxWidgets
	#####################################################
	
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
			elif bmpCirculaireIndexGbl==9:
				self.m_bmpCirculaire.SetBitmap(self.bmpCirculaireIndex9)
			elif bmpCirculaireIndexGbl==10:
				self.m_bmpCirculaire.SetBitmap(self.bmpCirculaireIndex10)
			elif bmpCirculaireIndexGbl==11:
				self.m_bmpCirculaire.SetBitmap(self.bmpCirculaireIndex11)
			elif bmpCirculaireIndexGbl==12:
				self.m_bmpCirculaire.SetBitmap(self.bmpCirculaireIndex12)
			bmpCirculaireIndexGbl=bmpCirculaireIndexGbl+1
			if bmpCirculaireIndexGbl > 12:
				bmpCirculaireIndexGbl = 1

	# capture de l'événement clic 'RUN'
	def m_bntRunEvt(self,event):
		self.AppliStart()

	# capture de l'événement clic 'STOP'
	def m_bntStopEvt(self,event):
		self.AppliStop()

	# capture de l'événement click checkBox 'Extraction Horodatage'
	def m_ExtractHorodateChkEvt(self,event):
		# mise à jour variable globale 'Extraction Horodatage'
		global gExtractHorodatageChk
		if event.IsChecked():
			gExtractHorodatageChk	= True
			# sélection séparateur '|' par défaut
			self.m_separateurCbx.SetSelection(0)
			gCaractereSeparateurTxt	= '|'
			MsgLog(self, u'SQL: Extraction Horodatage: Actif')
		else:
			gExtractHorodatageChk	= False
			MsgLog(self, u'SQL: Extraction Horodatage: Innactif')
		print u"gExtractHorodatageChk = " + str(gExtractHorodatageChk)
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
			MsgLog(self, u'SQL: Extraction Categorie: Actif')
		else:
			gExtractCategorieChk = False	# update image var globale
			#Activation saisie txt 'catégorie'
			#pour saisir manuellement la catégorie pour SQL
			self.m_CategorieTxt.Enable(True)
			MsgLog(self, u'SQL: Extraction Categorie: Innatif')
		print u"gExtractCategorieChk = " + str(gExtractCategorieChk)
		SeparateurEnable(self)

	# capture de l'événement Saisie Text 'Catégorie'
	def m_CategorieTxtEvt(self,event):
		global gExtractCategorieTxt
		gExtractCategorieTxt = self.m_CategorieTxt.GetValue()
		print u"m_CategorieTxtEvt: " + gExtractCategorieTxt
	# capture de l'événement Saisie Text 'Catégorie'
	def m_CategorieTxtTextEnter(self,event):
		global gExtractCategorieTxt
		gExtractCategorieTxt = self.m_CategorieTxt.GetValue()
		print u"m_CategorieTxtTextEnter: " + gExtractCategorieTxt

	# capture de l'événement click checkBox 'Extraction Priorité'
	def m_ExtractNivDetailChkEvt(self,event):
		global gExtractNivDetailChk
		# si la case 'Extraction Priorité' est cochée
		if event.IsChecked():
			gExtractNivDetailChk = True		# update image var globale
			#Désactivation saisie txt 'Priorité'
			#car le nom de la catégorie sera extraite des logs
			self.m_ExtractNivDetailNum.Enable(False)
			MsgLog(self, u'SQL: Extraction Priorite: Actif')
		else:
			gExtractNivDetailChk = False		# update image var globale
			#Activation saisie txt 'Priorité'
			#pour saisir manuellement la  Priorité pour SQL
			self.m_ExtractNivDetailNum.Enable(True)
			MsgLog(self, u'SQL: Extraction Priorite: Innactif')
		print u"gExtractNivDetailChk = " + str(gExtractNivDetailChk)
		SeparateurEnable(self)

	# capture de l'événement Saisie 'niveau détail' OnSpinCtrl
	def m_ExtractNivDetailNumEvt(self,event):
		global gExtractNivDetailNum
		gExtractNivDetailNum = self.m_ExtractNivDetailNum.GetValue()
		print u"gExtractNivDetailNum Evt = " + str(gExtractNivDetailNum)
		MsgLog(self, u'SQL: Extraction Num Priorite: ' + str(gExtractNivDetailNum))
	# capture de l'événement Saisie 'niveau détail' OnSpinCtrlText
	def m_ExtractNivDetailNumEvtTxt(self,event):
		global gExtractNivDetailNum
		gExtractNivDetailNum = self.m_ExtractNivDetailNum.GetValue()
		print u"gExtractNivDetailNum EvtTxt = " + str(gExtractNivDetailNum)
	# capture de l'événement Saisie 'niveau détail' OnSpinCtrlEnter
	def m_ExtractNivDetailNumEvtEnter(self,event):
		global gExtractNivDetailNum
		gExtractNivDetailNum = self.m_ExtractNivDetailNum.GetValue()
		print u"gExtractNivDetailNum EvtEnter = " + str(gExtractNivDetailNum)
		MsgLog(self, u'SQL: Extraction Num Priorite: ' + str(gExtractNivDetailNum))

	# capture de l'événement Sélection Cbo Evt 'Caractère séparateur'
	def m_separateurCbxEvt(self,event):
		global gCaractereSeparateurTxt
		gCaractereSeparateurTxt = self.m_separateurCbx.GetValue()
		print(u"gCaractereSeparateurTxt Evt = " + gCaractereSeparateurTxt)
		MsgLog(self, u'SQL: Caractere separateur: ' + gCaractereSeparateurTxt)
	# capture de l'événement Sélection Cbo OnText 'Caractère séparateur'
	def m_separateurCbxOnText(self,event):
		global gCaractereSeparateurTxt
		gCaractereSeparateurTxt = self.m_separateurCbx.GetValue()
		print(u"gCaractereSeparateurTxt OnText= " + gCaractereSeparateurTxt)
	# capture de l'événement Sélection Cbo OnTextEnter 'Caractère séparateur'
	def m_separateurCbxOnTextEnter(self,event):
		global gCaractereSeparateurTxt
		gCaractereSeparateurTxt = self.m_separateurCbx.GetValue()
		print(u"gCaractereSeparateurTxt OnTextEnter = " + gCaractereSeparateurTxt)

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
		print(u"Capture evenement bouton RUN")
		# START si port série déjà pas ouvert
		if not self.portSerie.isOpen(): 
			# test si variable COMselectGbl pas definie
			if COMselectGbl == "Non select.":
				print(u'Port serie non selectionne')
				MsgLog(self,u'Erreur: Port serie non selectionne')
				erreurGbl = True
				boxErr = wx.MessageDialog(None,u'Port série non selectionne', 'Erreur:', wx.OK)
				reponse= boxErr.ShowModal()
				boxErr.Destroy()
				# arret clignotant ERR
				erreurGbl = False
				self.m_bmpRunStop.SetBitmap(self.imageLedStop)
				self.m_RunStopTool.SetNormalBitmap(screenHome.imagePause)
			# le port COM est defini, on continue
			else:
				#initialisation et ouverture du port série
				try:
					self.portSerie = serial.Serial(str(COMselectGbl),int(COMvitesseGbl))
				except Exception:
					print(u'Erreur avec le port serie '+COMselectGbl)
					MsgLog(self,u'Erreur avec le port serie '+COMselectGbl)
					erreurGbl = True
					# appel popup erreur COM
					boxErr = wx.MessageDialog(None,'Erreur avec le port serie '+COMselectGbl, 'Erreur:', wx.OK)
					reponse=boxErr.ShowModal()
					boxErr.Destroy()
					# arret clignotant ERR
					erreurGbl = False
					#imageLedStop = wx.Bitmap("LedSTOP.png", wx.BITMAP_TYPE_ANY)
					self.m_bmpRunStop.SetBitmap(self.imageLedStop)
					self.m_RunStopTool.SetNormalBitmap(screenHome.imagePlay)
					self.m_toolBar1.Realize()
				else:
					# pas d'erreur, on continue:
					erreurGbl = False
					self.portSerie.timeout = 0.5   #make sure that the alive event can be checked from time to time
					# animation led run
					#imageLedRun  = wx.Bitmap("LedRUN_ON.png",  wx.BITMAP_TYPE_ANY)
					self.m_bmpRunStop.SetBitmap(self.imageLedRunOn)
					self.m_RunStopTool.SetNormalBitmap(screenHome.imagePause)
					self.m_toolBar1.Realize()
					print(u'Port série '+COMselectGbl+ u' ouvert.')
					MsgLog(self,u'Passage en RUN: Port serie '+COMselectGbl+ u' ouvert.')
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
		print(u"Capture evenement bouton STOP")
		erreurGbl = False
		#imageLedStop = wx.Bitmap("LedSTOP.png", wx.BITMAP_TYPE_ANY)
		self.m_bmpRunStop.SetBitmap(self.imageLedStop)
		self.m_RunStopTool.SetNormalBitmap(screenHome.imagePause)
		self.m_toolBar1.Realize()
		# STOP si port série déjà ouvert
		if self.portSerie.isOpen(): 
			# Arrêt de la scrutation réception série
			if self.alive:
				print(u'Arrêt de la scrutation réception série.')
				MsgLog(self, u'Arret de la scrutation reception serie ' + COMselectGbl)
				self._stop_reader()
				#Fermeture du port série
				try:
					self.portSerie.close()
				except NameError:
					print(u'Erreur a la fermeture du Port série '+COMselectGbl)
					MsgLog(self, u'Erreur a la fermeture du Port serie '+COMselectGbl)
					erreurGbl = True
					boxErr = wx.MessageDialog(None,u'Erreur à la fermeture du Port série '+COMselectGbl, 'Erreur:', wx.OK)
					reponse=boxErr.ShowModal()
					boxErr.Destroy()
				else:
					# pas d'erreur, on continue:
					erreurGbl = False
					# Fermeture du port série
					print(u'Passage en STOP: Port série '+COMselectGbl+u' fermé.')
					MsgLog(self, u'Port serie '+COMselectGbl+ u' ferme.')
					self.m_bmpRunStop.SetBitmap(self.imageLedStop)
					self.m_RunStopTool.SetNormalBitmap(screenHome.imagePlay)
					self.m_toolBar1.Realize()
					global statusRunStopGbl
					statusRunStopGbl = 0


	# START: regroupe les fonctions tâche Reception
	def _start_reader(self):
		"""Start reader thread"""
		self.alive = True
		# start serial->console thread
		self.receiver_thread = threading.Thread(target=self.reader)
		self.receiver_thread.setDaemon(True)
		self.receiver_thread.start()

	# STOP: Arrêt tâche de Reception
	def _stop_reader(self):
		"""Stop reader thread only, wait for clean exit of thread"""
		self.receiver_thread._Thread__stop()
		self.alive = False
		self.receiver_thread.join()


		
	# Lecture du port Série			
	def reader(self):
		global gDecodeSerieTxt
		global gEncodeSqlTxt
		global gSQLcompleteLineTxt
		# la liste texte est: logTextCtrl.Value = ""
		while self.alive:
			#desactive le RUN/STOP clignotant pour optimiser la réception
			enableBlinkGbl = False
			# lecture du port série, décodage à la voléeselon selection menu 'encodage / entrée série'
			##serialData = self.portSerie.read(1).decode(gDecodeSerieTxt, errors='replace')
			##serialData = self.portSerie.read(1).decode(gDecodeSerieTxt, errors='replace')
			try:
#				serialData = character(self.portSerie.read(1))
				serialData = self.portSerie.read(1)
				# caractère reçu ?
				if serialData:
					# Filtrage des guillemets à cause de SQL
					if ((serialData == "'") or (serialData == '"') or (serialData == '\n')):
						serialData = ""
					serialDataInWaiting= self.portSerie.inWaiting()     #regarde s'il y a encore des données à lire
#					if serialDataInWaiting:
#						serialData = serialData + self.portSerie.read(serialDataInWaiting) #Lit les caractères en attente
					# affichage caractère dans GUI
					#print type(serialData)
					#print "serialData: " + type(serialData)
					#pourAffichage = serialData.encode(gEncodeGuiTxt, errors='replace')
					event = SerialRxEvent(self.GetId(), serialData)
					self.GetEventHandler().AddPendingEvent(event)
					# si reception CR et SQL actif on doit enregistrer dans SQL
					if ((serialData == '\r') and gSQLenable):
						# enregistrement données reçu du port série en SQL
						MysqlInsert(self, gSQLcompleteLineTxt)
						gSQLcompleteLineTxt = ""
					# pas de CR
					else:
						# enrichissement de la ligne pour SQL
						# avec conversion encodage selon selection menu 'encodage / sortie SQL'
						if gSQLenable:
##							gSQLcompleteLineTxt = gSQLcompleteLineTxt + serialData.encode(gEncodeSqlTxt, errors='replace')
							gSQLcompleteLineTxt = gSQLcompleteLineTxt + serialData
			except serial.SerialException, e:
				self.alive = False
				MsgLog(self, u'Erreur de traitement de la reception')
				raise

	
	######## MENU [Fichier] ########
	# capture de l'événement selection menu <LogNew>
	def m_LogNewMnuEvt(self,event):
		print(u"Menu: Nouveau: Effacement des Logs")
		MsgLog(self, u'Fichier Nouveau: Effacement des Logs')
		self.logTextCtrl.Clear()
	# capture de l'événement selection menu <LogOpen>
	def m_LogOpenMnuEvt(self,event):
		global appliFolderName
		global logFileName
		global logFolderName
		global enableBlinkGbl
		print(u"Menu: Ouvrir Log")
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
				MsgLog(self, u'Fichier Ouvrir: ' + os.path.join(self.logFolderName, self.logFileName) + u' ouverture ok')
			except:
				MsgLog(self, u'Erreur lecture du fichier: '+ os.path.join(self.logFolderName, self.logFileName))
				print(u'Erreur lecture du fichier: '+self.logFileName)
				boxErr = wx.MessageDialog(None,'Erreur lecture du fichier: '+self.logFileName, 'Erreur lecture fichier:', wx.OK)
				reponse=boxErr.ShowModal()
				boxErr.Destroy()
		popupOpen.Destroy()
		enableBlinkGbl = True
		
	# capture de l'événement selection menu <LogSave>
	def m_LogSaveMnuEvt(self,event):
		global enableBlinkGbl
		print(u"Menu: Enregistrer Logs")
		enableBlinkGbl = False
		# enregistre si fichier/dossier ont un nom
		if (self.logFileName !="") and (self.logFolderName != ""):
			try:
				# accès fichier en écriture
				pointeurFichier = file(os.path.join(self.logFolderName, self.logFileName), 'w')
				pointeurFichier.write(self.logTextCtrl.GetValue())
				MsgLog(self, u'Fichier Enregistrer: ' + os.path.join(self.logFolderName, self.logFileName) + u' Sauvegarde ok')
				return True
			except:
				MsgLog(self, u'Erreur ecriture du fichier: '+ os.path.join(self.logFolderName, self.logFileName))
				print(u'Erreur écriture du fichier: '+self.logFileName)
				boxErr = wx.MessageDialog(None,'Erreur ecriture du fichier: '+self.logFileName, 'Erreur enregistrement fichier:', wx.OK)
				reponse=boxErr.ShowModal()
				boxErr.Destroy()
				return False
		# sinon popup <Enregistrer sous...>
		else:
			print(u'Fichier sans nom: go <Enregistrer sous...> ')
			self.m_LogSaveAsMnuEvt(self)
		enableBlinkGbl = True
		
	# capture de l'événement selection menu <LogSaveAs...>
	def m_LogSaveAsMnuEvt(self,event):
		global enableBlinkGbl
		print(u"Menu: Enregistrer Logs sous...")
		enableBlinkGbl = False
		popupSaveAs = wx.FileDialog(self, "Enregister fichier log sous...", self.logFolderName, self.logFileName,
						"Fichier texte (*.txt)|*.txt|All Files|*.*", wx.SAVE)
		if (popupSaveAs.ShowModal() == wx.ID_OK):
			self.logFileName = popupSaveAs.GetFilename()
			self.logFolderName = popupSaveAs.GetDirectory()
			# on réutilise la fonction d'enregistrement
			if self.m_LogSaveMnuEvt(self):
				#self.FenetrePrincipaleClass.SetTitle(self.APP_NAME + " - [" +self.logFileName+ "]")
				print(u"Serial SQL Logger - [" + self.logFileName + "]")
				MsgLog(self, u'Fichier Enregistrer sous: ' + os.path.join(self.logFolderName, self.logFileName) + u' Sauvegarde ok')
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
		self.m_ExtractNivDetailChk.SetValue(False)
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
		global gExtractNivDetailChk
		global gExtractNivDetailNum
		global gCaractereSeparateurTxt
		print(u"Menu: Ouvrir Profile")
		enableBlinkGbl = False
		popupOpen = wx.FileDialog(self, "Ouvrir fichier profile", self.profileFolderName, self.profileFileName,
										"Fichier profile (*.cfg)|*.cfg|All Files|*.*", wx.OPEN)
		if (popupOpen.ShowModal() == wx.ID_OK):
			self.profileFileName   = popupOpen.GetFilename()
			self.profileFolderName = popupOpen.GetDirectory()
			print(u'popupOpen: '+self.profileFolderName+' '+self.profileFileName)
			try:
				# accès fichier en lecture
				pointeurFichierProfile = file(os.path.join(self.profileFolderName, self.profileFileName), 'r')
			except Exception:
				MsgLog(self, u'Erreur lecture du fichier: '+ os.path.join(self.profileFolderName, self.profileFileName))
				print(u'Erreur lecture du fichier: '+ os.path.join(self.profileFolderName, self.profileFileName))
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
				gExtractNivDetailChk		= profile.getboolean('Decodage_Logs', 'Extract_Priorite_Chk')
				gExtractNivDetailNum		= profile.getint(    'Decodage_Logs', 'Extract_Priorite_Txt')
				gCaractereSeparateurTxt		= profile.get(       'Decodage_Logs', 'Caractere_Separateur_Txt')
				# test si le port série est bien sur la machine
				try:
					self.portSerie = serial.Serial(str(COMselectGbl),int(COMvitesseGbl))
				except Exception:
					print(u"Erreur: le port série "+COMselectGbl+ u" n'est pas sur cette machine")
					MsgLog(self, u"Erreur: le port serie "+COMselectGbl+ u" n'est pas sur cette machine")
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
					MsgLog(self, u"Port COM: "+COMselectGbl+ u"  Vitesse Port: "+ str(COMvitesseGbl))
					self.m_statusVitesseTextStat.SetLabel("Vitesse: "+str(COMvitesseGbl)+" bds")
					# memorisation du profile pour titre appli
					ProfileNameGbl = self.profileFileName
					#Fermeture du port série
					self.portSerie.close()
					# fermeture du fichier profile
					pointeurFichierProfile.close()
					DecodageRefresh(self)
					MsgLog(self, u'Fichier Ouvrir: ' + os.path.join(self.profileFolderName, self.profileFileName) + u' ouverture ok')
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
		global gExtractNivDetailChk
		global gExtractNivDetailNum
		global gCaractereSeparateurTxt
		print(u"Menu: Enregistrer Profile")
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
				profile.set('Decodage_Logs', 'Extract_Priorite_Chk',		str(gExtractNivDetailChk))
				profile.set('Decodage_Logs', 'Extract_Priorite_Txt',		str(gExtractNivDetailNum))
				profile.set('Decodage_Logs', 'Caractere_Separateur_Txt',	gCaractereSeparateurTxt)
				print(u"Dossier = " + self.profileFolderName)
				print(u"Fichier = " + self.profileFileName)
				print(u"gExtractHorodatageChk      = " + str(gExtractHorodatageChk))
				print(u"gExtractCategorieChk       = " + str(gExtractCategorieChk))
				print(u"gExtractCategorieTxt       = " + gExtractCategorieTxt)
				print(u"gExtractNivDetailChk        = " + str(gExtractNivDetailChk))
				print(u"gExtractNivDetailNum        = " + str(gExtractNivDetailNum))
				print(u"gCaractereSeparateurTxt    = " + gCaractereSeparateurTxt)
				MsgLog(self, u'Enregistrer profile: '+os.path.join(self.profileFolderName, self.profileFileName))
				profile.write(open(os.path.join(self.profileFolderName, self.profileFileName), 'w'))
				MsgLog(self, u'Fichier Enregistrer: ' + os.path.join(self.profileFolderName, self.profileFileName) + u' Sauvegarde ok')
				return True
			except:
				MsgLog(self, u'Erreur ecriture du fichier: '+ os.path.join(self.profileFolderName, self.profileFileName))
				print(u'Erreur écriture du fichier: '+self.profileFileName)
				boxErr = wx.MessageDialog(None,'Erreur ecriture du fichier: '+self.profileFileName, 'Erreur enregistrement fichier:', wx.OK)
				reponse=boxErr.ShowModal()
				boxErr.Destroy()
				return False
		# sinon popup <Enregistrer sous...>
		else:
			print(u'Fichier sans nom: go <Enregistrer Profile sous...> ')
			self.m_ProfileSaveAsMnuEvt(self)
		enableBlinkGbl = True
		
	# capture de l'événement selection menu <ProfileSaveAs>
	def m_ProfileSaveAsMnuEvt( self, event ):
		global AppliTitreGbl
		global ProfileNameGbl
		global enableBlinkGbl
		print(u"Menu: Enregistrer Profile sous...")
		enableBlinkGbl = False
		popupSaveAs = wx.FileDialog(self, "Enregister fichier profile sous...", self.profileFolderName, self.profileFileName,
						"Fichier profile (*.cfg)|*.cfg|All Files|*.*", wx.SAVE)
		if (popupSaveAs.ShowModal() == wx.ID_OK):
			self.profileFileName = popupSaveAs.GetFilename()
			self.profileFolderName = popupSaveAs.GetDirectory()
			# on réutilise la fonction d'enregistrement
			if self.m_ProfileSaveMnuEvt(self):
				#self.FenetrePrincipaleClass.SetTitle(self.APP_NAME + " - [" +self.profileFileName+ "]")
				print(u"Serial SQL Logger - [" + self.profileFileName + "]")
				MsgLog(self, u'Fichier Enregistrer sous: ' + os.path.join(self.profileFolderName, self.profileFileName) + u' Sauvegarde ok')
				# memorisation du profile
				ProfileNameGbl = self.profileFileName
		enableBlinkGbl = True
		AppliTitreCreation()
		screenHome.SetTitle(AppliTitreGbl)

	# capture de l'événement selection menu <Quiter>
	def m_quiterMnuEvt(self,event):
		print(u"Menu: Quiter")
		MsgLog(self, u'Menu: Quiter')
		global statusRunStopGbl
		if (statusRunStopGbl == 1):
			self.portSerie.close()
			print(u'Fermeture Port serie '+COMselectGbl + u' car reste ouvert...')
			MsgLog(self, u'Fermeture Port serie '+COMselectGbl + u' car reste ouvert...')
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
		print(u"<Actualiser> ")
		MsgLog(self,u'Recherche des Ports COM disponibles ...')
		self.m_statusActionTextStat.SetLabel(u"Recherche ports COM en cours...")
		FindCOM(self)
		print(u"<FIN> ")
		MsgLog(self,u'Recherche terminer: choisissez un port serie')
		self.m_statusActionTextStat.SetLabel(u"Recherche terminer: choisissez un port serie")
	#  menu <Select.Manuelle>
	def m_COMmanuMnuEvt(self,event):
		global COMselectGbl
		# scan port serie dispo:
		print(u"<Select.Manuel> ")
		box = wx.TextEntryDialog(None, "Entrez le nom du port serie:\n  Exemple: /dev/ttyACM0 pour Arduino", "Port serie:", "/dev/ttyACM0")
		if box.ShowModal()==wx.ID_OK:
			COMselectGbl=box.GetValue()
		print(u"Selection manuelle: "+ COMselectGbl)
		MsgLog(self, u"Selection manuelle Port COM: "+ COMselectGbl)
		self.m_statusActionTextStat.SetLabel("Selection manuelle: "+ COMselectGbl)
		self.m_statusComTextStat.SetLabel("Port serie: " + COMselectGbl)
	# capture de l'événement selection menu COM non selectionné
	def m_COMnonSelectEvt(self,event):
		global COMselectGbl
		global COMvitesseGbl
		COMselectGbl = "Non select."
		COMvitesseGbl = 115200
		MsgLog(self, u"Nouveau profile:    Port COM: "+COMselectGbl+ u"    Vitesse Port: "+ str(COMvitesseGbl))
		self.m_statusVitesseTextStat.SetLabel("Vitesse: "+str(COMvitesseGbl)+" bds")
		self.m_statusComTextStat.SetLabel("Port serie: "+COMselectGbl)

	# capture de l'événement selection ComboBox Port COM
	def m_portComCbxEvt( self, event ):
		global COMselectGbl
		bcb = event.GetEventObject()
		idx = event.GetInt()
		COMselectGbl  = bcb.GetString(idx)					# correction depuis wx2.8-examples
		print(u"COMselectGbl: " + COMselectGbl)
		MsgLog(self, u"Selection Port COM: "+ COMselectGbl)
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
		print(u"COMselectGbl: " + COMselectGbl)
		MsgLog(self, u"Selection Port COM: "+ COMselectGbl)
		self.m_statusComTextStat.SetLabel("Port serie: " + COMselectGbl)
		self.m_statusActionTextStat.SetLabel("Pret.")
	
		
	####################################
	########		MENU		########
	####################################
	
	######## MENU [Vitesse COM] ########
	# capture de l'événement selection menu <115200 bds>
	def m_115200mnuEvt(self,event):
		global COMvitesseGbl
		COMvitesseGbl = 115200
		print(u"COMvitesseGbl: " + str(COMvitesseGbl))
		global COMselectGbl
		MsgLog(self, u"Port COM: "+COMselectGbl+ u"  Vitesse: "+ str(COMvitesseGbl))
		self.m_statusVitesseTextStat.SetLabel("Vitesse: "+str(COMvitesseGbl)+" bds")
	# menu <57600 bds>
	def m_57600mnuEvt(self,event):
		global COMvitesseGbl
		COMvitesseGbl = 57600
		print(u"COMvitesseGbl: " + str(COMvitesseGbl))
		global COMselectGbl
		MsgLog(self, u"Port COM: "+COMselectGbl+ u"  Vitesse: "+ str(COMvitesseGbl))
		self.m_statusVitesseTextStat.SetLabel("Vitesse: "+str(COMvitesseGbl)+" bds")
	# menu <19200 bds>
	def m_19200mnuEvt(self,event):
		global COMvitesseGbl
		COMvitesseGbl = 19200
		print(u"COMvitesseGbl: " + str(COMvitesseGbl))
		global COMselectGbl
		MsgLog(self, u"Port COM: "+COMselectGbl+ u"  Vitesse: "+ str(COMvitesseGbl))
		self.m_statusVitesseTextStat.SetLabel("Vitesse: "+str(COMvitesseGbl)+" bds")
	# menu <9600 bds>
	def m_9600mnuEvt(self,event):
		global COMvitesseGbl
		COMvitesseGbl = 9600
		print(u"COMvitesseGbl: " + str(COMvitesseGbl))
		global COMselectGbl
		MsgLog(self, u"Port COM: "+COMselectGbl+ u"  Vitesse: "+ str(COMvitesseGbl))
		self.m_statusVitesseTextStat.SetLabel("Vitesse: "+str(COMvitesseGbl)+" bds")
	# menu <4800 bds>
	def m_4800mnuEvt(self,event):
		global COMvitesseGbl
		COMvitesseGbl = 4800
		print(u"COMvitesseGbl: " + str(COMvitesseGbl))
		global COMselectGbl
		MsgLog(self, u"Port COM: "+COMselectGbl+ u"  Vitesse: "+ str(COMvitesseGbl))
		self.m_statusVitesseTextStat.SetLabel("Vitesse: "+str(COMvitesseGbl)+" bds")
	# menu <2400 bds>
	def m_2400mnuEvt(self,event):
		global COMvitesseGbl
		COMvitesseGbl = 2400
		print(u"COMvitesseGbl: " + str(COMvitesseGbl))
		global COMselectGbl
		MsgLog(self, u"Port COM: "+COMselectGbl+ u"  Vitesse: "+ str(COMvitesseGbl))
		self.m_statusVitesseTextStat.SetLabel("Vitesse: "+str(COMvitesseGbl)+" bds")
	# menu <1200 bds>
	def m_1200mnuEvt(self,event):
		global COMvitesseGbl
		COMvitesseGbl = 1200
		print(u"COMvitesseGbl: " + str(COMvitesseGbl))
		global COMselectGbl
		MsgLog(self, u"Port COM: "+COMselectGbl+ u"  Vitesse: "+ str(COMvitesseGbl))
		self.m_statusVitesseTextStat.SetLabel(u"Vitesse: "+str(COMvitesseGbl)+" bds")

	######## MENU [Système] ########
	# menu <gestionnaire de periphérique>
	def m_gestPeriphMnuEvt(self,event):
		os.startfile('devmgmt.msc')
		MsgLog(self, u"Menu Systeme: gestionnaire de peripherique")

	######## MENU [Decodage Série] ########
	# menu <Décodage entrée série / UTF-8>
	def m_decodeUTF8MnuEvt(self,event):
		global gDecodeSerieTxt
		global gDecodeSerieISO_8859_15Chk
		global gDecodeSerieWin1252Chk
		global gDecodeSerieUTF8Chk
		global gDecodeSerieCP850Chk
		gDecodeSerieTxt		 		= "utf_8"
		gDecodeSerieUTF8Chk			= True
		gDecodeSerieWin1252Chk		= False
		gDecodeSerieISO_8859_15Chk	= False
		gDecodeSerieCP850Chk		= False
		MsgLog(self, u"Menu encodage: Entree Serie -> UTF-8 (Unicode )")
		self.m_statusDecodeSerieTxt.SetLabel("Decodage serie: " + gDecodeSerieTxt)
	# menu <Décodage entrée série / Win1252>
	def m_decodeWin1252MnuEvt(self,event):
		global gDecodeSerieTxt
		global gDecodeSerieISO_8859_15Chk
		global gDecodeSerieWin1252Chk
		global gDecodeSerieUTF8Chk
		global gDecodeSerieCP850Chk
		gDecodeSerieTxt		 		= "cp1252"
		gDecodeSerieUTF8Chk			= False
		gDecodeSerieWin1252Chk		= True
		gDecodeSerieISO_8859_15Chk	= False
		gDecodeSerieCP850Chk		= False
		MsgLog(self, u"Menu encodage: Entree Serie -> cp1252 (Windows ,Western)")
		self.m_statusDecodeSerieTxt.SetLabel("Decodage serie: " + gDecodeSerieTxt)
	# menu <Décodage entrée série / ISO-8859-15>
	def m_decodeISO_8859_15MnuEvt(self,event):
		global gDecodeSerieTxt
		global gDecodeSerieUTF8Chk
		global gDecodeSerieWin1252Chk
		global gDecodeSerieISO_8859_15Chk
		global gDecodeSerieCP850Chk
		gDecodeSerieTxt		 		= "iso8859_15"
		gDecodeSerieUTF8Chk			= False
		gDecodeSerieWin1252Chk		= False
		gDecodeSerieISO_8859_15Chk	= True
		gDecodeSerieCP850Chk		= False
		MsgLog(self, u"Menu encodage: Entree Serie -> ISO-8859-15 (Latin-1, West Europe,Touche Euro)")
		self.m_statusDecodeSerieTxt.SetLabel("DEcodage serie: " + gDecodeSerieTxt)
	# menu <Décodage entrée série / cp850>
	def m_decodeCP850MnuEvt(self,event):
		global gDecodeSerieTxt
		global gDecodeSerieISO_8859_15Chk
		global gDecodeSerieWin1252Chk
		global gDecodeSerieUTF8Chk
		global gDecodeSerieCP850Chk
		gDecodeSerieTxt		 		= "cp850"
		gDecodeSerieUTF8Chk			= False
		gDecodeSerieWin1252Chk		= False
		gDecodeSerieISO_8859_15Chk	= False
		gDecodeSerieCP850Chk		= True
		MsgLog(self, u"Menu encodage: Entree Serie -> cp850 (MS-DOS )")
		self.m_statusDecodeSerieTxt.SetLabel("Decodage serie: " + gDecodeSerieTxt)

	######## MENU [Encodage SQL] ########
	# menu <Encodage sortie SQL / UTF-8>
	def m_encodeUTF8MnuEvt(self,event):
		global gEncodeSqlTxt
		global gEncodeSqlISO_8859_15Chk
		global gEncodeSqlWin1252Chk
		global gEncodeSqlUTF8Chk
		global gEncodeSqlCP850Chk
		gEncodeSqlTxt		 		= "utf_8"
		gEncodeSqlUTF8Chk			= True
		gEncodeSqlWin1252Chk		= False
		gEncodeSqlISO_8859_15Chk	= False
		gEncodeSqlCP850Chk			= False
		MsgLog(self, u"Menu encodage: Sortie SQL -> UTF-8 (Unicode )")
		self.m_statusEncodeSqlTxt.SetLabel("Encodage SQL: " + gEncodeSqlTxt)
	# menu <Encodage sortie SQL / Win1252>
	def m_encodeWin1252MnuEvt(self,event):
		global gEncodeSqlTxt
		global gEncodeSqlUTF8Chk
		global gEncodeSqlWin1252Chk
		global gEncodeSqlISO_8859_15Chk
		global gEncodeSqlCP850Chk
		gEncodeSqlTxt		 		= "cp1252"
		gEncodeSqlEncodeUTF8Chk		= False
		gEncodeSqlWin1252Chk		= True
		gEncodeSqlISO_8859_15Chk	= False
		gEncodeSqlEncodeCP850Chk	= False
		MsgLog(self, u"Menu encodage: Sortie SQL -> cp1252 (Windows ,Western)")
		self.m_statusEncodeSqlTxt.SetLabel("Encodage SQL: "+ gEncodeSqlTxt)
	# menu <Encodage sortie SQL / ISO-8859-15>
	def m_encodeISO_8859_15MnuEvt(self,event):
		global gEncodeSqlTxt
		global gEncodeSqlUTF8Chk
		global gEncodeSqlWin1252Chk
		global gEncodeSqlISO_8859_15Chk
		global gEncodeSqlCP850Chk
		gEncodeSqlTxt		 		= "iso8859_15"
		gEncodeSqlISO_8859_15Chk	= True
		gEncodeSqlWin1252Chk		= False
		gEncodeSqlUTF8Chk			= False
		gEncodeSqlCP850Chk			= False
		MsgLog(self, u"Menu encodage: Sortie SQL -> ISO-8859-15 (Latin-1, West Europe,Touche Euro)")
		self.m_statusEncodeSqlTxt.SetLabel("Encodage SQL: "+ gEncodeSqlTxt)
	# menu <Encodage sortie SQL / cp850>
	def m_encodeCP850MnuEvt(self,event):
		global gEncodeSqlTxt
		global gEncodeSqlUTF8Chk
		global gEncodeSqlWin1252Chk
		global gEncodeSqlISO_8859_15Chk
		global gDecodeSqlEncodeCP850Chk
		gEncodeSqlTxt		 		= "cp850"
		gEncodeSqlUTF8Chk			= False
		gEncodeSqlWin1252Chk		= False
		gEncodeSqlISO_8859_15Chk	= False
		gEncodeSqlCP850Chk			= True
		MsgLog(self, u"Menu encodage: Sortie SQL -> cp850 (MS-DOS )")
		self.m_statusEncodeSqlTxt.SetLabel("Encodage SQL: "+ gEncodeSqlTxt)

	######## MENU [Encodage GUI] ########
	# menu <Encodage sortie SQL / UTF-8>
	def m_encodeGuiUTF8MnuEvt(self,event):
		global gEncodeGuiTxt
		global gEncodeGuiUTF8Chk
		global gEncodeGuiWin1252Chk
		global gEncodeGuiISO_8859_15Chk
		global gEncodeGuiCP850Chk
		gEncodeGuiTxt		 		= "utf_8"
		gEncodeGuiUTF8Chk			= True
		gEncodeGuiWin1252Chk		= False
		gEncodeGuiISO_8859_15Chk	= False
		gEncodeGuiCP850Chk			= False
		MsgLog(self, u"Menu encodage: Sortie Affichage -> UTF-8 (Unicode )")
		self.m_statusEncodeGuiTxt.SetLabel("Encodage GUI: "+ gEncodeGuiTxt)
	# menu <Encodage sortie SQL / Win1252>
	def m_encodeGuiWin1252MnuEvt(self,event):
		global gEncodeGuiTxt
		global gEncodeGuiUTF8Chk
		global gEncodeGuiWin1252Chk
		global gEncodeGuiISO_8859_15Chk
		global gEncodeGuiCP850Chk
		gEncodeGuiTxt		 		= "cp1252"
		gEncodeGuiEncodeUTF8Chk		= False
		gEncodeGuiWin1252Chk		= True
		gEncodeGuiISO_8859_15Chk	= False
		gEncodeGuiEncodeCP850Chk	= False
		MsgLog(self, u"Menu encodage: Sortie Affichage -> cp1252 (Windows ,Western)")
		self.m_statusEncodeGuiTxt.SetLabel("Encodage GUI: "+ gEncodeGuiTxt)
	# menu <Encodage sortie SQL / cp850>
	def m_encodeGuiCP850MnuEvt(self,event):
		global gEncodeGuiTxt
		global gEncodeGuiUTF8Chk
		global gEncodeGuiWin1252Chk
		global gEncodeGuiISO_8859_15Chk
		global gDecodeGuiEncodeCP850Chk
		gEncodeGuiTxt		 		= "cp850"
		gEncodeGuiUTF8Chk			= False
		gEncodeGuiWin1252Chk		= False
		gEncodeGuiISO_8859_15Chk	= False
		gEncodeGuiCP850Chk			= True
		MsgLog(self, u"Menu encodage: Sortie Affichage -> cp850 (MS-DOS )")
		self.m_statusEncodeGuiTxt.SetLabel("Encodage GUI: "+ gEncodeGuiTxt)
	# menu <Encodage sortie SQL / ISO-8859-15>
	def m_encodeISO_8859_15MnuEvt(self,event):
		global gEncodeGuiTxt
		global gEncodeGuiUTF8Chk
		global gEncodeGuiWin1252Chk
		global gEncodeGuiISO_8859_15Chk
		global gEncodeGuiCP850Chk
		gEncodeGuiTxt		 		= "iso8859_15"
		gEncodeGuiUTF8Chk			= False
		gEncodeGuiWin1252Chk		= False
		gEncodeGuiISO_8859_15Chk	= True
		gEncodeGuiCP850Chk			= False
		MsgLog(self, u"Menu encodage: Sortie Affichage -> ISO-8859-15 (Latin-1, West Europe,Touche Euro)")
		self.m_statusEncodeGuiTxt.SetLabel("Encodage GUI: "+ gEncodeGuiTxt)

	# capture de l'événement clic 'MySQL INSERT'
	def m_mysqlInsertEvt(self,event):
		MysqlInsert(self,"Test enregistrement")


	####################################
	########	  ToolBar		########
	####################################
	
	# icone <Find Port>
	def m_findPortToolEvt( self, event ):
		# scan port serie dispo:
		print(u"<Actualiser> ")
		MsgLog(self, u'Recherche des Ports COM disponibles ...')
		self.m_statusActionTextStat.SetLabel(u"Recherche ports COM en cours...")
		FindCOM(self)
		print(u"<FIN> ")
		MsgLog(self,u'Recherche terminer: choisissez un port serie')
		self.m_statusActionTextStat.SetLabel(u"Recherche terminer: choisissez un port série")

	# Icone <Run Stop>
	def m_RunStopToolEvt(self,event):
		global statusRunStopGbl
		if statusRunStopGbl == 0:
			self.AppliStart()
		else:
			self.AppliStop()

	# Icone <SQL on/off>
	def m_dataToolEvt(self,event):
		global gSQLenable
		global gSQLlisteTable
		if not gSQLenable:
			gSQLenable = True
			self.m_dataTool.SetNormalBitmap(screenHome.imageSQLon)
			self.m_toolBar1.Realize()
			#self.spacer_10x60.Show()
			self.m_separateurTxt.Show()
			self.m_separateurCbx.Show()
			self.spacer_10x20_01.Show()
			self.m_ExtractHorodateChk.Show()
			self.spacer_10x20_02.Show()
			self.m_ExtractCategorieChk.Show()
			self.spacer_10x20_03.Show()
			self.m_CategorieLbl.Show()
			self.m_CategorieTxt.Show()
			self.spacer_10x20_04.Show()
			self.m_ExtractNivDetailChk.Show()
			self.m_ExtractNivDetailLbl.Show()
			self.m_ExtractNivDetailNum.Show()
			# Liste des Tables SQL
			# efface la liste dans ComboBox
			self.m_tableArchiveCbx.Clear()
			self.m_tableArchiveCbx.Append(u" - - Actualiser --")
			# lecture des tables dispo
			MysqlShowTable(self)
			# ajout tables dispo dans combobox GUI
			print u'Ajout liste table cbo'
			for afficheTable in gSQLlisteTable:
				self.m_tableArchiveCbx.Append(afficheTable)
				print afficheTable
			MsgLog(self, u'SQL: actif')
		else:
			gSQLenable = False
			self.m_dataTool.SetNormalBitmap(screenHome.imageSQLoff)
			self.m_toolBar1.Realize()
			#self.spacer_10x60.Hide()
			self.m_separateurTxt.Hide()
			self.m_separateurCbx.Hide()
			self.spacer_10x20_01.Hide()
			self.m_ExtractHorodateChk.Hide()
			self.spacer_10x20_02.Hide()
			self.m_ExtractCategorieChk.Hide()
			self.spacer_10x20_03.Hide()
			self.m_CategorieLbl.Hide()
			self.m_CategorieTxt.Hide()
			self.spacer_10x20_04.Hide()
			self.m_ExtractNivDetailChk.Hide()
			self.m_ExtractNivDetailLbl.Hide()
			self.m_ExtractNivDetailNum.Hide()
			MsgLog(self, u'SQL: innactif')

	# Icone <CBO liste table d'archive>
	def m_tableArchiveCbxEvt(self,event):
		global gSQLdataTable
		# test si on ré-actualise la CBO
		if self.m_tableArchiveCbx.GetSelection() == 0:
			# reset de la liste
			gSQLlisteTable[:] = []
			self.m_tableArchiveCbx.Clear()
			self.m_tableArchiveCbx.Append(u" - - Actualiser --")
			# actualisation de la liste
			MysqlShowTable(self)
			# ajout tables dispo dans combobox GUI
			print u'Ajout liste table cbo'
			for afficheTable in gSQLlisteTable:
				self.m_tableArchiveCbx.Append(afficheTable)
			MsgLog(self, u'SQL: Actualisation.')
		else:
			gSQLdataTable =  self.m_tableArchiveCbx.GetStringSelection() 
			print gSQLdataTable

	# Icone <Quiter>
	def m_toolQuiterEvt(self,event):
		global COMselectGbl
		print(u"Menu: Quiter")
		MsgLog(self, u'Menu: Quiter')
		global statusRunStopGbl
		if (statusRunStopGbl == 1):
			self.portSerie.close()
			print(u'Fermeture Port serie '+COMselectGbl +' car reste ouvert...')
			MsgLog(self, u'Fermeture Port serie '+COMselectGbl + u' car reste ouvert...')
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
	self.logAppliTextCtrl.WriteText(u'\n' + time.strftime(u'%Y-%m-%d %H:%M:%S  ' + message))

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
	AppliTitreGbl = u"Serial to SQL Logger - Profile: ["+ProfileNameGbl+ u"]  Port:"+COMselectGbl+ u"  Vitesse:"+str(COMvitesseGbl)+ u" bds"

#####################################################
# 					Fonction ScanWin()
#					Reprise exemple lib pyserial
# Principe	:	Scan les ports COM disponibles sous Windows
# Dépandence:	import serial
# Appelé par:	Fonction FindCOM()
# 2014-04-19:	Création
#####################################################
def ScanWin():
	"""scan for available ports. return a list of tuples (num, name)"""
	available = []
	for i in range(100):
		try:
			s = serial.Serial(i)
			available.append( (i, s.portstr))
			s.close()
		except serial.SerialException:
			pass
	return available

#####################################################
# 					Fonction ScanLinux()
#					Reprise exemple lib pyserial
# Principe	:	Scan les ports séries disponibles sous linux
# Dépandence:	import serial glob
# Appelé par:	Fonction FindCOM()
# 2015-05-06	Création
#####################################################
def ScanLinux():
    """scan for available ports. return a list of device names."""
    return glob.glob('/dev/ttyACM*') + glob.glob('/dev/ttyUSB*') + glob.glob('/dev/ttyS*')

#####################################################
# 					Fonction FindCOM()
# Principe	:	Actualise la liste des Ports COM dispo.
# Dépandence:	import Serial_SQL_Logger_GUI
# Appelé par:	Fonction événement: m_COMactualiserMnuEvt
#									m_findPortToolEvt
# 2014-04-19:	Création
# 2015-02-28:	Pour Linux, ajout port série Bluetooth RFcommXX
# 2015-05-06:	Séparation scan ports séries en fonction OS: Linux/Win
#####################################################
def FindCOM(self):
	# efface la liste dans ComboBox
	self.m_portComCbx.Clear()
	print u"Ports dispo:"
	# scan pour Linux
	if g_OSname == "Linux":
		# Note: si appairage bluetooth fait alors fichier /dev/rfcomm0 présent
		# on test la pésence /dev/rfcomm0 à /dev/refcomm9
		for i in range(10):
			RFport = '/dev/rfcomm' + str(i)
			if os.path.exists(RFport):
				self.m_portComCbx.Append(RFport)
		# on poursuit la recherche des ports séries
		for name in ScanLinux():
			print name
			# actualisation liste port serie en fonction des COM dispo
			self.m_portComCbx.Append(name)
	# scan pour Windows
	else:
		# scan port serie dispo:
		for n,s in ScanWin():
			print "(%d) %s" % (n,s)
			MsgLog(self,"%s" % (s))
			# actualisation liste port serie en fonction des COM dispo
			self.m_portComCbx.Append(s)

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
	print(u"Menu: Enregistrer Logs")
	enableBlinkGbl = False
	# enregistre si fichier/dossier ont un nom
	if (self.logFileName !="") and (self.logFolderName != ""):
		try:
			# accès fichier en écriture
			pointeurFichier = file(os.path.join(folderName, fileName), 'w')
			# écriture du fichier
			pointeurFichier.write(COMselectGbl)
			MsgLog(self, u'Fichier Enregistrer: ' + os.path.join(FolderName, FileName) + u' Sauvegarde ok')
			return True
		except:
			MsgLog(self, u'Erreur ecriture du fichier: '+ os.path.join(self.logFolderName, self.logFileName))
			print(u'Erreur écriture du fichier: '+self.logFileName)
			boxErr = wx.MessageDialog(None,'Erreur ecriture du fichier: '+self.logFileName, 'Erreur enregistrement fichier:', wx.OK)
			reponse=boxErr.ShowModal()
			boxErr.Destroy()
			return False
	# sinon popup <Enregistrer sous...>
	else:
		print(u'Fichier sans nom: go <Enregistrer sous...> ')
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
	global gExtractNivDetailChk
	if gExtractHorodatageChk or gExtractCategorieChk or gExtractNivDetailChk:
		gCaractereSeparateurEnable = True		# update image variable globale
		# Activation comboBox 'Caractère séparateur'
		self.m_separateurCbx.Enable(True)
	else:
		gCaractereSeparateurEnable = False		# update image variable globale
		# Désactivation comboBox 'Caractère séparateur'
		self.m_separateurCbx.Enable(False)
	#print "m_ExtractNivDetailChkEvt ",gExtractNivDetailChk

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
	global gExtractNivDetailChk
	global gExtractNivDetailNum
	global gCaractereSeparateurTxt
	global gCaractereSeparateurEnable
	print(u'gExtractHorodatageChk=      ' + str(gExtractHorodatageChk))
	print(u'gExtractCategorieChk=       ' + str(gExtractCategorieChk))
	print(u'gExtractCategorieTxt=       ' + gExtractCategorieTxt)
	print(u'gExtractNivDetailChk=        ' + str(gExtractNivDetailChk))
	print(u'gExtractNivDetailNum=        ' + str(gExtractNivDetailNum))
	print(u'gCaractereSeparateurTxt=    ' + gCaractereSeparateurTxt)
	self.m_ExtractHorodateChk.SetValue(gExtractHorodatageChk)
	self.m_ExtractCategorieChk.SetValue(gExtractCategorieChk)
	self.m_CategorieTxt.Value = gExtractCategorieTxt
	self.m_ExtractNivDetailChk.SetValue(gExtractNivDetailChk)
	self.m_PrioriteInt.Value = gExtractNivDetailNum
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
def MysqlInsert(self,message):
	gExtractHorodatageChkRang = 0
	gExtractCategorieChkRang  = 0
	gExtractNivDetailChkRang  = 0
	global gSQLserver
	global gSQLuser
	global gSQLpasswd
	global gSQLdataBase
	try:
		#MysqlInsert: print "base MySQL ouverture..."
		db = MySQLdb.connect(host=gSQLserver,user=gSQLuser,passwd=gSQLpasswd,db=gSQLdataBase)
	except Exception:
		MsgLog(self, u'Erreur connexion SQL vers ' + gSQLserver)
		# appel popup erreur connexion MySQL
		boxErr = wx.MessageDialog(None,'Erreur connexion SQL vers ' + gSQLserver, 'Erreur:', wx.OK)
		reponse=boxErr.ShowModal()
		boxErr.Destroy()
	else:
		# séparation des données ?
		# oui: au moins une extraction
		if gExtractHorodatageChk or gExtractCategorieChk or gExtractNivDetailChk:
			messageSplit = message.split(gCaractereSeparateurTxt)
			#print u"====================================="
			#print  messageSplit 
			#====  horodatage inclus dans message ?
			# oui: horodatage inclus dans message donc on l'extrait
			if gExtractHorodatageChk:
				gExtractHorodatageChkRang = 1
				dateTimeSQL  = messageSplit[gExtractHorodatageChkRang -1]
			# non: horodatage pas dans message donc on le cré
			else:
				gExtractHorodatageChkRang = 0
				dateTimeSQL  = (time.strftime("%Y-%m-%d ") + time.strftime("%H:%M:%S"))
			#==== catégorie inclus dans message ?
			# oui: catégorie inclus dans message donc on l'extrait
			if gExtractCategorieChk:
				gExtractCategorieChkRang = 1
				categorieSQL   = messageSplit[gExtractHorodatageChkRang + gExtractCategorieChkRang -1]
			# non: catégorie pas dans message donc on le cré avec la saisie
			else:
				gExtractCategorieChkRang = 0
				categorieSQL   = gExtractCategorieTxt
			#==== niveau detail inclus dans message ?
			# oui: niveau detail inclus dans message donc on l'extrait
			if gExtractNivDetailChk:
				gExtractNivDetailChkRang = 1
				niv_detailSQL   = messageSplit[gExtractHorodatageChkRang + gExtractCategorieChkRang + gExtractNivDetailChkRang -1]
			# non: niveau detail pas dans message donc on le cré avec la saisie
			else:
				gExtractNivDetailChkRang = 0	
				niv_detailSQL   = gExtractNivDetailNum
			try:
				messageSQL = messageSplit[gExtractHorodatageChkRang + gExtractCategorieChkRang + gExtractNivDetailChkRang]
			except Exception:
				MsgLog(self,u'Erreur separation texte avec separateur: "' + gCaractereSeparateurTxt + u'". Forcage horodatage')
				dateTimeSQL  = (time.strftime("%Y-%m-%d ") + time.strftime("%H:%M:%S"))
				messageSQL   = message
		# non: pas d'extraction
		else:
			# date heure système +catégorie saisie +niveau détail saisie +message brut
			dateTimeSQL  = (time.strftime("%Y-%m-%d ") + time.strftime("%H:%M:%S"))
			categorieSQL = gExtractCategorieTxt
			niv_detailSQL= gExtractNivDetailNum
			messageSQL   = message
		# composition de la requete SQL
		#print u"== composition requete =="
		#print "message=" + message
		#print "dateTimeSQL  : " + dateTimeSQL
		#print "categorieSQL : " + categorieSQL
		#print "niv_detailSQL: " + niv_detailSQL
		#print "messageSQL   : " + messageSQL
		requeteSQL = ""
		requeteHeader = u"INSERT INTO " + gSQLdataTable + u" (horodatage,categorie,niv_detail,message) "
		#requeteHeader = u"INSERT INTO arduino " + u" (horodatage,categorie,niv_detail,message) "
		try:
			requeteSQL = requeteHeader + u"VALUES ('"+dateTimeSQL + u"','"+categorieSQL + u"',"+str(niv_detailSQL) + u",'"+messageSQL + u"')"
		except Exception:
			print u"MysqlInsert: Erreur avec la composition Requête"
		#else:
			#print u"MysqlInsert: Pas d erreur avec la composition Rêquete"
		# tentative d'execussion de la requete
		try:
			#print u"MysqlInsert: base MySQL ouverte"
			cur = db.cursor() 
			# execute la requete
			cur.execute(requeteSQL)
			#print u"MysqlInsert: ...Mise à jour de la base"
			db.commit()
		except Exception:
			print u"MysqlInsert: Erreur avec la Requête= " + requeteSQL
			print u"MysqlInsert: ...Retour etat précédant de la base"
			db.rollback()
		else:
			#print u"MysqlInsert: Requête éxecutée avec:"
			#print requeteSQL
			#MsgLog(self, requeteSQL)
			db.close()
			#print u"MysqlInsert: base fermée. Fin"
			
#####################################################
# 					Fonction MysqlShowTable(self)
# Principe	:	Donne la liste des table SQL disponibles
# Dépandence:	Import MySQLdb
# Appelé par:	bouton GUI SQL
# 2015-02-25:	Création
#####################################################
def MysqlShowTable(self):
	global gSQLserver
	global gSQLuser
	global gSQLpasswd
	global gSQLdataBase
	global gSQLlisteTable
	try:
		#MysqlInsert: print "base MySQL ouverture..."
		db = MySQLdb.connect(host=gSQLserver,user=gSQLuser,passwd=gSQLpasswd,db=gSQLdataBase)
	except Exception:
		MsgLog(self, u'Erreur connexion SQL vers ' + gSQLserver)
		# appel popup erreur connexion MySQL
		boxErr = wx.MessageDialog(None,'Erreur connexion SQL vers ' + gSQLserver, 'Erreur:', wx.OK)
		reponse=boxErr.ShowModal()
		boxErr.Destroy()
	else:
		# composition de la requete SQL
		requeteSQL = "SHOW TABLE STATUS FROM serial_sql_logger_data;"
		try:
			requeteSQL = requeteSQL
		except Exception:
			print u"MysqlShowTable: Erreur avec la composition Requête"
		#else:
			#print u"MysqlInsert: Pas d erreur avec la composition Rêquete"
		# tentative d'execussion de la requete
		try:
			print u"MysqlShowTable: base MySQL ouverte"
			cur = db.cursor() 
			# execute la requete
			cur.execute(requeteSQL)
			print u"MysqlShowTable: ...execute"
			db.commit()
		except Exception:
			print u"MysqlShowTable: Erreur avec la Requête= " + requeteSQL
			print u"MysqlShowTable: ...Retour etat précédant de la base"
			db.rollback()
		else:
			print u"MysqlShowTable: Requête éxecutée avec:"
			print requeteSQL
			#MsgLog(self, requeteSQL)
			# efface la liste
			gSQLlisteTable[:] = []
			# lecture résultat
			for row in cur.fetchall() :
				print row[0]
				gSQLlisteTable.append(row[0])   
			db.close()
			print u"MysqlShowTable: base fermée. Fin"

	
#####################################################
# 					Fonction character()
# Principe	:	Adapte l'encodage en fonction version python
# Notes		:	Repris de miniterm.py de pyserial
# Dépandence:	Aucune
# Appelé par:	reader()
# 2015-05-06:	Création
#####################################################
def character(b):
	if sys.version_info >= (3, 0):
		return b
	else:
		return b.decode('latin1')



#================ DEBUT APPLI ================
# Dossier de l'appli
appliFolderName = os.getcwd()
print u"appliFolderName= " + appliFolderName
# detection de l'OS
print u"Architecture systeme:"
print platform.architecture()
print u"Systeme d'exploitation:"
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
print(u'g_architectBits='+g_architectBits)
# detection version python
print "detection version python:"
print str(sys.version_info[0])+"."+str(sys.version_info[1])+str(sys.version_info[2])+" "+str(sys.version_info[3])
# start GUI
app = wx.App(False)
#wx.InitAllImageHandlers()
# creation de l'object screenHome depuis la class screenMain
screenHome = screenMain(None)
# scan port serie dispo:
#FindCOM()
compteurGbl 				= 0
erreurGbl					= False
erreurBlinkGbl 				= False
runBlinkGbl					= False
enableBlinkGbl				= True
enableErrBlinkGbl			= True
bmpCirculaireIndexGbl=1
# init zones de status appli
AppliTitreGbl 				= "Serial SQL Logger"
ProfileNameGbl				= "Aucun"
# Port série
COMselectGbl  				= "Non select."
COMvitesseGbl 				= 115200
statusRunStopGbl			= 0
# encodage
gDecodeSerieTxt		 		= "cp1252"
gDecodeSerieWin1252Chk		= True
gEncodeSqlTxt		 		= "utf_8"
gEncodeSqlUTF8Chk			= True
gEncodeGuiTxt				= "utf_8"
gEncodeGuiUTF8Chk			= True
# SQL
gSQLserver					= "localhost"
gSQLuser					= "root"
gSQLpasswd  				= ""
gSQLdataTable				= ""
gSQLdataBase				= "serial_sql_logger_data"
gSQLenable					= 0
gSQLcompleteLineTxt			= ""
gExtractHorodatageChk		= False
gExtractCategorieChk		= False
gExtractCategorieTxt		= ""
gExtractNivDetailChk		= False
gExtractNivDetailNum		= 1
gCaractereSeparateurTxt		= ""
gCaractereSeparateurEnable	= False
gSQLlisteTable = []			# liste vide
# init ligne status dans GUI
screenHome.m_statusActionTextStat.SetLabel("Choisissez un port serie.")
screenHome.m_statusComTextStat.SetLabel("Port serie: "+COMselectGbl)
screenHome.m_statusVitesseTextStat.SetLabel("Vitesse: "+str(COMvitesseGbl)+" bds")
# init status encodage
screenHome.m_statusDecodeSerieTxt.SetLabel("Decodage Serie: " + gDecodeSerieTxt)
screenHome.m_statusEncodeSqlTxt.SetLabel("Encodage SQL: " + gEncodeSqlTxt)
screenHome.m_statusEncodeGuiTxt.SetLabel("Encodage GUI: " + gEncodeGuiTxt)
# masquage par défaut des options SQL
screenHome.m_separateurTxt.Hide()
screenHome.m_separateurCbx.Hide()
screenHome.spacer_10x20_01.Hide()
screenHome.m_ExtractHorodateChk.Hide()
screenHome.spacer_10x20_02.Hide()
screenHome.m_ExtractCategorieChk.Hide()
screenHome.spacer_10x20_03.Hide()
screenHome.m_CategorieLbl.Hide()
screenHome.m_CategorieTxt.Hide()
screenHome.spacer_10x20_04.Hide()
screenHome.m_ExtractNivDetailChk.Hide()
screenHome.m_ExtractNivDetailLbl.Hide()
screenHome.m_ExtractNivDetailNum.Hide()

# affichage de l'écran principal
screenHome.Show(True)
# Démarrage de l'applications
app.MainLoop()

