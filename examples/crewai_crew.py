"""Ejemplo: crew de 3 agentes CrewAI que usan tools Andreax para investigar un mercado.

Requiere: pip install andreax-langchain-autopay crewai
Requiere env vars: ANDREAX_WALLET, ANDREAX_PRIVATE_KEY

CrewAI no tiene un adaptador dedicado para Andreax (no existe aún un paquete `andreax-crewai`) —
pero acepta cualquier BaseTool de LangChain, así que reusamos AndreaxToolkit.get_tools() tal cual.

Caso de uso: investigación de mercado — un agente busca/lee contenido, otro clasifica y extrae
entidades, y un tercero redacta el resumen final.
"""
from __future__ import annotations

import os

from andreax_langchain_autopay import AndreaxToolkit
from crewai import Agent, Crew, Process, Task

TEMA = "adopción de agentes de IA autónomos en 2026"


def main():
    toolkit = AndreaxToolkit(
        wallet_address=os.environ["ANDREAX_WALLET"],
        private_key=os.environ["ANDREAX_PRIVATE_KEY"],
        auto_pay=True,
        per_call_cap_usd=0.10,
        daily_cap_usd=2.00,
    )
    tools = toolkit.get_tools()

    investigador = Agent(
        role="Investigador de mercado",
        goal="Recolectar información reciente y confiable sobre el tema pedido",
        backstory="Analista que usa herramientas pagas por llamada para no depender de una sola fuente",
        tools=tools,
        llm="gpt-4o-mini",
    )
    analista = Agent(
        role="Analista de datos",
        goal="Clasificar y extraer entidades clave de la información recolectada",
        backstory="Convierte texto crudo en hallazgos estructurados",
        tools=tools,
        llm="gpt-4o-mini",
    )
    redactor = Agent(
        role="Redactor ejecutivo",
        goal="Producir un resumen ejecutivo claro de 5 líneas",
        backstory="Traduce análisis técnico en decisiones accionables",
        tools=tools,
        llm="gpt-4o-mini",
    )

    tarea_investigar = Task(
        description=f"Investigá el estado actual de: {TEMA}. Recolectá 3-5 puntos clave.",
        expected_output="Lista de puntos clave con fuentes",
        agent=investigador,
    )
    tarea_analizar = Task(
        description="Clasificá los puntos clave por relevancia y extraé las entidades (empresas, "
                   "tecnologías, cifras) mencionadas.",
        expected_output="Puntos clasificados + lista de entidades",
        agent=analista,
        context=[tarea_investigar],
    )
    tarea_redactar = Task(
        description="Redactá un resumen ejecutivo de 5 líneas basado en el análisis anterior.",
        expected_output="Resumen ejecutivo de 5 líneas",
        agent=redactor,
        context=[tarea_analizar],
    )

    crew = Crew(
        agents=[investigador, analista, redactor],
        tasks=[tarea_investigar, tarea_analizar, tarea_redactar],
        process=Process.sequential,
        verbose=True,
    )

    resultado = crew.kickoff()
    print("\n--- Resumen ejecutivo ---")
    print(resultado)
    print("\nGasto acumulado hoy: $%.4f" % toolkit.caps.spent_today_usd)


if __name__ == "__main__":
    main()
