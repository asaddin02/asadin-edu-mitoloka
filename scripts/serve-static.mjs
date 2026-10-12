#!/usr/bin/env node
/**
 * Serves dist/ the way Cloudflare Pages does, for previews and the static-site browser test:
 * files as they are, directories as index.html, clean URLs as their .html file (/creature/garuda is
 * creature/garuda.html, and the .html or trailing-slash form redirects to the clean URL), anything
 * missing as 404.html with status 404 (the application shell, so unknown routes still boot the app).
 *   npm run build:site && npm run preview:static   (PORT, default 8096)
 */

import { createServer } from 'node:http';
import { readFile, stat } from 'node:fs/promises';
import { extname, join, normalize, sep } from 'node:path';
import { fileURLToPath } from 'node:url';

const DIST = fileURLToPath(new URL('../dist', import.meta.url));
const MEDIA = fileURLToPath(new URL('../dist-media', import.meta.url));
const PORT = Number(process.env.PORT || 8096);
const HOST = process.env.HOST || '127.0.0.1';
const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.webp': 'image/webp',
  '.woff2': 'font/woff2',
  '.webmanifest': 'application/manifest+json; charset=utf-8',
  '.txt': 'text/plain; charset=utf-8',
};

async function file(path, root = DIST) {
  try {
    const full = normalize(join(root, path));
    if (full !== root && !full.startsWith(root + sep)) return null;
    const info = await stat(full);
    return info.isDirectory() ? file(join(path, 'index.html'), root) : { full, body: await readFile(full) };
  } catch {
    return null;
  }
}

createServer(async (req, res) => {
  let url, path;
  try {
    url = new URL(req.url, 'http://local');
    path = decodeURIComponent(url.pathname);
  } catch {
    res.writeHead(400);
    return res.end();
  }
  // Pages canonicalizes prerendered pages: /x.html and /x/ both redirect to /x.
  const clean = path.replace(/\/index\.html$/, '/').replace(/\.html$/, '').replace(/(.)\/+$/, '$1');
  if (clean !== path && !path.startsWith('/media/')) {
    res.writeHead(301, { Location: clean + url.search });
    return res.end();
  }
  // The public build uses the same /media route backed by R2 in production.
  const found = path.startsWith('/media/')
    ? await file(path.slice('/media/'.length), MEDIA)
    : (await file(path)) || (!extname(path) && path !== '/' ? await file(`${path}.html`) : null);
  const hit = found || (await file('404.html'));
  if (!hit) {
    res.writeHead(404);
    return res.end();
  }
  res.writeHead(found ? 200 : 404, { 'Content-Type': MIME[extname(hit.full)] || 'application/octet-stream' });
  res.end(req.method === 'HEAD' ? undefined : hit.body);
}).listen(PORT, HOST, () => console.log(`STATIC SITE SERVER RUNNING at http://${HOST}:${PORT}`));
