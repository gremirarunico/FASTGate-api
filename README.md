# README.md
For english version go down. I written this readme in italian firs because this plugin is for the router FASTGate by Fastweb used in GPON connection (until 2.5 GB/s) in Italy.

## Premessa
Questa libreria serve a fornire una API in python per comandare via CLI il router FASTGate.

Questa libreria è stata testata con un FASTGate alla seguente versione

| Versione |           Numero           |
|----------|----------------------------|
| software | 1.0.1b                     |
| firmware | 18.3.n.0466_FW_227_FGA2130 |
| hardware | GBNT-2                     |

## Utilizzo
Visto che il codice è meglio di 1000 parole, un esempio di codice commentato per l'uso della libreria

    #!/usr/bin/python3

    import FASTGate

    # Configuro username e password
    myFast = FASTGate("username", 'password')

    # Facoltativo, mostra a schermo tutti i passaggi della libreria
    myFast.verbose = 1

    # Inizializza la connessione
    myFast.connect()

    # Cerca una sessione precedente (viene di default salvata in ""~/FASTGateSession.json"), per cambiare la directory vedere myFast.sessionFile
    # Attenzione che se effettuate troppi login (cioè non caricate la sessione), verrete bannati dal FASTGate. Per risolvere sarà sufficiente riavviare il router.
    myFast.load()

    # Controlla se si è già collegati. Ritorna True se loggato False altrimenti
    # myFast.isLogged()

    # Effettua il login, ritorna True se ha avuto successo False altrimenti
    myFast.smartLogin()

    # Ottiene informazioni (quelle che si ottengono dalla pagina informazioni), ritorna un dizionario
    myFast.info()

    # Effettua un reboot del router, ritorna True se ha avuto successo False altrimenti
    myFast.reboot()

    # Salva lo stato della sessione, lanciarlo sempre per ultimo, la salva in myFast.sessionFile
    myFast.save()

    # myFast.logout()

## Eccezioni
La libreria lancia l'eccezione `ConnectionError` nel caso in cui ci sia un errore di connessione. Una delle cause più probabili è che siate stati bannati dal router;

## Altri metodi
Non sono stati mostrati tutti i metodi della libreria, ma solo quelli che possono essere utili. Per maggiori informazioni aprire la libreria (è moltro breve e il codice è autodocumentato).

## Dipendenze
Tra le dipendenze non generalmente installate di default c'è
* requests
