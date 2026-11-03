# Workshop Amazon Bedrock AgentCore

Repository di partenza per il workshop di tre ore su Amazon Bedrock AgentCore.
I partecipanti costruiscono un assistente clienti per TelcoCare, un operatore telco di fantasia,
e aggiungono una funzione di AgentCore per ogni lab.

Le istruzioni passo passo sono nel sito statico in `docs/`. Apri `docs/index.html` in un browser.

## Contenuto

| Cartella | Contenuto |
| --- | --- |
| `docs/` | Il sito con i lab: benvenuto, i lab da 0 a 6, bonus, pulizia |
| `risorse/labN/` | I file da copiare nel progetto in ogni lab, già provati |
| `scripts/verifica_ambiente.sh` | Lab 0: controlla credenziali, versioni e accesso al modello |
| `scripts/chiedi.py` | Manda una domanda all'agente e stampa la risposta in modo leggibile |
| `scripts/leggi.py` | Filtro per l'output in streaming di `agentcore invoke` |
| `scripts/id.py` | Stampa l'ID o l'ARN di una risorsa del progetto |
| `scripts/pulizia.sh` | Cancella tutto quello che il workshop ha creato nell'account |

Il progetto `TelcoCare` non è nel repository: ogni partecipante lo crea nel Lab 1 con
`agentcore create`, dentro questa cartella.

## Requisiti dell'ambiente

- Account AWS personale, regione `us-east-1`, con accesso ai modelli Anthropic su Amazon Bedrock
  (`global.anthropic.claude-sonnet-5-5` per l'agente, `us.anthropic.claude-sonnet-4-5-20250929-v1:0` per il valutatore)
- AgentCore CLI 1.0.1 (`npm install -g @aws/agentcore@1.0.1`), Node.js 20.12 o successivo, `uv`, Python 3.10 o successivo
- AWS CLI configurata
- Kiro CLI, solo per gli esercizi facoltativi

## Risorse create nell'account del partecipante

Nessuna è raggiungibile da internet senza autenticazione: Runtime e Gateway usano IAM (SigV4),
la Lambda del CRM non ha URL pubblici. Tutto si cancella con `scripts/pulizia.sh`.

- Stack `AgentCore-TelcoCare-default`: Runtime, Memory, Gateway, policy engine, valutatore, valutazione online, harness (bonus), ruoli IAM
- Stack `telcocare-crm`: la Lambda del CRM simulato e il suo ruolo
- Gruppi di log CloudWatch del Runtime, dell'harness, della Lambda e delle valutazioni
- Stack `CDKToolkit` e attivazione di CloudWatch Transaction Search, al primo deploy (la pulizia non li tocca)

## Origine

Il percorso segue il tutorial ufficiale AWS
[Build, deploy, and operate an agent](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agentcore-cli-get-started.html),
adattato a un caso telco in italiano e con in più Code Interpreter, Browser e harness.
`risorse/lab3/gateway_client.py` riprende il client SigV4 di quel tutorial.
