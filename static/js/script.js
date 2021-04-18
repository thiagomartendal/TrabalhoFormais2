if ( window.history.replaceState ) {
  window.history.replaceState( null, null, window.location.href );
}

function novoAF() {
  document.getElementById("fazer-gramatica").style.display = "none"
  document.getElementById("fazer-expressao").style.display = "none"
  document.getElementById("interseccao-automatos").style.display = "none"
  document.getElementById("uniao-automatos").style.display = "none"
  document.getElementById("reconhecimento-lexico").style.display = "none"
  let x = document.getElementById("fazer-automato")
  if (x.style.display === "none" || x.style.display === "") {
    x.style.display = "block"
  } else {
    x.style.display = "none"
  }
}

function novaGR() {
  document.getElementById("fazer-automato").style.display = "none"
  document.getElementById("fazer-expressao").style.display = "none"
  document.getElementById("interseccao-automatos").style.display = "none"
  document.getElementById("uniao-automatos").style.display = "none"
  document.getElementById("reconhecimento-lexico").style.display = "none"
  let x = document.getElementById("fazer-gramatica")
  if (x.style.display === "none" || x.style.display === "") {
    x.style.display = "block"
  } else {
    x.style.display = "none"
  }
}

function novaER() {
  document.getElementById("fazer-automato").style.display = "none"
  document.getElementById("fazer-gramatica").style.display = "none"
  document.getElementById("interseccao-automatos").style.display = "none"
  document.getElementById("uniao-automatos").style.display = "none"
  document.getElementById("reconhecimento-lexico").style.display = "none"
  let x = document.getElementById("fazer-expressao")
  if (x.style.display === "none" || x.style.display === "") {
    x.style.display = "block"
  } else {
    x.style.display = "none"
  }
}

function uniaoAF() {
  document.getElementById("fazer-automato").style.display = "none"
  document.getElementById("fazer-gramatica").style.display = "none"
  document.getElementById("fazer-expressao").style.display = "none"
  document.getElementById("interseccao-automatos").style.display = "none"
  document.getElementById("reconhecimento-lexico").style.display = "none"
  let x = document.getElementById("uniao-automatos")
  if (x.style.display === "none" || x.style.display === "") {
    x.style.display = "block"
  } else {
    x.style.display = "none"
  }
}

function interseccaoAF() {
  document.getElementById("fazer-automato").style.display = "none"
  document.getElementById("fazer-gramatica").style.display = "none"
  document.getElementById("fazer-expressao").style.display = "none"
  document.getElementById("uniao-automatos").style.display = "none"
  document.getElementById("reconhecimento-lexico").style.display = "none"
  let x = document.getElementById("interseccao-automatos")
  if (x.style.display === "none" || x.style.display === "") {
    x.style.display = "block"
  } else {
    x.style.display = "none"
  }
}

function reconhecimentoLexico() {
  document.getElementById("fazer-automato").style.display = "none"
  document.getElementById("fazer-gramatica").style.display = "none"
  document.getElementById("fazer-expressao").style.display = "none"
  document.getElementById("uniao-automatos").style.display = "none"
  document.getElementById("interseccao-automatos").style.display = "none"
  let x = document.getElementById("reconhecimento-lexico")
  if (x.style.display === "none" || x.style.display === "") {
    x.style.display = "block"
  } else {
    x.style.display = "none"
  }
}

function posItem(pos) {
  window.history.replaceState(null, null, "?pos="+pos)
}

function limpaURL() {
  window.history.pushState({}, document.title, "/")
}

// function numeroLinha(id) {
//   var caixaTexto = document.getElementById(id)
//   var areaLinhas = document.getElementById("linhasAutomato")
//   caixaTexto.addEventListener("keypress", function(event) {
//     var tecla = event.which || event.keyCode
//     if (tecla == 13) {
//       var linhas = caixaTexto.innerHTML.split("\n")
//       console.log(linhas)
//       console.log(linhas.length)
//       areaLinhas.innerHTML += (linhas.length)+"<br />"
//     }
//   })
// }

// function parametroURL(sParam) {
//   var sPageURL = window.location.search.substring(1);
//   var sURLVariables = sPageURL.split('&');
//   for (var i = 0; i < sURLVariables.length; i++) {
//     var sParameterName = sURLVariables[i].split('=');
//     if (sParameterName[0] == sParam) {
//       return sParameterName[1];
//     }
//   }
// }​
