from django.contrib import admin
from .models import Job, Node, Edge, Family, NodeFamilyRelation
# Register your models here.
admin.site.register(Job)
admin.site.register(Node)
admin.site.register(Edge)
admin.site.register(Family)
admin.site.register(NodeFamilyRelation)