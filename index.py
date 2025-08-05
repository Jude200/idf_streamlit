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
    create_comparison_plot
)
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
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--primary-color);
        color: white;
        box-shadow: var(--shadow);
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
                        return_periods=np.array([2, 5, 10, 20, 50, 100]), 
                        logger=logger
                    )
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
    """Gère l'analyse IDF"""
    with st.spinner("🧮 Analyse IDF en cours..."):
        with results_col:
            with st.container():
                logger = create_animated_logger(st.container())
                logger.info(f"🚀 Lancement de l'analyse IDF pour la station: {st.session_state.selected_station}")
                
                try:
                    idf = IDF(
                        data_path=st.session_state.temp_file_path, 
                        return_periods=np.array([2, 5, 10, 20, 50, 100]), 
                        logger=logger
                    )
                    
                    # Exécuter l'analyse pour la station sélectionnée
                    idf.do_analysis(st.session_state.selected_station)
                    
                    # Stocker l'IDF dans la session
                    st.session_state.idf = idf
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
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(16, 185, 129, 0.05)); 
                padding: 1.5rem; border-radius: 12px; margin: 1rem 0; text-align: center;
                border: 2px solid rgba(16, 185, 129, 0.3);">
        <h3 style="margin: 0; color: #059669;">🎉 Analyse Terminée!</h3>
        <p style="margin: 0.5rem 0 0 0; color: #065f46;">Station: <strong>{station_name}</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
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
    tab1, tab2, tab3 = st.tabs(["🔵 Courbes IDF", "🔶 Montana", "⚖️ Comparaison"])
    
    with tab1:
        st.markdown("**Courbes IDF** - *Distribution de Gumbel*")
        try:
            fig_idf = create_idf_curves_plot(idf_obj)
            st.pyplot(fig_idf)
            st.caption("📌 Intensités estimées à partir des données observées")
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
        st.markdown("**Comparaison** - *IDF vs Montana*")
        try:
            fig_comparison = create_comparison_plot(idf_obj)
            st.pyplot(fig_comparison)
            st.caption("📌 Évaluation de la qualité d'ajustement")
        except Exception as e:
            st.error(f"Erreur graphique comparaison: {e}")
    
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
    
    # Initialisation des variables de session
    if 'temp_file_path' not in st.session_state:
        st.session_state.temp_file_path = None
    if 'idf' not in st.session_state:
        st.session_state.idf = None
    if 'selected_station' not in st.session_state:
        st.session_state.selected_station = None
    if 'stations_loaded' not in st.session_state:
        st.session_state.stations_loaded = False
    
    # Layout principal avec colonnes
    col1, col2 = st.columns([1, 2], gap="large")
    
    with col1:
        # Section Upload avec style moderne
        # st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📁 Configuration des Données")
        st.markdown('<div style="margin-bottom: 1rem; color: #64748b;">Uploadez votre fichier de données météorologiques</div>', unsafe_allow_html=True)
        
        upload_method, uploaded_files = create_file_upload_section()
        
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
        load_button_style = "🔄 Charger les données" if not st.session_state.stations_loaded else "✅ Données chargées"
        if st.button(load_button_style, type="secondary", disabled=st.session_state.stations_loaded):
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
