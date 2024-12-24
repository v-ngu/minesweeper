from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from board_tile.models import BoardTile, BoardTileState
from .serializers import GameSerializer, GameBoardSerializer
from .models import Game
from board_tile.services import BoardTileService
from django.db import transaction


class GameView(viewsets.ModelViewSet):
    serializer_class = GameSerializer
    queryset = Game.objects.all()

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        with transaction.atomic():
            game = Game.objects.create(**validated_data)
            # Create board and save adjacent mines
            board_service = BoardTileService(validated_data["difficulty"])
            board_service.create_board(game)

        return Response(GameSerializer(game).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["get"], url_path="board")
    def get_game_board(self, request, pk=None):
        game = self.get_object()

        tiles = game.board_tiles.filter(
            state__in=[BoardTileState.REVEALED, BoardTileState.FLAGGED]
        )

        # Update tiles to set value to -1 if flagged
        for tile in tiles:
            BoardTile.handle_value_visibility(tile)

        response_data = {
            "tiles": tiles,
            "flags_count": BoardTile.get_flagged_count(game.id),
            "difficulty": game.difficulty,
            "game_status": game.status,
        }
        return Response(
            GameBoardSerializer(response_data).data, status=status.HTTP_200_OK
        )
