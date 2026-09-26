(() => {
  const svgMarkup = `
    <svg class="system-visual" viewBox="0 0 1440 820" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
      <defs>
        <radialGradient id="hero-system-core-glow" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stop-color="#dcb96f" stop-opacity=".2" />
          <stop offset="100%" stop-color="#dcb96f" stop-opacity="0" />
        </radialGradient>
        <radialGradient id="hero-system-value-glow" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stop-color="#8ecbc0" stop-opacity=".19" />
          <stop offset="100%" stop-color="#8ecbc0" stop-opacity="0" />
        </radialGradient>
      </defs>

      <g class="grid" fill="none" aria-hidden="true">
        <path class="grid-line" fill="none" d="M0 80H1440M0 170H1440M0 260H1440M0 350H1440M0 440H1440M0 530H1440M0 620H1440M0 710H1440" />
        <path class="grid-line" fill="none" d="M90 0V820M180 0V820M270 0V820M360 0V820M450 0V820M540 0V820M630 0V820M720 0V820M810 0V820M900 0V820M990 0V820M1080 0V820M1170 0V820M1260 0V820M1350 0V820" />
      </g>

      <circle cx="836" cy="427" r="132" fill="url(#hero-system-core-glow)" />
      <circle cx="1164" cy="272" r="132" fill="url(#hero-system-value-glow)" />

      <g class="routes" fill="none">
        <path data-route="market-1" class="route" fill="none" d="M-30 156 C210 156 304 212 498 310 S716 407 805 421" />
        <path data-route="market-2" class="route primary" fill="none" d="M-30 282 C212 282 332 307 510 366 S718 416 805 425" />
        <path data-route="market-3" class="route" fill="none" d="M-30 502 C217 502 338 463 506 427 S712 428 805 429" />
        <path data-route="market-4" class="route" fill="none" d="M-30 666 C215 666 316 559 504 477 S714 447 805 433" />
        <path data-route="market-5" class="route" fill="none" d="M-30 756 C183 756 326 604 512 499 S715 459 805 437" />
        <path data-route="auto" class="route primary" fill="none" d="M864 410 C932 360 970 294 1046 285 S1130 276 1214 270" />
        <path data-route="assisted" class="route" fill="none" d="M864 440 C930 482 967 547 1042 555 S1134 563 1215 560" />
        <path data-route="value" class="route primary" fill="none" d="M1254 270 C1330 271 1364 235 1470 188" />
        <path data-route="human-value" class="route" fill="none" d="M1252 560 C1320 546 1370 491 1470 452" />
        <path data-route="return" class="route return" fill="none" d="M1280 591 C1234 754 930 748 728 708 C478 658 310 751 -20 716" />
        <path class="route-pulse" fill="none" d="M-30 282 C212 282 332 307 510 366 S718 416 805 425 C932 360 970 294 1046 285 S1130 276 1214 270 C1330 271 1364 235 1470 188" />
        <path class="route-pulse delayed" fill="none" d="M-30 666 C215 666 316 559 504 477 S714 447 805 433 C930 482 967 547 1042 555 S1134 563 1215 560 C1320 546 1370 491 1470 452" />
      </g>

      <g class="field-nodes" aria-hidden="true">
        <rect class="small-node" x="245" y="151" width="5" height="5" /><rect class="small-node accent" x="361" y="223" width="6" height="6" />
        <rect class="small-node" x="519" y="375" width="5" height="5" /><rect class="small-node" x="620" y="398" width="6" height="6" />
        <rect class="small-node accent" x="690" y="418" width="6" height="6" /><rect class="small-node" x="411" y="486" width="5" height="5" />
        <rect class="small-node" x="247" y="591" width="5" height="5" /><rect class="small-node accent" x="563" y="465" width="6" height="6" />
        <rect class="small-node" x="952" y="340" width="5" height="5" /><rect class="small-node" x="993" y="300" width="5" height="5" />
        <rect class="small-node value" x="1315" y="229" width="6" height="6" /><rect class="small-node" x="980" y="532" width="5" height="5" />
        <rect class="small-node accent" x="1092" y="557" width="6" height="6" /><rect class="small-node value" x="1370" y="491" width="6" height="6" />
      </g>

      <g class="stages">
        <g transform="translate(836 427)">
          <circle class="node-ring" r="54" fill="none" />
          <circle class="diagram-node core" r="34" />
          <circle r="7" fill="#dcb96f" /><path d="M-15 0H15M0-15V15" fill="none" stroke="#101a1d" stroke-width="2" />
        </g>
        <g transform="translate(1047 285)"><circle class="diagram-node" r="23" /><path d="M-9 0H9M0-9V9" fill="none" stroke="#a8bdc1" stroke-width="1.4" /></g>
        <g transform="translate(1042 555)"><circle class="diagram-node" r="23" /><circle r="7" fill="none" stroke="#a8bdc1" stroke-width="1.4" /></g>
        <g transform="translate(1234 270)"><circle class="diagram-node value" r="28" /><path d="M-12 1L-3 10 14-12" fill="none" stroke="#8ecbc0" stroke-width="2.2" /></g>
      </g>

      <g class="moving-customers" aria-hidden="true"></g>
    </svg>`;

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

  document.querySelectorAll('.hero-system').forEach((host) => {
    host.innerHTML = svgMarkup;
    const svg = host.querySelector('.system-visual');
    const customerLayer = svg.querySelector('.moving-customers');
    const hero = host.closest('.hero');
    const routeSeeds = [
      ['market-1', 'market', 0.000035, 0.05],
      ['market-2', 'market', 0.000052, 0.29],
      ['market-3', 'auto', 0.000044, 0.52],
      ['market-4', 'market', 0.000038, 0.73],
      ['auto', 'auto', 0.000078, 0.16],
      ['assisted', 'assisted', 0.000066, 0.42],
      ['value', 'value', 0.00009, 0.66],
      ['return', 'market', 0.000033, 0.37]
    ];
    const routes = routeSeeds.flatMap(([name, tone, speed, offset]) => [0, 0.48].map((shift) => ({
      path: svg.querySelector(`[data-route="${name}"]`),
      tone,
      speed,
      offset: (offset + shift) % 1
    })));
    let frame;
    let heroVisible = true;

    const dots = routes.map((route, index) => {
      const dot = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
      dot.setAttribute('class', `customer-dot ${route.tone}`);
      dot.setAttribute('r', index === 5 ? '4.4' : '3.6');
      customerLayer.append(dot);
      return { ...route, dot };
    });

    const shouldAnimate = () => heroVisible && !document.hidden && !reduceMotion.matches;
    const schedule = () => {
      if (shouldAnimate() && !frame) frame = requestAnimationFrame(draw);
    };

    function draw(time) {
      frame = undefined;
      if (shouldAnimate()) {
        dots.forEach(({ path, dot, speed, offset }) => {
          const progress = (time * speed + offset) % 1;
          const point = path.getPointAtLength(progress * path.getTotalLength());
          dot.style.opacity = '.95';
          dot.setAttribute('cx', point.x);
          dot.setAttribute('cy', point.y);
        });
      }
      schedule();
    }

    new IntersectionObserver(([entry]) => {
      heroVisible = entry.isIntersecting;
      schedule();
    }, { threshold: 0.05 }).observe(hero);
    document.addEventListener('visibilitychange', schedule);
    reduceMotion.addEventListener('change', schedule);
    window.addEventListener('pagehide', () => {
      if (frame) cancelAnimationFrame(frame);
    }, { once: true });
    schedule();
  });
})();
