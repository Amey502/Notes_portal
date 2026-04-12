from django.contrib import admin
from .models import Team, Post, Comment

class TeamAdmin(admin.ModelAdmin):
    list_display = ('team_id', 'team_name', 'creator', 'member_count')
    search_fields = ('team_name', 'creator__username')
    list_filter = ('creator',)
    filter_horizontal = ('members',)
    readonly_fields = ('team_id',)

    def member_count(self, obj):
        return obj.members.count()
    member_count.short_description = "Members"

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ('user', 'text', 'created_at')

class PostAdmin(admin.ModelAdmin):
    list_display = (
    'post_id',
    'team',
    'user',
    'created_at',
    'like_count',
    'has_pdf',
    'has_summary'
    )

    search_fields = (
        'title',
        'content',
        'user__username',
        'team__team_name'
    )

    list_filter = ('team', 'user', 'created_at')
    readonly_fields = ('post_id', 'created_at')
    inlines = [CommentInline]

    def like_count(self, obj):
        return obj.likes.count()
    like_count.short_description = "Likes"

    def has_pdf(self, obj):
        return bool(obj.pdf)
    has_pdf.boolean = True
    has_pdf.short_description = "PDF"

    def has_summary(self, obj):
        return bool(obj.summary)
    has_summary.boolean = True
    has_summary.short_description = "Summary"

class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'created_at', 'short_text')
    search_fields = ('user__username', 'text')
    list_filter = ('created_at', 'user')

    def short_text(self, obj):
        return obj.text[:50]
    short_text.short_description = "Comment"

class PostAdmin(admin.ModelAdmin):
    list_display = ('post_id', 'team', 'user', 'created_at')

admin.site.register(Team, TeamAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)