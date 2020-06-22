# Setup
## Hinweis
- Die Anleitung bezieht sich auf einen Computer mit Windows 10
- Die Versionsnummern beziehen sich auf die beim Prototyp verwendeten Versionen

## Anforderungen
- `OpenJDK 13.0.2` und `Node.JS (Version 12.15.0)` mit `NPM (Version 6.13.4)` müssen installiert sein
- Entwicklungsumgebung, wie beispielsweise IntelliJ, muss installiert sein
- Bei `ngrok.com` muss ein Account angelegt und die Software muss heruntergealden werden
- Bei der Amazon Developer Console muss ein Account angelegt werden und das `Alexa Service Kit Command Line Interface (ASK CLI Version 1.7.23)` muss installierst und initialisiert werden
- GIT muss installiert sein

## Vorbereitung
Den Ordner `camunda-spring-boot` mit IntelliJ öffnen. Es handel sich dabei um ein Maven-Projekt. Alle erforderlichen Imports importieren und die`Open JDK 13 JRE` zum Ausführen des Codes konfigurieren. Anschließend kann die Spring-Boot-Applikation gestartet werden.

Im Ordner `external` die PowerShell öffnen und den Befehl `npm install` ausführen.

In der Alexa Developer Console (developer.amazon.com/alexa/console/ask) müssen fünf custom Skills (alexa-hosted) angelegt werden. Diese können den gleichen Namen wie die Skills im Ordner `alexa-skills` haben.

Nach dem Erstellen der Skills kann im JSON Editor des jeweiligen Skills die Datei aus dem Ordner `thesis-prototyp/alexa-skills/[skill-name]/models/de_DE.json` kopiert werden. Anschließend auf "save model" und dann auf "build model" klicken.  Dann zum "code"-Reiter wechseln. Die Datei aus dem Ordner `thesis-prototyp/alexa-skills/[skill-name]/lambda/lambda_function.py` kopieren und bei Code einfügen. Anschließend auf "save" und "deploy" klicken.

## Benachrichtigungen aktivieren
Den Inhalt des Ordners `alexa-skills` löschen. Ein PowerShell Fenster in diesem Ordner öffnen und `ask clone` ausführen. Mit diesem Befehl alle zuvor angelegten Skills herunterladen.

Um Benachrichtigungen zu ermöglichen, müssen die drei Skills "aufgaben anna", "aufgaben felix" und "aufgaben julian" konfiguriert werden. Dafür in einem Editor die Datei `thesis-prototyp/alexa-skills/[skill-name]/skill.json` öffnen. Unterhalb von "manifestVersion" folgenden Code-Schnipsel einfügen:
```
"manifestVersion": 1.0,
"permissions" : [
    {
        "name": "alexa::devices:all:notificatoins:write"
    }
],
"events": {
    "endpoint": {
        "uri" "arn:aws:lambda:........."
    },
    "publications": {
        {
            "eventName": "AMAZON.MessageAlert.Activated"
        }
    }
}
```
Der Eintrag bei "uri" kann von 
```
"manifest": {
    "apis": {
      "custom": {
        "endpoint": {
          "uri": "......."
        },
        "interfaces": []
      }
    },
```
kopiert werden. Anschließend ein PowerShell Fenster öffnen und die Änderungen mit mit GIT stagen, commiten und pushen. Daraufhin den Befehl `ask deploy` für jeden der drei Skills ausführen. Anschließend zur Alexa Developer Console wechseln. Innerhalb der drei Skills im Reiter "Build" ganz unten "Permissions" auswählen und auf der entsprechenden Seite ganz unten die bei Alexa Skill Messaging die Alexa Client Id und das Alexa Client Secret kopieren und in die Datei `thesis-prototyp/external/external.js` an der entsprechenden Stelle einfügen.
```
const felixSkillSecret = {
    'client_id': 'amzn1.application-oa2-client.XXXXXXXXXXXXXXXXXXXXXX',
    'client_secret': 'XXXXXXXXXXXXXXXXXXXXXX'
}
const annaSkillSecret = {
    'client_id': 'amzn1.application-oa2-client.XXXXXXXXXXXXXXXXXXXXXX',
    'client_secret': 'XXXXXXXXXXXXXXXXXXXXXX'
}
const julianSkillSecret = {
    'client_id': 'amzn1.application-oa2-client.XXXXXXXXXXXXXXXXXXXXXX',
    'client_secret': 'XXXXXXXXXXXXXXXXXXXXXX'
}
```
Anschließend ein PowerShell-Fenster im Ordner `thesis-prototyp/external` öffnen und das Skript mit `node.exe external.js` starten. Das Skript abonniert darufhin vier verschiedene Themen und kann entsprechende Nachrichten an einzelne Skills versenden.

## Alles starten
Die Spring-Boot Appliaktion starten.

Den Installationsordner von ngrok öffnen. Ein PowerShell-Fenster öffnen und `ngrok.exe http 8080` eingeben. Damit wird ngrok gestartet. Die HTTPS-URL kopieren.

Ein PowerShell-Fenster im Ordner `thesis-prototyp/alexa-skills` öffnen und `setup.ps1 [URL]` ausführen. Dieser speichert die URL in den einzelnen Skills.

Nun kann mit Alexa kommuniziert werden und Benachrichtugnen werden verschickt. Das `thesis-prototyp/alexa-skills/test.ps1` Skript kann ausgeführt werden, um zu testen, ob alle Interaktionen funktionieren. Um die Nachrichten zu erhalten müssen auf dem entsprechenden Alexa-Gerät die Benachrichtigungen in den Skill Einstellungen aktiviert werden.