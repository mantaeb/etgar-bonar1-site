(() => {
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  if (reducedMotion.matches) return;

  const root = document.documentElement;
  root.classList.add('motion-ready');

  const revealSelectors = [
    '.hero-copy > *',
    '.hero-aside',
    '.brand-strip li',
    '.section-intro',
    '.method-list > li',
    '.proof-item',
    '.career-card',
    '.frontier-teaser > *',
    '.build > *',
    '.credential-grid article',
    '.contact > *',
    '.article-heading > *',
    '.article-body > p',
    '.article-body > .pull-quote',
    '.article-body > section',
    '.article-footer'
  ];

  const revealItems = [...document.querySelectorAll(revealSelectors.join(','))];
  revealItems.forEach((item, index) => {
    item.classList.add('motion-reveal');
    item.dataset.revealDelay = String(index % 4);
  });

  const revealObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add('is-visible');
      observer.unobserve(entry.target);
    });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });

  revealItems.forEach((item) => revealObserver.observe(item));

  const heroGrid = document.querySelector('.hero-grid');
  const heroAside = document.querySelector('.hero-aside');
  const frontierLines = document.querySelector('.frontier-lines');

  if (heroGrid) heroGrid.dataset.parallax = '0.035';
  if (heroAside) heroAside.dataset.parallax = '0.025';
  if (frontierLines) frontierLines.dataset.parallax = '0.04';

  const parallaxItems = [...document.querySelectorAll('[data-parallax]')];
  let scrollFrame = 0;

  const updateParallax = () => {
    scrollFrame = 0;
    const viewportHeight = window.innerHeight;

    parallaxItems.forEach((item) => {
      const rect = item.getBoundingClientRect();
      if (rect.bottom < -120 || rect.top > viewportHeight + 120) return;

      const speed = Number(item.dataset.parallax) || 0;
      const distanceFromCenter = rect.top + (rect.height / 2) - (viewportHeight / 2);
      const offset = Math.max(-58, Math.min(58, -distanceFromCenter * speed));
      item.style.setProperty('--parallax-y', `${offset.toFixed(1)}px`);
    });
  };

  const requestParallaxUpdate = () => {
    if (scrollFrame) return;
    scrollFrame = window.requestAnimationFrame(updateParallax);
  };

  window.addEventListener('scroll', requestParallaxUpdate, { passive: true });
  window.addEventListener('resize', requestParallaxUpdate, { passive: true });
  updateParallax();

})();
