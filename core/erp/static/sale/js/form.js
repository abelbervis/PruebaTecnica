var tblProducts;
var porc_iva = 0.12;
var flag_init_update = true;
var pvp_ganancia = 0.20;

var vents = {
    items: {
        cli: '',
        date_joined: '',
        subtotal: 0.00,
        iva: 0.00,
        total: 0.00,
        products: []
    },
    calculate_invoice: function () {
        var subtotal = 0.00;

        var iva = $('input[name="iva"]').val();

        //recorro el arreglo y actualizo los valores
        $.each(this.items.products, function (pos, dict) {
            dict.pos = pos;
            //dict.pvp = parseFloat(dict.cost)+parseFloat(dict.cost)*pvp_ganancia;
            /* -------------------------------------------------------------------------*/
            //dict.pvp = dict.price;
            dict.subtotal = dict.cant * parseFloat(dict.pvp);
            dict.impuesto = dict.subtotal * iva;
            dict.total = dict.subtotal+dict.impuesto;
            subtotal += dict.subtotal;
        });

        this.items.subtotal = subtotal;

        this.items.iva = this.items.subtotal * iva;

        if ($('input[name="action"]').val() === "edit") {
            if (flag_init_update === true) {
                porc_iva = iva / this.items.subtotal;
                this.items.iva = this.items.subtotal * porc_iva;

            }
        }

        this.items.total = this.items.subtotal + this.items.iva;

        $('input[name="subtotal"]').val(this.items.subtotal.toFixed(2));
        $('input[name="ivacalc"]').val(this.items.iva.toFixed(2));
        $('input[name="total"]').val(this.items.total.toFixed(2));

        flag_init_update = false;

    },
    add: function (item) {
        //unshift agrega los elementos al inicio
        this.items.products.unshift(item);
        this.list();

    },
    list: function () {
        //calcula factura
        this.calculate_invoice();
        //llena el detalle
        tblProducts = $('#tblProducts').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            data: this.items.products,
            //detalle producto
            columns: [
                {"data": "id"},
                // diccionario de producto
                {"data": {"data": "name", "data":"image"}},
                {"data": "pvp"},
                {"data": "cant"},
                {"data": "subtotal"},
                {"data": "impuesto"},
                {"data": "total"},
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',

                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn btn-danger btn-xs btn-flat" style="color: white;"><i class="fas fa-trash-alt"></i></a>';
                    }
                },
                {
                    targets: [-3,-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-4],
                    class: 'text-center',
                    width: '100px',
                    orderable: false,
                    render: function (data, type, row) {
                        //<img src="'+data.+'" alt="Product 1" class="img-circle img-size-32 mr-2">
                        return '<input type="text" name="cant" class="form-control form-control-sm input-sm"  autocomplete="off" value="' + row.cant + '">';
                    }
                },
                {
                    targets: [-5],
                    class: 'text-center',
                    width: '100px',
                    orderable: false,
                    render: function (data, type, row) {
                        //return '<input type="text" name="pvp" class="form-control form-control-sm input-sm"  autocomplete="off" value="' + row.pvp + '">';
                        return '$' + parseFloat(row.pvp).toFixed(2);
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-6],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return data.name;
                    }
                },
            ],
            rowCallback(row, data, displayNum, displayIndex, dataIndex) {
                //console.log("rowCallback");
                //console.log(data);

                $(row).find('input[name="cant"]').TouchSpin({
                    min: 1,
                    max: 1000000000,
                    step: 1
                });
                /*
                $(row).find('input[name="pvp"]').TouchSpin({

                    //min: parseFloat(data.cost)+parseFloat(data.cost)*pvp_ganancia,//no se puede bajar de la ganancia
                    min: data.price,
                    max: 1000000000,
                    step: 1,
                });*/

            },
            initComplete: function (settings, json) {

            }
        });
    },
};

// formatos select
function formatoSelectProduct(item) {
    if (item.loading) {
        return item.item;
    }

    var option = $(
        '<div class="wrapper container">' +

        '<b>Nombre:</b> ' + item.name + '<br>' +
        '<b>Descripcion:</b> ' + item.description + '<br>' +
        '<b>Precio:</b> <span class="badge badge-warning">$' + item.pvp + '</span>' +

        '</div>');

    return option;
}
function formatoSelectClient(item) {
    if (item.loading) {
        return item.text;
    }

    var option = $(
        '<div class="wrapper container">' +

        '<b>Nombres:</b> ' + item.names + ' | <b>Apellidos:</b> ' + item.surnames + ' | ' +
        '<b>Dni:</b> ' + item.dni + '<br>' +

        '</div>');

    return option;
}

$(function () {

    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
    });
    $('#date_joined').datetimepicker({
        format: 'YYYY-MM-DD',
        date: moment().format("YYYY-MM-DD"),
        locale: 'es',
        //minDate: moment().format("YYYY-MM-DD")
    });
    $('#date_birthday').datetimepicker({
        format: 'YYYY-MM-DD',
        date: moment().format("YYYY-MM-DD"),
        locale: 'es',
        //minDate: moment().format("YYYY-MM-DD")
    });
    $("input[name='iva']").TouchSpin({
        min: 0,
        max: 100,
        step: 0.01,
        decimals: 2,
        maxboostedstep: 10,
        postfix: '%'
    }).on('change', function () {
        //para que al cambiar el iva me calcule todo de nuevo
        vents.items.iva = parseFloat($(this).val());
        vents.list();
    }).val(porc_iva.toFixed(2));
    vents.list();//si
    $('.btnRemoveAll').on('click', function () {
        if (vents.items.products.length === 0) return false;
        alert_action('Notificación', '¿Estas seguro de eliminar los ('+vents.items.products.length+') productos del detalle?', function () {
            vents.items.products = [];
            vents.list();
        }, function () {

        });
    });
    $('.btnAddClient').on('click', function () {
        $('#myModalClient').modal('show');
    });
    $('.btnAddProduct').on('click', function () {
        $('#myModalProduct').modal('show');
    });
    $('.btnClearSearch').on('click', function () {
        $('input[name="search"]').val('').focus();
    });

    // limpiando los modales
    $('#myModalClient').on('hidden.bs.modal', function () {
        $('#frmClient').trigger('reset');
    });
    $('#myModalProduct').on('hidden.bs.modal', function () {
        $('#frmProduct').trigger('reset');
    });

    // search products usando select2
    $('select[name="search"]').select2({
        theme: "bootstrap4",
        language: 'es',
        allowClear: true,
        ajax: {
            delay: 250,
            type: 'POST',
            url: window.location.pathname,
            data: function (params) {
                var queryParameters = {
                    term: params.term,
                    action: 'search_products'
                }
                return queryParameters;
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Ingrese el codigo o nombre del producto',
        minimumInputLength: 1,
        templateResult: formatoSelectProduct,
    }).on('select2:select', function (e) {
        // evento cuando se selecciona un elemento
        // recuperando la data del select
        var data = e.params.data;
        //var iva = $('input[name="iva"]').val();

        data.cant = 1;
        data.subtotal = 0.00;
        data.total = 0.00;
        data.impuesto = 0.00;
        vents.add(data);

        //limpiando select
        $(this).val('').trigger('change.select2');
        $(this).select2('open');
    });

    // event cant
    $('#tblProducts tbody')
        .on('click', 'a[rel="remove"]', function () {
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            alert_action('Notificación', '¿Estas seguro de eliminar <b>'+vents.items.products[tr.row].name+'</b>  del detalle?', function () {
                vents.items.products.splice(tr.row, 1);
                vents.list();
            }, function () {

            });
        })
        .on('change', 'input[name="cant"]', function () {
            console.clear();
            var cant = parseInt($(this).val());
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            vents.items.products[tr.row].cant = cant;
            vents.calculate_invoice();
            $('td:eq(4)', tblProducts.row(tr.row).node()).html('$' + vents.items.products[tr.row].subtotal.toFixed(2));
            $('td:eq(5)', tblProducts.row(tr.row).node()).html('$' + vents.items.products[tr.row].impuesto.toFixed(2));
            $('td:eq(6)', tblProducts.row(tr.row).node()).html('$' + vents.items.products[tr.row].total.toFixed(2));
        })
        /*
        .on('change', 'input[name="pvp"]', function () {
            var price = parseFloat($(this).val());
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            vents.items.products[tr.row].price = price;
            vents.calculate_invoice();
            $('td:eq(5)', tblProducts.row(tr.row).node()).html('$' + vents.items.products[tr.row].subtotal.toFixed(2));
            $('td:eq(6)', tblProducts.row(tr.row).node()).html('$' + vents.items.products[tr.row].impuesto.toFixed(2));
            $('td:eq(7)', tblProducts.row(tr.row).node()).html('$' + vents.items.products[tr.row].total.toFixed(2));
        })*/
    ;



    // event submit
    $('#frmSale').on('submit', function (e) {
        e.preventDefault();

        if (vents.items.products.length === 0) {
            message_error('Debe al menos tener un item en su detalle de venta');
            return false;
        }

        vents.items.date_joined = $('input[name="date_joined"]').val();
        vents.items.cli = $('select[name="cli"]').val();
        var parameters = new FormData();
        parameters.append('action', $('input[name="action"]').val());
        parameters.append('vents', JSON.stringify(vents.items));
        submit_with_ajax(window.location.pathname, 'Notificación',
            '¿Estas seguro de realizar la siguiente acción?', parameters, function (response) {

                alert_action('Notificacion', 'Desea imprimir la factura de la Venta?', function () {
                    window.open('/erp/sale/invoice/pdf/' + response.id + '/', '_blank');
                    location.href = '/erp/sale/list/';
                }, function () {
                    location.href = '/erp/sale/list/';
                })
            });
    });

    //formularios para nuevo registro
    $('#frmClient').on('submit', function (e) {
        e.preventDefault();

        var parameters = new FormData(this);
        parameters.append('action', 'create_client');
        submit_with_ajax(window.location.pathname, 'Notificación',
            '¿Estas seguro de crear al nuevo cliente?', parameters, function (response) {
                //console.log(response);
                var newOption = new Option(response.names, response.id, false, true);
                $('select[name="cli"]').append(newOption).trigger('change');
                Swal.fire(
                    'Agregado!',
                    'cliente agregado con exito!',
                    'success'
                )
                $('#myModalClient').modal('hide');
            });
    });
    $('#frmProduct').on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData(this); //obtengo los valores del formulario
        parameters.append('action', 'create_product');
        submit_with_ajax(window.location.pathname, 'Notificación',
            '¿Estas seguro de crear el nuevo producto?', parameters, function (response) {
                var newOption = new Option(response.name, response.id, false, true);
                //agrego el nuevo producto al select y lo selecciono
                $('select[name="search"]').append(newOption).trigger('change');
                // agrego el producto seleccionado a la lista detalle
                response.cant = 1;
                response.subtotal = 0.00;
                vents.add(response);
                //mensaje
                Swal.fire(
                    'Agregado!',
                    'el producto ' + response.name + 'agregado con exito!',
                    'success'
                )
                //limpio el select
                $('select[name="search"]').val('').trigger('change.select2');
                //cierro el formulario
                $('#myModalProduct').modal('hide');
            });
    });

    //para cliente
    $('select[name="cli"]').select2({
        theme: "bootstrap4",
        language: 'es',
        allowClear: true,
        ajax: {
            delay: 250,
            type: 'POST',
            url: window.location.pathname,
            data: function (params) {
                var queryParameters = {
                    term: params.term,
                    action: 'search_clients'
                }
                return queryParameters;
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Ingrese el nombre, apellido o dni',
        minimumInputLength: 1,
        templateResult: formatoSelectClient,
    });

    $(document).ready(function () {
        $('[data-toggle="tooltip"]').tooltip();
    });

});