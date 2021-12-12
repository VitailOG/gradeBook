let select = document.querySelector('select')
document.addEventListener('DOMContentLoaded', function () {
    let semester = select.querySelector('option:checked').value
    $.ajax({
        method: "GET",
        url: `/student/rating-by-semester/${semester}`,
        success: function (data) {
            if(data.s){
                $(`#gradeBook`).empty()
                for(let i of data.s){
                    $(`#gradeBook`).append(`
                        <tr style="${i.retransmission ? 'background: grey' : ''}">
                            <td>
                                <div id="subjects">
                                    ${i.subject__name_subject}
                                </div>
                            </td>
                            <td>
                                <div id="rating_5">
                                     ${i.rating_5}
                                </div>
                            </td>
                            <td>
                                <div id="rating_12">
                                     ${i.rating_12 === null ? '-' : i.rating_12}
                                </div>
                            </td>
                            <td>
                                <div id="retransmission">
                                    ${i.retransmission === true ? 'Перездана' : '-'}
                                </div>
                            </td>
                            <td>
                                <div id="credited">
                                    ${i.credited === true ? 'Зараховано' : '-'}
                                </div>
                            </td>
                            <td>
                                <div id="data">
                                    ${i.date_rating}
                                </div>
                            </td>
                            <td>
                                <div id="teacher">
                                    ${i.teacher__first_name.slice(0,1)}.
                                    ${i.teacher__surname.slice(0,1)}. 
                                    ${i.teacher__last_name}
                                </div>
                            </td>
                        </tr>
                    `)


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
                $(`#gradeBook`).empty()
                for(let i of data.s){
                                      
                    $(`#gradeBook`).append(`
                        <tr style="${i.retransmission ? 'background: grey' : ''}">
                            <td>
                                <div id="subjects">
                                    ${i.subject__name_subject}
                                </div>
                            </td>
                            <td>
                                <div id="rating_5">
                                     ${i.rating_5}
                                </div>
                            </td>
                            <td>
                                <div id="rating_12">
                                    ${i.rating_12 === null ? '-' : i.rating_12}
                                </div>
                            </td>
                            <td>
                                <div id="retransmission">
                                    ${i.retransmission === true ? 'Перездана' : '-'}
                                </div>
                            </td>
                            <td>
                                <div id="credited">
                                    ${i.credited === true ? 'Зараховано' : '-'}
                                </div>
                            </td>
                            <td>
                                <div id="data">
                                    ${i.date_rating}
                                </div>
                            </td>
                            <td>
                                <div id="teacher">
                                     ${i.teacher__first_name.slice(0,1)}.
                                    ${i.teacher__surname.slice(0,1)}. 
                                    ${i.teacher__last_name}
                                </div>
                            </td>
                        </tr>
                    `)
                }
            }
        }
    })
})