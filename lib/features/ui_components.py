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
    Create a compact file upload section using TABS for better UX.
    
    Returns:
        tuple: (upload_method, uploaded_files, uploaded_zip)
    """
    # Use tabs instead of radio buttons for more modern interface
    # tab1, tab2 = st.tabs(["📁 Fichiers", "📦 Archive ZIP"])
    
    uploaded_files = None
    upload_method = None
    
    upload_method = "Fichiers séparés (.xls, .xlsx, .csv, etc.)"
    uploaded_files = st.file_uploader(
        "Glissez-déposez vos fichiers shapefile:",
        type=['xls', 'xlsx', 'csv'],
        accept_multiple_files=False,
        help="Minimum: .xls, .xlsx, .csv",
        key="separate_files_uploader"
    )
    
    if uploaded_files:
        # Compact file display
        file_info = [f"**{f.name}** ({f.size//1024}KB)" for f in [uploaded_files]]
        st.success(f"✅ fichier uploadé")
        # with st.expander("📋 Détails du fichier"):
        #     st.write(" • ".join(file_info))
    
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
    Crée les courbes IDF - Intensité moyenne en fonction de la durée.
    
    Args:
        idf_obj: Objet IDF contenant les données calculées
        
    Returns:
        matplotlib.figure.Figure: Figure contenant les courbes IDF
    """
    # Configuration du graphique
    fig, ax = plt.subplots(figsize=FIGURE_SIZE)
    
    # Couleurs pour chaque période de retour  
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
    
    # Tracer une courbe pour chaque période de retour
    for i, period in enumerate(idf_obj.return_periods):
        intensities = idf_obj.intensity_estimator[period].values
        durations = idf_obj.columns.astype(float)
        
        ax.plot(durations, intensities, 
                 marker='o', linewidth=2, markersize=6,
                 color=colors[i % len(colors)],
                 label=f'{period} ans')
    
    # Configuration des axes et labels
    ax.set_xlabel('Durée (heures)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Intensité (mm/h)', fontsize=12, fontweight='bold') 
    ax.set_title('Courbes IDF - Intensité moyenne en fonction de la durée', 
                fontsize=14, fontweight='bold', pad=20)
    
    # Configuration de la grille
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(title='Période de retour', loc='upper right', frameon=True, fancybox=True)
    
    # Amélioration de l'apparence
    ax.tick_params(axis='both', which='major', labelsize=10)
    plt.tight_layout()
    
    return fig

def create_montana_curves_plot(idf_obj):
    """
    Crée les courbes Montana - Intensité moyenne en fonction de la durée.
    
    Args:
        idf_obj: Objet IDF contenant les données calculées
        
    Returns:
        matplotlib.figure.Figure: Figure contenant les courbes Montana
    """
    # Configuration du graphique
    fig, ax = plt.subplots(figsize=FIGURE_SIZE)
    
    # Couleurs pour chaque période de retour
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
    
    # Tracer une courbe pour chaque période de retour
    for i, period in enumerate(idf_obj.return_periods):
        intensities = idf_obj.montana_estimator[period].values
        durations = idf_obj.columns.astype(float)
        
        ax.plot(durations, intensities, 
                 marker='s', linewidth=2, markersize=6,
                 color=colors[i % len(colors)], linestyle='--',
                 label=f'{period} ans')
    
    # Configuration des axes et labels
    ax.set_xlabel('Durée (heures)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Intensité (mm/h)', fontsize=12, fontweight='bold')
    ax.set_title('Courbes Montana - Intensité moyenne en fonction de la durée', 
                fontsize=14, fontweight='bold', pad=20)
    
    # Configuration de la grille
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(title='Période de retour', loc='upper right', frameon=True, fancybox=True)
    
    # Amélioration de l'apparence
    ax.tick_params(axis='both', which='major', labelsize=10)
    plt.tight_layout()
    
    return fig

def create_comparison_plot(idf_obj):
    """
    Crée un graphique de comparaison entre les courbes IDF et Montana.
    
    Args:
        idf_obj: Objet IDF contenant les données calculées
        
    Returns:
        matplotlib.figure.Figure: Figure contenant la comparaison
    """
    # Configuration du graphique
    fig, ax = plt.subplots(figsize=FIGURE_SIZE)
    
    # Couleurs pour chaque période de retour
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
    
    # Tracer les courbes pour chaque période de retour
    for i, period in enumerate(idf_obj.return_periods):
        durations = idf_obj.columns.astype(float)
        
        # Courbes IDF (données observées/estimées)
        idf_intensities = idf_obj.intensity_estimator[period].values
        ax.plot(durations, idf_intensities, 
                 marker='o', linewidth=2, markersize=8,
                 color=colors[i % len(colors)], linestyle='-',
                 label=f'IDF {period} ans')
        
        # Courbes Montana (modèle ajusté) 
        montana_intensities = idf_obj.montana_estimator[period].values
        ax.plot(durations, montana_intensities, 
                 marker='s', linewidth=2, markersize=6,
                 color=colors[i % len(colors)], linestyle='--', alpha=0.7,
                 label=f'Montana {period} ans')
    
    # Configuration des axes et labels
    ax.set_xlabel('Durée (heures)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Intensité (mm/h)', fontsize=12, fontweight='bold')
    ax.set_title('Comparaison Courbes IDF vs Montana\nIntensité moyenne en fonction de la durée', 
                fontsize=14, fontweight='bold', pad=20)
    
    # Configuration de la grille
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(title='Type et Période de retour', loc='upper right', 
             frameon=True, fancybox=True, ncol=2)
    
    # Amélioration de l'apparence
    ax.tick_params(axis='both', which='major', labelsize=10)
    plt.tight_layout()
    
    return fig