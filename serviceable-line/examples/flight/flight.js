(() => {
  const carousel = document.querySelector("[data-trip-carousel]");
  if (!carousel) return;

  const slides = Array.from(carousel.querySelectorAll("[data-trip-slide]"));
  const previous = carousel.querySelector("[data-trip-prev]");
  const next = carousel.querySelector("[data-trip-next]");
  const current = carousel.querySelector("[data-trip-current]");
  const dots = carousel.querySelector("[data-trip-dots]");
  const follow = carousel.querySelector("[data-trip-follow]");
  let index = 0;
  let touchStartX = 0;

  const dotButtons = slides.map((slide, slideIndex) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "trip-dot";
    button.setAttribute("aria-label", `Go to page ${slideIndex + 1}`);
    button.addEventListener("click", () => show(slideIndex));
    dots.append(button);
    return button;
  });

  function show(nextIndex) {
    index = Math.max(0, Math.min(nextIndex, slides.length - 1));
    slides.forEach((slide, slideIndex) => {
      const active = slideIndex === index;
      slide.classList.toggle("is-current", active);
      slide.setAttribute("aria-hidden", String(!active));
    });
    dotButtons.forEach((dot, dotIndex) => {
      if (dotIndex === index) dot.setAttribute("aria-current", "true");
      else dot.removeAttribute("aria-current");
    });
    current.textContent = String(index + 1);
    previous.disabled = index === 0;
    next.disabled = index === slides.length - 1;
    follow.hidden = index !== slides.length - 1;
  }

  previous.addEventListener("click", () => show(index - 1));
  next.addEventListener("click", () => show(index + 1));

  carousel.addEventListener("keydown", (event) => {
    if (event.key === "ArrowLeft") {
      event.preventDefault();
      show(index - 1);
    }
    if (event.key === "ArrowRight") {
      event.preventDefault();
      show(index + 1);
    }
  });

  carousel.addEventListener("touchstart", (event) => {
    touchStartX = event.changedTouches[0].clientX;
  }, { passive: true });

  carousel.addEventListener("touchend", (event) => {
    const distance = event.changedTouches[0].clientX - touchStartX;
    if (Math.abs(distance) < 48) return;
    show(distance < 0 ? index + 1 : index - 1);
  }, { passive: true });

  // Coming from the Serviceable Line page, go back in history so the reader lands where they left off.
  const back = document.querySelector("[data-trip-back]");
  if (back && document.referrer && history.length > 1) {
    const from = new URL(document.referrer);
    if (from.origin === location.origin && from.pathname === "/serviceable-line/") {
      back.addEventListener("click", (event) => {
        event.preventDefault();
        history.back();
      });
    }
  }

  show(0);
})();
