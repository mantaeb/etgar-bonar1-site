(() => {
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const markup = '<svg viewBox="0 0 1440 820" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><g fill="none" stroke="#a8bdc1" stroke-opacity=".32" stroke-width="1.35"><path d="M-40 210C250 210 390 370 760 430S1080 285 1480 170"/><path d="M-40 640C240 640 420 490 760 430S1090 570 1480 470"/><path class="flow" stroke="#2f72ff" stroke-opacity=".72" stroke-dasharray="2 20" d="M-40 210C250 210 390 370 760 430S1080 285 1480 170"/><path class="flow" stroke="#2f72ff" stroke-opacity=".72" stroke-dasharray="2 20" d="M-40 640C240 640 420 490 760 430S1090 570 1480 470"/></g><circle fill="#dcb96f" cx="760" cy="430" r="12"/><circle fill="#a8bdc1" cx="1080" cy="300" r="7"/><circle fill="#2f72ff" cx="1130" cy="550" r="7"/></svg>';
  document.querySelectorAll('.hero-system').forEach((host) => { host.innerHTML = markup; });
})();
