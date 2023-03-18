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
    $(".cancel_btn").click(function (e) {
        e.preventDefault();
        const cancel_item_name = $(this).data("item-id");
        const base_url = window.location.href.split("/").slice(0,3).join("/");
        console.log(cancel_item_name);
        const item_element = $(this).closest(".item_card");
        
        $.ajax({
            type: "POST",
            url: base_url+ "/" + `cancel_item/${cancel_item_name}` + "/",
            data: {
                cancel_item_name: cancel_item_name,
                csrfmiddlewaretoken: csrftoken
            },
            dataType: "json",
            success: function (response) {
                item_element.remove();

                $("#tt").attr("title", "Cancel Successfully");
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