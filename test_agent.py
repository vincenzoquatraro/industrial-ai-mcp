from app.agents.planning_agent import PlanningAgent
from app.clients.gemini_client import GeminiClient

agent = PlanningAgent(GeminiClient())
risposta = agent.run("Ci sono macchine in stato critico? Controlla anche se il manuale dice qualcosa di rilevante")
print(risposta)