"""
📚 Documentation des Méthodes de Calcul IDF
Module contenant la documentation technique des courbes IDF
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def display_idf_methodology():
    """
    Affiche la documentation complète de la méthodologie de calcul des courbes IDF
    """
    
    st.markdown("""
    # 📚 Méthodologie de Calcul des Courbes IDF
    
    > **Intensité - Durée - Fréquence** : Méthodes statistiques pour l'analyse hydrologique
    
    ---
    """)
    
    # Section 1: Introduction
    with st.expander("🎯 **1. Introduction et Objectifs**", expanded=True):
        st.markdown("""
        ### Qu'est-ce qu'une courbe IDF ?
        
        Les courbes **IDF (Intensité-Durée-Fréquence)** permettent de déterminer l'intensité de précipitation 
        pour une durée donnée et un temps de retour spécifique. Elles sont essentielles pour :
        
        - 🏗️ **Dimensionnement d'ouvrages** (réseaux d'assainissement, évacuateurs de crues)
        - 🌊 **Gestion des risques hydrologiques** (inondations, ruissellement urbain)  
        - 📊 **Études d'impact climatique** (changement climatique, urbanisation)
        - ⚡ **Méthode rationnelle** : Calcul de $I_T(t = t_c)$
        
        ### Principe général
        
        1. **Échantillonnage** : Extraction des maxima annuels de précipitation
        2. **Ajustement statistique** : Loi de Gumbel pour modéliser les valeurs extrêmes
        3. **Calcul des intensités** : Valeurs pour différents temps de retour
        4. **Coefficients de Montana** : Modèle mathématique $I = a × t^{-b}$
        5. **Courbes IDF** : Représentation graphique finale
        """)
    
    # Section 2: Échantillonnage
    with st.expander("📊 **2. Échantillonnage : Maxima Annuels**"):
        st.markdown("""
        ### 2.1 Traitement des données brutes
        
        À partir des données de précipitation (pas de temps 5 minutes), on calcule les intensités 
        moyennes pour différentes durées glissantes :
        
        - **1 heure** : Cumul horaire glissant
        - **2 heures** : Cumul sur 2h divisé par 2 pour obtenir l'intensité moyenne
        - **4 heures** : Cumul sur 4h divisé par 4 pour obtenir l'intensité moyenne  
        - **8 heures** : Cumul sur 8h divisé par 8 pour obtenir l'intensité moyenne
        - **24 heures** : Cumul journalier divisé par 24 pour obtenir l'intensité moyenne
        
        ### 2.2 Extraction des maxima annuels
        
        **Principe** : Chaque année constitue un "bloc" indépendant
        
        On extrait le maximum annuel pour chaque durée d'agrégation. Cette méthode permet 
        d'obtenir une série temporelle de valeurs extrêmes indépendantes, condition nécessaire 
        pour l'application de la théorie des valeurs extrêmes.
        
        **Hypothèses** :
        - 🔄 **Indépendance** : Les précipitations sont indépendantes d'une année sur l'autre
        - 📊 **Stationnarité** : La distribution reste constante dans le temps
        - 🎯 **Homogénéité** : Même loi de distribution chaque année
        """)
    
    # Section 3: Loi de Gumbel
    with st.expander("📈 **3. Ajustement par la Loi de Gumbel**"):
        st.markdown("""
        ### 3.1 Théorie des valeurs extrêmes
        
        La **loi de Gumbel** est l'approximation théorique de la distribution du maximum 
        d'un échantillon de variables aléatoires indépendantes de même loi.
        
        ### 3.2 Fonction de répartition
        
        $$F(x; \\mu, \\sigma) = P(X \\leq x) = \\exp\\left[-\\exp\\left(-\\frac{x - \\mu}{\\sigma}\\right)\\right]$$
        
        **Paramètres** :
        - **μ** : paramètre de position (contrôle la moyenne)
        - **σ > 0** : paramètre d'échelle (contrôle la variabilité)
        
        ### 3.3 Variable de Gumbel
        
        Transformation linéarisante :
        
        $$U(x) = -\\ln[-\\ln(P(X \\leq x))]$$
        
        **Relation linéaire** : $x = \\sigma U(x) + \\mu$
        
        ### 3.4 Méthodes d'ajustement
        
        **A) Ajustement graphique** :
        
        1. Construction de la fonction de répartition empirique : $P(X ≤ x) = \\frac{rang - 0.5}{N}$
        2. Calcul de la variable de Gumbel : $U = -\\ln[-\\ln(P)]$
        3. Régression linéaire entre U et les observations
        4. Extraction des paramètres : μ (ordonnée à l'origine) et σ (pente)
        
        **B) Ajustement par maximum de vraisemblance** :
        
        Méthode statistique qui maximise la probabilité d'observer les données, 
        implémentée dans les librairies spécialisées. Cette méthode est généralement 
        plus précise que l'ajustement graphique car elle optimise directement 
        les paramètres de la loi.
        """)
    
    # Section 4: Temps de retour
    with st.expander("⏰ **4. Temps de Retour et Probabilités**"):
        st.markdown("""
        ### 4.1 Définition du temps de retour
        
        Un phénomène de **temps de retour T années** a une probabilité $\\frac{1}{T}$ 
        d'être dépassé chaque année.
        
        ### 4.2 Relation probabilité - temps de retour
        
        $$P(X \\leq x_T) = 1 - \\frac{1}{T}$$
        
        **Exemples** :
        - **T = 10 ans** → $P(X \\leq x_{10}) = 0.90$ (90% de non-dépassement)
        - **T = 100 ans** → $P(X \\leq x_{100}) = 0.99$ (99% de non-dépassement)
        
        ### 4.3 Calcul des valeurs de retour
        
        **Processus** :
        
        1. **Définition de la probabilité** : Pour chaque temps de retour T, calcul de la probabilité de non-dépassement
        2. **Application de la loi ajustée** : Utilisation de la fonction quantile (inverse de la fonction de répartition)
        3. **Extraction de l'intensité** : Obtention de la valeur d'intensité correspondante
        
        Ce processus est répété pour chaque durée d'agrégation et chaque temps de retour 
        d'intérêt, permettant de construire une matrice complète des valeurs IDF.
        
        ### 4.4 Interprétation statistique
        
        ⚠️ **Important** : Un événement centennal peut se produire plusieurs fois par siècle, 
        ou pas du tout ! C'est une probabilité, pas une prédiction déterministe.
        """)
    
    # Section 5: Coefficients de Montana
    with st.expander("🔢 **5. Coefficients de Montana**"):
        st.markdown("""
        ### 5.1 Modèle mathématique
        
        Observation empirique : relation puissance entre intensité et durée
        
        $$I_T(D) = a_T \\times D^{-b_T}$$
        
        **Où** :
        - **$I_T(D)$** : Intensité (mm/h) pour le temps de retour T et la durée D
        - **$a_T$** : Coefficient d'intensité pour le temps de retour T
        - **$b_T$** : Exposant (coefficient de décroissance) pour le temps de retour T
        - **D** : Durée de précipitation (heures)
        
        ### 5.2 Ajustement par régression
        
        **Linéarisation logarithmique** :
        
        $$\\log(I_T) = \\log(a_T) - b_T \\log(D)$$
        
        **Processus d'ajustement** :
        
        1. **Transformation logarithmique** des intensités et des durées
        2. **Régression linéaire** dans l'espace log-log
        3. **Extraction des coefficients** :
           - **a** = exponentielle de l'ordonnée à l'origine
           - **b** = opposé de la pente (pour avoir une valeur positive)
        
        Cette méthode permet d'ajuster le modèle de Montana pour chaque temps de retour, 
        en exploitant la relation quasi-linéaire observée entre log(intensité) et log(durée).
        
        ### 5.3 Calcul des cumuls
        
        **Précipitation totale** sur la durée D :
        
        $$C_T(D) = I_T(D) \\times D = a_T \\times D^{1-b_T}$$
        
        ### 5.4 Domaine de validité
        
        ⚠️ Les coefficients de Montana ne sont valides que sur la **plage de durées** 
        utilisée pour l'ajustement (ex: 1h à 24h).
        """)
    
    # Section 6: Construction des courbes
    with st.expander("📊 **6. Construction des Courbes IDF**"):
        st.markdown("""
        ### 6.1 Processus complet
        
        **Étapes de construction** :
        
        1. **Génération d'une grille** durée × temps de retour avec échelle logarithmique
        2. **Calcul des intensités** avec les coefficients de Montana : $I = a × D^{-b}$
        3. **Représentation graphique** avec échelles appropriées
        4. **Validation** et vérification de la cohérence physique
        
        La construction utilise une grille fine de durées (par exemple de 1h à 100h) 
        pour obtenir des courbes lisses et continues, permettant l'interpolation 
        pour n'importe quelle durée dans le domaine de validité.
        
        ### 6.2 Types de représentation
        
        **A) Courbes d'égale fréquence** :
        - Une courbe par temps de retour
        - Intensité vs Durée
        - Échelles logarithmiques
        
        **B) Courbes d'égale durée** :
        - Une courbe par durée
        - Intensité vs Temps de retour
        - Échelle semi-logarithmique
        
        ### 6.3 Validation et contrôle qualité
        
        - 📊 **Coefficient de corrélation** : R² > 0.95 souhaité
        - 📈 **Tests d'ajustement** : Kolmogorov-Smirnov, Anderson-Darling
        - 🎯 **Cohérence physique** : $b_T$ entre 0.4 et 1.2 typiquement
        - 📉 **Monotonie** : $a_T$ croissant avec T
        """)
    
    # Section 7: Applications pratiques
    with st.expander("⚙️ **7. Applications Pratiques**"):
        st.markdown("""
        ### 7.1 Dimensionnement hydraulique
        
        **Méthode rationnelle** :
        $$Q = C \\times I \\times A$$
        
        - **Q** : Débit de pointe (m³/s)
        - **C** : Coefficient de ruissellement
        - **I** : Intensité IDF pour le temps de retour T et le temps de concentration → **$I_T(t_c)$**
        - **A** : Surface du bassin versant (ha)
        
        **Application pratique** :
        
        Le temps de concentration $t_c$ du bassin versant détermine la durée à considérer 
        dans les courbes IDF. L'intensité correspondante $I_T(t_c)$ est alors utilisée 
        pour calculer le débit de pointe avec la méthode rationnelle.
        
        ### 7.2 Choix du temps de retour
        
        | **Type d'ouvrage** | **Temps de retour** |
        |-------------------|-------------------|
        | Réseau pluvial urbain | 2-10 ans |
        | Routes nationales | 10-20 ans |
        | Aéroports | 50-100 ans |
        | Barrages | 100-1000 ans |
        
        ### 7.3 Incertitudes et limitations
        
        **Sources d'incertitude** :
        - 📊 **Échantillonnage** : Taille limitée des séries
        - 📈 **Modèle statistique** : Hypothèse Gumbel
        - 🌡️ **Non-stationnarité** : Changement climatique
        - 📍 **Représentativité spatiale** : Extrapolation géographique
        
        **Bonnes pratiques** :
        - ✅ Utiliser au minimum 20-30 ans de données
        - ✅ Vérifier l'homogénéité des séries
        - ✅ Considérer plusieurs lois statistiques
        - ✅ Intégrer les intervalles de confiance
        """)
    
    # Section 8: Formules récapitulatives
    with st.expander("📋 **8. Formules de Référence**"):
        st.markdown("""
        ### 8.1 Loi de Gumbel
        
        **Fonction de répartition** :
        $$F(x) = \\exp\\left[-\\exp\\left(-\\frac{x - \\mu}{\\sigma}\\right)\\right]$$
        
        **Variable de Gumbel** :
        $$U = -\\ln[-\\ln(F)]$$
        
        **Relation linéaire** :
        $$x = \\sigma U + \\mu$$
        
        ### 8.2 Temps de retour
        
        **Probabilité de non-dépassement** :
        $$P(X \\leq x_T) = 1 - \\frac{1}{T}$$
        
        **Temps de retour à partir d'une probabilité** :
        $$T = \\frac{1}{1 - P(X \\leq x)}$$
        
        ### 8.3 Coefficients de Montana
        
        **Modèle d'intensité** :
        $$I_T(D) = a_T \\times D^{-b_T}$$
        
        **Modèle de cumul** :
        $$C_T(D) = a_T \\times D^{1-b_T}$$
        
        **Régression logarithmique** :
        $$\\log(I) = \\log(a) - b \\log(D)$$
        
        ### 8.4 Méthode rationnelle
        
        $$Q_{max} = C \\times I_T(t_c) \\times A$$
        
        Avec $t_c$ = temps de concentration du bassin versant
        """)

def display_calculation_example():
    """
    Affiche un exemple concret de calcul étape par étape
    """
    
    st.markdown("## 🔢 Exemple de Calcul Détaillé")
    
    with st.expander("📊 **Exemple : Station Deberegati (1990-2019)**", expanded=True):
        st.markdown("""
        ### Données d'entrée
        - **Station** : Deberegati (Niger, réseau AMMA-CATCH)
        - **Période** : 1990-2019 (30 ans)
        - **Pas de temps initial** : 5 minutes
        - **Durées analysées** : 1h, 2h, 4h, 8h, 24h
        
        ### Étape 1 : Maxima annuels pour 1h
        
        ```
        Année    Intensité max (mm/h)
        1990     45.2
        1991     52.8
        1992     41.6
        ...      ...
        2019     48.4
        ```
        
        ### Étape 2 : Ajustement Gumbel
        
        **Paramètres obtenus** :
        - μ = 39.72 mm/h
        - σ = 13.19 mm/h
        - R² = 0.94
        
        ### Étape 3 : Calcul des intensités de référence
        
        | **Temps de retour** | **Probabilité** | **Intensité (mm/h)** |
        |-------------------|----------------|-------------------|
        | 2 ans | 0.50 | 38.5 |
        | 5 ans | 0.80 | 48.2 |
        | 10 ans | 0.90 | 55.1 |
        | 50 ans | 0.98 | 69.8 |
        | 100 ans | 0.99 | 75.4 |
        
        ### Étape 4 : Coefficients de Montana
        
        **Régression pour T=100 ans** :
        - Données d'entrée : (1h→75.4), (2h→64.2), (4h→48.1), (8h→35.7), (24h→21.8)
        - Modèle obtenu : $I_{100}(D) = 85.4 \\times D^{-0.42}$
        - Coefficients : a = 85.4, b = 0.42
        - Qualité d'ajustement : R² = 0.98
        
        ### Étape 5 : Application pratique
        
        **Dimensionnement d'un bassin de 5 ha, C=0.6, T=10 ans, tc=2h** :
        
        **Calcul de l'intensité** : $I_{10}(2h) = 68.4 \\times 2^{-0.38} = 52.1$ mm/h
        
        **Débit de pointe** : $Q_{max} = 0.6 \\times 52.1 \\times 5 = 156.3$ m³/h = 43.4 l/s
        """)

def create_methodology_page():
    """
    Page principale de documentation méthodologique
    """
    
    st.set_page_config(
        page_title="Documentation IDF",
        page_icon="📚",
        layout="wide"
    )
    
    # En-tête avec style
    st.markdown("""
    <div style="background: linear-gradient(90deg, #4f46e5, #06b6d4, #10b981); 
                height: 4px; margin-bottom: 2rem; border-radius: 2px;"></div>
    """, unsafe_allow_html=True)
    
    # Menu de navigation
    tab1, tab2 = st.tabs([
        "📊 Méthodologie", 
        "🔢 Exemple de calcul"
    ])
    
    with tab1:
        display_idf_methodology()
    
    with tab2:
        display_calculation_example()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #64748b; font-size: 0.9rem;">
        📚 Documentation générée automatiquement à partir du notebook de référence<br>
        🔄 Mise à jour : Septembre 2025 | ⚡ Application IDF v2.0
    </div>
    """, unsafe_allow_html=True)

# Fonction utilitaire pour intégration dans l'application principale
def show_documentation_section():
    """
    Section documentation à intégrer dans l'application principale
    Version compacte pour sidebar ou expander
    """
    
    st.markdown("### 📚 Documentation Méthodologique")
    
    # Liens vers les sections principales
    if st.button("📊 Voir la méthodologie complète", key="methodology"):
        display_idf_methodology()
    
    # Version résumée pour aperçu rapide
    with st.expander("🔍 Aperçu des méthodes", expanded=False):
        st.markdown("""
        **Processus de calcul IDF** :
        
        1. **📊 Échantillonnage** : Maxima annuels par durée
        2. **📈 Ajustement** : Loi de Gumbel (valeurs extrêmes)  
        3. **⏰ Temps de retour** : $P = 1 - 1/T$
        4. **🔢 Montana** : $I = a × D^{-b}$
        5. **📊 Courbes IDF** : Visualisation finale
        
        **Formule clé** : $I_T(D) = a_T × D^{-b_T}$
        
        *Cliquez sur "Voir la méthodologie complète" pour plus de détails.*
        """)

if __name__ == "__main__":
    create_methodology_page()