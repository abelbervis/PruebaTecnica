var tblSale;

function format(d) {
    console.log(d);
    var html = '<table class="table"';
    html += '<thead>';
    html += '<tr><th scope="col">Producto</th>';
    html += '<th scope="col">PVP</th>';
    html += '<th scope="col">Cantidad</th>';
    html += '<th scope="col">Subtotal</th></tr>';
    html += '</thead>';
    html += '<tbody>';

    //d.det es la variable que se obtiene en models del toJSON de Sale
    $.each(d.det, function (key, value) {
        html += '<tr>'
        html += '<td>' + value.prod.name + '</td>'
        html += '<td>' + value.price + '</td>'
        html += '<td>' + value.cant + '</td>'
        html += '<td>' + value.subtotal + '</td>'
        html += '</tr>'
    });
    html += '</tbody>';

    return html;
}

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

        tblSale = $('#data').DataTable({
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
                /*{
                    "className": 'details-control',
                    "orderable": false,
                    "data": null,
                    "defaultContent": ''
                },*/
                {"data": "id"},
                {"data": "cli"},
                {"data": "date_joined"},
                {"data": "subtotal"},
                {"data": "iva"},
                {"data": "total"},
                {"data": "id"},
            ],
            columnDefs: [
                {
                    targets: [-2, -3, -4],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        var buttons = '<a href="/erp/sale/delete/' + row.id + '/" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a> ';
                        buttons += '<a href="/erp/sale/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat" style="color: white;"><i class="fas fa-edit"></i></a> ';
                        buttons += '<a rel="details" class="btn btn-primary btn-xs btn-flat" style="color: white;"><i class="fas fa-shopping-cart"></i> <span class="badge badge-danger">' + row.det.length + '</span></a> ';
                        return buttons;
                    }
                },
                {
                    targets: [-6],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        var buttons = '<p>' + data.names + ' ' + data.surnames + ' <b>|</b> <span class="badge badge-pill badge-secondary">' + data.dni + '</span></p>';
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
    /*
    tblSale = $('#data').DataTable({
        //responsive: true,
        scrollX: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchdata'
            },
            dataSrc: ""
        },
        columns: [
            {
                "className": 'details-control',
                "orderable": false,
                "data": null,
                "defaultContent": ''
            },
            {"data": "cli"},
            {"data": "date_joined"},
            {"data": "subtotal"},
            {"data": "iva"},
            {"data": "total"},
            {"data": "id"},
        ],
        columnDefs: [
            {
                targets: [-2, -3, -4],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '$' + parseFloat(data).toFixed(2);
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="/erp/sale/delete/' + row.id + '/" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a> ';
                    buttons += '<a href="/erp/sale/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat" style="color: white;"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a rel="details" class="btn btn-primary btn-xs btn-flat" style="color: white;"><i class="fas fa-shopping-cart"></i> <span class="badge badge-danger">' + row.det.length + '</span></a> ';
                    return buttons;
                }
            },
            {
                targets: [-6],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<p>' + data.names + ' ' + data.surnames + ' <b>|</b> <span class="badge badge-pill badge-secondary">' + data.dni + '</span></p>';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });*/

    // event details
    $('#data tbody')
        .on('click', 'a[rel="details"]', function () {

            //obtengo el objeto
            var tr = tblSale.cell($(this).closest('td, li')).index();
            var data = tblSale.row(tr.row).data();
            console.log(data);

            //datos del cliente
            document.getElementById("client_name").innerHTML = data.cli.names + " " + data.cli.surnames;
            document.getElementById("client_dni").innerHTML = '<strong>DNI: </strong>' + data.cli.dni;

            //datos de factura
            document.getElementById("invoice_number").innerHTML = '<strong>Factura #</strong>' + data.id;
            document.getElementById("date").innerHTML = 'FECHA: ' + data.date_joined;
            document.getElementById("subtotal").innerHTML = data.subtotal;
            document.getElementById("iva").innerHTML = data.iva;
            document.getElementById("total").innerHTML = data.total;

            //boton pdf
            document.getElementById("buttonPDF").innerHTML = '<a class="btn btn-primary float-right" href="/erp/sale/invoice/pdf/' + data.id + '/" target="_blank" style="margin-right: 5px;color: white;" ><i class="fas fa-download"></i>Generar PDF</a>';

            //tabla detalle
            var t = $('#tblDet').DataTable();
            t.clear(); //para no sobrescribir el modal limpio antes de llenar
            $.each(data.det, function (key, value) {
                t.row.add([value.prod.name, value.price, value.cant, value.subtotal]).draw(false);

            });

            $('#myModelDet').modal('show');
        })


    // pagination.js
    PaginationConstructor();
});