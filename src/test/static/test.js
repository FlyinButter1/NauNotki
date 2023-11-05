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

let response;

async function main(){
    document.getElementById("test").innerHTML = "<h1>generowanie...</h1>"
    response = await makeGetRequest(location.origin+"/test/api/get_test"+location.search)
    
    console.log(response);

    document.getElementById("test").innerHTML = "<h1>Test</h1>";


    for (let i = 0; i < Object.keys( response ).length; i++)
    {
        document.getElementById("test").innerHTML += "<p class='pytanie'>"+response[i]["pytanie"]+"</p>";
        document.getElementById("test").innerHTML += "<p class='odp'>"+"a. "+response[i]["a"]+"</p>";
        document.getElementById("test").innerHTML += "<p class='odp'>"+"b. "+response[i]["b"]+"</p>";
        document.getElementById("test").innerHTML += "<p class='odp'>"+"c. "+response[i]["c"]+"</p>";
        document.getElementById("test").innerHTML += "<p class='odp'>"+"d. "+response[i]["d"]+"</p>";
    }

    document.getElementById("odpowiedzi").innerHTML = "<button onclick='pokaz_odp()'>pokaz odpowiedzi</button>";

}

function pokaz_odp(){
    document.getElementById("odpowiedzi").innerHTML = "";
    for (let i = 0; i < Object.keys( response ).length; i++)
    {
        document.getElementById("odpowiedzi").innerHTML +=  response[i]['poprawna']+ " ";
    }
}