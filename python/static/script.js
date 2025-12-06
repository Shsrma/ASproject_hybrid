// =============================
// ELEMENTS
// =============================
const themeToggle = document.getElementById("themeToggle");
const langSelect = document.getElementById("langSelect");
const tzSelect = document.getElementById("tzSelect");
const tzDisplay = document.getElementById("tzDisplay");

const uploadForm = document.getElementById("uploadForm");
const uploadResult = document.getElementById("uploadResult");

const downloadBtn = document.getElementById("downloadBtn");
const hashInput = document.getElementById("hashInput");

// =============================
// THEME SYSTEM
// =============================
const savedTheme = localStorage.getItem("theme") || "light";
document.documentElement.setAttribute("data-theme", savedTheme);

themeToggle.textContent =
  savedTheme === "dark" ? "Light Mode" : "Dark Mode";

themeToggle.addEventListener("click", () => {
  const newTheme =
    document.documentElement.getAttribute("data-theme") === "dark"
      ? "light"
      : "dark";

  document.documentElement.setAttribute("data-theme", newTheme);
  localStorage.setItem("theme", newTheme);

  themeToggle.textContent =
    newTheme === "dark" ? "Light Mode" : "Dark Mode";
});

// =============================
// LANGUAGE SYSTEM
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

langSelect.value = localStorage.getItem("lang") || "en";
applyLang(langSelect.value);

langSelect.addEventListener("change", (e) => applyLang(e.target.value));

// =============================
// TIMEZONE
// =============================
function updateTimezoneDisplay(region = "") {
  const url = region
    ? `/timezone-info?region=${encodeURIComponent(region)}`
    : "/timezone-info";

  fetch(url)
    .then((r) => r.json())
    .then((data) => {
      tzDisplay.textContent = data.timezone
        ? `${data.timezone} — ${data.datetime}`
        : "Timezone Error";
    })
    .catch(() => {
      tzDisplay.textContent = "TZ Error";
    });
}

tzSelect.addEventListener("change", () => {
  updateTimezoneDisplay(tzSelect.value || "");
});

updateTimezoneDisplay();

// =============================
// FILE UPLOAD
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
      uploadResult.textContent = "Upload Error: " + json.error;
      return;
    }

    uploadResult.innerHTML =
      `✔ Uploaded!\nIPFS Hash:\n${json.ipfs_hash}\n\n` +
      `Blockchain Verify:\n${JSON.stringify(json.verify)}`;
  } catch (err) {
    uploadResult.textContent = "Upload failed: " + err.message;
  }
});

// =============================
// DOWNLOAD
// =============================
downloadBtn.addEventListener("click", () => {
  if (!hashInput.value.trim()) {
    alert("Please enter an IPFS hash.");
    return;
  }
  document.getElementById("downloadForm").submit();
});
