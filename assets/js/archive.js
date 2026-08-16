(function () {
  const buttons = document.querySelectorAll("[data-filter]");
  const cards = document.querySelectorAll("[data-subject]");
  const empty = document.querySelector("[data-empty]");
  if (!buttons.length) return;

  function apply(subject) {
    let visible = 0;
    cards.forEach(function (card) {
      const show = subject === "all" || card.getAttribute("data-subject") === subject;
      card.hidden = !show;
      if (show) visible += 1;
    });
    if (empty) empty.hidden = visible !== 0;
    buttons.forEach(function (btn) {
      const on = btn.getAttribute("data-filter") === subject;
      btn.setAttribute("aria-pressed", on ? "true" : "false");
    });
  }

  buttons.forEach(function (btn) {
    btn.addEventListener("click", function () {
      apply(btn.getAttribute("data-filter"));
    });
  });
})();
