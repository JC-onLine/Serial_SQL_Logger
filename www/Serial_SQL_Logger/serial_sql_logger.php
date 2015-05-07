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
# 2015-03-23:	Suppression 'echo' pour afficher html5
#				Ajout lecture/ecriture base SQL keyword color
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
		<!-- Liaisons aux fichiers css de Bootstrap-toggle -->
		<link href="dist/css/bootstrap-toggle.min.css" rel="stylesheet">
		<!-- Liaisons aux fichiers css personnalisé -->
		<link href="css/serial_sql_logger.css" rel="stylesheet"/>
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
		// définition des constantes:
		$KEYWORD_MAXI = 10;
		// gestion base de données
		include "php/connect.php";
		// suite si pas erreur connexion
		$parametreJour = 0;
		$jourDebut = -1000;
		$jourFin   = 0;
		$touche6Active = ' class="active"';
		
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
		// on veut le profile de coloration courant
		// composition requête SQL
		$sqlQuery = "SELECT currentKeywordProfileName FROM filter WHERE id=1;";
		// préparation de la transaction
		$qid = $cnxSetting->prepare($sqlQuery);
		// execute la requête
		$qid->execute();
		// récup de l'extraction sql
		while ($row=$qid->fetch(PDO::FETCH_OBJ)){
			$profileNameValue = $row->currentKeywordProfileName;
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
		// affiche la barre de navigation ?>
		<div class="navbar navbar-inverse navbar-fixed-top">
			<div class="collapse navbar-collapse">
				<ul class="nav navbar-nav">
					
					<!-- ================ -->
					<!-- 1ere touche menu -->
					<!-- ================ -->
					<li class="dropdown">
						<a href="#" class="dropdown-toggle" data-toggle="dropdown">Table archivage <b class="caret"></b></a>
							<ul class="dropdown-menu">
							<?php
								// on veut la liste des tables d'archivage pour le menu déroulant
								// composition requête SQL
								$sqlQuery = "SHOW TABLE STATUS FROM serial_sql_logger_data;";
								// préparation de la transaction
								$qid = $cnxSetting->prepare($sqlQuery);
								// execute la requête
								$qid->execute();
								// récup de l'extraction sql des tables disponibles
								while ($row=$qid->fetch(PDO::FETCH_OBJ)){
									// affichage en gras de la table archive sélectionnée
									if ($row->Name == $currentArchive)	{ $liClass = ' class="active"'; $boldOpen = '<b>'; $boldClose = '</b>'; }
									else 								{ $liClass = "";                $boldOpen = '';    $boldClose = '';		  }
									echo '<li'.$liClass.'><a href="php/setting.php?archive='.$row->Name.'">'.$boldOpen.$row->Name.$boldClose.'</a></li>';
								}
							?>
						</ul>
					</li>
					
					<!-- ================ -->
					<!-- 2eme touche menu -->
					<!-- ================ -->
					<li class="dropdown">
						<a href="#" class="dropdown-toggle" data-toggle="dropdown">Catégorie <b class="caret"></b></a>
						<ul class="dropdown-menu">
							<!-- 1er  choix Catégorie: Toutes -->
							<?php
								// affichage en gras de la table archive sélectionnée
								if ($currentCategory == 'all')  { $liClass = ' class="active"'; $boldOpen = '<b>'; $boldClose = '</b>'; }
								else 							{ $liClass = "";                $boldOpen = '';    $boldClose = '';		  }
								echo '<li'.$liClass.'><a href="php/setting.php?category=all">'.$boldOpen.'Toutes'.$boldClose.'</a></li>';
								// 2eme choix Catégorie: Aucune
								// affichage en gras de la table archive sélectionnée
								if ($currentCategory == 'none') { $liClass = ' class="active"'; $boldOpen = '<b>'; $boldClose = '</b>'; }
								else 							{ $liClass = "";                $boldOpen = '';    $boldClose = '';		  }
								echo '<li'.$liClass.'><a href="php/setting.php?category=none">'.$boldOpen.'Aucune'.$boldClose.'</a></li>';
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
									if ($row->categorie == $currentCategory){ $liClass = ' class="active"'; $boldOpen = '<b>'; $boldClose = '</b>'; }
									else 									{ $liClass = "";                $boldOpen = '';    $boldClose = '';		  }
									echo '<li'.$liClass.'><a href="php/setting.php?category='.$row->categorie.'">'.$boldOpen.$row->categorie.$boldClose.'</a></li>';
								}
							?>
						</ul>
					</li>
						<!-- ===================== -->
						<!-- Touches 3,4,5,6,7,8   -->
						<!-- ===================== -->
						<!-- menu des jours précédants avec Animation touche sélectionnée -->
						<!-- 3eme touche menu -->
						<li <?php$touche1Active?> <a href="serial_sql_logger.php?jour=4">Jour J-4</a></li>
						<!-- 4eme touche menu -->
						<li <?php$touche2Active?> <a href="serial_sql_logger.php?jour=3">Jour J-3</a></li>
						<!-- 5eme touche menu -->
						<li <?php$touche3Active?> <a href="serial_sql_logger.php?jour=2">Jour J-2</a></li>
						<!-- 6eme touche menu -->
						<li <?php$touche4Active?> <a href="serial_sql_logger.php?jour=1">Jour J-1</a></li>
						<!-- 7eme touche menu -->
						<li <?php$touche5Active?> <a href="serial_sql_logger.php?jour=0">Jour J</a></li>
						<!-- 8eme touche menu -->
						<li <?php$touche6Active?> <a href="serial_sql_logger.php?jour=1000">Complet</a></li>
						<!-- 9eme touche menu -->
		<!--				<li>
							<div class="checkbox"> 
							<label>
								<input type="checkbox" data-toggle="toggle">
								Visu auto
							</label>
							</div> 
						</li>	-->
				</ul>
				<!-- dernière touche menu dashboard -->
				<ul class="nav navbar-nav navbar-right">
					<li class="dashboard-icon"><a href="dashboard.php"><i class="ion-gear-b"></i> <i class="ion-speedometer"></i></a></li>
				</ul>
			</div>		<!-- <div class="collapse navbar-collapse"> -->
		</div>			<!-- <div class="navbar navbar-inverse navbar-fixed-top"> -->
		
		<!-- ============================ -->
		<!-- Affichage en-tête du tableau -->
		<!-- ============================ -->
		<?php
			// on veut les largeurs des 15 colonnes dans la base SQL:
			// composition requête SQL
			$sqlQuery = "SELECT * FROM size WHERE id=1;";
			// préparation de la transaction
			$qid = $cnxSetting->prepare($sqlQuery);
			// execute la requête
			$qid->execute();
			// récup de l'extraction sql
			while ($row=$qid->fetch(PDO::FETCH_OBJ)){
				$colGetSize[1]  = $row->sizeCol1;
				$colGetSize[2]  = $row->sizeCol2;
				$colGetSize[3]  = $row->sizeCol3;
				$colGetSize[4]  = $row->sizeCol4;
				$colGetSize[5]  = $row->sizeCol5;
				$colGetSize[6]  = $row->sizeCol6;
				$colGetSize[7]  = $row->sizeCol7;
				$colGetSize[8]  = $row->sizeCol8;
				$colGetSize[9]  = $row->sizeCol9;
				$colGetSize[10] = $row->sizeCol10;
				$colGetSize[11] = $row->sizeCol11;
				$colGetSize[12] = $row->sizeCol12;
				$colGetSize[13] = $row->sizeCol13;
				$colGetSize[14] = $row->sizeCol14;
				$colGetSize[15] = $row->sizeCol15;
			}
			// application des largeur de colonne:
			for ($i=1; $i<16; $i++){
				echo '<style>';
				echo 	'th.col'.$i.', td.col'.$i.' { width: '.$colGetSize[$i].'px;}';
				echo '</style>';
			}
		?>
		
		<!-- Header du tableau de log -->
		<div class="table-header">
			<table>
			<!-- supprimé  <table class="table table-condensed"> -->
				<thead>
					<tr class="active">
						<th class="col1"></th>
						<th class="col2">Horodatage</th>
						<th class="col3">Catégorie</th>
						<th class="col4">Détail</th>
						<th class="col5">Message</th>
					</tr>
				</thead>
			</table>
		</div>

		<!-- Affiche les données du tableau: -->
		<div class="div-table-content">
			<table>
				<tbody>
				<?php
					// on veut les mots clés et couleurs:
					// composition requête SQL
					//$sqlQuery = "SELECT * FROM keyword_color ;";
					$sqlQuery = "SELECT * ".
								"FROM keyword_color ".
								"JOIN keyword_color_profile ON ".
								"keyword_color_profile.id = keyword_color.keywordProfile_id ".
								"WHERE ".
								"keyword_color_profile.profilename = '".$profileNameValue."';";
					// préparation de la transaction
					$qid = $cnxSetting->prepare($sqlQuery);
					// execute la requête
					$qid->execute();
					// récup de l'extraction sql
					while ($row=$qid->fetch(PDO::FETCH_OBJ)){
						for ($i=1; $i<=$KEYWORD_MAXI; $i++){
							// constuction nom champ pour extraction SQL:
							$keywordCheckIdx = 'keywordCheck'.$i;
							$keywordValueIdx = 'keywordValue'.$i;
							$keywordColorIdx = 'keywordColor'.$i;
							$keywordCheckArray[$i] = $row->$keywordCheckIdx;
							$keywordValueArray[$i] = $row->$keywordValueIdx;
							$keywordColorArray[$i] = $row->$keywordColorIdx;
						}
					}
					
					// fonction auxiliaire pour la coloration des mots clés
					function ColorKeyword($message){
						global $keywordCheckArray, $keywordValueArray, $keywordColorArray;
						// scan le tableau de mots clés et remplace par le style colorié
						$newMessage = $message;
						//$i=2;
						for ($i=1; $i<11; $i++){
							if ($keywordCheckArray[$i] == "checked"){
								// remplacement keyword avec sa couleur
								$newMessage = str_replace($keywordValueArray[$i], 
												'<style>.mark'.$i.' { background-color:'.$keywordColorArray[$i].'; color:black; }</style><mark class="mark'.$i.'">'.$keywordValueArray[$i].'</mark>', 
												$newMessage);
							}
						}
						return($newMessage);
					}
					
					
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
							echo '<td class="col1'.$markerStatus.'"><a href="php/setting.php?id='.$row->id.'&marker='.$markerToggle.'">';
							echo '<i class="ion-play"></i></td>';
							echo '<td class="col2'.$markerStatus.'">'.$row->horodatage.'</td>';
							echo '<td class="col3'.$markerStatus.'">'.$row->categorie.'</td>';
							echo '<td class="col4'.$markerStatus.'">'.$row->niv_detail.'</td>';
							echo '<td class="col5'.$markerStatus.'">'.ColorKeyword($row->message).'</td>';
						echo '</tr>';
					}
				?>
				</tbody>
				<!-- fin du tableau -->
			</table>
		</div>		<!-- div-table-content -->

		<!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
		<script src="assets/js/jquery-1.11.2.min.js" type="text/javascript"></script>
		<!-- Include all compiled plugins (below), or include individual files as needed -->
		<script src="dist/js/bootstrap.min.js" type="text/javascript"></script>
		<!-- Liaisons aux fichiers css de Bootstrap-toggle -->
		<script src="dist/js/bootstrap-toggle.min.js"></script>
	</body>
</html>
