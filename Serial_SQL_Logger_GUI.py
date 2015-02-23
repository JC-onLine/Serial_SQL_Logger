# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun  5 2014)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.combo

###########################################################################
## Class FenetrePrincipaleClass
###########################################################################

class FenetrePrincipaleClass ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Serial SQL Logger", pos = wx.DefaultPosition, size = wx.Size( 1020,710 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.MAXIMIZE_BOX|wx.MINIMIZE_BOX|wx.SYSTEM_MENU|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		self.SetForegroundColour( wx.Colour( 170, 170, 170 ) )
		self.SetBackgroundColour( wx.Colour( 100, 100, 100 ) )
		
		self.m_timer1 = wx.Timer()
		self.m_timer1.SetOwner( self, wx.ID_ANY )
		self.m_timer1.Start( 100 )
		
		self.m_statusBar1 = self.CreateStatusBar( 2, wx.ST_SIZEGRIP, wx.ID_ANY )
		self.m_statusBar1.SetForegroundColour( wx.Colour( 207, 207, 207 ) )
		self.m_statusBar1.SetBackgroundColour( wx.Colour( 100, 100, 100 ) )
		
		self.m_menubar1 = wx.MenuBar( 0 )
		self.m_menubar1.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 90, False, wx.EmptyString ) )
		self.m_menubar1.SetForegroundColour( wx.Colour( 154, 154, 154 ) )
		self.m_menubar1.SetBackgroundColour( wx.Colour( 98, 98, 98 ) )
		
		self.m_fichierMnu = wx.Menu()
		self.m_LogFileDeco = wx.MenuItem( self.m_fichierMnu, wx.ID_ANY, u"Fichier log :", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_fichierMnu.AppendItem( self.m_LogFileDeco )
		self.m_LogFileDeco.Enable( False )
		
		self.m_LogNewMnu = wx.MenuItem( self.m_fichierMnu, wx.ID_ANY, u"  Nouveau log"+ u"\t" + u"CTRL+N", u"Nouveau fichier log", wx.ITEM_NORMAL )
		self.m_LogNewMnu.SetBitmap( wx.Bitmap( u"Icons/Log/document-new.png", wx.BITMAP_TYPE_ANY ) )
		self.m_fichierMnu.AppendItem( self.m_LogNewMnu )
		
		self.m_LogOpenMnu = wx.MenuItem( self.m_fichierMnu, wx.ID_ANY, u"  Ouvrir log"+ u"\t" + u"CTRL+O", u"Ouvrir un fichier log", wx.ITEM_NORMAL )
		self.m_LogOpenMnu.SetBitmap( wx.Bitmap( u"Icons/Log/document-open.png", wx.BITMAP_TYPE_ANY ) )
		self.m_fichierMnu.AppendItem( self.m_LogOpenMnu )
		
		self.m_LogSaveMnu = wx.MenuItem( self.m_fichierMnu, wx.ID_ANY, u"  Enregistrer log"+ u"\t" + u"CTRL+S", u"Enregistrer un fichier log", wx.ITEM_NORMAL )
		self.m_LogSaveMnu.SetBitmap( wx.Bitmap( u"Icons/Log/document-save.png", wx.BITMAP_TYPE_ANY ) )
		self.m_fichierMnu.AppendItem( self.m_LogSaveMnu )
		
		self.m_LogSaveAsMnu = wx.MenuItem( self.m_fichierMnu, wx.ID_ANY, u"  Enregistrer  log sous..."+ u"\t" + u"CTRL+SHIFT+S", u"Enregistrer un fichier log sous...", wx.ITEM_NORMAL )
		self.m_LogSaveAsMnu.SetBitmap( wx.Bitmap( u"Icons/Log/document-save-as.png", wx.BITMAP_TYPE_ANY ) )
		self.m_fichierMnu.AppendItem( self.m_LogSaveAsMnu )
		
		self.m_fichierMnu.AppendSeparator()
		
		self.m_ProfileFileDeco = wx.MenuItem( self.m_fichierMnu, wx.ID_ANY, u"Fichier profile réglages :", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_fichierMnu.AppendItem( self.m_ProfileFileDeco )
		self.m_ProfileFileDeco.Enable( False )
		
		self.m_ProfileNewMnu = wx.MenuItem( self.m_fichierMnu, wx.ID_ANY, u"  Nouveau profile"+ u"\t" + u"CTRL+ALT+N", u"Nouveau fichier profile", wx.ITEM_NORMAL )
		self.m_ProfileNewMnu.SetBitmap( wx.Bitmap( u"Icons/Profile/document-new.png", wx.BITMAP_TYPE_ANY ) )
		self.m_fichierMnu.AppendItem( self.m_ProfileNewMnu )
		
		self.m_ProfileOpenMnu = wx.MenuItem( self.m_fichierMnu, wx.ID_ANY, u"  Ouvrir profile"+ u"\t" + u"CTRL+ALT+O", u"Ouvrir un fichier profile", wx.ITEM_NORMAL )
		self.m_ProfileOpenMnu.SetBitmap( wx.Bitmap( u"Icons/Profile/document-open.png", wx.BITMAP_TYPE_ANY ) )
		self.m_fichierMnu.AppendItem( self.m_ProfileOpenMnu )
		
		self.m_ProfileSaveMnu = wx.MenuItem( self.m_fichierMnu, wx.ID_ANY, u"  Enregistrer profile"+ u"\t" + u"CTRL+ALT+S", u"Enregistrer un fichier profile", wx.ITEM_NORMAL )
		self.m_ProfileSaveMnu.SetBitmap( wx.Bitmap( u"Icons/Profile/document-save.png", wx.BITMAP_TYPE_ANY ) )
		self.m_fichierMnu.AppendItem( self.m_ProfileSaveMnu )
		
		self.m_ProfileSaveAsMnu = wx.MenuItem( self.m_fichierMnu, wx.ID_ANY, u"  Enregistrer profile sous..."+ u"\t" + u"CTRL+ALT+SHIFT+S", u"Enregistrer un fichier profile sous...", wx.ITEM_NORMAL )
		self.m_ProfileSaveAsMnu.SetBitmap( wx.Bitmap( u"Icons/Profile/document-save-as.png", wx.BITMAP_TYPE_ANY ) )
		self.m_fichierMnu.AppendItem( self.m_ProfileSaveAsMnu )
		
		self.m_fichierMnu.AppendSeparator()
		
		self.m_quiterMnu = wx.MenuItem( self.m_fichierMnu, wx.ID_ANY, u"Quiter"+ u"\t" + u"CTRL+Q", u"Quiter l'application", wx.ITEM_NORMAL )
		self.m_quiterMnu.SetBitmap( wx.Bitmap( u"Icons/System/system-shutdown.png", wx.BITMAP_TYPE_ANY ) )
		self.m_fichierMnu.AppendItem( self.m_quiterMnu )
		
		self.m_menubar1.Append( self.m_fichierMnu, u"Fichier" ) 
		
		self.m_portComMnu = wx.Menu()
		self.m_COMactualiserMnu = wx.MenuItem( self.m_portComMnu, wx.ID_ANY, u"<Actualiser>"+ u"\t" + u"CTRL+F", u"Recherche Port COM dispo.", wx.ITEM_NORMAL )
		self.m_portComMnu.AppendItem( self.m_COMactualiserMnu )
		
		self.m_COMmanuMnu = wx.MenuItem( self.m_portComMnu, wx.ID_ANY, u"<Sélection Manuelle>"+ u"\t" + u"CTRL+M", u"Saisir au clavier le nom du port série", wx.ITEM_NORMAL )
		self.m_portComMnu.AppendItem( self.m_COMmanuMnu )
		
		self.m_COMnonSelect = wx.MenuItem( self.m_portComMnu, wx.ID_ANY, u"Non selectionné", wx.EmptyString, wx.ITEM_RADIO )
		self.m_portComMnu.AppendItem( self.m_COMnonSelect )
		
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
		self.m_gestPeriphMnu.SetBitmap( wx.Bitmap( u"Icons/System/applications-system.png", wx.BITMAP_TYPE_ANY ) )
		self.m_systemeMnu.AppendItem( self.m_gestPeriphMnu )
		
		self.m_menubar1.Append( self.m_systemeMnu, u"Système" ) 
		
		self.m_serveur = wx.Menu()
		self.m_menubar1.Append( self.m_serveur, u"Serveur" ) 
		
		self.SetMenuBar( self.m_menubar1 )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.logTextCtrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 1000,395 ), wx.TE_MULTILINE )
		self.logTextCtrl.SetForegroundColour( wx.Colour( 207, 207, 207 ) )
		self.logTextCtrl.SetBackgroundColour( wx.Colour( 40, 40, 40 ) )
		
		bSizer1.Add( self.logTextCtrl, 0, wx.ALL, 5 )
		
		bSizer31 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.spacer_10x60 = wx.StaticBitmap( self, wx.ID_ANY, wx.Bitmap( u"Icons/spacer/spacer_10x60.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer31.Add( self.spacer_10x60, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		bSizer5 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_separateurTxt = wx.StaticText( self, wx.ID_ANY, u"Séparateur", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_separateurTxt.Wrap( -1 )
		bSizer5.Add( self.m_separateurTxt, 0, wx.ALL, 5 )
		
		m_separateurCbxChoices = []
		self.m_separateurCbx = wx.ComboBox( self, wx.ID_ANY, u"|", wx.DefaultPosition, wx.Size( 60,-1 ), m_separateurCbxChoices, 0 )
		self.m_separateurCbx.Enable( False )
		
		bSizer5.Add( self.m_separateurCbx, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer31.Add( bSizer5, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.spacer_10x20_01 = wx.StaticBitmap( self, wx.ID_ANY, wx.Bitmap( u"Icons/spacer/spacer_10x20.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer31.Add( self.spacer_10x20_01, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_ExtractHorodateChk = wx.CheckBox( self, wx.ID_ANY, u"Horodatage\ninclus dans logs", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer31.Add( self.m_ExtractHorodateChk, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.spacer_10x20_02 = wx.StaticBitmap( self, wx.ID_ANY, wx.Bitmap( u"Icons/spacer/spacer_10x20.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer31.Add( self.spacer_10x20_02, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_ExtractCategorieChk = wx.CheckBox( self, wx.ID_ANY, u"Catégorie\ninclus dans logs", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		bSizer31.Add( self.m_ExtractCategorieChk, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.spacer_10x20_03 = wx.StaticBitmap( self, wx.ID_ANY, wx.Bitmap( u"Icons/spacer/spacer_10x20.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer31.Add( self.spacer_10x20_03, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		bSizer6 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_CategorieLbl = wx.StaticText( self, wx.ID_ANY, u"Ajout catégorie", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_CategorieLbl.Wrap( -1 )
		bSizer6.Add( self.m_CategorieLbl, 0, wx.ALL, 5 )
		
		self.m_CategorieTxt = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_CategorieTxt.SetBackgroundColour( wx.Colour( 130, 130, 130 ) )
		
		bSizer6.Add( self.m_CategorieTxt, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		
		bSizer31.Add( bSizer6, 0, wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.spacer_10x20_04 = wx.StaticBitmap( self, wx.ID_ANY, wx.Bitmap( u"Icons/spacer/spacer_10x20.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer31.Add( self.spacer_10x20_04, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_ExtractNivDetailChk = wx.CheckBox( self, wx.ID_ANY, u"Niveau détail\ninclus dans logs", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		bSizer31.Add( self.m_ExtractNivDetailChk, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		bSizer7 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_ExtractNivDetailLbl = wx.StaticText( self, wx.ID_ANY, u"Ajout num\ndétail", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_ExtractNivDetailLbl.Wrap( -1 )
		bSizer7.Add( self.m_ExtractNivDetailLbl, 0, wx.ALL, 5 )
		
		self.m_ExtractNivDetailNum = wx.SpinCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 50,-1 ), wx.SP_ARROW_KEYS, 0, 10, 1 )
		bSizer7.Add( self.m_ExtractNivDetailNum, 0, wx.ALL, 5 )
		
		
		bSizer31.Add( bSizer7, 0, wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_compteurTxt = wx.StaticText( self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_compteurTxt.Wrap( -1 )
		self.m_compteurTxt.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 90, False, wx.EmptyString ) )
		self.m_compteurTxt.Hide()
		self.m_compteurTxt.SetToolTipString( u"Compteur de test" )
		
		bSizer31.Add( self.m_compteurTxt, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.LEFT, 5 )
		
		
		bSizer1.Add( bSizer31, 0, wx.ALL|wx.EXPAND, 5 )
		
		bSizer3 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer3.SetMinSize( wx.Size( -1,32 ) ) 
		self.m_statusActionTextStat = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 300,-1 ), 0|wx.FULL_REPAINT_ON_RESIZE|wx.SUNKEN_BORDER )
		self.m_statusActionTextStat.Wrap( -1 )
		self.m_statusActionTextStat.SetBackgroundColour( wx.Colour( 40, 40, 40 ) )
		
		bSizer3.Add( self.m_statusActionTextStat, 0, wx.RIGHT|wx.LEFT|wx.ALIGN_BOTTOM, 5 )
		
		self.m_statusComTextStat = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 150,-1 ), 0|wx.FULL_REPAINT_ON_RESIZE|wx.SUNKEN_BORDER )
		self.m_statusComTextStat.Wrap( -1 )
		self.m_statusComTextStat.SetBackgroundColour( wx.Colour( 40, 40, 40 ) )
		
		bSizer3.Add( self.m_statusComTextStat, 0, wx.RIGHT|wx.LEFT|wx.ALIGN_BOTTOM, 5 )
		
		self.m_statusVitesseTextStat = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 150,-1 ), 0|wx.FULL_REPAINT_ON_RESIZE|wx.SUNKEN_BORDER )
		self.m_statusVitesseTextStat.Wrap( -1 )
		self.m_statusVitesseTextStat.SetBackgroundColour( wx.Colour( 40, 40, 40 ) )
		
		bSizer3.Add( self.m_statusVitesseTextStat, 0, wx.RIGHT|wx.LEFT|wx.ALIGN_BOTTOM, 5 )
		
		
		bSizer3.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.m_btn_mysqlInsert = wx.Button( self, wx.ID_ANY, u"MySQL INSERT", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer3.Add( self.m_btn_mysqlInsert, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_OsTxt = wx.StaticText( self, wx.ID_ANY, u"OS :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_OsTxt.Wrap( -1 )
		bSizer3.Add( self.m_OsTxt, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.LEFT, 5 )
		
		self.m_bmpOS = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer3.Add( self.m_bmpOS, 0, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.RIGHT|wx.LEFT, 5 )
		
		self.m_OSdetailsTxt = wx.StaticText( self, wx.ID_ANY, u"details", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_OSdetailsTxt.Wrap( -1 )
		bSizer3.Add( self.m_OSdetailsTxt, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.LEFT, 5 )
		
		self.m_ArchBitsTxt = wx.StaticText( self, wx.ID_ANY, u"xx bits", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_ArchBitsTxt.Wrap( -1 )
		bSizer3.Add( self.m_ArchBitsTxt, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.LEFT, 5 )
		
		
		bSizer1.Add( bSizer3, 0, wx.EXPAND, 5 )
		
		bSizer4 = wx.BoxSizer( wx.VERTICAL )
		
		self.logAppliTextCtrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,100 ), wx.TE_MULTILINE )
		self.logAppliTextCtrl.SetForegroundColour( wx.Colour( 207, 207, 207 ) )
		self.logAppliTextCtrl.SetBackgroundColour( wx.Colour( 40, 40, 40 ) )
		self.logAppliTextCtrl.SetMinSize( wx.Size( -1,80 ) )
		self.logAppliTextCtrl.SetMaxSize( wx.Size( -1,80 ) )
		
		bSizer4.Add( self.logAppliTextCtrl, 0, wx.EXPAND|wx.ALL, 5 )
		
		
		bSizer1.Add( bSizer4, 0, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		self.m_toolBar1 = self.CreateToolBar( wx.TB_FLAT|wx.TB_HORIZONTAL|wx.TB_TEXT, wx.ID_ANY ) 
		self.m_toolBar1.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 90, False, wx.EmptyString ) )
		self.m_toolBar1.SetForegroundColour( wx.Colour( 180, 180, 180 ) )
		self.m_toolBar1.SetBackgroundColour( wx.Colour( 230, 230, 230 ) )
		
		self.m_findPortTool = self.m_toolBar1.AddLabelTool( wx.ID_ANY, u"Recherche Port COM", wx.Bitmap( u"Icons/ToolBar/Find.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, u"Rechercher les ports de communication", u"Rechercher les ports de communication", None ) 
		
		self.m_COMdispoTxt = wx.StaticText( self.m_toolBar1, wx.ID_ANY, u"  Port COM dispo:  ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_COMdispoTxt.Wrap( -1 )
		self.m_COMdispoTxt.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		
		self.m_toolBar1.AddControl( self.m_COMdispoTxt )
		self.m_portComCbx = wx.combo.BitmapComboBox( self.m_toolBar1, wx.ID_ANY, wx.EmptyString, wx.Point( -1,-1 ), wx.Size( -1,-1 ), "", 0 ) 
		self.m_portComCbx.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		self.m_portComCbx.SetBackgroundColour( wx.Colour( 230, 230, 230 ) )
		self.m_portComCbx.SetToolTipString( u"Liste des ports de communication disponible" )
		self.m_portComCbx.SetHelpText( u"Cliquer sur <Recherche Port COM> puis choisir dans la liste" )
		
		self.m_toolBar1.AddControl( self.m_portComCbx )
		self.m_bitmap6 = wx.StaticBitmap( self.m_toolBar1, wx.ID_ANY, wx.Bitmap( u"Icons/spacer/spacer_10x20.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_toolBar1.AddControl( self.m_bitmap6 )
		self.m_toolBar1.AddSeparator()
		
		self.m_RunStopTool = self.m_toolBar1.AddLabelTool( wx.ID_ANY, u"RUN/STOP", wx.Bitmap( u"Icons/ToolBar/Oxygen/media-playback-start.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.m_bitmap4 = wx.StaticBitmap( self.m_toolBar1, wx.ID_ANY, wx.Bitmap( u"Icons/spacer/spacer_10x20.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_toolBar1.AddControl( self.m_bitmap4 )
		self.m_bmpRunStop = wx.StaticBitmap( self.m_toolBar1, wx.ID_ANY, wx.Bitmap( u"Icons/LED/LedSTOP.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		self.m_toolBar1.AddControl( self.m_bmpRunStop )
		self.m_bitmap5 = wx.StaticBitmap( self.m_toolBar1, wx.ID_ANY, wx.Bitmap( u"Icons/spacer/spacer_10x20.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_toolBar1.AddControl( self.m_bitmap5 )
		self.m_bmpCirculaire = wx.StaticBitmap( self.m_toolBar1, wx.ID_ANY, wx.Bitmap( u"Icons/Loader/loader_32x32_01.png", wx.BITMAP_TYPE_ANY ), wx.Point( -1,20 ), wx.Size( -1,-1 ), 0 )
		self.m_toolBar1.AddControl( self.m_bmpCirculaire )
		self.m_bitmap7 = wx.StaticBitmap( self.m_toolBar1, wx.ID_ANY, wx.Bitmap( u"Icons/spacer/spacer_10x20.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_toolBar1.AddControl( self.m_bitmap7 )
		self.m_toolBar1.AddSeparator()
		
		self.m_dataTool = self.m_toolBar1.AddLabelTool( wx.ID_ANY, u"SQL", wx.Bitmap( u"Icons/ToolBar/data-disable_32x32.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.m_bitmap41 = wx.StaticBitmap( self.m_toolBar1, wx.ID_ANY, wx.Bitmap( u"Icons/spacer/spacer_10x20.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_toolBar1.AddControl( self.m_bitmap41 )
		m_tableArchiveCbxChoices = []
		self.m_tableArchiveCbx = wx.ComboBox( self.m_toolBar1, wx.ID_ANY, u"Hacklab", wx.DefaultPosition, wx.DefaultSize, m_tableArchiveCbxChoices, 0 )
		self.m_toolBar1.AddControl( self.m_tableArchiveCbx )
		self.m_bitmap8 = wx.StaticBitmap( self.m_toolBar1, wx.ID_ANY, wx.Bitmap( u"Icons/spacer/spacer_200x20.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_bitmap8.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		
		self.m_toolBar1.AddControl( self.m_bitmap8 )
		self.m_bitmap81 = wx.StaticBitmap( self.m_toolBar1, wx.ID_ANY, wx.Bitmap( u"Icons/spacer/spacer_50x20.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_bitmap81.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		
		self.m_toolBar1.AddControl( self.m_bitmap81 )
		self.m_toolQuiter = self.m_toolBar1.AddLabelTool( wx.ID_ANY, u"Quiter", wx.Bitmap( u"Icons/ToolBar/system-shutdown.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, u"Quiter l'application", wx.EmptyString, None ) 
		
		self.m_toolBar1.Realize() 
		
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_TIMER, self.m_timer1Evt, id=wx.ID_ANY )
		self.Bind( wx.EVT_MENU, self.m_LogNewMnuEvt, id = self.m_LogNewMnu.GetId() )
		self.Bind( wx.EVT_MENU, self.m_LogOpenMnuEvt, id = self.m_LogOpenMnu.GetId() )
		self.Bind( wx.EVT_MENU, self.m_LogSaveMnuEvt, id = self.m_LogSaveMnu.GetId() )
		self.Bind( wx.EVT_MENU, self.m_LogSaveAsMnuEvt, id = self.m_LogSaveAsMnu.GetId() )
		self.Bind( wx.EVT_MENU, self.m_ProfileNewMnuEvt, id = self.m_ProfileNewMnu.GetId() )
		self.Bind( wx.EVT_MENU, self.m_ProfileOpenMnuEvt, id = self.m_ProfileOpenMnu.GetId() )
		self.Bind( wx.EVT_MENU, self.m_ProfileSaveMnuEvt, id = self.m_ProfileSaveMnu.GetId() )
		self.Bind( wx.EVT_MENU, self.m_ProfileSaveAsMnuEvt, id = self.m_ProfileSaveAsMnu.GetId() )
		self.Bind( wx.EVT_MENU, self.m_quiterMnuEvt, id = self.m_quiterMnu.GetId() )
		self.Bind( wx.EVT_MENU, self.m_COMactualiserMnuEvt, id = self.m_COMactualiserMnu.GetId() )
		self.Bind( wx.EVT_MENU, self.m_COMmanuMnuEvt, id = self.m_COMmanuMnu.GetId() )
		self.Bind( wx.EVT_MENU, self.m_COMnonSelectEvt, id = self.m_COMnonSelect.GetId() )
		self.Bind( wx.EVT_MENU, self.m_115200mnuEvt, id = self.m_115200mnu.GetId() )
		self.Bind( wx.EVT_MENU, self.m_57600mnuEvt, id = self.m_57600mnu.GetId() )
		self.Bind( wx.EVT_MENU, self.m_19200mnuEvt, id = self.m_19200mnu.GetId() )
		self.Bind( wx.EVT_MENU, self.m_9600mnuEvt, id = self.m_9600mnu.GetId() )
		self.Bind( wx.EVT_MENU, self.m_4800mnuEvt, id = self.m_4800mnu.GetId() )
		self.Bind( wx.EVT_MENU, self.m_2400mnuEvt, id = self.m_2400mnu.GetId() )
		self.Bind( wx.EVT_MENU, self.m_1200mnuEvt, id = self.m_1200mnu.GetId() )
		self.Bind( wx.EVT_MENU, self.m_gestPeriphMnuEvt, id = self.m_gestPeriphMnu.GetId() )
		self.m_separateurCbx.Bind( wx.EVT_COMBOBOX, self.m_separateurCbxEvt )
		self.m_separateurCbx.Bind( wx.EVT_TEXT, self.m_separateurCbxOnText )
		self.m_separateurCbx.Bind( wx.EVT_TEXT_ENTER, self.m_separateurCbxOnTextEnter )
		self.m_ExtractHorodateChk.Bind( wx.EVT_CHECKBOX, self.m_ExtractHorodateChkEvt )
		self.m_ExtractCategorieChk.Bind( wx.EVT_CHECKBOX, self.m_ExtractCategorieChkEvt )
		self.m_CategorieTxt.Bind( wx.EVT_TEXT, self.m_CategorieTxtEvt )
		self.m_CategorieTxt.Bind( wx.EVT_TEXT_ENTER, self.m_CategorieTxtTextEnter )
		self.m_ExtractNivDetailChk.Bind( wx.EVT_CHECKBOX, self.m_ExtractNivDetailChkEvt )
		self.m_ExtractNivDetailNum.Bind( wx.EVT_SPINCTRL, self.m_ExtractNivDetailNumEvt )
		self.m_ExtractNivDetailNum.Bind( wx.EVT_TEXT, self.m_ExtractNivDetailNumEvtTxt )
		self.m_ExtractNivDetailNum.Bind( wx.EVT_TEXT_ENTER, self.m_ExtractNivDetailNumEvtEnter )
		self.m_btn_mysqlInsert.Bind( wx.EVT_BUTTON, self.m_btn_mysqlInsertEvt )
		self.Bind( wx.EVT_TOOL, self.m_findPortToolEvt, id = self.m_findPortTool.GetId() )
		self.m_portComCbx.Bind( wx.EVT_COMBOBOX, self.m_portComCbxEvt )
		self.m_portComCbx.Bind( wx.EVT_TEXT, self.m_portComCbxEvtOnText )
		self.m_portComCbx.Bind( wx.EVT_TEXT_ENTER, self.m_portComCbxEvtOnTextEnter )
		self.Bind( wx.EVT_TOOL, self.m_RunStopToolEvt, id = self.m_RunStopTool.GetId() )
		self.Bind( wx.EVT_TOOL, self.m_dataToolEvt, id = self.m_dataTool.GetId() )
		self.Bind( wx.EVT_TOOL, self.m_toolQuiterEvt, id = self.m_toolQuiter.GetId() )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def m_timer1Evt( self, event ):
		event.Skip()
	
	def m_LogNewMnuEvt( self, event ):
		event.Skip()
	
	def m_LogOpenMnuEvt( self, event ):
		event.Skip()
	
	def m_LogSaveMnuEvt( self, event ):
		event.Skip()
	
	def m_LogSaveAsMnuEvt( self, event ):
		event.Skip()
	
	def m_ProfileNewMnuEvt( self, event ):
		event.Skip()
	
	def m_ProfileOpenMnuEvt( self, event ):
		event.Skip()
	
	def m_ProfileSaveMnuEvt( self, event ):
		event.Skip()
	
	def m_ProfileSaveAsMnuEvt( self, event ):
		event.Skip()
	
	def m_quiterMnuEvt( self, event ):
		event.Skip()
	
	def m_COMactualiserMnuEvt( self, event ):
		event.Skip()
	
	def m_COMmanuMnuEvt( self, event ):
		event.Skip()
	
	def m_COMnonSelectEvt( self, event ):
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
	
	def m_separateurCbxEvt( self, event ):
		event.Skip()
	
	def m_separateurCbxOnText( self, event ):
		event.Skip()
	
	def m_separateurCbxOnTextEnter( self, event ):
		event.Skip()
	
	def m_ExtractHorodateChkEvt( self, event ):
		event.Skip()
	
	def m_ExtractCategorieChkEvt( self, event ):
		event.Skip()
	
	def m_CategorieTxtEvt( self, event ):
		event.Skip()
	
	def m_CategorieTxtTextEnter( self, event ):
		event.Skip()
	
	def m_ExtractNivDetailChkEvt( self, event ):
		event.Skip()
	
	def m_ExtractNivDetailNumEvt( self, event ):
		event.Skip()
	
	def m_ExtractNivDetailNumEvtTxt( self, event ):
		event.Skip()
	
	def m_ExtractNivDetailNumEvtEnter( self, event ):
		event.Skip()
	
	def m_btn_mysqlInsertEvt( self, event ):
		event.Skip()
	
	def m_findPortToolEvt( self, event ):
		event.Skip()
	
	def m_portComCbxEvt( self, event ):
		event.Skip()
	
	def m_portComCbxEvtOnText( self, event ):
		event.Skip()
	
	def m_portComCbxEvtOnTextEnter( self, event ):
		event.Skip()
	
	def m_RunStopToolEvt( self, event ):
		event.Skip()
	
	def m_dataToolEvt( self, event ):
		event.Skip()
	
	def m_toolQuiterEvt( self, event ):
		event.Skip()
	

