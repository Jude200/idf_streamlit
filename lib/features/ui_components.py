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
        layout="wide",
        initial_sidebar_state="collapsed")  # Sidebar fermée par défaut

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
        # st.markdown(f"""
        # <div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(16, 185, 129, 0.05)); 
        #             padding: 1rem; border-radius: 8px; margin: 1rem 0; 
        #             border-left: 4px solid #10b981; text-align: center;">
        #     <strong style="color: #065f46;">✅ Fichier uploadé</strong><br>
        #     <span style="color: #047857;">{file_info}</span>
        # </div>
        # """, unsafe_allow_html=True)
    
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
    # ax.loglog()
    # ax.semilogx()
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
    ax.loglog()
    ax.semilogx()
    
    xTicks = idf_obj.windows
    xtlabs = ["{0:.0f}".format(np.rint(x)) + 'h' for x in xTicks]
    
    # Configuration des ticks pour l'axe Y (intensités)
    # Calcul de la plage des intensités pour définir les ticks Y appropriés
    all_intensities = []
    for period in idf_obj.return_periods:
        all_intensities.extend(idf_obj.montana_estimator[period].values)
    
    min_intensity = min(all_intensities)
    max_intensity = max(all_intensities)
    
    # Création de ticks Y logarithmiques appropriés
    yTicks = [1, 2, 5, 10, 20, 50, 100, 200, 500]
    # Filtrer les ticks pour qu'ils soient dans la plage des données
    yTicks = [y for y in yTicks if min_intensity * 0.5 <= y <= max_intensity * 2]
    
    # Labels pour les ticks Y
    ytlabs = ["{0:.0f}".format(y) for y in yTicks]
    
    ax.grid(axis='both', ls='--', lw=0.5)
    
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
    # ax.set_xlabel('Durée (heures)', fontsize=14, fontweight='600', color='#374151')
    # ax.set_ylabel('Intensité (mm/h)', fontsize=14, fontweight='600', color='#374151')
    # ax.set_title('Courbes Montana', 
    #             fontsize=16, fontweight='700', color='#1f2937', pad=20)
    
    # # Grille moderne
    # ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5, color='#d1d5db')
    ax.set(title='Valeurs Intensité Durée fréquence', 
           xticks=xTicks, xticklabels=xtlabs, 
           yticks=yTicks, yticklabels=ytlabs,
           xlabel='Durée de précipitation', 
           ylabel='Intensité de précipitation (mm/h)')
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

def create_cumuls_curve(idf_obj):
    """
    Crée la courbe des cumuls par durée et fréquence avec un style moderne et professionnel.
    
    Args:
        idf_obj: Objet IDF contenant les données calculées
        
    Returns:
        matplotlib.figure.Figure: Figure contenant la courbe des cumuls par durée et fréquence
    """
    # Configuration du graphique avec style moderne
    plt.style.use('default')
    # Activer le rendu LaTeX pour matplotlib
    plt.rcParams['text.usetex'] = False  # Utiliser mathtext au lieu de LaTeX complet
    plt.rcParams['mathtext.default'] = 'regular'
    
    fig, ax = plt.subplots(figsize=FIGURE_SIZE, dpi=100)
    ax.semilogx()
    
    # Configuration des ticks pour les axes
    xTicks = idf_obj.windows
    xtlabs = ["{0:.0f}".format(np.rint(x)) + 'h' for x in xTicks]
    
    ax.grid(axis='both', ls='--', lw=0.5, alpha=0.7)
    
    fig.patch.set_facecolor('white')
    
    # Palette de couleurs moderne et professionnelle
    colors = ['#4f46e5', '#06b6d4', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6']
    
    # Paramètres de Montana
    params = idf_obj.montana_params
    
    # Tracer une courbe pour chaque période de retour
    for i, period in enumerate(idf_obj.return_periods):
        # Calcul des cumuls : regression[tr] * durées
        # regression[tr] = A[tr] * YearMax.columns**(-B[tr])
        a_param = params.loc[period, 'a']  # coefficient a (exposant)
        b_param = params.loc[period, 'b']  # coefficient b (intensité à 1h)
        
        # Calcul de la régression Montana : I = b * t^(-a)
        regression_values = b_param * (idf_obj.columns.astype(float) ** (-a_param))
        
        # Calcul des cumuls : C = I * t (cumul = intensité × durée)
        cumuls = regression_values * idf_obj.columns.astype(float)
        
        # Label avec formule mathématique (syntaxe mathtext)
        label = f'{period} ans : $C_T(D) = {b_param:.2f} \\times D^{{(1 - {a_param:.3f})}}$'
        
        ax.plot(idf_obj.columns.astype(float), cumuls, 
                color=colors[i % len(colors)], linewidth=2.5,
                label=label, alpha=0.9)
    
    # Configuration des axes avec style moderne
    ax.set(title='Cumuls par Durée et Fréquence', 
           xticks=xTicks, xticklabels=xtlabs,
           xlabel='Durée de précipitation', 
           ylabel='Cumul de précipitation (mm)')
    ax.set_axisbelow(True)
    
    # Légende moderne avec formules mathématiques
    legend = ax.legend(title='Temps de retour - Coefficients de Montana', 
                      loc='center left', bbox_to_anchor=(1.05, 0.5),
                      frameon=True, fancybox=True, shadow=True,
                      title_fontsize=11, fontsize=10)
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

def create_distribution_plot(idf_obj):
    """
    Crée un graphique de distribution des ajustements Gumbel pour chaque durée.
    
    Args:
        idf_obj: Objet IDF contenant les données calculées
        
    Returns:
        matplotlib.figure.Figure: Figure contenant les ajustements Gumbel
    """
    import scipy.stats
    
    # Activer le rendu LaTeX pour matplotlib
    plt.rcParams['text.usetex'] = False
    plt.rcParams['mathtext.default'] = 'regular'

    # Configuration des sous-graphiques
    fig, axs = plt.subplots(2, 3, figsize=(16, 10), dpi=100)
    plt.subplots_adjust(left=0.07, right=0.75, bottom=0.07, top=0.9, wspace=0.3, hspace=0.3)
    
    fig.patch.set_facecolor('white')
    objLegend = []
    
    # Parcourir chaque durée
    for k, duration in enumerate(idf_obj.columns):
        i = int(np.floor(k/3))
        j = k % 3
        
        # Récupérer les paramètres Gumbel pour cette durée
        mu = idf_obj.summary.loc[duration, 'mu']
        beta = idf_obj.summary.loc[duration, 'beta']
        
        # Créer la distribution Gumbel (c=0 pour Gumbel dans genextreme)
        g = scipy.stats.genextreme(c=0, loc=mu, scale=beta)
        
        # Données observées triées
        q_obs = idf_obj.df[duration].sort_values().values
        size = q_obs.size
        allranks = np.arange(size) + 1
        probs = allranks / (allranks.size + 1)
        
        # Fonction de répartition théorique
        l = np.arange(0, 1, 0.002)
        q_func = g.ppf(l)
        
        # Calcul des ticks
        xCent = g.ppf(0.99)
        yTicks = [0, 0.2, 0.4, 0.6, 0.8, 0.99]
        
        if xCent > 20.0:
            xTicks = [0, 10*np.round(0.02*xCent, 0), 10*np.round(0.04*xCent, 0), 
                     10*np.round(0.06*xCent, 0), 10*np.round(0.08*xCent, 0), 
                     xCent, 10*np.round(0.12*xCent, 0)]
        else:
            xTicks = [0, 2*np.round(0.1*xCent, 0), 2*np.round(0.2*xCent, 0), 
                     2*np.round(0.3*xCent, 0), 2*np.round(0.4*xCent, 0), 
                     xCent, 2*np.round(0.6*xCent, 0)]
        
        xTicks = np.unique(xTicks)
        xLabels = []
        for n in np.arange(len(xTicks)):
            if xTicks[n] == xCent:
                xLabels.append("{0:.1f}".format(xTicks[n]))
            else:
                xLabels.append("{0:.0f}".format(xTicks[n]))
        
        # Traçage
        id_y99 = 5
        id_xcent = np.where(xTicks == xCent)[0][0] if len(np.where(xTicks == xCent)[0]) > 0 else -1
        
        # Lignes de référence
        axs[i,j].hlines(0.99, 0, xCent, color='black', lw=0.5, ls='--')
        axs[i,j].vlines(xCent, -0.1, 0.99, color='black', lw=0.5, ls='--')
        
        # Points observés
        obj1 = axs[i,j].scatter(q_obs, probs, color='#10b981', edgecolor='black', 
                               s=50, alpha=0.7, label="Observations :\nRépartition empirique")
        
        # Courbe théorique
        obj2, = axs[i,j].plot(q_func, l, color='#4f46e5', lw=2, 
                             label="Ajustement Gumbel :\nFonction de répartition")
        
        # Percentile 99
        obj3 = axs[i,j].scatter(xCent, 0.99, color='#f59e0b', edgecolor='black', 
                               s=80, label="Percentile 99")
        
        # Configuration des axes
        maxX = np.maximum(q_func.max(), q_obs.max()) + 0.2
        axs[i,j].set_xlim(0, maxX)
        axs[i,j].set_ylim(-0.05, 1.1)
        axs[i,j].set_yticks(yTicks)
        
        title = f'Durée = {duration}h'
        yLabel = r"$P(max_{annuel}\leq Value)$"
        axs[i,j].set(title=title, xticks=xTicks, xticklabels=xLabels, 
                    xlabel='Value (mm/h)', ylabel=yLabel)
        
        # Coloration des ticks spéciaux
        plt.setp(axs[i,j].get_yticklabels()[id_y99], color='red')
        if id_xcent >= 0:
            plt.setp(axs[i,j].get_xticklabels()[id_xcent], color='red')
        
        # Garder les objets pour la légende (première itération seulement)
        if k == 0:
            objLegend = [obj1, obj2, obj3]
    
    # Supprimer le dernier sous-graphique (position [1,2])
    axs[1,2].remove()
    
    # Légende et titre général
    fig.legend(handles=objLegend, loc='right', fontsize=12, labelspacing=2.0)
    fig.suptitle('Ajustement Gumbel - Visualisation des valeurs intensité - fréquence\nsur les fonctions de répartition', 
                fontsize=14, fontweight='600')
    
    return fig
