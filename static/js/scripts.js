$(document).ready(function () {
    $(".add-ingr").click(function () {
        $(".ingredient").append(' <input class="form-control form-control-md shadow" name="ingredients" type="text" placeholder="Ingredient"> ');
    });
     $(".add-step").click(function () {
        $(".step").append(' <<input class="form-control form-control-md shadow" name="steps" type="text" placeholder="Step"> ');
    });
});