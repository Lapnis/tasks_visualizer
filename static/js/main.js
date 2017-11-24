$(document).ready(function () {
    //CSRF Token configuration for Jquery Ajax
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });


    $("#datepicker").datepicker({dateFormat: 'dd/mm/yy'});
    $("#load").imagepicker({
        show_label: true
    });
    $("#addbtn").on('click', function () {
        $("#canceldiv").show();
        $("#adddiv").hide();
    });
    $("#cancelbtn").on('click', function () {
        $("#canceldiv").hide();
        $("#adddiv").show();
        clearForm();
    });
    $('.event').on("dragstart", function (event) {
        var dt = event.originalEvent.dataTransfer;
        dt.setData('Text', $(this).attr('id'));
    });
    $('table td').on("dragenter dragover drop", function (event) {
        event.preventDefault();
        if (event.type === 'drop') {
            var data = event.originalEvent.dataTransfer.getData('Text', $(this).attr('id'));
            de = $('#' + data).detach();
            de.appendTo($(this));
        }
    });

    function dateTextToTimeStamp(date) {
        s = date.split("/");
        d = s[0];
        m = s[1];
        y = s[2];
        //return (new Date(y, m, d)).getTime();
        return date;
    }

    function clearForm() {
        deadline = $("#datepicker").val("");
        name = $("#name").val("");
    }

    $("#savebtn").click(submitEvent);

    function submitEvent() {
        var csrfToken = $("[name=csrfmiddlewaretoken]").val();
        course = $("#course").val();
        week = $("#week").val();
        deadline = dateTextToTimeStamp($("#datepicker").val());
        name = $("#name").val();
        type = $("#type").val();
        load = $("#load").val();
        data = {
            csrfmiddlewaretoken: csrfToken,
            course: course,
            week: week,
            deadline: deadline,
            name: name,
            type: type,
            load: load
        };
        $.ajax({
            url: "/week_scheduler/add_event/",
            data: data,
            method: "POST",
            statusCode: {
                200: function () {
                    alert("Se agregó exitosamente!");
                    clearForm();
                }
            }
        });
    }
});