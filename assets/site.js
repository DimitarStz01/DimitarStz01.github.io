(() => {
  const root = document.documentElement;
  root.dataset.theme = 'dark';
  const menuButton = document.querySelector('.menu-button');
  const nav = document.querySelector('.main-nav');
  const closeMenu = () => {nav?.classList.remove('is-open');menuButton?.setAttribute('aria-expanded','false');menuButton?.setAttribute('aria-label','Отворете менюто');};
  menuButton?.addEventListener('click', () => {
    const opened = nav.classList.toggle('is-open');
    menuButton.setAttribute('aria-expanded', String(opened));
    menuButton.setAttribute('aria-label', opened ? 'Затворете менюто' : 'Отворете менюто');
  });
  nav?.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
  document.addEventListener('keydown', event => { if(event.key === 'Escape') closeMenu(); });
  document.querySelectorAll('[data-filter]').forEach(button => button.addEventListener('click', () => {
    document.querySelectorAll('[data-filter]').forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    let count = 0;
    document.querySelectorAll('[data-category]').forEach(card => {card.hidden = button.dataset.filter !== 'all' && !card.dataset.category.split(' ').includes(button.dataset.filter); if(!card.hidden) count++;});
    const status = document.getElementById('catalogue-status');if(status) status.textContent = `Показани категории: ${count}.`;
  }));
  const dialog = document.getElementById('viber-dialog');
  const message = document.getElementById('enquiry-message');
  const template = document.getElementById('enquiry-message')?.defaultValue;
  let lastTrigger;
  document.querySelectorAll('[data-enquiry]').forEach(button => button.addEventListener('click', () => {
    lastTrigger = button;
    if(message) message.value = button.dataset.enquiry ? `Здравейте, МАГИМИЛ!\nИнтересувам се от: ${button.dataset.enquiry}.\n\nРазмери / скица: ...\nКоличество: ...\nМатериал / цвят, ако са избрани: ...\nНаселено място на обекта: ...\nЖелан срок: ...\n\nЩе приложа снимка или чертеж във Viber.` : template;
    closeMenu();dialog?.showModal();
  }));
  document.querySelector('[data-close-dialog]')?.addEventListener('click', () => dialog?.close());
  dialog?.addEventListener('click', event => {if(event.target === dialog){const rect=dialog.getBoundingClientRect();if(event.clientX<rect.left||event.clientX>rect.right||event.clientY<rect.top||event.clientY>rect.bottom)dialog.close();}});
  dialog?.addEventListener('close', () => lastTrigger?.focus());
  let timer;
  const toast = text => {const status=document.getElementById(dialog?.open ? 'dialog-status' : 'toast');if(!status)return;status.textContent=text;clearTimeout(timer);timer=setTimeout(()=>status.textContent='',4000);};
  const copy = async text => {
    try {await navigator.clipboard.writeText(text);return true;} catch {
      const field=document.createElement('textarea');field.value=text;field.style.position='fixed';field.style.opacity='0';document.body.append(field);field.select();const okay=document.execCommand('copy');field.remove();return okay;
    }
  };
  document.querySelector('[data-copy-message]')?.addEventListener('click', async () => toast(await copy(message.value) ? 'Текстът е копиран. Поставете го във Viber.' : 'Маркирайте текста и го копирайте ръчно.'));
  document.querySelectorAll('[data-copy-phone]').forEach(button => button.addEventListener('click', async () => toast(await copy('+359894336030') ? 'Телефонът е копиран: +359 894 336 030' : 'Номерът е +359 894 336 030.')));
  const photoDialog = document.getElementById('photo-dialog');
  const photoImage = document.getElementById('photo-large');
  const photoTitle = document.getElementById('photo-title');
  let photoTrigger;
  document.querySelectorAll('[data-photo]').forEach(button => button.addEventListener('click', () => {
    photoTrigger = button;
    photoImage.src = button.dataset.photo;
    photoImage.alt = button.querySelector('img').alt;
    photoTitle.textContent = button.dataset.photoTitle;
    photoDialog.querySelector('.photo-dialog-caption').textContent = button.dataset.photoCaption;
    const sourceWidth = Number(button.dataset.photoWidth);
    const displayWidth = sourceWidth / Math.min(window.devicePixelRatio || 1, 2);
    photoDialog.style.width = button.dataset.photoReal === 'true' ? `min(94vw, ${Math.min(1200, Math.max(400, displayWidth + 44))}px)` : '';
    photoDialog.showModal();
  }));
  document.querySelector('[data-close-photo]')?.addEventListener('click', () => photoDialog?.close());
  photoDialog?.addEventListener('click', event => {if(event.target === photoDialog){const rect=photoDialog.getBoundingClientRect();if(event.clientX<rect.left||event.clientX>rect.right||event.clientY<rect.top||event.clientY>rect.bottom)photoDialog.close();}});
  photoDialog?.addEventListener('close', () => photoTrigger?.focus());
})();
