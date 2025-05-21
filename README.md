📘 Scrapeur de Montres Breguet – EveryWatch.com

Ce script Python utilise Playwright pour automatiser la navigation sur le site everywatch.com et scraper toutes les montres de la marque Breguet visibles sur la page de listing.

🚀 Fonctionnement du script

📦 Pré-requis

Assure-toi d’avoir Python 3.8+ et les bibliothèques suivantes :

(Commandes pour les installer:)
pip install pandas playwright
playwright install

▶️ Lancer le script

python3 scrape_breguet_cards.py

Le script va automatiquement :

    - Ouvrir le navigateur

    - Se rendre sur la page de toutes les montres (/watch-listing)

    - Supprimer les popups ou bloqueurs

    - Faire défiler la page pour charger tous les modèles visibles

    - Filtrer uniquement ceux contenant “Breguet”

    - Récupérer pour chaque montre :

        Le modèle

        La référence

        L’estimation de prix

        Le lien vers la fiche

        L’image

    - Générer un fichier Excel breguet_watches_YYYYMMDD_HHMMSS.xlsx avec tous les résultats


📋 Structure du script

1. handle_obstacles(page)

Supprime dynamiquement les popups, overlays, et paywalls éventuels avec JavaScript pour éviter les blocages.

2. scrape_breguet_cards()

La fonction principale :

    - Ouvre la page https://everywatch.com/watch-listing

    - Scrolle dynamiquement la page jusqu'à ce qu'il n'y ait plus de montres qui se chargent

    - Sélectionne toutes les cartes .ew-watch-card

    - Pour chaque carte contenant le mot "breguet", récupère :

        Texte du modèle

        Référence

        Estimation

        Image

        Lien

3. Export Excel

Toutes les données sont rassemblées dans un fichier .xlsx avec la bibliothèque pandas.



-----------------   BONUS   -----------------


👶 Explication comme à un enfant

Imagine que tu veux faire un album de toutes les montres Breguet qu’on voit sur un grand site internet.

Ce script, c’est un robot intelligent :

   1. Il ouvre le site comme toi sur ton navigateur.

   2. Il ferme les fenêtres gênantes (pubs ou messages).

   3. Il descend la page doucement pour voir toutes les montres.

   4. Il regarde chaque montre, et si elle porte le nom “Breguet”, il dit :

        “Oh ! Une Breguet ! Je vais la noter !”

   5. Il note alors :

        Le nom de la montre

        Son numéro de référence

        Son prix estimé

        Sa photo

        Son lien cliquable

   6. Et quand il a fini, il fait un tableau Excel tout propre avec tout ce qu’il a trouvé.

🧠 En gros, ton robot fait le travail d’un collectionneur numérique, mais automatiquement et sans erreur !
