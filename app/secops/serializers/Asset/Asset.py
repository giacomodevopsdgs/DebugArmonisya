from rest_framework import serializers


class AssetSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    technology = serializers.CharField(max_length=32, required=True)
    fqdn = serializers.CharField(max_length=255, required=True)
    protocol = serializers.CharField(max_length=16, required=False)
    port = serializers.IntegerField(required=False)
    path = serializers.CharField(max_length=255, required=False)
    tlsverify = serializers.BooleanField(required=False)
    baseurl = serializers.CharField(max_length=255, required=False)
    account = serializers.CharField(max_length=255, required=False, allow_blank=True)
    datacenter = serializers.CharField(max_length=255, required=False, allow_blank=True)
    environment = serializers.CharField(max_length=255, required=True)
    position = serializers.CharField(max_length=255, required=False, allow_blank=True)
    username = serializers.CharField(max_length=64, required=False)
    password = serializers.CharField(max_length=64, required=False)
    repokey = serializers.CharField(max_length=4096, required=False, allow_blank=True)
    userkey = serializers.CharField(max_length=4096, required=False, allow_blank=True)
    certificate_authority_data = serializers.CharField(max_length=4096, required=False, allow_blank=True)
    client_certificate_data = serializers.CharField(max_length=4096, required=False, allow_blank=True)
    client_key_data = serializers.CharField(max_length=4096, required=False, allow_blank=True)
