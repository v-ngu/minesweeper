from rest_framework import serializers
from board_tile.serializers import BoardTileSerializer
from .models import Game
from collections import defaultdict


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = "__all__"


class GameBoardSerializer(serializers.Serializer):
    tiles = BoardTileSerializer(many=True)
    flags_count = serializers.IntegerField()
    difficulty = serializers.CharField()
    game_status = serializers.CharField()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        tiles = representation.pop("tiles", [])

        # Create a map from x to a list of y coordinates using a dictionary comprehension
        tiles_by_row = defaultdict(list)
        for tile in tiles:
            tiles_by_row[tile["row"]].append(tile)

        # Add the map to the representation
        representation["tiles_by_row"] = dict(tiles_by_row)
        return representation
