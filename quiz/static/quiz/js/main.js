function scrollbottom() {
    const scrollbarVisible = (element) => {
        return element.scrollHeight > element.clientHeight;
    }

    const body = document.querySelector('body')

    //alert(scrollbarVisible(body));

    if (scrollbarVisible(body)) {
        $('#foot').removeClass('fixed-bottom');
    } else {
        $('#foot').addClass('fixed-bottom');
    }
}
$(document).ready(function (e) {
    scrollbottom();
    document.querySelector('html').scrollTop = 0;

    const ITEMS_COUNT_PER_CLICK = 3;

    const showButton = document.querySelector('a[id=quiz_game_btn]');
    const items = document.querySelectorAll('div[id=quiz_game]')
    const itemsCount = items.length;
    let i = ITEMS_COUNT_PER_CLICK;

    if (i >= itemsCount) {
        showButton.style.display = 'none';
    }

    for (; i < itemsCount; ++i) {
        items[i].style.display = 'none';
    }

    i = ITEMS_COUNT_PER_CLICK;

    const callback = (event) => {
        let k = 0;
        while (i < itemsCount) {
            ++k;
            items[i++].style.display = '';
            if (k == 3) {
                break;
            }
        }
        if (i >= itemsCount) {
            showButton.style.display = 'none';
        }
    };

    showButton.addEventListener('click', callback);

});

document.querySelectorAll('#drop-popover')
    .forEach((drop) => {
        drop.style.width = parseInt($("#card-game").width(), 10) - 32 + 'px';
        /*alert(drop.width());*/
    })
/*document.getElementById('drop-popover').style.width = parseInt($("#card-game").width(), 10) - 32 + 'px';*/
$(window).resize(function () {
    /*alert($("#card-game1").width());*/
    document.querySelectorAll('#drop-popover')
        .forEach((drop) => {
            drop.style.width = parseInt($("#card-game").width(), 10) - 32 + 'px';
            /*alert(drop.width());*/
        })

    /*document.getElementById('drop-popover').style.width = parseInt($("#card-game").width(), 10) - 32 + 'px';*/
});

document.querySelectorAll('[data-bs-toggle="popover"]')
    .forEach(popover => {
        new bootstrap.Popover(popover, {
            container: '.card'
        })
    })

 // ajax form
//for (const element of quiz_game) {
    //$('#write-quiz, #write-quiz_body').submit(function (event) {
    $('form').submit(function (event) {
        event.preventDefault();
        //const modal = document.querySelector('#participatequiz');
        var $button = $(this).find('button');
        /* Переменные для валидация номера телефона */
        var $phone_number= $(this).find('#phone_number');
        var $invalid_phone_number= $(this).find('#invalid-feedback-phone_number');
        /* Переменные для валидация уникальности имени команды на данную игру */
        var $name_team= $(this).find('#name_team');
        var $invalid_name_team= $(this).find('#invalid-feedback-name_team');
        /* Переменные для валидация уникальности имени капитана на данную игру */
        var $name_leader= $(this).find('#name_leader');
        var $invalid_name_leader= $(this).find('#invalid-feedback-name_leader');
        /* email */
        var $email= $(this).find('#email');
        var $invalid_email= $(this).find('#invalid-feedback-email');
        /* comment */
        var $comment= $(this).find('#comment');
        var $invalid_comment= $(this).find('#invalid-feedback-comment');
        /* certificate */
        var $certificate= $(this).find('#certificate');
        var $invalid_certificate= $(this).find('#invalid-feedback-certificate');
        $button.attr('class', 'btn btn-cyan disabled').html('<span class="spinner-border spinner-border-sm me-1" role="status" aria-hidden="true"></span> Готово');
        $name_team.attr('class', 'form-control-custom text-center is-valid');
        $invalid_name_team.html('');
        $name_leader.attr('class', 'form-control-custom text-center is-valid');
        $invalid_name_leader.html('');
        $email.attr('class', 'form-control-custom text-center is-valid');
        $invalid_email.html('');
        $phone_number.attr('class', 'form-control-custom text-center is-valid');
        $invalid_phone_number.html('');
        $comment.attr('class', 'form-control-custom text-center is-valid');
        $invalid_comment.html('');
        $certificate.attr('class', 'form-control-custom text-center is-valid');
        $invalid_certificate.html('');
        // create an AJAX call
        //alert('AJAX')
        $.ajax({
            data: $(this).serialize(), // get the form data
            type: $(this).attr('method'), // GET or POST
            url: "",
            // on success
            success: function (response) {
                var errors = response.errors;
                var error_name_team = response.error_name_team;
                var error_name_leader = response.error_name_leader;
                var error_certificate = response.error_certificate;
                //alert(errors);
                if (errors || error_name_team || error_name_leader || error_certificate) {
                    $button.attr('class', 'btn btn-cyan').html('Готово');
                    //alert(errors['phone_number']);
                    /* Валидация */
                    if (error_name_team == 'invalid-dublicate_name_team')
                    {
                        $name_team.attr('class', 'form-control-custom text-center is-invalid');
                        $invalid_name_team.html('<span>Ваша команда уже записана на данную игру! Или Вы пытаетесь записаться на такую же игру, которая проходит в другой день.</span>\n')
                    }
                    else
                    {
                        $name_team.attr('class', 'form-control-custom text-center is-valid');
                        $invalid_name_team.html('');
                    }
                    if (error_name_leader == 'invalid-dublicate_name_leader')
                    {
                        $name_leader.attr('class', 'form-control-custom text-center is-invalid');
                        $invalid_name_leader.html('<span>Вы уже записана на данную игру за другую команду! Или Вы пытаетесь записаться на такую же игру за другую команду, которая проходит в другой день.</span>\n')
                    }
                    else
                    {
                        $name_leader.attr('class', 'form-control-custom text-center is-valid');
                        $invalid_name_leader.html('');
                    }
                    if (error_certificate == 'invalid-certificate')
                    {
                        $certificate.attr('class', 'form-control-custom text-center is-invalid');
                        $invalid_certificate.html('<span>Номер сертификата для вашей команды не найден. Проверьте правильность введенного номера.</span>\n')
                    }
                    else
                    {
                        $certificate.attr('class', 'form-control-custom text-center is-valid');
                        $invalid_certificate.html('');
                    }
                    if (errors) {
                        if (errors['name_team']) {
                            //alert('name_team');
                            $name_team.attr('class', 'form-control-custom text-center is-invalid');
                            $invalid_name_team.html('<span>' + errors['name_team'] + '</span>\n');
                            /*const div = document.createElement("div");
                            div.classList.add('invalid-feedback');
                            div.innerHTML = '<span>' + errors['phone_number'] + '</span>\n';
                            $phone_number.after(div);*/
                            //alert(response.errors['phone_number'])
                        }
                        else
                        {
                            //alert('name_team valid');
                            $name_team.attr('class', 'form-control-custom text-center is-valid');
                            $invalid_name_team.html('');
                        }
                        if (errors['name_leader']) {
                            //alert('name_leader');
                            $name_leader.attr('class', 'form-control-custom text-center is-invalid');
                            $invalid_name_leader.html('<span>' + errors['name_leader'] + '</span>\n');
                            /*const div = document.createElement("div");
                            div.classList.add('invalid-feedback');
                            div.innerHTML = '<span>' + errors['phone_number'] + '</span>\n';
                            $phone_number.after(div);*/
                            //alert(response.errors['phone_number'])
                        }
                        else
                        {
                            //alert('name_leader valid');
                            $name_leader.attr('class', 'form-control-custom text-center is-valid');
                            $invalid_name_leader.html('');
                        }
                        if (errors['phone_number']) {
                            //alert($phone_number);
                            $phone_number.attr('class', 'form-control-custom text-center is-invalid');
                            $invalid_phone_number.html('<span>' + errors['phone_number'] + '</span>\n');
                            /*const div = document.createElement("div");
                            div.classList.add('invalid-feedback');
                            div.innerHTML = '<span>' + errors['phone_number'] + '</span>\n';
                            $phone_number.after(div);*/
                            //alert(response.errors['phone_number'])
                        }
                        else
                        {
                            $phone_number.attr('class', 'form-control-custom text-center is-valid');
                            $invalid_phone_number.html('');
                        }
                        if (errors['email']) {
                            //alert($phone_number);
                            $email.attr('class', 'form-control-custom text-center is-invalid');
                            $invalid_email.html('<span>' + errors['email'] + '</span>\n');
                            /*const div = document.createElement("div");
                            div.classList.add('invalid-feedback');
                            div.innerHTML = '<span>' + errors['phone_number'] + '</span>\n';
                            $phone_number.after(div);*/
                            //alert(response.errors['phone_number'])
                        }
                        else
                        {
                            $email.attr('class', 'form-control-custom text-center is-valid');
                            $invalid_email.html('');
                        }
                        if (errors['comment']) {
                            //alert($phone_number);
                            $comment.attr('class', 'form-control-custom text-center is-invalid');
                            $invalid_comment.html('<span>' + errors['comment'] + '</span>\n');
                            /*const div = document.createElement("div");
                            div.classList.add('invalid-feedback');
                            div.innerHTML = '<span>' + errors['phone_number'] + '</span>\n';
                            $phone_number.after(div);*/
                            //alert(response.errors['phone_number'])
                        }
                        else
                        {
                            $comment.attr('class', 'form-control-custom text-center is-valid');
                            $invalid_comment.html('');
                        }
                        if (errors['certificate']) {
                            //alert($phone_number);
                            $certificate.attr('class', 'form-control-custom text-center is-invalid');
                            $invalid_certificate.html('<span>' + errors['certificate'] + '</span>\n');
                            /*const div = document.createElement("div");
                            div.classList.add('invalid-feedback');
                            div.innerHTML = '<span>' + errors['phone_number'] + '</span>\n';
                            $phone_number.after(div);*/
                            //alert(response.errors['phone_number'])
                        }
                        else
                        {
                            $certificate.attr('class', 'form-control-custom text-center is-valid');
                            $invalid_certificate.html('');
                        }
                    }
                    /*else {
                        $name_team.attr('class', 'form-control-custom text-center is-valid');
                        $invalid_name_team.html('');
                        $name_leader.attr('class', 'form-control-custom text-center is-valid');
                        $invalid_name_leader.html('');
                        $phone_number.attr('class', 'form-control-custom text-center is-valid');
                        $invalid_phone_number.html('');
                        $email.attr('class', 'form-control-custom text-center is-valid');
                        $invalid_email.html('');
                        $comment.attr('class', 'form-control-custom text-center is-valid');
                        $invalid_comment.html('');
                        $certificate.attr('class', 'form-control-custom text-center is-valid');
                        $invalid_certificate.html('');
                    }*/
                }
                else {
                    location.reload();
                    //document.querySelector('html').scrollTop = 0;
                    //document.querySelector('html').scrollTop = 0;
                }
                //alert("Thank you for reaching us out, " + response.name);
                //location.reload();
            },
            // on error
            error: function (response) {
                var errors = response.errors;
            }
                //alert(response.errors);
                //document.getElementById(response.responseJSON.errors)
                //console.log(response.errors)
                //document.getElementById()
        });
        return false;
    });
//}
/*$('#write-quiz select[name=quiz_game_]').change(function() {
    alert('quiz_game_')
    var optionSelected = $(this).find('option:selected');
    var valueSelected = optionSelected.val();
    $.ajax({
        type: 'GET',
        url: '{% url "quiz-timetable" %}',
        data: {
            'selected_value': valueSelected
        },
        success: function(data, textStatus, jqXHR) {
            $('#write-quiz select[name=quiz_game_]').empty();
            $.each(data, function(key, value) {
                $('#write-quiz select[name=quiz_game_]')
                    .append($('<option>', {value: value[0]})
                    .text(value[1]));
            });
        },
        dataType: 'json'
    });
});*/

document.addEventListener('DOMContentLoaded', () => {

  const elements = document.querySelectorAll('[data-mask="phone"]') // ищем все поля с атрибутом data-mask="phone"
  if (!elements) return // если таких нет, прекращаем выполнение функции
  const phoneOptions = { // создаем объект параметров
    mask: '+{7}0000000000' // задаем единственный параметр mask
  }
  elements.forEach(el => { // для каждого найденного поля с атрибутом [data-mask="phone"]
    IMask(el, phoneOptions) // инициализируем плагин с установленными выше параметрами
  })

})

var dataTable = $('#example').dataTable({
        "ordering": true,
        "order": [[ 2, "desc" ]],
        "info": false,
        "bLengthChange": false,
        "responsive": true,
        "iDisplayLength": 20,
        "sDom": '<"row view-filter"<"col-sm-12"<"pull-left"l><"pull-right"f><"clearfix">>>t<"row view-pager"<"col-sm-12"<"text-center"ip>>>',
        "fnDrawCallback": function ( oSettings ){
            if(oSettings.fnRecordsTotal() < 20){
                $('.dataTables_length').hide();
                $('.dataTables_paginate').hide();
            } else {
                $('.dataTables_length').show();
                $('.dataTables_paginate').show();
            }
        },
        language: {
            url: '/static/quiz/js/datatables.ru.json',
        },
    });

$("#searchbox").keyup(function() {
    if (this.value === "")
    {
        $('#foot').removeClass('fixed-bottom');
    }
    dataTable.fnFilter(this.value);

    scrollbottom();
});

window.addEventListener('resize', function(event) {
    scrollbottom();
}, true);
