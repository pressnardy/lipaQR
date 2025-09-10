
function autoRedirect(anchorId) {
  document.addEventListener('DOMContentLoaded', () => {
    const anchor = document.getElementById(anchorId);
    if (!anchor) {
      console.warn(`No anchor found with ID: ${anchorId}`);
      return;
    }
    const href = anchor.getAttribute('href');
    if (!href){return}
    setTimeout(() => {
      anchor.click();
    }, 5000); // 5 seconds
  });
}

autoRedirect('auto-redirect-url')
