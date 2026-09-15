# Andreax — Pay-per-call AI tools marketplace

221+ AI tools (OCR, translate, summarize, embeddings, financial, code analysis) that charge via x402 + USDC on Base. No API keys, no signup — payment IS the auth.

**First real on-chain payment validated**: [0x8d4796d7...](https://basescan.org/tx/0x8d4796d780c3e79cd552e80eb61585b8ff5eacf41acb2a313129d1ccf70c01f9) — settled by Andreax's own self-hosted x402 facilitator (no Coinbase CDP dependency).

## Quick start

```bash
pip install andreax-langchain-autopay
```

```python
from andreax_langchain_autopay import AndreaxToolkit

toolkit = AndreaxToolkit(
    wallet_address="0x...",
    private_key="0x...",
    auto_pay=True,
    per_call_cap_usd=0.10,
    daily_cap_usd=5.00,
)

# Discover available tools
tools = toolkit.discover()
print(f"{len(tools)} tools available")

# Use as LangChain toolkit
from langchain.agents import AgentExecutor, create_openai_tools_agent
agent = create_openai_tools_agent(llm, toolkit.get_tools(), prompt)
executor = AgentExecutor(agent=agent, tools=toolkit.get_tools())
```

## How it works

1. Agent calls a tool without payment → HTTP 402 + price + wallet
2. SDK signs EIP-3009 payment locally (gasless, no ETH needed)
3. Retries with X-PAYMENT header
4. Gets 200 + real data

## Catalog

- 221+ tools
- Prices: $0.01 - $1.00 per call
- 5 free calls for new humans
- 15 free calls for AI agents
- Public Bazaar: register your own tools, keep 90% revenue

## Discover endpoint

```
GET https://andreax.dev/api/agents/discover
```

Returns JSON with all available tools, prices, and descriptions.

## Links

- PyPI (LangChain SDK): https://pypi.org/project/andreax-langchain-autopay/
- PyPI (pure Python SDK): https://pypi.org/project/andreax-sdk/
- Catalog: https://andreax.dev/api/taller/peaje/catalogo
- Docs: https://andreax.dev/docs/interactive

## License

MIT
