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
                {"data": "id"},
                {"data": "name"},
                {"data": "description"},
                {"data": "image"},
                {"data": "cost"},
                {"data": "pvp"},
                {"data": "active"},
                {"data": "id"},
            ],
            columnDefs: [
                {
                    targets: [-5],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<img src="' + data + '" class="img-fluid d-block mx-auto" style="width: 20px; height: 20px;">';
                    }
                },
                {
                    targets: [-3,-4],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        console.log(data);
                        if(data === 0){
                            return '<i class="fas fa-check-circle text-green"></i>';
                        }
                        if(data === 1){
                            return '<i class="fas fa-times-circle text-red"></i>';
                        }
                        //return '$' + parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        var buttons = '<a href="/erp/product/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                        buttons += '<a href="/erp/product/delete/' + row.id + '/" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
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
