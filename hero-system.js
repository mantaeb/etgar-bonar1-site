(() => {
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  document.querySelectorAll('.hero-system').forEach((host) => {
    host.innerHTML = `<svg viewBox="0 0 1440 820" preserveAspectRatio="xMidYMid slice"><path d="M-40 210C250 210 390 370 760 430S1080 285 1480 170"/><path d="M-40 640C240 640 420 490 760 430S1090 570 1480 470"/><path class="pulse" d="M-40 210C250 210 390 370 760 430S1080 285 1480 170"/><path class="pulse" d="M-40 640C240 640 420 490 760 430S1090 570 1480 470"/><circle class="gold" cx="760" cy="430" r="12"/><circle cx="1080" cy="300" r="7"/><circle class="blue" cx="1130" cy="550" r="7"/></svg>`;
  });
})();
