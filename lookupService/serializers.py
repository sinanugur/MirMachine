from rest_framework import serializers
from .models import Job, Node, Edge, Family, NodeFamilyRelation


class JobSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Job
        fields = ['id', 'initiated', 'status',
                  'data', 'hash', 'mode',
                  'species', 'node',
                  'model_type', 'single_node', 'family',
                  'single_fam_mode', 'mail_address']


class NodeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Node
        fields = ['id', 'text']


class EdgeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Edge
        fields = ['id', 'from_node', 'to_node']


class FamilySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Family
        fields = ['name', 'proto', 'deutero']


class NodeFamilyRelationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = NodeFamilyRelation
        fields = ['node', 'family']