# studienarbeit_playground
Hier können Dinge vorab versioniert werden, welche eventuell später umgeordnet werden.

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