from rest_framework import serializers
from api.models import User, RequestLog, Device


class RequestLogSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    username = serializers.CharField()
    deviceid = serializers.CharField()
    datetime = serializers.DateTimeField()
    wasgranted = serializers.BooleanField()
    imagebytes = serializers.CharField()

    def create(self, validated_data):
        return RequestLog.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username',instance.username)
        instance.deviceid = validated_data.get('deviceid',instance.deviceid)
        instance.datetime = validated_data.get('datetime',instance.datetime)
        instance.wasgranted = validated_data.get('wasgranted',instance.wasgranted)
        instance.imagebytes = validated_data.get('imagebytes',instance.imagebytes)
        instance.save()
        return instance


class DeviceSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    deviceid = serializers.CharField()
    username = serializers.CharField()
    imagebytes = serializers.CharField()
    pendingrequest = serializers.BooleanField()
    requestgranted = serializers.BooleanField()

    def create(self, validated_data):
        return Device.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username',instance.username)
        instance.deviceid = validated_data.get('deviceid',instance.deviceid)
        instance.pendingrequest = validated_data.get('pendingrequest',instance.pendingrequest)
        instance.requestgranted = validated_data.get('requestgranted',instance.requestgranted)
        instance.imagebytes = validated_data.get('imagebytes',instance.imagebytes)
        instance.save()
        return instance


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    username = serializers.CharField()
    pwhash = serializers.CharField()
    masterpw = serializers.CharField()
    phonenum = serializers.CharField()
    deviceid = serializers.CharField()

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username',instance.username)
        instance.pwhash = validated_data.get('pwhash',instance.pwhash)
        instance.phonenum = validated_data.get('phonenum',instance.phonenum)
        instance.deviceid = validated_data.get('deviceid',instance.didhash)
        instance.save()
        return instance

