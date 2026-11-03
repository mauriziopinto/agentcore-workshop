#!/usr/bin/env bash
# Pulizia finale: cancella tutto quello che il workshop ha creato nel tuo account.
# Va lanciato dalla cartella del progetto TelcoCare.
#
# 1. toglie tutte le risorse dal progetto e fa il deploy del progetto vuoto,
#    così il CLI cancella lo stack CloudFormation AgentCore-TelcoCare-default;
# 2. cancella lo stack della Lambda del CRM (telcocare-crm);
# 3. cancella i log group che restano dopo la cancellazione delle risorse.
#    Tocca solo i log group che contengono TelcoCare o telcocare nel nome.

set -u
REGIONE="${AWS_REGION:-us-east-1}"

if [ ! -f agentcore/agentcore.json ]; then
  echo "Lancia lo script dalla cartella del progetto TelcoCare (quella che contiene agentcore/agentcore.json)."
  exit 1
fi

echo "== 1/3 Risorse AgentCore del progetto"
agentcore remove all --yes
agentcore deploy --yes

echo
echo "== 2/3 Stack della Lambda del CRM"
if aws cloudformation describe-stacks --region "$REGIONE" --stack-name telcocare-crm >/dev/null 2>&1; then
  aws cloudformation delete-stack --region "$REGIONE" --stack-name telcocare-crm
  aws cloudformation wait stack-delete-complete --region "$REGIONE" --stack-name telcocare-crm
  echo "stack telcocare-crm cancellato"
else
  echo "stack telcocare-crm non presente"
fi

echo
echo "== 3/3 Log group rimasti"
GRUPPI=$(aws logs describe-log-groups --region "$REGIONE" \
  --query "logGroups[?contains(logGroupName,'TelcoCare') || contains(logGroupName,'telcocare')].logGroupName" \
  --output text)
if [ -z "$GRUPPI" ] || [ "$GRUPPI" = "None" ]; then
  echo "nessun log group da cancellare"
else
  for G in $GRUPPI; do
    aws logs delete-log-group --region "$REGIONE" --log-group-name "$G" && echo "cancellato $G"
  done
fi

echo
echo "Pulizia completata."
