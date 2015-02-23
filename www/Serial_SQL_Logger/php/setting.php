<!--
# 					menu_auto.php
#
# Principe	:	mémoriser le nom de la table courante dans 'serial_sql_logger_setting'
#
# Dépendance:	base MySQL 'serial_sql_logger_setting'
# 2015-02-15:	Creation
#
#-->
<!DOCTYPE html>
<html lang="fr">
	<head>
		<meta charset="utf-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<title>Serial SQL Logger</title>
	</head>
	<body>
		<?php
			// init var
			$currentArchive  = "";
			$currentCategory = "";
			$currentMarker   = 0;
			$currentId       = 0;
			// récupération des paramètres:
			// table archive
			if (isset($_GET['archive']) ){
				$currentArchive = $_GET['archive'];
			}
			// category
			if (isset($_GET['category']) ) {
				$currentCategory = $_GET['category'];
			}
			// marker
			if (isset($_GET['marker']) ) {
				$currentMarker = $_GET['marker'];
			}
			// id
			if (isset($_GET['id']) ) {
				$currentId = $_GET['id'];
			}
			// connexion SQL
			$server		= "localhost";
			$user		= "root";
			$passwd		= "";
			$db_setting = "serial_sql_logger_setting";
			$db_data	= "serial_sql_logger_data";
			$port		= "3306";
			// tentative de connexion base de réglages
			try {
				$cnxSetting = new PDO('mysql:host='.$server.';port='.$port.';dbname='.$db_setting, $user, $passwd);
			}
			// capture éventuelle erreur
			catch(PDOExeption $e){
				echo 'N° : '.$e->getCode().'<br />';
				die ('Erreur base de réglages : '.$e->getMessage().'<br />');
			}
			// tentative de connexion base de data
			try {
				$cnxData = new PDO('mysql:host='.$server.';port='.$port.';dbname='.$db_data, $user, $passwd);
			}
			// capture éventuelle erreur
			catch(PDOExeption $e){
				echo 'N° : '.$e->getCode().'<br />';
				die ('Erreur base de réglages : '.$e->getMessage().'<br />');
			}
			// suite si pas erreur connexion
			$cnxData->exec("set names utf8");
			$cnxData->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
			
			// on veut mémoriser la table archive selectionnée
			if ($currentArchive != ""){
				// composition requête SQL
				$sqlQuery = "UPDATE filter SET tableArchive='".$currentArchive."' WHERE id=1;";
				// préparation de la transaction
				$qid = $cnxSetting->prepare($sqlQuery);
				// execute la requête
				$qid->execute();
				// forçage de la catégorie à '*'
				$sqlQuery = "UPDATE filter SET category='all' WHERE id=1;";
				// préparation de la transaction
				$qid = $cnxSetting->prepare($sqlQuery);
				// execute la requête
				$qid->execute();
			}
			// sinon on li dans la base réglages, la table en cours
			else{
				// composition requête SQL
				$sqlQuery = "SELECT tableArchive FROM filter WHERE id=1;";
				// préparation de la transaction
				$qid = $cnxSetting->prepare($sqlQuery);
				// execute la requête
				$qid->execute();
				while ($row=$qid->fetch(PDO::FETCH_OBJ)){
					// récupération nom table archive en cours depuis table réglages
					$currentArchive = $row->tableArchive;
				}
			}
			
			// on veut mémoriser la categorie selectionnée dans la table de réglages
			if ($currentCategory != ""){
				// composition requête SQL
				$sqlQuery = "UPDATE filter SET category='".$currentCategory."' WHERE id=1;";
				// préparation de la transaction
				$qid = $cnxSetting->prepare($sqlQuery);
				// execute la requête
				$qid->execute();
			}
			// sinon lecture dans la base réglages, la table en cours
			else{
				// composition requête SQL
				$sqlQuery = "SELECT category FROM filter WHERE id=1;";
				// préparation de la transaction
				$qid = $cnxSetting->prepare($sqlQuery);
				// execute la requête
				$qid->execute();
				while ($row=$qid->fetch(PDO::FETCH_OBJ)){
					// récupération catégorie en cours depuis table réglages
					$currentCategory = $row->category;
				}
			}
			// on veut mémoriser la marker selectionné
			if ($currentMarker != ""){
				// composition requête SQL
				$sqlQuery = "UPDATE `".$currentArchive."` SET marker=".$currentMarker." WHERE id=".$currentId.";";
				// préparation de la transaction
				$qid = $cnxData->prepare($sqlQuery);
				// execute la requête
				$qid->execute();
			}
			//dirige le chargement vers page d'accueil 
			header('Location: ../serial_sql_logger.php');
		?>
	</body>
</html>

