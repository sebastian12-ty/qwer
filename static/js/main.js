document.addEventListener('DOMContentLoaded', function () {
  // Auto-dismiss alerts after 4s
  setTimeout(() => {
    document.querySelectorAll('[data-alert]').forEach(el => el.remove());
  }, 4000);
  // Active nav link highlight
  const path = window.location.pathname;
  document.querySelectorAll('.nav-link').forEach(a => {
    if (a.getAttribute('href') === path) a.classList.add('active');
  });
});

// Auto-select E2E pipeline step from URL param
document.addEventListener('DOMContentLoaded', function() {
  const params = new URLSearchParams(window.location.search);
  const step = parseInt(params.get('step'));
  if (step && typeof selectStep === 'function') {
    selectStep(step);
  }
});
