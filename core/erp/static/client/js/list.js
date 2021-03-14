var mytable = {
    parametersTable: {
        action: '',
        start_page: 0,
        end_page: 0,
    },
    list: function (act, start, end) {

        this.parametersTable.action = act;
        this.parametersTable.start_page = start;
        this.parametersTable.end_page = end

        $('#data').DataTable({
            // mensaje de cargando
            "processing": true,
            "serverSide": true,
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            order: false,
            // que no tenga paginacion
            paging: false,
            // que no se ordene
            ordering: false,
            // que no muestre el valor total
            info: false,
            // que no tenga la caja de busqueda
            searching: false,
            // se crea el datatable con la busqueda dependiendo de si tiene busqueda o no
            ajax: {
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': this.parametersTable.action,
                    'start_page': this.parametersTable.start_page,
                    'end_page': this.parametersTable.end_page,
                    'search': pagination.items.search,
                },
                dataSrc: ""
            },
            columns: [
                {"data": "names"},
                {"data": "surnames"},
                {"data": "dni"},
                {"data": "date_birthday"},
                {"data": "gender.name"},
                {"data": "id"},
            ],
            columnDefs: [
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        var buttons = '<a href="/erp/client/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                        buttons += '<a href="/erp/client/delete/' + row.id + '/" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                        return buttons;
                    }
                },
            ],
            initComplete: function (settings, json) {
                // actualice el numero de elementos visibles
                $('input[name="visible_rows_count"]').val(json.length);
            }
        });
    }
}

$(function () {
    // pagination.js
    PaginationConstructor();
});
