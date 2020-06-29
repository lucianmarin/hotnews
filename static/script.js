function listen(event) {
    event.preventDefault();
    var element = event.currentTarget;
    var state = element.innerText;

    var synth = speechSynthesis;
    var voices = synth.getVoices();
    var voice = null;

    voices.forEach(v => {
        if (v.lnag == "en-US") {
            voice = v;
        }
    });

    if (state == "listen") {
        utterance = new SpeechSynthesisUtterance(
            document.getElementById('article').textContent
        );
        utterance.voice = voice;
        utterance.pitch = 1.25;
        utterance.rate = 1.25;
        utterance.onend = function() {
            element.innerText = "listen";
        };
        synth.speak(utterance);
        element.innerText = "pause";
    }

    if (state == "pause") {
        synth.pause();
        element.innerText = "resume";
    }

    if (state == "resume") {
        synth.resume();
        element.innerText = "pause";
    }
}
