from rest_framework import serializers
from base.models import Customer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id','firstname','lastname','email','password','phone']
        extra_kwargs = {
            "password":{"write_only":True}
        }
    def create(self,validated_data):
        pwd = validated_data.pop("password",None)
        ins = self.Meta.model(**validated_data)
        if pwd is not None:
            ins.set_password(pwd)
        ins.save()
        return ins