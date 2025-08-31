#!/usr/bin/env python3
"""
Script pour optimiser automatiquement les balises img dans index.html
"""

import re

def optimize_image_tags():
    # Lire le fichier HTML
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern pour trouver les balises img non optimisées (sans loading="lazy")
    pattern = r'<img([^>]*?)(?<!loading="lazy")([^>]*?)>'
    
    def replace_img(match):
        img_content = match.group(0)
        # Si l'image n'a pas déjà loading="lazy", l'ajouter
        if 'loading="lazy"' not in img_content:
            # Insérer loading="lazy" decoding="async" après le premier attribut
            if 'src=' in img_content:
                # Trouver la position après src
                src_pos = img_content.find('src=')
                quote_char = img_content[src_pos + 4]  # " ou '
                end_quote = img_content.find(quote_char, src_pos + 5)
                insert_pos = end_quote + 1
                return img_content[:insert_pos] + ' loading="lazy" decoding="async"' + img_content[insert_pos:]
            else:
                # Si pas de src, ajouter à la fin de la balise
                return img_content.replace('>', ' loading="lazy" decoding="async">')
        return img_content
    
    # Remplacer toutes les occurrences
    optimized_content = re.sub(pattern, replace_img, content)
    
    # Écrire le fichier optimisé
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(optimized_content)
    
    print("✅ Optimisation des balises img terminée !")

if __name__ == "__main__":
    optimize_image_tags()
