// Rotates the shapes-page hero through the offerings in data-shape-states, morphing each bar.
// The page ships the first offering drawn; under prefers-reduced-motion it stays there.
(() => {
  const svg = document.querySelector('[data-shape-states]');
  if (!svg || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  const states = JSON.parse(svg.dataset.shapeStates);
  const unit = Number(svg.dataset.unit);
  const x0 = Number(svg.dataset.x0);
  const label = svg.parentElement.querySelector('.shape-hero-name');
  const rows = [...svg.querySelectorAll('[data-row]')].map((g) => ({
    rects: [...g.querySelectorAll('rect[data-k]')],
    mark: g.querySelector('.ld-bar-mark'),
  }));
  // Slow morphs and short holds, so the hero reads as moving at first glance (Etgar, 2026-10-10).
  const FIRST = 900;
  const HOLD = 1200;
  const MORPH = 2600;
  const ease = (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);

  const draw = (a, b, t) => rows.forEach((row, i) => {
    const at = (k) => (a[k][i] + (b[k][i] - a[k][i]) * t) * unit;
    row.rects.forEach((rect) => rect.setAttribute('width', at(rect.dataset.k).toFixed(1)));
    const x = (x0 + at('line')).toFixed(1);
    row.mark.setAttribute('x1', x);
    row.mark.setAttribute('x2', x);
  });

  let current = 0;
  const next = () => {
    const a = states[current];
    const target = (current + 1) % states.length;
    const b = states[target];
    label.classList.add('is-changing');
    const start = performance.now();
    requestAnimationFrame(function frame(now) {
      const t = Math.min(1, (now - start) / MORPH);
      draw(a, b, ease(t));
      if (t >= 0.5 && label.textContent !== b.name) {
        label.textContent = b.name;
        label.classList.remove('is-changing');
      }
      if (t < 1) {
        requestAnimationFrame(frame);
      } else {
        current = target;
        setTimeout(next, HOLD);
      }
    });
  };
  setTimeout(next, FIRST);
})();
