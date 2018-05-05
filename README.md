# studienarbeit_playground
Hier können Dinge vorab versioniert werden, welche eventuell später umgeordnet werden.

# ACHTUNG

## Wir nutzen Python 3.5.2 (+) und Tensorflow "tensorflow-1.6.0" 

Die Pfadangaben müssen dem Nutzer angepasst werden, eventuell diese auslagern und dann mit gitignore erhalten lassen.


# Howto Install TF mit GPU support

* Als erstes am besten Anaconda downloaden
* Dann installieren und eine Umgebung erstellen. Dort Tensorflow und tensorflow-gpu inkl. Abhängigkeiten installieren.
* Dieses Repo zum Testen downloaden
* Beim nutzen von Tensorflow sollten bei Nutzung der GPU anzeigen im Log über Taktrate und Speicher stehen. + Es geht deutlich schneller!
* Sollte keine anzeige oder ein Fehler erscheinen Fehlen Pakete

Wichtige Pakete sind:
* cuda v8.0 (nicht 9.0 oder 9.1!)
* cudnn-8.0 v5.1 (nicht die neuste Version)
* aktueller Treiber (cuda version is insufficient - Fehler beim Ausführen)


## Todo

* Erstellung Abbildungen Wie funktionieren layer,etc
* erstellung tabelle lerndauerr pro datensatz
* Erstellung Vergleich genauigkeit
* Erstellung Datensatz pipeline wie funktioniert es (test/train vs predict, labels, etc. input fn
* Todonotes in der Studienarbeit abarbeiten
* Fehlene Texte Schreiben besonders ABstract, Fazit, Ausblick, Motivation (umformulieren), Tensorflow und Website fertig schreiben und neu lesen
