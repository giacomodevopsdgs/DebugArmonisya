from rest_framework import serializers

from secops.serializers.Permission.Permission import PermissionSerializer


class PermissionsSerializer(serializers.Serializer):
    items = PermissionSerializer(many=True)
