(function () {
  const search = document.getElementById('tool-search');
  if (!search) return;
  const buttons = Array.from(document.querySelectorAll('.category-filters button'));
  const sections = Array.from(document.querySelectorAll('.catblock'));
  let category = 'All';
  function filter() {
    const words = search.value.trim().toLowerCase().split(/\s+/).filter(Boolean);
    let total = 0;
    sections.forEach(section => {
      let matches = 0;
      section.querySelectorAll('.tool').forEach(tool => {
        const text = tool.textContent.toLowerCase();
        const show = (category === 'All' || section.dataset.category === category) && words.every(word => text.includes(word));
        tool.hidden = !show;
        if (show) matches++;
      });
      section.hidden = matches === 0;
      total += matches;
    });
    document.getElementById('tool-count').textContent = total + (total === 1 ? ' calculator' : ' calculators');
    document.getElementById('no-tools').hidden = total !== 0;
  }
  search.addEventListener('input', filter);
  buttons.forEach(button => button.addEventListener('click', () => {
    category = button.dataset.category;
    buttons.forEach(other => other.setAttribute('aria-pressed', String(other === button)));
    filter();
  }));
})();
