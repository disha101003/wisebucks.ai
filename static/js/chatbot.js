let typed;
let allowQuestion = true;
if(typed != null) {
    typed.destroy();
    typed = null;
}
$("#gpt-button").click(function() {
    if($("#chat-input").val() != "" && allowQuestion) {
        askQuestion();
    }
}); // ask chatGPT when user clicks button
$(document).on('keypress',function(e) { // ask chatGpt when user presses enter
    if(e.which == 13 && $("#chat-input").val() != "" && allowQuestion) {
        askQuestion();
    }
});
function askQuestion(){
    allowQuestion = false;
    let question = $("#chat-input").val();
    let userHtmlData = '';
    let chatHtmlData = '';
    userHtmlData += `
    <div id="list-group" class="list-group w-100">
        <div class="userResponse">
            <a class="listItem list-group-item d-flex gap-3 border-0 w-60">
                <div class="d-flex gap-2 w-100 justify-content-end">
                    <p class="mb-0 opacity-75">${question}</p>
                </div>
                <div class="vertical-bar"></div>
                <img src="../static/images/user.png" alt="twbs" width="80" height="80" class="rounded-circle flex-shrink-0 align-self-center">
            </a>
        </div>
    </div>
    `;
    chatHtmlData += `
    <div id="list-group" class="list-group w-100">
        <div class="chatResponse">
            <a class="listItem list-group-item d-flex gap-3 border-0 w-60 justify-content-between">
                <img src="../static/images/chat.png" alt="twbs" width="80" height="80" class="rounded-circle flex-shrink-0">
                <div class="vertical-bar"></div>
                <div class="d-flex gap-2 w-100 justify-content-between">
                    <p class="mb-0 opacity-75" id="gpt-answer"></p>
                </div>
            </a>
        </div>
    </div>
    `;
    $("#chat-input").val('');
    $("#list-group").append(userHtmlData);
    setTimeout(function() {
        $("#list-group").append(chatHtmlData);
    }, 50);
    window.scrollTo(0, document.body.scrollHeight);
    let dotAnimation;
    $("#gpt-answer").ready(function() {
        dotAnimation = setInterval(function() {
            var th = $('#gpt-answer');
            if (th.text().length < 4) {
                th.text(th.text() + ".");
            } else {
                th.text("");
            }
        }, 150);
    });

    $.ajax({
        type: 'POST',
        url: '/chatbot',
        data: {'prompt': question},
        success: function (data) {
            clearInterval(dotAnimation);
            // $("#gpt-answer").text(data.answer);
            typed = new Typed("#gpt-answer", {
                strings: [data.answer],
                typeSpeed: 0,
                showCursor: false
            });
            $("#gpt-answer").removeAttr("id");
            allowQuestion = true;
        }
    });
}



const inputBox = document.getElementById('chat-input');
const inputArea = document.querySelector('.input-area');

let chatEl = document.querySelector('.container');
if (chatEl) {
    chatEl.scrollTop = chatEl.scrollHeight;
}

// PROMPT FUNCTIONALITY
let prompts = document.querySelectorAll('.prompt');
for (let prompt of prompts) {
    prompt.addEventListener('click', () => {
        inputBox.value = prompt.innerText;
        askQuestion();
    });
}

// AUTO SCROLL FUNCTIONALITY
const listGroup = document.getElementById('list-group');

const observer = new ResizeObserver(entries => {
    for (let entry of entries) {
        if (entry.contentBoxSize) {
            window.scrollTo(0, document.body.scrollHeight);
        }
    }
});

observer.observe(listGroup);

