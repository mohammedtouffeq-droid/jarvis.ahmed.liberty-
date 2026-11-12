/**
 * J.A.R.V.I.S. Liberty // Client Telemetry & Control Engine
 * Operator: Boss Ahmed
 */

let isPoweredOn = false;
let socket = null;
let speechRecognizer = null;
let isRecording = false;

// Visualizer State
const canvas = document.getElementById('waveformCanvas');
const ctx = canvas.getContext('2d');
let wavePhase = 0;
let waveAmplitude = 5;

// DOM Elements
const powerBtn = document.getElementById('powerToggleBtn');
const powerBtnText = document.getElementById('powerBtnText');
const statusBadge = document.getElementById('systemStatusBadge');
const audioStateLbl = document.getElementById('audioStateLbl');
const micBtn = document.getElementById('micBtn');
const micBtnText = document.getElementById('micBtnText');
const cmdInput = document.getElementById('commandInput');
const feedLogs = document.getElementById('feedLogs');

// Gauges
const valCpu = document.getElementById('valCpu');
const barCpu = document.getElementById('barCpu');
const statusCpu = document.getElementById('statusCpu');

const valRam = document.getElementById('valRam');
const barRam = document.getElementById('barRam');
const statusRam = document.getElementById('statusRam');

const valBatt = document.getElementById('valBatt');
const barBatt = document.getElementById('barBatt');
const statusBatt = document.getElementById('statusBatt');

const valDisk = document.getElementById('valDisk');

// ================== INIT & WEBSOCKET ==================

window.addEventListener('DOMContentLoaded', () => {
  connectWebSocket();
  initVisualizer();
  initWebSpeech();
  pollVitals();
  setInterval(pollVitals, 2500);
});

function connectWebSocket() {
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  const url = `${protocol}//${window.location.host}/ws`;
  socket = new WebSocket(url);

  socket.onopen = () => {
    addLog('NEURAL LINK CONNECTED. WebSocket stream established.', 'SYSTEM');
  };

  socket.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);
      if (data.type === 'log') {
        addLog(data.message, data.tag || 'JARVIS');
      } else if (data.type === 'vitals') {
        renderVitals(data.payload);
      }
    } catch (e) {
      console.error('WS Parse Error', e);
    }
  };

  socket.onclose = () => {
    setTimeout(connectWebSocket, 3000);
  };
}

// ================== MASTER POWER SWITCH ==================

async function toggleMasterPower() {
  isPoweredOn = !isPoweredOn;

  if (isPoweredOn) {
    powerBtn.classList.add('active');
    powerBtnText.textContent = '⛔ DISENGAGE (POWER OFF)';
    statusBadge.textContent = '● ARMED // ONLINE';
    statusBadge.classList.add('active');
    audioStateLbl.textContent = 'ACTIVE RESONANCE';
    waveAmplitude = 22;

    try {
      const res = await fetch('/api/power/on', { method: 'POST' });
      const data = await res.json();
      addLog(data.salute, 'JARVIS');
    } catch (err) {
      addLog('Error initializing power routine: ' + err, 'ALERT');
    }
  } else {
    powerBtn.classList.remove('active');
    powerBtnText.textContent = '⚡ ENGAGE JARVIS (POWER ON)';
    statusBadge.textContent = '● STANDBY';
    statusBadge.classList.remove('active');
    audioStateLbl.textContent = 'DORMANT';
    waveAmplitude = 4;

    try {
      await fetch('/api/power/off', { method: 'POST' });
      addLog('System safe standby engaged. Auxiliary voice and loops deactivated.', 'SYSTEM');
    } catch (err) {
      console.error(err);
    }
  }
}

// ================== DIRECTIVE DISPATCH ==================

async function submitDirective() {
  const text = cmdInput.value.trim();
  if (!text) return;

  if (!isPoweredOn) {
    addLog('Directive rejected: J.A.R.V.I.S. is currently in SAFE STANDBY. Engage Master Power first.', 'ALERT');
    return;
  }

  cmdInput.value = '';
  addLog(`Directive received: "${text}"`, 'OPERATOR');

  try {
    const res = await fetch('/api/execute', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ command: text })
    });
    const result = await res.json();
    addLog(result.message, result.status === 'success' ? 'EXECUTED' : 'ALERT');
  } catch (err) {
    addLog('Transmission error: ' + err, 'ALERT');
  }
}

cmdInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') submitDirective();
});

function executeQuickAction(commandStr) {
  if (!isPoweredOn) {
    toggleMasterPower();
  }
  cmdInput.value = commandStr;
  submitDirective();
}

// ================== VOICE DICTATION & SPEECH ==================

function initWebSpeech() {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) {
    micBtn.disabled = true;
    micBtnText.textContent = 'USE TEXT INPUT';
    return;
  }

  speechRecognizer = new SpeechRecognition();
  speechRecognizer.continuous = false;
  speechRecognizer.interimResults = false;
  speechRecognizer.lang = 'en-US';

  speechRecognizer.onstart = () => {
    isRecording = true;
    micBtn.classList.add('recording');
    micBtnText.textContent = 'LISTENING...';
    waveAmplitude = 35;
  };

  speechRecognizer.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    addLog(`Spoken Directive Captured: "${transcript}"`, 'VOICE');
    cmdInput.value = transcript;
    submitDirective();
  };

  speechRecognizer.onerror = (event) => {
    console.error('Speech error:', event.error);
    stopRecording();
  };

  speechRecognizer.onend = () => {
    stopRecording();
  };
}

function toggleSpeechRecognition() {
  if (!speechRecognizer) return;
  if (!isPoweredOn) {
    toggleMasterPower();
  }
  if (!isRecording) {
    try {
      speechRecognizer.start();
    } catch (e) {
      console.warn(e);
    }
  } else {
    speechRecognizer.stop();
  }
}

function stopRecording() {
  isRecording = false;
  micBtn.classList.remove('recording');
  micBtnText.textContent = 'HOLD TO SPEAK';
  waveAmplitude = isPoweredOn ? 20 : 4;
}

// ================== HARDWARE VITALS POLLING ==================

async function pollVitals() {
  try {
    const res = await fetch('/api/vitals');
    const vitals = await res.json();
    renderVitals(vitals);
  } catch (err) {
    // offline or restarting
  }
}

function renderVitals(v) {
  valCpu.textContent = `${v.cpu_percent}%`;
  barCpu.style.width = `${Math.min(v.cpu_percent, 100)}%`;
  statusCpu.textContent = v.cpu_percent > 80 ? 'HIGH LOAD' : 'NOMINAL';

  valRam.textContent = `${v.ram_used_gb} GB`;
  barRam.style.width = `${v.ram_percent}%`;
  statusRam.textContent = `${v.ram_percent}% LOAD`;

  valBatt.textContent = `${v.battery_percent}%`;
  barBatt.style.width = `${v.battery_percent}%`;
  statusBatt.textContent = v.battery_status;

  valDisk.textContent = `${v.disk_free_gb} GB Free`;
}

// ================== AUDIO SINE VISUALIZER ==================

function initVisualizer() {
  function draw() {
    requestAnimationFrame(draw);
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    ctx.lineWidth = 2;
    ctx.strokeStyle = isPoweredOn ? '#00f2fe' : '#232e42';
    ctx.beginPath();

    const sliceWidth = canvas.width / 50;
    let x = 0;

    for (let i = 0; i <= 50; i++) {
      const y = (canvas.height / 2) + Math.sin(i * 0.3 + wavePhase) * waveAmplitude;
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
      x += sliceWidth;
    }

    ctx.stroke();
    wavePhase += isPoweredOn ? 0.08 : 0.02;
  }
  draw();
}

// ================== EVENT LOG HELPER ==================

function addLog(msg, tag = 'JARVIS') {
  const now = new Date();
  const ts = `[${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}:${String(now.getSeconds()).padStart(2, '0')}]`;

  const div = document.createElement('div');
  div.className = `log-entry log-${tag.toLowerCase()}`;

  const tsSpan = document.createElement('span');
  tsSpan.className = 'log-ts';
  tsSpan.textContent = ts;

  const badgeSpan = document.createElement('span');
  badgeSpan.className = 'log-badge';
  badgeSpan.textContent = `[${tag}]`;

  const msgSpan = document.createElement('span');
  msgSpan.className = 'log-msg';
  msgSpan.textContent = msg;

  div.append(tsSpan, badgeSpan, msgSpan);
  feedLogs.appendChild(div);
  feedLogs.scrollTop = feedLogs.scrollHeight;
}

function clearFeed() {
  feedLogs.replaceChildren();
}
