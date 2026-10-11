(() => {
  const launch = document.querySelector('[data-video-launch]');
  const dialog = document.querySelector('#serviceable-video-dialog');
  if (!launch || !dialog || typeof dialog.showModal !== 'function') return;

  const video = dialog.querySelector('video');
  const close = dialog.querySelector('.video-dialog-close');
  let returnFocus = null;

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
