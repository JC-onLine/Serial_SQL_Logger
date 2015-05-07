// Description:	Fichier code.js du projet Serial_SQL_Logger.
// 2015-03-18 :	Création.


function SelectionCouleur(idKeyword, codeCouleur){
	// renvoie le code couleur selectionné dans le champ de saisie colorCodeXX
	$("#colorCode"+idKeyword).val(codeCouleur);
	// colorie le bouton de palatte avec la couleur selectionnée
	document.getElementById("idColorVisu"+idKeyword).style.background = codeCouleur;
}


//window.onload = function(){
$(function() {
	$( "keywordcolorform" ).submit(function( event ) {
		if ( $( "input:first" ).val() === "correct" ) {
			$( "span" ).text( "Validated..." ).show();
			return;
		}
		$( "span" ).text( "Not valid!" ).show().fadeOut( 1000 );
			event.preventDefault();
		});
	
	// scan les sliders pour rafraichissement des valeurs dans les champs de saisie
	$( "#col-slider1" ).slider({
		range:	"min",
		min: 	0,
		max: 	1000,
		value:	$("#col-value1").val(),
		slide: 	function( event, ui ) {
					$("#col-value1").val( ui.value );
		}
	});
	$("#col-slider2").slider({
		range: 	"min",
		min: 	0,
		max: 	1000,
		value:	$("#col-value2").val(),
		slide: 	function( event, ui ) {
					$( "#col-value2" ).val( ui.value );
		}
	});
	$( "#col-slider3" ).slider({
		range:	"min",
		min: 	0,
		max: 	1000,
		value:	$("#col-value3").val(),
		slide: 	function( event, ui ) {
					$( "#col-value3" ).val( ui.value );
		}
	});
	$( "#col-slider4" ).slider({
		range:	"min",
		min:	0,
		max:	1000,
		value:	$("#col-value4").val(),
		slide: 	function( event, ui ) {
					$( "#col-value4" ).val( ui.value );
		}
	});
	$( "#col-slider5" ).slider({
		range:	"min",
		min:	0,
		max:	1000,
		value:	$("#col-value5").val(),
		slide: 	function( event, ui ) {
					$( "#col-value5" ).val( ui.value );
		}
	});
	$( "#col-slider6" ).slider({
		range:	"min",
		min:	0,
		max:	1000,
		value:	$("#col-value6").val(),
		slide:	function( event, ui ) {
					$( "#col-value6" ).val( ui.value );
		}
	});
	$( "#col-slider7" ).slider({
		range:	"min",
		min:	0,
		max:	1000,
		value:	$("#col-value7").val(),
		slide:	function( event, ui ) {
					$( "#col-value7" ).val( ui.value );
		}
	});
	$( "#col-slider8" ).slider({
		range:	"min",
		min:	0,
		max:	1000,
		value:	$("#col-value8").val(),
		slide:	function( event, ui ) {
					$( "#col-value8" ).val( ui.value );
		}
	});
	$( "#col-slider9" ).slider({
		range:	"min",
		min:	0,
		max:	1000,
		value:	$("#col-value9").val(),
		slide:	function( event, ui ) {
					$( "#col-value9" ).val( ui.value );
		}
	});
	$( "#col-slider10" ).slider({
		range:	"min",
		min:	0,
		max:	1000,
		value:	$("#col-value10").val(),
		slide:	function( event, ui ) {
					$( "#col-value10" ).val( ui.value );
		}
	});
	$( "#col-slider11" ).slider({
		range:	"min",
		min:	0,
		max:	1000,
		value:	$("#col-value11").val(),
		slide:	function( event, ui ) {
					$( "#col-value11" ).val( ui.value );
		}
	});
	$( "#col-slider12" ).slider({
		range:	"min",
		min:	0,
		max:	1000,
		value:	$("#col-value12").val(),
		slide:	function( event, ui ) {
					$( "#col-value12" ).val( ui.value );
		}
	});
	$( "#col-slider13" ).slider({
		range:	"min",
		min:	0,
		max:	1000,
		value:	$("#col-value13").val(),
		slide:	function( event, ui ) {
					$( "#col-value13" ).val( ui.value );
		}
	});
	$( "#col-slider14" ).slider({
		range:	"min",
		min:	0,
		max:	1000,
		value:	$("#col-value14").val(),
		slide:	function( event, ui ) {
					$( "#col-value14" ).val( ui.value );
		}
	});
	$( "#col-slider15" ).slider({
		range:	"min",
		min:	0,
		max:	1000,
		value:	$("#col-value15").val(),
		slide:	function( event, ui ) {
					$( "#col-value15" ).val( ui.value );
		}
	});

// pour afficher au démarrage, la valeur du slider
//	$( "#col-value2").val($("#col-slider2").slider("value") );
});



function ValidSQL(){
	bootbox.confirm("Are you sure?", function(result) {
		Example.show("Confirm result: "+result);
	}); 
}

