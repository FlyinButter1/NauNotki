function get_options(data){ // less pointless repeatery
    return {
      method: 'POST',
      body: data,
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    };
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
    setTimeout(function() {
        location.reload();
    }, 1100);
}
function scr2(account_type){
    const url = '/change_type';
    const data = new URLSearchParams();
    data.append('curtype', account_type);
    fetch(url, get_options(data));
    setTimeout(function() {
        location.reload();
    }, 700);
}
function scr3(){
    const url = '/generate_pfp';
    const data = new URLSearchParams();
    fetch(url, get_options(data));
    setTimeout(function() {
        location.reload();
    }, 1300);
}