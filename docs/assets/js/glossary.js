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

  function fold(s) {
    return String(s || "")
      .normalize("NFC")
      .replace(/[\u201c\u201d\u201e\u00ab\u00bb]/g, '"')
      .replace(/[\u2018\u2019]/g, "'")
      .replace(/[*_]/g, "")
      .replace(/\s+/g, " ")
      .trim()
      .toLowerCase();
  }

  function foldAccents(s) {
    return fold(s).normalize("NFD").replace(/\p{M}/gu, "");
  }

  function stripPossessive(s) {
    return s.replace(/['’]s$/i, "").replace(/['’]$/i, "");
  }

  function lookup(phrase) {
    const raw = fold(phrase);
    if (!raw) return null;
    const variants = [raw, stripPossessive(raw), foldAccents(raw), foldAccents(stripPossessive(raw))];
    const seen = {};
    const queries = [];
    variants.forEach(function (q) {
      if (q && !seen[q]) {
        seen[q] = true;
        queries.push(q);
      }
    });

    function namesOf(entry) {
      return [entry.term].concat(entry.aliases || []).map(function (n) {
        return fold(n);
      });
    }

    function namesFolded(entry) {
      return [entry.term].concat(entry.aliases || []).map(function (n) {
        return foldAccents(n);
      });
    }

    for (let i = 0; i < entries.length; i += 1) {
      const names = namesOf(entries[i]);
      for (let q = 0; q < queries.length; q += 1) {
        if (names.indexOf(queries[q]) !== -1) return entries[i];
      }
    }
    for (let i = 0; i < entries.length; i += 1) {
      const names = namesFolded(entries[i]);
      for (let q = 0; q < queries.length; q += 1) {
        if (names.indexOf(queries[q]) !== -1) return entries[i];
      }
    }
    for (let i = 0; i < entries.length; i += 1) {
      const entry = entries[i];
      const names = namesOf(entry).concat(namesFolded(entry));
      for (let j = 0; j < names.length; j += 1) {
        const n = names[j];
        for (let q = 0; q < queries.length; q += 1) {
          const query = queries[q];
          if (n && query && (query.indexOf(n) !== -1 || n.indexOf(query) !== -1) && Math.min(query.length, n.length) >= 3) {
            return entry;
          }
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
