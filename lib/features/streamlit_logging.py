import logging
from lib.const import PROGRESS_CTN
import streamlit as st


class StreamlitHandler(logging.Handler):
    """Affiche le dernier log dans un container Streamlit unique et dynamique."""
    def __init__(self, container=None):
        super().__init__()
        self.container = container

    def emit(self, record):
        try:
            msg = self.format(record)
            
            # Utiliser le container fourni pour afficher le message
            if self.container:
                # Vider le container et afficher le nouveau message
                self.container.empty()
                with self.container:
                    if record.levelno >= logging.ERROR:
                        st.error(msg)
                    elif record.levelno >= logging.WARNING:
                        st.warning(msg)
                    elif record.levelno >= logging.INFO:
                        st.info(msg)
                    else:
                        st.write(msg)
        except Exception as e:
            # En cas d'erreur, éviter une boucle infinie
            print(f"Erreur dans StreamlitHandler: {e}")

def get_pipeline_logger(name="pipeline", container=None):
    """Retourne un logger configuré avec un container dynamique."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.propagate = False  # <- bloque la remontée vers le root

    # Nettoyer les anciens handlers
    logger.handlers.clear()
    
    # Ajouter le nouveau handler avec le container
    h = StreamlitHandler(container)
    h.setFormatter(logging.Formatter("%(levelname)s — %(message)s"))
    logger.addHandler(h)

    return logger
    