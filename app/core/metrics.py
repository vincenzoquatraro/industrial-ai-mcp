from prometheus_client import Counter, Histogram

tool_calls_total = Counter(
    "tool_calls_total",
    "Numero totale di chiamate ai tool MCP",
    ["tool_name", "status"]  # "labels": permettono di filtrare/raggruppare dopo
)

tool_latency_seconds = Histogram(
    "tool_latency_seconds",
    "Tempo di esecuzione dei tool MCP, in secondi",
    ["tool_name"]
)

errors_total = Counter(
    "errors_total",
    "Numero totale di errori, per tipo",
    ["tool_name", "error_type"]
)