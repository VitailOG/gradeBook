function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function studentId(id) {
    let add = document.querySelector('.create-student');
    add.setAttribute('id', id);

}

function createStudent() {
    let year_entry = document.querySelector('#form-edit #id_year_entry').value;
    let group = document.querySelector('#form-edit #inputGroupSelect01').querySelectorAll('option:checked')[0].value;
    let educational_program = document.querySelector('#form-edit #inputGroupSelect02')
        .querySelectorAll('option:checked')[0].value;
    let id = document.querySelector('.create-student').id;

    let form_education = document.querySelector('#form-edit #inputGroupSelect03')
        .querySelectorAll('option:checked')[0].value;
    console.log(form_education);

    $.ajax({
        method: "POST",
        data: { year_entry: year_entry, group: group, educational_program: educational_program, form_education: form_education },
        headers: { "X-CSRFToken": csrftoken },
        url: `/add-student/${id}`,
        success: function (data) {
            if (data.created_student) {
                $(`#row-${id}`).remove();

                $('#form-edit #id_year_entry').val('');
                $('#form-edit #inputGroupSelect01').val('');
                $('#form-edit #inputGroupSelect02').val('');
                $('#form-edit #inputGroupSelect03').val('');
            }
        }
    })
}

function fun() {
    $('#form-edit #id_year_entry').val('');
    $('#form-edit #inputGroupSelect01').val('');
    $('#form-edit #inputGroupSelect02').val('');
}


