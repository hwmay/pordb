# -*- coding: utf-8 -*-
from pyPgSQL import PgSQL

import glob
import string
import sys
import os

if len(sys.argv) > 1:
	cd_string = sys.argv[1]
	try:
		cd = int(cd_string)
	except:
		print "CD-Nummer ist falsch"
		sys.exit()
else:
	cd = 0

cx = PgSQL.connect(database='por')
dbname = 'por'

# Make a connection to the database and check to see if it succeeded.
try:
    cnx = PgSQL.connect(database=dbname)
except PgSQL.Error, msg:
    print "Connection to database '%s' failed" % dbname
    print msg,
    sys.exit()

cur = cnx.cursor()

zu_lesen = "select * from vid"
try:
	cur.execute(zu_lesen)
except PgSQL.Error, msg:
	message = QtGui.QMessageBox.critical(self, "Fehler ", str(msg))
	sys.exit()
try:
	res = cur.fetchall()
except StandardError, msg:
	message = QtGui.QMessageBox.critical(self, "Fehler ", str(msg))
	sys.exit()
for i in res:
	#print i, "CS= ", res[0][6]
	if i[6] == "f":
		zu_aendern = "update vid set csf = 1 where primkey = '" +str(i[8]) +"'"
	elif i[6] == "h":
		zu_aendern = "update vid set csh = 1 where primkey = '" +str(i[8]) +"'"
	elif i[6] == "t":
		zu_aendern = "update vid set cst = 1 where primkey = '" +str(i[8]) +"'"
	elif i[6] == "c":
		zu_aendern = "update vid set csc = 1 where primkey = '" +str(i[8]) +"'"
	elif i[6] == "x":
		zu_aendern = "update vid set csx = 1 where primkey = '" +str(i[8]) +"'"
	elif i[6] == "o":
		zu_aendern = "update vid set cso = 1 where primkey = '" +str(i[8]) +"'"
	elif i[6] == "v":
		zu_aendern = "update vid set csv = 1 where primkey = '" +str(i[8]) +"'"
	elif i[6] == "b":
		zu_aendern = "update vid set csb = 1 where primkey = '" +str(i[8]) +"'"
	elif i[6] == "a":
		zu_aendern = "update vid set csa = 1 where primkey = '" +str(i[8]) +"'"
	elif i[6] == "s":
		zu_aendern = "update vid set css = 1 where primkey = '" +str(i[8]) +"'"
	else:
		zu_aendern = "update vid set csk = 1 where primkey = '" +str(i[8]) +"'"
	print zu_aendern
	try:
		cur.execute(zu_aendern)
	except PgSQL.Error, msg:
		print msg
		
	cnx.commit()
