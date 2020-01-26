$(document).ready(function() {
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function(e) {
                /*var image = $("#image");
                image.src = e.target.result;
                console.log(image.src)*/
                $('#image').attr('src', e.target.result);
            }
            reader.readAsDataURL(input.files[0])
        }
    }

    

    $(".custom-file-input").on("change", function() {
        //console.log(this)
        var fileName = $(this).val().split("\\").pop();
        $(this).siblings(".custom-file-label").addClass("selected").html(fileName);
        readURL(this);
        $('#upload-file').append('<img id="image" class="img-fluid img-thumbnail mt-3" >');
        
        
        /*$('#upload-file-btn').click(function() {
            $(this).siblings('.custom-file-label').removeClass("selected").html(fileName);    
        })*/
    })



    $('#upload-file-btn').click(function() {
        

        var form_data = new FormData($('#upload-file')[0]);
        var filename = $('.custom-file-label');
        filename.html('');

        var imagedissappear = $('#image');
        imagedissappear.remove();
        console.log(imagedissappear);
       
        //var form_data = new FormData()
        //form_data.append('file', $('input[type=file]')[0].files[0]);
        //var info = $('#info');
        //info.hide();
        $('#loadingmessage').show();
        
        $.ajax({
            type: 'POST',
            url: '/uploadajax',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            success: function(data) {
                console.log(data);
                console.log(data.date_of_birth);
                /*var dob = (data.date_of_birth.split(' '));
                data.date_of_birth = `${dob[0]} ${dob[1]} ${dob[2]} ${dob[3]}`;
                var doe = (data.expiration_date.split(' '));
                data.expiration_date = `${doe[0]} ${doe[1]} ${doe[2]} ${doe[3]}`;*/
                // Names
                var names = document.createElement("LI");
                var namesTextNode = document.createTextNode("Names: " + data.names);
                names.appendChild(namesTextNode);
                names.className = "list-group-item";
                document.getElementById("dataList").appendChild(names);
                // Surname
                var surname = document.createElement("LI");
                var surnameTextNode = document.createTextNode("Surname: " + data.surname);
                surname.appendChild(surnameTextNode);
                surname.className = "list-group-item";
                document.getElementById("dataList").appendChild(surname);
                // Gender
                var gender = document.createElement("LI");
                var genderTextNode = document.createTextNode("Gender: " + data.sex);
                gender.appendChild(genderTextNode);
                gender.className = "list-group-item";
                document.getElementById("dataList").appendChild(gender);
                // Passport Number
                var number = document.createElement("LI");
                var numberTextNode = document.createTextNode("Passport Number: " + data.number);
                number.appendChild(numberTextNode);
                number.className = "list-group-item";
                document.getElementById("dataList").appendChild(number);
                // Country Output
                var country = document.createElement("LI");
                var countryTextNode = document.createTextNode("Country: " + data.country);
                country.appendChild(countryTextNode);
                country.className = "list-group-item";
                document.getElementById("dataList").appendChild(country);
                // Nationality Output
                var nationality = document.createElement("LI");
                var nationalityTextNode = document.createTextNode("Nationality: " + data.nationality);
                nationality.appendChild(nationalityTextNode);
                nationality.className = "list-group-item";
                document.getElementById("dataList").appendChild(nationality);
                // Date of Birth Output
                var dateofbirth = document.createElement("LI");
                var dateofbirthTextNode = document.createTextNode("Date of Birth: " + data.date_of_birth);
                dateofbirth.appendChild(dateofbirthTextNode);
                dateofbirth.className = "list-group-item";
                document.getElementById("dataList").appendChild(dateofbirth);
                // Expiry date
                var expirydate = document.createElement("LI");
                var expirydateTextNode = document.createTextNode("Expiry Date: " + data.expiration_date);
                expirydate.appendChild(expirydateTextNode);
                expirydate.className = "list-group-item";
                document.getElementById("dataList").appendChild(expirydate);
                $('#loadingmessage').hide();
                
                // $('#upload-file').trigger("reset");
                $(".custom-file-input").on("change", function() {
                    location.reload();
                })
                
                //alert(data.names)
            }
        }).done(function(data){
            //$("upload-file").reset();
            //console.log(data.country + data.names);
            
            
        })
    })
})
//console.log($)
