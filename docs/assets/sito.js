// Indice laterale, pagina attiva e pulsanti "Copia" sui blocchi di comandi.
(function () {
  var PAGINE = [
    { gruppo: "Inizio" },
    { file: "index.html", titolo: "Benvenuto", durata: "10'" },
    { file: "lab0.html", titolo: "Lab 0 · L'ambiente", durata: "10'" },
    { gruppo: "Costruire l'agente" },
    { file: "lab1.html", titolo: "Lab 1 · Runtime", durata: "25'" },
    { file: "lab2.html", titolo: "Lab 2 · Memory", durata: "25'" },
    { file: "lab3.html", titolo: "Lab 3 · Gateway e Identity", durata: "25'" },
    { file: "lab4.html", titolo: "Lab 4 · Policy", durata: "15'" },
    { file: "lab5.html", titolo: "Lab 5 · Code Interpreter e Browser", durata: "20'" },
    { gruppo: "Gestire l'agente" },
    { file: "lab6.html", titolo: "Lab 6 · Observability ed Evaluations", durata: "25'" },
    { file: "bonus.html", titolo: "Bonus · Agente senza codice", durata: "" },
    { file: "pulizia.html", titolo: "Pulizia finale", durata: "7'" },
  ];

  var corrente = location.pathname.split("/").pop() || "index.html";

  var nav = document.querySelector("nav.indice");
  if (nav) {
    PAGINE.forEach(function (p) {
      if (p.gruppo) {
        var g = document.createElement("div");
        g.className = "gruppo";
        g.textContent = p.gruppo;
        nav.appendChild(g);
        return;
      }
      var a = document.createElement("a");
      a.href = p.file;
      a.textContent = p.titolo;
      if (p.durata) {
        var d = document.createElement("span");
        d.className = "durata";
        d.textContent = p.durata;
        a.appendChild(d);
      }
      if (p.file === corrente) a.className = "attivo";
      nav.appendChild(a);
    });
  }

  var bottone = document.querySelector(".menu-bottone");
  if (bottone && nav) {
    bottone.addEventListener("click", function () { nav.classList.toggle("aperto"); });
  }

  // Navigazione precedente / successiva in fondo alla pagina
  var solo = PAGINE.filter(function (p) { return p.file; });
  var i = solo.findIndex(function (p) { return p.file === corrente; });
  var main = document.querySelector("main");
  if (main && i >= 0) {
    var barra = document.createElement("div");
    barra.className = "navigazione";
    var sx = document.createElement("span");
    var dx = document.createElement("span");
    if (i > 0) { sx.innerHTML = '<a href="' + solo[i - 1].file + '">&larr; ' + solo[i - 1].titolo + "</a>"; }
    if (i < solo.length - 1) { dx.innerHTML = '<a href="' + solo[i + 1].file + '">' + solo[i + 1].titolo + " &rarr;</a>"; }
    barra.appendChild(sx);
    barra.appendChild(dx);
    main.appendChild(barra);
  }

  // Pulsante "Copia" su ogni blocco di comandi
  document.querySelectorAll(".blocco").forEach(function (blocco) {
    var pre = blocco.querySelector("pre");
    if (!pre) return;
    var b = document.createElement("button");
    b.className = "copia";
    b.type = "button";
    b.textContent = "Copia";
    b.addEventListener("click", function () {
      var testo = pre.innerText.replace(/\n$/, "");
      var fatto = function () {
        b.textContent = "Copiato";
        setTimeout(function () { b.textContent = "Copia"; }, 1500);
      };
      if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(testo).then(fatto);
      } else {
        var t = document.createElement("textarea");
        t.value = testo;
        document.body.appendChild(t);
        t.select();
        document.execCommand("copy");
        document.body.removeChild(t);
        fatto();
      }
    });
    blocco.appendChild(b);
  });
})();
