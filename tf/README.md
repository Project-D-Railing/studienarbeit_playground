# Howto SQL

Alle Züge holen ohne die Stationsnummer am Ende. Damit kann man die nächsten Abgagen vereinfachen.

`SELECT Distinct(SUBSTRING_INDEX(SUBSTRING(zugid FROM 2), '-', 2)) FROM \`zuege2\``

Abfrage aller Haltestellen auf einer Zugfahrt

`SELECT haltestellen2.name FROM zuege2,haltestellen2 where zuege2.evanr=haltestellen2.eva_nr AND zugid like '%6957575484712982863-1711301729%'"`