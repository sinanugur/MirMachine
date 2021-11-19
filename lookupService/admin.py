from django.contrib import admin
from .models import Job, Node, Edge, Family, NodeFamilyRelation, Cookie


class JobAdmin(admin.ModelAdmin):
    list_display = ('species', 'mode', 'status')


# Register your models here.
admin.site.register(Job, JobAdmin)
admin.site.register(Node)
admin.site.register(Edge)
admin.site.register(Family)
admin.site.register(NodeFamilyRelation)
admin.site.register(Cookie)