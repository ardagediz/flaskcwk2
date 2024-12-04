$(document).ready(function () {
    var csrf_token = $('meta[name=csrf-token]').attr('content');

    $.ajaxSetup({
        beforeSend: function (xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrf_token);
        }
    });

    $(".like-product").click(function () {
        const productId = $(this).data("id");
        const likeButton = $(this);
        const likeCount = likeButton.closest('.card-body').find(".like-count");

        console.log("Product ID:", productId);
        console.log("Like Button:", likeButton);
        console.log("Like Count Element:", likeCount);

        $.ajax({
            url: "/like_product",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({ product_id: productId }),
            success: function (response) {
                console.log("AJAX Success Response:", response);
                likeCount.text(response.likes);
                console.log("Updated Like Count:", likeCount.text());
            },
            error: function (response) {
                console.log("AJAX Error Response:", response.responseJSON.message);
            }
        });
    });
});