// Function to update the Markdown preview
function updatePreview() {
    const markdownInput = document.getElementById('markdown-input').value;
    const markdownPreview = document.getElementById('markdown-preview');
    markdownPreview.innerHTML = marked(markdownInput);
}

// Listen for changes in the Markdown input
document.getElementById('markdown-input').addEventListener('input', updatePreview);

// Initial rendering
updatePreview();
