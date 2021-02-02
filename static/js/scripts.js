$(document).ready(function () {
    $(".add-ingr").click(function () {
        $(".ingredient").append(' <input class="form-control form-control-md shadow mb-1" name="ingredients" type="text" minlength="3" placeholder="Ingredient"> ');
    });
     $(".add-step").click(function () {
        $(".step").append(' <input class="form-control form-control-md shadow mb-1" name="steps" type="text" minlength="3" placeholder="Step"> ');
    });
});