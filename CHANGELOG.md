CHANGELOG
=========

### 2015-05-06
  * Py: FindCOM(): Séparation scan ports séries en fonction OS: Linux/Win
  * Py: Suppresion AddMemnuPortCOM(COMname) obsolète
  * Py: Ajout gestion événement OnSerialRead pour rafraichir wxTextCtrl

### 2015-04-16 [commit]
  * PHP: La gestion profile des mot clé est opérationnelle

### 2015-04-12 
  * SQL: Suppression PRIMARY KEY sur horodatage

### 2015-04-08
  * La gestion profile des mot clé est opérationnelle

### 2015-04-04
  * Remplacement $_GET par $_POST
  * KeywordColor: Ajout paramètres profile via $_POST

### 2015-04-01
  * PHP: Dashboard.php: section coloration par mot clés

### 2015-03-23
  * Suppression 'echo' pour afficher html5
  * Ajout lecture/ecriture base SQL keyword color

### 2015-03-18
  * PHP/JS: Dashboard.php: section column size ajout slider x15

### 2015-03-17
  * PHP: Dashboard.php: section column size

### 2015-03-16
  * PHP: Dashboard.php: gestion menu color/column

### 2015-03-15
  * PHP: Création page Dashboard.php: navbar nav section keyword color

### 2015-02-25 [commit]
  * Ajout table archive dispo dans liste ComboBox avec actualisation	
  * Ajout séléction par défaut séparateur '|' si coche 'Horodadage..'
  * Ajout logs checkBox extraction pour SQL

### 2015-02-24 [commit]
  * GIT: Utilisation de Ungit pour le versioning
  * GUI: Ajout menu encodage Entrée série/Sortie SQL

### 2015-02-23
  * PHP: Ajout css 'active' dans selection en cours menu bootstrap

### 2015-02-18
  * PHP: Ajout du marqueur de ligne

### 2015-02-17
  * PHP: Suppression format bootstrap du tableau. retour custom

### 2015-02-16
  * PHP: Ajout filtre catégorie: Toutes+Aucune+séparateur

### 2015-02-14
  * PHP: Correction utf8 coté PHP MySQL -> merci WOoOinux !
  * $cnx->exec("set names utf8");

### 2015-02-15	Correction de toutes les chaines caractères en utf-8. ex: u'texte'

### 2015-02-12
  * Ajout gestion utf-8

### 2015-02-08 [commit]
  * Mise en place sélection extraction Horodatage/Catégorie/NivDétail/MessageLog
  * Remplacement de l'animation loader

### 2015-02-07
  * Correction animation Play/Pause
  * Ajout icone SQL on/off

### 2014-10-12 [commit]
  * Ajout selections case à cocher dans le profile de réglage

### 2014-10-10
  * Modif GUI case à cocher décodage Horodatage/Catégorie/Priorité

### 2014-09-29
  * Ajout événements checkBox + Enable/Disable Txt et comboBox

### 2014-09-28
  * Ajout chekBox pour extraction et séparation des données

### 2014-09-24
  * Ajout MysqlInsert sur réception CR = ok

### 2014-09-23
  * Bouton MySQL INSERT fonctionne vers base serial_sql_logger Cubietruck

### 2014-09-21
  * Recherche MySQLdb

### 2014-09-20
  * Ajout test MySQL MySQLdb 64bits http://www.codegood.com/archives/129

### 2014-09-19
  * Ajout de png spacer pour toolbar séparation des objets

### 2014-09-08 [commit]
  * Ajout AppliStart/AppliStop sur bouton Play/Stop toolbar test Linux Debian=ok
  * Etude bug graphique RUN clignotant bmp ON/OFF
  * le bug est du à la toolbar -> Déplacement du clignotant dans la toolbar

### 2014-09-07
  * Correction wxBitmapComboBox: compatibilité linux=ok

### 2014-08-10
  * Création ToolBar, remplacement terme 'Actualisation port' par 'Rechercher port'
  * Suppression menu COM1..25 fonction EnableCOM() CheckCOM()

### 2014-07-27
  * Actualisation port COM dans comboBox: w7+debian=ok				

### 2014-07-26	
  * wxFB: redimenssionnement GUI pour CubieTruck résol. 1024x768
  * Indication OS+architecture 32/64bits

### 2014-07-22 [commit]
  * Fin gestion profile conf port série, avec rappel dans titre appli

### 2014-07-21
  * Gestion profile New/Open/Save/SaveAS
  * Fonctions CheckCOM() CheckVitesse() pour actu selection menu depuis profile

### 2014-07-20
  * renome variable fichier en logFolderName/logFileName
  * création gestion profile avec module ConfigParser

### 2014-07-19
  * Remome wxFB nouveau/ouvrir/enreg/enreg en newLog/openLog/saveLog/saveAsLog
  * Ajout  wxFB newProfil/openProfil/saveProfil/saveAsProfil

### 2014-06-15
  * Remplacement disableBlinkGbl par enableBlinkGbl

### 2014-06-01 [commit]
  * GUI: Ajout CtrlTxt pour zone logs appli en plus de print
  * Ajout fonction MsgLog(self,"message") pour "logAppliTextCtrl"

### 2014-05-31 [commit]
  * Correction open-save-saveas car textCtrl nom différent
  * wxFB changement titre fenêtre appli
  * wxFB logTextCtrl enabled=true pour capture logs copier-coller
  * Ajout menu Port COM21 à COM25
  * Ajout RUN clignotant
  * Remplacement self.logTextCtrl.Value par self.logTextCtrl.WriteText
  * Modif self.repr_mode=1 pour gestion CRLF
  * Ajout arrêt clignotant pendant popup open/save/saveas
  * Essai ok: pc jc bluetooth COM20, avec VM prog08 WinCC Bac63 Ligne10 COM4

### 2014-05-17
  * Ajout réception série dans le textCtrl (aide miniterm.py de pySerial)
  * Ajout Led ERR rouge/gris clignotant, si erreur definition port COM

--------------------------------------------------------------------------------
### 2014-05-11: [commit]
  * Fork de Serie_vers_Afficheur_Uno_MAIN.py
  * Adaptation:
  * suppression des boutons, slider, progressbar etc
--------------------------------------------------------------------------------

### 2014-05-04:
  * Ajout dev menu [Fichier] <Enregistrer>
  *                [Fichier] <Enregistrer sous...>
  *                [Fichier] <Ouvrir>
  * Correction bug menu [Port COM]/<Actualiser> en wxITEM_RADIO
  * Correction orthographe 'périphérique'+'Système' dans menu [Système]
  * Mise en commentaire fonction 'ActualiserCOM()' au démarrage appli

### 2014-04-26b:
  * Correction bug menu [Port COM]/<Séléction manuelle> en wxITEM_RADIO


### 2014-04-26a:
  * Ajout menu [Fichier]/<Nouveau> 
  * mot COM dans menu [Vitesse COM]
  * différenciation des commentaires [menu] et <menuItem>
  * ré-indentation des commentaires du header de l'appli

### 2014-04-24:
  * Ajout COM16 à COM20 dans menu 'Port COM'

### 2014-04-24:
  * Ajout menu <Gestionnaire de periphérique>
  
### 2014-04-22:
  * Ajout boite dialogue saisie manu port COM
  * Boite dialogue erreur choix du port COM

### 2014-04-21:
  * Ajout menu <Vitesse> 
  * description menu status
  * Remplacement status Ctrtxt par StaticText
  
### 2014-04-20:	
  * Ajout menu <Port COM>
  * activation COM dispo dans menu

### 2014-04-19:	
  * Creation Python
  
