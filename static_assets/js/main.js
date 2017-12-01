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

    $(".load-1").addClass("bg-success");
    $(".load-2").addClass("bg-info");
    $(".load-3").addClass("bg-danger");

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

    $("#dialog").on('change', '.weekEvent', function () {
        var csrfToken = $("[name=csrfmiddlewaretoken]").val();

        data = {
            csrfmiddlewaretoken: csrfToken,
            eventId: $(this).data('id'),
            newWeek: $(this).val(),
        };
        $.ajax({
            url: "/week_scheduler/change_event_week/",
            data: data,
            method: "POST",
            statusCode: {
                200: function () {
                    location.reload();
                }
            },
            error: function () {
                alert("ups, ha ocurrido un error :(");
            }
        });
    });

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
                    location.reload();
                }
            },
            error: function () {
                alert("ups, ha ocurrido un error :(");
            }
        });
    }

    $("#dialog").dialog(
        {
            autoOpen: false
        });

    $(".event").click(function () {
        var id = $(this).attr('id');
        var innerHtml = $("#" + id + "details").html();
        var title = $("#" + id + "details").data('name');
        $("#dialog").html(innerHtml);
        $("#dialog").dialog("option", 'title', title);
        $("#dialog").dialog("open");
    });
});