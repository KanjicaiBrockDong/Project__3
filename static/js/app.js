const tl = gsap.timeline({ defaults: { ease: "power1.out" } });

tl.to(".text", { y: "0%", duration: 1, stagger: 0.25 });
tl.to(".slider", { y: "-100%", duration: 1.5, delay: 0.5 });
tl.to(".intro", { y: "-100%", duration: 1 }, "-=1");
tl.fromTo("nav", { opacity: 0 }, { opacity: 1, duration: 1 });
tl.fromTo(".big-text", { opacity: 0 }, { opacity: 1, duration: 1 }, "-=1");

function init() {
    console.log("in load")
}


// Add the image
$(".imgAdd").click(function () {
    $(this).closest(".row").find('.imgAdd').before(
        '<div class="col-lg-3 col-sm-3 imgUp">\
                      <figcaption class="figure-caption" id="image-name" placeholder="Image name here.">Upload to Predict</figcaption>\
                      <br>\
                      <div class="form-group"> \
                      <div class="imagePreview"></div> \
                      <div class="upload-options"> \
                      <label><i class="fas fa-upload"></i><input type="file" name="file" class="image-upload" accept="image/*;capture=camera" /></label> \
                      </div></div> \
                      <i class="fa fa-times del"></i></div>');
});


// $("#how").click(function () {
//     document.getElementById('how').scrollIntoView();
// });



// $(document).on("click", "i.del", function () {
//     $(this).parent().remove();
// });


//Upload the image and predict
$(function () {
    $(document).on("change", ".image-upload", function () {
        var uploadFile = $(this);
        var files = !!this.files ? this.files : [];
        if (!files.length || !window.FileReader) return; 

        var caption = $("#image-name"); 
        caption.text("Predicting ... ");
        console.log(caption.text())

        if (/^image/.test(files[0].type)) { // only image file
            var reader = new FileReader(); // instance of the FileReader
            reader.readAsDataURL(files[0]); // read the local file

            reader.onloadend = function () { 
                uploadFile.closest(".imgUp").find('.imagePreview').css("background-image", "url(" + this.result + "); height: 225px; width: 225px;");
                var form_data = new FormData();
                $.each($(".image-upload"), function (i, obj) {
                    $.each(obj.files, function (j, file) {
                        form_data.append('file', file); 
                        console.log(file);
                    });
                });
                var request = new XMLHttpRequest();
                request.open("POST", "/predict");
                request.onload = function(event) {
                    if (request.status == 200) {
                      var result = JSON.parse(this.responseText)
                      //caption.html(result.predictions[0][1]);
                      caption.html(result.prediction);
                    } else {
                     caption.html("Error " + request.status + " occurred when trying to upload your file.<br \/>");
                    }
                  };
                request.send(form_data);
            }
        }
    },
    );
}

);
