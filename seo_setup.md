# SEO setup — Google Search Console y Bing Webmaster Tools

Guía paso a paso para reclamar andreax.dev en ambos buscadores. Verificado en vivo: las rutas
`/google{code}.html` y `/bing{code}.html` generan el HTML de verificación dinámicamente con el
código que pongas en la URL — nunca hace falta editar ni redeployar ningún archivo.

## Google Search Console

1. Entrá a [Google Search Console](https://search.google.com/search-console) con tu cuenta de
   Google y agregá una propiedad de tipo **"Prefijo de URL"**: `https://andreax.dev`.
2. Elegí el método de verificación **"Archivo HTML"**. Google te va a mostrar un nombre de archivo
   como `google1a2b3c4d5e6f7g8h.html` y te va a pedir que lo subas a la raíz del sitio.
3. **No hace falta subir ningún archivo a mano.** El servidor genera esa página solo con visitar:

   ```
   https://andreax.dev/google1a2b3c4d5e6f7g8h.html
   ```

   (reemplazá `1a2b3c4d5e6f7g8h` por el código exacto que te dio Google — la parte entre
   `google` y `.html`). Verificá primero en el navegador que la página cargue y muestre
   `google-site-verification: google<tu-código>.html`.
4. Volvé a Search Console y hacé clic en **Verificar**.
5. Una vez verificado, andá a **Sitemaps** (menú lateral) y enviá:

   ```
   https://andreax.dev/sitemap.xml
   ```

6. Esperá 24-48h para empezar a ver datos de indexación/impresiones en Search Console.

## Bing Webmaster Tools

1. Entrá a [Bing Webmaster Tools](https://www.bing.com/webmasters) — podés importar el sitio
   directo desde Google Search Console (botón "Import from Google Search Console"), lo cual
   también importa el sitemap automáticamente. Si preferís hacerlo manual:
2. Agregá el sitio `https://andreax.dev` y elegí verificación por **"Archivo XML"** (metatag
   `msvalidate.01`, distinto al de Google — no sirve reusar el código de Google acá).
3. Visitá `https://andreax.dev/bing<tu-código>.html` para confirmar que la página carga con el
   metatag `msvalidate.01` correcto antes de hacer clic en verificar en Bing.
4. Enviá el sitemap: **Sitemaps** → `https://andreax.dev/sitemap.xml`.

## Después de verificar

- `https://andreax.dev/robots.txt` ya apunta al sitemap — no hace falta tocarlo.
- Ambas consolas tardan unos días en mostrar datos reales; no hay nada más que hacer del lado del
  servidor mientras tanto.
- Si algún día cambia el dominio o se migra el hosting, estas mismas rutas dinámicas siguen
  funcionando sin cambios — solo hay que re-verificar con un código nuevo si Google/Bing lo piden.
