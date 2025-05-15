from rest_framework import serializers


class PermissionSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    identity_group_identifier = serializers.CharField(max_length=255, required=True)
    role = serializers.CharField(max_length=64, required=True) # not using composition here, for simpler data structure exposed to consumer.
