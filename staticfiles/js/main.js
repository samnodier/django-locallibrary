document.addEventListener('click', (e) => {
	if(e.target.classList.contains('fa')) {
		document.querySelector('.fa-times').classList.toggle('show');
		document.querySelector('.fa-bars').classList.toggle('hide');
		document.querySelector('.nav-list').classList.toggle('toggle-on');
		document.querySelector('.btn-container').classList.toggle('toggle-on');
	}
})
