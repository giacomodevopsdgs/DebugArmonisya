from rest_framework import serializers

from secops.serializers.Asset.Asset import AssetSerializer


class AssetsSerializer(serializers.Serializer):
    items = AssetSerializer(many=True)
