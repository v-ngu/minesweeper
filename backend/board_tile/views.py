from rest_framework import viewsets, status
from board_tile.services import BoardTileService
from .models import BoardTile
from .serializers import BoardTileSerializer, UpdateStateSerializer
from rest_framework.response import Response
from rest_framework.decorators import action


class BoardTileView(viewsets.ModelViewSet):
    serializer_class = BoardTileSerializer
    queryset = BoardTile.objects.all()

    @action(detail=False, methods=["patch"], url_path="update-state")
    def update_state(self, request):
        serializer = UpdateStateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data: dict = (
            serializer.validated_data
            if isinstance(serializer.validated_data, dict)
            else {}
        )
        game_id = validated_data["game_id"]
        row = validated_data["row"]
        column = validated_data["column"]
        new_state = validated_data["state"]
        tile = self.queryset.filter(game_id=game_id, row=row, column=column).first()

        if not tile:
            return Response(
                {"error": "Tile not found."}, status=status.HTTP_404_NOT_FOUND
            )

        service = BoardTileService()
        serializer = service.update_tile_state(tile, new_state, game_id)
        return Response(serializer.data, status=status.HTTP_200_OK)
