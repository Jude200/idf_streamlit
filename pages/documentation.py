"""
📚 Page Documentation IDF - Standalone
Page dédiée pour la documentation méthodologique des courbes IDF
"""

import sys
import os

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.features.documentation import create_methodology_page

if __name__ == "__main__":
    create_methodology_page()