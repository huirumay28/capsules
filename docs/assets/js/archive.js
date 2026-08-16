(function () {
  const buttons = document.querySelectorAll("[data-filter]");
  const cards = document.querySelectorAll(".card[data-subject]");
  const empties = document.querySelectorAll("[data-empty]");
  const search = document.querySelector("#archive-search");
  if (!buttons.length && !search) return;

  let subject = "all";
  let query = "";

  function apply() {
    const q = query.trim().toLowerCase();
    let visible = 0;
    cards.forEach(function (card) {
      const matchSubject = subject === "all" || card.getAttribute("data-subject") === subject;
      const hay = card.getAttribute("data-search") || "";
      const matchQuery = !q || hay.indexOf(q) !== -1;
      const show = matchSubject && matchQuery;
      card.hidden = !show;
      if (show) visible += 1;
    });
    empties.forEach(function (empty) {
      const block = empty.closest("[data-week]");
      let count = 0;
      const scope = block ? block.querySelectorAll(".card[data-subject]") : cards;
      scope.forEach(function (card) {
        if (!card.hidden) count += 1;
      });
      empty.hidden = count !== 0;
      if (!count) {
        empty.textContent = q
          ? "Nothing matches. Try another word, or clear the search."
          : (block && block.getAttribute("data-week") === "previous"
            ? "No earlier capsules yet."
            : "No capsules in this subject yet.");
      }
    });
    buttons.forEach(function (btn) {
      const on = btn.getAttribute("data-filter") === subject;
      btn.setAttribute("aria-pressed", on ? "true" : "false");
    });
  }

  buttons.forEach(function (btn) {
    btn.addEventListener("click", function () {
      subject = btn.getAttribute("data-filter") || "all";
      apply();
    });
  });

  if (search) {
    search.addEventListener("input", function () {
      query = search.value || "";
      apply();
    });
  }
})();
