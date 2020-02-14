

const yearBirth = document.getElementById("year-birth");

yearBirth.addEventListener('click', function(){
	for(i = 2018; i > 1880; i--){
		let year = document.createElement('option');
		year.innerHTML = i;
		yearBirth.appendChild(year);
	}
});

document.getElementById("log-in-link").addEventListener('click', function(){

	document.getElementById("almost-everything").style.opacity = 0.1;

	let logInBox = document.getElementById('log-in-box');
	logInBox.style.display = "block";

});



(function() {
  'use strict';
  window.addEventListener('load', function() {
    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    var forms = document.getElementsByClassName('needs-validation');
    // Loop over them and prevent submission
    var validation = Array.prototype.filter.call(forms, function(form) {
      form.addEventListener('submit', function(event) {
        if (form.checkValidity() === false) {
          event.preventDefault();
          event.stopPropagation();
        }
        form.classList.add('was-validated');
      }, false);
    });
  }, false);
})();