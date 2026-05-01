# ❄️ Guide Snowflake pas à pas

Ce guide détaille comment créer un compte Snowflake gratuit, récupérer les
identifiants, les injecter dans le projet et vérifier la connexion.

---

## 1. Créer un compte trial (gratuit, 400 $ de crédits, 30 jours)

1. Ouvre https://signup.snowflake.com/
2. Remplis :
   - **Nom / email professionnel** (pro recommandé, gmail accepté)
   - **Edition** : `Standard` (largement suffisant pour ce projet)
   - **Cloud provider** : `AWS`
   - **Région** : `EU (Paris)` ou `EU (Ireland)`
3. Valide l'email → clic sur le lien d'activation
4. Définis ton **username** et ton **password** admin → tu arrives dans **Snowsight** (l'UI web)

---

## 2. Récupérer l'**Account Identifier**

⚠️ C'est l'étape qui bloque le plus de monde. L'`ACCOUNT` demandé par le connecteur **n'est pas l'URL complète**.

### Méthode 1 — via Snowsight

1. En bas à gauche, clique sur **ton nom d'utilisateur**
2. Survole le nom du **compte** → un panneau s'ouvre à droite
3. Copie la valeur **Account Identifier**

Format attendu : `ORGNAME-ACCOUNTNAME` (ex. `ABCDEFG-XY12345`).

### Méthode 2 — via l'URL

Si ton URL de connexion est :
```
https://abcdefg-xy12345.snowflakecomputing.com
```
alors `SNOWFLAKE_ACCOUNT=abcdefg-xy12345`.

### Méthode 3 — via SQL (depuis une feuille Snowsight)

```sql
SELECT CURRENT_ORGANIZATION_NAME() || '-' || CURRENT_ACCOUNT_NAME();
```

---

## 3. Vérifier / créer un warehouse

Dans Snowsight → **Admin → Warehouses**.

- `COMPUTE_WH` existe déjà par défaut → rien à faire.
- Sinon, clique **+ Warehouse** :
  - Name : `COMPUTE_WH`
  - Size : `X-Small` (suffit, coût minimal)
  - Auto suspend : `60 seconds` (pour économiser les crédits)

---

## 4. Remplir `.env`

Dans la racine du projet :

```bash
cp .env.example .env   # si pas déjà fait
```

Édite `.env` :

```env
SNOWFLAKE_ACCOUNT=ABCDEFG-XY12345         # format ORGNAME-ACCOUNTNAME
SNOWFLAKE_USER=ton_username
SNOWFLAKE_PASSWORD=ton_password
SNOWFLAKE_ROLE=ACCOUNTADMIN                # OK pour un trial
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_DATABASE=BOOKSHOP                # sera créée par le DAG
SNOWFLAKE_SCHEMA=RAW
```

---

## 5. Connecter Airflow

Une fois `.env` rempli, **recharge les services** (ils relisent `.env` au démarrage) :

```bash
docker compose restart airflow-scheduler airflow-webserver streamlit
```

Puis crée les connexions Airflow :

```bash
make conns
```

Ce script exécute [scripts/create_airflow_connections.sh](../scripts/create_airflow_connections.sh), qui crée :
- `postgres_bookshop` (source locale)
- `snowflake_bookshop` (data warehouse)

### Tester la connexion Snowflake

```bash
docker compose exec airflow-webserver airflow connections test snowflake_bookshop
```

Sortie attendue :
```
Connection success!
```

Si tu vois `Incorrect username or password` ou `404 Not Found for account`, consulte la section **Dépannage** plus bas.

---

## 6. Vérifier le pipeline

Déclenche le DAG :
```bash
docker compose exec airflow-webserver airflow dags trigger bookshop_pipeline
```

Dans Snowsight, exécute :
```sql
USE DATABASE BOOKSHOP;
SHOW SCHEMAS;                -- attendu : RAW, STAGING, WAREHOUSE, MARTS
SELECT COUNT(*) FROM RAW.BOOKS;
SELECT COUNT(*) FROM MARTS.OBT_SALES;
```

Ou plus rapidement, utilise les requêtes prêtes :
[sql/snowflake/03_verification_queries.sql](../sql/snowflake/03_verification_queries.sql)

---

## 7. Dépannage

| Erreur | Cause probable | Solution |
|---|---|---|
| `404 Not Found` sur l'account | Mauvais format d'`ACCOUNT` | Utilise `ORGNAME-ACCOUNTNAME`, pas l'URL complète |
| `Incorrect username or password` | Mot de passe erroné | Réinitialise dans Snowsight → Admin → Users |
| `No active warehouse selected` | Warehouse suspendu ou inexistant | `ALTER WAREHOUSE COMPUTE_WH RESUME;` dans Snowsight |
| `Insufficient privileges` sur `CREATE DATABASE` | Rôle insuffisant | Vérifie `SNOWFLAKE_ROLE=ACCOUNTADMIN` |
| `Network timeout` | VPN / proxy bloque `.snowflakecomputing.com` | Désactiver VPN ou whitelister le domaine |
| `JWT token invalid` | Horloge système désynchronisée | `sudo sntp -sS time.apple.com` (macOS) |

---

## 8. Avancé — authentification par clé (recommandé en prod)

Les mots de passe sont à proscrire en production. Génère une paire de clés :

```bash
openssl genrsa 2048 | openssl pkcs8 -topk8 -v2 des3 -inform PEM -out rsa_key.p8
openssl rsa -in rsa_key.p8 -pubout -out rsa_key.pub
```

Enrôle la clé publique dans Snowflake :

```sql
ALTER USER ton_username SET RSA_PUBLIC_KEY='<contenu de rsa_key.pub sans BEGIN/END>';
```

Puis dans la connexion Airflow Snowflake, utilise `private_key_file` au lieu de `password`.

---

## 9. Coûts & limites du trial

- **400 $ de crédits** ≈ largement assez pour ce projet (< 1 $ de consommation réelle)
- **30 jours** à partir de l'inscription
- Au-delà : compte suspendu, données conservées 30 jours supplémentaires
- Pour éviter les surprises : garder le warehouse en `X-Small` + auto-suspend 60s
