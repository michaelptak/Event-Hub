from django.contrib import admin

from .models import FavoriteEvent

# Register your models here.
@admin.register(FavoriteEvent)
class FavoriteEventAdmin(admin.ModelAdmin):
    list_display = ('user', 'event_name', 'event_date', 'event_time', 'created_at', 'last_updated')
    list_filter = ('created_at', 'last_updated', 'user')
    search_fields = ('event_name', 'user__username', 'venue_name', 'venue_city')
    readonly_fields = ('created_at', 'last_updated')
    ordering = ('-created_at',)  # Most recent first
