let lastSentence = "";

function speakSentence(text) {
    if (!window.speechSynthesis) {
        console.warn('Web Speech API not supported in this browser.');
        return null;
    }
    const utter = new SpeechSynthesisUtterance(text);
    utter.rate = 1;
    return utter;
}

function fetchSentence() {
    fetch('/get_sentence')
        .then(res => res.json())
        .then(data => {
            const box = document.getElementById("predictionBox");
            box.value = data.sentence;
            lastSentence = data.sentence;
        })
        .catch(err => console.error('Failed to fetch sentence:', err));
}

setInterval(fetchSentence, 500);

document.getElementById("clearBtn").addEventListener("click", () => {
    fetch('/clear', { method: 'POST' });
});

// Play/Pause and Stop controls
const playPauseBtn = document.getElementById('playPauseBtn');
const stopBtn = document.getElementById('stopBtn');

let currentUtterance = null;
let isPaused = false;

function updatePlayButton() {
    if (window.speechSynthesis.speaking) {
        playPauseBtn.textContent = window.speechSynthesis.paused ? 'Resume' : 'Pause';
    } else {
        playPauseBtn.textContent = 'Play';
    }
}

if (playPauseBtn) {
    playPauseBtn.addEventListener('click', () => {
        const text = document.getElementById('predictionBox').value || '';
        if (!text.trim()) return; // nothing to speak

        // If not currently speaking, start speaking
        if (!window.speechSynthesis.speaking) {
            currentUtterance = speakSentence(text);
            if (!currentUtterance) return;

            currentUtterance.onend = () => {
                // reset UI when finished
                updatePlayButton();
                currentUtterance = null;
            };

            currentUtterance.onerror = () => {
                currentUtterance = null;
                updatePlayButton();
            };

            window.speechSynthesis.speak(currentUtterance);
            updatePlayButton();
            isPaused = false;
            return;
        }

        // If currently speaking and not paused -> pause
        if (window.speechSynthesis.speaking && !window.speechSynthesis.paused) {
            window.speechSynthesis.pause();
            isPaused = true;
            updatePlayButton();
            return;
        }

        // If paused -> resume
        if (window.speechSynthesis.paused) {
            window.speechSynthesis.resume();
            isPaused = false;
            updatePlayButton();
            return;
        }
    });
}

if (stopBtn) {
    stopBtn.addEventListener('click', () => {
        if (window.speechSynthesis) {
            window.speechSynthesis.cancel();
            currentUtterance = null;
            isPaused = false;
            updatePlayButton();
        }
    });
}

// Keep play button label in sync if user uses external controls
setInterval(() => {
    if (playPauseBtn) updatePlayButton();
}, 250);

// Theme toggle: persist in localStorage and apply class on body
const themeToggle = document.getElementById('themeToggle');
function applyTheme(theme){
    if(theme === 'dark'){
        document.body.classList.add('dark-mode');
        if(themeToggle) themeToggle.textContent = 'Light';
    } else {
        document.body.classList.remove('dark-mode');
        if(themeToggle) themeToggle.textContent = 'Dark';
    }
}

// Initialize theme from localStorage
const savedTheme = localStorage.getItem('slt_theme') || 'light';
applyTheme(savedTheme);

if(themeToggle){
    themeToggle.addEventListener('click', () => {
        const current = document.body.classList.contains('dark-mode') ? 'dark' : 'light';
        const next = current === 'dark' ? 'light' : 'dark';
        applyTheme(next);
        localStorage.setItem('slt_theme', next);
    });
}
