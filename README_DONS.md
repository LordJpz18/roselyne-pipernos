# Système de Dons ARSC

Ce système permet de collecter des dons pour l'Association de Recherche sur la Stimulation Cérébrale (ARSC) via virement bancaire.

## Fonctionnalités

- ✅ Formulaire de don en 3 étapes
- ✅ Sélection de montants prédéfinis ou personnalisés
- ✅ Collecte des informations du donateur
- ✅ Affichage de l'IBAN pour virement
- ✅ Calcul automatique des avantages fiscaux
- ✅ Envoi d'emails de confirmation
- ✅ Sauvegarde des dons en JSON
- ✅ Interface responsive et moderne

## Installation

### 1. Dépendances Python

```bash
pip install -r requirements.txt
```

### 2. Configuration Email

Modifiez les paramètres email dans `server.py` :

```python
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',  # Votre serveur SMTP
    'smtp_port': 587,
    'email': 'votre-email@gmail.com',  # Email de l'association
    'password': 'votre-mot-de-passe-app'  # Mot de passe d'application
}
```

**Note :** Pour Gmail, utilisez un "mot de passe d'application" et non votre mot de passe principal.

### 3. Configuration IBAN

Modifiez l'IBAN et le BIC de l'association dans `server.py` :

```python
IBAN = "FR76 3000 2005 5000 0000 0000 000"  # IBAN de l'association
BIC = "CRLYFRPP"  # Code BIC de l'association
```

## Utilisation

### 1. Démarrage du serveur

```bash
python server.py
```

Le serveur démarre sur `http://localhost:5000`

### 2. Accès au site

- Site principal : `http://localhost:8000`
- Page de dons : `http://localhost:8000/don.html`

### 3. Test du système

1. Cliquez sur "Faire un don à l'ARSC" depuis le site principal
2. Suivez les 3 étapes du formulaire
3. Confirmez le don
4. Vérifiez la réception de l'email de confirmation

## Structure des fichiers

```
roselyne-pipernos/
├── index.html          # Site principal
├── i.html             # Version alternative
├── don.html           # Page de dons
├── server.py          # Serveur backend
├── requirements.txt   # Dépendances Python
├── donations.json     # Base de données des dons (créé automatiquement)
└── README_DONS.md     # Ce fichier
```

## API Endpoints

### POST /api/donations
Crée un nouveau don

**Corps de la requête :**
```json
{
    "amount": 100,
    "firstName": "Jean",
    "lastName": "Dupont",
    "email": "jean.dupont@email.com",
    "address": "123 Rue de la Paix",
    "postalCode": "75001",
    "city": "Paris",
    "message": "Message optionnel"
}
```

**Réponse :**
```json
{
    "success": true,
    "message": "Don enregistré avec succès",
    "donation_id": 1,
    "iban": "FR76 3000 2005 5000 0000 0000 000",
    "bic": "CRLYFRPP"
}
```

### GET /api/donations
Récupère la liste de tous les dons (admin)

### GET /api/donations/{id}
Récupère un don spécifique

## Sécurité

- ✅ Validation des données côté serveur
- ✅ Protection contre les injections
- ✅ Gestion des erreurs
- ✅ Logs détaillés

## Avantages fiscaux

Les dons sont déductibles à 66% des impôts :
- Don de 100€ = Coût réel de 34€ après déduction
- Don de 500€ = Coût réel de 170€ après déduction

## Personnalisation

### Couleurs
Modifiez les variables CSS dans `don.html` :

```css
:root {
    --primary-color: #2c3e50;
    --secondary-color: #3498db;
    --success-color: #27ae60;
    /* ... */
}
```

### Montants prédéfinis
Modifiez les options dans `don.html` :

```html
<div class="amount-option" data-amount="10">
    <div class="text-lg font-bold">10€</div>
    <div class="text-sm text-gray-600">Don de base</div>
</div>
```

## Dépannage

### Erreur de connexion au serveur
- Vérifiez que le serveur Python est démarré
- Vérifiez le port 5000
- Vérifiez les paramètres CORS

### Erreur d'envoi d'email
- Vérifiez les paramètres SMTP
- Vérifiez le mot de passe d'application
- Vérifiez que l'email de destination est valide

### Erreur de sauvegarde
- Vérifiez les permissions d'écriture
- Vérifiez l'espace disque disponible

## Support

Pour toute question ou problème, contactez l'équipe technique de l'ARSC.
