// $(document).ready(function() {
//     parentDiv = $('#id_code').parent().closest('div');
//     var valCode = $("#id_code").val()
//     $("#id_code").hide();
//     parentDiv.html('<select id= "id_code_select"><option>' + valCode + '</option></select>');
//     parentDiv = $('#id_parsing_model').parent().closest('div');
//     var model = $("#id_parsing_model").val();
//     $("#id_parsing_model").hide();
//     parentDiv.html('<select id= "id_parsing_model_select"></select>')
//     var models = ["api_lkp", "billing", "cdek", "cdek_box", "dpd", "pochta", "sberlogistic"]
//     console.log(model)
//     $.each(models, function(index, value){
//         console.log(value)
//         if (value == model) {
//             $('#id_parsing_model_select').append($('<option>', {
//                 value: value,
//                 text: value,
//                 selected: true
//             }));
//         }
//         else {
//             $('#id_parsing_model_select').append($('<option>', {
//             value: value,
//             text: value
//         }));
//         }
//     });

    // parentDiv.html('<select id= "id_parsing_model">' +
    //     '<option>api_lkp</option><option>billing</option><option>cdek</option><option>cdek_box</option>' +
    //     '<option>dpd</option><option>pochta</option><option>sberlogistic</option>' +
    //     '</select>');
//     $('#id_delivery_servise').on('change', function () {
//         $('#id_code').find('option').remove()
//         $.each(apiCodes, function(index, value){
//             if (value.serviсe_id == $('#id_delivery_servise').val()) {
//                 $('#id_code').append($('<option>', {
//                     value: value.code,
//                     text: value.tittle
//                 }));
//             }
//         });
//     });
//     $('#id_parsing_model_select').on('change', function () {
//         var mod = $('id_parsing_model_select').val()
//         $('#id_parsing_model').val(mod)
//
//     });
//     $('#id_code_select').on('change', function () {
//         var mod = $('id_code_select').val()
//         $('#id_code').val(mod)
//
//     });
// })
