function autoResize(){
    $.fn.autoResize = function(){
      let r = e => {
        e.style.height = '';
        e.style.height = e.scrollHeight + 'px'
      };
      return this.each((i,e) => {
        e.style.overflow = 'hidden';
        r(e);
        $(e).bind('input', e => {
          r(e.target);
        })
      })
    };
    $("#resume").autoResize()
    $("#commentaire-field").autoResize()
    $("#message").autoResize()
}

function customFileUploadButton(){
    const ajoutPDF = document.getElementById('ajout_pdf');
    const ajoutIMG = document.getElementById('ajout_img');
    const fileChosenPDF = document.querySelector(".upload-file-input .ajout_pdf #file-chosen")
    const fileChosenIMG = document.querySelector(".upload-file-input .ajout_img #file-chosen")

    ajoutPDF.addEventListener('change', function(){
      fileChosenPDF.textContent = this.files[0].name
    })

    ajoutIMG.addEventListener('change', function(){
      fileChosenIMG.textContent = this.files[0].name
    })
}

function showCurrentImg(){
    $(".new-img").hide()
    document.getElementById("ajout_img").addEventListener("change", (event)=>{
        var output = document.getElementById('current_img');
        output.src = URL.createObjectURL(event.target.files[0]);
        output.onload = function() {
          URL.revokeObjectURL(output.src)
            $(".new-img").show()
        };
    })
}
$(document).ready(function (){
    autoResize()
    customFileUploadButton()
    showCurrentImg()
})

