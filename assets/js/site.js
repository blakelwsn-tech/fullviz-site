/* FullViz · site.js. Four small jobs: the mobile menu, the Field Notes filter, the interview player, and the "Elsewhere" list. */
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
    var start = location.hash.replace("#", "");
    show(filters.querySelector('[data-filter="' + start + '"]') ? start : "all");
  }

  /* The interview: YouTube's player is only fetched when a visitor presses play. */
  var stage = document.querySelector(".player__screen[data-video]");
  var play = stage && stage.querySelector(".player__play");
  if (play) {
    play.addEventListener("click", function (event) {
      event.preventDefault();
      var frame = document.createElement("iframe");
      frame.src = "https://www.youtube-nocookie.com/embed/" + stage.getAttribute("data-video") +
        "?autoplay=1&rel=0&start=" + (stage.getAttribute("data-start") || 0);
      frame.title = stage.getAttribute("data-title");
      frame.setAttribute("allow", "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share");
      frame.setAttribute("referrerpolicy", "strict-origin-when-cross-origin");
      frame.setAttribute("allowfullscreen", "");
      stage.textContent = "";
      stage.appendChild(frame);
      frame.focus();
    });
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
      var row = document.createElement("div");
      row.className = "links__row";
      row.appendChild(a);
      li.appendChild(row);
      if (item.embed) {
        /* The post is only fetched from LinkedIn when a visitor asks for it. */
        var show = document.createElement("button");
        var box = document.createElement("div");
        show.type = "button";
        show.className = "links__show";
        show.setAttribute("aria-expanded", "false");
        show.textContent = "Show it here";
        box.className = "links__embed";
        box.hidden = true;
        show.addEventListener("click", function () {
          var opening = box.hidden;
          if (opening && !box.firstChild) {
            var frame = document.createElement("iframe");
            frame.src = item.embed;
            frame.title = "LinkedIn post: " + item.title;
            frame.height = item.height || 670;
            frame.width = 504;
            frame.setAttribute("frameborder", "0");
            frame.setAttribute("allowfullscreen", "");
            box.appendChild(frame);
          }
          box.hidden = !opening;
          show.setAttribute("aria-expanded", String(opening));
          show.textContent = opening ? "Hide it" : "Show it here";
        });
        row.appendChild(show);
        li.appendChild(box);
      }
      list.appendChild(li);
    });
  }
})();
