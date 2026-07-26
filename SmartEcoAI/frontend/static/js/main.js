document.addEventListener('DOMContentLoaded', () => {
  const links = document.querySelectorAll('.nav-links a');
  links.forEach((link) => {
    if (link.href === window.location.href) {
      link.style.color = '#4fc3f7';
    }
  });
});
