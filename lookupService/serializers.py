from rest_framework import serializers
from .models import Job


class JobSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Job
        fields = ['id','initiated',
                  'data','mode',
                  'species','node',
                  'model_type','dry_run',
                  'single_fam_mode','mail_address']
