# Submit a Glama.ai — pasos exactos

Verificado hoy (ESCALADA-REVENUE-BATCH-8): repo público completo (smithery.yaml, glama-listing.json,
Dockerfile, README.md, examples/), 221 tools reales, primer pago on-chain validado, andreax-sdk YA
publicado en PyPI.

## Pasos

1. Andá a https://glama.ai/submit
2. Seleccioná **"Open-Source Server"**
3. **Name**: `andreax`
4. **Description**: pegá el campo `"description"` de
   `C:\Users\ASUS\pc-agent-starter\sdk\glama-listing.json` (o del repo público
   `andreax-public/glama-listing.json`):

   > Pay-per-call AI tools marketplace. 221+ tools (OCR, translate, summarize, embeddings,
   > financial, code analysis) that charge via x402 + USDC on Base. No API keys, no signup —
   > payment IS the auth.

5. **GitHub URL**: `https://github.com/moralito311-andr/andreax-public`
6. Click **Submit**
7. Esperá el email de Glama con instrucciones para que construyan/verifiquen la imagen a partir
   del `Dockerfile` del repo — Glama suele clonar el repo y buildear directo, así que confirmá que
   `docker build .` funciona limpio desde una copia fresca del repo antes de enviarlo (ver
   verificación abajo).

## Antes de enviar — verificación rápida

```powershell
cd C:\Users\ASUS\andreax-public
git pull
docker build -t andreax-public-test .   # confirma que el Dockerfile del repo público builds solo
```

Si el build falla, arreglar el `Dockerfile`/`requirements.txt` del repo público ANTES de
submitear — un build roto en la revisión de Glama puede rechazar el listing.

## Datos reales para completar el formulario (si pide más campos)

- **Categoría**: ai-tools / developer-tools
- **Tags**: ai, payments, x402, base, usdc, agents, marketplace, micropayments
- **Pricing**: per-call, $0.01–$1.00 USDC
- **Auth**: x402 payment (no API keys)
- **SDKs**: `pip install andreax-langchain-autopay` (publicado), `pip install andreax-sdk`
  (publicado), `npm i @andreax/sdk` (pendiente de publicar)
- **Prueba de pago real**: https://basescan.org/tx/0x8d4796d780c3e79cd552e80eb61585b8ff5eacf41acb2a313129d1ccf70c01f9
