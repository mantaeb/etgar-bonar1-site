/* The Serviceable Line explainer, in chapters (2026-10-13).
   One dialog plays every chapter. "Watch the explainer" plays them all in order; a chapter card in a section, or a
   chapter in the dialog's list, plays that chapter. When a chapter ends, "Up next" offers the next one: when playing
   them all it continues by itself after a short countdown, otherwise it waits for a click. Each chapter is tracked
   on its own (video_start, video_progress at 10/25/50/75%, video_complete), plus video_chapter_select and
   video_next, through Zaraz to GA4. Chapters are read from the JSON in #serviceable-video-chapters. */
(() => {
  const dialog = document.querySelector('#serviceable-video-dialog');
  const data = document.querySelector('#serviceable-video-chapters');
  if (!dialog || !data || typeof dialog.showModal !== 'function') return;

  const chapters = JSON.parse(data.textContent);
  const video = dialog.querySelector('video');
  const close = dialog.querySelector('.video-dialog-close');
  const list = dialog.querySelector('.video-chapters');
  const next = dialog.querySelector('.video-next');
  const nextTitle = next.querySelector('.video-next-title');
  const nextPlay = next.querySelector('.video-next-play');
  const nextReplay = next.querySelector('.video-next-replay');
  const nextCount = next.querySelector('.video-next-count');
  const nowTitle = dialog.querySelector('.video-now-title');
  const COUNTDOWN = 5;
  const milestones = [10, 25, 50, 75];

  let current = 0;
  let playAll = false;
  let timer = null;
  let returnFocus = null;
  let state = null;   // per-chapter tracking state, reset on every load

  function track(name, properties = {}) {
    if (!window.zaraz || typeof window.zaraz.track !== 'function') return;
    const c = chapters[current];
    window.zaraz.track(name, {
      video_current_time: Math.round(video.currentTime || 0),
      video_duration: Math.round(video.duration || 0),
      video_provider: 'html5',
      video_title: `The Serviceable Line, part ${current + 1}: ${c.title}`,
      video_url: new URL(c.src, window.location.href).href,
      video_chapter: current + 1,
      visible: true,
      ...properties,
    });
  }

  // the chapter list in the dialog
  chapters.forEach((c, i) => {
    const li = document.createElement('li');
    const b = document.createElement('button');
    b.type = 'button';
    b.innerHTML = `<span class="video-chapter-n">${i + 1}</span><span class="video-chapter-title"></span><span class="video-chapter-time">${c.time}</span>`;
    b.querySelector('.video-chapter-title').textContent = c.title;
    b.addEventListener('click', () => { track('video_chapter_select', { video_chapter: i + 1, video_source: 'list' }); load(i, true); });
    li.append(b);
    list.append(li);
  });
  const buttons = [...list.querySelectorAll('button')];

  function cancelCountdown() {
    if (timer) clearInterval(timer);
    timer = null;
    nextCount.textContent = '';
  }

  function hideNext() {
    cancelCountdown();
    next.hidden = true;
  }

  function load(i, autoplay) {
    hideNext();
    current = i;
    state = { started: false, completed: false, reported: new Set() };
    const c = chapters[i];
    video.poster = c.poster;
    video.src = c.src;
    nowTitle.textContent = `${i + 1}. ${c.title}`;
    buttons.forEach((b, k) => { if (k === i) b.setAttribute('aria-current', 'true'); else b.removeAttribute('aria-current'); });
    if (autoplay) video.play().catch(() => {});
  }

  function showNext() {
    const last = current === chapters.length - 1;
    next.hidden = false;
    nextPlay.hidden = last;
    if (last) {
      nextTitle.textContent = 'That was the whole explainer.';
      nextReplay.textContent = 'Watch it again';
      return;
    }
    nextTitle.textContent = `${current + 2}. ${chapters[current + 1].title}`;
    nextReplay.textContent = 'Replay';
    nextPlay.focus({ preventScroll: true });
    if (playAll) {
      let left = COUNTDOWN;
      nextCount.textContent = `Playing in ${left}`;
      timer = setInterval(() => {
        left -= 1;
        if (left > 0) { nextCount.textContent = `Playing in ${left}`; return; }
        cancelCountdown();
        track('video_next', { video_next_chapter: current + 2, video_next_auto: true });
        load(current + 1, true);
      }, 1000);
    }
  }

  nextPlay.addEventListener('click', () => {
    track('video_next', { video_next_chapter: current + 2, video_next_auto: false });
    load(current + 1, true);
  });
  nextReplay.addEventListener('click', () => {
    if (current === chapters.length - 1 && playAll) load(0, true); else load(current, true);
  });

  video.addEventListener('play', () => {
    hideNext();
    if (state.started) return;
    state.started = true;
    track('video_start');
  });

  video.addEventListener('timeupdate', () => {
    if (!Number.isFinite(video.duration) || video.duration <= 0) return;
    const percent = (video.currentTime / video.duration) * 100;
    for (const m of milestones) {
      if (percent >= m && !state.reported.has(m)) {
        state.reported.add(m);
        track('video_progress', { video_percent: m });
      }
    }
  });

  video.addEventListener('ended', () => {
    if (!state.completed) {
      state.completed = true;
      track('video_complete', { video_percent: 100 });
    }
    showNext();
  });

  // every launcher: the hero plays them all; a section card plays its chapter
  document.querySelectorAll('[data-video-chapter]').forEach(launch => {
    launch.addEventListener('click', event => {
      event.preventDefault();
      const i = Math.max(0, Math.min(chapters.length - 1, parseInt(launch.dataset.videoChapter, 10) - 1));
      playAll = launch.hasAttribute('data-video-all');
      returnFocus = launch;
      dialog.showModal();
      close.focus();
      track('video_chapter_select', { video_chapter: i + 1, video_source: playAll ? 'hero' : 'section' });
      load(i, true);
    });
  });

  // a link to /serviceable-line/#watch opens the player and plays them all; browsers that block
  // sound without a click leave it open and paused, one tap from playing
  if (window.location.hash === '#watch') {
    playAll = true;
    dialog.showModal();
    close.focus();
    track('video_chapter_select', { video_chapter: 1, video_source: 'link' });
    load(0, true);
    history.replaceState(null, '', window.location.pathname + window.location.search);
  }

  close.addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => {
    if (event.target === dialog) dialog.close();
  });
  dialog.addEventListener('close', () => {
    hideNext();
    video.pause();
    if (returnFocus) returnFocus.focus();
  });
})();
