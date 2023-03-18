function star_rating(row, avg_rating){

    var stars = row.querySelectorAll(".bi-star-fill");
    starArray = Array.from(stars).reverse();

    starArray.forEach((element, index) => {
        if (index < avg_rating) {
                
            element.classList.add("filled");
        }else{
            element.classList.remove("filled");
                
        }
    });
};

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

  var csrftoken = getCookie('csrftoken');

$(document).ready(function () {
    $("#tt").tooltip({
        hide:true,
        disable:true
    });

    $(".card").each(function(){
      var rating = $(this).find(".avg_rating").val();
      star_rating(this, rating);
    });

    $(".add_inventory_btn").click(function (e) { 
        e.preventDefault();
        const item_name = $(this).val();
        const base_url = window.location.href.split("/").slice(0,3).join("/");
        const quantity = document.querySelector("#quantity").value;

        $.ajax({
            type: "POST",
            url: base_url+ "/" + `add_inventory/${item_name}` + "/",
            data: {
                item_name:item_name,
                quantity:quantity,
                csrfmiddlewaretoken: csrftoken
            },
            dataType: "json",
            success: function (response) {

                $("#tt").attr("title", "Add Successfully");
                $("#tt").tooltip("dispose").tooltip("show");
                setTimeout(() => {
                    $("#tt").tooltip("disable").tooltip("hide");
                }, 1500);
                
                
            },
            error: function(xhr, textStatus, errorThrow) {
                console.log("Error: " + errorThrow);
            }   
        });
    }); 
 
});

