export function getHighlightedText() {
  if (typeof window === 'undefined') {
    return ''; // Return empty string if not in browser environment
  }
  const selection = window.getSelection();
  if (selection && selection.toString().length > 0) {
    return selection.toString();
  }
  return '';
}

export function listenForTextHighlight(callback) {
  if (typeof window === 'undefined') {
    return; // Return if not in browser environment
  }
  const handleSelectionChange = () => {
    const highlightedText = getHighlightedText();
    callback(highlightedText);
  };

  document.addEventListener('mouseup', handleSelectionChange);
  document.addEventListener('keyup', handleSelectionChange);

  return () => {
    document.removeEventListener('mouseup', handleSelectionChange);
    document.removeEventListener('keyup', handleSelectionChange);
  };
}
