var currentLocation = window.location.pathname.split('/')

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

function createRating(userId, ocinkuId, semester=null) {
    let rating_5 = document.querySelector(`#user_row_${userId} #id_rating_5`).value;
    let rating_12 = document.querySelector(`#user_row_${userId} #id_rating_12`).value;
    let date = document.querySelector(`#user_row_${userId} #id_date_rating`).value;
    let retransmission = document.querySelector(`#user_row_${userId} #id_retransmission`).checked;
    let credited = document.querySelector(`#user_row_${userId} #id_credited`).checked;
    let teacher = document.querySelector(`#user_row_${userId} #id_teacher`).value;

    let currentSemester = currentLocation[currentLocation.length - 1]

    // refactoring
    let data = {
        rating_5: rating_5,
        rating_12: rating_12,
        date_rating: date,
        retransmission: retransmission,
        credited: credited,
        teacher: teacher
    }

    if(semester !== null){
        Object.assign(data, {semester: currentSemester})
    }

    $.ajax({
        method: "POST",
        data: data,
        headers: {"X-CSRFToken": csrftoken},
        url: `/create-rating/${ocinkuId}/${userId}`,
        success: function (data) {
            console.log(data)
            if(data.create){
                    document.querySelector(`#user_row_${userId} #id_rating_5`).value = rating_5;
                    document.querySelector(`#user_row_${userId} #id_rating_12`).value = rating_12;
                    document.querySelector(`#user_row_${userId} #id_date_rating`).value = date;
                    document.querySelector(`#user_row_${userId} #id_retransmission`).checked = retransmission;
                    document.querySelector(`#user_row_${userId} #id_credited`).checked = credited;
                    document.querySelector(`#user_row_${userId} #id_teacher`).value = teacher;
                    $(`#action_${userId}`).empty()
                    $(`#action_${userId}`).append(
                        `<a id="but_${userId}" class="btn btn-warning"
                               onclick="updateRating(${data.rating_id}, ${userId}, ${currentSemester})">Оновити</a>`
                    )
                    console.log(document.querySelector(`#but_${userId}`))
                }
        }
    })
}

function updateRating(id, userId, semester=null) {
    let rating_5 = document.querySelector(`#user_row_${userId} #id_rating_5`).value;
    let rating_12 = document.querySelector(`#user_row_${userId} #id_rating_12`).value;
    let date = document.querySelector(`#user_row_${userId} #id_date_rating`).value;
    let retransmission = document.querySelector(`#user_row_${userId} #id_retransmission`).checked;
    let credited = document.querySelector(`#user_row_${userId} #id_credited`).checked;
    let teacher = document.querySelector(`#user_row_${userId} #id_teacher`).value;

    let data = {
        rating_5: rating_5,
        rating_12: rating_12,
        date_rating: date,
        retransmission: retransmission,
        credited: credited,
        teacher: teacher
    }

    if(semester !== null){
        Object.assign(data, {semester: semester})
    }

    $.ajax({
        method: "POST",
        data: data,
        headers: {"X-CSRFToken": csrftoken},
        url: `/update-rating/${id}`,
        success: function (data) {
            document.querySelector(`#user_row_${userId} #id_rating_5`).value = rating_5;
            document.querySelector(`#user_row_${userId} #id_rating_12`).value = rating_12;
            document.querySelector(`#user_row_${userId} #id_date_rating`).value = date;
            document.querySelector(`#user_row_${userId} #id_retransmission`).checked = retransmission;
            document.querySelector(`#user_row_${userId} #id_credited`).checked = credited;
            document.querySelector(`#user_row_${userId} #id_teacher`).value = teacher;
            console.log('update')
        }
    })

}