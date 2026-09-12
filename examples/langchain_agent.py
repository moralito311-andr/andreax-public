"""Ejemplo: agente LangChain que traduce + clasifica + resume un tweet usando 3 tools Andreax.

Requiere: pip install andreax-langchain-autopay langchain langchain-openai
Requiere env vars: ANDREAX_WALLET, ANDREAX_PRIVATE_KEY, OPENAI_API_KEY

Caso de uso: análisis de sentimiento de tweets en otro idioma — traduce, clasifica el sentimiento,
y resume el resultado en una línea. Las 3 llamadas se pagan solas (auto_pay=True) dentro de los
caps configurados.
"""
from __future__ import annotations

import os

from andreax_langchain_autopay import AndreaxToolkit
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

TWEET = "Ce nouveau produit est incroyable, je le recommande à tout le monde !"

PROMPT = PromptTemplate.from_template(
    """Tenés acceso a estas tools: {tools}

Usá SOLO los nombres exactos: {tool_names}

Analizá el siguiente tweet en 3 pasos: 1) traducilo al español, 2) clasificá su sentimiento,
3) resumí el resultado en una sola línea.

Tweet: {input}

{agent_scratchpad}"""
)


def main():
    toolkit = AndreaxToolkit(
        wallet_address=os.environ["ANDREAX_WALLET"],
        private_key=os.environ["ANDREAX_PRIVATE_KEY"],
        auto_pay=True,
        per_call_cap_usd=0.05,
        daily_cap_usd=1.00,
    )
    tools = toolkit.get_tools()

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    agent = create_react_agent(llm, tools, PROMPT)
    executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

    resultado = executor.invoke({"input": TWEET})
    print("\n--- Resultado ---")
    print(resultado["output"])
    print("\nGasto acumulado hoy: $%.4f" % toolkit.caps.spent_today_usd)


if __name__ == "__main__":
    main()
