from django.db import models
from django.utils import timezone
import uuid
import os


def boolean_default():
    return False


def species_default():
    now = timezone.now().strftime('%H:%M:%S')
    return 'job@' + now


def status_default():
    return 'queued'


def name_uploaded_file(instance, filename):
    path = 'uploads/'
    # extension doesn't matter, using txt for consistency
    new_name = '{id}.txt'.format(id=str(instance.id))
    return os.path.join(path, new_name)


class Job(models.Model):
    MODE_OPTIONS = [
        ('text','Text input'),
        ('file','File upload'),
        ('accNum','Accession number')
    ]
    MODEL_TYPES = [
        ('proto', 'Protostomes'),
        ('deutero', 'Deuterostomes'),
        ('combined','Combined')
    ]
    STATUSES = [
        ('queued', 'Queued'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('halted', 'Halted')
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_cookie = models.TextField(blank=True)
    status = models.CharField(choices=STATUSES, max_length=15, default=status_default)
    hash = models.CharField(max_length=168, blank=True)
    submitted = models.DateTimeField(auto_now_add=True)
    initiated = models.DateTimeField(blank=True, null=True)
    completed = models.DateTimeField(blank=True, null=True)
    data = models.TextField(blank=True)
    data_file = models.FileField(upload_to=name_uploaded_file, null=True, blank=True)
    mode = models.CharField(choices=MODE_OPTIONS, max_length=10)
    species = models.TextField(default=species_default)
    node = models.CharField(max_length=100, blank=True)
    model_type = models.CharField(choices=MODEL_TYPES, max_length=15)
    single_node = models.BooleanField(default=boolean_default)
    single_fam_mode = models.BooleanField(default=boolean_default)
    family = models.CharField(blank=True, max_length=18)
    mail_address = models.EmailField(max_length=254, blank=True)


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
