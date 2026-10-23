// Galerie de photos de la page Hors campus.
// Un clic sur la photo d'un voyage ouvre toutes ses photos en grand.
// Flèches du clavier ou boutons pour naviguer, Échap ou clic à côté pour fermer.
(function () {
	var voyages = document.querySelectorAll('.voyage[data-photos]');
	if (!voyages.length) return;

	var anglais = document.documentElement.lang === 'en';
	var mots = anglais
		? { fermer: 'Close', prec: 'Previous photo', suiv: 'Next photo', sur: 'of' }
		: { fermer: 'Fermer', prec: 'Photo précédente', suiv: 'Photo suivante', sur: 'sur' };

	// Construction de la visionneuse (une seule pour toute la page)
	var boite = document.createElement('dialog');
	boite.className = 'visionneuse';
	boite.innerHTML =
		'<figure><img alt="" /><figcaption></figcaption></figure>' +
		'<button type="button" class="v-prec" aria-label="' + mots.prec + '">&#8249;</button>' +
		'<button type="button" class="v-suiv" aria-label="' + mots.suiv + '">&#8250;</button>' +
		'<button type="button" class="v-fermer" aria-label="' + mots.fermer + '">&#215;</button>';
	document.body.appendChild(boite);

	var image = boite.querySelector('img');
	var legende = boite.querySelector('figcaption');
	var photos = [], titre = '', position = 0;

	function afficher(i) {
		position = (i + photos.length) % photos.length;
		image.src = photos[position];
		image.alt = titre + ' (' + (position + 1) + ' ' + mots.sur + ' ' + photos.length + ')';
		legende.textContent = titre + '   ' + (position + 1) + ' / ' + photos.length;
		// Précharge la photo suivante
		new Image().src = photos[(position + 1) % photos.length];
	}

	voyages.forEach(function (v) {
		v.querySelector('.voyage-photo').addEventListener('click', function () {
			photos = v.getAttribute('data-photos').split(' ');
			titre = v.getAttribute('data-titre');
			afficher(0);
			boite.showModal();
		});
	});

	boite.querySelector('.v-prec').addEventListener('click', function () { afficher(position - 1); });
	boite.querySelector('.v-suiv').addEventListener('click', function () { afficher(position + 1); });
	boite.querySelector('.v-fermer').addEventListener('click', function () { boite.close(); });
	// Un clic sur le fond sombre ferme la visionneuse
	boite.addEventListener('click', function (e) { if (e.target === boite) boite.close(); });
	boite.addEventListener('keydown', function (e) {
		if (e.key === 'ArrowLeft') afficher(position - 1);
		if (e.key === 'ArrowRight') afficher(position + 1);
	});
	// Glisser du doigt sur téléphone
	var departX = null;
	boite.addEventListener('touchstart', function (e) { departX = e.touches[0].clientX; }, { passive: true });
	boite.addEventListener('touchend', function (e) {
		if (departX === null) return;
		var dx = e.changedTouches[0].clientX - departX;
		if (Math.abs(dx) > 40) afficher(position + (dx < 0 ? 1 : -1));
		departX = null;
	});
})();
