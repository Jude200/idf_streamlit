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
        
        À partir des données de précipitation (pas de temps 5 minutes) :
        
        ```python
        # Calcul des intensités pour différentes durées glissantes
        df[1] = df_raw.rolling(pd.Timedelta(1, "h")).sum()      # 1 heure
        df[2] = df_raw.rolling(pd.Timedelta(2, "h")).sum() / 2  # 2 heures  
        df[4] = df_raw.rolling(pd.Timedelta(4, "h")).sum() / 4  # 4 heures
        df[8] = df_raw.rolling(pd.Timedelta(8, "h")).sum() / 8  # 8 heures
        df[24] = df_raw.rolling(pd.Timedelta(24, "h")).sum() / 24  # 24 heures
        ```
        
        ### 2.2 Extraction des maxima annuels
        
        **Principe** : Chaque année constitue un "bloc" indépendant
        
        ```python
        # Maxima annuels pour chaque durée
        YearMax = df.resample('YE').max()
        
        # Dates des maxima (optionnel, pour analyse)
        DateMax = df.resample('YE').apply(custom_resampler)
        ```
        
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
        ```python
        # Fonction de répartition empirique
        probs = (ranks - 0.5) / N_obs
        
        # Variable de Gumbel
        U = -np.log(-np.log(probs))
        
        # Régression linéaire
        regression = scipy.stats.linregress(U, observations)
        μ = regression.intercept
        σ = regression.slope
        ```
        
        **B) Ajustement par maximum de vraisemblance** :
        ```python
        # Utilisation de scipy (recommandé)
        fit_params = scipy.stats.genextreme.fit(data, fc=0)
        μ = fit_params[1]  # Paramètre de position
        σ = fit_params[2]  # Paramètre d'échelle
        ```
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
        
        ```python
        # Pour chaque durée et temps de retour
        for duration in durations:
            for T in return_periods:
                # Probabilité de non-dépassement
                prob = 1 - (1/T)
                
                # Loi de Gumbel ajustée pour cette durée
                gumbel_dist = scipy.stats.genextreme(loc=μ, scale=σ, c=0)
                
                # Valeur d'intensité correspondante
                intensity = gumbel_dist.ppf(prob)
        ```
        
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
        
        ```python
        # Pour chaque temps de retour
        for T in return_periods:
            log_intensities = np.log(intensities[T])
            log_durations = np.log(durations)
            
            # Régression linéaire
            regression = scipy.stats.linregress(log_durations, log_intensities)
            
            # Coefficients de Montana
            a[T] = np.exp(regression.intercept)  # Ordonnée à l'origine → a
            b[T] = -regression.slope             # Pente négative → b
        ```
        
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
        
        ```python
        # 1. Génération d'une grille durée × temps de retour
        durations = np.logspace(0, 2, 100)  # 1h à 100h (échelle log)
        return_periods = [2, 5, 10, 20, 50, 100]
        
        # 2. Calcul des intensités avec Montana
        for T in return_periods:
            intensities[T] = a[T] * durations**(-b[T])
        
        # 3. Représentation graphique
        plt.loglog(durations, intensities[T], label=f'{T} ans')
        ```
        
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
        - **I** : Intensité IDF pour $T$ et $t_c$ → **$I_T(t_c)$**
        - **A** : Surface du bassin versant (ha)
        
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
        - Données : (1h→75.4), (2h→64.2), (4h→48.1), (8h→35.7), (24h→21.8)
        - Résultat : $I_{100}(D) = 85.4 \\times D^{-0.42}$
        - Coefficients : a = 85.4, b = 0.42
        - R² = 0.98
        
        ### Étape 5 : Application pratique
        
        **Dimensionnement d'un bassin de 5 ha, C=0.6, T=10 ans, tc=2h** :
        
        ```python
        I_10_2h = 68.4 * 2**(-0.38) = 52.1 mm/h
        Q_max = 0.6 * 52.1 * 5 = 156.3 m³/h = 43.4 l/s
        ```
        """)

def display_quality_control():
    """
    Affiche les méthodes de contrôle qualité et validation
    """
    
    st.markdown("## ✅ Contrôle Qualité et Validation")
    
    with st.expander("🔍 **Tests de Validation Statistique**"):
        st.markdown("""
        ### 1. Test d'ajustement de la loi
        
        **Test de Kolmogorov-Smirnov** :
        ```python
        from scipy.stats import kstest
        
        # Test d'ajustement à la loi de Gumbel
        statistic, p_value = kstest(observations, gumbel_cdf)
        
        # Critère : p_value > 0.05 pour accepter H0 (bon ajustement)
        ```
        
        **Test d'Anderson-Darling** :
        Plus sensible aux queues de distribution (valeurs extrêmes)
        
        ### 2. Qualité de la régression Montana
        
        **Coefficient de détermination** :
        - R² > 0.95 : Excellent ajustement
        - R² > 0.90 : Bon ajustement  
        - R² < 0.90 : Ajustement questionnable
        
        **Analyse des résidus** :
        ```python
        residuals = np.log(I_observed) - np.log(I_montana)
        # Vérifier : moyenne ≈ 0, distribution normale, pas de tendance
        ```
        
        ### 3. Cohérence des coefficients
        
        **Coefficient b** :
        - Domaine physique : 0.3 < b < 1.2
        - Valeurs typiques : 0.4 à 0.8
        - Cohérence climatique : b plus faible en climat tropical
        
        **Coefficient a** :
        - Croissance monotone avec le temps de retour
        - Cohérence avec les valeurs régionales
        
        ### 4. Tests de robustesse
        
        **Bootstrap** :
        ```python
        # Génération d'échantillons bootstrap
        bootstrap_params = []
        for i in range(1000):
            sample = np.random.choice(data, size=len(data), replace=True)
            params = fit_gumbel(sample)
            bootstrap_params.append(params)
        
        # Intervalles de confiance à 95%
        CI_95 = np.percentile(bootstrap_params, [2.5, 97.5], axis=0)
        ```
        
        **Validation croisée** :
        - Diviser les données en périodes
        - Ajuster sur période 1, valider sur période 2
        - Comparer les paramètres obtenus
        """)
    
    with st.expander("⚠️ **Limitations et Précautions**"):
        st.markdown("""
        ### Sources d'erreur principales
        
        **1. Échantillonnage insuffisant** :
        - Minimum recommandé : 20-30 ans
        - Impact : Sous-estimation des valeurs extrêmes
        - Solution : Analyse régionale, méthodes bayésiennes
        
        **2. Non-stationnarité climatique** :
        - Changement climatique
        - Modifications d'occupation du sol  
        - Solution : Tests de stationnarité, modèles non-stationnaires
        
        **3. Données manquantes ou erronées** :
        - Lacunes dans les séries
        - Erreurs de mesure ou de saisie
        - Solution : Contrôle qualité préalable, reconstitution
        
        **4. Extrapolation spatiale** :
        - Station non représentative du site d'étude
        - Climat local différent
        - Solution : Analyse de plusieurs stations, régionalisation
        
        ### Recommandations pratiques
        
        ✅ **Toujours** :
        - Vérifier l'homogénéité des données
        - Calculer les intervalles de confiance
        - Comparer avec les valeurs régionales
        - Documenter les hypothèses et limitations
        
        ⚠️ **Éviter** :
        - Extrapolation au-delà du domaine d'ajustement
        - Utilisation sans validation des hypothèses
        - Négligence des incertitudes
        - Application aveugle des formules
        
        ### Mise à jour et révision
        
        📅 **Fréquence recommandée** :
        - Révision tous les 10-15 ans minimum
        - Intégration de nouvelles données annuelles
        - Réévaluation après événements extrêmes
        - Adaptation aux évolutions climatiques
        """)

def display_references():
    """
    Affiche les références bibliographiques et ressources
    """
    
    st.markdown("## 📚 Références et Ressources")
    
    with st.expander("📖 **Bibliographie Technique**"):
        st.markdown("""
        ### Ouvrages de référence
        
        **Hydrologie statistique** :
        - Musy, A. & Higy, C. (2004). *Hydrologie : Une science de la nature*. PPUR.
        - Roche, M. (1963). *Hydrologie de surface*. Gauthier-Villars.
        - Hingray, B., Picouet, C., & Musy, A. (2009). *Hydrologie 2 : Une science pour l'ingénieur*. PPUR.
        
        **Statistiques des extrêmes** :
        - Coles, S. (2001). *An Introduction to Statistical Modeling of Extreme Values*. Springer.
        - Katz, R. W., Parlange, M. B., & Naveau, P. (2002). Statistics of extremes in hydrology. *Advances in Water Resources*, 25(8-12), 1287-1304.
        
        **Applications pratiques** :
        - Chow, V. T., Maidment, D. R., & Mays, L. W. (1988). *Applied Hydrology*. McGraw-Hill.
        - Shaw, E. M., Beven, K. J., Chappell, N. A., & Lamb, R. (2010). *Hydrology in Practice*. CRC Press.
        
        ### Standards et normes
        
        **France** :
        - Instruction technique pour la surveillance et l'entretien des ouvrages d'art (ITSEOA)
        - Guide technique SETRA : "Assainissement routier"
        - Circulaire du 12 mai 1995 relative à l'assainissement des routes nationales
        
        **International** :
        - WMO (2008). *Guide to Hydrological Practices*. World Meteorological Organization.
        - Stedinger, J. R., Vogel, R. M., & Foufoula-Georgiou, E. (1993). Frequency analysis of extreme events. *Handbook of Hydrology*.
        
        ### Ressources numériques
        
        **Logiciels spécialisés** :
        - R : Packages `extRemes`, `evd`, `ismev`
        - Python : Modules `scipy.stats`, `pyextremes`
        - MATLAB : Statistics and Machine Learning Toolbox
        
        **Bases de données** :
        - Météo-France : Données climatologiques
        - AMMA-CATCH : Observatoire hydrométéorologique Afrique de l'Ouest
        - GRDC : Global Runoff Data Centre
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
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Méthodologie", 
        "🔢 Exemple de calcul", 
        "✅ Contrôle qualité",
        "📚 Références"
    ])
    
    with tab1:
        display_idf_methodology()
    
    with tab2:
        display_calculation_example()
    
    with tab3:
        display_quality_control()
    
    with tab4:
        display_references()
    
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