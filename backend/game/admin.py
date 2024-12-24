from django.contrib import admin
from .models import Game


class GameAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "difficulty")


admin.site.register(Game, GameAdmin)
