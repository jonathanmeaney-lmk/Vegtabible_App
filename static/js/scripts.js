$(document).ready(function () {

    // Add ingredient input on add/edit recipe form:
    $(".add-ingr").click(function () {
        $(".ingredient").append(' <input class="form-control form-control-md shadow mb-1 ingredient-input" name="ingredients" type="text" minlength="3" aria-label="step input" placeholder="Ingredient"> ');
    });

    // Add step input on add/edit recipe form:
    $(".add-step").click(function () {
        $(".step").append(' <input class="form-control form-control-md shadow mb-1 step-input" name="steps" type="text" minlength="3" aria-label="step input" placeholder="Step"> ');
    });
 
    // Remove last ingredient input added on add/edit recipe form:
    $(".remove-ingr").click(function () {
        $(".ingredient-input").last().remove();
    });

    // Remove last step input on added add/edit recipe form:
    $(".remove-step").click(function () {
        $(".step-input").last().remove();
    });

    // Show confirm (yes/no) delete buttons when delete recipe button is pressed:
    $(".delete-btn").click(function() {
        $(this).next().show();
    });

    // Hide confirm (yes/no) delete buttons when "No" button is pressed:
    $(".cancel-delete-btn").click(function() {
        $(this).parent().hide();
    });
        
});