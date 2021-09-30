var refresh = true;

if(JSON.parse(localStorage.getItem('refresh'))){
    localStorage.setItem('refresh', false)
    window.location.reload();
}else{
    localStorage.setItem('refresh', true)
}


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

function createSubject() {
    let nameSubject = document.querySelector('#id_name_subject');
    let group = document.querySelector('#id_group');
    let hours = document.querySelector('#id_hours');

    let semester = document.querySelector('#id_semester');
    let final_semester = document.querySelector('#id_final_semester');

    let teachers = document.querySelector('#id_teachers').getElementsByTagName('option');
    let urlOnMoodle = document.querySelector('#id_url_on_moodle');
    let formOfControl = document.querySelector('#id_form_of_control');
    let finallySubject = document.querySelector('#id_finally_subject');

    let loans = hours.value / 2

    let teacherList = [];
    let nameTeachers = [];

    for (let i of teachers) {
        if (i.selected) {
            teacherList.push(i.value);
            nameTeachers.push(i.innerText);
        }
    }
    let nameGroup = $.trim($("#id_group").children("option:selected").text())

    $.ajax({
        method: "POST",
        data: {name_subject: nameSubject.value, group: group.value,
               hours: hours.value, finally_subject: finallySubject.value,
               semester: semester.value, teachers: teacherList, final_semester: final_semester.value,
               form_of_control: formOfControl.value, url_on_moodle: urlOnMoodle.value},
        headers: {"X-CSRFToken": csrftoken},
        url: `http://127.0.0.1:8000/create-subjects/`,
        traditional: true,
        success: function (data) {
            if(data.created_subject){
                $(`#tbody`).append(
                `<tr id="row_${ data.subject_id }">
                        <td><a href="/semesters/${data.subject_id}" id="name_subject">${ nameSubject.value }</a></td>
                        <td id="group" data-id="${group.value}" class="${group.value}">${ nameGroup }</td>
                        <td id="teachers">
                        </td>
                        <td id="hours">${ hours.value }</td>
                        <th scope="row" id="loans">${ loans }</th>
                        <td id="semester">${ semester.value }</td>
                        <td id="final_semester">${ final_semester.value }</td>
                        <td id="form_of_control">${ formOfControl.value }</td>
                        <td id="finally_subject">${finallySubject.value ? "Так": "Ні"}</td>
                        <td><a href="${ urlOnMoodle.value }" id="link">Посилання на Moodle</a></td>
                        <td><a class="btn btn-warning" data-toggle="modal" data-target="#exampleModal1" onclick="updateForm(${ data.subject_id })">Редагувати</a></td>
                        <td>
                            <a class="btn btn-danger" onclick="deleteSubject(${ data.subject_id })">Видалити</a>
                        </td>
                    </tr>`
                )
                for(let i of nameTeachers){
                    $(`#tbody #row_${ data.subject_id } #teachers`).append(i + "<br/>")
                }
            }
        }})
}

function deleteSubject(id) {
    $.ajax({
        method: "POST",
        headers: {"X-CSRFToken": csrftoken},
        url: `http://127.0.0.1:8000/delete/${id}`,
        success: function (data) {
            console.log(data)
            if (data.delete) {
                $(`#row_${id}`).remove()
            }
        }
    })
}

function updateForm(id){

    let nameSubject = document.querySelector(`#row_${id} #name_subject`).innerText;
    let group = document.querySelector(`#row_${id} #group`);
    let teachers = document.querySelector(`#row_${id} #teachers`).innerText.split('\n').slice(0, -1);
    let hours = document.querySelector(`#row_${id} #hours`).innerText;
    let loans = document.querySelector(`#row_${id} #loans`).innerText;

    let finallySubject = document.querySelector(`#row_${id} #finally_subject`).innerText;

    let semester = document.querySelector(`#row_${id} #semester`).innerText;
    let final_semester = document.querySelector(`#row_${id} #final_semester`).innerText;

    let formOfControl = document.querySelector(`#row_${id} #form_of_control`).innerText;
    let link = document.querySelector(`#row_${id} #link`).href;

    console.log(group.getAttribute('data-id'))
    console.log(group)

    document.querySelector('#id_name_subject1').value = nameSubject
    document.querySelector('#id_group1').value = group.getAttribute('data-id')
    document.querySelector('#id_hours1').value = hours
    document.querySelector('#id_semestr1').value = semester
    document.querySelector('#id_semestr2').value = final_semester
    let option = document.querySelector('#id_teachers1').getElementsByTagName('option')
    document.querySelector('#id_forma_control1').value = formOfControl
    document.querySelector('#id_url_on_moodle1').value = link

    if(finallySubject === "Так"){
        document.querySelector('#finally-subject').checked = true
    }

    for (let i of option) {
        if (teachers.includes(i.innerText)) {
            i.selected = true;
        } else {
            i.selected = false;
        }
    }

    updateButton = document.querySelector('.button')
    updateButton.setAttribute('id', id)
}

function updateSubject(){
    let nameSubject = document.querySelector('#id_name_subject1').value;
    let group = document.querySelector('#id_group1').value;
    let hours = document.querySelector('#id_hours1').value;
    let semester = document.querySelector('#id_semestr1').value;
    let final_semester = document.querySelector('#id_semestr2').value;
    let teachers = document.querySelector('#id_teachers1').getElementsByTagName('option');
    let urlOnMoodle = document.querySelector('#id_url_on_moodle1').value;
    let formOfControl = document.querySelector('#id_forma_control1').value;
    let finallySubject = document.querySelector('#finally-subject').value;
    let id = document.querySelector('.button').id;

    let teacherId = []
    let teacherName = []

    for(let i of teachers){
        if(i.selected){
            teacherId.push(i.value)
            teacherName.push(i.innerText)
        }
    }

    let loans = hours / 2

    let groupTd = document.querySelector(`#row_${id} #group`)

    console.log(group)

    $.ajax({
        method: "POST",
        data: {name_subject: nameSubject, hours: hours,
               semester: semester, teachers: teacherId, final_semester: final_semester, group: group,
               form_of_control: formOfControl, url_on_moodle: urlOnMoodle, finally_subject: finallySubject},
        headers: {"X-CSRFToken": csrftoken},
        url: `/update/${id}`,
        traditional: true,
        success: function (data) {
            console.log(data)
            if(data.update_subject){
                document.querySelector(`#row_${id} #name_subject`).innerText = nameSubject;
                groupTd.innerText = $('#id_group1 option:selected').text();
                document.querySelector(`#row_${id} #hours`).innerText = hours;
                document.querySelector(`#row_${id} #semester`).innerText = semester;
                document.querySelector(`#row_${id} #final_semester`).innerText = final_semester;
                document.querySelector(`#row_${id} #form_of_control`).innerText = formOfControl;
                document.querySelector(`#row_${id} #link`).href = urlOnMoodle;
                document.querySelector(`#row_${id} #loans`).innerText = loans;
                $(`#row_${id} #teachers`).empty()
                for(let i of teacherName){
                    $(`#row_${id} #teachers`).append(i + '<br/>')
                }
                groupTd.setAttribute('data-id', $('#id_group1 option:selected').val())
            }
    }})

}