from rest_framework import serializers
from api.models import PackageMonitor

class RequestLogSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    username = serializers.CharField()
    didhash = serializers.CharField()
    datetime = serializers.DateTimeField()
    wasgranted = serializers.BooleanField()
    imagebytes = serializers.CharField()
    
    def create(self, validated_data):
        return RequestLog.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username',intance.username)
        instance.didhash = validated_data.get('didhash',instance.didhash)
        instance.datetime = validated_data.get('datetime',instance.datetime)
        instance.wasgranted = validated_data.get('wasgranted',instance.wasgranted)
        instance.imagebytes = validated_data.get('imagebytes',instance.imagebytes)
        instance.save()
        return instance


class PackageMonitorSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    username = serializers.CharField()
    pwhash = serializers.CharField()
    masterpw = serializers.CharField()
    phonenum = serializers.CharField()
    didhash = serializers.CharField()
    pendingrequest = serializers.BooleanField()
    requestgranted = serializers.BooleanField()

    def create(self, validated_data):
        return PackageMonitor.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username',intance.username)
        instance.pwhash = validated_data.get('pwhash',instance.pwhash)
        instance.phonenum = validated_data.get('phonenum',instance.phonenum)
        instance.didhash = validated_data.get('didhash',instance.didhash)
        instance.pendingrequest = validated_data.get('pendingreqeust',instance.pendingrequest)
        instance.requestgranted = validated_data.get('reqeustgranted',instance.pendingrequest)
        instance.save()
        return instance
