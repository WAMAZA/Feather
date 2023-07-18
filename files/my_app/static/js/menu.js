// Fonction qui sert à souligner la page sur laquelle on se trouve dans le menu
function underlineActivePage () {
  const activePage = window.location.href;
  const navLinks = document.querySelectorAll('.navbar ul a');
  const span = document.querySelectorAll('.navbar ul li a');

  for(let i = 0; i < span.length; i++){
    if(navLinks[i].href === activePage){
      span[i].style.textDecoration = "underline"
    }
  }
}

underlineActivePage()

