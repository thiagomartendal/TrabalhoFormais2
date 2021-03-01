// Impede reenvio de formulário
if ( window.history.replaceState ) {
  window.history.replaceState( null, null, window.location.href );
}

function novoAF() {
  document.getElementById("fazer-gramatica").style.display = "none"
  let x = document.getElementById("fazer-automato")
  if (x.style.display === "none" || x.style.display === "") {
    x.style.display = "block"
  } else {
    x.style.display = "none"
  }
}

function novaGR() {
  document.getElementById("fazer-automato").style.display = "none"
  let x = document.getElementById("fazer-gramatica")
  if (x.style.display === "none" || x.style.display === "") {
    x.style.display = "block"
  } else {
    x.style.display = "none"
  }
}
