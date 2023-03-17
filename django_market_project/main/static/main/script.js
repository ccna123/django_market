function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
          var cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

// Rating Initialization
    

    var csrftoken = getCookie('csrftoken');
    var itemName = $('input[name="review_item_name"]').val();
    var rating = 0;

    $(document).ready(function () {

      $('input[type="radio"]').click(function (e) { 
         rating = $(this).nextAll(':visible').length;
      });

      $("#sub-btn").click(function (e) { 
        e.preventDefault();
        const review_text = $("#review_area").val();
      $.ajax({
        type: "POST",
        url: "http://localhost:8000/review/" + itemName + "/",
        data: {
          comments: review_text,
          csrfmiddlewaretoken: csrftoken,
          item_name: itemName,
          rating: rating
        },
        dataType: "json",
        success: function (response) {
          $('input[type="radio"]').prop('checked', false);
          $("#review_section").html(response.review_part);
          $("#review_area").val('');
        }
      });
    });
        
      });

      
    

   