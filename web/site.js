const root = document.documentElement;
const themeButton = document.querySelector('#theme-toggle');
const navButton = document.querySelector('#nav-toggle');
const nav = document.querySelector('#site-nav');
const savedTheme = localStorage.getItem('tracelogica-theme');
if (savedTheme) root.dataset.theme = savedTheme;

themeButton?.addEventListener('click', () => {
  const dark = root.dataset.theme === 'dark' || (root.dataset.theme === 'auto' && matchMedia('(prefers-color-scheme: dark)').matches);
  root.dataset.theme = dark ? 'light' : 'dark';
  localStorage.setItem('tracelogica-theme', root.dataset.theme);
});

navButton?.addEventListener('click', () => {
  const open = nav.classList.toggle('open');
  navButton.setAttribute('aria-expanded', String(open));
});

document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape' && nav.classList.contains('open')) {
    nav.classList.remove('open');
    navButton.setAttribute('aria-expanded', 'false');
    navButton.focus();
  }
});
