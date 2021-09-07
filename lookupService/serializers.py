from rest_framework import serializers
from .models import Job, Node, Edge


class JobSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Job
        fields = ['id', 'initiated',
                  'data', 'mode',
                  'species', 'node',
                  'model_type', 'dry_run',
                  'single_fam_mode', 'mail_address']


class NodeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Node
        fields = ['id', 'text']


class EdgeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Edge
        fields = ['id', 'from_node', 'to_node']

