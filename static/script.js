// Handles theme, language, timezone UI behavior
const themeToggle = document.getElementById('themeToggle');
const langSelect = document.getElementById('langSelect');
const tzSelect = document.getElementById('tzSelect');
const tzDisplay = document.getElementById('tzDisplay');
const uploadForm = document.getElementById('uploadForm');
const uploadResult = document.getElementById('uploadResult');

// Restore theme
const currentTheme = localStorage.getItem('theme') || 'light';
document.documentElement.setAttribute('data-theme', currentTheme);
themeToggle.textContent = currentTheme === 'dark' ? 'Toggle Light' : 'Toggle Dark';

themeToggle.addEventListener('click', () => {
  const t = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', t);
  localStorage.setItem('theme', t);
  themeToggle.textContent = t === 'dark' ? 'Toggle Light' : 'Toggle Dark';
});

// Language switching - simple UI label changes
const translations = {
  en: { title: 'BlockShareCloud', upload: 'Upload a File', download: 'Download a File', uploadBtn: 'Upload', downloadBtn: 'Download' },
  hi: { title: 'ब्लॉकशेयरक्लाउड', upload: 'फ़ाइल अपलोड करें', download: 'फ़ाइल डाउनलोड करें', uploadBtn: 'अपलोड', downloadBtn: 'डाउनलोड' },
  es: { title: 'NubeBlockShare', upload: 'Subir un archivo', download: 'Descargar un archivo', uploadBtn: 'Subir', downloadBtn: 'Descargar' }
};

function applyLang(lang) {
  const t = translations[lang] || translations['en'];
  document.getElementById('title').textContent = t.title;
  document.getElementById('uploadTitle').textContent = t.upload;
  document.getElementById('downloadTitle').textContent = t.download;
  document.getElementById('uploadBtn').value = t.uploadBtn;
  document.getElementById('downloadBtn').value = t.downloadBtn;
  localStorage.setItem('lang', lang);
}

const savedLang = localStorage.getItem('lang') || 'en';
langSelect.value = savedLang;
applyLang(savedLang);

langSelect.addEventListener('change', (e) => {
  applyLang(e.target.value);
});

// Timezone: call Flask endpoint which proxies Java service
function updateTimezoneDisplay(region) {
  const url = '/timezone-info' + (region ? ('?region=' + encodeURIComponent(region)) : '');
  fetch(url).then(r => r.json()).then(data => {
    if (data.error) {
      tzDisplay.textContent = 'TZ Err';
    } else {
      tzDisplay.textContent = data.timezone + ' — ' + data.datetime;
    }
  }).catch(()=>{ tzDisplay.textContent = 'TZ Err'; });
}

// Auto-detect on load
tzSelect.addEventListener('change', () => {
  const val = tzSelect.value;
  updateTimezoneDisplay(val || '');
});

// initial
updateTimezoneDisplay('');


// Upload via fetch to show JSON response (so we can show verify result from Java)
uploadForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const formData = new FormData(uploadForm);
  uploadResult.textContent = 'Uploading...';
  try {
    const resp = await fetch('/upload', { method: 'POST', body: formData });
    const j = await resp.json();
    uploadResult.textContent = 'Uploaded! Hash: ' + j.ipfs_hash + ' | Verify: ' + JSON.stringify(j.verify);
  } catch (err) {
    uploadResult.textContent = 'Upload failed: ' + err;
  }
});
