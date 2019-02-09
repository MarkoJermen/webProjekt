//SLIDER
//==========================

	var i = 0;
	var images = [];
	var time = 6000;
	 
	//Images list				 
	images [0] = 'static/img/img1.jpg';
	images [1] = 'static/img/img2.jpg';
	images [2] = 'static/img/img3.jpg';
	images [3] = 'static/img/img4.jpg';
						
	// Change image					
	function changeImg(){
	document.slide.src = images [i];
							
		if(i < images.length - 1) {
		i++;
		} else {
		i = 0;
		}
			
	setTimeout("changeImg()", time);
						
	}	
						
	window.onload =  changeImg;
	
//ACCORDION
//==========================

	var acc = document.getElementsByClassName("accordion");
	var i;

	for (i = 0; i < acc.length; i++) {
	  acc[i].addEventListener("click", function() {
		this.classList.toggle("active");
		var panel = this.nextElementSibling;
		if (panel.style.display === "block") {
		  panel.style.display = "none";
		} else {
		  panel.style.display = "block";
		}
	  });
	}

