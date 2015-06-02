README
======

Principe:	
--------
	Le but est de lire des logs depuis le port série et	de les enregistrer:
	* dans un fichier texte.
	* dans une base de données MySQL.
	
	L'enregistreur est écrit en Python.
	L'interface graphique (GUI)	utilise les librairies wxWidgets via wxPython3
	
	Une visionneuse en PHP permet de voir, filter, colorier les logs
	dans une page web.
	

Dependance:
----------
	La procedure d'installation/deployement n'est pas encore developpee.
	
	Le fichier principale Python est `Serial_SQL_Logger_MAIN.py`
	
	Interface graphique `Serial_SQL_Logger_GUI_GUI.py`
	GUI developpee avec `wxFormBuilder v3.5.0 beta (unicode)`
	Executable windows, fonctionne aussi sous wine ubuntu 15.04 Gnome3.14

Installation Windows7:
---------------------
	Installation cote Python:
	------------------------
	* python-2.7.6.amd64.msi
	* pyserial-2.7
	* MySQL-python-1.2.5
	* wxPython3.0-win64-3.0.0.0-py27.exe
	* wxFormBuilder_v3.4.2-beta.exe (Editeur GUI)
	
	Installation cote MySQL PHP
	---------------------------
	Developpement realise avec WAMP 2.4:
	* Apache 2.4.4
	* PHP    5.4.12
	* MySQL  5.6.12
	
	Base de donnees MySQL:
	---------------------
	* Importer `serial_sql_logger_import_2015-04-18.sql` dans dossier MySQL appli.

Installation Linux Debian/Ubuntu (Rasp 2 / Cubietruck):
--------------------------------
	Installation cote Python:
	------------------------
	* python-2.7 32bits
	* python-wxgtk     2.8.12.1-12
	* python-wxtools   2.8-12.1-12
	* python-wxversion 2.8-12.1-12
	* wx-common        2.8-12.1-12
	* wx-2.8-examples  2.8-12.1-12
	* python-mysqldb   1.2.3-2
	* python-serial    2.5-2.1
	
Notes:
-----
	Le point de depart de cette appli est un fork de `Serie_vers_Afficheur_Uno_MAIN.py`.
	Le port série USB Arduino utilisé normalement pour le monitoring de	l'IDE Arduino,
	est exploité par Python.
	Cette appli permet d'envoyer des instructions vers une carte Arduino via ce port série. 

