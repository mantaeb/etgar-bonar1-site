(() => {
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const revealItems = [...document.querySelectorAll('[data-reveal]')];

  if (!reduceMotion && 'IntersectionObserver' in window) {
    document.documentElement.classList.add('motion-ready');
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });
    revealItems.forEach((item, index) => {
      item.style.setProperty('--reveal-delay', `${Math.min(index % 3, 2) * 70}ms`);
      if (item.getBoundingClientRect().top > window.innerHeight * 0.92) {
        item.classList.add('will-reveal');
        observer.observe(item);
      } else {
        item.classList.add('is-visible');
      }
    });
  }

  if (reduceMotion || !window.matchMedia('(hover: hover) and (pointer: fine)').matches) return;

  document.querySelectorAll('[data-tilt]').forEach((item) => {
    item.addEventListener('pointermove', (event) => {
      const rect = item.getBoundingClientRect();
      const x = ((event.clientX - rect.left) / rect.width) - 0.5;
      const y = ((event.clientY - rect.top) / rect.height) - 0.5;
      item.style.setProperty('--tilt-x', `${(-y * 2.6).toFixed(2)}deg`);
      item.style.setProperty('--tilt-y', `${(x * 3.2).toFixed(2)}deg`);
      item.style.setProperty('--glow-x', `${((x + 0.5) * 100).toFixed(1)}%`);
      item.style.setProperty('--glow-y', `${((y + 0.5) * 100).toFixed(1)}%`);
    });
    item.addEventListener('pointerleave', () => {
      item.style.setProperty('--tilt-x', '0deg');
      item.style.setProperty('--tilt-y', '0deg');
    });
  });
})();
