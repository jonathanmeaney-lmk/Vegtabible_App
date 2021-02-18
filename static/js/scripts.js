$(document).ready(function () {

    $(".add-ingr").click(function () {
        $(".ingredient").append(' <input class="form-control form-control-md shadow mb-1 ingredient-input" name="ingredients" type="text" minlength="3" aria-label="step input" placeholder="Ingredient"> ');
    });

    $(".add-step").click(function () {
        $(".step").append(' <input class="form-control form-control-md shadow mb-1 step-input" name="steps" type="text" minlength="3" aria-label="step input" placeholder="Step"> ');
    });

    $(".remove-ingr").click(function () {
        $(".ingredient-input").last().remove()
    });

     $(".remove-step").click(function () {
        $(".step-input").last().remove()
    });

    $(".delete-btn").click(function() {
        $(this).next().show()
    });

    $(".cancel-delete-btn").click(function() {
        $(this).parent().hide()
    });
        
});