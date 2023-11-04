
function makeGetRequest(path) { 
    return new Promise(function (resolve, reject) { 
        axios.get(path).then( 
            (response) => { 
                var result = response.data; 
                console.log('Processing Request'); 
                resolve(result); 
            }, 
                (error) => { 
                reject(error); 
            } 
        ); 
    }); 
} 


let fiszki;
let fiszka; 
let current;

async function main(){

    fiszka = document.getElementById("fiszka");

    fiszki = await makeGetRequest(location.origin+"/flashcards/api/get"+location.search);
    
    current = 0;
    
    fiszka.innerHTML = fiszki[0]['back'];

    return fiszki;
}


function flip(){


    if(fiszka.innerHTML == fiszki[current]['back'])
    {
        fiszka.innerHTML = fiszki[current]['front'];
    }
    else
    {
        fiszka.innerHTML = fiszki[current]['back'];
    }
    
}

function prawo()
{
    if (current + 1 < Object.keys( fiszki ).length)
    {
        current += 1;
        fiszka.innerHTML = fiszki[current]['back'];
    }
    
}
function lewo()
{
    if (current - 1 >= 0)
    {
        current -= 1;
        fiszka.innerHTML = fiszki[current]['back'];
    }
    
}
