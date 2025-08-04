# 🚦 Système de Gestion des Infractions Routières et d’Identification des Plaques en RDC

> Une solution numérique pour le traitement des infractions routières, l’identification automatique des plaques d’immatriculation et le suivi des paiements en République Démocratique du Congo.

## 📌 Objectif du projet

Ce projet vise à **digitaliser la gestion des contraventions routières** en RDC, en fournissant une plateforme web permettant :

- L’enregistrement des infractions par les agents de la PCR
- L’identification des propriétaires à partir des plaques d’immatriculation
- Le suivi des paiements d’amendes
- La génération automatique de QR codes et de notes de perception
- La contestation par les usagers
- L’automatisation des sanctions en cas de non-paiement

## 🧱 Fonctionnalités principales

- 📄 **Enregistrement d'infractions** avec preuve (image) par les agents
- 🚘 **Identification du véhicule** via la plaque et le numéro fiscal unique
- 🧑‍⚖️ **Traitement judiciaire** par l’OPJ : validation, transmission au parquet, classement
- 💳 **Paiement des amendes** par banque ou mobile money
- ⏰ **Relance automatique** après délai dépassé, avec majoration
- 📧 **Envoi de QR Code** par email contenant les détails de l’amende
- 📝 **Contestation** par l’usager avec gestion des réponses OPJ
- 📊 **Tableau de bord administratif** avec statistiques

## 🧰 Stack technique

| Côté | Technologie |
|------|-------------|
| Backend | Python, Django, Django REST Framework |
| Frontend | HTML, CSS, Bootstrap (ou React à venir) |
| Base de données | MySQL |
| Authentification | JWT |
| Emails | SMTP (SendGrid ou Mailtrap pour dev) |
| Tâches asynchrones | Celery + Redis |
| Conteneurisation | Docker |
| Déploiement | Kubernetes (en cours) |

## 🗃️ Modèle de données

- **Usager**
- **Véhicule** (lié à un usager)
- **Infraction** (lieu, date, agent, preuve, type)
- **Type d’infraction** (avec montant ou fourchette)
- **Agent PCR**
- **OPJ**
- **Paiement**
- **Note de perception**
- **Contestation**

## 📷 Exemple de flux de travail

1. L’agent saisit une infraction sur le terrain (plaque, image, lieu…)
2. Le système génère un QR Code et envoie un email à l’usager
3. L’usager visualise ses infractions en ligne
4. Il peut payer via banque/mobile ou contester
5. L’OPJ reçoit les demandes et les traite
6. Si le délai est dépassé sans paiement → majoration automatique

## ⚙️ Installation (en local)

```bash
git clone https://github.com/Marus253/infractions-routieres.git
cd infractions-routieres
cp .env.example .env
docker-compose up --build
