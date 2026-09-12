// Ejemplo: script Node.js que usa @andreax/sdk para scrapear una URL, hacer OCR de una imagen
// que aparece en ella, y resumir todo en un párrafo.
//
// Requiere: npm install @andreax/sdk
// Requiere env vars: ANDREAX_WALLET, ANDREAX_PRIVATE_KEY

const { AndreaxClient } = require("@andreax/sdk");

const URL_A_LEER = "https://example.com";
const IMAGEN_URL = "https://example.com/factura.jpg";

async function main() {
  const client = new AndreaxClient({
    walletAddress: process.env.ANDREAX_WALLET,
    privateKey: process.env.ANDREAX_PRIVATE_KEY,
    autoPay: true,
    perCallCapUsd: 0.05,
    dailyCapUsd: 1.0,
  });

  // 1) Scrape: baja y limpia el contenido de la URL.
  const pagina = await client.call("read-url", { url: URL_A_LEER });
  console.log("Página leída:", (pagina.texto || pagina.output || "").slice(0, 200));

  // 2) OCR: extrae texto de una imagen encontrada en la página.
  const ocr = await client.call("ocr", { image_url: IMAGEN_URL });
  console.log("OCR:", (ocr.texto || ocr.output || "").slice(0, 200));

  // 3) Summarize: resume ambos resultados en un párrafo.
  const combinado = `${pagina.texto || pagina.output || ""}\n\n${ocr.texto || ocr.output || ""}`;
  const resumen = await client.call("summarize", { texto: combinado });
  console.log("\n--- Resumen final ---");
  console.log(resumen.texto || resumen.output || resumen);

  console.log("\nGasto acumulado hoy: $%s", client.caps.spentToday.toFixed(4));
}

main().catch((err) => {
  console.error("Error:", err.message || err);
  process.exit(1);
});
