# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Feb 26 2014)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class FenetrePrincipaleClass
###########################################################################

class FenetrePrincipaleClass ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Serial SQL Logger", pos = wx.DefaultPosition, size = wx.Size( 1000,700 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.MINIMIZE_BOX|wx.SYSTEM_MENU|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_3DLIGHT ) )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.logTextCtrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,550 ), wx.TE_MULTILINE )
		bSizer1.Add( self.logTextCtrl, 0, wx.ALL|wx.EXPAND, 5 )
		
		bSizer31 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_bmpRunStop = wx.StaticBitmap( self, wx.ID_ANY, wx.Bitmap( u"LedSTOP.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		bSizer31.Add( self.m_bmpRunStop, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_bntRun = wx.Button( self, wx.ID_ANY, u"RUN", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer31.Add( self.m_bntRun, 0, wx.ALL, 5 )
		
		self.m_bntStop = wx.Button( self, wx.ID_ANY, u"STOP", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer31.Add( self.m_bntStop, 0, wx.ALL, 5 )
		
		self.m_compteurTxt = wx.StaticText( self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_compteurTxt.Wrap( -1 )
		self.m_compteurTxt.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 90, False, wx.EmptyString ) )
		self.m_compteurTxt.SetToolTipString( u"Compteur de test" )
		
		bSizer31.Add( self.m_compteurTxt, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer1.Add( bSizer31, 1, wx.EXPAND, 5 )
		
		bSizer3 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_statusActionTextStat = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 300,-1 ), 0|wx.DOUBLE_BORDER )
		self.m_statusActionTextStat.Wrap( -1 )
		bSizer3.Add( self.m_statusActionTextStat, 0, wx.ALL, 5 )
		
		self.m_statusComTextStat = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 150,-1 ), 0|wx.DOUBLE_BORDER )
		self.m_statusComTextStat.Wrap( -1 )
		bSizer3.Add( self.m_statusComTextStat, 0, wx.ALL, 5 )
		
		self.m_statusVitesseTextStat = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 150,-1 ), 0|wx.DOUBLE_BORDER )
		self.m_statusVitesseTextStat.Wrap( -1 )
		bSizer3.Add( self.m_statusVitesseTextStat, 0, wx.ALL, 5 )
		
		
		bSizer1.Add( bSizer3, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		self.m_timer1 = wx.Timer()
		self.m_timer1.SetOwner( self, wx.ID_ANY )
		self.m_timer1.Start( 500 )
		
		self.m_statusBar1 = self.CreateStatusBar( 2, wx.ST_SIZEGRIP, wx.ID_ANY )
		self.m_menubar1 = wx.MenuBar( 0 )
		self.m_fichierMnu = wx.Menu()
		self.m_nouveauMnu = wx.MenuItem( self.m_fichierMnu, wx.ID_ANY, u"Nouveau", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_fichierMnu.AppendItem( self.m_nouveauMnu )
		
		self.m_ouvrirCdeMnu = wx.MenuItem( self.m_fichierMnu, wx.ID_ANY, u"Ouvrir", u"Ouvrir un fichier de commande", wx.ITEM_NORMAL )
		self.m_fichierMnu.AppendItem( self.m_ouvrirCdeMnu )
		
		self.m_enregistrerCdeMnu = wx.MenuItem( self.m_fichierMnu, wx.ID_ANY, u"Enregistrer", u"Enregistrer un fichier de commande", wx.ITEM_NORMAL )
		self.m_fichierMnu.AppendItem( self.m_enregistrerCdeMnu )
		
		self.m_enregistrerSousCdeMnu = wx.MenuItem( self.m_fichierMnu, wx.ID_ANY, u"Enregistrer sous...", u"Enregistrer un fichier de commande, sous...", wx.ITEM_NORMAL )
		self.m_fichierMnu.AppendItem( self.m_enregistrerSousCdeMnu )
		
		self.m_quiterMnu = wx.MenuItem( self.m_fichierMnu, wx.ID_ANY, u"Quiter", u"Quiter l'application", wx.ITEM_NORMAL )
		self.m_fichierMnu.AppendItem( self.m_quiterMnu )
		
		self.m_menubar1.Append( self.m_fichierMnu, u"Fichier" ) 
		
		self.m_portComMnu = wx.Menu()
		self.m_menuVide = wx.MenuItem( self.m_portComMnu, wx.ID_ANY, u"    -  -  -  -", wx.EmptyString, wx.ITEM_RADIO )
		self.m_portComMnu.AppendItem( self.m_menuVide )
		
		self.m_COMactualiserMnu = wx.MenuItem( self.m_portComMnu, wx.ID_ANY, u"<Actualiser>", u"Saisir au clavier le nom du port série", wx.ITEM_RADIO )
		self.m_portComMnu.AppendItem( self.m_COMactualiserMnu )
		
		self.m_COMmanuMnu = wx.MenuItem( self.m_portComMnu, wx.ID_ANY, u"<Sélection Manuelle>", wx.EmptyString, wx.ITEM_RADIO )
		self.m_portComMnu.AppendItem( self.m_COMmanuMnu )
		
		self.m_COM1mnu = wx.MenuItem( self.m_portComMnu, wx.ID_ANY, u"COM1", wx.EmptyString, wx.ITEM_RADIO )
		self.m_portComMnu.AppendItem( self.m_COM1mnu )
		self.m_COM1mnu.Enable( False )
		
		self.m_COM2mnu = wx.MenuItem( self.m_portComMnu, wx.ID_ANY, u"COM2", wx.EmptyString, wx.ITEM_RADIO )
		self.m_portComMnu.AppendItem( self.m_COM2mnu )
		self.m_COM2mnu.Enable( False )
		
		self.m_COM3mnu = wx.MenuItem( self.m_portComMnu, wx.ID_ANY, u"COM3", wx.EmptyString, wx.ITEM_RADIO )
		self.m_portComMnu.AppendItem( self.m_COM3mnu )
		self.m_COM3mnu.Enable( False )
		
		self.m_COM4mnu = wx.MenuItem( self.m_portComMnu, wx.ID_ANY, u"COM4", wx.EmptyString, wx.ITEM_RADIO )
		self.m_portComMnu.AppendItem( self.m_COM4mnu )
		self.m_COM4mnu.Enable( False )
		
		self.m_COM5mnu = wx.MenuItem( self.m_portComMnu, wx.ID_ANY, u"COM5", wx.EmptyString, wx.ITEM_RADIO )
		self.m_portComMnu.AppendItem( self.m_COM5mnu )
		self.m_COM5mnu.Enable( False )
		
		self.m_COM6mnu = wx.MenuItem( self.m_portComMnu, wx.ID_ANY, u"COM6", wx.EmptyString, wx.ITEM_RADIO )
		self.m_portComMnu.AppendItem( self.m_COM6mnu )
		self.m_COM6mnu.Enable( False )
		
		self.m_COM7mnu = wx.MenuItem( self.m_portComMnu, wx.ID_ANY, u"COM7", wx.EmptyString, wx.ITEM_RADIO )
		self.m_portComMnu.AppendItem( self.m_COM7mnu )
		self.m_COM7mnu.Enable( False )
		
		self.m_COM8mnu = wx.MenuItem( self.m_portComMnu, wx.ID_ANY, u"COM8", wx.EmptyString, wx.ITEM_RADIO )
		self.m_portComMnu.AppendItem( self.m_COM8mnu )
		self.m_COM8mnu.Enable( False )
		
		self.m_COM9mnu = wx.MenuItem( self.m_portComMnu, wx.ID_ANY, u"COM9", wx.EmptyString, wx.ITEM_RADIO )
		self.m_portComMnu.AppendItem( self.m_COM9mnu )
		self.m_COM9mnu.Enable( False )
		
		self.m_COM10mnu = wx.MenuItem( self.m_portComMnu, wx.ID_ANY, u"COM10", wx.EmptyString, wx.ITEM_RADIO )
		self.m_portComMnu.AppendItem( self.m_COM10mnu )
		self.m_COM10mnu.Enable( False )
		
		self.m_COM11mnu = wx.MenuItem( self.m_portComMnu, wx.ID_ANY, u"COM11", wx.EmptyString, wx.ITEM_RADIO )
		self.m_portComMnu.AppendItem( self.m_COM11mnu )
		self.m_COM11mnu.Enable( False )
		
		self.m_COM12mnu = wx.MenuItem( self.m_portComMnu, wx.ID_ANY, u"COM12", wx.EmptyString, wx.ITEM_RADIO )
		self.m_portComMnu.AppendItem( self.m_COM12mnu )
		self.m_COM12mnu.Enable( False )
		
		self.m_COM13mnu = wx.MenuItem( self.m_portComMnu, wx.ID_ANY, u"COM13", wx.EmptyString, wx.ITEM_RADIO )
		self.m_portComMnu.AppendItem( self.m_COM13mnu )
		self.m_COM13mnu.Enable( False )
		
		self.m_COM14mnu = wx.MenuItem( self.m_portComMnu, wx.ID_ANY, u"COM14", wx.EmptyString, wx.ITEM_RADIO )
		self.m_portComMnu.AppendItem( self.m_COM14mnu )
		self.m_COM14mnu.Enable( False )
		
		self.m_COM15mnu = wx.MenuItem( self.m_portComMnu, wx.ID_ANY, u"COM15", wx.EmptyString, wx.ITEM_RADIO )
		self.m_portComMnu.AppendItem( self.m_COM15mnu )
		self.m_COM15mnu.Enable( False )
		
		self.m_COM16mnu = wx.MenuItem( self.m_portComMnu, wx.ID_ANY, u"COM16", wx.EmptyString, wx.ITEM_RADIO )
		self.m_portComMnu.AppendItem( self.m_COM16mnu )
		self.m_COM16mnu.Enable( False )
		
		self.m_COM17mnu = wx.MenuItem( self.m_portComMnu, wx.ID_ANY, u"COM17", wx.EmptyString, wx.ITEM_RADIO )
		self.m_portComMnu.AppendItem( self.m_COM17mnu )
		self.m_COM17mnu.Enable( False )
		
		self.m_COM18mnu = wx.MenuItem( self.m_portComMnu, wx.ID_ANY, u"COM18", wx.EmptyString, wx.ITEM_RADIO )
		self.m_portComMnu.AppendItem( self.m_COM18mnu )
		self.m_COM18mnu.Enable( False )
		
		self.m_COM19mnu = wx.MenuItem( self.m_portComMnu, wx.ID_ANY, u"COM19", wx.EmptyString, wx.ITEM_RADIO )
		self.m_portComMnu.AppendItem( self.m_COM19mnu )
		self.m_COM19mnu.Enable( False )
		
		self.m_COM20mnu = wx.MenuItem( self.m_portComMnu, wx.ID_ANY, u"COM20", wx.EmptyString, wx.ITEM_RADIO )
		self.m_portComMnu.AppendItem( self.m_COM20mnu )
		self.m_COM20mnu.Enable( False )
		
		self.m_COM21mnu = wx.MenuItem( self.m_portComMnu, wx.ID_ANY, u"COM21", wx.EmptyString, wx.ITEM_RADIO )
		self.m_portComMnu.AppendItem( self.m_COM21mnu )
		self.m_COM21mnu.Enable( False )
		
		self.m_COM22mnu = wx.MenuItem( self.m_portComMnu, wx.ID_ANY, u"COM22", wx.EmptyString, wx.ITEM_RADIO )
		self.m_portComMnu.AppendItem( self.m_COM22mnu )
		self.m_COM22mnu.Enable( False )
		
		self.m_COM23mnu = wx.MenuItem( self.m_portComMnu, wx.ID_ANY, u"COM23", wx.EmptyString, wx.ITEM_RADIO )
		self.m_portComMnu.AppendItem( self.m_COM23mnu )
		self.m_COM23mnu.Enable( False )
		
		self.m_COM24mnu = wx.MenuItem( self.m_portComMnu, wx.ID_ANY, u"COM24", wx.EmptyString, wx.ITEM_RADIO )
		self.m_portComMnu.AppendItem( self.m_COM24mnu )
		self.m_COM24mnu.Enable( False )
		
		self.m_COM25mnu = wx.MenuItem( self.m_portComMnu, wx.ID_ANY, u"COM25", wx.EmptyString, wx.ITEM_RADIO )
		self.m_portComMnu.AppendItem( self.m_COM25mnu )
		self.m_COM25mnu.Enable( False )
		
		self.m_menubar1.Append( self.m_portComMnu, u"Port COM" ) 
		
		self.m_vitesseMnu = wx.Menu()
		self.m_115200mnu = wx.MenuItem( self.m_vitesseMnu, wx.ID_ANY, u"115200 bds", u"Selectionne la vitesse 115200 bds", wx.ITEM_RADIO )
		self.m_vitesseMnu.AppendItem( self.m_115200mnu )
		
		self.m_57600mnu = wx.MenuItem( self.m_vitesseMnu, wx.ID_ANY, u"  57600 bds", u"Selectionne la vitesse 57600 bds", wx.ITEM_RADIO )
		self.m_vitesseMnu.AppendItem( self.m_57600mnu )
		
		self.m_19200mnu = wx.MenuItem( self.m_vitesseMnu, wx.ID_ANY, u"  19200 bds", u"Selectionne la vitesse 19200 bds", wx.ITEM_RADIO )
		self.m_vitesseMnu.AppendItem( self.m_19200mnu )
		
		self.m_9600mnu = wx.MenuItem( self.m_vitesseMnu, wx.ID_ANY, u"    9600 bds", u"Selectionne la vitesse 9600 bds", wx.ITEM_RADIO )
		self.m_vitesseMnu.AppendItem( self.m_9600mnu )
		
		self.m_4800mnu = wx.MenuItem( self.m_vitesseMnu, wx.ID_ANY, u"    4800 bds", u"Selectionne la vitesse 4800 bds", wx.ITEM_RADIO )
		self.m_vitesseMnu.AppendItem( self.m_4800mnu )
		
		self.m_2400mnu = wx.MenuItem( self.m_vitesseMnu, wx.ID_ANY, u"    2400 bds", u"Selectionne la vitesse 2400 bds", wx.ITEM_RADIO )
		self.m_vitesseMnu.AppendItem( self.m_2400mnu )
		
		self.m_1200mnu = wx.MenuItem( self.m_vitesseMnu, wx.ID_ANY, u"    1200 bds", u"Selectionne la vitesse 1200 bds", wx.ITEM_RADIO )
		self.m_vitesseMnu.AppendItem( self.m_1200mnu )
		
		self.m_menubar1.Append( self.m_vitesseMnu, u"Vitesse COM" ) 
		
		self.m_systemeMnu = wx.Menu()
		self.m_gestPeriphMnu = wx.MenuItem( self.m_systemeMnu, wx.ID_ANY, u"Gestionnaire de périphérique", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_systemeMnu.AppendItem( self.m_gestPeriphMnu )
		
		self.m_menubar1.Append( self.m_systemeMnu, u"Système" ) 
		
		self.SetMenuBar( self.m_menubar1 )
		
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.m_bntRun.Bind( wx.EVT_BUTTON, self.m_bntRunEvt )
		self.m_bntStop.Bind( wx.EVT_BUTTON, self.m_bntStopEvt )
		self.Bind( wx.EVT_TIMER, self.m_timer1Evt, id=wx.ID_ANY )
		self.Bind( wx.EVT_MENU, self.m_nouveauMnuEvt, id = self.m_nouveauMnu.GetId() )
		self.Bind( wx.EVT_MENU, self.m_ouvrirCdeMnuEvt, id = self.m_ouvrirCdeMnu.GetId() )
		self.Bind( wx.EVT_MENU, self.m_enregistrerCdeMnuEvt, id = self.m_enregistrerCdeMnu.GetId() )
		self.Bind( wx.EVT_MENU, self.m_enregistrerSousCdeMnuEvt, id = self.m_enregistrerSousCdeMnu.GetId() )
		self.Bind( wx.EVT_MENU, self.m_quiterMnuEvt, id = self.m_quiterMnu.GetId() )
		self.Bind( wx.EVT_MENU, self.m_COMactualiserMnuEvt, id = self.m_COMactualiserMnu.GetId() )
		self.Bind( wx.EVT_MENU, self.m_COMmanuMnuEvt, id = self.m_COMmanuMnu.GetId() )
		self.Bind( wx.EVT_MENU, self.m_COM1mnuEvt, id = self.m_COM1mnu.GetId() )
		self.Bind( wx.EVT_MENU, self.m_COM2mnuEvt, id = self.m_COM2mnu.GetId() )
		self.Bind( wx.EVT_MENU, self.m_COM3mnuEvt, id = self.m_COM3mnu.GetId() )
		self.Bind( wx.EVT_MENU, self.m_COM4mnuEvt, id = self.m_COM4mnu.GetId() )
		self.Bind( wx.EVT_MENU, self.m_COM5mnuEvt, id = self.m_COM5mnu.GetId() )
		self.Bind( wx.EVT_MENU, self.m_COM6mnuEvt, id = self.m_COM6mnu.GetId() )
		self.Bind( wx.EVT_MENU, self.m_COM7mnuEvt, id = self.m_COM7mnu.GetId() )
		self.Bind( wx.EVT_MENU, self.m_COM8mnuEvt, id = self.m_COM8mnu.GetId() )
		self.Bind( wx.EVT_MENU, self.m_COM9mnuEvt, id = self.m_COM9mnu.GetId() )
		self.Bind( wx.EVT_MENU, self.m_COM10mnuEvt, id = self.m_COM10mnu.GetId() )
		self.Bind( wx.EVT_MENU, self.m_COM11mnuEvt, id = self.m_COM11mnu.GetId() )
		self.Bind( wx.EVT_MENU, self.m_COM12mnuEvt, id = self.m_COM12mnu.GetId() )
		self.Bind( wx.EVT_MENU, self.m_COM13mnuEvt, id = self.m_COM13mnu.GetId() )
		self.Bind( wx.EVT_MENU, self.m_COM14mnuEvt, id = self.m_COM14mnu.GetId() )
		self.Bind( wx.EVT_MENU, self.m_COM15mnuEvt, id = self.m_COM15mnu.GetId() )
		self.Bind( wx.EVT_MENU, self.m_COM16mnuEvt, id = self.m_COM16mnu.GetId() )
		self.Bind( wx.EVT_MENU, self.m_COM17mnuEvt, id = self.m_COM17mnu.GetId() )
		self.Bind( wx.EVT_MENU, self.m_COM18mnuEvt, id = self.m_COM18mnu.GetId() )
		self.Bind( wx.EVT_MENU, self.m_COM19mnuEvt, id = self.m_COM19mnu.GetId() )
		self.Bind( wx.EVT_MENU, self.m_COM20mnuEvt, id = self.m_COM20mnu.GetId() )
		self.Bind( wx.EVT_MENU, self.m_COM21mnuEvt, id = self.m_COM21mnu.GetId() )
		self.Bind( wx.EVT_MENU, self.m_COM22mnuEvt, id = self.m_COM22mnu.GetId() )
		self.Bind( wx.EVT_MENU, self.m_COM23mnuEvt, id = self.m_COM23mnu.GetId() )
		self.Bind( wx.EVT_MENU, self.m_COM24mnuEvt, id = self.m_COM24mnu.GetId() )
		self.Bind( wx.EVT_MENU, self.m_COM25mnuEvt, id = self.m_COM25mnu.GetId() )
		self.Bind( wx.EVT_MENU, self.m_115200mnuEvt, id = self.m_115200mnu.GetId() )
		self.Bind( wx.EVT_MENU, self.m_57600mnuEvt, id = self.m_57600mnu.GetId() )
		self.Bind( wx.EVT_MENU, self.m_19200mnuEvt, id = self.m_19200mnu.GetId() )
		self.Bind( wx.EVT_MENU, self.m_9600mnuEvt, id = self.m_9600mnu.GetId() )
		self.Bind( wx.EVT_MENU, self.m_4800mnuEvt, id = self.m_4800mnu.GetId() )
		self.Bind( wx.EVT_MENU, self.m_2400mnuEvt, id = self.m_2400mnu.GetId() )
		self.Bind( wx.EVT_MENU, self.m_1200mnuEvt, id = self.m_1200mnu.GetId() )
		self.Bind( wx.EVT_MENU, self.m_gestPeriphMnuEvt, id = self.m_gestPeriphMnu.GetId() )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def m_bntRunEvt( self, event ):
		event.Skip()
	
	def m_bntStopEvt( self, event ):
		event.Skip()
	
	def m_timer1Evt( self, event ):
		event.Skip()
	
	def m_nouveauMnuEvt( self, event ):
		event.Skip()
	
	def m_ouvrirCdeMnuEvt( self, event ):
		event.Skip()
	
	def m_enregistrerCdeMnuEvt( self, event ):
		event.Skip()
	
	def m_enregistrerSousCdeMnuEvt( self, event ):
		event.Skip()
	
	def m_quiterMnuEvt( self, event ):
		event.Skip()
	
	def m_COMactualiserMnuEvt( self, event ):
		event.Skip()
	
	def m_COMmanuMnuEvt( self, event ):
		event.Skip()
	
	def m_COM1mnuEvt( self, event ):
		event.Skip()
	
	def m_COM2mnuEvt( self, event ):
		event.Skip()
	
	def m_COM3mnuEvt( self, event ):
		event.Skip()
	
	def m_COM4mnuEvt( self, event ):
		event.Skip()
	
	def m_COM5mnuEvt( self, event ):
		event.Skip()
	
	def m_COM6mnuEvt( self, event ):
		event.Skip()
	
	def m_COM7mnuEvt( self, event ):
		event.Skip()
	
	def m_COM8mnuEvt( self, event ):
		event.Skip()
	
	def m_COM9mnuEvt( self, event ):
		event.Skip()
	
	def m_COM10mnuEvt( self, event ):
		event.Skip()
	
	def m_COM11mnuEvt( self, event ):
		event.Skip()
	
	def m_COM12mnuEvt( self, event ):
		event.Skip()
	
	def m_COM13mnuEvt( self, event ):
		event.Skip()
	
	def m_COM14mnuEvt( self, event ):
		event.Skip()
	
	def m_COM15mnuEvt( self, event ):
		event.Skip()
	
	def m_COM16mnuEvt( self, event ):
		event.Skip()
	
	def m_COM17mnuEvt( self, event ):
		event.Skip()
	
	def m_COM18mnuEvt( self, event ):
		event.Skip()
	
	def m_COM19mnuEvt( self, event ):
		event.Skip()
	
	def m_COM20mnuEvt( self, event ):
		event.Skip()
	
	def m_COM21mnuEvt( self, event ):
		event.Skip()
	
	def m_COM22mnuEvt( self, event ):
		event.Skip()
	
	def m_COM23mnuEvt( self, event ):
		event.Skip()
	
	def m_COM24mnuEvt( self, event ):
		event.Skip()
	
	def m_COM25mnuEvt( self, event ):
		event.Skip()
	
	def m_115200mnuEvt( self, event ):
		event.Skip()
	
	def m_57600mnuEvt( self, event ):
		event.Skip()
	
	def m_19200mnuEvt( self, event ):
		event.Skip()
	
	def m_9600mnuEvt( self, event ):
		event.Skip()
	
	def m_4800mnuEvt( self, event ):
		event.Skip()
	
	def m_2400mnuEvt( self, event ):
		event.Skip()
	
	def m_1200mnuEvt( self, event ):
		event.Skip()
	
	def m_gestPeriphMnuEvt( self, event ):
		event.Skip()
	

###########################################################################
## Class saisieComDlgClass
###########################################################################

class saisieComDlgClass ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Saisie manuelle nom du port série:", pos = wx.DefaultPosition, size = wx.Size( 376,114 ), style = wx.DEFAULT_DIALOG_STYLE|wx.STAY_ON_TOP )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		gSizer3 = wx.GridSizer( 2, 2, 0, 0 )
		
		self.m_saisieCOMtxt = wx.StaticText( self, wx.ID_ANY, u"Nom du port série : \n   exemple: COM1", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_saisieCOMtxt.Wrap( -1 )
		gSizer3.Add( self.m_saisieCOMtxt, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.COMmanuTextCtrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer3.Add( self.COMmanuTextCtrl, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		gSizer3.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		m_okCancelMnu = wx.StdDialogButtonSizer()
		self.m_okCancelMnuOK = wx.Button( self, wx.ID_OK )
		m_okCancelMnu.AddButton( self.m_okCancelMnuOK )
		self.m_okCancelMnuCancel = wx.Button( self, wx.ID_CANCEL )
		m_okCancelMnu.AddButton( self.m_okCancelMnuCancel )
		m_okCancelMnu.Realize();
		
		gSizer3.Add( m_okCancelMnu, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
		self.SetSizer( gSizer3 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.m_okCancelMnuCancel.Bind( wx.EVT_BUTTON, self.m_cancelMnuEvt )
		self.m_okCancelMnuOK.Bind( wx.EVT_BUTTON, self.m_okMnuEvt )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def m_cancelMnuEvt( self, event ):
		event.Skip()
	
	def m_okMnuEvt( self, event ):
		event.Skip()
	

