import MySQLdb

conn = MySQLdb.connect (host = "localhost",
					   user = "root",
					   passwd = "",
					   db = "serial_sql_logger")
cursor = conn.cursor ()
requete="INSERT INTO arduino (horodatage,categorie,niv_detail,message) VALUES ('2014-09-22 10:00:20','robot1','1','Message1')"
cursor.execute (requete)
#row = cursor.fetchone ()
#print "server version:", row[0]
cursor.close ()
conn.close ()
