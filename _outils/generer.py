# Génère les pages du site (FR à la racine, EN dans /en/).
# Usage : python3 _outils/generer.py   (depuis la racine du dépôt)
# Le contenu de chaque page se trouve dans _outils/contenu/<langue>/<page>.html
import pathlib

RACINE = pathlib.Path(__file__).resolve().parent.parent
CONTENU = RACINE / "_outils" / "contenu"

# (identifiant, fichier FR, fichier EN)
PAGES = [
    ("accueil", "index.html", "index.html"),
    ("apropos", "a-propos.html", "about.html"),
    ("cv", "cv.html", "cv.html"),
    ("recos", "recommandations.html", "recommendations.html"),
]

TEXTES = {
    "fr": {
        "menu": {"accueil": "Accueil", "apropos": "À propos", "cv": "CV",
                 "engagements": "Engagements", "recos": "Hors campus"},
        "description": "Annabelle Dussault, étudiante à la maîtrise en science politique à l'Université Laval.",
        "pied": "Étudiante à la maîtrise en science politique, Université Laval",
        "droits": "Tous droits réservés.",
        "autre_langue": ("en", "EN", "Read in English"),
        "theme": ("Passer en mode nuit", "Passer en mode jour"),
        "menu_bouton": "Menu",
        "evitement": "Aller au contenu",
    },
    "en": {
        "menu": {"accueil": "Home", "apropos": "About", "cv": "CV",
                 "engagements": "Involvement", "recos": "Off campus"},
        "description": "Annabelle Dussault, master's student in political science at Université Laval.",
        "pied": "Master's student in political science, Université Laval",
        "droits": "All rights reserved.",
        "autre_langue": ("fr", "FR", "Lire en français"),
        "theme": ("Switch to dark mode", "Switch to light mode"),
        "menu_bouton": "Menu",
        "evitement": "Skip to content",
    },
}


def fichier(page_id, langue):
    for pid, fr, en in PAGES:
        if pid == page_id:
            return fr if langue == "fr" else en


def lien(page_id, de, vers):
    """Chemin relatif d'une page de langue `de` vers une page de langue `vers`."""
    nom = fichier(page_id, vers)
    if de == vers:
        return nom
    return ("en/" + nom) if vers == "en" else ("../" + nom)


def construire(page_id, langue):
    t = TEXTES[langue]
    p = "" if langue == "fr" else "../"
    corps = (CONTENU / langue / f"{page_id}.html").read_text(encoding="utf-8")
    titre_page = corps.split("\n", 1)[0].replace("<!-- titre:", "").replace("-->", "").strip()
    corps = corps.split("\n", 1)[1].replace("{p}", p)
    titre = "Annabelle Dussault" if page_id == "accueil" else f"{titre_page} | Annabelle Dussault"
    autre, autre_court, autre_long = t["autre_langue"]

    actif = ' class="active" aria-current="page"'
    menu = "\n".join(
        "\t\t\t\t\t" + f'<li><a href="{lien(pid, langue, langue)}"'
        f'{actif if pid == page_id else ""}>{t["menu"][pid]}</a></li>'
        for pid, _, _ in PAGES)

    return f"""<!DOCTYPE html>
<!-- Page générée par _outils/generer.py : modifier le contenu dans _outils/contenu/ -->
<html lang="{langue}">
<head>
	<meta charset="utf-8" />
	<meta name="viewport" content="width=device-width, initial-scale=1" />
	<title>{titre}</title>
	<meta name="description" content="{t["description"]}" />
	<link rel="alternate" hreflang="{autre}" href="{lien(page_id, langue, autre)}" />
	<link rel="icon" type="image/svg+xml" href="{p}images/favicon.svg" />
	<link rel="preload" href="{p}assets/fonts/newsreader-latin-500-normal.woff2" as="font" type="font/woff2" crossorigin />
	<link rel="stylesheet" href="{p}assets/css/fontawesome-all.min.css" />
	<link rel="stylesheet" href="{p}assets/css/perso.css" />
	<script>
		// Applique le mode jour ou nuit avant l'affichage (évite un flash blanc)
		(function () {{
			// Le soir et la nuit (de 19 h à 7 h), le site s'ouvre en mode nuit.
			var DEBUT_NUIT = 19, FIN_NUIT = 7;
			var t = null;
			// Un choix fait avec le bouton reste valable jusqu'à la fermeture de l'onglet
			try {{ t = sessionStorage.getItem('theme'); }} catch (e) {{}}
			if (!t) {{
				var h = new Date().getHours();
				t = (h >= DEBUT_NUIT || h < FIN_NUIT) ? 'dark' : 'light';
			}}
			document.documentElement.setAttribute('data-theme', t);
		}})();
	</script>
</head>
<body class="page-{page_id}">
	<a class="lien-evitement" href="#contenu">{t["evitement"]}</a>

	<!-- En-tête et menu -->
	<header class="entete">
		<div class="page">
			<a class="nom" href="{lien("accueil", langue, langue)}">Annabelle Dussault</a>
			<nav class="menu" id="menu" aria-label="Menu">
				<ul>
{menu}
				</ul>
			</nav>
			<div class="outils">
				<button type="button" class="bouton-saison" aria-pressed="true"><svg class="ico cadran" width="24" height="24" viewBox="0 0 24 24" aria-hidden="true"><circle class="anneau" cx="12" cy="12" r="10.2"/><path class="quart quart-hiver" d="M12 12L12.00 4.40A7.6 7.6 0 0 1 19.60 12.00Z"/><path class="quart quart-printemps" d="M12 12L19.60 12.00A7.6 7.6 0 0 1 12.00 19.60Z"/><path class="quart quart-ete" d="M12 12L12.00 19.60A7.6 7.6 0 0 1 4.40 12.00Z"/><path class="quart quart-automne" d="M12 12L4.40 12.00A7.6 7.6 0 0 1 12.00 4.40Z"/><line class="aiguille" x1="12" y1="12" x2="12" y2="5.6"/><circle class="pivot" cx="12" cy="12" r="1.5"/></svg></button>
				<button type="button" class="bouton-theme" data-nuit="{t["theme"][0]}" data-jour="{t["theme"][1]}" title="{t["theme"][0]}" aria-label="{t["theme"][0]}"><svg class="ico icone-lune" width="24" height="24" viewBox="0 0 24 24" aria-hidden="true"><circle class="anneau" cx="12" cy="12" r="10.2"/><mask id="masque-lune"><rect width="24" height="24" fill="#fff"/><circle cx="14.6" cy="9.8" r="4.6" fill="#000"/></mask><circle class="plein" cx="12" cy="12" r="5.6" mask="url(#masque-lune)"/></svg><svg class="ico icone-soleil" width="24" height="24" viewBox="0 0 24 24" aria-hidden="true"><circle class="anneau" cx="12" cy="12" r="10.2"/><circle class="plein" cx="12" cy="12" r="2.6"/><g class="trait"><line x1="16.40" y1="12.00" x2="18.40" y2="12.00"/><line x1="15.11" y1="15.11" x2="16.53" y2="16.53"/><line x1="12.00" y1="16.40" x2="12.00" y2="18.40"/><line x1="8.89" y1="15.11" x2="7.47" y2="16.53"/><line x1="7.60" y1="12.00" x2="5.60" y2="12.00"/><line x1="8.89" y1="8.89" x2="7.47" y2="7.47"/><line x1="12.00" y1="7.60" x2="12.00" y2="5.60"/><line x1="15.11" y1="8.89" x2="16.53" y2="7.47"/></g></svg></button>
				<a href="https://www.linkedin.com/in/annabelle-dussault-625a05303/" target="_blank" rel="noopener" class="lien-icone" title="LinkedIn" aria-label="LinkedIn"><svg class="ico " width="24" height="24" viewBox="0 0 24 24" aria-hidden="true"><circle class="anneau" cx="12" cy="12" r="10.2"/><circle class="plein" cx="8.7" cy="8.1" r="1.15"/><g class="trait"><line x1="8.7" y1="10.7" x2="8.7" y2="16.2"/><path d="M11.9 16.2V10.7M11.9 13.3a2.5 2.5 0 0 1 5 0v2.9"/></g></svg></a>
				<a href="https://github.com/annabelle-dussault" target="_blank" rel="noopener" class="lien-icone" title="GitHub" aria-label="GitHub"><svg class="ico " width="24" height="24" viewBox="0 0 24 24" aria-hidden="true"><circle class="anneau" cx="12" cy="12" r="10.2"/><g class="trait"><circle cx="9" cy="7.4" r="1.6"/><circle cx="9" cy="16.6" r="1.6"/><circle cx="15.2" cy="9.4" r="1.6"/><line x1="9" y1="9" x2="9" y2="15"/><path d="M15.2 11v0.6a3 3 0 0 1-3 3H9.4"/></g></svg></a>
				<a href="{lien(page_id, langue, autre)}" class="langue" hreflang="{autre}" title="{autre_long}"><span class="{'on' if langue == 'fr' else ''}">FR</span><span class="{'on' if langue == 'en' else ''}">EN</span></a>
				<button type="button" class="bouton-menu" aria-controls="menu" aria-expanded="false"><span class="icon solid fa-bars"></span> {t["menu_bouton"]}</button>
			</div>
		</div>
	</header>

	<main id="contenu">
		<div class="page">
{corps}
		</div>
	</main>

	<!-- Pied de page -->
	<footer class="pied">
		<div class="page">
			<div>
				<p class="nom">Annabelle Dussault</p>
				<p>{t["pied"]}</p>
			</div>
			<ul>
				<li><a href="mailto:anna5.dussault@gmail.com">anna5.dussault@gmail.com</a></li>
				<li><a href="https://www.linkedin.com/in/annabelle-dussault-625a05303/" target="_blank" rel="noopener">LinkedIn</a></li>
				<li><a href="https://github.com/annabelle-dussault" target="_blank" rel="noopener">GitHub</a></li>
			</ul>
			<p class="droits">&copy; 2026 Annabelle Dussault. {t["droits"]}</p>
		</div>
	</footer>

	<script src="{p}assets/js/theme.js"></script>
	<script src="{p}assets/js/menu.js"></script>
	<script src="{p}assets/js/saisons.js"></script>
	<script src="{p}assets/js/galerie.js"></script>
	<script src="{p}assets/js/carrousel.js"></script>
</body>
</html>
"""


for langue in ("fr", "en"):
    dossier = RACINE if langue == "fr" else RACINE / "en"
    dossier.mkdir(exist_ok=True)
    for pid, _, _ in PAGES:
        (dossier / fichier(pid, langue)).write_text(construire(pid, langue), encoding="utf-8")
print("Pages générées.")
