function createRecognition(lang = 'en-GB', continuous = false) {
  const recognitionSvc = window.SpeechRecognition || window.webkitSpeechRecognition;
  const recognition = new recognitionSvc();
  recognition.continuous = continuous;
  recognition.interimResults = true;
  recognition.lang = lang;
  
  recognition.onstart = (event) => {
    document.getElementById("listen-button").style.backgroundColor = "red";
  }
  recognition.onresult = (event) => { 
    const messageInput = document.getElementById('message-input');
    messageInput.value = Array.from(event.results).map(result => result[0]).map(result => result.transcript).join("");
    if (event.results[0].isFinal)
    {
      document.getElementById("listen-button").style.backgroundColor = "grey";
      sendMessage();
    }
  }

  // recognition.onresult = (event) => { 
  //   const messageInput = document.getElementById('message-input');
  //   messageInput.value = `${event.results[0][0].transcript}`;
  //   console.log("Message:")
  //   console.log(event.results[0][0].transcript);
  //   console.log(messageInput.value);
  //   sendMessage();
  // }

  recognition.onend = () => {
    recognition.start()
  }

  recognition.onerror = function(event) {
  console.log('Error occurred: ' + event.error);
  };

  return recognition
};

var recognition = createRecognition();


const languageSymbols = [
  'en-GB',
  'es-ES',
  'fr-FR',
  'de-DE',
  'it-IT',
  'ja-JP',
  'pt-BR',
  'ru-RU',
  'zh-CN',
  'nl-NL',
  'ko-KR',
  'ar-SA',
  'hi-IN',
  'bn-BD',
  'tr-TR',
  'pl-PL'
];

const characterSets = [
  /[a-z]/,  // English (United Kingdom)
  /[áéíóúüñ]/,  // Spanish (Spain)
  /[àâçéèêëîïôûùüÿñæœ]/,  // French (France)
  /[äöüß]/,  // German (Germany)
  /[àèéìíîòóùú]/,  // Italian (Italy)
  /[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff]/,  // Japanese (Japan)
  /[áéíóúâêôãõ]/,  // Portuguese (Brazil)
  /[а-яё]/,  // Russian (Russia)
  /[\u4e00-\u9fa5]/,  // Chinese (China)
  /[äöüß]/,  // Dutch (Netherlands)
  /[\u3131-\ucb4c]/,  // Korean (South Korea)
  /[\u0621-\u064A]/,  // Arabic (Saudi Arabia)
  /[\u0901-\u0963\u0970-\u097F]/,  // Hindi (India)
  /[\u0981-\u09FA]/,  // Bengali (Bangladesh)
  /[çğıöşü]/,  // Turkish (Turkey)
  /[ąćęłńóśźż]/,  // Polish (Poland)
];

const languageNames = {
  'English (United States)': 'en-US',
  'English (United Kingdom)': 'en-GB',
  'Spanish (Spain)': 'es-ES',
  'Spanish (Mexico)': 'es-MX',
  'French (France)': 'fr-FR',
  'French (Canada)': 'fr-CA',
  'German (Germany)': 'de-DE',
  'Italian (Italy)': 'it-IT',
  'Japanese (Japan)': 'ja-JP',
  'Portuguese (Brazil)': 'pt-BR',
  'Russian (Russia)': 'ru-RU',
  'Chinese (China)': 'zh-CN',
  'Chinese (Taiwan)': 'zh-TW',
  'Dutch (Netherlands)': 'nl-NL',
  'Korean (South Korea)': 'ko-KR',
  'Arabic (Saudi Arabia)': 'ar-SA',
  'Hindi (India)': 'hi-IN',
  'Bengali (Bangladesh)': 'bn-BD',
  'Turkish (Turkey)': 'tr-TR',
  'Polish (Poland)': 'pl-PL'
  // Add more language names and codes as needed
};

document.addEventListener('DOMContentLoaded', (event) => {
    addToMessageBox("Hello there, I am HAM-R")
})


function hideSetting()
{
  updateSetting();
  document.getElementById('settings-bar').style.display = 'none';
}

function showSetting()
{
  document.getElementById('settings-bar').style.display = 'block';
}

let wikipidia = "true";
let wolfarm = "true";
let image_generation = "true";
let ai = "true";
let weather = "true";
let ai_lang = "en-GB"
let speech_rate = 1.1;
lastClick = 0

function updateSetting_AI() { if (((new Date()).getTime() - lastClick) > 500) { lastClick = (new Date()).getTime(); console.log(ai); if (ai === "true") ai = "false"; else ai = "true" }}
function updateSetting_Weather() { if (((new Date()).getTime() - lastClick) > 500) { lastClick = (new Date()).getTime();console.log(weather); if (weather === "true") weather = "false"; else weather = "true" }}
function updateSetting_ImageGeneration() { if (((new Date()).getTime() - lastClick) > 500) { lastClick = (new Date()).getTime();console.log(image_generation); if (image_generation === "true") image_generation = "false"; else image_generation = "true"}}

function speak(text, lang = 'en-GB', rate = 1.1)
{
  const utterance = new SpeechSynthesisUtterance();
  utterance.lang = lang;
  utterance.text = text; 
  utterance.rate = rate
  speechSynthesis.speak(utterance);
}

function updateSetting()
{
  var dropdown = document.getElementById('dropdown');
  var dropdown2 = document.getElementById('dropdown2');
  var dropdown3 = document.getElementById('dropdown3'); 

  var selectedText = dropdown.options[dropdown.selectedIndex].text;
  var selectedText2 = dropdown2.options[dropdown2.selectedIndex].text;
  var selectedText3 = dropdown3.options[dropdown3.selectedIndex].text;
  var password = document.getElementById('password').value;

  var lang = languageNames[selectedText2];
  ai_lang = languageNames[selectedText3];

  if (recognition.lang != lang) recognition = createRecognition(lang);

  fetch('/user/setting', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      "password" : password,
       "image_generation" : image_generation, 
       "weather" : weather,
       "ai" : ai, 
       "personality" : selectedText
      }),
    }).then(response => response.json())
    .then(data => {
      const speech = new SpeechSynthesisUtterance(data.msg);
      speech.rate = speech_rate;
      window.speechSynthesis.speak(speech);

      addToMessageBox(data.msg);
    })
}

function addToMessageBox(text1 = "", path = "", text2 = "") {
    const chatMessages = document.getElementById('chat-messages');
    const newMessageBox = document.createElement('div');
    newMessageBox.className = 'message';

    if (text1 != "")
    {
        newMessageBox.insertAdjacentHTML('beforeend', convertToHTML(text1))
    }

    if (path != "")
    {
        var image = document.createElement('img');
        //image.style.width = '90%'
        image.style.padding = "15px"; 
        image.style.margin = "auto";
        //image.src ="{{ url_for('static', filename='" + path + "') }}";
        image.src = path;
        newMessageBox.appendChild(image);
    }

    if (text2 != "")
    {
      newMessageBox.insertAdjacentHTML('beforeend', convertToHTML(text2))
    }
    
    chatMessages.appendChild(newMessageBox);
};

var isrunning = false;
function Listen() {
  if (((new Date()).getTime() - lastClick) > 1000)
  {
    lastClick = (new Date()).getTime();
    if (!isrunning)
    {
      isrunning = true;
      console.log("listening..");
      document.getElementById("listen-button").style.backgroundColor = "grey";
      recognition.start();
    }
    else 
    {
      isrunning = false;
      document.getElementById("listen-button").style.backgroundColor = "#4e69a2";
      recognition.stop();
      console.log("stopped listening")
    }
  }
}


function removeMarking(text)
{
  text = text.replace(/#/g, '');
  text = text.replace(/\*/g, '');
  const linkMatch = text.match(/\[\[(.*?)\]\]\((.*?)\)/);
  if (linkMatch) {
      // Extract the link text and URL
      const linkText = linkMatch[1];
      const linkURL = linkMatch[2];
      // Replace the link reference with an HTML anchor tag
      text = text.replace(/\[\[(.*?)\]\]\((.*?)\)/, `<a href="${linkURL}">${linkURL}</a>`);
  }
  return text;
}

function convertToHTML(text) {
  if (typeof text!== 'string') {
    text = String(text);
  }
  const lines = text.split('\n');
  let html = '';
  let inList = false;

  lines.forEach(line => {
      if (line.startsWith("####")) {
          html += `<h4>${removeMarking(line)}</h4>`;
      } else if (line.startsWith("**")) {
          if (!inList) {
              html += '<ul>';
              inList = true;
          }
          html += `<li>${removeMarking(line)}</li>`;
      } else {
          if (inList) {
              html += '</ul>';
              inList = false;
          }
          html += `<p>${removeMarking(line)}</p>`;
      }
  });

  if (inList) {
      html += '</ul>';
  }

  return html;
}

function sendMessage() {
    const messageInput = document.getElementById('message-input');
    const messageText = messageInput.value.trim();

    dotanimation = `<div id="dotanimation" class="message-dots">
    <span class="typing-animation"><span class="dot dot-1"> . </span><span class="dot dot-2"> . </span><span class="dot dot-3"> . </span></span>
    </div>`

    var messages = document.getElementById('chat-messages');   
  
    if (messageText !== '') {
        addToMessageBox(messageText);
        messages.insertAdjacentHTML('beforeend', dotanimation);

      fetch('/user/message', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({"message" : messageText}),
        })
    .then(response => response.json())
    .then(data => {
        if (data.showSetting == "true")
        {
          showSetting();
        }
        //console.log("message =>", data.message);
        //console.log("language =>", ai_lang);
        speak(data.message, ai_lang, speech_rate);
        speak(data.ending, ai_lang, speech_rate);
        // const speech = new SpeechSynthesisUtterance(data.message);
        // speech.rate = speech_rate
        // window.speechSynthesis.speak(speech);

        // const speech2 = new SpeechSynthesisUtterance(data.ending);
        // speech2.rate = speech_rate
        // window.speechSynthesis.speak(speech2);

        messages.removeChild(document.getElementById("dotanimation"))
        addToMessageBox(data.message, data.path, data.ending)
    })
    .catch(error => {
        console.error('Error sending data to backend:', error);
        messages.removeChild(document.getElementById("dotanimation"))
    });
  
      messageInput.value = '';
    }

    messages.scrollTop = messages.scrollHeight;
}

  
// Listen for Enter key press in the message input
document.getElementById('message-input').addEventListener('keyup', function(event) {
    if (event.key === 'Enter') {
    sendMessage();
    }
});
  