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

$(document).ready(function () {
    $(".card").each(function(){
      var rating = $(this).find(".avg_rating").val();
      star_rating(this, rating);
    });
 
});

