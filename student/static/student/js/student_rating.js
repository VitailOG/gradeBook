let select = document.querySelector('select')
document.addEventListener('DOMContentLoaded', function () {
    let semester = select.querySelector('option:checked').value
    $.ajax({
        method: "GET",
        url: `/student/rating-by-semester/${semester}`,
        success: function (data) {
            if(data.s){
                $(`#subjects`).empty()
                for(let i of data.s){
                    console.log(i)
                    $(`#subjects`).append(
                        `
                          <div>${i.subject__name_subject} - ${i.rating_5}</div>
                        `
                    )
                }
            }
        }
    })
})

select.addEventListener('change', function () {
    let semester = select.querySelector('option:checked').value
    $.ajax({
        method: "GET",
        url: `/student/rating-by-semester/${semester}`,
        success: function (data) {
            if(data.s){
                $(`#subjects`).empty()
                for(let i of data.s){
                    console.log(i)
                    $(`#subjects`).append(
                        `
                          <div>${i.subject__name_subject} - ${i.rating_5}</div>
                        `
                    )
                }
            }
        }
    })
})