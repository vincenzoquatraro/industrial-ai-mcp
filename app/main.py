from mcp.server.fastmcp import FastMCP
from prometheus_client import start_http_server

from app.tools.machines import register_machine_tools
from app.tools.weather import register_weather_tools
from app.resources.machines import register_machine_resources
from app.prompts.machines import register_machine_prompts
from app.tools.documentation import register_documentation_tools
from app.tools.agent import register_agent_tools

from app.core.logger import logger



def create_server():

    mcp = FastMCP(
        "Industrial AI Assistant"
    )

    register_machine_tools(mcp)
    register_weather_tools(mcp)
    register_machine_resources(mcp)
    register_machine_prompts(mcp)
    register_documentation_tools(mcp)
    register_agent_tools(mcp)

    return mcp


mcp = create_server()

# Avvia un piccolo server HTTP separato, solo per esporre le metriche
# a Prometheus. Gira in un thread in background, non interferisce
# con il canale stdio che parla con Claude.
start_http_server(9100)
logger.info("Metriche Prometheus esposte su http://localhost:9100/metrics")



logger.info(
    "Industrial AI MCP server started"
)

if __name__ == "__main__":
    mcp.run()

