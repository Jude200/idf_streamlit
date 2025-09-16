"""
📚 Page Documentation IDF - Standalone
Page dédiée pour la documentation méthodologique des courbes IDF
"""

import streamlit as st

# Configuration de la page
st.set_page_config(
    page_title="Documentation IDF",
    page_icon="📚",
    layout="wide"
)

# Documentation intégrée directement dans le fichier pour éviter les problèmes d'import
def display_documentation():
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

# Afficher la documentation
display_documentation()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 0.9rem;">
    📚 Documentation méthodologique des courbes IDF<br>
    🔄 Mise à jour : Septembre 2025 | ⚡ Application IDF v2.0
</div>
""", unsafe_allow_html=True)