// Impede reenvio de formulário
if ( window.history.replaceState ) {
  window.history.replaceState( null, null, window.location.href );
}

function novoAF() {
  document.getElementById("fazer-gramatica").style.display = "none"
  document.getElementById("fazer-expressao").style.display = "none"
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
  let x = document.getElementById("fazer-expressao")
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
