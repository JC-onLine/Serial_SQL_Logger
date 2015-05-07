<!--
# 					menu_auto.php
#
# Principe	:	mémoriser le nom de la table courante dans 'serial_sql_logger_setting'
#
# Dépendance:	base MySQL 'serial_sql_logger_setting'
# 2015-02-15:	Creation
# 2015-03-22:	Lecture/écriture réglages colonne SQL
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
	</head>
	<style>
		body{
			background:			#2E3436; 
			color:				#A0D400; 
		}
	</style>
	<body>
		<?php
			// définition des constantes:
			$KEYWORD_MAXI = 10;
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
				//echo 'setting.php: update marker ok';
			}
			// ==== UPDATE COLUMN SIZE ====
			// ============================
			if ((array_key_exists('setting',$_POST)) && ($_POST['setting'] == 'SetColSize')){
				echo '<p>ok pour mise à jour des colonnes...</p>';
				echo 'col-value1='.$_POST["col-value1"].'<br /><br />';
				var_dump($_POST);
				// composition requête SQL
				$sqlQuery = "UPDATE `size` SET ";
				for ($i=1; $i<15; $i++){
					$sqlQuery = $sqlQuery."sizeCol".$i."=".$_POST["col-value".$i].", ";
					
				}
				$sqlQuery = $sqlQuery."sizeCol".$i."=".$_POST["col-value".$i];
				$sqlQuery = $sqlQuery." WHERE id=1;";
				echo '$sqlQuery='.$sqlQuery;
				// préparation de la transaction
				$qid = $cnxSetting->prepare($sqlQuery);
				// execute la requête
				$qid->execute();
				//echo 'setting.php: update sizeColxx ok';
			}
			
			// ==== UPDATE KEYWORD COLOR ====
			// ==============================
			if ((array_key_exists('setting',$_POST)) && ($_POST['setting'] == 'SetKeywordColor')){
				echo '<p>ok pour mise à jour des mots clés et couleurs...</p>';
				var_dump($_POST);
				// composition requête SQL
				$sqlQuery = "UPDATE `keyword_color` SET ";
				for ($i=1; $i<=$KEYWORD_MAXI - 1; $i++){
					// gestion case à cocher = 'null' ou 'On'
					if (!isset($_POST["keywordCheck".$i])){
						$_POST["keywordCheck".$i] = '';
					}
					else{
						$_POST["keywordCheck".$i] = 'checked';
					}
					$sqlQuery = $sqlQuery. 
									"keywordCheck".$i."='".$_POST["keywordCheck".$i]. "', ".
									"keywordValue".$i."='".$_POST["keywordValue".$i]. "', ".
									"keywordColor".$i."='".$_POST["keywordColor".$i]. "', ";
				}
				// derniere ligne sans virgule en fin de ligne:
				$i = $KEYWORD_MAXI;
				$sqlQuery = $sqlQuery. 
									"keywordCheck".$i."='".$_POST["keywordCheck".$i]. "', ".
									"keywordValue".$i."='".$_POST["keywordValue".$i]. "', ".
									"keywordColor".$i."='".$_POST["keywordColor".$i]. "' ";
									"WHERE keywordProfileName='Bacacier07';";
					echo '$sqlQuery= '.$sqlQuery.'<br />';
				// préparation de la transaction
				$qid = $cnxSetting->prepare($sqlQuery);
				// execute la requête
				$qid->execute();
				echo 'setting.php: update keyword color ok';
			}
			
			//dirige le chargement vers page d'accueil 
			header('Location: ../serial_sql_logger.php');
		?>
	</body>
</html>



