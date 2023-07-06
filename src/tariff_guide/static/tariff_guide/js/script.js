$(document).ready(function() {
    // var parentDiv = $('#маршруты-tab');
    // parentDiv.html('<div class= "form-group field-r_list">Hello!</div>');
    parentDiv = $(".form-group.field-routes_list").parent().closest('div');
    // var cardBody = $("#маршруты-tab").children(".card-body").eq(0);
    parentDiv.append('<div class= "form-group field-r_list"><div class="row">\n' +
        '            \n' +
        '                <label class="col-sm-3 text-left" for="id_sender">\n' +
        '                    Город отправитель\n' +
        '                    \n' +
        '                    <span class="text-red">* </span>\n' +
        '                    \n' +
        '                </label>\n' +
        '                <div class=" col-auto  fieldBox \n' +
        '                              field-script\n' +
        '                             \n' +
        '                             \n' +
        '                             ">\n' +
        '                    \n' +
        '                        <div class="related-widget-wrapper" data-model-ref="Город отправитель">\n' +
        '    <select name="script" required="" id="id_sender" data-select2-id="select2-data-id_sender" tabindex="-1" class="select2-hidden-accessible" aria-hidden="true">\n' +
        '  <option value="">---------</option>\n' +
        '\n' +
        '  <option value="8" selected="" data-select2-id="select2-data-2-fpxp">Между собой</option>\n' +
        '\n' +
        '  <option value="10">Во все города</option>\n' +
        '\n' +
        '  <option value="11">В города региона</option>\n' +
        '\n' +
        '  <option value="12">ТОП маршрутов</option>\n' +
        '\n' +
        '  <option value="13">Маршруты</option>\n' +
        '\n' +
        '  <option value="14">Фильтр по количеству</option>\n' +
        '\n' +
        '</select><span class="select2 select2-container select2-container--default" dir="ltr" data-select2-id="select2-data-1-iipu" style="width: 194px;"><span class="selection"><span class="select2-selection select2-selection--single" role="combobox" aria-haspopup="true" aria-expanded="false" tabindex="0" aria-disabled="false" aria-labelledby="select2-id_sender-container" aria-controls="select2-id_sender-container"><span class="select2-selection__rendered" id="select2-id_sender-container" role="textbox" aria-readonly="true" title="Между собой">Между собой</span><span class="select2-selection__arrow" role="presentation"><b role="presentation"></b></span></span></span><span class="dropdown-wrapper" aria-hidden="true"></span></span>\n' +
        '    \n' +
        '        <a class="related-widget-wrapper-link change-related" id="change_id_sender" data-href-template="/admin/tariff_guide/script/__fk__/change/?_to_field=id&amp;_popup=1" data-popup="yes" title="Изменить выбранный объект типа " Город отправитель""="" href="/admin/tariff_guide/script/8/change/?_to_field=id&amp;_popup=1"><img src="/static/admin/img/icon-changelink.svg" alt="Изменить"></a><a class="related-widget-wrapper-link add-related" id="add_id_sender" data-popup="yes" href="/admin/tariff_guide/script/add/?_to_field=id&amp;_popup=1" title="Добавить ещё один объект типа " Город отправитель""=""><img src="/static/admin/img/icon-addlink.svg" alt="Добавить"></a><a class="related-widget-wrapper-link view-related" id="view_id_sender" data-href-template="/admin/tariff_guide/script/__fk__/change/?_to_field=id" title="Просмотреть выбранный объект типа " Город отправитель""="" href="/admin/tariff_guide/script/8/change/?_to_field=id"><img src="/static/admin/img/icon-viewlink.svg" alt="Просмотреть"></a>\n' +
        '    \n' +
        '</div>\n' +
        '                    \n' +
        '                    <div class="help-block red">\n' +
        '                        \n' +
        '                    </div>\n' +
        '                    \n' +
        '                    <div class="help-block text-red">\n' +
        '                        \n' +
        '                    </div>\n' +
        '                </div>\n' +
        '            \n' +
        '                <label class="col-auto text-left" for="id_receiver">\n' +
        '                    Город получатель\n' +
        '                    \n' +
        '                    <span class="text-red">* </span>\n' +
        '                    \n' +
        '                </label>\n' +
        '                <div class=" col-auto  fieldBox \n' +
        '                              field-direction\n' +
        '                             \n' +
        '                             \n' +
        '                             ">\n' +
        '                    \n' +
        '                        <div class="related-widget-wrapper" data-model-ref="Канал">\n' +
        '    <select name="direction" required="" id="id_receiver" data-select2-id="select2-data-id_receiver" tabindex="-1" class="select2-hidden-accessible" aria-hidden="true">\n' +
        '  <option value="">---------</option>\n' +
        '\n' +
        '  <option value="7">ПиП</option>\n' +
        '\n' +
        '  <option value="8" selected="" data-select2-id="select2-data-4-1nv1">ИМ</option>\n' +
        '\n' +
        '</select><span class="select2 select2-container select2-container--default" dir="ltr" data-select2-id="select2-data-3-18eg" style="width: 66px;"><span class="selection"><span class="select2-selection select2-selection--single" role="combobox" aria-haspopup="true" aria-expanded="false" tabindex="0" aria-disabled="false" aria-labelledby="select2-id_receiver-container" aria-controls="select2-id_receiver-container"><span class="select2-selection__rendered" id="select2-id_receiver-container" role="textbox" aria-readonly="true" title="ИМ">ИМ</span><span class="select2-selection__arrow" role="presentation"><b role="presentation"></b></span></span></span><span class="dropdown-wrapper" aria-hidden="true"></span></span>\n' +
        '    \n' +
        '        <a class="related-widget-wrapper-link change-related" id="change_id_receiver" data-href-template="/admin/tariff_guide/direction/__fk__/change/?_to_field=id&amp;_popup=1" data-popup="yes" title="Изменить выбранный объект типа " Канал""="" href="/admin/tariff_guide/direction/8/change/?_to_field=id&amp;_popup=1"><img src="/static/admin/img/icon-changelink.svg" alt="Изменить"></a><a class="related-widget-wrapper-link add-related" id="add_id_receiver" data-popup="yes" href="/admin/tariff_guide/direction/add/?_to_field=id&amp;_popup=1" title="Добавить ещё один объект типа " Канал""=""><img src="/static/admin/img/icon-addlink.svg" alt="Добавить"></a><a class="related-widget-wrapper-link view-related" id="view_id_receiver" data-href-template="/admin/tariff_guide/direction/__fk__/change/?_to_field=id" title="Просмотреть выбранный объект типа " Канал""="" href="/admin/tariff_guide/direction/8/change/?_to_field=id"><img src="/static/admin/img/icon-viewlink.svg" alt="Просмотреть"></a>\n' +
        '    \n' +
        '</div>\n' +
        '                    \n' +
        '                    <div class="help-block red">\n' +
        '                        \n' +
        '                    </div>\n' +
        '                    \n' +
        '                    <div class="help-block text-red">\n' +
        '                        \n' +
        '                    </div>\n' +
        '                </div>\n' +
        '            \n' +
        '        </div></div>');
    console.log(parentDiv)
    // parentDiv = $('#id_parsing_model').parent().closest('div');
    // var model = $("#id_parsing_model").val();
    // $("#id_parsing_model").hide();
    // parentDiv.html('<select id= "id_parsing_model_select"></select>')
    // var models = ["api_lkp", "billing", "cdek", "cdek_box", "dpd", "pochta", "sberlogistic"]
    // console.log(model)
    // $.each(models, function(index, value){
    //     console.log(value)
    //     if (value == model) {
    //         $('#id_parsing_model_select').append($('<option>', {
    //             value: value,
    //             text: value,
    //             selected: true
    //         }));
    //     }
    //     else {
    //         $('#id_parsing_model_select').append($('<option>', {
    //         value: value,
    //         text: value
    //     }));
    //     }
    // });
    //
    // parentDiv.html('<select id= "id_parsing_model">' +
    //     '<option>api_lkp</option><option>billing</option><option>cdek</option><option>cdek_box</option>' +
    //     '<option>dpd</option><option>pochta</option><option>sberlogistic</option>' +
    //     '</select>');
    // $('#id_delivery_servise').on('change', function () {
    //     $('#id_code').find('option').remove()
    //     $.each(apiCodes, function(index, value){
    //         if (value.serviсe_id == $('#id_delivery_servise').val()) {
    //             $('#id_code').append($('<option>', {
    //                 value: value.code,
    //                 text: value.tittle
    //             }));
    //         }
    //     });
    // });
    // $('#id_parsing_model_select').on('change', function () {
    //     var mod = $('id_parsing_model_select').val()
    //     $('#id_parsing_model').val(mod)
    //
    // });
    // $('#id_code_select').on('change', function () {
    //     var mod = $('id_code_select').val()
    //     $('#id_code').val(mod)
    //
    // });
})
