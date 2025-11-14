$('#search-button').click(function () {
  // Default to ensure buttons are hidden
  $('#city-empty-alert').addClass('d-none');
  $('#genre-empty-alert').addClass('d-none');

  // Get input values
  let cityValue = $('#cityInput').val().trim()
  let genreValue = $('#classificationInput').val().trim()

  // Check if fields are empty, if show alerts
  if (cityValue === '') {
    $('#city-empty-alert').removeClass('d-none');
  }

  if (genreValue === '') {
    $('#genre-empty-alert').removeClass('d-none');
  }

  // If both fields have values, proceed with search
  if (cityValue !== '' && genreValue !== '') {
    console.log('Search for:', genreValue, 'in', cityValue);
    $.ajax({
      type: "GET",
      url: "/api/search-events/",  // Django backend endpoint
      data: {
        classificationName: genreValue,
        city: cityValue
      },
      dataType: "json",
      success: function (json) {
        console.log("API Response:", json);
        //Clear div before adding data
        $('#results').empty();

        // Check if events were found
        if (json._embedded && json._embedded.events) {
          const eventCount = json._embedded.events.length;
          // console.log("Number of events found:", json._embedded.events.length);

          $('#results').removeClass('d-none');
          $('#results').text(`${eventCount} events found`);


          $.each(json._embedded.events, function (i, event) {
            const eventName = event.name;
            const eventImage = event.images[0].url;
            const eventDateTime = event.dates.start.dateTime;
            const startDate = new Date(eventDateTime)
            const formattedDate = startDate.toDateString();
            const formattedTime = startDate.toLocaleTimeString('en-US');
            // const eventTime = event.dates.start.localTime;
            const eventUrl = event.url;
            const eventVenue = event._embedded.venues[0].name;
            const eventVenueCity = event._embedded.venues[0].city.name;
            const eventVenueState = event._embedded.venues[0].state.name;
            const eventVenueAddress = event._embedded.venues[0].address.line1;

            $('#results').append('' +
              '<div class="card mb-3">' +
              '  <div class="row g-0 align-items-center">' +
              '    <div class="col-sm-4">' +
              `      <img class="card-img rounded p-2" src="${eventImage}" alt="${eventName}">` +
              '    </div>' +
              '    <div class="col-sm-8">' +
              '      <div class="card-body">' +
              '        <div class="row">' +
              '          <div class="col-8">' +
              `            <h3 class="card-title mb-4">${eventName}</h3>` +
              `            <h5 class="card-text text-secondary fw-bold mb-1"><i class="bi bi-geo-alt"></i> ${eventVenue}</h5>` +
              `            <p class="card-text text-secondary mb-1">${eventVenueAddress}</p>` +
              `            <p class="card-text text-secondary mb-1">${eventVenueCity}, ${eventVenueState}</p>` +
              '          </div>' +
              '          <div class="col-4 text-end">' +
              `            <p class="card-text text-primary-emphasis mb-1 fw-bold">${formattedDate}</p>` +
              `            <p class="card-text text-primary-emphasis mb-3">${formattedTime}</p>` +
              `            <a href="${eventUrl}" target="_blank" class="btn btn-outline-primary"><i class="bi bi-ticket-perforated"></i> Find tickets</a>` +
              '          </div>' +
              '        </div>' +
              '      </div>' +
              '    </div>' +
              '  </div>' +
              '</div>');
          })

        } else {
          console.log("No events found");
          $('#results').append('<p>Sorry... No results were found for the entered search term and city.</p>');
        }
      },
      error: function (xhr, status, err) {
        console.error("API Error:", status, err);
        console.error("Response:", xhr.responseText);
      }
    })
  }
})
