from django.contrib import admin
from .models import Team, Post

class TeamAdmin(admin.ModelAdmin):
    list_display = ('team_id', 'team_name', 'creator')
    filter_horizontal = ('members',)

class PostAdmin(admin.ModelAdmin):
    list_display = ('post_id', 'team', 'user', 'created_at')

admin.site.register(Team, TeamAdmin)
admin.site.register(Post, PostAdmin)