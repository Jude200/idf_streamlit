import streamlit as st
import os
import sys
import tempfile
import matplotlib.pyplot as plt
import numpy as np

from lib.const import FIGURE_SIZE



def setup_page_config():
    """
    Set up the Streamlit page configuration.
    
    This should be called at the very beginning of the application.
    """
    st.set_page_config(
        page_title="IDF",
        page_icon="📈",
        layout="wide")  # Use full width of the page

def display_error_message(message):
    """
    Display an error message in the Streamlit interface.
    
    Args:
        message (str): Error message to display
    """
    st.error(message)

def display_warning_message(message):
    """
    Display a warning message in the Streamlit interface.
    
    Args:
        message (str): Warning message to display
    """
    st.warning(message)

def display_info_message(message):
    """
    Display an info message in the Streamlit interface.
    
    Args:
        message (str): Info message to display
    """
    st.info(message)
    

def create_file_upload_section():
    """
    Create a modern file upload section with enhanced UX.
    
    Returns:
        tuple: (upload_method, uploaded_files)
    """
    uploaded_files = None
    upload_method = "Fichiers séparés (.xls, .xlsx, .csv, etc.)"
    
    # Upload moderne avec style personnalisé
    st.markdown("""
    <div style="text-align: center; margin-bottom: 1rem;">
        <p style="color: #64748b; margin: 0;">Glissez-déposez votre fichier ou cliquez pour parcourir</p>
        <small style="color: #94a3b8;">Formats supportés: .xls, .xlsx, .csv</small>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_files = st.file_uploader(
        "Fichier de données météorologiques:",
        type=['xls', 'xlsx', 'csv'],
        accept_multiple_files=False,
        help="Uploadez votre fichier contenant les données de précipitations",
        key="modern_file_uploader",
        label_visibility="collapsed"
    )
    
    if uploaded_files:
        # Affichage moderne du fichier uploadé
        file_info = f"**{uploaded_files.name}** ({uploaded_files.size//1024}KB)"
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(16, 185, 129, 0.05)); 
                    padding: 1rem; border-radius: 8px; margin: 1rem 0; 
                    border-left: 4px solid #10b981; text-align: center;">
            <strong style="color: #065f46;">✅ Fichier uploadé</strong><br>
            <span style="color: #047857;">{file_info}</span>
        </div>
        """, unsafe_allow_html=True)
    
    return upload_method, uploaded_files


def create_loading_spinner(message="Chargement en cours..."):
    """
    Create ANIMATED loading indicator.
    
    Args:
        message (str): Loading message
        
    Returns:
        streamlit spinner context manager
    """
    return st.spinner(message)

def process_uploaded_shapefile(uploaded_files):
    """
    Process uploaded shapefile components and create a temporary shapefile.
    
    Args:
        uploaded_files (list): List of uploaded files (should contain .shp, .shx, .dbf, etc.)
        
    Returns:
        str or None: Path to the main .shp file if successful, None if error
    """
    if not uploaded_files:
        return None
    
    # # Required shapefile extensions
    # required_extensions = {'.xls', '.xlsx', '.csv'}
     
    # # Get file extensions from uploaded files
    # uploaded_extensions = {os.path.splitext(file.name)[1].lower() for file in uploaded_files}

    try:
        # Create a temporary directory

        temp_dir = tempfile.mkdtemp()

        # Save  uploaded files to the temporary directory
        # for uploaded_file in uploaded_files:
        
        file_path = os.path.join(temp_dir, uploaded_files.name)
        with open(file_path, 'wb') as f:
            f.write(uploaded_files.getbuffer())
        
        return file_path
    except Exception as e:
        st.error(f"Erreur lors du traitement des fichiers uploadés: {e}")
        return None
    
def add_padding(pad:float):
    """_summary_

    Args:
        pad (_type_): _description_
    """
    st.markdown(f'<div style="padding: {pad}px;"></div>', unsafe_allow_html=True)

def create_idf_curves_plot(idf_obj):
    """
    Crée les courbes IDF avec un style moderne et professionnel.
    
    Args:
        idf_obj: Objet IDF contenant les données calculées
        
    Returns:
        matplotlib.figure.Figure: Figure contenant les courbes IDF
    """
    # Configuration du graphique avec style moderne
    plt.style.use('default')
    fig, ax = plt.subplots(figsize=FIGURE_SIZE, dpi=100)
    fig.patch.set_facecolor('white')
    
    # Palette de couleurs moderne et professionnelle
    colors = ['#4f46e5', '#06b6d4', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6']
    
    # Tracer une courbe pour chaque période de retour
    for i, period in enumerate(idf_obj.return_periods):
        intensities = idf_obj.intensity_estimator[period].values
        durations = idf_obj.columns.astype(float)
        
        ax.plot(durations, intensities, 
                marker='o', linewidth=3, markersize=8,
                color=colors[i % len(colors)],
                label=f'{period} ans',
                markeredgecolor='white',
                markeredgewidth=2,
                alpha=0.9)
    
    # Configuration des axes avec style moderne
    ax.set_xlabel('Durée (heures)', fontsize=14, fontweight='600', color='#374151')
    ax.set_ylabel('Intensité (mm/h)', fontsize=14, fontweight='600', color='#374151') 
    ax.set_title('Courbes IDF - Intensité vs Durée', 
                fontsize=16, fontweight='700', color='#1f2937', pad=20)
    
    # Grille moderne
    ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5, color='#d1d5db')
    ax.set_axisbelow(True)
    
    # Légende moderne
    legend = ax.legend(title='Période de retour', loc='upper right', 
                      frameon=True, fancybox=True, shadow=True,
                      title_fontsize=12, fontsize=11)
    legend.get_frame().set_facecolor('white')
    legend.get_frame().set_alpha(0.95)
    legend.get_frame().set_edgecolor('#e5e7eb')
    
    # Style des axes
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#e5e7eb')
    ax.spines['bottom'].set_color('#e5e7eb')
    ax.tick_params(colors='#6b7280', labelsize=10)
    
    plt.tight_layout()
    return fig

def create_montana_curves_plot(idf_obj):
    """
    Crée les courbes Montana avec un style moderne et professionnel.
    
    Args:
        idf_obj: Objet IDF contenant les données calculées
        
    Returns:
        matplotlib.figure.Figure: Figure contenant les courbes Montana
    """
    # Configuration du graphique avec style moderne
    plt.style.use('default')
    fig, ax = plt.subplots(figsize=FIGURE_SIZE, dpi=100)
    fig.patch.set_facecolor('white')
    
    # Palette de couleurs moderne et professionnelle
    colors = ['#4f46e5', '#06b6d4', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6']
    
    # Tracer une courbe pour chaque période de retour
    for i, period in enumerate(idf_obj.return_periods):
        intensities = idf_obj.montana_estimator[period].values
        durations = idf_obj.columns.astype(float)
        
        ax.plot(durations, intensities, 
                marker='s', linewidth=3, markersize=8,
                color=colors[i % len(colors)], linestyle='--',
                label=f'{period} ans',
                markeredgecolor='white',
                markeredgewidth=2,
                alpha=0.9)
    
    # Configuration des axes avec style moderne
    ax.set_xlabel('Durée (heures)', fontsize=14, fontweight='600', color='#374151')
    ax.set_ylabel('Intensité (mm/h)', fontsize=14, fontweight='600', color='#374151')
    ax.set_title('Courbes Montana - Modèle I = b × t^(-a)', 
                fontsize=16, fontweight='700', color='#1f2937', pad=20)
    
    # Grille moderne
    ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5, color='#d1d5db')
    ax.set_axisbelow(True)
    
    # Légende moderne
    legend = ax.legend(title='Période de retour', loc='upper right', 
                      frameon=True, fancybox=True, shadow=True,
                      title_fontsize=12, fontsize=11)
    legend.get_frame().set_facecolor('white')
    legend.get_frame().set_alpha(0.95)
    legend.get_frame().set_edgecolor('#e5e7eb')
    
    # Style des axes
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#e5e7eb')
    ax.spines['bottom'].set_color('#e5e7eb')
    ax.tick_params(colors='#6b7280', labelsize=10)
    
    plt.tight_layout()
    return fig

def create_comparison_plot(idf_obj):
    """
    Crée un graphique de comparaison moderne entre les courbes IDF et Montana.
    
    Args:
        idf_obj: Objet IDF contenant les données calculées
        
    Returns:
        matplotlib.figure.Figure: Figure contenant la comparaison
    """
    # Configuration du graphique avec style moderne
    plt.style.use('default')
    fig, ax = plt.subplots(figsize=FIGURE_SIZE, dpi=100)
    fig.patch.set_facecolor('white')
    
    # Palette de couleurs moderne et professionnelle
    colors = ['#4f46e5', '#06b6d4', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6']
    
    # Tracer les courbes pour chaque période de retour
    for i, period in enumerate(idf_obj.return_periods):
        durations = idf_obj.columns.astype(float)
        
        # Courbes IDF (données observées/estimées) - lignes pleines
        idf_intensities = idf_obj.intensity_estimator[period].values
        ax.plot(durations, idf_intensities, 
                marker='o', linewidth=3, markersize=8,
                color=colors[i % len(colors)], linestyle='-',
                label=f'IDF {period} ans',
                markeredgecolor='white',
                markeredgewidth=2,
                alpha=0.9)
        
        # Courbes Montana (modèle ajusté) - lignes pointillées
        montana_intensities = idf_obj.montana_estimator[period].values
        ax.plot(durations, montana_intensities, 
                marker='s', linewidth=2, markersize=6,
                color=colors[i % len(colors)], linestyle='--', alpha=0.7,
                label=f'Montana {period} ans',
                markeredgecolor='white',
                markeredgewidth=1)
    
    # Configuration des axes avec style moderne
    ax.set_xlabel('Durée (heures)', fontsize=14, fontweight='600', color='#374151')
    ax.set_ylabel('Intensité (mm/h)', fontsize=14, fontweight='600', color='#374151')
    ax.set_title('Comparaison IDF vs Montana\nÉvaluation de la qualité d\'ajustement', 
                fontsize=16, fontweight='700', color='#1f2937', pad=20)
    
    # Grille moderne
    ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5, color='#d1d5db')
    ax.set_axisbelow(True)
    
    # Légende moderne avec deux colonnes
    legend = ax.legend(title='Type et Période de retour', loc='upper right', 
                      frameon=True, fancybox=True, shadow=True, ncol=2,
                      title_fontsize=12, fontsize=10)
    legend.get_frame().set_facecolor('white')
    legend.get_frame().set_alpha(0.95)
    legend.get_frame().set_edgecolor('#e5e7eb')
    
    # Style des axes
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#e5e7eb')
    ax.spines['bottom'].set_color('#e5e7eb')
    ax.tick_params(colors='#6b7280', labelsize=10)
    
    # Annotation explicative
    ax.text(0.02, 0.98, 'Lignes pleines: IDF observé\nLignes pointillées: Modèle Montana', 
            transform=ax.transAxes, fontsize=10, color='#6b7280',
            verticalalignment='top', bbox=dict(boxstyle='round,pad=0.3', 
            facecolor='white', edgecolor='#e5e7eb', alpha=0.9))
    
    plt.tight_layout()
    return fig