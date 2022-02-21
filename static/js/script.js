$(document).ready(function ($) {

    $(document).find('.btn_save').hide();
    $(document).find('.btn_cancel').hide();

    //--->make div editable > start
    $(document).on('click', '.row_data', function (event) {
        event.preventDefault();

        if ($(this).attr('edit_type') == 'button') {
            return false;
        }

        //make div editable
        $(this).closest('div').attr('contenteditable', 'true');
        //add bg css
        $(this).addClass('bg-warning').css('padding', '5px');

        $(this).focus();
    })
    //--->make div editable > end

    //--->save single field data > start
    $(document).on('focusout', '.row_data', function (event) {
        event.preventDefault();

        if ($(this).attr('edit_type') == 'button') {
            return false;
        }

        var row_id = $(this).closest('tr').attr('row_id');

        var row_div = $(this)
            .removeClass('bg-warning') //remove bg css
            .css('padding', '')

        var col_name = row_div.attr('col_name');
        var col_val = row_div.html();

        var arr = {};
        arr[col_name] = col_val;

        //use the "arr"	object for your ajax call
        $.extend(arr, { row_id: row_id });

        //output to show
        $('.post_msg').html('<pre class="bg-success">' + JSON.stringify(arr, null, 2) + '</pre>');
    })
    //--->save single field data > end

    //--->button > edit > start
    $(document).on('click', '.btn_edit', function (event) {
        event.preventDefault();
        var tbl_row = $(this).closest('tr');

        var row_id = tbl_row.attr('row_id');

        tbl_row.find('.btn_save').show();
        tbl_row.find('.btn_cancel').show();

        //hide edit button
        tbl_row.find('.btn_edit').hide();

        //make the whole row editable
        tbl_row.find('.row_data')
            .attr('contenteditable', 'true')
            .attr('edit_type', 'button')
            .addClass('bg-warning')
            .css('padding', '3px')

        //--->add the original entry > start
        tbl_row.find('.row_data').each(function (index, val) {
            //this will help in case user decided to click on cancel button
            $(this).attr('original_entry', $(this).html());
        });
        //--->add the original entry > end

    });
    //--->button > edit > end

    //--->button > cancel > start
    $(document).on('click', '.btn_cancel', function (event) {
        event.preventDefault();

        var tbl_row = $(this).closest('tr');

        var row_id = tbl_row.attr('row_id');

        //hide save and cacel buttons
        tbl_row.find('.btn_save').hide();
        tbl_row.find('.btn_cancel').hide();

        //show edit button
        tbl_row.find('.btn_edit').show();

        //make the whole row editable
        tbl_row.find('.row_data')
            .attr('edit_type', 'click')
            .removeClass('bg-warning')
            .css('padding', '')

        tbl_row.find('.row_data').each(function (index, val) {
            $(this).html($(this).attr('original_entry'));
        });
    });
    //--->button > cancel > end

    //--->save whole row entery > start
    $(document).on('click', '.btn_save', function (event) {
        event.preventDefault();
        var tbl_row = $(this).closest('tr');

        var row_id = tbl_row.attr('row_id');


        //hide save and cacel buttons
        tbl_row.find('.btn_save').hide();
        tbl_row.find('.btn_cancel').hide();

        //show edit button
        tbl_row.find('.btn_edit').show();


        //make the whole row editable
        tbl_row.find('.row_data')
            .attr('edit_type', 'click')
            .removeClass('bg-warning')
            .css('padding', '')

        //--->get row data > start
        var arr = {};
        tbl_row.find('.row_data').each(function (index, val) {
            var col_name = $(this).attr('col_name');
            var col_val = $(this).html();
            arr[col_name] = col_val;
        });
        //--->get row data > end

        //use the "arr"	object for your ajax call
        $.extend(arr, { row_id: row_id });

        //out put to show
        $('.post_msg').html('<pre class="bg-success">' + JSON.stringify(arr, null, 2) + '</pre>')


    });
    //--->save whole row entery > end
});