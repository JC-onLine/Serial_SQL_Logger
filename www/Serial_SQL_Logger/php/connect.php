<?php
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

	// base de données appli
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
?>
