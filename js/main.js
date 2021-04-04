//responsive header

var path = window.location.pathname;
if(path == "/" || path == "/index"){
	document.getElementById("bouton_navigation_article").hidden = false;
}

var yd = 0;
window.onscroll = function (e){
	var y = this.scrollY;
	if (y > 200){
		if (yd > y){
			document.getElementsByTagName("header")[0].style.top = "0";
			document.getElementsByTagName("header")[0].style.borderRadius = "0 0 50% 50%";
		}else{
			document.getElementsByTagName("header")[0].style.top = "-100px";
			document.getElementsByTagName("header")[0].style.borderRadius = "0";
		}

		yd = y;
	}else{
		document.getElementsByTagName("header")[0].style.top = "0";
		document.getElementsByTagName("header")[0].style.borderRadius = "0 0 50% 50%";
	}

	//actualisation du bouton de navigation
	if (y > document.getElementById("section_presentation").clientHeight + 100){
		document.getElementById("bouton_navigation_article").textContent = "Aller en haut";
	}else{
		document.getElementById("bouton_navigation_article").textContent = "Voir le contenue du CV";
	}
}

//scrolleur
document.getElementById("bouton_navigation_article").onclick = function (){
	if (window.scrollY < document.getElementById("section_presentation").clientHeight + 100){
		document.getElementById("section_infos").scrollIntoView({behavior: "smooth"});
	}else{
		document.body.scrollIntoView({behavior: "smooth"});
	}
}
