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
		if ( (! isset($_GET['table'])) ){
			$selectionTable = 'bacacier07ligne01';
			//$selectionTable = 'arduino';
		}
		else {
			$selectionTable = $_GET['table'];
		}
		$parametreJour = 0;
		$jourDebut = -1000;
		$jourFin   = 0;
		$touche6Active = ' class="active"';
		// connexion SQL
		$server = "localhost";
		$user   = "root";
		$passwd = "";
		$bdd    = "serial_sql_logger_data";
		$port   = "3306";
		// tantative de connexion
		try {
			$cnx = new PDO('mysql:host='.$server.';port='.$port.';dbname='.$bdd, $user, $passwd);
		}
		// capture éventuelle erreur
		catch(PDOExeption $e){
			echo 'N° : '.$e->getCode().'<br />';
			die ('Erreur : '.$e->getMessage().'<br />');
		}
		// suite si pas erreur connexion
		$cnx->exec("set names utf8");
		$cnx->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
		
		//======== GESTION DES PARAMETRES URL + COMPOSITION REQUETE SQL ========
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
									$qid = $cnx->prepare($sqlQuery);
									// execute la requête
									$qid->execute();
									// récup de l'extraction sql des tables disponibles
									while ($row=$qid->fetch(PDO::FETCH_OBJ)){
											echo '<li><a href="menu_auto.php?table='.$row->Name.'">'.$row->Name.'</a></li>';
											//echo '<li><a href="#">'.'test'.'</a></li>';
									}
								echo '</ul>';
							echo '</li>';
							// 2ere touche menu
							echo '<li class="dropdown">';
								echo '<a href="#" class="dropdown-toggle" data-toggle="dropdown">Catégorie <b class="caret"></b></a>';
								echo '<ul class="dropdown-menu">';
									// on veut la liste des catégorie
									// composition requête SQL
									$sqlQuery = "SELECT DISTINCT (categorie) FROM bacacier07ligne01 ORDER BY categorie ASC;";
									// préparation de la transaction
									$qid = $cnx->prepare($sqlQuery);
									// execute la requête
									$qid->execute();
									// récup de l'extraction sql des catégories disponibles
									while ($row=$qid->fetch(PDO::FETCH_OBJ)){
											echo '<li><a href="menu_auto.php?categorie='.$row->categorie.'">'.$row->categorie.'</a></li>';
											//echo '<li><a href="#">'.'test'.'</a></li>';
									}
								echo '</ul>';
							echo '</li>';
							echo '<li'.$touche1Active.'><a href="menu_auto.php?jour=4">Jour J-4</a></li>';
							echo '<li'.$touche2Active.'><a href="menu_auto.php?jour=3">Jour J-3</a></li>';
							echo '<li'.$touche3Active.'><a href="menu_auto.php?jour=2">Jour J-2</a></li>';
							echo '<li'.$touche4Active.'><a href="menu_auto.php?jour=1">Jour J-1</a></li>';
							echo '<li'.$touche5Active.'><a href="menu_auto.php?jour=0">Jour J</a></li>';
							echo '<li'.$touche6Active.'><a href="menu_auto.php?jour=1000">Complet</a></li>';
						echo '</ul>';
					echo '</div>';
				echo '</div>';
	//		echo '</div>';
			echo '<table class="table table-striped table-bordered table-hover table-condensed">';
				echo '<thead>';
					echo '<tr class="active">';
						echo '<th>Horodatage</th>';
						echo '<th>Catégorie</th>';
						echo '<th>Niveau détail</th>';
						echo '<th>Message</th>';
					echo '</tr>';
				echo '</thead>';
				// affiche les données du tableau
				echo '<tbody>';
					// composition requête SQL liste des messages logs
					$sqlQuery = "SELECT * FROM ".$selectionTable." WHERE horodatage BETWEEN NOW() + INTERVAL ".$jourDebut." DAY AND NOW() + INTERVAL ".$jourFin." DAY ORDER BY horodatage ASC";
					// préparation de la transaction
					$qid = $cnx->prepare($sqlQuery);
					// execute la requête
					$qid->execute();
					// récup de l'extraction sql
					while ($row=$qid->fetch(PDO::FETCH_OBJ)){
						echo '<tr>';
							echo '<td>'.$row->horodatage.'</td><td>'.$row->categorie.'</td><td>'.$row->niv_detail.'</td><td>'.$row->message.'</td>';
						echo '</tr>';
					}
				echo '</tbody>';
			// fin du tableau boostrap
			echo '</table>';
	//		echo '</div>';
	//		echo '</div>';
		?>

		<!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
		<script src="assets/js/jquery-1.11.2.min.js" type="text/javascript"></script>
		<!-- Include all compiled plugins (below), or include individual files as needed -->
		<script src="dist/js/bootstrap.min.js" type="text/javascript"></script>
	</body>
</html>