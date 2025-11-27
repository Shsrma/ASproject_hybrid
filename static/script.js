// =============================
// ELEMENT REFERENCES
// =============================
const themeToggle = document.getElementById("themeToggle");
const langSelect = document.getElementById("langSelect");
const tzSelect = document.getElementById("tzSelect");
const tzDisplay = document.getElementById("tzDisplay");

const uploadForm = document.getElementById("uploadForm");
const uploadResult = document.getElementById("uploadResult");

const downloadBtn = document.getElementById("downloadBtn"); // NEW
const hashInput = document.getElementById("hashInput");     // NEW

// =============================
// THEME TOGGLE
// =============================
const savedTheme = localStorage.getItem("theme") || "light";
document.documentElement.setAttribute("data-theme", savedTheme);
themeToggle.textContent =
  savedTheme === "dark" ? "Toggle Light" : "Toggle Dark";

themeToggle.addEventListener("click", () => {
  const newTheme =
    document.documentElement.getAttribute("data-theme") === "dark"
      ? "light"
      : "dark";

  document.documentElement.setAttribute("data-theme", newTheme);
  localStorage.setItem("theme", newTheme);
  themeToggle.textContent =
    newTheme === "dark" ? "Toggle Light" : "Toggle Dark";
});

// =============================
// LANGUAGE TRANSLATION SYSTEM
// =============================
const translations = {
  en: {
    title: "BlockShareCloud",
    upload: "Upload a File",
    download: "Download a File",
    uploadBtn: "Upload",
    downloadBtn: "Download",
  },
  hi: {
    title: "ब्लॉकशेयरक्लाउड",
    upload: "फ़ाइल अपलोड करें",
    download: "फ़ाइल डाउनलोड करें",
    uploadBtn: "अपलोड",
    downloadBtn: "डाउनलोड",
  },
  es: {
    title: "NubeBlockShare",
    upload: "Subir un archivo",
    download: "Descargar un archivo",
    uploadBtn: "Subir",
    downloadBtn: "Descargar",
  },
};

function applyLang(lang) {
  const t = translations[lang] || translations.en;

  document.getElementById("title").textContent = t.title;
  document.getElementById("uploadTitle").textContent = t.upload;
  document.getElementById("downloadTitle").textContent = t.download;

  document.getElementById("uploadBtn").textContent = t.uploadBtn;
  document.getElementById("downloadBtn").textContent = t.downloadBtn;

  localStorage.setItem("lang", lang);
}

const savedLang = localStorage.getItem("lang") || "en";
langSelect.value = savedLang;
applyLang(savedLang);

langSelect.addEventListener("change", (e) =>
  applyLang(e.target.value)
);

// =============================
// TIMEZONE SYSTEM
// =============================
function updateTimezoneDisplay(region = "") {
  const url = region
    ? `/timezone-info?region=${encodeURIComponent(region)}`
    : "/timezone-info";

  fetch(url)
    .then((r) => r.json())
    .then((data) => {
      if (data.error) {
        tzDisplay.textContent = "Timezone Error";
      } else {
        tzDisplay.textContent = `${data.timezone} — ${data.datetime}`;
      }
    })
    .catch(() => {
      tzDisplay.textContent = "TZ Error";
    });
}

tzSelect.addEventListener("change", () => {
  const region = tzSelect.value;
  updateTimezoneDisplay(region || "");
});

updateTimezoneDisplay();

// =============================
// FILE UPLOAD SYSTEM (AJAX)
// =============================
uploadForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  uploadResult.textContent = "Uploading...";
  const formData = new FormData(uploadForm);

  try {
    const resp = await fetch("/upload", {
      method: "POST",
      body: formData,
    });

    const json = await resp.json();

    if (json.error) {
      uploadResult.textContent = "Upload error: " + json.error;
      return;
    }

    uploadResult.innerHTML =
      `✅ <b>Uploaded!</b><br>IPFS Hash:<br><code>${json.ipfs_hash}</code><br><br>` +
      `Blockchain Verify:<br><code>${JSON.stringify(json.verify)}</code>`;
  } catch (err) {
    uploadResult.textContent = "Upload failed: " + err.message;
  }
});

// =============================
// DOWNLOAD BUTTON HANDLER
// =============================
downloadBtn.addEventListener("click", () => {
  if (!hashInput.value.trim()) {
    alert("Please enter an IPFS hash.");
    return;
  }

  document.getElementById("downloadForm").submit();
});
