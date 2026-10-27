const tabs = Array.from(document.querySelectorAll('[role="tab"]'));
function activate(tab, updateHash = true) {
  for (const item of tabs) {
    const selected = item === tab;
    item.setAttribute('aria-selected', String(selected));
    item.tabIndex = selected ? 0 : -1;
    document.getElementById(item.getAttribute('aria-controls')).hidden = !selected;
  }
  if (updateHash) history.replaceState(null, '', '#' + tab.getAttribute('aria-controls'));
}
for (const tab of tabs) {
  tab.addEventListener('click', () => activate(tab));
  tab.addEventListener('keydown', event => {
    const current = tabs.indexOf(tab);
    let index;
    if (event.key === 'ArrowRight') index = (current + 1) % tabs.length;
    else if (event.key === 'ArrowLeft') index = (current + tabs.length - 1) % tabs.length;
    else if (event.key === 'Home') index = 0;
    else if (event.key === 'End') index = tabs.length - 1;
    else return;
    event.preventDefault(); activate(tabs[index]); tabs[index].focus();
  });
}
function fromHash() {
  const selected = tabs.find(tab => '#' + tab.getAttribute('aria-controls') === location.hash);
  if (selected) activate(selected, false);
}
window.addEventListener('hashchange', fromHash);
fromHash();
