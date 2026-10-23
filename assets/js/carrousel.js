// Carrousel de photos de la page À propos.
// Les photos défilent toutes seules (une toutes les 5 secondes) et se mettent
// en pause quand la souris est dessus. Flèches et points pour naviguer.
(function () {
	var c = document.querySelector('.carrousel');
	if (!c) return;
	var DELAI = 5000; // millisecondes entre deux photos

	var photos = c.querySelectorAll('.carrousel-piste img');
	var zonePoints = c.querySelector('.carrousel-points');
	var anglais = document.documentElement.lang === 'en';
	var reduire = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
	var actuelle = 0, minuterie = null;

	photos.forEach(function (_, i) {
		var p = document.createElement('button');
		p.type = 'button';
		p.setAttribute('aria-label', (anglais ? 'Photo ' : 'Photo ') + (i + 1));
		p.addEventListener('click', function () { montrer(i); relancer(); });
		zonePoints.appendChild(p);
	});
	var points = zonePoints.querySelectorAll('button');

	function montrer(i) {
		actuelle = (i + photos.length) % photos.length;
		photos.forEach(function (img, k) { img.classList.toggle('actif', k === actuelle); });
		points.forEach(function (p, k) { p.classList.toggle('actif', k === actuelle); });
	}
	function suivante() { montrer(actuelle + 1); }
	function arreter() { clearInterval(minuterie); minuterie = null; }
	function relancer() { arreter(); if (!reduire) minuterie = setInterval(suivante, DELAI); }

	c.querySelector('.carrousel-prec').addEventListener('click', function () { montrer(actuelle - 1); relancer(); });
	c.querySelector('.carrousel-suiv').addEventListener('click', function () { suivante(); relancer(); });
	c.addEventListener('mouseenter', arreter);
	c.addEventListener('mouseleave', relancer);
	c.addEventListener('focusin', arreter);
	c.addEventListener('focusout', relancer);
	document.addEventListener('visibilitychange', function () { if (document.hidden) arreter(); else relancer(); });

	montrer(0);
	relancer();
})();
