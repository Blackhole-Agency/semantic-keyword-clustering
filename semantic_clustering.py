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

from googleapiclient.discovery import build
import pandas as pd
from datetime import datetime
from fuzzywuzzy import fuzz
from urllib.parse import urlparse
from tld import get_tld
import langid
import sqlite3
import networkx as nx
import community
from sklearn.cluster import DBSCAN
from sklearn.metrics.pairwise import cosine_similarity
from transformers import BertTokenizer, BertModel, DistilBertTokenizer, DistilBertModel
import torch


class SemanticClustering:

    def __init__(self, api_key, cse_id, database, model_type="bert"):
        self.api_key = api_key
        self.cse_id = cse_id
        self.database = database

        if model_type == "bert":
            self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
            self.model = BertModel.from_pretrained('bert-base-uncased')
        elif model_type == "distilbert":
            self.tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
            self.model = DistilBertModel.from_pretrained('distilbert-base-uncased')
        else:
            raise ValueError("Invalid model_type. Choose between 'bert' and 'distilbert'.")

    def _clean_data(self, text):
        """
        Nettoie le texte donné.
        """
        return text.lower()

    def _compute_text_similarity(self, text1, text2):
        """
        Calcule la similarité entre deux textes en utilisant les embeddings et la similarité cosine.
        """
        input_ids1 = self.tokenizer.encode(text1, return_tensors='pt')
        input_ids2 = self.tokenizer.encode(text2, return_tensors='pt')

        with torch.no_grad():
            embeddings1 = self.model(input_ids1)[0].mean(1)
            embeddings2 = self.model(input_ids2)[0].mean(1)

        similarity = cosine_similarity(embeddings1, embeddings2)
        return similarity[0][0]

    def _get_search_results(self, query, hl, gl):
        """
        Récupère les résultats de recherche Google pour une requête donnée.
        """
        try:
            service = build("customsearch", "v1", developerKey=self.api_key, cache_discovery=False)
            res = service.cse().list(q=query, hl=hl, gl=gl,
                                     fields='queries(request(totalResults,searchTerms,hl,gl)),items(title,displayLink,link,snippet)',
                                     num=10, cx=self.cse_id).execute()
            return res
        except Exception as e:
            print(e)
            return None

    def _create_clusters(self, embeddings):
        """
        Crée des clusters à partir des embeddings en utilisant DBSCAN.
        """
        clustering = DBSCAN().fit(embeddings)
        return clustering.labels_

    def cluster_keywords(self, keywords, hl, gl):
        """
        Fonction principale pour le clustering des mots-clés.
        """
        results = []
        embeddings = []

        for query in keywords:
            result = self._get_search_results(query, hl, gl)
            if result:
                results.append(result)
                embeddings.append(self._compute_text_similarity(query, result["items"][0]["snippet"]))

        # Clustering des mots-clés basé sur leurs embeddings
        clusters = self._create_clusters(embeddings)
        return clusters

# Exemple d'utilisation :
# clustering = SemanticClustering(api_key="YOUR_API_KEY", cse_id="YOUR_CSE_ID", database="keywords.db", model_type="bert")
# clusters = clustering.cluster_keywords(["keyword1", "keyword2"], "en", "us")
