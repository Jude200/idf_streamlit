import os
import sys
import logging

import numpy as np

import streamlit as st
from lib.features.streamlit_logging import StreamlitHandler, get_pipeline_logger
from lib.features.loading_animation import create_animated_logger, LoadingAnimator

from lib.features.ui_components import (
    create_file_upload_section,
    process_uploaded_shapefile, 
    setup_page_config,
    create_loading_spinner,
    create_idf_curves_plot,
    create_montana_curves_plot,
    create_comparison_plot
)

from lib.core.idf import IDF


# Configuration de la page
setup_page_config()

# CSS personnalisé pour les animations
st.markdown("""
<style>
    /* Animation pour les containers de logs */
    .log-container {
        animation: fadeIn 0.5s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Style pour les boutons avec animation */
    .stButton > button {
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Animation pour les expanders */
    .streamlit-expanderHeader {
        transition: all 0.2s ease;
    }
    
    /* Style pour les messages de statut */
    .status-message {
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
        animation: slideIn 0.3s ease;
    }
    
    @keyframes slideIn {
        from { transform: translateX(-20px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
</style>
""", unsafe_allow_html=True)

# Ajouter le répertoire courant au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    st.title("📈 Analyse des Courbes IDF (Intensité-Durée-Fréquence)")
    st.markdown("---")
    
    # Initialisation des variables de session
    if 'temp_file_path' not in st.session_state:
        st.session_state.temp_file_path = None
    if 'idf' not in st.session_state:
        st.session_state.idf = None
    
    col1, col2 = st.columns([1, 3])
    
    with col2:
        st.subheader("📊 Résultats et Logs")
        
        # Container pour les logs avec animation - CRÉÉ EN PREMIER
        log_container = st.container()
        
        # Initialisation du logger avec animations
        logger = create_animated_logger(log_container)
        
        # Message initial avec icône
        with log_container:
            st.info("🎯 Application prête - Veuillez uploader un fichier pour commencer")
    
    with col1:
        st.subheader("📁 Upload du fichier")
        upload_method, uploaded_files = create_file_upload_section()
        
        if st.button("🚀 Commencer", type="primary"):
            if not uploaded_files:
                st.warning("Veuillez déposer vos fichiers avant de commencer")
                with log_container:
                    st.warning("⚠️ Aucun fichier uploadé - Veuillez sélectionner un fichier")
            else:
                # Animation de traitement du fichier
                with st.spinner("🔄 Traitement du fichier en cours..."):
                    logger.info("📤 Traitement du fichier en cours...")
                    try:
                        st.session_state.temp_file_path = process_uploaded_shapefile(uploaded_files)
                        logger.info("✅ Fichier traité avec succès")
                    except Exception as e:
                        st.session_state.temp_file_path = None
                        error_msg = f"Erreur lors du traitement: {str(e)}"
                        st.error(f"❌ {error_msg}")
                        logger.error(error_msg)
                    
        if st.session_state.temp_file_path:
            # Animation de l'analyse IDF
            with st.spinner("🧮 Analyse IDF en cours..."):
                logger.info("🚀 Lancement de l'analyse IDF...")
                try:
                    idf = IDF(
                        data_path=st.session_state.temp_file_path, 
                        return_periods=np.array([2, 5, 10, 20, 50, 100]), 
                        logger=logger
                    )
                    # Stocker l'IDF dans la session pour éviter de le recalculer
                    st.session_state.idf = idf
                    logger.info("🎉 Analyse IDF terminée avec succès!")
                    
                    # Animation de succès
                    # st.balloons()  # Animation de ballons pour célébrer le succès
                    st.success('✅ Analyse IDF terminée avec succès!')
                    
                    # Affichage des résultats dans la colonne 2 sous les logs
                    with col2:
                        st.markdown("### 📊 Résultats de l'analyse")
                        
                        # Affichage des résultats
                        with st.expander("📊 Résultats des paramètres de Montana", expanded=True):
                            st.dataframe(idf.get_montana_params(), use_container_width=True)
                        
                        with st.expander("📈 Intensités estimées"):
                            st.dataframe(idf.montana_estimator, use_container_width=True)
                        
                        # Affichage des graphiques
                        st.markdown("### 📈 Visualisations des courbes")
                        
                        # Onglets pour les différents graphiques
                        tab1, tab2, tab3 = st.tabs(["🔵 Courbes IDF", "🔶 Courbes Montana", "⚖️ Comparaison"])
                        
                        with tab1:
                            st.markdown("#### Courbes IDF - Intensité moyenne en fonction de la durée")
                            st.markdown("*Basées sur les intensités estimées par la distribution de Gumbel*")
                            try:
                                fig_idf = create_idf_curves_plot(idf)
                                st.pyplot(fig_idf)
                                st.caption("📌 Ces courbes montrent les intensités pluviométriques estimées directement à partir des données observées")
                            except Exception as e:
                                st.error(f"Erreur lors de la création du graphique IDF: {e}")
                        
                        with tab2:
                            st.markdown("#### Courbes Montana - Intensité moyenne en fonction de la durée")
                            st.markdown("*Basées sur le modèle de Montana avec paramètres ajustés*")
                            try:
                                fig_montana = create_montana_curves_plot(idf)
                                st.pyplot(fig_montana)
                                st.caption("📌 Ces courbes utilisent la formule de Montana: I = b × t^(-a)")
                            except Exception as e:
                                st.error(f"Erreur lors de la création du graphique Montana: {e}")
                        
                        with tab3:
                            st.markdown("#### Comparaison IDF vs Montana")
                            st.markdown("*Comparaison entre les deux approches*")
                            try:
                                fig_comp = create_comparison_plot(idf)
                                st.pyplot(fig_comp)
                                st.caption("📌 Lignes pleines: courbes IDF | Lignes pointillées: courbes Montana")
                            except Exception as e:
                                st.error(f"Erreur lors de la création du graphique de comparaison: {e}")
                
                except Exception as e:
                    error_msg = f"Erreur lors de l'analyse IDF: {str(e)}"
                    st.error(f"❌ {error_msg}")
                    logger.error(error_msg)
                    st.exception(e)
        
        # Affichage des instructions si aucun fichier n'est uploadé
        if not uploaded_files and not st.session_state.temp_file_path:
            st.info("""
            **Instructions d'utilisation :**
            
            1. 📁 Uploadez un fichier CSV/Excel contenant :
               - Une colonne 'Year' avec les années
               - Des colonnes avec les durées en heures (1, 2, 3, 6, 12, 24, etc.)
               - Les valeurs de précipitations maximales annuelles
            
            2. 🚀 Cliquez sur "Commencer" pour lancer l'analyse
            
            3. 📈 Consultez les résultats des courbes IDF
            """)

def run_app():
    """🚀 Point d'entrée de l'application révolutionnaire"""
    try:
        main()
    except Exception as e:
        st.error(f"❌ **Erreur inattendue:** {e}")
        st.write("Contactez le support technique si le problème persiste.")

# ===========================================
# 🎬 LANCEMENT DE L'APPLICATION
# ===========================================

if __name__ == "__main__":
    run_app()
