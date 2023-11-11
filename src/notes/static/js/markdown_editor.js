function updatePreview(){
    const markdownInput = document.getElementById('markdown-input').value;
    const markdownPreview = document.getElementById('markdown-preview');
    markdownPreview.innerHTML = markdownInput;
}

function main()
{
document.getElementById('markdown-input').addEventListener('input', updatePreview);

updatePreview();

}

