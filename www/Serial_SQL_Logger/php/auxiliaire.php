<?php
/*! 
 *  \brief     Gesion des fonctions auxiliaires
 *  \details   Permet de centraliser les fonctions
 *  \author    JC
 *  \pre       Centralisation des fonctions
 *  \warning   Ne pas oublier cette class avant d'afficher un profile dashboard
 *  \version   1.0
 *  \date      2015-04-04	Création
 */
class AUX{
	
	static function CallPalette($idKeyword, $colorCode){
	/**
	 * Principe		:	Permet d'afficher une palette 4x4 
	 * 						et donne le code couleur séléctionné
	 * 					Dessinne un bouton d'appelle palette, 
	 * 						celui-ci prend la couleur sélectionnée
	 * Paramètres	:	id de la couleur et son code correspodant
	 * Retour		:	Retourne dans input text id="codeCouleurXX" le code au format #FF0000
	 * Dependance	:	Id de l'input text
	 * 2015-03-25	:	Création
	 * 2015-03-26	:	Ajout paramètres id + code couleur
	 * 2015-04-04	:	Déplacement fonction dans la class AUX
	 * */
	?>
	<div class="btn-group"> 
		<?php echo '<button class="btn btn-default dropdown-toggle bnt-call-palette'.$idKeyword.'" data-toggle="dropdown" id="idColorVisu'.$idKeyword.'"  style="background:'.$colorCode.'"><i class="ion-android-color-palette"></i></button>'; ?>
			<ul class="dropdown-menu">
				<table class="palette">
					<?php
					// tableau correspondance id / code couleur
					$codeBkgColor = array(17);
					$codeTxtColor = array(17);
					$codeBkgColor[ 1] = '#FF0000';	$codeTxtColor[ 1] = '#000000';
					$codeBkgColor[ 2] = '#808000';	$codeTxtColor[ 2] = '#000000';
					$codeBkgColor[ 3] = '#FFFF00';	$codeTxtColor[ 3] = '#000000';
					$codeBkgColor[ 4] = '#008000';	$codeTxtColor[ 4] = '#000000';
					$codeBkgColor[ 5] = '#00FF00';	$codeTxtColor[ 5] = '#000000';
					$codeBkgColor[ 6] = '#008080';	$codeTxtColor[ 6] = '#000000';
					$codeBkgColor[ 7] = '#00FFFF';	$codeTxtColor[ 7] = '#000000';
					$codeBkgColor[ 8] = '#0000FF';	$codeTxtColor[ 8] = '#FFFFFF';
					$codeBkgColor[ 9] = '#800080';	$codeTxtColor[ 9] = '#000000';
					$codeBkgColor[10] = '#FF00FF';	$codeTxtColor[10] = '#000000';
					$codeBkgColor[11] = '#2B00FF';	$codeTxtColor[11] = '#000000';
					$codeBkgColor[12] = '#800000';	$codeTxtColor[12] = '#FFFFFF';
					$codeBkgColor[13] = '#666666';	$codeTxtColor[13] = '#000000';
					$codeBkgColor[14] = '#999999';	$codeTxtColor[14] = '#000000';
					$codeBkgColor[15] = '#CCCCCC';	$codeTxtColor[15] = '#000000';
					$codeBkgColor[16] = '#FFFFFF';	$codeTxtColor[16] = '#000000';
					// init index n° couleur palette
					$id=1;
					for ($ligne=1; $ligne<=4; $ligne++){
						echo '<tr>';
						for ($colonne=1; $colonne<=4; $colonne++){
							//echo '<td id="color'.$i.'" class="td-palette palette-color'.$i.'"><p><a href="#"> </p></a></td>';
							// affiche icone de la couleur selectionnée:
							if ($codeBkgColor[$id] == $colorCode){
								$colorSelected = '<i class="ion-checkmark-round"></i>';
							}
							else {
								$colorSelected = '';
							}
							echo '<td id="color'.$id.'" class="td-palette palette-color'.$id.'" bgcolor="'.$codeBkgColor[$id].'" onclick="SelectionCouleur('.$idKeyword.', \''.$codeBkgColor[$id].'\');"><font color="#000000"> '.$colorSelected.' </td>';
							//echo '<input type="submit" name="boutonValider" id="boutonValider" VALUE="Valider" onclick="fonctionValider()"/>';
							$id++;
						}
						echo '</tr>';
					} ?>
				</table>
			</ul>
	</div>
	<?php
	}



}	// fin de la class
?>
