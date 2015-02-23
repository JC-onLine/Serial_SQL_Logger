<!DOCTYPE html>
<html lang="fr">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Bootstrap Template</title>

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
		padding-top: 70px;
	}
	</style>
  </head>
  <body>
	<?php
	// connexion SQL
	$server = "localhost";
	$user   = "root";
	$passwd = "";
	$bdd    = "serial_sql_logger";
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
	$cnx->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
	// composition de la requête SQL
	$sqlQuery = "SELECT * FROM bacacier07ligne01 ORDER BY horodatage ASC";
	// préparation de la transaction
	$qid = $cnx->prepare($sqlQuery);
	// execute la requête
	$qid->execute();
	// affiche l'entête du tableau bootstrap
	echo '<div class="container">';
		echo '<div class="row">';
			echo '<div class="navbar navbar-inverse navbar-fixed-top">';
				echo '<div class="collapse navbar-collapse">';
					echo '<ul class="nav navbar-nav">';
						echo '<li><a href="#">Jour J-4</a></li>';
						echo '<li><a href="#">Jour J-3</a></li>';
						echo '<li><a href="#">Jour J-2</a></li>';
						echo '<li><a href="#">Jour J-1</a></li>';
						echo '<li class="active"><a href="#">Jour H-4</a></li>';
					echo '</ul>';
				echo '</div>';
			echo '</div>';
		echo '</div>';
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
			// récup de l'extraction sql
			while ($row=$qid->fetch(PDO::FETCH_OBJ)){
				echo '<tr>';
					echo '<td>'.$row->horodatage.'</td><td>'.$row->categorie.'</td><td>'.$row->niv_detail.'</td><td>'.$row->message.'</td>';
				echo '</tr>';
			}
		echo '</tbody>';
	// fin du tableau boostrap
	echo '</table>';
	echo '</div>';
	echo '</div>';
	?>

    <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
    <script src="assets/js/jquery-1.11.2.min.js" type="text/javascript"></script>
    <!-- Include all compiled plugins (below), or include individual files as needed -->
    <script src="dist/js/bootstrap.min.js" type="text/javascript"></script>
  </body>
</html>
