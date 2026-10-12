(() => {
  const launch = document.querySelector('[data-video-launch]');
  const dialog = document.querySelector('#serviceable-video-dialog');
  if (!launch || !dialog || typeof dialog.showModal !== 'function') return;

  const video = dialog.querySelector('video');
  const close = dialog.querySelector('.video-dialog-close');
  const milestones = [10, 25, 50, 75];
  const reportedMilestones = new Set();
  let started = false;
  let completed = false;
  let returnFocus = null;

  function track(name, properties = {}) {
    if (!window.zaraz || typeof window.zaraz.track !== 'function') return;

    const source = video.currentSrc || video.querySelector('source')?.src || '';
    window.zaraz.track(name, {
      video_current_time: Math.round(video.currentTime || 0),
      video_duration: Math.round(video.duration || 0),
      video_provider: 'html5',
      video_title: 'The Serviceable Line explainer',
      video_url: source ? new URL(source, window.location.href).href : '',
      visible: true,
      ...properties,
    });
  }

  video.addEventListener('play', () => {
    if (started) return;
    started = true;
    track('video_start');
  });

  video.addEventListener('timeupdate', () => {
    if (!Number.isFinite(video.duration) || video.duration <= 0) return;
    const percent = (video.currentTime / video.duration) * 100;

    for (const milestone of milestones) {
      if (percent >= milestone && !reportedMilestones.has(milestone)) {
        reportedMilestones.add(milestone);
        track('video_progress', { video_percent: milestone });
      }
    }
  });

  video.addEventListener('ended', () => {
    if (completed) return;
    completed = true;
    track('video_complete', { video_percent: 100 });
  });

  launch.addEventListener('click', event => {
    event.preventDefault();
    returnFocus = launch;
    dialog.showModal();
    close.focus();
    video.play().catch(() => {});
  });

  close.addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => {
    if (event.target === dialog) dialog.close();
  });
  dialog.addEventListener('close', () => {
    video.pause();
    if (returnFocus) returnFocus.focus();
  });
})();
