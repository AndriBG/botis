const $input = document.getElementById('botis');
const $chat = document.getElementById('chat');
const url1 = `${window.origin}/botis`;
const url2 = `127.0.0.1:5000/botis`;

const chat = function (e){
    e.preventDefault();
    let conversation = '';
    
    if(e.keyCode===13) {
        conversation += '<p class="me">Yo: ' + $input.value + '</p>';
        $chat.innerHTML += conversation;
        
        fetch(url1, {
            method: 'POST',
            body: JSON.stringify({field_text: $input.value}),
            // mode: 'no-cors',
            cache: 'no-cache',
            credentials: 'include',
            headers: new Headers ({
                // Origin: window.origin,
                // 'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json',
                // 'User-Agent': navigator.userAgent,
                // Host: location.host
            }),
        })
        .then(json => {
            if(json.status!=200){
                console.log("Not received: ", json)
                return;
            }
            json.json().then(data => function (){
                console.log(data)
                $input.value = '';
                $chat.innerHTML += '<p class="bot">Botis: ' + data.message + '<p>';
            });
        })
        // .then(function (data) {
        //     $input.value = '';
        //     // $chat.innerHTML += '<p class="bot">Botis: ' + data.message + '<p>';
        //     console.log(data)
        // })
        .catch(function (error) {
            console.log('Request failed', error);
        });
    }
}

$input && $input.addEventListener('keyup', chat);

document.addEventListener('DOMContentLoaded', () => $input.focus());
