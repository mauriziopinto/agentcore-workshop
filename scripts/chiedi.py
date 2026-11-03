#!/usr/bin/env python3
"""Manda una domanda all'agente TelcoCare e stampa la risposta in modo leggibile.

Uso (dalla cartella del progetto TelcoCare):
    python3 ../scripts/chiedi.py --utente anna --sessione uno "Ciao, sono Anna"
    python3 ../scripts/chiedi.py --locale "Ciao"          # agente in locale (agentcore dev --port 8181)

Lo script costruisce il payload JSON (così gli apostrofi non rompono la shell),
stampa il comando `agentcore invoke` che esegue e filtra la risposta in streaming.
Lo stesso nome di sessione, con lo stesso utente, dà sempre lo stesso ID di sessione.
"""
import argparse
import json
import os
import shlex
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import leggi  # noqa: E402


def id_sessione(utente: str, sessione: str) -> str:
    # AgentCore Runtime vuole ID di sessione di almeno 33 caratteri.
    base = f"telcocare-{utente}-{sessione}-"
    return base + "0" * max(0, 40 - len(base))


def main() -> None:
    p = argparse.ArgumentParser(description="Domanda all'agente TelcoCare")
    p.add_argument("domanda", nargs="?", help="il testo da mandare all'agente")
    p.add_argument("--utente", default="default", help="chi sta scrivendo (actorId per la Memory)")
    p.add_argument("--sessione", default="uno", help="nome breve della conversazione")
    p.add_argument("--locale", action="store_true", help="usa l'agente in locale (agentcore dev)")
    p.add_argument("--porta", default="8181", help="porta dell'agente locale (default 8181, la 8080 è di Code Editor)")
    p.add_argument("--solo-id", action="store_true", help="stampa solo l'ID di sessione, senza chiamare l'agente")
    a = p.parse_args()

    if a.solo_id:
        print(id_sessione(a.utente, a.sessione))
        return
    if not a.domanda:
        p.error("manca la domanda")

    payload = json.dumps({"prompt": a.domanda, "actorId": a.utente}, ensure_ascii=False)
    comando = ["agentcore", "invoke", "--runtime", "agent", "--payload", payload]
    if a.locale:
        comando += ["--local", "--port", a.porta]
    else:
        comando += ["--session-id", id_sessione(a.utente, a.sessione)]

    print("[comando] " + " ".join(shlex.quote(c) for c in comando))
    print()
    proc = subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    sys.stdin = proc.stdout
    leggi.main()
    sys.exit(proc.wait())


if __name__ == "__main__":
    main()
