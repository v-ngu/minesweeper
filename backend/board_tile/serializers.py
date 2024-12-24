from rest_framework import serializers
from .models import BoardTile


class BoardTileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardTile
        fields = "__all__"


class UpdateStateSerializer(serializers.Serializer):
    game_id = serializers.IntegerField(required=True)
    row = serializers.IntegerField(required=True)
    column = serializers.IntegerField(required=True)
    state = serializers.CharField(required=True, allow_null=True)


class TileUpdatesSerializer(serializers.Serializer):
    tiles = BoardTileSerializer(many=True)
    flags_count = serializers.IntegerField()
    game_status = serializers.CharField(required=False)
