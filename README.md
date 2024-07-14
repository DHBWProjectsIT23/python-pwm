![Main Status](https://img.shields.io/badge/Main%20Brach-Status-blue)
![MyPy Badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/DefinitelyNotSimon13/328c50761ab662216df5dfb1debb334a/raw/mypy_warnings.json)
![Pylint Badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/DefinitelyNotSimon13/328c50761ab662216df5dfb1debb334a/raw/pylint-score.json)
![Coverage Badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/DefinitelyNotSimon13/328c50761ab662216df5dfb1debb334a/raw/coverage.json)


# 3 Hauptmodule?!

1. TUI mit curses
    - Gedanken machen wie aufgebaut -> Alle Anforderungen mit einbinden/erweiterbarkeit
    - Am besten wsl vorher mal aufzeichnen
    - Umsetzung mit Curses - gute UX
2. cryptography, verschlüsseln, entschlüsseln, ...
3. Have I been pwned? API
    - Asynchronous

Nebenbei:
- CI mit mypy, pylint, coverage fixen
- Anforderungen auf Github packen
- Sichergehen dass Tests stehen
- Sichergehen dass die Dokumentation steht
# Hauptaufgabe
- TUI - Simon
  - Wie aufgebaut? Alle Requirements beachten
  - Vorher maybe aufzeichnen o.Ä.
  - Implementierung in Curses

- Cryption
  - Submodules
    - Verschlüsselung/Enschlüsselung - Gekapselt
    - Passwortspeichern
    - Passowrtgenerieren - Gekapselt
    - Passwortabruf 
    - Passwortbearbeitung 
    - Master Passowrt
    - Passwortüberprüfung - Gekapselt
    - Nutzermanagement
  - Zuerst Grundlagen - Max
  - Recharchieren, was für eine Art verschlüsselung etc

- HaveIBeenPwned API - Gekapselt - Ruth
  - Async
 
# Nebenaufgaben
- Requirements auf Github packen
- CI fixen (mypy, coverage, unittest)
- Tests schreiben
- Dokumentation schreiben
