from django.db import models
from django.utils import timezone
import uuid
# Create your models here.


def boolean_default():
    return False


def species_default():
    now = timezone.now().strftime('%H:%M:%S')
    return 'job@' + now


def status_default():
    return 'queued'


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
    STATUSES = [
        ('queued', 'Queued'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('halted','Halted')
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField(choices=STATUSES, max_length=15, default=status_default)
    hash = models.CharField(max_length=168, blank=True)
    initiated = models.DateTimeField(auto_now_add=True)
    data = models.CharField(max_length=10000)
    mode = models.CharField(choices=MODE_OPTIONS, max_length=10)
    species = models.CharField(blank=True, max_length=60, default=species_default)
    node = models.CharField(max_length=100, blank=True)
    model_type = models.CharField(choices=MODEL_TYPES, max_length=15)
    single_node = models.BooleanField(default=boolean_default)
    single_fam_mode = models.BooleanField(default=boolean_default)
    family = models.CharField(blank=True, max_length=18)
    mail_address = models.CharField(blank=True, max_length=100)


class Node(models.Model):
    id = models.CharField(primary_key=True, max_length=168)
    text = models.CharField(max_length=168)


class Edge(models.Model):
    id = models.CharField(primary_key=True, max_length=332)
    from_node = models.CharField(max_length=168)
    to_node = models.CharField(max_length=168)


class Family(models.Model):
    name = models.CharField(primary_key=True, max_length=68)
    proto = models.BooleanField(default=boolean_default)
    deutero = models.BooleanField(default=boolean_default)


class NodeFamilyRelation(models.Model):
    node = models.CharField(max_length=168)
    family = models.CharField(max_length=68)