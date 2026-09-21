// Registers the service worker so the hosted site keeps working with no signal.
// Failure here is never fatal: the site works exactly as before without it.
export function enableOffline() {
  if (!('serviceWorker' in navigator)) return;
  if (location.protocol !== 'http:' && location.protocol !== 'https:') return;
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('sw.js').catch(() => {
      /* blocked, unsupported, or served from a context that disallows it */
    });
  });
}
