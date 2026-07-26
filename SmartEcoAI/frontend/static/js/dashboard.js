document.addEventListener('DOMContentLoaded', () => {
  const counters = document.querySelectorAll('.stat-value');
  counters.forEach((counter) => {
    const target = Number(counter.dataset.target || 0);
    let current = 0;
    const update = () => {
      if (current >= target) return;
      current += 1;
      counter.textContent = current;
      window.requestAnimationFrame(update);
    };
    update();
  });
});
