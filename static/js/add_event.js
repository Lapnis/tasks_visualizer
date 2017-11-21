function dateTextToTimeStamp(date) {
    s = date.split("/");
    d = s[0];
    m = s[1];
    y = s[2];
    return (new Date(y, m, d)).getTime()
}

function clearForm() {
    $("#course").val("CC6402");
    $("#week").val("15");
    deadline = $("#deadline").val("");
    name = $("#name").val("");
    type = $("#type").val("0");
    load = $("#load").val("2");
}

function submitEvent(){
    course = $("#course").val();
    week = $("#week").val();
    deadline = dateTextToTimeStamp($("#deadline").val());
    name = $("#name").val();
    type = $("#type").val();
    load = $("#load").val();
    data = {
        course : course,
        week : week,
        deadline: deadline,
        name: name,
        type: type,
        load: load,
    };

    $.ajax({
        url: "/week_scheduler/add_event/",
        data : data,
        method: "POST",
        statusCode: {
            200: function () {
                alert("Se agerego exitosamente!");
                clearForm();
            }
        }
    });
}