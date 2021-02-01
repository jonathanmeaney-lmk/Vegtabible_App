$(document).ready(function () {
    $(".add-ingr").click(function () {
        $(".ingredient").append(' <input class="form-control form-control-md shadow" name="ingredient" type="text" placeholder="Ingredient"> ');
    });
     $(".add-step").click(function () {
        $(".step").append(' <input class="form-control form-control-md shadow" name="step" type="text" placeholder="Step"> ');
    });
});