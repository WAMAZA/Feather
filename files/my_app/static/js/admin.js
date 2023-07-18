function showUsers() {
    var x = document.getElementById("crossUser");
    x.style.display = "block";
    var x = document.getElementById("arrowUser");
    x.style.display = "none";
    var x = document.getElementById("crossPublication");
    x.style.display = "none";
    var x = document.getElementById("arrowPublication");
    x.style.display = "block";

    var x = document.getElementById("affichageMain");
    x.style.display = "none";
    var x = document.getElementById("affichagePublication1");
    x.style.display = "none";
    var x = document.getElementById("affichagePublication2");
    x.style.display = "none";

    var x = document.getElementById("affichageUsers1");
    x.style.display = "block";
    var x = document.getElementById("showMoreBtnUser");
    x.style.display = "block";
    var x = document.getElementById("affichageUsers2");
    x.style.display = "none";
}

function showPublications() {
    var x = document.getElementById("crossUser");
    x.style.display = "none";
    var x = document.getElementById("arrowUser");
    x.style.display = "block";
    var x = document.getElementById("arrowPublication");
    x.style.display = "none";
    var x = document.getElementById("crossPublication");
    x.style.display = "block";

    var x = document.getElementById("affichageUsers1");
    x.style.display = "none";
    var x = document.getElementById("affichageUsers2");
    x.style.display = "none";
    var x = document.getElementById("affichageMain");
    x.style.display = "none";

    var x = document.getElementById("affichagePublication1");
    x.style.display = "block";
    var x = document.getElementById("showMoreBtnPublication");
    x.style.display = "block";
    var x = document.getElementById("affichagePublication2");
    x.style.display = "none";
}


function updateStatus(event) {
    var userId = event.target.form.elements.user_id.value;
    var newStatus = event.target.value;

    $.ajax({
        type: "POST",
        url: "/update_user_status",
        data: { user_id: userId, new_status: newStatus },
        success: function(response) {
            console.log(response);
        }
    });
}

function updateGroup(event) {
    var userId = event.target.form.elements.user_id.value;
    var newGroup = event.target.value;

    $.ajax({
        type: "POST",
        url: "/update_user_group",
        data: { user_id: userId, new_group: newGroup },
        success: function(response) {
            console.log(response);
        }
    });
}

function showMorePub() {
    var x = document.getElementById("affichagePublication1");
    x.style.display = "block";
    var x = document.getElementById("affichagePublication2");
    x.style.display = "block";
    var x = document.getElementById("showLessBtnPublication");
    x.style.display = "block";

    var x = document.getElementById("showMoreBtnPublication");
    x.style.display = "none";
}

function showLessPub() {
    var x = document.getElementById("affichagePublication1");
    x.style.display = "block";
    var x = document.getElementById("affichagePublication2");
    x.style.display = "none";
    var x = document.getElementById("showMoreBtnPublication");
    x.style.display = "block";
    var x = document.getElementById("showLessBtnPublication");
    x.style.display = "none";
}

function showMoreUser() {
    var x = document.getElementById("affichageUsers2");
    x.style.display = "block";
    var x = document.getElementById("showMoreBtnUser");
    x.style.display = "none";
    var x = document.getElementById("showLessBtnUser");
    x.style.display = "block";
}

function showLessUser() {
    var x = document.getElementById("affichageUsers2");
    x.style.display = "none";
    var x = document.getElementById("showMoreBtnUser");
    x.style.display = "block";
    var x = document.getElementById("showLessBtnUser");
    x.style.display = "none";
}