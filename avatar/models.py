from django.db import models

# Create your models here.
class Personagem(models.Model):
    id = models.AutoField(primary_key=True)  # Gera automaticamente IDs
    name = models.CharField(max_length=255)
    affiliation = models.TextField(blank=True)
    allies = models.TextField(blank=True)
    enemies = models.TextField(blank=True)