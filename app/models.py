from django.db import models
from django.forms import ValidationError
from django.utils import timezone
from celery.schedules import crontab
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('USAGER', 'Usager'),
        ('AGENT', 'Agent'),
        ('OPJ', 'Officier de Police Judiciaire'),
        ('ADMIN', 'Administrateur'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='USAGER')

    def is_agent(self):
        return self.role == 'AGENT'

    def is_opj(self):
        return self.role == 'OPJ'

    def is_admin(self):
        return self.role == 'ADMIN'

    def is_usager(self):
        return self.role == 'USAGER'
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

# ==========================
# USAGER
# ==========================
class Usager(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    numero_fiscal = models.CharField(max_length=50, unique=True)
    telephone = models.CharField(max_length=15)
    adresse = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()}"

# ==========================
# VEHICULE
# ==========================
class Vehicule(models.Model):
    usager = models.ForeignKey(Usager, on_delete=models.CASCADE, related_name="vehicules")
    plaque_immatriculation = models.CharField(max_length=15, unique=True)
    marque = models.CharField(max_length=50)
    modele = models.CharField(max_length=50)
    annee = models.PositiveIntegerField()

    def __str__(self):
        return self.plaque_immatriculation

# ==========================
# AGENT
# ==========================
class Agent(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    matricule = models.CharField(max_length=20, unique=True)
    fonction = models.CharField(max_length=100)
    zone_affectation = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.matricule})"

# ==========================
# OPJ
# ==========================
class OPJ(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    matricule = models.CharField(max_length=20, unique=True)
    grade = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.grade})"

# ==========================
# TYPE D'INFRACTION
# ==========================
class TypeInfraction(models.Model):
    
    libelle = models.CharField(max_length=255)
    montant_min = models.DecimalField(max_digits=10, decimal_places=2)
    montant_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    article_loi = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.libelle

    def montant_affiche(self):
        if self.montant_max and self.montant_max != self.montant_min:
            return f"{self.montant_min} à {self.montant_max} $"
        return f"{self.montant_min} $"
    
class Bareme(models.Model):
    type_infraction = models.ForeignKey(TypeInfraction, on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    montant = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.type_infraction.libelle} - {self.montant} FC"

# ==========================
# INFRACTION
# ==========================
class Infraction(models.Model):
    bareme = models.ForeignKey(Bareme, on_delete=models.SET_NULL, null=True, blank=True)
    vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE)
    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True)
    plaque = models.CharField(max_length=15, blank=True)  # Pour compatibilité template
    description = models.TextField(blank=True)  # Pour compatibilité template
    date_infraction = models.DateTimeField(default=timezone.now)  # Pour compatibilité template
    lieu = models.CharField(max_length=255)
    image_preuve = models.ImageField(upload_to='preuves/', null=True, blank=True)
    montant_actuel = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    date_limite = models.DateField(null=True, blank=True)
    majore = models.BooleanField(default=False)
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True, null=True)
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('validee', 'Validée par OPJ'),
        ('classee', 'Classée sans suite'),
        ('transmise', 'Transmise au parquet'),
        ('payee', 'Payée'),
        ('conteste', 'Contestée'),
        ('non_payee', 'Non Payée'),
        ('retard', 'En retard'),
    ]
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    date_traitement = models.DateTimeField(null=True, blank=True)
    opj_traitant = models.ForeignKey('OPJ', null=True, blank=True, on_delete=models.SET_NULL, related_name="infractions_traitees")
    stripe_payment_intent_id = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.vehicule.plaque_immatriculation} - {self.bareme.type_infraction.libelle}"

# ==========================
# CONTESTATION
# ==========================
class Contestation(models.Model):
    infraction = models.ForeignKey(Infraction, on_delete=models.CASCADE)
    usager = models.ForeignKey(Usager, on_delete=models.CASCADE)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=[('en attente', 'En attente'), ('acceptée', 'Acceptée'), ('rejetée', 'Rejetée')], default='en attente')
    opj_traitant = models.ForeignKey(OPJ, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Contestation de {self.infraction}"

# ==========================
# PAIEMENT
# ==========================
class Paiement(models.Model):
    infraction = models.OneToOneField(Infraction, on_delete=models.CASCADE)
    date_paiement = models.DateTimeField(auto_now_add=True)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    moyen_paiement = models.CharField(max_length=50, default="manuelle")
    statut = models.CharField(max_length=20, choices=[('en attente', 'En attente'), ('validé', 'Validé')], default='en attente')
    reçu = models.FileField(upload_to='reçus/', null=True, blank=True)

    def __str__(self):
        return f"Paiement de {self.infraction.id}"

# ==========================
# NOTE DE PERCEPTION
# ==========================
from django.core.exceptions import ValidationError

class NotePerception(models.Model):
    paiement = models.OneToOneField(Paiement, on_delete=models.CASCADE)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date_emission = models.DateField(auto_now_add=True)
    date_limite = models.DateField()

    def clean(self):
        if self.date_limite and self.paiement.infraction.date_infraction:
            date_infraction = self.paiement.infraction.date_infraction.date()
            if self.date_limite < date_infraction:
                raise ValidationError("La date limite doit être postérieure à la date de l'infraction.")

    def __str__(self):
        return f"Note de perception {self.id}"


