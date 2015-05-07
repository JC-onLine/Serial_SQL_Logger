<!--
# 					dashboard.php
#
# Principe	:	Le but est d'avoir une page de réglages du tableau.
#
# Dépendance:	base MySQL 'serial_sql_logger'
#				Bootstrap 3: 'bootstrap-3.3.1-dist.zip'
# 2015-03-15:	Creation zone header, nav, section, footer
# 2015-03-17:	création présentation page couleurs mots clés
# 2015-03-19:	création présentation page largeurs colonnes 
#				avec slider en refresh jQuerry
# 2015-03-22:	Lecture/écriture réglages colonne SQL
# 2015-03-23:	Suppression 'echo' pour afficher html5
#				Ajout lecture/ecriture base SQL keyword color
# 2015-04-04:	Remplacement $_GET par $_POST
# 				KeywordColor: Ajout paramètres profile via $_POST
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
		<link href="css/dashboard.css" rel="stylesheet"/>
		<link href="assets/ionicons-2.0.1/css/ionicons.min.css" rel="stylesheet"/>

		<link rel="stylesheet" media="screen" href="assets/jquery-ui-1.11.4.custom/jquery-ui.min.css" type="text/css"/>

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
		<header>
			<!-- affiche l'entête du dashboard -->
			<div class="navbar navbar-inverse navbar-fixed-top">
				<div class="collapse navbar-collapse">
					<!-- texte fixe 'Tableau de bord -->
					<div class="navbar-header">
						<a class="navbar-brand" href="#">Tableau de bord</a>
					</div>
					<!-- touche retour menu -->
					<ul class="nav navbar-nav navbar-right">
						<li class="dashboard-icon active">
							<a href="serial_sql_logger.php"><i class="ion-ios-home"> <i class="ion-reply"></i></i></a>
						</li>
					</ul>
				</div>
			</div>
		</header>
		<nav>
			<?php
			// définition des constantes:
			$DEBUG = false;
			// contrôle accès base de données
			include "php/connect.php";
			// intégration des fonctions auxiliaires
			require ('php\auxiliaire.php');
			// init touche nav active
			$nav1active = '';
			$nav2active = '';
			$nav3active = '';
			$nav4active = '';
			// traitement du paramètre nav
			if ( (! isset($_GET['nav'])) OR  (! is_numeric($_GET['nav'])) OR (! (($_GET['nav'] >=0) AND ($_GET['nav'] <=7)))){
				// paramètre 'nav' incorrecte donc init:
				$nav = 1;
				$nav1active = ' class="active"';
			}
			else{
				// paramètre 'nav' donc gestion nav aside
				$nav = $_GET['nav'];
				// gestion touche active du menu nav
				if ($nav == 1) { $nav1active = ' class="active"'; } 
				if ($nav == 2) { $nav2active = ' class="active"'; } 
				if ($nav == 3) { $nav3active = ' class="active"'; } 
				if ($nav == 4) { $nav4active = ' class="active"'; } 
			}
			// traitement du paramètre profileName
			if ( (! isset($_GET['profileName'])) OR  ( is_numeric($_GET['profileName'])) ){
				// paramètre 'profileName' incorrecte donc init:
				$profileName = '';
			}
			else{
				// paramètre 'profileName' donc gestion profileName
				$profileName = $_GET['profileName'];
				// mémorisation SQL du profile courant dans la table 'filter'
				$sqlQuery = "UPDATE `filter` SET 
								currentKeywordProfileName='".$profileName."'
								WHERE id=1;";
				if ($DEBUG){ echo '$sqlQuery= '.$sqlQuery.'<br />'; }
				// préparation de la transaction
				$qid = $cnxSetting->prepare($sqlQuery);
				// execute la requête
				$qid->execute();
			}
			?>


			<!-- BOUTONS NAVIGATEUR DE GAUCHE -->
			<div class="navdash">
				<ul class="nav navbar-inverse nav-pills nav-stacked">
					<?php echo '<li'.$nav1active.'><a href="dashboard.php?nav=1"><i class="icon-dashboard ion-android-color-palette"></i>Coloration mots clés</a></li>
								<li'.$nav2active.'><a href="dashboard.php?nav=2"><i class="icon-dashboard ion-ios-book"></i>Mise en page</a></li>'; ?>
				</ul>
			</div>
		</nav>
		<section>
			<?php
			//=======================================
			//======== nav1: Couleur mot clé ========
			//=======================================
			if ($nav == 1) { 
				// définition des constantes:
				$KEYWORD_MAXI = 10;
				// Principe: le keywordValue peut provenir de:
				// profileNameInput défini : => envoyé via formulaire 'submit'
				// profileNameInput non déf: => sinon reprise nom profile courant dans SQL
				// Test récup nom profile par 'submit' via formulaire:
				if (isset($_POST['profileNameInput'])) {
					$profileNameInput = $_POST['profileNameInput'];
					if ($DEBUG){ echo 'profileNameInput DEFINI : => envoyé via formulaire submit: '.$profileNameInput.'<br />'; }
				}
				// Sinon lecture nom du profile courant dans SQL table 'filter':
				else{
					$profileNameInput = '';
					$sqlQuery = "SELECT currentKeywordProfileName FROM filter WHERE id=1;";
//					echo '$sqlQuery= '.$sqlQuery.'<br />';
					// préparation de la transaction
					$qid = $cnxSetting->prepare($sqlQuery);
					// execute la requête
					$qid->execute();
					while ($row=$qid->fetch(PDO::FETCH_OBJ)){
						$profileName = $row->currentKeywordProfileName;
					}
					if ($DEBUG){ echo 'profileNameInput NON DEFINI: => Reprise nom profile courant dans SQL table filter: '.$profileName.'<br />'; }
				}
				
				// gestion ACTION à faire demandé par boutons 'submit':
				// Principe: 2 actions possibles sur boutons profile: Sauvegarde et Suppression
				// 1-Sauvegarde: bouton 'submit' name="profileSave"
				// mais la sauvegarde peut-être un UPDATE ou INSERT en fonction de l'<input>
				if (isset($_POST['profileSave'])) {	
					// filtrage du profile champ <input> vide
					if ($profileNameInput != ''){
						// determination si update ou ajout d'item:
						// on veut la liste des profiles
						// composition requête SQL
						if ($DEBUG){ echo "Submit via bouton 'Sauvegarder'<br />"; }
						$sqlQuery = "SELECT * FROM keyword_color_profile WHERE profilename='".$profileNameInput."';";
						if ($DEBUG){ echo '$sqlQuery= '.$sqlQuery.'<br />'; }
						// préparation de la transaction
						$qid = $cnxSetting->prepare($sqlQuery);
						// execute la requête
						$qid->execute();
						// Principe: test le compteur de ligne trouvée:
							// 0  -> profile non trouvé donc il faut INSERT
							// >0 -> profile trouvé donc il faut UPDATE
						if ($DEBUG){ echo 'Determination UPDATE(existe) ou INSERT(existe pas): <br />$qid->rowCount() = '.$qid->rowCount().'<br />'; }
						// ==== Profile non trouvé donc il faut INSERT
						if ($qid->rowCount() == 0){
							if ($DEBUG){ echo 'profile non trouvé donc il faut INSERT<br />'; }
							$profileAction = 'profileInsert';
							// ==== AJOUT dans 'keyword_color_profile' id en auto-incrément
							$sqlQuery = "INSERT INTO keyword_color_profile (profilename) VALUES ('".$profileNameInput."');";
							if ($DEBUG){ echo '$sqlQuery= '.$sqlQuery.'<br />'; }
							// préparation de la transaction
							$qid = $cnxSetting->prepare($sqlQuery);
							// execute la requête
							$qid->execute();
							// ==== LECTURE du nouvel 'id' du 'profile'
							$sqlQuery = "SELECT * FROM keyword_color_profile WHERE profilename='".$profileNameInput."';";
							if ($DEBUG){ echo '$sqlQuery= '.$sqlQuery.'<br />'; }
							// préparation de la transaction
							$qid = $cnxSetting->prepare($sqlQuery);
							// execute la requête
							$qid->execute();
							while ($row=$qid->fetch(PDO::FETCH_OBJ)){
								$id = $row->id;
							}
							if ($DEBUG){ echo 'le nouvel id de profile est : '.$id.'<br />';  }
							
							// ==== AJOUT dans 'keyword_color'
							$sqlQuery = "INSERT INTO keyword_color (`keywordProfile_id`, `keywordProfileName`, ";
							for ($i=1; $i<=$KEYWORD_MAXI - 1; $i++){		// boucle parametre check* keywordValue* keywordColor* 1->9
								$sqlQuery = $sqlQuery. "`keywordCheck".$i."`, `keywordValue".$i."`, `keywordColor".$i."`, ";
							}
							$sqlQuery = $sqlQuery. "`keywordCheck10`, `keywordValue10`, `keywordColor10` ";
							$sqlQuery = $sqlQuery. ") VALUES (".$id.", '".$profileNameInput."', ";
							// valeurs à enregistrer via submit:
							for ($i=1; $i<=$KEYWORD_MAXI - 1; $i++){		// boucle lecture paramètres POST jusque avant dernière ligne
								// gestion case à cocher = 'null' ou 'On' -> '' ou 'checked' ligne de 1 à 9
								if    (!isset($_POST["keywordCheck".$i])){ 
									  $_POST["keywordCheck".$i] = '';	}
								else{ $_POST["keywordCheck".$i] = 'checked';}
								$sqlQuery = $sqlQuery. 
											"'".$_POST["keywordCheck".$i]. "', ".
											"'".$_POST["keywordValue".$i]. "', ".
											"'".$_POST["keywordColor".$i]. "', ";
							}
							$i = $KEYWORD_MAXI;								// derniere ligne sans virgule en fin de ligne:
							// gestion case à cocher = 'null' ou 'On' -> '' ou 'checked' 10eme ligne
							if (!isset($_POST["keywordCheck".$i])){
									$_POST["keywordCheck".$i] = '';	}
							else{	$_POST["keywordCheck".$i] = 'checked'; }
							$sqlQuery = $sqlQuery. 
											"'".$_POST["keywordCheck".$i]. "', ".
											"'".$_POST["keywordValue".$i]. "', ".
											"'".$_POST["keywordColor".$i]. "');";
	/*						if ($DEBUG){ echo '$sqlQuery= '.$sqlQuery.'<br />'; }
							// préparation de la transaction
							$qid = $cnxSetting->prepare($sqlQuery);
							// execute la requête
							$qid->execute(); */
							
						}
						
						// ==== Profile trouvé donc il faut UPDATE
						else{
							if ($DEBUG){ echo 'profile trouvé donc il faut UPDATE<br />'; }
							$profileAction = 'prolileUpdate';
							$sqlQuery = "UPDATE keyword_color ".
											"JOIN keyword_color_profile ON keyword_color_profile.id = keyword_color.keywordProfile_id ".
										"SET ";
							for ($i=1; $i<=$KEYWORD_MAXI - 1; $i++){		// boucle lecture paramètres POST jusque avant dernière ligne
							// gestion case à cocher = 'null' ou 'On' -> '' ou 'checked'
							if    (!isset($_POST["keywordCheck".$i])){ 
								  $_POST["keywordCheck".$i] = '';	}
							else{ $_POST["keywordCheck".$i] = 'checked';}
							$sqlQuery = $sqlQuery. 
											"keywordCheck".$i."='".$_POST["keywordCheck".$i]. "', ".
											"keywordValue".$i."='".$_POST["keywordValue".$i]. "', ".
											"keywordColor".$i."='".$_POST["keywordColor".$i]. "', ";
							}
							$i = $KEYWORD_MAXI;								// derniere ligne sans virgule en fin de ligne:
							// gestion case à cocher = 'null' ou 'On'
							if (!isset($_POST["keywordCheck".$i])){
									$_POST["keywordCheck".$i] = '';	}
							else{	$_POST["keywordCheck".$i] = 'checked'; }
							$sqlQuery = $sqlQuery. 
											"keywordCheck".$i."='".$_POST["keywordCheck".$i]. "', ".
											"keywordValue".$i."='".$_POST["keywordValue".$i]. "', ".
											"keywordColor".$i."='".$_POST["keywordColor".$i]. "' ".
											"WHERE keyword_color_profile.profilename='".$profileNameInput."';";
						}
						// filtrage du profile 'aucun'
						if ($profileName != 'Aucun'){
							if ($DEBUG){ echo '$sqlQuery= '.$sqlQuery.'<br />'; }
							// préparation de la transaction
							$qid = $cnxSetting->prepare($sqlQuery);
							// execute la requête
							$qid->execute();
							//dirige le chargement vers page d'accueil 
							//if ( !$DEBUG){ header('Location: serial_sql_logger.php'); }
						}
					}	// $profileNameInput != ''
				}
				
				// 2-Suppression: bouton 'submit' name="profileDelete"
				elseif (isset($_POST['profileDelete'])) {
					// filtrage du profile champ <input> vide
					if ($profileNameInput != ''){
						if ($DEBUG){ echo "Submit via bouton 'Supprimer'<br />"; }
						$profileAction = 'Supprimer';
						// Principe: 
						// 1: lecture 'id' du 'profileName' sélectionné
						// 2: Suppression fiche 'keyword*' correspondant à 'id' du 'profile'
						// 3: Suppression fiche 'profileName'
						
						// ==== 1: lecture 'id' du 'profileName' sélectionné
						$sqlQuery = "SELECT * FROM `keyword_color_profile` ".
									"WHERE profilename='".$profileNameInput."';";
						if ($DEBUG){ echo '$sqlQuery= '.$sqlQuery.'<br />'; }
						// préparation de la transaction
						$qid = $cnxSetting->prepare($sqlQuery);
						// execute la requête
						$qid->execute();
						// lecture résultat SQL
						while ($row=$qid->fetch(PDO::FETCH_OBJ)){
							$profileNameId = $row->id;
						}
						if ($DEBUG){ echo 'id profile à supprimer= '.$profileNameId.'<br />'; }
						
						// ==== 2: Suppression fiche 'keyword*' correspondant à 'id' du 'profile'
						$sqlQuery = "DELETE FROM `keyword_color` WHERE
										keywordProfile_id=".$profileNameId.";";
						if ($DEBUG){ echo '$sqlQuery= '.$sqlQuery.'<br />'; }
						// préparation de la transaction
						$qid = $cnxSetting->prepare($sqlQuery);
						// execute la requête
						$qid->execute();
						
						// ==== 3: Suppression fiche 'profileName'
						$sqlQuery = "DELETE FROM `keyword_color_profile` WHERE
										profilename='".$profileNameInput."';";
						if ($DEBUG){ echo '$sqlQuery= '.$sqlQuery.'<br />'; }
						// préparation de la transaction
						$qid = $cnxSetting->prepare($sqlQuery);
						// execute la requête
						$qid->execute();
						// RESET champ de saisie:
						$profileNameInput = '';
					}
				}
				else{
					$profileAction = 'vide';
				}
				
				if ($DEBUG){ echo '<h3>nav='.$nav.'</h3>'; }
				if ($DEBUG){ echo '<p>profileName(url)='.$profileName.'</p>'; }
				if ($DEBUG){ echo '<p>profileNameInput='.$profileNameInput.'</p>'; }
				if ($DEBUG){ echo '<p>profileAction='.$profileAction.'</p>'; }
				
				?>
				<p><strong>Gestion des profiles:</strong> Les réglages de coloration peuvent être sauvegardés dans des profiles</p>
				<form class="form-inline" role="form" action="dashboard.php" method="POST">
					<label for="profile" class="hidden">Profile</label>
					<div class="input-group">
						<div class="input-group-btn">
							<button name="profileSelect" type="button" class="btn btn-primary dropdown-toggle" data-toggle="dropdown">
								<i class="icon-button ion-clipboard"></i> Sélection profile <span class="caret"></span>
							</button>
							<ul class="dropdown-menu">
								<!-- 1er  choix Profile: 'Aucun' -->
								<?php
									// ==== Sélection de 'Aucun' profile
									// affichage en gras de la table archive sélectionnée
									if ($profileName == 'Aucun') { $liClass = ' class="active"'; $boldOpen = '<b>'; $boldClose = '</b>'; }
									else 						 { $liClass = "";                $boldOpen = '';    $boldClose = '';		  }
									echo '<li'.$liClass.'><a href="dashboard.php?profileName=Aucun">'.$boldOpen.'Aucun'.$boldClose.'</a></li>';
									// Ligne de séparation
									echo '<li class="divider"></li>';
									// affichage en gras de la table archive sélectionnée
									// ==== on veut la liste des profiles
									// composition requête SQL
									$sqlQuery = "SELECT * FROM keyword_color_profile ORDER BY profilename ASC;";
									// préparation de la transaction
									$qid = $cnxSetting->prepare($sqlQuery);
									// execute la requête
									$qid->execute();
									// récup de l'extraction sql des catégories disponibles
									while ($row=$qid->fetch(PDO::FETCH_OBJ)){
										// affichage en gras de la table archive sélectionnée
										if (($row->profilename == $profileName) || ($row->profilename == $profileNameInput)){ 
											$liClass = ' class="active"'; $boldOpen = '<b>'; $boldClose = '</b>'; 
										}
										else{
											$liClass = "";                $boldOpen = '';    $boldClose = '';
										}
										echo '<li'.$liClass.'><a href="dashboard.php?profileName='.$row->profilename.'">'.$boldOpen.$row->profilename.$boldClose.'</a></li>';
										//echo '<li><button type="submit" <a href="dashboard.php'.$row->profilename.'">'.$row->profilename.'</a></button></li>';
									}
								?>
							</ul>
						</div>
						<?php
						
						if ($profileName!=''){
							if ($profileName == 'Aucun'){
								$profileNameValue = '';
							}
							else{
								$profileNameValue = $profileName;
							}
						}
						else{
							$profileNameValue = $profileNameInput;
						}
							echo '<input  name="profileNameInput"  value="'.$profileNameValue.'" id="profile" type="text" class="form-control profilevalue col-md-6" id="profileName" placeholder="Nom du profile">';
						?>
						<!--	<input  name="nav"  type="hidden" value="2"> -->
					</div>
						<button name="profileSave"   type="submit" class="btn btn-primary"><i class="icon-button ion-checkmark-circled" ></i> Sauvegarder</button>
						<button name="profileDelete" type="submit" class="btn btn-primary"><i class="icon-button ion-trash-b"></i> Supprimer</button>
						<br />
						<br />
	<!--			</form>
				<br />
				<p><strong>Edition du surlignage:</strong> Paramètrage des mots clés et couleurs associées:</p>
				<form action="php/setting.php" method="POST" name="keywordColorForm">		-->
					<table>
						<input type="hidden" name="setting" value="SetKeywordColor"/>
						<?php
							// composition requête SQL
							// si sélection 'Aucun'
							if ($profileName == 'Aucun'){
								$sqlQuery = "SELECT * FROM keyword_color WHERE id=0;";
							}
							// sinon 
							// on veut les mots clés et couleurs:
							else{
								$sqlQuery = "SELECT * 
											 FROM keyword_color INNER JOIN keyword_color_profile ON keyword_color_profile.id = keyword_color.keywordProfile_id 
											 WHERE keyword_color_profile.profilename = '$profileNameValue'";
							}
							// préparation de la transaction
							$qid = $cnxSetting->prepare($sqlQuery);
							// execute la requête
							$qid->execute();
							// récup de l'extraction sql
							while ($row=$qid->fetch(PDO::FETCH_OBJ)){
								for ($i=1; $i<=$KEYWORD_MAXI; $i++){
									echo '<tr>';
										// constuction nom champ pour extraction SQL:
										$keywordCheckIdx = 'keywordCheck'.$i;
										$keywordValueIdx = 'keywordValue'.$i;
										$keywordColorIdx = 'keywordColor'.$i;
										echo '<td class="colorId">'.$i.'</td>';
										echo '<td><input '.$row->$keywordCheckIdx.' type="checkbox" 
														data-toggle="toggle" name="keywordCheck'.$i.'"></td>';
										echo '<td><input type="text" class="form-control colorKey"            name="keywordValue'.$i.
														'" placeholder="Mot clé " value="'.$row->$keywordValueIdx.'"></td>';
										echo '<td><input type="text" class="form-control colorCode"           name="keywordColor'.$i.
														'" id="colorCode'.$i.'"  placeholder="Code couleur" value="'.$row->$keywordColorIdx.'"></td>';
										echo '<td>';
											AUX::CallPalette($i, $row->$keywordColorIdx);
										echo '</td>';
									echo '</tr>';
								}
							}
						?>
					</table>
				<!--	<div class="spacer"></div>	-->
	<!--				<br />
					<button type="submit" class="btn btn-success">Valider</button>		-->
				</form>

		<!--		<a tabindex="0" class="btn btn-lg btn-danger" role="button" data-toggle="popover" data-trigger="focus" title="Dismissible popover" data-content="And here's some amazing content. It's very engaging. Right?">Dismissible popover</a>   -->

			<?php
			}
			
			
			//===========================================
			//======== nav2: Largeur des colonne ========
			//===========================================
			if ($nav == 2) {
				echo '<p>Réglages de la largeur des colonnes:</p>';
				// on veut les largeurs courantes des 15 colonnes:
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
				// déinition des labels des sliders
				$colSetLabel[1] = 'Marqueur (30)';
				$colSetLabel[2] = 'Horodatage (150)';
				$colSetLabel[3] = 'Catégorie (100)';
				$colSetLabel[4] = 'Détail (60)';
				$colSetLabel[5] = 'Message';
				for ($i=6; $i<16; $i++)	$colSetLabel[$i] = 'Largeur colonne '.$i; ?>
				<!-- FORMULAIRE setting=SetColSize UPDATE COLUMN SIZE -->
				<form action="php/setting.php" method="POST" name="formulaire">
					<table>
						<input type="hidden" name="setting" value="SetColSize"/>
						<?php for ($i=1; $i<16; $i++){
							echo '<tr><td class="td-col-id">'.$colSetLabel[$i].'</td>'; ?>
								<td>
									<?php echo '<input class="td-col-value" type="text" id="col-value'.$i.'" name="col-value'.$i.'" value="'.$colGetSize[$i].'">'; ?>
								</td>
								<td>
									<?php echo'<div id="col-slider'.$i.'" class="td-col-slider ui-slider ui-slider-horizontal ui-widget ui-widget-content ui-corner-all">'; ?>
									<span class="ui-slider-handle ui-state-default ui-corner-all" tabindex="0" style="left: 4%;"></span></div>
								</td>
							</tr>
						<?php } ?>
					</table>
				<button type="submit" class="btn btn-success">Valider</button>
				</form>
			<?php } ?>
		</section>
		<footer>
			Visionneuse de log SQL - 2015
		</footer>
		<!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
		<script src="assets/js/jquery-1.11.2.min.js" type="text/javascript"></script>
		<!-- Include all compiled plugins (below), or include individual files as needed -->
		<script src="dist/js/bootstrap.min.js" type="text/javascript"></script>
		<!-- Liaisons aux fichiers css de Bootstrap-toggle -->
		<script src="dist/js/bootstrap-toggle.min.js"></script>
		
		<script type="text/javascript" src="assets/jquery-ui-1.11.4.custom/jquery-ui.js"></script>
		<script src="js/dashboard.js"></script>
	</body>
</html>
