# 🎬 Script vidéo — Présentation projet Bookshop Big Data

**Durée cible** : 10-12 minutes
**Format** : screencast avec voix off
**Outil d'enregistrement suggéré** : QuickTime (macOS) ou OBS Studio

---

## 🧰 Avant de commencer (checklist)

- [ ] Docker Desktop lancé, tous les services Up : `docker compose ps`
- [ ] DAG déjà exécuté au moins une fois (données présentes dans Snowflake)
- [ ] Onglets navigateur préparés :
  - Airflow : http://localhost:8080
  - Streamlit : http://localhost:8501
  - Snowsight : https://app.snowflake.com (connecté)
- [ ] VS Code / ton IDE ouvert sur le projet `big_data`
- [ ] Résolution d'écran à 1920x1080 (zoom navigateur à 125 % pour la lisibilité)
- [ ] Micro testé, son réglé

---

## 📋 Plan de la vidéo (7 chapitres)

| # | Chapitre | Durée | Support |
|---|---|---|---|
| 1 | Intro & contexte | 1 min | Slide / visage |
| 2 | Architecture | 1 min 30 | Diagramme Mermaid |
| 3 | Source PostgreSQL | 1 min 30 | Terminal + `psql` |
| 4 | Orchestration Airflow | 2 min | UI Airflow |
| 5 | Transformations dbt | 2 min | Code + Snowsight |
| 6 | Dashboard Streamlit | 1 min 30 | UI Streamlit |
| 7 | Conclusion & perspectives | 30 s | Slide |

---

## CHAPITRE 1 — Intro & contexte (≈ 1 min)

### 🎙️ Texte à dire

> « Bonjour, je suis [Prénom Nom], étudiant en Master 2 Big Data.
>
> Dans cette vidéo, je vais vous présenter mon projet **Bookshop Analytics** :
> un **pipeline de données complet**, de la base transactionnelle d'une
> librairie jusqu'au dashboard de visualisation, en passant par un entrepôt
> cloud et des transformations SQL industrialisées.
>
> L'objectif : démontrer la mise en place d'une architecture Big Data moderne
> de bout en bout, reproductible en une seule commande. »

### 🎬 Actions à l'écran

- **[0:00 → 0:20]** Slide titre avec : nom du projet, ton nom, M2 Big Data, date
- **[0:20 → 0:40]** Slide "Problématique" : 3 puces
  - Source transactionnelle (Postgres) non adaptée à l'analytique
  - Besoin d'un entrepôt pour agrégations et historisation
  - Visualisation accessible pour le métier
- **[0:40 → 1:00]** Slide "Objectifs" : 3 puces
  - Pipeline automatisé et reproductible
  - Stack cloud moderne (Snowflake + dbt)
  - Dashboard interactif

---

## CHAPITRE 2 — Architecture (≈ 1 min 30)

### 🎙️ Texte à dire

> « Voici l'architecture retenue.
>
> À gauche, **PostgreSQL**, la base source de la librairie : 5 tables
> transactionnelles — books, categories, customers, factures, ventes.
>
> Au centre, **Snowflake**, notre data warehouse cloud, organisé en
> quatre couches :
> - **RAW** : copie brute des données Postgres, sans transformation
> - **STAGING** : nettoyage, typage, renommage
> - **WAREHOUSE** : modèle dimensionnel en étoile, avec dimensions et faits
> - **MARTS** : un "One Big Table" optimisé pour la restitution
>
> Entre les deux, **Airflow** orchestre l'ensemble : il déclenche
> l'ingestion Postgres vers Snowflake, puis lance **dbt** qui applique
> toutes les transformations SQL.
>
> Enfin, **Streamlit** consomme les tables du schéma MARTS pour produire
> un dashboard interactif avec Plotly. »

### 🎬 Actions à l'écran

- **[0:00 → 0:30]** Afficher le diagramme Mermaid `docs/architecture.mmd` (rendu sur mermaid.live)
- **[0:30 → 1:00]** Zoom sur chaque bloc en parlant (Postgres → Airflow → Snowflake → Streamlit)
- **[1:00 → 1:30]** Tableau de la stack technique :

| Couche | Techno |
|---|---|
| Source | PostgreSQL 15 |
| Orchestration | Airflow 2.10 |
| Warehouse | Snowflake |
| Transformations | dbt 1.9 |
| Dashboard | Streamlit + Plotly |
| Infra | Docker Compose |

---

## CHAPITRE 3 — Source PostgreSQL (≈ 1 min 30)

### 🎙️ Texte à dire

> « Commençons par la source. J'ai provisionné une base Postgres dans un
> conteneur Docker, avec un schéma et un jeu de données réaliste.
>
> Connectons-nous pour voir les tables... et voici les 5 tables attendues.
>
> La table `books` contient le catalogue — 5 livres pour la démo. La table
> `ventes` contient les lignes de factures, reliées à `factures` et `books`
> par clés étrangères. »

### 🎬 Actions à faire (pas à pas)

**Action 1** — Montrer le fichier de schéma
```bash
# Ouvrir dans l'IDE :
sql/postgres/01_schema.sql
```
Pointer sur les 5 `CREATE TABLE` et les foreign keys.

**Action 2** — Montrer le seed
```bash
# Ouvrir dans l'IDE :
sql/postgres/02_seed.sql
```
Scroller pour montrer quelques `INSERT`.

**Action 3** — Se connecter à Postgres
```bash
docker compose exec postgres-source psql -U bookshop -d bookshop_source
```

**Action 4** — Dans psql, taper :
```sql
\dt
SELECT COUNT(*) FROM books;
SELECT COUNT(*) FROM ventes;
SELECT b.intitule, SUM(v.qte) AS qte_vendue
FROM ventes v
JOIN books b ON b.id = v.book_id
GROUP BY b.intitule
ORDER BY qte_vendue DESC;
\q
```

---

## CHAPITRE 4 — Orchestration Airflow (≈ 2 min)

### 🎙️ Texte à dire

> « L'orchestration est assurée par Airflow. Rendons-nous sur l'interface
> à l'adresse `localhost:8080`.
>
> Voici le DAG `bookshop_pipeline`. Il contient 4 tâches enchaînées :
>
> 1. **create_bookshop_structures** : crée la base et les tables RAW dans Snowflake
> 2. **ingest_postgres_to_snowflake** : extrait les données Postgres et les insère dans RAW
> 3. **ensure_dbt_profile** : prépare le profil dbt
> 4. **dbt_build** : exécute toutes les transformations dbt
>
> Déclenchons le pipeline en cliquant sur le bouton "Trigger DAG"...
>
> Les tâches passent en vert les unes après les autres. On peut cliquer sur
> chaque tâche pour voir ses logs détaillés — ici par exemple, on voit le
> nombre de lignes ingérées par table. »

### 🎬 Actions à faire

**Action 1** — Ouvrir http://localhost:8080, se connecter (`admin` / mot de passe)

**Action 2** — Cliquer sur le DAG `bookshop_pipeline` → vue **Graph**

**Action 3** — Ouvrir le code du DAG dans l'IDE :
```
airflow/dags/bookshop_pipeline.py
```
Pointer sur les fonctions Python et le chaînage des tâches.

**Action 4** — Dans l'UI Airflow : cliquer ▶️ **Trigger DAG**

**Action 5** — Observer l'exécution en temps réel (cases qui passent au vert)

**Action 6** — Cliquer sur la tâche `ingest_postgres_to_snowflake` → **Logs** →
montrer les lignes `Fetched X rows from Postgres table Y` et
`Inserted X rows into Snowflake`.

---

## CHAPITRE 5 — Transformations dbt (≈ 2 min)

### 🎙️ Texte à dire

> « Les transformations sont gérées par dbt. Voyons la structure du projet.
>
> Trois couches de modèles : **staging**, **warehouse**, **marts**.
>
> Le **staging** fait du nettoyage léger : typage, renommage en anglais,
> déduplication si besoin.
>
> Le **warehouse** construit un modèle en étoile : des dimensions
> (`DIM_BOOKS`, `DIM_CUSTOMERS`, `DIM_CATEGORY`) et des tables de faits
> (`FACT_VENTES`, `FACT_FACTURES`, plus des agrégats par mois et par année).
>
> Enfin, `MARTS.OBT_SALES` est une "One Big Table" qui joint tout ce
> qu'un analyste veut croiser pour son dashboard, sans avoir à écrire de JOIN.
>
> dbt exécute aussi des **tests** automatiques — unicité des clés, non-null,
> intégrité référentielle — sur chaque build. Aucun modèle ne passe en
> production si un test échoue. »

### 🎬 Actions à faire

**Action 1** — Dans l'IDE, ouvrir l'arborescence :
```
app/dbt_bookshop/
├── dbt_project.yml
├── models/
│   ├── staging/
│   ├── warehouse/
│   └── marts/
├── macros/
└── profiles.yml.example
```

**Action 2** — Ouvrir et commenter `dbt_project.yml` : la hiérarchie des schémas.

**Action 3** — Ouvrir un modèle staging, ex. `models/staging/stg_books.sql` : expliquer le `SELECT` et le cast de types.

**Action 4** — Ouvrir un modèle warehouse, ex. `models/warehouse/fact_ventes.sql` : expliquer le `JOIN` avec les staging.

**Action 5** — Ouvrir `models/marts/obt_sales.sql` : la OBT dénormalisée.

**Action 6** — Aller sur Snowsight :
- Cliquer sur **Data → Databases → BOOKSHOP**
- Dérouler les schémas : `RAW`, `STAGGING`, `WAREHOUSE`, `MARTS`
- Cliquer sur `MARTS.OBT_SALES` → **Preview** : montrer les lignes jointes

**Action 7** — Exécuter dans une worksheet Snowsight :
```sql
SELECT COUNT(*) FROM BOOKSHOP.MARTS.OBT_SALES;

SELECT book_intitule, SUM(qte) AS qte_vendue, SUM(pu * qte) AS ca
FROM BOOKSHOP.MARTS.OBT_SALES
GROUP BY book_intitule
ORDER BY ca DESC;
```

---

## CHAPITRE 6 — Dashboard Streamlit (≈ 1 min 30)

### 🎙️ Texte à dire

> « La dernière couche : la restitution. J'ai développé un dashboard
> Streamlit qui interroge directement Snowflake.
>
> On y trouve :
>
> - Trois KPI en haut : nombre de ventes, chiffre d'affaires, montant encaissé
> - Un graphique du chiffre d'affaires mensuel
> - La répartition des ventes par livre, en camembert
> - Les montants payés par client
> - Et un aperçu tabulaire de la OBT
>
> Le code est concis : une trentaine de lignes. La connexion Snowflake
> inclut un retry automatique avec timeout configurable, pour gérer les
> coupures réseau temporaires. »

### 🎬 Actions à faire

**Action 1** — Ouvrir dans l'IDE `app/dashboard.py` — pointer sur :
- `get_connection()` : les paramètres de timeout
- `query_df()` : la logique de retry
- Les 5 requêtes SQL

**Action 2** — Aller sur http://localhost:8501

**Action 3** — Montrer chaque composant du dashboard en parlant :
- KPI
- Graphique mensuel
- Camembert livres
- Barres clients
- Tableau de la OBT

**Action 4** — (Bonus) Survoler un graphique Plotly pour montrer l'interactivité.

---

## CHAPITRE 7 — Conclusion & perspectives (≈ 30 s)

### 🎙️ Texte à dire

> « Pour conclure, ce projet démontre qu'avec une stack moderne — Docker,
> Airflow, Snowflake, dbt, Streamlit — on peut construire un pipeline de
> données complet, testé et reproductible en quelques centaines de lignes
> de code.
>
> Les perspectives d'évolution :
>
> - Passer en **ingestion incrémentale** avec CDC plutôt qu'un truncate/insert
> - Ajouter un **monitoring** avec alertes (Sentry, email) sur échec de DAG
> - Intégrer un **catalogue de données** (dbt docs ou Datahub)
> - Déployer en **production** : Airflow managed (MWAA / Astro), secrets
>   manager, authentification Snowflake par clé
>
> Merci de votre attention. Le code source est disponible sur mon GitHub. »

### 🎬 Actions à l'écran

- **[0:00 → 0:20]** Slide "Bilan" : 3 puces (pipeline fonctionnel, tests auto, reproductible en 1 commande)
- **[0:20 → 0:40]** Slide "Perspectives" : 4 puces
- **[0:40 → 0:50]** Slide finale : ton nom + URL du repo GitHub

---

## 🎞️ Conseils de post-production

- **Coupes** : supprimer les temps morts (attente que le DAG tourne → couper et afficher "Quelques secondes plus tard...")
- **Titres** : insérer un titre au début de chaque chapitre
- **Zooms** : zoomer sur les parties importantes du code (commandes, lignes clés)
- **Musique** : optionnelle, volume bas, libre de droits (ex. YouTube Audio Library)
- **Sous-titres** : si rendu pour jury, générer des sous-titres français automatiques

---

## ⏱️ Répétitions recommandées

1. **Lecture sèche** du script à voix haute (5 min) → vérifier la fluidité
2. **Répétition complète avec actions** (sans enregistrer) → vérifier le timing
3. **Enregistrement final** chapitre par chapitre (plus facile à monter)

---

## 📦 Livrables attendus à côté de la vidéo

- `docs/rapport_projet.md` — rapport écrit
- `docs/plan_presentation.md` — slides
- Lien GitHub du projet
- Lien vidéo (YouTube privé ou Drive)
