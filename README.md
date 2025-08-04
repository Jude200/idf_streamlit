# 📈 Analyse des Courbes IDF (Intensité-Durée-Fréquence)

Application web interactive pour l'analyse des courbes IDF des précipitations développée avec Streamlit.

## 🎯 Fonctionnalités

- **📊 Analyse statistique complète** : Calcul automatique des paramètres de Gumbel
- **⚙️ Modélisation Montana** : Estimation des paramètres a et b de la formule de Montana
- **📈 Visualisations interactives** :
  - Courbes IDF basées sur la distribution de Gumbel
  - Courbes Montana avec modèle ajusté
  - Comparaison entre les deux approches
- **💻 Interface moderne** : Interface utilisateur intuitive avec animations
- **📁 Support multi-formats** : Excel (.xlsx, .xls) et CSV

## 🚀 Installation

### Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de packages Python)

### Installation des dépendances

1. **Clonez ou téléchargez le projet**

2. **Créez un environnement virtuel (recommandé)**

```bash
python -m venv venv
venv\\Scripts\\activate  # Windows
# ou
source venv/bin/activate  # Linux/Mac
```

3. **Installez les dépendances**

```bash
pip install -r requirements.txt
```

## 🏃‍♂️ Utilisation

### Lancement de l'application

```bash
streamlit run index.py
```

L'application s'ouvrira automatiquement dans votre navigateur web à l'adresse `http://localhost:8501`

### Format des données d'entrée

Votre fichier doit contenir :

- Une colonne `Year` avec les années d'observation
- Des colonnes numériques représentant les durées en heures (1, 2, 3, 6, 12, 24, etc.)
- Les valeurs de précipitations maximales annuelles correspondantes

**Exemple de structure :**

```
Year | 1  | 2  | 3  | 6  | 12 | 24
-----|----|----|----|----|----|----|
2000 | 25 | 35 | 42 | 58 | 75 | 89
2001 | 28 | 38 | 45 | 62 | 78 | 92
...
```

## 📊 Méthodes d'analyse

### Distribution de Gumbel

- Calcul des paramètres μ (mu) et β (beta) par la méthode des moments
- Estimation des quantiles pour différentes périodes de retour

### Formule de Montana

- Modèle : `I = b × t^(-a)`
- Estimation des paramètres par régression linéaire en échelle log-log
- Validation par coefficient de détermination (r²)

## 🎨 Interface utilisateur

- **📁 Section Upload** : Glisser-déposer de fichiers avec validation
- **📊 Résultats en temps réel** : Tableaux interactifs des paramètres
- **📈 Graphiques dynamiques** : Visualisations avec onglets séparés
- **🔄 Animations** : Indicateurs de progression et feedbacks visuels

## 🛠️ Structure du projet

```
📦 idf/
├── 📄 index.py                 # Application principale Streamlit
├── 📄 main.py                  # Script de test autonome
├── 📄 requirements.txt         # Dépendances Python
├── 📄 README.md               # Documentation du projet
├── 📁 data/
│   └── 📄 data.csv            # Données d'exemple
└── 📁 lib/
    ├── 📄 const.py            # Constantes du projet
    ├── 📁 core/
    │   ├── 📄 idf.py          # Classe principale d'analyse IDF
    │   └── 📄 utils.py        # Utilitaires mathématiques
    └── 📁 features/
        ├── 📄 ui_components.py     # Composants interface utilisateur
        ├── 📄 loading_animation.py # Système d'animations
        └── 📄 streamlit_logging.py # Gestion des logs
```

## 🧪 Test rapide

Utilisez le fichier `data/data.csv` fourni pour tester l'application :

```bash
python main.py  # Test en ligne de commande
# ou
streamlit run index.py  # Interface web complète
```

## 📚 Références scientifiques

- Distribution de Gumbel pour l'analyse des valeurs extrêmes
- Formule de Montana pour les courbes IDF
- Méthode des moments pour l'estimation des paramètres

## 👨‍💻 Développement

Le code est structuré de manière modulaire :

- `lib/core/idf.py` : Logique métier et calculs
- `lib/features/` : Composants interface et animations
- `index.py` : Orchestration Streamlit

## 🐛 Dépannage

**Erreur d'import :** Vérifiez que toutes les dépendances sont installées

```bash
pip install -r requirements.txt
```

**Erreur de format de fichier :** Vérifiez que votre fichier contient une colonne 'Year' et des colonnes numériques pour les durées

**Performance :** Pour de gros datasets, l'analyse peut prendre quelques secondes - les animations indiquent le progrès

---

🔬 **Développé pour l'analyse hydrologique et la gestion des risques pluviométriques**
