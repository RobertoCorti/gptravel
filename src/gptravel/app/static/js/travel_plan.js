$(document).ready(function() {
  // When the travel itinerary title is clicked
  $('.travel-itinerary-title').click(function() {
    // Toggle the open class on the travel itinerary list
    $(this).next('.travel-itinerary-list').toggleClass('open');
  });
});