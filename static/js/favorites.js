// CSRF token helper function from Django docs
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + "=")) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Handle "Add to Favorites" button clicks
$('.favorite-btn').click(function() {
  const button = $(this);

  // Don't do anything if already favorited
  if (button.prop('disabled')) {
    return;
  }

  // Get event data from button's data attributes
  const eventData = {
    event_id: button.data('event-id'),
    name: button.data('event-name'),
    url: button.data('event-url'),
    image: button.data('event-image'),
    datetime: button.data('event-datetime'),
    venue_name: button.data('venue-name'),
    venue_address: button.data('venue-address'),
    venue_city: button.data('venue-city'),
    venue_state: button.data('venue-state'),
    price_range: button.data('price-range')
  };

  // Send AJAX request
  $.ajax({
    url: '/favorites/add/',
    type: 'POST',
    dataType: 'json',
    data: JSON.stringify({payload: eventData}),
    headers: {
      'X-Requested-With': 'XMLHttpRequest',
      'X-CSRFToken': getCookie('csrftoken'),
    },
    success: function(data) {
      if (data.status === 'success' || data.status === 'already_exists') {
        // Update button to show favorited state
        button.removeClass('btn-outline-secondary')
              .addClass('btn-success')
              .prop('disabled', true)
              .html('<i class="bi bi-check-circle"></i> Favorited');
      }
    },
    error: function(error) {
      console.error('Error adding to favorites:', error);
      alert('Failed to add to favorites. Please try again.');
    }
  });
});
