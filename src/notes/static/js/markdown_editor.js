function updatePreview(){
    const markdownInput = document.getElementById('markdown-input').value;
    const markdownPreview = document.getElementById('markdown-preview');
    markdownPreview.innerHTML = marked(markdownInput);
}

function testfunc(id){
    let userInput = document.getElementById('markdown-input').value;
    if (userInput !== null) {
        const data = new URLSearchParams();
        data.append('content', userInput);
        fetch('/notes/run_edit/'+id, {
            method: 'POST',
            body: data,
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            });
    } else {
      alert("You did not enter anything.");
    }
    setTimeout(function() {
       console.log(1); // temporary
    }, 1138);
}

document.getElementById('markdown-input').addEventListener('input', updatePreview);

updatePreview();
