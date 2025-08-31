#!/usr/bin/env python3
"""
Serveur simple pour gérer les dons de l'ARSC
"""

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import os
from datetime import datetime
import logging

app = Flask(__name__)
CORS(app)

# Configuration
DONATIONS_FILE = 'donations.json'
IBAN = "FR7630004008550001011758824"  # IBAN de l'association
BIC = "BNPAFRPPXXX"  # Code BIC de l'association

# Configuration email (à adapter selon votre fournisseur)
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',  # ou votre serveur SMTP
    'smtp_port': 587,
    'email': 'votre-email@gmail.com',  # Email de l'association
    'password': 'votre-mot-de-passe-app'  # Mot de passe d'application
}

# Configuration de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_donations():
    """Charge les dons existants depuis le fichier JSON"""
    if os.path.exists(DONATIONS_FILE):
        try:
            with open(DONATIONS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Erreur lors du chargement des dons: {e}")
            return []
    return []

def save_donation(donation_data):
    """Sauvegarde un nouveau don"""
    donations = load_donations()
    
    # Ajouter un ID unique et la date
    donation_data['id'] = len(donations) + 1
    donation_data['date'] = datetime.now().isoformat()
    donation_data['status'] = 'en_attente'
    
    donations.append(donation_data)
    
    try:
        with open(DONATIONS_FILE, 'w', encoding='utf-8') as f:
            json.dump(donations, f, ensure_ascii=False, indent=2)
        logger.info(f"Don sauvegardé: {donation_data['id']}")
        return True
    except Exception as e:
        logger.error(f"Erreur lors de la sauvegarde: {e}")
        return False

def send_confirmation_email(donation_data):
    """Envoie un email de confirmation au donateur"""
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_CONFIG['email']
        msg['To'] = donation_data['email']
        msg['Subject'] = f"Confirmation de votre don - ARSC (Don #{donation_data['id']})"
        
        # Corps de l'email
        body = f"""
        <html>
        <body>
            <h2>Merci pour votre don à l'ARSC !</h2>
            
            <p>Bonjour {donation_data['firstName']} {donation_data['lastName']},</p>
            
            <p>Nous avons bien reçu votre intention de don de <strong>{donation_data['amount']}€</strong> 
            pour soutenir la recherche sur la stimulation cérébrale.</p>
            
            <h3>Détails de votre don :</h3>
            <ul>
                <li><strong>Numéro de don :</strong> #{donation_data['id']}</li>
                <li><strong>Montant :</strong> {donation_data['amount']}€</li>
                <li><strong>Date :</strong> {datetime.now().strftime('%d/%m/%Y à %H:%M')}</li>
            </ul>
            
            <h3>Instructions pour finaliser votre don :</h3>
            <p>Pour finaliser votre don, veuillez effectuer un virement bancaire avec les informations suivantes :</p>
            
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 15px 0;">
                <p><strong>Bénéficiaire :</strong> ARSC - Association de Recherche sur la Stimulation Cérébrale</p>
                <p><strong>IBAN :</strong> {IBAN}</p>
                <p><strong>BIC :</strong> {BIC}</p>
                <p><strong>Référence :</strong> DON{donation_data['id']} - {donation_data['firstName']} {donation_data['lastName']}</p>
            </div>
            
            <h3>Avantages fiscaux :</h3>
            <p>Votre don est déductible à 66% de vos impôts. Un don de {donation_data['amount']}€ 
            ne vous coûte que {(donation_data['amount'] * 0.34):.2f}€ après déduction fiscale.</p>
            
            <p>Une fois le virement effectué, nous vous enverrons un reçu fiscal par email.</p>
            
            <p>Merci de votre générosité !</p>
            
            <p>Cordialement,<br>
            L'équipe de l'ARSC</p>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(body, 'html'))
        
        # Connexion au serveur SMTP
        server = smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'])
        server.starttls()
        server.login(EMAIL_CONFIG['email'], EMAIL_CONFIG['password'])
        
        # Envoi de l'email
        text = msg.as_string()
        server.sendmail(EMAIL_CONFIG['email'], donation_data['email'], text)
        server.quit()
        
        logger.info(f"Email de confirmation envoyé à {donation_data['email']}")
        return True
        
    except Exception as e:
        logger.error(f"Erreur lors de l'envoi de l'email: {e}")
        return False

@app.route('/')
def index():
    """Page d'accueil"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>ARSC - Serveur de Dons</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .container { max-width: 800px; margin: 0 auto; }
            .status { padding: 10px; border-radius: 5px; margin: 10px 0; }
            .success { background-color: #d4edda; color: #155724; }
            .error { background-color: #f8d7da; color: #721c24; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>ARSC - Serveur de Dons</h1>
            <p>Le serveur est opérationnel et prêt à recevoir les dons.</p>
            <p><strong>IBAN de l'association :</strong> {}</p>
            <p><strong>BIC :</strong> {}</p>
        </div>
    </body>
    </html>
    """.format(IBAN, BIC)

@app.route('/api/donations', methods=['POST'])
def create_donation():
    """Endpoint pour créer un nouveau don"""
    try:
        data = request.get_json()
        
        # Validation des données
        required_fields = ['amount', 'firstName', 'lastName', 'email']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'Le champ {field} est requis'}), 400
        
        # Validation du montant
        try:
            amount = float(data['amount'])
            if amount <= 0:
                return jsonify({'error': 'Le montant doit être positif'}), 400
        except ValueError:
            return jsonify({'error': 'Le montant doit être un nombre valide'}), 400
        
        # Sauvegarde du don
        if save_donation(data):
            # Envoi de l'email de confirmation
            send_confirmation_email(data)
            
            return jsonify({
                'success': True,
                'message': 'Don enregistré avec succès',
                'donation_id': data.get('id'),
                'iban': IBAN,
                'bic': BIC
            }), 201
        else:
            return jsonify({'error': 'Erreur lors de la sauvegarde du don'}), 500
            
    except Exception as e:
        logger.error(f"Erreur lors de la création du don: {e}")
        return jsonify({'error': 'Erreur interne du serveur'}), 500

@app.route('/api/donations', methods=['GET'])
def get_donations():
    """Endpoint pour récupérer la liste des dons (admin)"""
    try:
        donations = load_donations()
        return jsonify({
            'donations': donations,
            'total_count': len(donations),
            'total_amount': sum(d['amount'] for d in donations)
        })
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des dons: {e}")
        return jsonify({'error': 'Erreur interne du serveur'}), 500

@app.route('/api/donations/<int:donation_id>', methods=['GET'])
def get_donation(donation_id):
    """Endpoint pour récupérer un don spécifique"""
    try:
        donations = load_donations()
        donation = next((d for d in donations if d['id'] == donation_id), None)
        
        if donation:
            return jsonify(donation)
        else:
            return jsonify({'error': 'Don non trouvé'}), 404
            
    except Exception as e:
        logger.error(f"Erreur lors de la récupération du don {donation_id}: {e}")
        return jsonify({'error': 'Erreur interne du serveur'}), 500

if __name__ == '__main__':
    print("🚀 Démarrage du serveur de dons ARSC...")
    print(f"📧 IBAN: {IBAN}")
    print(f"🏦 BIC: {BIC}")
    print("⚠️  N'oubliez pas de configurer les paramètres email dans le code !")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
