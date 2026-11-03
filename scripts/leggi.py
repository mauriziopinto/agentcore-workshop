#!/usr/bin/env python3
"""Rende leggibile la risposta in streaming di `agentcore invoke`.

Uso:
    agentcore invoke --runtime agent --payload '{"prompt":"..."}' 2>&1 | python3 ../scripts/leggi.py

Stampa il testo della risposta e, su righe separate, gli strumenti che l'agente
ha chiamato. Le righe che non riconosce (errori, riepilogo finale) le stampa così come sono.
"""
import json
import sys


def main() -> None:
    in_testo = False
    for riga in sys.stdin:
        riga = riga.rstrip("\n")
        if not riga.startswith("data: "):
            if riga.startswith("status="):
                campi = dict(p.split("=", 1) for p in riga.split() if "=" in p)
                if in_testo:
                    print()
                    in_testo = False
                print(f"[sessione] {campi.get('runtime-session-id', '-')}  [http] {campi.get('status', '-')}")
            elif riga.strip():
                if in_testo:
                    print()
                    in_testo = False
                print(riga)
            continue
        try:
            dato = json.loads(riga[len("data: "):])
        except json.JSONDecodeError:
            print(riga[len("data: "):])
            continue
        if isinstance(dato, str):
            print(dato)
            continue
        evento = dato.get("event", {}) if isinstance(dato, dict) else {}

        inizio = evento.get("contentBlockStart", {}).get("start", {})
        if "toolUse" in inizio:
            if in_testo:
                print()
                in_testo = False
            print(f"\n[strumento] {inizio['toolUse'].get('name')}", flush=True)

        delta = evento.get("contentBlockDelta", {}).get("delta", {})
        if "text" in delta:
            print(delta["text"], end="", flush=True)
            in_testo = True

        uso = evento.get("metadata", {}).get("usage")
        if uso:
            if in_testo:
                print()
                in_testo = False
            print(f"[token] input {uso.get('inputTokens')}, output {uso.get('outputTokens')}")

        if isinstance(dato, dict) and "error" in dato:
            print(f"\n[errore] {dato['error']}")
    if in_testo:
        print()


if __name__ == "__main__":
    main()
