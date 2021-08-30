from django.db import models
from django.utils import timezone
import uuid
# Create your models here.


def boolean_default():
    return False


def species_default():
    now = timezone.now().strftime('%H:%M:%S')
    return 'job@' + now


class Job(models.Model):
    MODE_OPTIONS = [
        ('text','Text input'),
        ('file','File upload'),
        ('link','Genome link'),
        ('accNum','Accession number')
    ]
    MODEL_TYPES = [
        ('proto', 'Protostomes'),
        ('deutero', 'Deuterostomes'),
        ('both','Both')
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    initiated = models.DateTimeField(auto_now_add=True)
    data = models.CharField(max_length=10000)
    mode = models.CharField(choices=MODE_OPTIONS, max_length=10)
    species = models.CharField(blank=True, max_length=60, default=species_default)
    node = models.CharField(max_length=100)
    model_type = models.CharField(choices=MODEL_TYPES, max_length=15)
    dry_run = models.BooleanField(default=boolean_default)
    single_fam_mode = models.BooleanField(default=boolean_default)
    mail_address = models.CharField(blank=True, max_length=100)



