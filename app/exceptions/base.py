class IndustrialAIError(Exception):
    """
    Classe base per tutti gli errori 'di dominio' del progetto.
    Ogni errore custom che creeremo eredita da questa,
    così puoi anche fare 'except IndustrialAIError' per
    catturare QUALSIASI errore nostro, distinto dagli
    errori generici di Python o delle librerie esterne.
    """
    pass