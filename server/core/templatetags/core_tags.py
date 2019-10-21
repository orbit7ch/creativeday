import json

from django import template
from rest_framework import serializers

register = template.Library()


@register.filter(name='json_dumps')
def json_dumps(obj):
    class Serializer(serializers.ModelSerializer):
        class Meta:
            model = obj.__class__
            exclude = ['path', 'depth', 'numchild', 'draft_title', 'content_type']

    return json.dumps(Serializer(obj).data, indent=4)


@register.filter(name='class_name')
def class_name(obj):
    return str(obj.__class__.__name__)