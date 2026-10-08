/* FullViz · site.js. Three small jobs: the mobile menu, the Field Notes filter, and the "Elsewhere" list. */
(function () {
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", String(open));
    });
  }

  /* Field Notes: show cards by domain. A hash like #returns picks a filter on load. */
  var filters = document.querySelector(".filters");
  var cards = document.querySelectorAll("#note-cards .card");
  var count = document.querySelector(".filter-count");
  if (filters && cards.length) {
    var buttons = filters.querySelectorAll(".filter");
    var show = function (key) {
      var shown = 0;
      cards.forEach(function (card) {
        var match = key === "all" || (" " + card.getAttribute("data-domains") + " ").indexOf(" " + key + " ") > -1;
        card.hidden = !match;
        if (match) { shown += 1; }
      });
      buttons.forEach(function (b) {
        b.setAttribute("aria-pressed", String(b.getAttribute("data-filter") === key));
      });
      if (count) {
        count.hidden = false;
        count.textContent = "Showing " + shown + " of " + cards.length;
      }
    };
    buttons.forEach(function (b) {
      b.addEventListener("click", function () {
        var key = b.getAttribute("data-filter");
        show(key);
        history.replaceState(null, "", key === "all" ? location.pathname : "#" + key);
      });
    });
    filters.hidden = false;
    var start = location.hash.replace("#", "");
    show(filters.querySelector('[data-filter="' + start + '"]') ? start : "all");
  }

  var list = document.getElementById("writing-list");
  var items = window.FULLVIZ_WRITING;
  if (list && items && items.length) {
    list.textContent = "";
    items.forEach(function (item) {
      var li = document.createElement("li");
      var a = document.createElement("a");
      var title = document.createElement("strong");
      var source = document.createElement("span");
      a.href = item.url;
      a.rel = "noopener";
      title.textContent = item.title;
      source.textContent = item.source || "";
      a.appendChild(title);
      a.appendChild(source);
      li.appendChild(a);
      list.appendChild(li);
    });
  }
})();
