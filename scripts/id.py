#!/usr/bin/env python3
"""Stampa l'ID (o l'ARN) di una risorsa del progetto, letto da `agentcore status --json`.

Uso (dalla cartella del progetto TelcoCare):
    python3 ../scripts/id.py runtime            # ID del Runtime
    python3 ../scripts/id.py memory             # ID della Memory
    python3 ../scripts/id.py gateway --arn      # ARN del Gateway
    python3 ../scripts/id.py evaluator          # ID del valutatore

L'ID è l'ultima parte dell'ARN, quella dopo l'ultima barra.
"""
import argparse
import json
import subprocess
import sys


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("tipo", help="runtime, memory, gateway, policy-engine, evaluator, online-eval, harness")
    p.add_argument("--nome", help="nome della risorsa nel progetto, se ce n'è più di una")
    p.add_argument("--arn", action="store_true", help="stampa l'ARN completo invece dell'ID")
    a = p.parse_args()

    uscita = subprocess.run(["agentcore", "status", "--json"], capture_output=True, text=True)
    try:
        stato = json.loads(uscita.stdout)
    except json.JSONDecodeError:
        sys.exit("agentcore status --json non ha restituito JSON:\n" + uscita.stdout + uscita.stderr)

    trovate = [
        r for r in stato.get("resources", [])
        if r.get("resourceType") == a.tipo and (a.nome is None or r.get("name") == a.nome) and r.get("arn")
    ]
    if not trovate:
        sys.exit(f"nessuna risorsa deployata di tipo {a.tipo}: hai fatto agentcore deploy?")
    arn = trovate[0]["arn"]
    print(arn if a.arn else arn.split("/")[-1])


if __name__ == "__main__":
    main()
