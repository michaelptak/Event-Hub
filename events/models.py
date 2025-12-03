from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class FavoriteEvent(models.Model):
    # Link to the user who favorited this event
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_events')

    # Ticketmaster event ID (unique identifier from the API)
    event_id = models.CharField(max_length=255, db_index=True)

    # Event details
    event_name = models.CharField(max_length=500)
    event_url = models.URLField(max_length=1000)
    event_image = models.URLField(max_length=1000)

    # Date and time information
    event_date = models.CharField(max_length=50, null=True)
    event_time = models.CharField(max_length=20, null=True)

    # Venue information
    venue_name = models.CharField(max_length=500)
    venue_address = models.CharField(max_length=500, blank=True, null=True)
    venue_city = models.CharField(max_length=200)
    venue_state = models.CharField(max_length=200)

    # Price information
    price_range = models.CharField(max_length=200, blank=True, null=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        # Ensure a user can't favorite the same event twice
        unique_together = ('user', 'event_id')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.event_name}"
