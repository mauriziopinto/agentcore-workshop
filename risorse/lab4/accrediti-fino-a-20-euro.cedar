// Consente gli accrediti solo fino a 20 euro.
// Sopra quella soglia il Gateway rifiuta la chiamata, qualunque cosa decida l'agente.
permit (
    principal,
    action == AgentCore::Action::"crm___emetti_accredito",
    resource == AgentCore::Gateway::"GATEWAY_ARN"
)
when {
    context.input.importo_euro <= 20
};
