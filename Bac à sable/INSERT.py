# -*- coding: utf-8 -*-

# gestion MySQL
import MySQLdb

print "base MySQL connexion..."
try:
	db = MySQLdb.connect(host='192.168.1.150',user='root',passwd='mysql',db='serial_sql_logger')
except Exception:
	print "Erreur connexion MySQL en 192.168.1.150"
else:
	print "base MySQL ouverte"
	cur = db.cursor() 
	requete="INSERT INTO arduino (horodatage,categorie,niv_detail,message) VALUES ('2014-09-22 10:00:28','robot2','1','Hello Cubietruck !')"
	try:
		# execute la requete
		cur.execute(requete)
		print "...Mise a jour de la base"
		db.commit()
	except Exception:
		print "Erreur avec la Requete= " + requete
		print "...Retour etat precedant de la base"
		db.rollback()
	else:
		print "Requete executee"
		db.close()
		print "base fermee"
