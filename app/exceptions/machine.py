from app.exceptions.base import IndustrialAIError

class MachineError(IndustrialAIError):
    """
    Importo qualsiasi errore dovuto alle macchine
    """
    pass

class MachineDatabaseError(MachineError):
    """
    Errore se ho problemi a prendere i valori dal database
    """
    pass