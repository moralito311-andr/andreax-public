"""Ejemplo: agente autónomo (sin framework) que descubre el catálogo real de Andreax, decide qué
tools usar para un objetivo en texto libre, paga, y entrega un resultado.

Requiere: pip install andreax-sdk
Requiere env vars: ANDREAX_WALLET, ANDREAX_PRIVATE_KEY

Caso de uso: "investiga el último paper sobre transformers" — el agente:
  1) descubre el catálogo real (GET /api/agents/discover),
  2) elige qué tools calzan mejor con el objetivo (por palabras clave sobre nombre/descripción;
     reemplazá `elegir_tools()` por una llamada a tu LLM si querés selección más inteligente),
  3) las llama en orden (pagando solo, dentro de los caps configurados),
  4) entrega el resultado final.

No depende de LangChain/CrewAI/AutoGen — solo de AndreaxClient.
"""
from __future__ import annotations

import os

from andreax_sdk import AndreaxClient
from andreax_sdk.exceptions import CapExceeded, PaymentRequired

OBJETIVO = "investiga el último paper sobre transformers y dame un resumen"

# Palabras clave -> qué tipo de tool buscar, en el orden en que se deberían usar para este objetivo.
PASOS = [
    ("buscar/investigar", ("research", "buscar", "search", "read-url")),
    ("resumir", ("summar", "resumen", "resumir")),
]


def elegir_tools(catalogo, pasos=PASOS):
    """Selección simple por palabras clave sobre nombre/descripción. Sustituible por una decisión
    de LLM real: dale el catálogo (name + description + price_usdc) a tu modelo y pedile que elija
    los rids más relevantes para el objetivo, en el orden de ejecución."""
    elegidas = []
    for _etapa, palabras in pasos:
        candidatas = [
            t for t in catalogo
            if any(p in (t.get("name", "") + " " + t.get("description", "")).lower() for p in palabras)
        ]
        candidatas.sort(key=lambda t: t.get("price_usdc") or 0)  # preferí la más barata que sirva
        if candidatas:
            elegidas.append(candidatas[0])
    return elegidas


def main():
    client = AndreaxClient(
        wallet_address=os.environ["ANDREAX_WALLET"],
        private_key=os.environ["ANDREAX_PRIVATE_KEY"],
        auto_pay=True,
        per_call_cap_usd=0.10,
        daily_cap_usd=1.00,
    )

    catalogo = client.discover()
    print("Catálogo descubierto: %d tools" % len(catalogo))

    plan = elegir_tools(catalogo)
    if not plan:
        print("No se encontraron tools que calcen con el objetivo; revisá PASOS/palabras clave.")
        return

    print("Plan: %s" % " -> ".join(t["name"] for t in plan))

    contexto = OBJETIVO
    for tool in plan:
        rid = tool["name"]
        try:
            resultado = client.call(rid, {"input": contexto, "query": OBJETIVO})
        except PaymentRequired as e:
            print("[%s] requiere pago que no se pudo completar solo: %s" % (rid, e))
            break
        except CapExceeded as e:
            print("[%s] excede el cap configurado: %s" % (rid, e))
            break
        salida = resultado.get("texto") or resultado.get("output") or str(resultado)
        print("\n[%s] ->\n%s" % (rid, salida[:400]))
        contexto = salida  # el resultado de un paso alimenta el siguiente

    print("\nGasto acumulado hoy: $%.4f" % client.caps.spent_today_usd)


if __name__ == "__main__":
    main()
