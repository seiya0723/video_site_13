from rest_framework import serializers

from .models import CustomUser,FollowUser,BlockUser

class FollowUserSerializer(serializers.ModelSerializer):

    class Meta:
        model  = FollowUser
        fields =[ "from_user","to_user" ]



class BlockUserSerializer(serializers.ModelSerializer):

    class Meta:
        model  = BlockUser
        fields =[ "from_user","to_user" ]


class IconSerializer(serializers.ModelSerializer):

    class Meta:
        model  = CustomUser
        fields = ["usericon",]
