"""
Système d'animation et d'icônes de chargement pour l'interface IDF
"""
import streamlit as st
import time
import threading
import logging
from typing import Dict, Any


class LoadingAnimator:
    """Gestionnaire d'animations de chargement"""
    
    # Séquences d'animation
    SPINNER_FRAMES = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    DOTS_FRAMES = ["⠀", "⠁", "⠃", "⠇", "⠏", "⠟", "⠿", "⡿", "⣿", "⣾", "⣼", "⣸", "⣀"]
    CIRCLE_FRAMES = ["◐", "◓", "◑", "◒"]
    ARROW_FRAMES = ["→", "↘", "↓", "↙", "←", "↖", "↑", "↗"]
    
    @staticmethod
    def get_loading_icon(step: str = "processing") -> str:
        """Retourne une icône de chargement selon l'étape"""
        icons = {
            "upload": "📤",
            "processing": "⚙️",
            "calculating": "🧮",
            "analyzing": "🔍",
            "estimating": "📊",
            "finalizing": "✨",
            "complete": "✅",
            "error": "❌",
            "warning": "⚠️"
        }
        return icons.get(step, "🔄")
    
    @staticmethod
    def get_animated_message(base_message: str, frame_index: int = 0) -> str:
        """Génère un message avec animation"""
        spinner = LoadingAnimator.SPINNER_FRAMES[frame_index % len(LoadingAnimator.SPINNER_FRAMES)]
        return f"{spinner} {base_message}"


class ProgressTracker:
    """Gestionnaire de progression avec animation"""
    
    def __init__(self, container, total_steps: int = 7):
        self.container = container
        self.total_steps = total_steps
        self.current_step = 0
        self.progress_bar = None
        self.status_text = None
    
    def start(self):
        """Initialise la barre de progression"""
        with self.container:
            self.progress_bar = st.progress(0)
            self.status_text = st.empty()
    
    def update(self, message: str, step_type: str = "processing"):
        """Met à jour la progression"""
        if self.progress_bar and self.status_text:
            self.current_step += 1
            progress = min(self.current_step / self.total_steps, 1.0)
            
            # Mise à jour de la barre de progression
            self.progress_bar.progress(progress)
            
            # Icône selon le type d'étape
            icon = LoadingAnimator.get_loading_icon(step_type)
            
            # Message avec animation
            animated_msg = f"{icon} {message}"
            
            # Affichage du statut
            with self.status_text:
                if step_type == "error":
                    st.error(animated_msg)
                elif step_type == "warning":
                    st.warning(animated_msg)
                elif step_type == "complete":
                    st.success(animated_msg)
                else:
                    st.info(animated_msg)
    
    def complete(self, message: str = "Traitement terminé avec succès!"):
        """Termine la progression"""
        if self.progress_bar and self.status_text:
            self.progress_bar.progress(1.0)
            with self.status_text:
                st.success(f"✅ {message}")
    
    def error(self, message: str):
        """Affiche une erreur"""
        if self.status_text:
            with self.status_text:
                st.error(f"❌ {message}")


def create_animated_logger(container):
    """Crée un logger avec animations"""
    progress_tracker = ProgressTracker(container)
    
    class AnimatedStreamlitHandler(logging.Handler):
        def __init__(self):
            super().__init__()
            self.tracker = progress_tracker
            self.step_mapping = {
                "Données chargées": ("complete", "📊 Données chargées"),
                "Calcul des statistiques": ("calculating", "🧮 Calcul statistiques..."),
                "Estimation des lames": ("analyzing", "🔍 Estimation lames..."),
                "Calcul des intensités": ("estimating", "📊 Calcul intensités..."),
                "Calcul des paramètres": ("processing", "⚙️ Paramètres Montana..."),
                "Application de la formule": ("finalizing", "✨ Finalisation..."),
                "Analyse IDF terminée": ("complete", "🎉 Analyse terminée!")
            }
            self.initialized = False
        
        def emit(self, record):
            try:
                if not self.initialized:
                    self.tracker.start()
                    self.initialized = True
                
                msg = record.getMessage()
                
                # Déterminer le type d'étape
                step_type = "processing"
                display_msg = msg
                
                for key, (stype, dmsg) in self.step_mapping.items():
                    if key.lower() in msg.lower():
                        step_type = stype
                        display_msg = dmsg
                        break
                
                # Déterminer le type selon le niveau de log
                if record.levelno >= logging.ERROR:
                    step_type = "error"
                elif record.levelno >= logging.WARNING:
                    step_type = "warning"
                
                self.tracker.update(display_msg, step_type)
                
            except Exception as e:
                print(f"Erreur dans AnimatedStreamlitHandler: {e}")
    
    # Création du logger avec le handler personnalisé
    logger = logging.getLogger("animated_pipeline")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    logger.handlers.clear()
    
    handler = AnimatedStreamlitHandler()
    handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(handler)
    
    return logger
