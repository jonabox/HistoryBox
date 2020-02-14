document.getElementById("profile-picture").addEventListener("click", function(){
	document.getElementById("almost-everything").style.opacity = 0.1;
	

	const image = document.createElement("img");
	image.src = "../static/images/bg.jpg";
	image.style.position = "absolute";
	image.style.top = "10%"
	image.style.height = "80%";
	image.style.width = "auto";
	image.style.maxWidth = "100%";
	document.getElementById("body").appendChild(image)


});