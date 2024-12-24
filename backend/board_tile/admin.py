from django.contrib import admin

from .models import BoardTile


class BoardTileAdmin(admin.ModelAdmin):
    list_display = ("game", "row", "column", "value", "state")


admin.site.register(BoardTile, BoardTileAdmin)
