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

function getIdStudent(id) {

    let update = document.querySelector('.update');
    update.setAttribute('id', `${id}`);

    let i1 = document.querySelector(`#date_${id}`).innerText;
    let i3 = document.querySelector(`#educational_program_${id}`).innerText;
    let i2 = document.querySelector(`#group_${id}`).innerText;

    console.log(update);
    console.log(i1);
    console.log(i2);
    console.log(i3);

    let options = document.querySelector('#form-edit #inputGroupSelect01').getElementsByTagName('option');

    for (let i of options) {
        if (i2 === i.innerText) {
            i.selected = true;
        } else {
            i.selected = false;
        }
    }
    let option = document.querySelector('#form-edit #inputGroupSelect02')
        .getElementsByTagName('option');

    for (let i of option) {
        if (i3 === i.innerText) {
            i.selected = true;
        } else {
            i.selected = false;
        }
    }

    document.querySelector('#form-edit #id_year_entry').value = i1;
}

function deleteStudent(id) {
    console.log(id);
    $.ajax({
        method: "POST",
        headers: {"X-CSRFToken": csrftoken},
        url: `http://127.0.0.1:8000/delete-student/${id}`,
        success: function (data) {
            console.log(data)
            if (data.delete) {
                $(`#row_${id}`).remove()
            }
        }
    })
}

function updateStudent() {
    let year_entry = document.querySelector('#form-edit #id_year_entry');
    let group = document.querySelector('#form-edit #inputGroupSelect01').querySelectorAll('option:checked')[0];
    let educational_program = document.querySelector('#form-edit #inputGroupSelect02')
        .querySelectorAll('option:checked')[0];
    let id = document.querySelector('.update').id;
    let update = document.querySelector('.update');

    console.log(id)
    console.log(year_entry.value)
    $.ajax({
        method: "POST",
        data: {year_entry: year_entry.value, group: group.value, educational_program: educational_program.value},
        headers: {"X-CSRFToken": csrftoken},
        url: `http://127.0.0.1:8000/update-student/${id}`,
        success: function (data) {
            if (data.update) {
                $(`#date_${id}`).text(year_entry.value)
                $(`#group_${id}`).text(group.innerText)
                $(`#educational_program_${id}`).text(educational_program.innerText)

                $('#form-edit #id_year_entry').val('');
                $('#form-edit #id_group').val('');
                $('#form-edit #id_educational_program').val('');
                update.setAttribute('id', '');
            }
        }
    })
}

function filterStudents(ord = null) {
    let y = document.querySelector('#id_year_entry');
    let g = document.querySelector('#id_group').querySelector('option:checked');
    let e = document.querySelector('#id_educational_program').querySelector('option:checked');
    let u = document.querySelector('#id_user__username');
    let l = document.querySelector('#id_user__last_name');

    console.log(ord)

    $.ajax({
        method: "GET",
        data: {
            ordering: ord,
            year_entry: y.value ? y.value : "",
            group: g.value ? g.value : "",
            educational_program: e.value ? e.value : "",
            user__username: u.value ? u.value : "",
            user__last_name: l.value ? l.value : "",
        },
        headers: {"X-CSRFToken": csrftoken},
        url: `http://127.0.0.1:8000/filter-student/`,
        success: function (data) {
            console.log(data.students)
            if (data.students.length) {
                $('#tbody').empty()
                for (let i of data.students) {
                    $('#tbody').append(
                        `<tr id="row_${i.id}">
                                <th scope="row">${i.id}</th>
                                <td>${i.user__last_name}</td>
                                <td>${i.user__first_name}</td>
                                <td>${i.user__surname}</td>
                                <td id="date_${i.id}">${i.year_entry}</td>
                                <td id="educational_program_${i.id}">${i.educational_program__name}</td>
                                <td id="group_${i.id}">${i.group__name}</td>
                                <td data-toggle="modal" data-target="#exampleModal" onclick="getIdStudent('${i.id}')">
                                    <a class="btn btn-warning">Редагувати</a>
                                </td>

                                <th scope="row">
                                    <a class="btn btn-danger" onclick="deleteStudent('${i.id}')">Видалити</a>
                                </th>
                            </tr>
                            `
                    )
                }
            } else {
                $('#tbody').empty()
            }
        }
    })
}
