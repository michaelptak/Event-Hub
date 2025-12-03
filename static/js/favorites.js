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
    formatted_date: button.data('formatted-date'),
    formatted_time: button.data('formatted-time'),
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

// Handle "Remove from Favorites" button clicks
let eventToRemove = null;

$('.remove-favorite-btn').click(function() {
  const button = $(this);

  // Don't do anything if already disabled
  if (button.prop('disabled')) {
    return;
  }

  eventToRemove = button;

  // Show the Bootstrap modal
  $('#confirmDeleteModal').modal('show');
});

// Handle the actual deletion when user confirms
$('#confirmDeleteBtn').click(function() {
  if (!eventToRemove) return;

  const button = eventToRemove;

  // Get event data from button's data attributes
  const buttonData = {
    event_id: button.data('event-id'),
  };

  // Send AJAX request
  $.ajax({
    url: '/favorites/remove/',
    type: 'POST',
    dataType: 'json',
    data: JSON.stringify({payload: buttonData}),
    headers: {
      'X-Requested-With': 'XMLHttpRequest',
      'X-CSRFToken': getCookie('csrftoken'),
    },
    success: function(data) {
      if (data.status === 'success') {
        const card = button.closest('.card');

        $('#confirmDeleteModal').modal('hide');

        card.fadeOut(300, function() {
          location.reload();
        });
      }
    },
    error: function(error) {
      console.error('Error removing from favorites:', error);
      $('#confirmDeleteModal').modal('hide');
      alert('Failed to remove from favorites. Please try again.');
    }
  });

  eventToRemove = null;
});

// Handle "Save Notes" button clicks
$('.save-notes-btn').click(function() {
  const button = $(this);
  const eventId = button.data('event-id');
  const notesField = $(`#notes-${eventId}`);
  const notes = notesField.val();

  // Disable button while saving
  button.prop('disabled', true).html('<i class="bi bi-hourglass-split me-1"></i>Saving...');

  // Send AJAX request
  $.ajax({
    url: '/favorites/update-notes/',
    type: 'POST',
    dataType: 'json',
    data: JSON.stringify({
      event_id: eventId,
      notes: notes
    }),
    headers: {
      'X-Requested-With': 'XMLHttpRequest',
      'X-CSRFToken': getCookie('csrftoken'),
    },
    success: function(data) {
      if (data.status === 'success') {
        // Update button to show success state
        button.removeClass('btn-success')
              .addClass('btn-outline-success')
              .html('<i class="bi bi-check-circle me-1"></i>Saved!');

        // Reset button after 2 seconds
        setTimeout(function() {
          button.removeClass('btn-outline-success')
                .addClass('btn-success')
                .html('<i class="bi bi-check-lg me-1"></i>Save Notes')
                .prop('disabled', false);
        }, 2000);
      }
    },
    error: function(error) {
      console.error('Error saving notes:', error);
      button.removeClass('btn-success')
            .addClass('btn-danger')
            .html('<i class="bi bi-x-circle me-1"></i>Failed')
            .prop('disabled', false);

      // Reset button after 2 seconds
      setTimeout(function() {
        button.removeClass('btn-danger')
              .addClass('btn-success')
              .html('<i class="bi bi-check-lg me-1"></i>Save Notes');
      }, 2000);
    }
  });
});
