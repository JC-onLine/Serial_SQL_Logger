<html>
	<head>
		<meta charset="utf-8">
		<title>Formulaire</title>
	</head>
	<body>
		<?php

		if (!empty($_POST)) {
			echo '<p>Le bouton enfoncé est le bouton ';
			if (isset($_POST['profileSave'])) {
				echo 'Sauvegarder';
			}
			elseif (isset($_POST['profileDelete'])) {
				echo 'Supprimer';
			}
			else {
				// par défaut, c'est le bouton 1, même si on ne clique pas/
				echo '1';
			}
			echo '</p>';
			echo '<p>Le champ texte contient: ', $_POST['profileValue'], '</p>';
			echo '<p>Le navigateur contient : ', $_POST['nav'], '</p>';
		}
	//	$_POST())
	?><form action="<?php echo $_SERVER['PHP_SELF'] ?>" method="post">
		<p><input type="text" name="champ" /></p>
		<p><input type="submit" name="bouton1" value="Le bouton 1" />&nbsp;
		<input type="submit" name="bouton2" value="Le bouton 2" />&nbsp;
		<input type="submit" name="bouton3" value="Le bouton 3" /></p>
	</form>
</html>
