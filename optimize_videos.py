#!/usr/bin/env python3
"""
Script pour optimiser automatiquement les balises vidéo dans index.html
"""

import re

def optimize_video_tags():
    # Lire le fichier HTML
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern pour trouver les balises vidéo non optimisées
    pattern = r'<video muted preload="metadata">'
    replacement = '<video muted preload="metadata" loading="lazy" poster="data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 1 1\'%3E%3Crect width=\'1\' height=\'1\' fill=\'%23f0f0f0\'/%3E%3C/svg%3E">'
    
    # Remplacer toutes les occurrences
    optimized_content = re.sub(pattern, replacement, content)
    
    # Écrire le fichier optimisé
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(optimized_content)
    
    print("✅ Optimisation des balises vidéo terminée !")

if __name__ == "__main__":
    optimize_video_tags()
