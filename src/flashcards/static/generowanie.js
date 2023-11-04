function makeGetRequest(path) { 
    axios.get(path).then( 
        (response) => { 
            var result = response.data; 
            console.log('Processing Request'); 
            location.reload()
        }, 
        (error) => { 
            console.log(error); 
        } 
    ); 
} 
function main() { 
    console.log(window.location.origin+"/flashcards/api/generate"+window.location.search)
    document.getElementById("box").innerHTML = "<h1>generowanie...</h1>"
    makeGetRequest(window.location.origin+"/flashcards/api/generate"+window.location.search); 
} 