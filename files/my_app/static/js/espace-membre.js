/**
 * This function allows you to show the real submit btn instead of the fake one which is
 * only used to show the real btn
 */
function showRealBtn(){
    $("#fakeBtn").click(function (){
        // clean and show success message or not
        $(".success").empty().show()
        // clean and show error message or not
        $(".ch-info-error").empty().show()

        // hide the fake button and show the real submit button
        $(".submit-btn-div").show()
        $("#cancel-btn").show()

        $("#ch_password_btn").hide()
        $("#fakeBtn").hide()

        // active all input with the class "field-input" except the id one
        $('.field-input:not(#id)').prop("disabled", false);
    })
}

function hideRealBtn(){
    $("#cancel-btn").click(function (){
        // hide the real button and show the fake submit button
        $(".submit-btn-div").hide()
        $("#cancel-btn").hide()

        $("#ch_password_btn").show()
        $("#fakeBtn").show()

        // active all input with the class "field-input" except the id one
        $('.field-input:not(#id)').prop("disabled", true);
    })
}

/**
 * This function allows you to change user info
 */
function changeInfo(){
    let url = "http://127.0.0.1:8000/change_info";
    let obligatoire = "Ce champ est obligatoire."
    let taille_min = "Ce champ doit être de 3 caractères au minimum"

    // validation du formulaire
    $("#ch_info_form").validate({
        rules: {
            id: {
                required: false
            },
            last_name: {
                required: true,
                minlength: 3
            },
            first_name: {
                required: true,
                minlength: 3
            },
            username: {
                required: true,
                minlength: 3
            },
            email: {
                required: true,
                email: true
            },
            birthday: {
                required: true
            }
        },
        messages: {
            last_name: {
                required: obligatoire,
                minlength: taille_min
            },
            first_name: {
                required: obligatoire,
                minlength: taille_min
            },
            username: {
                required: obligatoire,
                minlength: taille_min
            },
            email: {
                required: obligatoire,
                email: "Ceci n'est pas une adresse mail (exemple: adresse@hotmail.com)"
            },
            birthday: {
                required: obligatoire
            }
        },

        // ajax
        submitHandler : function (){
            $.ajax({
                type: "POST",
                url: url,
                data: $("#ch_info_form").serialize(),
                success: function (){
                    // message of success
                    $(".success").text("Changement avec succès !").fadeOut(3000)

                    // In case of username modification, also update the username in the menu
                    $("#navbar-username").text($("#username").val())

                    // hide the real button and show the fake submit button
                    $(".submit-btn-div").hide()
                    $("#fakeBtn").show()
                    $('#cancel-btn').hide()
                    $("#ch_password_btn").show()


                    // disable all input with the class "field-input" except the "id" one
                    $('.field-input:not(#id)').prop("disabled", true);
                },
                error: function (){
                    $(".ch-info-error").text("Nom d'utilisateur ou email déjà utilisé !").fadeOut(3000)
                }
            });
        }
    })

    // Inject our CSRF token into our AJAX request.
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", "{{ form.csrf_token._value() }}")
            }
        }
    })
}

function verifyBeforeDelete(){
    // show the window
    $("#fake-delete-btn").click(function (){
        $(".delete-verification-screen").show()
    })
}

function optionScript(){
    // hide options field (mes likes and mes commentaires)
    $(".mesLikes").hide()
    $(".mesComments").hide()
    $(".deleteAccount").hide()

    const mesLikesBtn = $(".mesLikesbtn")
    const mesCommentsBtn = $(".mesCommentsBtn")
    const deleteAccountBtn = $(".deleteAccountBtn")

    const mesLikesField = $(".mesLikes")
    const mesCommentField = $(".mesComments")
    const deleteAccountField = $(".deleteAccount")

    showOption(mesLikesBtn, mesLikesField)
    showOption(mesCommentsBtn, mesCommentField)
    showOption(deleteAccountBtn,deleteAccountField)
}

function showOption(button, field){
    button.click(function (){
        /* lorsqu'aucun n'est ouvert */
        if (button.hasClass("fa-angle-right")
            && $(".label-field-show").length < 1
            && $(".active-btn").length < 1)
        {
            // cacher le texte de base
            $("#optionText").hide()
            // changer l'icone du bouton
            button.removeClass("fa-angle-right"); button.addClass("fa-xmark")
            // ajout d'une class pour savoir si le btn est actif
            button.addClass("active-btn")
            // afficher la field conrespondant
            field.show()
            // ajout d'une class pour savoir si la field est affichée
            field.addClass("label-field-show")
        } /* lorsqu'un label est ouvert */
        else if (button.hasClass("fa-angle-right")
            && $(".label-field-show").length > 0
            && $(".active-btn").length > 0)
        {
            // cacher le texte de base
            $("#optionText").hide()
            // cacher le l'ancienne field
            $(".label-field-show").hide()
            // changer l'icone de l'ancien bouton
            $(".active-btn").removeClass("fa-xmark"); $(".active-btn").addClass("fa-angle-right")
            // changer l'icone du nouveau bouton
            button.removeClass("fa-angle-right")
            button.addClass("fa-xmark")
            // ajout d'une class pour savoir si le btn est actif
            button.addClass("active-btn")
            // afficher la field
            field.show()
            // ajout d'une class pour savoir si la field est affichée
            field.addClass("label-field-show")
        } else {
            // afficher le message de base
            $("#optionText").show()
            // changer l'icone du bouton
            button.addClass("fa-angle-right") ; button.removeClass("fa-xmark")
            // suppresion d'une class pour savoir si le btn est actif
            button.removeClass("active-btn")
            // cacher la field
            field.hide()
            // suppression d'une class pour savoir si la field est affichée
            field.removeClass("label-field-show")
        }
    })
}

function deleteAccountNo(){
    const noBtn = $(".no-btn")

    noBtn.click(function (){
        $(".label-field-show").hide()
        $("#optionText").show()
        $(".deleteAccountBtn").removeClass("fa-xmark"); $(".deleteAccountBtn").addClass("fa-angle-right");
        $(".deleteAccount").removeClass("label-field-show")
        $(".deleteAccountBtn").removeClass("active-btn")
    })
}

$(document).ready(function (){
    // Hide btn or field by default
    $(".submit-btn-div").hide()
    $("#cancel-btn").hide()
    $(".ch_pass_success").fadeOut(3000)

    // call functions
    showRealBtn()
    hideRealBtn()
    changeInfo()
    verifyBeforeDelete()
    optionScript()
    deleteAccountNo()
})