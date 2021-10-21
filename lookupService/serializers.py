from rest_framework import serializers
from .models import Job, Node, Edge, Family, NodeFamilyRelation


class StrippedJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        exclude = ['data', 'data_file', 'user_cookie']


class JobSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'


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
