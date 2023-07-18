function showForm(){
    $("#fake-btn").click(function (){
        $('#connect_before').show()
    })

    $("#add-comment-btn").click(function (){
        $("#avis-form").fadeIn(200).show();
        $("#add-comment-btn").hide()
    })
}

function hideForm(){
    $("#cancel-btn").click(function (){
        $("#avis-form").hide();
        $("#add-comment-btn").show()
    })
}

function addComment(){
    let url = "http://127.0.0.1:8000/ajout_commentaire/" + window.location.pathname.split("/produit/")[1]
    console.log(url)
    let obligatoire = "Ce champ est obligatoire."
    let taille_min = "Un minimum de 100 caractères s'il vous plaît. Nous acceptons que les commentaires constructifs."

    // validation du formulaire
    $("#avis-form").validate({
        rules: {
            avis_text: {
                required: true,
                minlength: 100
            },
            avis_note: {
                required: false
            }
        },
        messages: {
            avis_text: {
                required: obligatoire,
                minlength: taille_min
            }
        },

        // ajax
        submitHandler : function (){
            $.ajax({
                type: "POST",
                url: url,
                data: $("#avis-form").serialize(),
                success: function (){
                    window.location.reload()
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

$(document).ready(function (){
    $("#avis-form").hide()
    showForm()
    hideForm()
    addComment()
})
