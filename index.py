"""
🌧️ Application d'Analyse des Courbes IDF
Interface moderne et intuitive pour l'analyse hydrologique
"""

import streamlit as st
import os
import sys
import numpy as np
import io
import pandas as pd
import json

# Ajouter le répertoire courant au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib.features.streamlit_logging import StreamlitHandler, get_pipeline_logger
from lib.features.loading_animation import create_animated_logger, LoadingAnimator
from lib.features.ui_components import (
    create_file_upload_section,
    process_uploaded_shapefile, 
    setup_page_config,
    create_loading_spinner,
    create_idf_curves_plot,
    create_montana_curves_plot,
    create_cumuls_curve,
    create_comparison_plot,
    create_distribution_plot
)
# from lib.features.documentation import display_idf_methodology, show_documentation_section
from lib.core.idf import IDF

# Configuration de la page
setup_page_config()

# CSS personnalisé moderne et cool
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Variables CSS */
    :root {
        --primary-color: #4f46e5;
        --secondary-color: #06b6d4;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --error-color: #ef4444;
        --border-radius: 12px;
        --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    
    /* Layout principal */
    .main .block-container {
        padding-top: 2rem;
        max-width: 1200px;
        font-family: 'Inter', sans-serif;
    }
    
    /* Titre avec gradient */
    .main-title {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 1rem;
        animation: fadeInUp 0.8s ease-out;
    }
    
    /* Cartes glassmorphism */
    .glass-card {
        background: rgba(255, 255, 255, 0.25);
        backdrop-filter: blur(10px);
        border-radius: var(--border-radius);
        border: 1px solid rgba(255, 255, 255, 0.18);
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: var(--shadow-lg);
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
    }
    
    /* Boutons modernes */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white !important;
        border: none;
        border-radius: var(--border-radius);
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        transition: all 0.3s ease;
        box-shadow: var(--shadow);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
        background: linear-gradient(135deg, #4338ca, #0891b2);
    }
    
    /* Bouton secondaire */
    .stButton > button[kind="secondary"] {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 2px solid var(--primary-color) !important;
        color: var(--primary-color) !important;
    }
    
    .stButton > button[kind="secondary"]:hover {
        background: var(--primary-color) !important;
        color: white !important;
    }
    
    /* Upload area */
    .stFileUploader > div {
        border: 2px dashed var(--primary-color);
        border-radius: var(--border-radius);
        background: linear-gradient(135deg, rgba(79, 70, 229, 0.05), rgba(6, 182, 212, 0.05));
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .stFileUploader > div:hover {
        border-color: var(--secondary-color);
        background: linear-gradient(135deg, rgba(79, 70, 229, 0.1), rgba(6, 182, 212, 0.1));
        transform: scale(1.02);
    }
    
    /* Selectbox */
    .stSelectbox > div > div {
        border-radius: var(--border-radius);
        border: 2px solid rgba(79, 70, 229, 0.2);
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
    }
    
    /* Messages de statut */
    .stAlert {
        border-radius: var(--border-radius);
        border: none;
        animation: slideInRight 0.5s ease-out;
        backdrop-filter: blur(10px);
    }
    
    .stSuccess {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(16, 185, 129, 0.05));
        border-left: 4px solid var(--success-color);
    }
    
    .stWarning {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.1), rgba(245, 158, 11, 0.05));
        border-left: 4px solid var(--warning-color);
    }
    
    .stError {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.1), rgba(239, 68, 68, 0.05));
        border-left: 4px solid var(--error-color);
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
        border-radius: 10px;
    }
    
    /* Dataframe */
    .stDataFrame {
        border-radius: var(--border-radius);
        overflow: hidden;
        box-shadow: var(--shadow);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: var(--border-radius);
        padding: 4px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        transition: all 0.3s ease;
        font-weight: 500;
        padding: 12px 24px !important;
        margin: 0 4px;
        min-width: auto !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--primary-color);
        color: white;
        box-shadow: var(--shadow);
        transform: translateY(-1px);
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(79, 70, 229, 0.1);
        transform: translateY(-1px);
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, rgba(79, 70, 229, 0.1), rgba(6, 182, 212, 0.1));
        border-radius: var(--border-radius);
        transition: all 0.3s ease;
        border: 1px solid rgba(79, 70, 229, 0.2);
    }
    
    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg, rgba(79, 70, 229, 0.15), rgba(6, 182, 212, 0.15));
        transform: translateX(4px);
    }
    
    /* Animations */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(30px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    /* Metrics */
    .metric-container {
        background: linear-gradient(135deg, rgba(79, 70, 229, 0.1), rgba(6, 182, 212, 0.1));
        padding: 1rem;
        border-radius: var(--border-radius);
        text-align: center;
        border: 1px solid rgba(79, 70, 229, 0.2);
    }
    
    /* Download buttons */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #059669, #10b981) !important;
        color: white !important;
        border: none !important;
        border-radius: var(--border-radius) !important;
        padding: 0.5rem 1rem !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        box-shadow: var(--shadow) !important;
    }
    
    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #047857, #059669) !important;
        transform: translateY(-1px) !important;
        box-shadow: var(--shadow-lg) !important;
    }
    
    .stDownloadButton > button:active {
        transform: translateY(0) !important;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .main-title { font-size: 2rem; }
        .glass-card { padding: 1rem; margin: 0.5rem 0; }
        .stDownloadButton > button { font-size: 0.8rem !important; padding: 0.4rem 0.8rem !important; }
    }
</style>
""", unsafe_allow_html=True)

def handle_data_loading(uploaded_files, results_col):
    """Gère le chargement et le traitement des données"""
    with st.spinner("🔄 Traitement du fichier en cours..."):
        with results_col:
            with st.container():
                logger = create_animated_logger(st.container())
                logger.info("📤 Traitement du fichier en cours...")
                
                try:
                    st.session_state.temp_file_path = process_uploaded_shapefile(uploaded_files)
                    logger.info("✅ Fichier traité avec succès")
                    
                    # Créer une instance IDF temporaire pour récupérer les stations
                    temp_idf = IDF(
                        data_path=st.session_state.temp_file_path, 
                        return_periods=np.array([5, 10, 20, 50, 100]), 
                        windows=np.array([1, 2, 4, 8, 24]),
                        logger=logger
                    )
                    # Afficher les stations disponibles
                    # print("Stations disponibles:", temp_idf.stations)
                    st.session_state.stations_loaded = True
                    st.session_state.available_stations = temp_idf.stations
                    logger.info(f"🏢 {len(temp_idf.stations)} stations disponibles")
                    st.rerun()
                    
                except Exception as e:
                    st.session_state.temp_file_path = None
                    st.session_state.stations_loaded = False
                    error_msg = f"Erreur lors du traitement: {str(e)}"
                    st.error(f"❌ {error_msg}")
                    logger.error(error_msg)

def handle_analysis(results_col):
    """Gère l'analyse IDF avec paramètres personnalisés"""
    with st.spinner("🧮 Analyse IDF en cours..."):
        with results_col:
            with st.container():
                logger = create_animated_logger(st.container())
                logger.info(f"🚀 Lancement de l'analyse IDF pour la station: {st.session_state.selected_station}")
                
                # Récupérer les paramètres personnalisés ou utiliser les valeurs par défaut
                custom_periods = getattr(st.session_state, 'custom_periods', [5, 10, 20, 50, 100])
                custom_durations = getattr(st.session_state, 'custom_durations', [1, 2, 4, 8, 24])
                
                logger.info(f"📊 Périodes de retour: {custom_periods}")
                logger.info(f"⏱️ Durées d'agrégation: {custom_durations}h")
                
                try:
                    idf = IDF(
                        data_path=st.session_state.temp_file_path, 
                        return_periods=np.array(custom_periods),
                        windows=np.array(custom_durations),
                        logger=logger
                    )
                    
                    # Exécuter l'analyse pour la station sélectionnée
                    idf.do_analysis(st.session_state.selected_station)
                    
                    # Stocker l'IDF dans la session avec les paramètres utilisés
                    st.session_state.idf = idf
                    st.session_state.analysis_periods = custom_periods
                    st.session_state.analysis_durations = custom_durations
                    
                    logger.info(f"🎉 Analyse IDF terminée avec succès!")
                    
                    st.success(f'✅ Analyse terminée pour la station **{st.session_state.selected_station}**!')
                    st.balloons()  # Animation de célébration
                    st.rerun()
                    
                except Exception as e:
                    error_msg = f"Erreur lors de l'analyse IDF: {str(e)}"
                    st.error(f"❌ {error_msg}")
                    logger.error(error_msg)

def display_results(idf_obj, station_name):
    """Affiche les résultats de l'analyse IDF"""
    # Récupérer les paramètres utilisés pour l'analyse
    analysis_periods = getattr(st.session_state, 'analysis_periods', [5, 10, 20, 50, 100])
    analysis_durations = getattr(st.session_state, 'analysis_durations', [1, 2, 4, 8, 24])
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(16, 185, 129, 0.05)); 
                padding: 1.5rem; border-radius: 12px; margin: 1rem 0; text-align: center;
                border: 2px solid rgba(16, 185, 129, 0.3);">
        <h3 style="margin: 0; color: #059669;">🎉 Analyse Terminée!</h3>
        <p style="margin: 0.5rem 0 0 0; color: #065f46;">Station: <strong>{station_name}</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Affichage des paramètres de configuration utilisés
    # st.markdown("### ⚙️ Configuration Utilisée")
    # col1, col2 = st.columns(2)
    
    # with col1:
    #     periods_text = ", ".join([f"{p} ans" for p in analysis_periods])
    #     st.markdown(f"""
    #     <div style="background: rgba(79, 70, 229, 0.1); padding: 1rem; border-radius: 8px; text-align: center;">
    #         <h4 style="margin: 0; color: #4f46e5;">🎯 Périodes de Retour</h4>
    #         <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem;">{periods_text}</p>
    #     </div>
    #     """, unsafe_allow_html=True)
    
    # with col2:
    #     durations_text = ", ".join([f"{d}h" for d in analysis_durations])
    #     st.markdown(f"""
    #     <div style="background: rgba(6, 182, 212, 0.1); padding: 1rem; border-radius: 8px; text-align: center;">
    #         <h4 style="margin: 0; color: #06b6d4;">⏱️ Durées d'Agrégation</h4>
    #         <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem;">{durations_text}</p>
    #     </div>
    #     """, unsafe_allow_html=True)
    
    # Métriques importantes
    # col1, col2, col3 = st.columns(3)
    # with col1:
    #     st.markdown(f"""
    #     <div class="metric-container">
    #         <h3 style="margin: 0; color: var(--primary-color);">🏢</h3>
    #         <p style="margin: 0; font-weight: 600;">{station_name}</p>
    #         <small>Station</small>
    #     </div>
    #     """, unsafe_allow_html=True)
    
    # with col2:
    #     st.markdown(f"""
    #     <div class="metric-container">
    #         <h3 style="margin: 0; color: var(--secondary-color);">⏱️</h3>
    #         <p style="margin: 0; font-weight: 600;">{len(idf_obj.columns)}</p>
    #         <small>Durées</small>
    #     </div>
    #     """, unsafe_allow_html=True)
    
    # with col3:
    #     st.markdown(f"""
    #     <div class="metric-container">
    #         <h3 style="margin: 0; color: var(--success-color);">📅</h3>
    #         <p style="margin: 0; font-weight: 600;">{len(idf_obj.return_periods)}</p>
    #         <small>Périodes</small>
    #     </div>
    #     """, unsafe_allow_html=True)
    
    # Affichage des résultats avec style moderne
    with st.expander("📊 Paramètres de Montana", expanded=True):
        montana_params_df = idf_obj.get_montana_params()
        st.dataframe(montana_params_df, use_container_width=True)
        
        # Bouton d'export Excel pour les paramètres de Montana
        excel_buffer = io.BytesIO()
        montana_params_df.to_excel(excel_buffer, index=True, engine='openpyxl')
        st.download_button(
            label="📊 Export Excel",
            data=excel_buffer.getvalue(),
            file_name=f"parametres_montana_{station_name}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            help="Télécharger les paramètres de Montana au format Excel"
        )
    
    with st.expander("📈 Intensités Estimées"):
        intensites_df = idf_obj.montana_estimator
        st.dataframe(intensites_df, use_container_width=True)
        
        # Bouton d'export Excel pour les intensités estimées
        excel_buffer = io.BytesIO()
        intensites_df.to_excel(excel_buffer, index=True, engine='openpyxl')
        st.download_button(
            label="📊 Export Excel",
            data=excel_buffer.getvalue(),
            file_name=f"intensites_estimees_{station_name}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            help="Télécharger les intensités estimées au format Excel"
        )
    
    # Graphiques avec onglets modernes
    st.markdown("### 📈 Visualisations")
    tab1, tab2, tab3, tab4 = st.tabs([" Courbes - Gumbel", " Courbes - Montana", " Cumuls", " Comparaison"])
    
    with tab1:
        st.markdown("**Courbes IDF** - *Intensité vs Durée*")
        try:
            fig_idf = create_idf_curves_plot(idf_obj)
            st.pyplot(fig_idf)
            st.caption("📌 Courbes Intensité-Durée-Fréquence - Gumbel")
        except Exception as e:
            st.error(f"Erreur graphique IDF: {e}")
    
    with tab2:
        st.markdown("**Courbes Montana** - *Modèle I = b × t^(-a)*")
        try:
            fig_montana = create_montana_curves_plot(idf_obj)
            st.pyplot(fig_montana)
            st.caption("📌 Modèle de Montana avec paramètres ajustés")
        except Exception as e:
            st.error(f"Erreur graphique Montana: {e}")
    
    with tab3:
        st.markdown("**Cumuls Annuels** - *Précipitations cumulées*")
        try:
            fig_cumuls = create_cumuls_curve(idf_obj)
            st.pyplot(fig_cumuls)
            st.caption("📌 Cumul annuel des précipitations par période de retour")
        except Exception as e:
            st.error(f"Erreur graphique cumuls: {e}")
    
    with tab4:
        st.markdown("**Comparaison** - *IDF vs Montana*")
        try:
            fig_comparison = create_comparison_plot(idf_obj)
            st.pyplot(fig_comparison)
            st.caption("📌 Comparaison entre courbes IDF Gumbel et modèle de Montana")
        except Exception as e:
            st.error(f"Erreur graphique comparaison: {e}")
        # try:
        #     fig_cumuls = create_cumuls_curve(idf_obj)
        #     st.pyplot(fig_cumuls)
        #     st.caption("📌 Cumul annuel des précipitations par période de retour")
        # except Exception as e:
        #     st.error(f"Erreur graphique cumuls: {e}")
    
    # Onglet supplémentaire pour la distribution
    # st.markdown("---")
    # with st.expander("📊 Analyse des Distributions (Ajustements Gumbel)", expanded=False):
    #     st.markdown("**Ajustements Gumbel** - *Distribution des valeurs extrêmes*")
    #     try:
    #         fig_distribution = create_distribution_plot(idf_obj)
    #         st.pyplot(fig_distribution)
    #         st.caption("📌 Analyse statistique des ajustements Gumbel par durée")
    #     except Exception as e:
    #         st.error(f"Erreur graphique distribution: {e}")
    
    # with tab4:
    #     st.markdown("**Méthodologie de Calcul** - *Comprendre les courbes IDF*")
    #     try:
    #         display_idf_methodology()
    #     except Exception as e:
    #         st.error(f"Erreur affichage documentation: {e}")
    #         # Fallback: affichage d'informations de base
    #         st.markdown("""
    #         ### 📚 Guide Méthodologique IDF
            
    #         Les courbes **Intensité-Durée-Fréquence (IDF)** permettent de déterminer 
    #         l'intensité de précipitation pour une durée donnée et un temps de retour spécifique.
            
    #         **Processus de calcul** :
    #         1. **📊 Échantillonnage** : Maxima annuels par durée  
    #         2. **📈 Ajustement** : Loi de Gumbel pour modéliser les valeurs extrêmes
    #         3. **⏰ Temps de retour** : P = 1 - 1/T
    #         4. **🔢 Montana** : I = a × D^(-b)
    #         5. **📊 Courbes IDF** : Visualisation finale
            
    #         **Formule clé** : $I_T(D) = a_T × D^{-b_T}$
    #         """)
    
    # # Section d'export complet
    # st.markdown("---")
    # st.markdown("### 💾 Export Complet des Résultats")
    
    # with st.container():
    #     st.markdown("""
    #     <div style="background: linear-gradient(135deg, rgba(79, 70, 229, 0.1), rgba(6, 182, 212, 0.1)); 
    #                 padding: 1.5rem; border-radius: 12px; margin: 1rem 0; text-align: center;
    #                 border: 2px solid rgba(79, 70, 229, 0.3);">
    #         <h4 style="margin: 0; color: #4f46e5;">📋 Rapport Complet d'Analyse IDF</h4>
    #         <p style="margin: 0.5rem 0 0 0; color: #6366f1;">Exportez tous les résultats de l'analyse en un seul fichier</p>
    #     </div>
    #     """, unsafe_allow_html=True)
        
    #     col1, col2 = st.columns(2)
    #     with col1:
    #         # Export Excel complet avec plusieurs feuilles
    #         excel_buffer_complete = io.BytesIO()
    #         with pd.ExcelWriter(excel_buffer_complete, engine='openpyxl') as writer:
    #             # Feuille 1: Paramètres de Montana
    #             idf_obj.get_montana_params().to_excel(writer, sheet_name='Paramètres Montana', index=True)
                
    #             # Feuille 2: Intensités estimées
    #             idf_obj.montana_estimator.to_excel(writer, sheet_name='Intensités Estimées', index=True)
                
    #             # Feuille 3: Intensités IDF originales
    #             idf_obj.intensity_estimator.to_excel(writer, sheet_name='Intensités IDF', index=True)
                
    #             # Feuille 4: Statistiques de base
    #             if hasattr(idf_obj, 'summary'):
    #                 idf_obj.summary.to_excel(writer, sheet_name='Statistiques', index=True)
            
    #         st.download_button(
    #             label="📊 Rapport Excel Complet",
    #             data=excel_buffer_complete.getvalue(),
    #             file_name=f"rapport_idf_complet_{station_name}.xlsx",
    #             mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    #             help="Télécharger un fichier Excel avec tous les résultats (plusieurs onglets)"
    #         )
        
    #     with col2:
    #         # Export JSON complet
    #         rapport_json = {
    #             "station": station_name,
    #             "parametres_montana": idf_obj.get_montana_params().to_dict('index'),
    #             "intensites_estimees": idf_obj.montana_estimator.to_dict('index'),
    #             "intensites_idf": idf_obj.intensity_estimator.to_dict('index'),
    #             "periodes_retour": list(idf_obj.return_periods),
    #             "durees": list(idf_obj.columns.astype(str))
    #         }
            
    #         if hasattr(idf_obj, 'summary'):
    #             rapport_json["statistiques"] = idf_obj.summary.to_dict('index')
            
    #         st.download_button(
    #             label="🔗 Rapport JSON Complet",
    #             data=json.dumps(rapport_json, indent=2, ensure_ascii=False),
    #             file_name=f"rapport_idf_complet_{station_name}.json",
    #             mime="application/json",
    #             help="Télécharger tous les résultats au format JSON structuré"
    #         )

def display_instructions():
    """Affiche les instructions d'utilisation"""
    # st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 📋 Instructions")
    st.markdown("""
    <div style="line-height: 1.8;">
    <strong>🔄 Étapes d'utilisation:</strong><br><br>
    
    <span style="color: #4f46e5;">1️⃣</span> <strong>Upload</strong> - Déposez votre fichier CSV/Excel<br>
    <span style="color: #06b6d4;">2️⃣</span> <strong>Chargement</strong> - Cliquez sur "Charger les données"<br>
    <span style="color: #10b981;">3️⃣</span> <strong>Station</strong> - Sélectionnez une station météo<br>
    <span style="color: #f59e0b;">4️⃣</span> <strong>Analyse</strong> - Lancez l'analyse IDF<br>
    <span style="color: #ef4444;">5️⃣</span> <strong>Résultats</strong> - Consultez les courbes générées<br><br>
    
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    # Titre principal avec style moderne
    st.markdown('<h1 class="main-title">🌧️ Analyse des Courbes IDF</h1>', unsafe_allow_html=True)
    st.markdown('<div style="text-align: center; margin-bottom: 1rem; color: #64748b; font-size: 1.1rem;">Intensité • Durée • Fréquence </div>', unsafe_allow_html=True)
    
    # Barre de séparation élégante
    st.markdown('<div style="height: 2px; background: linear-gradient(90deg, #4f46e5, #06b6d4, #10b981); margin: 2rem 0; border-radius: 2px;"></div>', unsafe_allow_html=True)
    
    # ========================================
    # 🎛️ SIDEBAR - PERSONNALISATION AVANCÉE
    # ========================================
    with st.sidebar:
        st.markdown("## ⚙️ Configuration Avancée")
        
        # Séparateur visuel
        st.markdown('<div style="height: 1px; background: linear-gradient(90deg, #4f46e5, #06b6d4); margin: 1rem 0;"></div>', unsafe_allow_html=True)
        
        # 🎯 Périodes de retour personnalisables
        st.markdown("### 🎯 Périodes de Retour")
        st.markdown('<small style="color: #64748b;">Sélectionnez les années d\'analyse</small>', unsafe_allow_html=True)
        
        # Options disponibles
        period_options = [2, 5, 10, 20, 25, 50, 100, 200]
        
        # Sélection par défaut (anciennes valeurs)
        default_periods = [5, 10, 20, 50, 100]
        
        selected_periods = st.multiselect(
            "Périodes de retour (années):",
            options=period_options,
            default=default_periods,
            help="Choisissez au moins 2 périodes pour l'analyse"
        )
        
        # Validation des périodes
        if len(selected_periods) < 2:
            st.warning("⚠️ Sélectionnez au moins 2 périodes")
            selected_periods = default_periods
        
        # Affichage des périodes sélectionnées
        periods_text = ", ".join([f"{p} ans" for p in sorted(selected_periods)])
        st.markdown(f'<div style="background: rgba(79, 70, 229, 0.1); padding: 0.5rem; border-radius: 8px; font-size: 0.8rem; margin-top: 0.5rem;"><strong>Sélectionnées:</strong> {periods_text}</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # ⏱️ Durées d'agrégation personnalisables
        st.markdown("### ⏱️ Durées d'Agrégation")
        st.markdown('<small style="color: #64748b;">Sélectionnez les durées d\'analyse</small>', unsafe_allow_html=True)
        
        # Options disponibles
        duration_options = [1, 2, 3, 4, 6, 8, 12, 24]
        duration_labels = [f"{d}h" for d in duration_options]
        
        # Sélection par défaut (anciennes valeurs)
        default_durations = [1, 2, 4, 8, 24]
        default_duration_labels = [f"{d}h" for d in default_durations]
        
        selected_duration_labels = st.multiselect(
            "Durées d'agrégation:",
            options=duration_labels,
            default=default_duration_labels,
            help="Choisissez au moins 2 durées pour l'analyse"
        )
        
        # Convertir les labels en valeurs numériques
        selected_durations = [int(label.replace('h', '')) for label in selected_duration_labels]
        
        # Validation des durées
        if len(selected_durations) < 2:
            st.warning("⚠️ Sélectionnez au moins 2 durées")
            selected_durations = default_durations
        
        # Affichage des durées sélectionnées
        durations_text = ", ".join([f"{d}h" for d in sorted(selected_durations)])
        st.markdown(f'<div style="background: rgba(6, 182, 212, 0.1); padding: 0.5rem; border-radius: 8px; font-size: 0.8rem; margin-top: 0.5rem;"><strong>Sélectionnées:</strong> {durations_text}</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # 📊 Résumé de la configuration
        st.markdown("### 📊 Résumé")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Périodes", len(selected_periods))
        with col2:
            st.metric("Durées", len(selected_durations))
        
        st.markdown("---")
        
        # # 📚 Section Documentation rapide
        # st.markdown("### 📚 Documentation")
        # with st.expander("ℹ️ Guide Rapide IDF", expanded=False):
        #     st.markdown("""
        #     **Processus de calcul IDF** :
            
        #     1. **📊 Échantillonnage** : Maxima annuels
        #     2. **📈 Ajustement** : Loi de Gumbel  
        #     3. **⏰ Temps de retour** : P = 1 - 1/T
        #     4. **🔢 Montana** : I = a × D^(-b)
        #     5. **📊 Visualisation** : Courbes finales
            
        #     **Applications** :
        #     - Dimensionnement hydraulique
        #     - Méthode rationnelle : Q = C × I × A
        #     - Gestion des risques d'inondation
            
        #     💡 *Consultez l'onglet "Documentation" pour plus de détails*
        #     """)
        
        # Sauvegarder dans session state
        st.session_state.custom_periods = sorted(selected_periods)
        st.session_state.custom_durations = sorted(selected_durations)
        
        # Détecter les changements de configuration et réinitialiser l'analyse
        previous_periods = getattr(st.session_state, 'previous_periods', None)
        previous_durations = getattr(st.session_state, 'previous_durations', None)
        
        if (previous_periods != st.session_state.custom_periods or 
            previous_durations != st.session_state.custom_durations):
            # Configuration changée, réinitialiser l'analyse
            if hasattr(st.session_state, 'idf') and st.session_state.idf is not None:
                st.session_state.idf = None
                st.info("🔄 Configuration modifiée - Relancez l'analyse pour appliquer les nouveaux paramètres")
            
            st.session_state.previous_periods = st.session_state.custom_periods
            st.session_state.previous_durations = st.session_state.custom_durations
    
    # Initialisation des variables de session
    if 'temp_file_path' not in st.session_state:
        st.session_state.temp_file_path = None
    if 'idf' not in st.session_state:
        st.session_state.idf = None
    if 'selected_station' not in st.session_state:
        st.session_state.selected_station = None
    if 'stations_loaded' not in st.session_state:
        st.session_state.stations_loaded = False
    if 'uploaded_file_name' not in st.session_state:
        st.session_state.uploaded_file_name = None
    
    # Layout principal avec colonnes
    col1, col2 = st.columns([1, 2], gap="large")
    
    with col1:
        # Section Upload avec style moderne
        # st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📁 Configuration des Données")
        st.markdown('<div style="margin-bottom: 1rem; color: #64748b;">Uploadez votre fichier de données météorologiques</div>', unsafe_allow_html=True)
        
        upload_method, uploaded_files = create_file_upload_section()
        
        # Détecter si un nouveau fichier a été uploadé
        new_file_uploaded = False
        if uploaded_files and (st.session_state.uploaded_file_name != uploaded_files.name):
            new_file_uploaded = True
            st.session_state.uploaded_file_name = uploaded_files.name
            # Réinitialiser les états quand un nouveau fichier est uploadé
            st.session_state.stations_loaded = False
            st.session_state.idf = None
            st.session_state.selected_station = None
            st.session_state.temp_file_path = None
        
        # Informations sur le fichier uploadé
        # if uploaded_files:
            # file_size = uploaded_files.size / 1024  # en KB
            # st.markdown(f"""
            # <div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(16, 185, 129, 0.05)); 
            #             padding: 1rem; border-radius: 8px; margin: 1rem 0; border-left: 4px solid #10b981;">
            #     <strong>📄 {uploaded_files.name}</strong><br>
            #     <small>Taille: {file_size:.1f} KB • Type: {uploaded_files.type}</small>
            # </div>
            # """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Section Actions avec style moderne
        # st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### ⚡ Actions")
        
        # Bouton pour charger les données
        if uploaded_files:
            # Si un fichier est présent, le bouton est toujours disponible
            load_button_style = "🔄 Charger les données" if not st.session_state.stations_loaded else "🔄 Recharger les données"
            button_disabled = False
        else:
            # Pas de fichier uploadé
            load_button_style = "📁 Aucun fichier sélectionné"
            button_disabled = True
        
        if st.button(load_button_style, type="secondary", disabled=button_disabled):
            if not uploaded_files:
                st.error("📁 Veuillez d'abord uploader un fichier")
            else:
                handle_data_loading(uploaded_files, col2)
        
        # Section sélection de station
        if st.session_state.stations_loaded and 'available_stations' in st.session_state:
            st.markdown("---")
            st.markdown("### 🏢 Station Météorologique")
            
            selected_station = st.selectbox(
                "Sélectionnez la station d'analyse:",
                options=st.session_state.available_stations,
                index=0,
                help="Choisissez la station pour l'analyse des courbes IDF"
            )
            
            st.session_state.selected_station = selected_station
            
            # # Badge de station sélectionnée
            # st.markdown(f"""
            # <div style="background: linear-gradient(135deg, rgba(79, 70, 229, 0.1), rgba(6, 182, 212, 0.1)); 
            #             padding: 0.8rem; border-radius: 8px; margin: 1rem 0; text-align: center; 
            #             border: 2px solid rgba(79, 70, 229, 0.2);">
            #     <strong>📍 Station: {selected_station}</strong>
            # </div>
            # """, unsafe_allow_html=True)
        
        # Bouton d'analyse principal
        analysis_disabled = not (st.session_state.stations_loaded and st.session_state.selected_station)
        button_text = "🚀 Lancer l'Analyse IDF" if not analysis_disabled else "⏳ Sélectionnez une station"
        
        if st.button(button_text, type="primary", disabled=analysis_disabled):
            handle_analysis(col2)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Instructions avec style moderne
        if not uploaded_files and not st.session_state.stations_loaded:
            display_instructions()
    
    with col2:
        # Section Résultats avec style moderne
        # st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📊 Tableau de Bord")
        
        # Affichage conditionnel du contenu
        if not st.session_state.idf:
            st.markdown("""
            <div style="text-align: center; padding: 3rem 1rem; color: #64748b;">
                <div style="font-size: 4rem; margin-bottom: 1rem;">📈</div>
                <h3>Prêt pour l'Analyse</h3>
                <p>Uploadez un fichier et sélectionnez une station pour commencer</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            display_results(st.session_state.idf, st.session_state.selected_station)
        
        st.markdown('</div>', unsafe_allow_html=True)

def run_app():
    """🚀 Point d'entrée de l'application moderne"""
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
