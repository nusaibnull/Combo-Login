/***** CONFIG (তোমার অনুযায়ী বদলাতে পারো) *****/
const LOGIN_URL   = "https://mytempsms.com/login";
const EMAIL_ID    = "email"; 
const PASS_ID     = "password";
const OPEN_GAP_MS = 1000;   // ট্যাব ওপেনের মধ্যে গ্যাপ (popup blocker এড়াতে)
const MAX_TABS    = 30;    // combo.txt খুব বড় হলে সেফটি ক্যাপ

/***** HELPER: একটি ট্যাবে ফিল্ড ফিল করা *****/
function fillFields(win, u, p) {
  try {
    const d = win.document;
    const emailInput =
      d.getElementById(EMAIL_ID) || d.querySelector(`[name="${EMAIL_ID}"]`);
    const passInput =
      d.getElementById(PASS_ID) || d.querySelector(`[name="${PASS_ID}"]`);

    if (!emailInput || !passInput) return false;

    emailInput.focus();
    emailInput.value = u;
    emailInput.dispatchEvent(new Event("input", { bubbles: true }));

    passInput.focus();
    passInput.value = p;
    passInput.dispatchEvent(new Event("input", { bubbles: true }));

    // ভিজ্যুয়াল ইঙ্গিত (ঐচ্ছিক)
    [emailInput, passInput].forEach(el => {
      el.style.outline = "2px solid limegreen";
      setTimeout(() => (el.style.outline = ""), 1500);
    });
    return true;
  } catch (_) { return false; }
}

/***** HELPER: একাউন্ট লিস্ট থেকে ট্যাব ওপেন + পোলিং করে ফিল্ড ফিল *****/
function openAndFillAll(accounts) {
  const list = accounts.slice(0, MAX_TABS); // সেফটি ক্যাপ
  console.log(`Preparing ${list.length} tabs (of ${accounts.length})…`);
  list.forEach((acc, idx) => {
    setTimeout(() => {
      const w = window.open(LOGIN_URL, "_blank");
      let tries = 0, maxTries = 100; // ~20s (500ms * 40)
      const poll = setInterval(() => {
        tries++;
        if (!w || w.closed) { clearInterval(poll); return; }
        const ok = fillFields(w, acc.user, acc.pass);
        if (ok || tries >= maxTries) clearInterval(poll);
      }, 1000);
    }, idx * OPEN_GAP_MS);
  });
}

/***** FILE PICKER: combo.txt আপলোড করে পড়া *****/
(function pickFileAndRun(){
  const input = document.createElement("input");
  input.type = "file";
  input.accept = ".txt,text/plain";
  input.style.display = "none";
  document.body.appendChild(input);

  input.addEventListener("change", () => {
    const file = input.files && input.files[0];
    if (!file) { console.warn("No file selected."); input.remove(); return; }

    const reader = new FileReader();
    reader.onload = () => {
      const text = String(reader.result || "");
      // প্রতি লাইনে username:password — মন্তব্য (#) বা ফাঁকা লাইন স্কিপ
      const accounts = text
        .split(/\r?\n/)
        .map(l => l.trim())
        .filter(l => l && !l.startsWith("#"))
        .map(l => {
          const i = l.indexOf(":");           // প্রথম কোলনেই split (password-এ কোলন থাকলে বাকিটা পাসওয়ার্ড)
          if (i < 1) return null;
          const user = l.slice(0, i).trim();
          const pass = l.slice(i + 1).trim();
          return (user && pass) ? { user, pass } : null;
        })
        .filter(Boolean);

      if (!accounts.length) {
        console.error("No valid lines found in combo.txt (format: username:password).");
        input.remove();
        return;
      }
      console.log(`Loaded ${accounts.length} accounts from file.`);
      openAndFillAll(accounts);
      input.remove();
    };
    reader.onerror = (e) => {
      console.error("Failed to read file:", e);
      input.remove();
    };
    reader.readAsText(file);
  });

  // ফাইল সিলেক্ট ডায়ালগ খুলবে
  input.click();
})();
