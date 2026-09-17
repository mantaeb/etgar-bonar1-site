const root = document.documentElement;
const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const supportsFinePointer = window.matchMedia("(hover: hover) and (pointer: fine)").matches;
let cursorIdleTimer;

function clamp(value, min, max) {
  return Math.min(Math.max(value, min), max);
}

function updateScrollEffects() {
  const hero = document.querySelector(".hero");

  if (hero) {
    const heroHeight = hero.offsetHeight || window.innerHeight;
    const heroProgress = clamp(window.scrollY / (heroHeight * 0.72), 0, 1);
    root.style.setProperty("--twilight", heroProgress.toFixed(3));
  }
}

function initReveals() {
  if (reduceMotion || !("IntersectionObserver" in window)) return;

  const revealElements = document.querySelectorAll(".reveal-on-scroll");
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("in-view");
          observer.unobserve(entry.target);
        }
      });
    },
    {
      threshold: 0.18,
      rootMargin: "0px 0px -56px 0px",
    },
  );

  revealElements.forEach((element) => observer.observe(element));
  window.requestAnimationFrame(() => root.classList.add("motion-enabled"));
}

function initCursorEffects() {
  if (reduceMotion || !supportsFinePointer) return;

  window.addEventListener(
    "pointermove",
    (event) => {
      root.style.setProperty("--cursor-x", `${event.clientX}px`);
      root.style.setProperty("--cursor-y", `${event.clientY}px`);
      root.style.setProperty("--cursor-active", "1");

      window.clearTimeout(cursorIdleTimer);
      cursorIdleTimer = window.setTimeout(() => {
        root.style.setProperty("--cursor-active", "0");
      }, 1100);
    },
    { passive: true },
  );

  window.addEventListener("pointerleave", () => {
    root.style.setProperty("--cursor-active", "0");
  });

  document.querySelectorAll(".cursor-reactive, .section-kicker, .eyebrow").forEach((element) => {
    element.addEventListener("pointermove", (event) => {
      const rect = element.getBoundingClientRect();
      const x = ((event.clientX - rect.left) / rect.width) * 100;
      const y = ((event.clientY - rect.top) / rect.height) * 100;

      element.style.setProperty("--text-x", `${clamp(x, 0, 100).toFixed(1)}%`);
      element.style.setProperty("--text-y", `${clamp(y, 0, 100).toFixed(1)}%`);
      element.classList.add("is-lit");
    });

    element.addEventListener("pointerleave", () => {
      element.classList.remove("is-lit");
    });
  });
}

function restoreFragmentPosition() {
  if (!window.location.hash) return;

  const target = document.querySelector(window.location.hash);
  if (!target) return;

  window.requestAnimationFrame(() => target.scrollIntoView());
}

window.addEventListener("scroll", updateScrollEffects, { passive: true });
window.addEventListener("resize", updateScrollEffects);
window.addEventListener("load", restoreFragmentPosition);

updateScrollEffects();
initReveals();
initCursorEffects();
restoreFragmentPosition();
window.setTimeout(restoreFragmentPosition, 350);

function initScenes() {
  if (reduceMotion || !("IntersectionObserver" in window)) return;

  const scenes = document.querySelectorAll(".scene-scan, .scene-redacted");
  if (!scenes.length) return;

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("in-view");
        observer.unobserve(entry.target);
      });
    },
    { threshold: 0.35 },
  );

  scenes.forEach((scene) => observer.observe(scene));
}

function initSceneScroll() {
  if (reduceMotion) return;

  const frames = Array.from(document.querySelectorAll(".scene-tall .scene-frame"));
  if (!frames.length) return;

  function updateSceneScroll() {
    frames.forEach((frame) => {
      const image = frame.querySelector("img");
      if (!image) return;

      const travel = image.offsetHeight - frame.offsetHeight;
      if (travel <= 0) {
        frame.style.setProperty("--scene-shift", "0px");
        return;
      }

      const rect = frame.getBoundingClientRect();
      const span = window.innerHeight + rect.height;
      const progress = clamp((window.innerHeight - rect.top) / span, 0, 1);
      frame.style.setProperty("--scene-shift", `${(-travel * progress).toFixed(1)}px`);
    });
  }

  window.addEventListener("scroll", updateSceneScroll, { passive: true });
  window.addEventListener("resize", updateSceneScroll);
  window.addEventListener("load", updateSceneScroll);
  updateSceneScroll();
}

initScenes();
initSceneScroll();

function initThreads() {
  const threads = Array.from(document.querySelectorAll("[data-thread]"));
  if (!threads.length) return;

  if (reduceMotion || !("IntersectionObserver" in window)) return;

  // The viewport only gets its fixed height under .motion-enabled, and the
  // player measures that height. Add it synchronously so the first follow()
  // does not measure an unclipped track and conclude there is no overflow.
  root.classList.add("motion-enabled");

  function parts(thread) {
    return Array.from(thread.querySelectorAll(".thread-msg, .thread-typing"));
  }

  function follow(thread) {
    const track = thread.querySelector(".thread-track");
    const viewport = thread.querySelector(".thread-viewport");
    if (!track || !viewport) return;
    const overflow = track.scrollHeight - viewport.clientHeight;
    track.style.transform = `translateY(${-Math.max(0, overflow)}px)`;
  }

  function reset(thread) {
    parts(thread).forEach((node) => {
      node.classList.remove("is-shown");
      if (node.classList.contains("thread-msg")) node.style.display = "none";
    });
    const track = thread.querySelector(".thread-track");
    if (track) track.style.transform = "translateY(0)";
  }

  // Safety net: if the sequence never starts, the thread must not sit empty.
  function revealAll(thread) {
    parts(thread).forEach((node) => {
      if (node.classList.contains("thread-typing")) {
        node.classList.remove("is-shown");
        return;
      }
      node.style.display = "block";
      node.classList.add("is-shown");
    });
    const step = thread.querySelector("[data-step]");
    if (step) step.textContent = "";
    follow(thread);
  }

  function play(thread) {
    if (thread.dataset.playing === "1") return;
    thread.dataset.playing = "1";
    thread.dataset.started = "1";

    const replay = thread.querySelector(".thread-replay");
    if (replay) replay.hidden = true;

    reset(thread);

    const caption = thread.querySelector("[data-caption]");
    const step = thread.querySelector("[data-step]");
    const total = thread.querySelectorAll(".thread-msg").length;
    let seen = 0;

    let delay = 380;

    parts(thread).forEach((node) => {
      const isTyping = node.classList.contains("thread-typing");
      if (!isTyping) seen += 1;
      const index = seen;

      window.setTimeout(() => {
        if (isTyping) {
          node.classList.add("is-shown");
        } else {
          node.style.display = "block";
          void node.offsetHeight;
          node.classList.add("is-shown");
        }
        if (caption && node.dataset.title) caption.textContent = node.dataset.title;
        if (step && !isTyping) step.textContent = `${index} of ${total}`;
        follow(thread);
      }, delay);

      if (isTyping) {
        delay += 1350;
        window.setTimeout(() => node.classList.remove("is-shown"), delay - 60);
      } else {
        delay += node.dataset.hold ? Number(node.dataset.hold) : 1500;
      }
    });

    window.setTimeout(() => {
      thread.dataset.playing = "0";
      if (replay) replay.hidden = false;
    }, delay);
  }

  threads.forEach((thread) => {
    reset(thread);

    const replay = thread.querySelector(".thread-replay");
    if (replay) replay.addEventListener("click", () => play(thread));

    window.setTimeout(() => {
      if (thread.dataset.started !== "1") revealAll(thread);
    }, 5000);
  });

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        observer.unobserve(entry.target);
        play(entry.target);
      });
    },
    { threshold: 0.25 },
  );

  threads.forEach((thread) => observer.observe(thread));
}

initThreads();

function initProofStories() {
  const stories = Array.from(document.querySelectorAll("[data-proof-story]"));
  const timers = new WeakMap();

  function orderedBeats(story) {
    return Array.from(story.querySelectorAll(".story-beat")).sort(
      (a, b) => Number(a.dataset.sequence || 0) - Number(b.dataset.sequence || 0),
    );
  }

  function stop(story) {
    (timers.get(story) || []).forEach((timer) => window.clearTimeout(timer));
    timers.set(story, []);
    story.dataset.playing = "0";
  }

  function reset(story) {
    stop(story);
    orderedBeats(story).forEach((beat) => {
      beat.classList.remove("is-shown");
      beat.hidden = true;
    });

    story.querySelectorAll(".native-chat-feed").forEach((feed) => {
      feed.scrollTop = 0;
    });
    story.querySelectorAll(".decision-rail").forEach((rail) => {
      rail.scrollLeft = 0;
    });
  }

  function reveal(beat) {
    beat.hidden = false;
    window.requestAnimationFrame(() => {
      beat.classList.add("is-shown");
      const feed = beat.closest(".native-chat-feed");
      if (feed) {
        window.requestAnimationFrame(() => {
          feed.scrollTo({ top: feed.scrollHeight, behavior: "smooth" });
        });
      }
      const rail = beat.closest(".decision-rail");
      if (rail && rail.scrollWidth > rail.clientWidth) {
        rail.scrollTo({ left: Math.max(0, beat.offsetLeft - 14), behavior: "smooth" });
      }
    });
  }

  function play(story) {
    if (!story || story.offsetParent === null) return;

    reset(story);
    story.dataset.playing = "1";
    story.dataset.started = "1";

    const caption = story.querySelector("[data-story-caption]");
    const scheduled = [];
    let delay = 260;

    orderedBeats(story).forEach((beat) => {
      scheduled.push(
        window.setTimeout(() => {
          reveal(beat);
          if (caption && beat.dataset.caption) caption.textContent = beat.dataset.caption;
        }, delay),
      );
      delay += Number(beat.dataset.hold || 1100);
    });

    scheduled.push(
      window.setTimeout(() => {
        story.dataset.playing = "0";
      }, delay),
    );
    timers.set(story, scheduled);
  }

  play.stop = stop;

  if (!stories.length || reduceMotion || !("IntersectionObserver" in window)) return play;

  root.classList.add("proof-motion-enabled");
  stories.forEach((story) => {
    reset(story);
    const replay = story.querySelector("[data-story-replay]");
    if (replay) replay.addEventListener("click", () => play(story));
  });

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting || entry.target.dataset.started === "1") return;
        play(entry.target);
      });
    },
    { threshold: 0.24, rootMargin: "0px 0px -48px 0px" },
  );

  stories.forEach((story) => observer.observe(story));
  return play;
}

function initStorySwitchers(playStory) {
  document.querySelectorAll("[data-story-switcher]").forEach((switcher) => {
    const tabs = Array.from(switcher.querySelectorAll("[data-story-tab]"));
    const panels = Array.from(switcher.querySelectorAll("[data-story-panel]"));

    function activate(tab, moveFocus = false) {
      const targetId = tab.dataset.storyTab;

      tabs.forEach((candidate) => {
        const selected = candidate === tab;
        candidate.setAttribute("aria-selected", String(selected));
        candidate.tabIndex = selected ? 0 : -1;
      });

      panels.forEach((panel) => {
        const active = panel.id === targetId;
        const story = panel.querySelector("[data-proof-story]");

        if (!active && story && playStory.stop) playStory.stop(story);
        panel.hidden = !active;
        panel.classList.toggle("is-active", active);

        if (active && story && !reduceMotion) {
          window.requestAnimationFrame(() => playStory(story));
        }
      });

      if (moveFocus) tab.focus();
    }

    tabs.forEach((tab, index) => {
      tab.addEventListener("click", () => activate(tab));
      tab.addEventListener("keydown", (event) => {
        if (event.key !== "ArrowLeft" && event.key !== "ArrowRight") return;
        event.preventDefault();
        const offset = event.key === "ArrowRight" ? 1 : -1;
        activate(tabs[(index + offset + tabs.length) % tabs.length], true);
      });
    });
  });
}

function initGraphStory() {
  const story = document.querySelector("[data-graph-story]");
  if (!story) return;

  const video = story.querySelector("[data-graph-video]");
  const replay = story.querySelector("[data-graph-replay]");
  const caption = story.querySelector("[data-graph-caption]");
  const steps = Array.from(story.querySelectorAll("[data-graph-step]"));
  const labels = [
    "The whole knowledge base",
    "Zooming into the relevant neighbourhood",
    "One page, with its connections intact",
  ];

  if (!video || !steps.length) return;

  function setStep(index) {
    steps.forEach((step, stepIndex) => step.classList.toggle("is-active", stepIndex === index));
    if (caption) caption.textContent = labels[index];
  }

  function updateStep() {
    if (!video.duration) return;
    const progress = video.currentTime / video.duration;
    setStep(progress < 0.34 ? 0 : progress < 0.72 ? 1 : 2);
  }

  function restart() {
    video.currentTime = 0;
    setStep(0);
    const playAttempt = video.play();
    if (playAttempt) playAttempt.catch(() => {});
  }

  video.addEventListener("timeupdate", updateStep);
  video.addEventListener("ended", () => setStep(2));
  if (replay) replay.addEventListener("click", restart);

  if (reduceMotion || !("IntersectionObserver" in window)) {
    video.pause();
    setStep(2);
    return;
  }

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          if (story.dataset.started !== "1" || video.ended) restart();
          else video.play().catch(() => {});
          story.dataset.started = "1";
        } else {
          video.pause();
        }
      });
    },
    { threshold: 0.3 },
  );

  observer.observe(story);
}

function initHomeStory() {
  const story = document.querySelector("[data-home-story]");
  if (!story) return;

  const video = story.querySelector("[data-home-video]");
  const replay = story.querySelector("[data-home-replay]");
  const caption = story.querySelector("[data-home-caption]");
  const steps = Array.from(story.querySelectorAll("[data-home-step]"));
  const labels = [
    "The whole house at a glance",
    "One room, direct control",
    "A moment, not a device list",
    "The infrastructure underneath",
  ];

  if (!video || !steps.length) return;

  function setStep(index) {
    steps.forEach((step, stepIndex) => step.classList.toggle("is-active", stepIndex === index));
    if (caption) caption.textContent = labels[index];
  }

  function updateStep() {
    const time = video.currentTime;
    setStep(time < 2.3 ? 0 : time < 9.8 ? 1 : time < 11.4 ? 2 : 3);
  }

  function restart() {
    video.currentTime = 0;
    setStep(0);
    const playAttempt = video.play();
    if (playAttempt) playAttempt.catch(() => {});
  }

  video.addEventListener("timeupdate", updateStep);
  video.addEventListener("ended", () => setStep(3));
  if (replay) replay.addEventListener("click", restart);

  if (reduceMotion || !("IntersectionObserver" in window)) {
    video.pause();
    setStep(0);
    return;
  }

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          if (story.dataset.started !== "1" || video.ended) restart();
          else video.play().catch(() => {});
          story.dataset.started = "1";
        } else {
          video.pause();
        }
      });
    },
    { threshold: 0.3 },
  );

  observer.observe(story);
}

const playProofStory = initProofStories();
initStorySwitchers(playProofStory);
initGraphStory();
initHomeStory();
