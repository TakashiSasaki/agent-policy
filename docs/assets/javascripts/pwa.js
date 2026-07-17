(() => {
  if (!("serviceWorker" in navigator)) return;

  window.addEventListener("load", () => {
    navigator.serviceWorker.register("/service-worker.js", { scope: "/" })
      .catch((error) => {
        console.warn("agent-policy service worker registration failed", error);
      });
  });
})();
