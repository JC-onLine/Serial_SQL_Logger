# -*- coding: utf-8 -*-

#####################################################################################
#
# 					Serial_SQL_Logger_GUI_MAIN.py
#
# Principe	:	Le but est derecevoir des logs depuis le port série,
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
#
#####################################################################################
# TODO:
#				[ ] Marquer le nom du fichier en cours dans la barre de titre appli
#				[ ] Raccourcie clavier Ctrl+N Ctrl+O Ctrl+S Ctrl+Shift+S Ctrl+Q
#				[ ] Remplacer boutons OK/Cancel par un bouton 'Envoyer vers Arduino'
#				[ ] Mettre une icônes dans la barre de titre appli
#				[ ] Voir si possible de mettre icônes dans menu Fichier/ouvrir etc
#				[ ] Detecter OS pour compatibilité Windows/Linux
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
# gestion des tâches
import threading

# variables globales
global COMselectGbl
global COMvitesseGbl
global statusRunStopGbl

# Evénement lié au port série
SERIALRX = wx.NewEventType()
# bind to serial data receive events
EVT_SERIALRX = wx.PyEventBinder(SERIALRX, 0)

class SerialRxEvent(wx.PyCommandEvent):
	eventType = SERIALRX
	def __init__(self, windowID, data):
		wx.PyCommandEvent.__init__(self, self.eventType, windowID)
		self.data = data
	def Clone(self):
		self.__class__(self.GetId(), self.data)

ID_CLEAR        = wx.NewId()
ID_SAVEAS       = wx.NewId()
ID_SETTINGS     = wx.NewId()
ID_TERM         = wx.NewId()
ID_EXIT         = wx.NewId()
# constante caratère fin de ligne
NEWLINE_CR      = 0
NEWLINE_LF      = 1
NEWLINE_CRLF    = 2


class screenMain(Serial_SQL_Logger_GUI.FenetrePrincipaleClass):
	# constructor
	def __init__(self,parent):
		self.Bind( wx.PyEventBinder(SERIALRX, 0), self.OnSerialRead)
		#self.Bind( wx.EVT_MENU,                   self.m_COM1mnuEvt, id = self.m_COM1mnu.GetId() )
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
        #self.SetSize((546, 383))
		# init nom fichier+dossier
        nomFichierDonnees = ""
        nomDossierDonnees = ""
		
	def OnSerialRead(self, event):
		"""Handle input from the serial port."""
		text = event.data
		#unprintable = 
		#if self.settings.unprintable:
		#	text = ''.join([(c >= ' ') and c or '<%d>' % ord(c)  for c in text])
		self.logTextCtrl.AppendText(text)

	#def __attach_events(self):
		#register events at the controls
		#self.Bind(EVT_SERIALRX, self.OnSerialRead)
		#self.Bind(wx.EVT_CLOSE, self.OnClose)

	def ComPortThread(self):
		"""Thread that handles the incomming traffic. Does the basic input
			transformation (newlines) and generates an SerialRxEvent"""
		while self.alive.isSet():				#loop while alive event is true
			#text = self.portSerie.read(1)		#read one, with timout
			#text = ""		#read one, with timout
			if text:							#check if not timeout
				n = self.portSerie.inWaiting()		#look if there is more to read
				if n:
					text = text + self.portSerie.read(n) #get it
				#newline transformation
				setting = NEWLINE_CRLF
				if setting == NEWLINE_CR:
					text = text.replace('\r', '\n')
				elif setting == NEWLINE_LF:
					pass
				elif setting == NEWLINE_CRLF:
					text = text.replace('\r\n', '\n')
				event = SerialRxEvent(self.GetId(), text)
				self.GetEventHandler().AddPendingEvent(event)
				
	def StartThread(self):
		# défini la tache surveillance réception série (fonction ComPortThread)
		self.thread = threading.Thread(target=self.ComPortThread)
		self.thread.setDaemon(1)
		self.alive.set()
		try:
			self.thread.start()
		except:
			print('Erreur StartThread')
			boxErr = wx.MessageDialog(None,'Erreur StartThread', 'Erreur lecture fichier:', wx.OK)
			reponse=boxErr.ShowModal()
			boxErr.Destroy()

	def StopThread(self):
		"""Stop the receiver thread, wait util it's finished."""
		if self.thread is not None:
			self.alive.clear()			#clear alive event for thread
			self.thread.join()			#wait until thread has finished
			self.thread = None

	def OnClose(self, event):
		"""Called on application shutdown."""
		self.StopThread()				#stop reader thread
		self.portSerie.close()			#cleanup
		self.Destroy()					#close windows, exit app

	# capture de l'événement clic 'RUN'
	def m_bntRunEvt(self,event):
		global COMselectGbl
		global COMvitesseGbl
		print("Capture evenement bouton RUN")
		# test si variable COMselectGbl est definie
		try:
			COMselectGbl
		except NameError:
			print('Port serie non defini.')
			boxErr = wx.MessageDialog(None,'Port serie non defini.', 'Erreur:', wx.OK)
			reponse=boxErr.ShowModal()
			boxErr.Destroy()
		# la variable est definie, on continue
		else:
			#initialisation et ouverture du port série
			try:
				#self.portSerie = serial.Serial(str(COMselectGbl),int(COMvitesseGbl))
				#self.portSerie.portstr  = str(COMselectGbl)
				#self.portSerie.baudrate = int(COMvitesseGbl)
				self.portSerie.portstr  = "COM4"
				#self.portSerie.baudrate = 115200
				#self.portSerie.open()
			except Exception:
				print('Erreur avec le port serie '+COMselectGbl)
				boxErr = wx.MessageDialog(None,'Erreur avec le port serie '+COMselectGbl, 'Erreur:', wx.OK)
				reponse=boxErr.ShowModal()
				boxErr.Destroy()
			else:
				# pas d'erreur, on continue:
				self.portSerie.timeout = 0.5   #make sure that the alive event can be checked from time to time
				# animation led run
				imageLedRun  = wx.Bitmap("LedRUN.png",  wx.BITMAP_TYPE_ANY)
				self.m_bmpRunStop.SetBitmap(imageLedRun)
				print('Port serie '+COMselectGbl+' ouvert.')
				# flag appli en run
				global statusRunStopGbl
				statusRunStopGbl = 1
				# démarrage scrutation réception série
				self.StartThread()
				
	# capture de l'événement clic 'STOP'
	def m_bntStopEvt(self,event):
		global COMselectGbl
		print("Capture evenement bouton STOP")
		#Fermeture du pour série
		try:
			self.portSerie.close()
		except NameError:
			print('Erreur a la fermeture du Port serie '+COMselectGbl)
			boxErr = wx.MessageDialog(None,'Erreur a la fermeture du Port serie '+COMselectGbl, 'Erreur:', wx.OK)
			reponse=boxErr.ShowModal()
			boxErr.Destroy()
		else:
			print('Port serie '+COMselectGbl+' ferme.')
			imageLedStop = wx.Bitmap("LedSTOP.png", wx.BITMAP_TYPE_ANY)
			self.m_bmpRunStop.SetBitmap(imageLedStop)
			global statusRunStopGbl
			statusRunStopGbl = 0
			self.StopThread()               #stop reader thread
			self.portSerie.close()             #cleanup
					
	
	######## MENU [Fichier] ########
	# capture de l'événement selection menu <Nouveau>
	def m_nouveauMnuEvt(self,event):
		print("Nouveau script")
		self.m_progressBar.Value = 0
		self.commandeTextCtrl.Value = ""
	# capture de l'événement selection menu <Ouvrir>
	def m_ouvrirCdeMnuEvt(self,event):
		print("Menu: Ouvrir")
		popupOpen = wx.FileDialog(self, "Ouvrir", self.nomDossierDonnees, self.nomFichierDonnees,
						"Fichier texte (*.txt)|*.txt|All Files|*.*", wx.OPEN)
		if (popupOpen.ShowModal() == wx.ID_OK):
			self.nomFichierDonnees = popupOpen.GetFilename()
			self.nomDossierDonnees = popupOpen.GetDirectory()
			try:
				# accès fichier en lecture
				pointeurFichier = file(os.path.join(self.nomDossierDonnees, self.nomFichierDonnees), 'r')
				self.commandeTextCtrl.SetValue(pointeurFichier.read())
				pointeurFichier.close()
			except:
				print('Erreur lecture du fichier: '+self.nomFichierDonnees)
				boxErr = wx.MessageDialog(None,'Erreur lecture du fichier: '+self.nomFichierDonnees, 'Erreur lecture fichier:', wx.OK)
				reponse=boxErr.ShowModal()
				boxErr.Destroy()
		popupOpen.Destroy()
	# capture de l'événement selection menu <Enregistrer>
	def m_enregistrerCdeMnuEvt(self,event):
		print("Menu: Enregistrer commandes")
		# enregistre si fichier/dossier ont un nom
		if (self.nomFichierDonnees !="") and (self.nomDossierDonnees != ""):
			try:
				# accès fichier en écriture
				pointeurFichier = file(os.path.join(self.nomDossierDonnees, self.nomFichierDonnees), 'w')
				pointeurFichier.write(self.commandeTextCtrl.GetValue())
				return True
			except:
				print('Erreur ecriture du fichier: '+self.nomFichierDonnees)
				boxErr = wx.MessageDialog(None,'Erreur ecriture du fichier: '+self.nomFichierDonnees, 'Erreur enregistrement fichier:', wx.OK)
				reponse=boxErr.ShowModal()
				boxErr.Destroy()
				return False
		# sinon popup <Enregistrer sous...>
		else:
			print('Fichier sans nom: go <Enregistrer sous...> ')
			self.m_enregistrerSousCdeMnuEvt(self)
	# capture de l'événement selection menu <Enregistrer sous...>
	def m_enregistrerSousCdeMnuEvt(self,event):
		print("Menu: Enregistrer commandes sous...")
		popupSaveAs = wx.FileDialog(self, "Enregister sous...", self.nomDossierDonnees, self.nomFichierDonnees,
						"Fichier texte (*.txt)|*.txt|All Files|*.*", wx.SAVE)
		if (popupSaveAs.ShowModal() == wx.ID_OK):
			self.nomFichierDonnees = popupSaveAs.GetFilename()
			self.nomDossierDonnees = popupSaveAs.GetDirectory()
			# on réutilise la fonction d'enregistrement
			if self.m_enregistrerCdeMnuEvt(self):
				#self.FenetrePrincipaleClass.SetTitle(self.APP_NAME + " - [" +self.nomFichierDonnees+ "]")
				print("Commandes serie vers Afficheur Arduino Uno - [" + self.nomFichierDonnees + "]")
	# capture de l'événement selection menu <Quiter>
	def m_quiterMnuEvt(self,event):
		print("Menu: Quiter")
		global statusRunStopGbl
		if (statusRunStopGbl == 1):
			self.portSerie.close()
			print('Fermeture Port serie '+COMselectGbl +' car reste ouvert...')
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
		self.m_statusActionTextStat.SetLabel("Recherche ports COM en cours...")
		ActualiserCOM()
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
		self.m_statusActionTextStat.SetLabel("Selection manuelle: "+ COMselectGbl)
		self.m_statusComTextStat.SetLabel("Port serie: " + COMselectGbl)
	# capture de l'événement selection menu COM1
	def m_COM1mnuEvt(self,event):
		global COMselectGbl
		COMselectGbl = "COM1"
		print("COMselectGbl: " + COMselectGbl)
		self.m_statusComTextStat.SetLabel("Port serie: " + COMselectGbl)
		self.m_statusActionTextStat.SetLabel("Pret.")
	# menu COM2
	def m_COM2mnuEvt(self,event):
		global COMselectGbl
		COMselectGbl = "COM2"
		print("COMselectGbl: " + COMselectGbl)
		self.m_statusComTextStat.SetLabel("Port serie: " + COMselectGbl)
		self.m_statusActionTextStat.SetLabel("Pret.")
	# menu COM3
	def m_COM3mnuEvt(self,event):
		global COMselectGbl
		COMselectGbl = "COM3"
		print("COMselectGbl: " + COMselectGbl)
		self.m_statusComTextStat.SetLabel("Port serie: " + COMselectGbl)
		self.m_statusActionTextStat.SetLabel("Pret.")
	# menu COM4
	def m_COM4mnuEvt(self,event):
		global COMselectGbl
		COMselectGbl = "COM4"
		print("COMselectGbl: " + COMselectGbl)
		self.m_statusComTextStat.SetLabel("Port serie: " + COMselectGbl)
		self.m_statusActionTextStat.SetLabel("Pret.")
	# menu COM5
	def m_COM5mnuEvt(self,event):
		global COMselectGbl
		COMselectGbl = "COM5"
		print("COMselectGbl: " + COMselectGbl)
		self.m_statusComTextStat.SetLabel("Port serie: " + COMselectGbl)
		self.m_statusActionTextStat.SetLabel("Pret.")
	# menu COM6
	def m_COM6mnuEvt(self,event):
		global COMselectGbl
		COMselectGbl = "COM6"
		print("COMselectGbl: " + COMselectGbl)
		self.m_statusComTextStat.SetLabel("Port serie: " + COMselectGbl)
		self.m_statusActionTextStat.SetLabel("Pret.")
	# menu COM7
	def m_COM7mnuEvt(self,event):
		global COMselectGbl
		COMselectGbl = "COM7"
		print("COMselectGbl: " + COMselectGbl)
		self.m_statusComTextStat.SetLabel("Port serie: " + COMselectGbl)
		self.m_statusActionTextStat.SetLabel("Pret.")
	# menu COM8
	def m_COM8mnuEvt(self,event):
		global COMselectGbl
		COMselectGbl = "COM8"
		print("COMselectGbl: " + COMselectGbl)
		self.m_statusComTextStat.SetLabel("Port serie: " + COMselectGbl)
		self.m_statusActionTextStat.SetLabel("Pret.")
	# menu COM9
	def m_COM9mnuEvt(self,event):
		global COMselectGbl
		COMselectGbl = "COM9"
		print("COMselectGbl: " + COMselectGbl)
		self.m_statusComTextStat.SetLabel("Port serie: " + COMselectGbl)
		self.m_statusActionTextStat.SetLabel("Pret.")
	# menu COM10
	def m_COM10mnuEvt(self,event):
		global COMselectGbl
		COMselectGbl = "COM10"
		print("COMselectGbl: " + COMselectGbl)
		self.m_statusComTextStat.SetLabel("Port serie: " + COMselectGbl)
		self.m_statusActionTextStat.SetLabel("Pret.")
	# menu COM11
	def m_COM11mnuEvt(self,event):
		global COMselectGbl
		COMselectGbl = "COM11"
		print("COMselectGbl: " + COMselectGbl)
		self.m_statusComTextStat.SetLabel("Port serie: " + COMselectGbl)
		self.m_statusActionTextStat.SetLabel("Pret.")
	# menu COM12
	def m_COM12mnuEvt(self,event):
		global COMselectGbl
		COMselectGbl = "COM12"
		print("COMselectGbl: " + COMselectGbl)
		self.m_statusComTextStat.SetLabel("Port serie: " + COMselectGbl)
		self.m_statusActionTextStat.SetLabel("Pret.")
	# menu COM13
	def m_COM13mnuEvt(self,event):
		global COMselectGbl
		COMselectGbl = "COM13"
		print("COMselectGbl: " + COMselectGbl)
		self.m_statusComTextStat.SetLabel("Port serie: " + COMselectGbl)
		self.m_statusActionTextStat.SetLabel("Pret.")
	# menu COM14
	def m_COM14mnuEvt(self,event):
		global COMselectGbl
		COMselectGbl = "COM14"
		print("COMselectGbl: " + COMselectGbl)
		self.m_statusComTextStat.SetLabel("Port serie: " + COMselectGbl)
		self.m_statusActionTextStat.SetLabel("Pret.")
	# menu COM15
	def m_COM15mnuEvt(self,event):
		global COMselectGbl
		COMselectGbl = "COM15"
		print("COMselectGbl: " + COMselectGbl)
		self.m_statusComTextStat.SetLabel("Port serie: " + COMselectGbl)
		self.m_statusActionTextStat.SetLabel("Pret.")
	# menu COM16
	def m_COM16mnuEvt(self,event):
		global COMselectGbl
		COMselectGbl = "COM16"
		print("COMselectGbl: " + COMselectGbl)
		self.m_statusComTextStat.SetLabel("Port serie: " + COMselectGbl)
		self.m_statusActionTextStat.SetLabel("Pret.")
	# menu COM17
	def m_COM17mnuEvt(self,event):
		global COMselectGbl
		COMselectGbl = "COM17"
		print("COMselectGbl: " + COMselectGbl)
		self.m_statusComTextStat.SetLabel("Port serie: " + COMselectGbl)
		self.m_statusActionTextStat.SetLabel("Pret.")
	# menu COM18
	def m_COM18mnuEvt(self,event):
		global COMselectGbl
		COMselectGbl = "COM18"
		print("COMselectGbl: " + COMselectGbl)
		self.m_statusComTextStat.SetLabel("Port serie: " + COMselectGbl)
		self.m_statusActionTextStat.SetLabel("Pret.")
	# menu COM19
	def m_COM19mnuEvt(self,event):
		global COMselectGbl
		COMselectGbl = "COM19"
		print("COMselectGbl: " + COMselectGbl)
		self.m_statusComTextStat.SetLabel("Port serie: " + COMselectGbl)
		self.m_statusActionTextStat.SetLabel("Pret.")
	# menu COM20
	def m_COM20mnuEvt(self,event):
		global COMselectGbl
		COMselectGbl = "COM20"
		print("COMselectGbl: " + COMselectGbl)
		self.m_statusComTextStat.SetLabel("Port serie: " + COMselectGbl)
		self.m_statusActionTextStat.SetLabel("Pret.")
	######## MENU [Vitesse COM] ########
	# capture de l'événement selection menu <115200 bds>
	def m_115200mnuEvt(self,event):
		global COMvitesseGbl
		COMvitesseGbl = 115200
		print("COMvitesseGbl: " + str(COMvitesseGbl))
		self.m_statusVitesseTextStat.SetLabel("Vitesse: "+str(COMvitesseGbl)+" bds")
	# menu <57600 bds>
	def m_57600mnuEvt(self,event):
		global COMvitesseGbl
		COMvitesseGbl = 57600
		print("COMvitesseGbl: " + str(COMvitesseGbl))
		self.m_statusVitesseTextStat.SetLabel("Vitesse: "+str(COMvitesseGbl)+" bds")
	# menu <19200 bds>
	def m_19200mnuEvt(self,event):
		global COMvitesseGbl
		COMvitesseGbl = 19200
		print("COMvitesseGbl: " + str(COMvitesseGbl))
		self.m_statusVitesseTextStat.SetLabel("Vitesse: "+str(COMvitesseGbl)+" bds")
	# menu <9600 bds>
	def m_9600mnuEvt(self,event):
		global COMvitesseGbl
		COMvitesseGbl = 9600
		print("COMvitesseGbl: " + str(COMvitesseGbl))
		self.m_statusVitesseTextStat.SetLabel("Vitesse: "+str(COMvitesseGbl)+" bds")
	# menu <4800 bds>
	def m_4800mnuEvt(self,event):
		global COMvitesseGbl
		COMvitesseGbl = 4800
		print("COMvitesseGbl: " + str(COMvitesseGbl))
		self.m_statusVitesseTextStat.SetLabel("Vitesse: "+str(COMvitesseGbl)+" bds")
	# menu <2400 bds>
	def m_2400mnuEvt(self,event):
		global COMvitesseGbl
		COMvitesseGbl = 2400
		print("COMvitesseGbl: " + str(COMvitesseGbl))
		self.m_statusVitesseTextStat.SetLabel("Vitesse: "+str(COMvitesseGbl)+" bds")
	# menu <1200 bds>
	def m_1200mnuEvt(self,event):
		global COMvitesseGbl
		COMvitesseGbl = 1200
		print("COMvitesseGbl: " + str(COMvitesseGbl))
		self.m_statusVitesseTextStat.SetLabel("Vitesse: "+str(COMvitesseGbl)+" bds")
	######## MENU [Système] ########
	# menu <gestionnaire de periphérique>
	def m_gestPeriphMnuEvt(self,event):
		os.startfile('devmgmt.msc')
	######## BOUTONS + SLIDER ########
	# supprimer..




def scan():
	"""scan for available ports. return a list of tuples (num, name)"""
	available = []
	for i in range(256):
		try:
			s = serial.Serial(i)
			available.append( (i, s.portstr))
			s.close()   # explicit close 'cause of delayed GC in java
		except serial.SerialException:
			pass
	return available

def ActualiserCOM():
	# désactivation de tous les ports dans le menu avant actualisation
	screenHome.m_COM1mnu.Enable( False )
	screenHome.m_COM2mnu.Enable( False )
	screenHome.m_COM3mnu.Enable( False )
	screenHome.m_COM4mnu.Enable( False )
	screenHome.m_COM5mnu.Enable( False )
	screenHome.m_COM6mnu.Enable( False )
	screenHome.m_COM7mnu.Enable( False )
	screenHome.m_COM8mnu.Enable( False )
	screenHome.m_COM9mnu.Enable( False )
	screenHome.m_COM10mnu.Enable( False )
	screenHome.m_COM11mnu.Enable( False )
	screenHome.m_COM12mnu.Enable( False )
	screenHome.m_COM13mnu.Enable( False )
	screenHome.m_COM14mnu.Enable( False )
	screenHome.m_COM15mnu.Enable( False )
	screenHome.m_COM16mnu.Enable( False )
	screenHome.m_COM17mnu.Enable( False )
	screenHome.m_COM18mnu.Enable( False )
	screenHome.m_COM19mnu.Enable( False )
	screenHome.m_COM20mnu.Enable( False )
	# scan port serie dispo:
	#COMselectGbl = "COM1"
	print "Ports dispo:"
	for n,s in scan():
		print "(%d) %s" % (n,s)
		# activation menu port serie en fonction des COM dispo
		enableCOM(s)

def enableCOM(COMname):
	global COMselectGbl
	if COMname == "COM1":
		screenHome.m_COM1mnu.Enable( True )
	if COMname == "COM2":
		screenHome.m_COM2mnu.Enable( True )
	if COMname == "COM3":
		screenHome.m_COM3mnu.Enable( True )
	if COMname == "COM4":
		screenHome.m_COM4mnu.Enable( True )
	if COMname == "COM5":
		screenHome.m_COM5mnu.Enable( True )
	if COMname == "COM6":
		screenHome.m_COM6mnu.Enable( True )
	if COMname == "COM7":
		screenHome.m_COM7mnu.Enable( True )
	if COMname == "COM8":
		screenHome.m_COM8mnu.Enable( True )
	if COMname == "COM9":
		screenHome.m_COM9mnu.Enable( True )
	if COMname == "COM10":
		screenHome.m_COM10mnu.Enable( True )
	if COMname == "COM11":
		screenHome.m_COM11mnu.Enable( True )
	if COMname == "COM12":
		screenHome.m_COM12mnu.Enable( True )
	if COMname == "COM13":
		screenHome.m_COM13mnu.Enable( True )
	if COMname == "COM14":
		screenHome.m_COM14mnu.Enable( True )
	if COMname == "COM15":
		screenHome.m_COM15mnu.Enable( True )
	if COMname == "COM16":
		screenHome.m_COM16mnu.Enable( True )
	if COMname == "COM17":
		screenHome.m_COM17mnu.Enable( True )
	if COMname == "COM18":
		screenHome.m_COM18mnu.Enable( True )
	if COMname == "COM19":
		screenHome.m_COM19mnu.Enable( True )
	if COMname == "COM20":
		screenHome.m_COM20mnu.Enable( True )
	COMselectGbl = COMname


#================ DEBUT APPLI ================
app = wx.App(False)
#wx.InitAllImageHandlers()
# creation de l'object screenHome depuis la class screenMain
screenHome = screenMain(None)
# scan port serie dispo:
#ActualiserCOM()

#portSerie = serial.Serial()

# init zones de status appli
screenHome.m_statusActionTextStat.SetLabel("Choisissez un port serie.")
screenHome.m_statusComTextStat.SetLabel("Port serie: Non select.")
COMvitesseGbl = 115200
statusRunStopGbl = 0
screenHome.m_statusVitesseTextStat.SetLabel("Vitesse: "+str(COMvitesseGbl)+" bds")
# affichage de l'écran principal
screenHome.Show(True)
# Démarrage de l'applications
app.MainLoop()

