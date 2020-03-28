// Owl Related
$('.dis-owl').owlCarousel({
	loop:true,
	margin:20,
	nav:true,
	navText: ["<i class='fa fa-chevron-left'></i>", "<i class='fa fa-chevron-right'></i>"],
	responsive:{
		0:{
			items:1
		},
		600:{
			items:2
		},
		1000:{
			items:5
		}
	}
})


// Owl browse
$('.browse-owl').owlCarousel({
	loop:true,
	margin:30,
	nav:false,
	autoplay:true,
	autoplayTimeout:5000,
	autoplayHoverPause:true,
	responsive:{
		0:{
			items:1
		},
		600:{
			items:3
		},
		1000:{
			items:6
		}
	}
})

// Owl browse
$('.searchs-owl').owlCarousel({
	loop:true,
	margin:30,
	nav:false,
	autoplay:true,
	autoplayTimeout:5000,
	autoplayHoverPause:true,
	responsive:{
		0:{
			items:1
		},
		600:{
			items:3
		},
		1000:{
			items:5
		}
	}
})