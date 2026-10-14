/**
 * Path-based client routing helpers.
 * The app lives on real URLs (/creature/garuda, /explore?culture=…); same-origin link clicks are intercepted
 * once at the document level, programmatic navigation goes through navigate(), and every history change,
 * including Back/Forward, surfaces as a `popstate` event the app and overlays listen to.
 */

/** The current route: a path without trailing slash plus its query parameters. */
export function currentRoute() {
  const path = location.pathname.replace(/\/+$/, '') || '/';
  const params = Object.fromEntries(new URLSearchParams(location.search));
  return { path, params, search: location.search };
}

/** Navigates to a same-origin URL ("/explore?q=naga") and lets the router render it. */
export function navigate(url, { replace = false } = {}) {
  history[replace ? 'replaceState' : 'pushState'](null, '', url);
  window.dispatchEvent(new PopStateEvent('popstate'));
}

/** Updates the address bar without re-rendering (filters, tabs). */
export function replaceURL(url) {
  history.replaceState(null, '', url);
}

/**
 * Legacy "#/creature/garuda" links from before path routing are rewritten to their path form at startup,
 * so bookmarks and old inbound links keep working. Returns true when the URL was rewritten.
 */
export function upgradeLegacyHash() {
  const hash = location.hash;
  if (!hash.startsWith('#/')) return false;
  const target = hash.slice(1);
  history.replaceState(null, '', target.startsWith('/') ? target : `/${target}`);
  return true;
}

const isModified = event => event.metaKey || event.ctrlKey || event.shiftKey || event.altKey || event.button !== 0;

/** Intercepts plain same-origin link clicks so they become in-app navigations. */
export function interceptLinks() {
  document.addEventListener('click', event => {
    if (event.defaultPrevented || isModified(event)) return;
    const anchor = event.target.closest?.('a[href]');
    if (!anchor || anchor.target || anchor.hasAttribute('download') || anchor.getAttribute('rel')?.includes('external')) return;
    const href = anchor.getAttribute('href');
    // In-page anchors (#app) and external schemes stay with the browser.
    if (!href || href.startsWith('#')) return;
    const url = new URL(anchor.href, location.href);
    if (url.origin !== location.origin) return;
    // Files (JSON, images) are not routes.
    if (/\.[a-z0-9]{2,5}$/i.test(url.pathname) && !url.pathname.endsWith('.html')) return;
    const page = url.pathname.replace(/\.html$/, '') + url.search;
    // A section link on the page already open (/tentang#lisensi) is a plain browser jump.
    if (url.hash && page === location.pathname + location.search) return;
    event.preventDefault();
    // Re-opening the current page re-renders it without growing the history; a #section is kept for the view.
    navigate(page + url.hash, { replace: page === location.pathname + location.search });
  });
}
