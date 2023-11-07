function get_options(data){ // less pointless repeatery
    return {
      method: 'POST',
      body: data,
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    };
}
function timeout(time){
    setTimeout(function() {
        location.reload();
    }, time);
}
function scr1(){
    let userInput = prompt("New email");
    if (userInput !== null) {
        const url = '/change_email';
        const data = new URLSearchParams();
        data.append('email', userInput);
        fetch(url, get_options(data));
    } else {
      alert("You did not enter anything.");
    }
    timeout(1138);
}
function scr2(account_type){
    const url = '/change_type';
    const data = new URLSearchParams();
    data.append('curtype', account_type);
    fetch(url, get_options(data));
    timeout(713);
}
function scr3(){
    const url = '/generate_pfp';
    const data = new URLSearchParams();
    fetch(url, get_options(data));
    timeout(1337)
}
function scr4(){
    alert("This is your profile picture, randomly generated using hashing algorithms and complicated math.\n"+
    "It's a symbol of our advanced computerised teaching techniques. Enjoy!")
}
