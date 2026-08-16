(function () {
  const dataEl = document.getElementById("glossary-data");
  const panel = document.getElementById("explain");
  if (!dataEl || !panel) return;

  let entries = [];
  try {
    entries = JSON.parse(dataEl.textContent || "[]");
  } catch (err) {
    entries = [];
  }

  const termEl = panel.querySelector("[data-explain-term]");
  const bodyEl = panel.querySelector("[data-explain-body]");
  const closeBtn = panel.querySelector("[data-explain-close]");

  function norm(s) {
    return String(s || "")
      .replace(/\s+/g, " ")
      .trim()
      .toLowerCase();
  }

  function lookup(phrase) {
    const q = norm(phrase);
    if (!q) return null;
    for (let i = 0; i < entries.length; i += 1) {
      const entry = entries[i];
      const names = [entry.term].concat(entry.aliases || []);
      for (let j = 0; j < names.length; j += 1) {
        if (norm(names[j]) === q) return entry;
      }
    }
    for (let i = 0; i < entries.length; i += 1) {
      const entry = entries[i];
      const names = [entry.term].concat(entry.aliases || []);
      for (let j = 0; j < names.length; j += 1) {
        const n = norm(names[j]);
        if (n && (q.indexOf(n) !== -1 || n.indexOf(q) !== -1) && Math.min(q.length, n.length) >= 3) {
          return entry;
        }
      }
    }
    return null;
  }

  function openPanel(title, text, found) {
    panel.hidden = false;
    panel.classList.toggle("is-fallback", !found);
    if (termEl) termEl.textContent = title;
    if (bodyEl) bodyEl.textContent = text;
    document.body.classList.add("explain-open");
  }

  function closePanel() {
    panel.hidden = true;
    document.body.classList.remove("explain-open");
  }

  function showEntry(entry, fallbackPhrase) {
    if (entry) {
      openPanel(entry.term, entry.explain, true);
    } else {
      const phrase = (fallbackPhrase || "").replace(/\s+/g, " ").trim();
      const label = phrase ? "“" + phrase + "”" : "This selection";
      openPanel(label, "No entry for this.", false);
    }
  }

  document.addEventListener("click", function (event) {
    const term = event.target.closest(".term");
    if (term) {
      event.preventDefault();
      const wanted = term.getAttribute("data-term") || term.textContent;
      const entry = lookup(wanted) || lookup(term.textContent);
      showEntry(entry, term.textContent);
      return;
    }
    if (event.target.closest("[data-explain-close]")) {
      closePanel();
      return;
    }
    if (!panel.hidden && !event.target.closest(".explain") && !event.target.closest(".term")) {
      // leave open; selection handler may reuse it
    }
  });

  if (closeBtn) {
    closeBtn.addEventListener("click", closePanel);
  }

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") closePanel();
  });

  function selectionPhrase() {
    const sel = window.getSelection();
    if (!sel || sel.isCollapsed) return "";
    const text = String(sel.toString() || "").replace(/\s+/g, " ").trim();
    if (text.length < 2 || text.length > 80) return "";
    const anchor = sel.anchorNode && sel.anchorNode.parentElement;
    if (anchor && (anchor.closest(".explain") || anchor.closest("input, textarea, .search"))) return "";
    const lesson = document.querySelector(".lesson");
    if (lesson && anchor && !lesson.contains(anchor)) return "";
    return text;
  }

  let selectTimer = 0;
  function onSelect() {
    window.clearTimeout(selectTimer);
    selectTimer = window.setTimeout(function () {
      const phrase = selectionPhrase();
      if (!phrase) return;
      showEntry(lookup(phrase), phrase);
    }, 180);
  }

  document.addEventListener("mouseup", onSelect);
  document.addEventListener("touchend", onSelect);
  document.addEventListener("keyup", function (event) {
    if (event.key === "Shift" || event.shiftKey) onSelect();
  });
})();
