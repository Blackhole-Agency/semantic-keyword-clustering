import sqlite3

# Connexion à la base de données SQLite
conn = sqlite3.connect('data/keywords.db')
cursor = conn.cursor()

# Création de la table pour stocker les résultats de recherche
cursor.execute('''
CREATE TABLE IF NOT EXISTS keywords_serps (
    requestTimestamp DATETIME,
    searchTerms TEXT,
    gl TEXT,
    hl TEXT,
    totalResults INTEGER,
    link TEXT,
    displayLink TEXT,
    main_domain TEXT,
    position INTEGER,
    snippet TEXT,
    snipped_language TEXT,
    snippet_matchScore_order INTEGER,
    snippet_matchScore_token INTEGER,
    title TEXT,
    title_matchScore_order INTEGER,
    title_matchScore_token INTEGER
)
''')

# Création de la table pour stocker les informations de clustering
cursor.execute('''
CREATE TABLE IF NOT EXISTS keyword_clusters (
    requestTimestamp DATETIME,
    cluster INTEGER,
    searchTerms TEXT
)
''')

# Valider les changements et fermer la connexion
conn.commit()
conn.close()
