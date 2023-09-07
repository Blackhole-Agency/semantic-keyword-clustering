"""
Semantic Keyword Clustering
===========================

Auteur : Brule Nicolas
Développé par : Blackhole

Description
-----------
Ce module fournit un outil de clustering sémantique pour regrouper des mots-clés basés sur leur pertinence dans les résultats de recherche Google. En utilisant des modèles de traitement du langage naturel avancés tels que BERT et DistilBERT, cet outil peut identifier et regrouper des mots-clés qui ont des significations ou des contextes similaires dans les résultats de recherche.

Caractéristiques Principales
----------------------------
- Clustering Sémantique : Utilise BERT ou DistilBERT pour obtenir des embeddings de mots-clés et les regroupe en fonction de leur similarité.
- Intégration avec Google Custom Search : Récupère les résultats de recherche Google pour chaque mot-clé pour améliorer la précision du clustering.
- Flexibilité : Permet aux utilisateurs de choisir entre BERT et DistilBERT en fonction de leurs besoins et ressources.
- Base de Données Intégrée : Stocke les résultats de recherche et les clusters dans une base de données SQLite pour une récupération facile.

Exemple d'Utilisation
---------------------
from semantic_clustering import SemanticClustering

# Initialisez l'outil avec votre clé API, ID de moteur de recherche, et le modèle de votre choix
clustering = SemanticClustering(api_key="YOUR_API_KEY", cse_id="YOUR_CSE_ID", database="keywords.db", model_type="bert")

# Clusterisez vos mots-clés
clusters = clustering.cluster_keywords(["keyword1", "keyword2"], "en", "us")

Contribution
------------
Les contributions sont les bienvenues ! Si vous avez des suggestions d'amélioration, des corrections de bugs ou d'autres contributions, n'hésitez pas à soumettre une pull request ou à ouvrir une issue.

Licence
-------
Ce projet est sous licence MIT. Pour plus de détails, veuillez consulter le fichier de licence associé.

"""

# [Le code de la classe et des fonctions irait ici]
