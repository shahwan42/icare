/*global $ */
/*eslint-env browser*/

$(document).ready(function () {
    $(".side-nav .aside-control span.minus").click(function () {
        $(this).hide().siblings().show();
        $(this).parent().parent().parent().addClass("sidbar");
    });
    $(".side-nav .aside-control span.plus").click(function () {
        $(this).hide().siblings().show();
        $(this).parent().parent().parent().removeClass("sidbar");
    });

    $(".aside_list ul li").click(function () {
        $(this).addClass("active").siblings().removeClass("active");
    });
    if ($(window).width() < 576) {
        $(".page-body-wrapper").addClass("sidbar");
    }

});
$(document).ready(function () {
    $('#table_id').DataTable();
});


// ========================================= Handle Custom Fields for a new task

function short_text_field(short_text) {
    return `
    <p>
        <label>${short_text.name} *</label>
        <input type="text" class="textinput textInput form-control custom_field" required id="${short_text.clickup_id}">
    </p>
    `
}

function text_field(text) {
    return `
    <p>
        <label>${text.name} *</label>
        <textarea cols="30" rows="5" class="textarea form-control custom_field" required="" id="${text.clickup_id}"></textarea>
    </p>
    `
}

function dropdown_field_options(drop_down) {
    options = drop_down.type_config.options
    optionsStr = ``
    options.forEach(option => {
        optionsStr += `<option value="${option.id}">${option.name}</option>`
    })
    return optionsStr
}

function dropdown_field(drop_down) {
    return `
    <p>
        <label>${drop_down.name} *</label>
        <select class="custom_field">
            <option value="" selected="">------</option>
            ${dropdown_field_options(drop_down)}
        </select>
    </p>
    `
}
/*
function getCustomFields() {
    // Get list's primary key
    pk = $("select").children("option:selected").val()

    custom_fields = $("#custom_fields")
    $.get(`/lists/${pk}/custom_fields`, function (data, status) {
        console.log(status)
        console.log(data);
        console.log(custom_fields)
        if (status == "success") {
            custom_fields.empty()
            data.fields.forEach(field => {
                if (field.type == "short_text") {
                    custom_fields.append(short_text_field(field))
                } else if (field.type == "text") {
                    custom_fields.append(text_field(field))
                } else if (field.type == "drop_down") {
                    custom_fields.append(dropdown_field(field))
                } else { }
            });
        }
    });
}
*/
