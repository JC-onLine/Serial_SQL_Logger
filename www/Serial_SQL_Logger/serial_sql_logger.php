<!--
# 					menu_auto.php
#
# Principe	:	Le but est de visionner des logs enregistrés dans une base MySQL.
#
# Dépendance:	base MySQL 'serial_sql_logger'
#				Bootstrap 3: 'bootstrap-3.3.1-dist.zip'
# 2015-02-09:	Creation
# 2015-02-14:	Correction utf8 coté PHP MySQL -> merci Rémy !
#					$cnx->exec("set names utf8");
# 2015-02-15:	Ajout menu des tables de stockage
# 2015-02-15:	Ajout base serial_sql_logger_setting pour les réglages
# 2015-02-16:	Ajout filtre catégorie: Toutes+Aucune+séparateur
# 2015-02-17:	Suppression format bootstrap du tableau. retour custom
# 2015-02-18:	Ajout du marqueur de ligne
#
#-->
<!DOCTYPE html>
<html lang="fr">
	<head>
		<meta charset="utf-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<title>Serial SQL Logger</title>
		<!-- Liaisons aux fichiers css de Bootstrap -->
		<link href="dist/css/bootstrap.min.css" rel="stylesheet"/>
		<link href="dist/css/bootstrap-theme.min.css" rel="stylesheet"/>
		<!-- Liaisons aux fichiers css personnalisé -->
		<link href="css/style_custom.css" rel="stylesheet"/>
		<link href="assets/ionicons-2.0.1/css/ionicons.min.css" rel="stylesheet"/>
		<!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
		<!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
		<!--[if lt IE 9]>
		  <script src="assets/js/html5shiv.min.js"></script>
		  <script src="assets/js/respond.min.js"></script>
		<![endif]-->
		<style>
			body {
				padding-top:  52px;
			}
		</style>
	</head>
	<body>
		<?php
		$parametreJour = 0;
		$jourDebut = -1000;
		$jourFin   = 0;
		$touche6Active = ' class="active"';
		// connexion SQL
		$server		= "localhost";
		$user		= "root";
		$passwd		= "";
		$db_setting = "serial_sql_logger_setting";
		$db_data	= "serial_sql_logger_data";
		$port		= "3306";
		// tentative de connexion aux base de données
		// base de réglages
		try {
			$cnxSetting = new PDO('mysql:host='.$server.';port='.$port.';dbname='.$db_setting, $user, $passwd);
		}
		// capture éventuelle erreur
		catch(PDOExeption $e){
			echo 'N° : '.$e->getCode().'<br />';
			die ('Erreur base de réglages : '.$e->getMessage().'<br />');
		}
		// suite si pas erreur connexion
		$cnxSetting->exec("set names utf8");
		$cnxSetting->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
		// base de données aooli
		try {
			$cnxData	= new PDO('mysql:host='.$server.';port='.$port.';dbname='.$db_data, $user, $passwd);
		}
		// capture éventuelle erreur
		catch(PDOExeption $e){
			echo 'N° : '.$e->getCode().'<br />';
			die ('Erreur base de données: '.$e->getMessage().'<br />');
		}
		// suite si pas erreur connexion
		$cnxData->exec("set names utf8");
		$cnxData->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
		
		//======== GESTION DES PARAMETRES URL + COMPOSITION REQUETE SQL ========
		// on veut la tables d'archivage courante
		// composition requête SQL
		$sqlQuery = "SELECT tableArchive FROM filter WHERE id=1;";
		// préparation de la transaction
		$qid = $cnxSetting->prepare($sqlQuery);
		// execute la requête
		$qid->execute();
		// récup de l'extraction sql
		while ($row=$qid->fetch(PDO::FETCH_OBJ)){
			$currentArchive = $row->tableArchive;
		}
		// on veut la catégorie courante
		// composition requête SQL
		$sqlQuery = "SELECT category FROM filter WHERE id=1;";
		// préparation de la transaction
		$qid = $cnxSetting->prepare($sqlQuery);
		// execute la requête
		$qid->execute();
		// récup de l'extraction sql
		while ($row=$qid->fetch(PDO::FETCH_OBJ)){
			$currentCategory = $row->category;
		}

		// init de la touche active
		$touche1Active = "";
		$touche2Active = "";
		$touche3Active = "";
		$touche4Active = "";
		$touche5Active = "";
		$touche6Active = "";
		// test du parametre 'jour'
		// le paramètre jour existe t-il ?
	//	if ( (! isset($parametreJour)) OR  (! is_numeric($parametreJour)) OR (! ($parametreJour >=0) AND ($parametreJour <=7))){
		if ( (! isset($_GET['jour'])) OR  (! is_numeric($_GET['jour'])) OR (! (($_GET['jour'] >=0) AND ($_GET['jour'] <=7)))){
			$parametreJour = 0;
			$jourDebut = -1000;
			$jourFin   = 0;
			$touche6Active = ' class="active"';
		}
		else{
			$parametreJour = $_GET['jour'];
			$jourDebut = ($_GET['jour'] + 1 ) * -1;
			$jourFin   =  $_GET['jour'] * -1;
			// gestion touche active du menu
			if ($parametreJour == 4) { $touche1Active = ' class="active"'; } 
			if ($parametreJour == 3) { $touche2Active = ' class="active"'; } 
			if ($parametreJour == 2) { $touche3Active = ' class="active"'; } 
			if ($parametreJour == 1) { $touche4Active = ' class="active"'; } 
			if ($parametreJour == 0) { $touche5Active = ' class="active"'; } 
			if ($parametreJour == 1000) { $touche6Active = ' class="active"'; } 
		}
		// affiche l'entête du tableau bootstrap
	//	echo '<div class="container">';
	//		echo '<div class="row">';
				echo '<div class="navbar navbar-inverse navbar-fixed-top">';
					echo '<div class="collapse navbar-collapse">';
						echo '<ul class="nav navbar-nav">';
							// 1ere touche menu
							echo '<li class="dropdown">';
								echo '<a href="#" class="dropdown-toggle" data-toggle="dropdown">Table archivage <b class="caret"></b></a>';
								echo '<ul class="dropdown-menu">';
									// on veut la liste des tables d'archivage
									// composition requête SQL
									$sqlQuery = "SHOW TABLE STATUS FROM serial_sql_logger_data;";
									// préparation de la transaction
									$qid = $cnxSetting->prepare($sqlQuery);
									// execute la requête
									$qid->execute();
									// récup de l'extraction sql des tables disponibles
									while ($row=$qid->fetch(PDO::FETCH_OBJ)){
										// affichage en gras de la table archive sélectionnée
										if ($row->Name == $currentArchive)	{ $boldOpen = '<b>'; $boldClose = '</b>'; }
										else 								{ $boldOpen = '';    $boldClose = '';		  }
										echo '<li><a href="php/setting.php?archive='.$row->Name.'">'.$boldOpen.$row->Name.$boldClose.'</a></li>';
									}
								echo '</ul>';
							echo '</li>';
							// 2eme touche menu
							echo '<li class="dropdown">';
								echo '<a href="#" class="dropdown-toggle" data-toggle="dropdown">Catégorie <b class="caret"></b></a>';
								echo '<ul class="dropdown-menu">';
									// 1er  choix Catégorie: Toutes
									// affichage en gras de la table archive sélectionnée
									if ($currentCategory == 'all')  { $boldOpen = '<b>'; $boldClose = '</b>'; }
									else 							{ $boldOpen = '';    $boldClose = '';		  }
									echo '<li><a href="php/setting.php?category=all">'.$boldOpen.'Toutes'.$boldClose.'</a></li>';
									// 2eme choix Catégorie: Aucune
									// affichage en gras de la table archive sélectionnée
									if ($currentCategory == 'none') { $boldOpen = '<b>'; $boldClose = '</b>'; }
									else 							{ $boldOpen = '';    $boldClose = '';		  }
									echo '<li><a href="php/setting.php?category=none">'.$boldOpen.'Aucune'.$boldClose.'</a></li>';
									// Ligne de séparation
									echo '<li class="divider"></li>';
									// on veut la liste des catégorie
									// composition requête SQL
									$sqlQuery = "SELECT DISTINCT (categorie) FROM ".$currentArchive." ORDER BY categorie ASC;";
									// préparation de la transaction
									$qid = $cnxData->prepare($sqlQuery);
									// execute la requête
									$qid->execute();
									// récup de l'extraction sql des catégories disponibles
									while ($row=$qid->fetch(PDO::FETCH_OBJ)){
										// affichage en gras de la table archive sélectionnée
										if ($row->categorie == $currentCategory){ $boldOpen = '<b>'; $boldClose = '</b>'; }
										else 									{ $boldOpen = '';    $boldClose = '';		  }
										echo '<li><a href="php/setting.php?category='.$row->categorie.'">'.$boldOpen.$row->categorie.$boldClose.'</a></li>';
									}
								echo '</ul>';
							echo '</li>';
							echo '<li'.$touche1Active.'><a href="serial_sql_logger.php?jour=4">Jour J-4</a></li>';
							echo '<li'.$touche2Active.'><a href="serial_sql_logger.php?jour=3">Jour J-3</a></li>';
							echo '<li'.$touche3Active.'><a href="serial_sql_logger.php?jour=2">Jour J-2</a></li>';
							echo '<li'.$touche4Active.'><a href="serial_sql_logger.php?jour=1">Jour J-1</a></li>';
							echo '<li'.$touche5Active.'><a href="serial_sql_logger.php?jour=0">Jour J</a></li>';
							echo '<li'.$touche6Active.'><a href="serial_sql_logger.php?jour=1000">Complet</a></li>';
						echo '</ul>';
					echo '</div>';
				echo '</div>';
	//		echo '</div>';
			// Affichage en-tête du tableau
			//echo '<div class="panel panel-default">';
			echo '<div class="table-header">';
				echo '<table>';
				//echo '<table class="table table-condensed">';
					echo '<thead>';
						echo '<tr class="active">';
							echo '<th class="col01"></th>';
							echo '<th class="col02">Horodatage</th>';
							echo '<th class="col03">Catégorie</th>';
							echo '<th class="col04">Détail</th>';
							echo '<th class="col05">Message</th>';
						echo '</tr>';
					echo '</thead>';
				echo '</table>';
			echo '</div>';
			// affiche les données du tableau
			echo '<div class="div-table-content">';
		//		echo '<table class="table table-striped table-bordered table-hover table-condensed">';
				echo '<table>';
		//			echo '<tbody>';
						// composition requête SQL liste des messages logs
						// filtre catégorie: Toutes
						if ($currentCategory == "all"){
							$sqlQuery = "SELECT * FROM ".$currentArchive." WHERE horodatage BETWEEN NOW() + INTERVAL ".$jourDebut." DAY AND NOW() + INTERVAL ".$jourFin." DAY ORDER BY horodatage ASC";
						}
						// filtre catégorie: Aucune
						else if ($currentCategory == "none"){
							$sqlQuery = "SELECT * FROM ".$currentArchive." WHERE categorie='' AND horodatage BETWEEN NOW() + INTERVAL ".$jourDebut." DAY AND NOW() + INTERVAL ".$jourFin." DAY ORDER BY horodatage ASC";
						}
						// filtre catégorie: le reste
						else{
							$sqlQuery = "SELECT * FROM ".$currentArchive." WHERE categorie='".$currentCategory."' AND horodatage BETWEEN NOW() + INTERVAL ".$jourDebut." DAY AND NOW() + INTERVAL ".$jourFin." DAY ORDER BY horodatage ASC";
						}
						// préparation de la transaction
						$qid = $cnxData->prepare($sqlQuery);
						// execute la requête
						$qid->execute();
						// récup de l'extraction sql
						$lineCount = 0;
						while ($row=$qid->fetch(PDO::FETCH_OBJ)){
							// lecture du marqueur de la ligne
							if ($row->marker == 1) { 
								$markerStatus = " markerOn";
								$markerToggle = 0;
							}
							else { 
								$markerStatus = " markerOff";
								$markerToggle = 1;
							}
							echo '<tr class="trData">';
								echo '<td class="col01'.$markerStatus.'"><a href="php/setting.php?id='.$row->id.'&marker='.$markerToggle.'"><i class="ion-arrow-right-a"></i></a></td><td class="col02'.$markerStatus.'">'.$row->horodatage.'</td><td class="col03'.$markerStatus.'">'.$row->categorie.'</td><td class="col04'.$markerStatus.'">'.$row->niv_detail.'</td><td class="col05'.$markerStatus.'">'.$row->message.'</td>';
							echo '</tr>';
						/*	$lineCount++;
							if ($lineCount >= 28){
								echo '<thead>';
									echo '<tr class="active">';
										echo '<th>Horodatage</th>';
										echo '<th>Catégorie</th>';
										echo '<th>Détail</th>';
										echo '<th>Message</th>';
									echo '</tr>';
								echo '</thead>';
								$lineCount = 0;
							} */
						}
		//			echo '</tbody>';
					// fin du tableau boostrap
				echo '</table>';
			echo '</div>';		// div-table-content
	//		echo '</div>';
	//		echo '</div>';
		?>

		<!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
		<script src="assets/js/jquery-1.11.2.min.js" type="text/javascript"></script>
		<!-- Include all compiled plugins (below), or include individual files as needed -->
		<script src="dist/js/bootstrap.min.js" type="text/javascript"></script>
	</body>
</html>
