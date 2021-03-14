var pagination = {
    items: {
        totalPages_p: 1,// numero de paginas que tendra la consulta
        action_p: "",// action para la vista
        visiblePages_p: 3,// paginas visibles en la paginacion
        rows_number: 10, // select para visualizar el numero de filas
        search: "", // input para buscar
        start_page: 0,// numero del primer item de la pagina actual
        end_page: 0,// numero del ultimo item de la pagina actual
        count: 0,// total de items mostrados actualmente
    },
    create: function (rows_number, action) {
        this.items.rows_number = rows_number;
        this.items.action_p = action;
        // consultando el total de registros de la tabla
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: {
                //'action': this.items.action_p,
                'action': this.items.action_p,
                'start_page': this.items.start_page,
                'end_page': this.items.end_page,
                'search': this.items.search,
            },
            dataType: 'json',
        }).done(function (data) {
            // actualizamos la cuenta con el total de registros de la tabla
            pagination.items.count = data.count;

            // calculando el numero de paginas que tendra la navegacion
            if (data.count != 0) {
                // calculamos el numero de elementos maximos que tendra cada pagina
                data.count = data.count / pagination.items.rows_number;
                if (data.count % 1 != 0) {
                    // Es un numero decimal, es decir que la ultima pagina no estara llena
                    // tomamos el valor mayor mas proximo para obtener un entero
                    // Ej: Math.ceil(2.8) = 3
                    data.count = Math.ceil(data.count);
                }
            }
            // si la consulta no retorno valores, y no hay paginas
            if (data.count == 0) {
                //no se cree la paginacion
                $('#pagination').twbsPagination('destroy');
                //se vuelva a dibujar el datatable sin valores
                mytable.list('searchdatapagination', 0, 0);
            } else {
                //si ya existe, se destruye para que se vuelva a dibujar la navegacion
                $('#pagination').twbsPagination('destroy');
                //se define la paginacion
                $('#pagination').twbsPagination({
                    // oculta la navegacion si solo tiene una pagina
                    //hideOnlyOnePage: true,
                    // texto de la paginacion
                    first: 'Primero',
                    prev: '<',
                    next: '>',
                    last: 'Ultimo',
                    // se define la cantidad de items que tendra la navegacion
                    totalPages: data.count,
                    // numero de elementos que muestra la navegacion
                    visiblePages: 3,
                    // cuando se de click a un elemento de la navegacion se cargue la
                    // pagina seleccionada con sus registros.
                    onPageClick: function (event, page) {
                        // page nos devolvera el numero de la pagina que se selecciono
                        str = page;
                        end = page;
                        // pagina seleccionada * select de filas que mostrar
                        end = end * pagination.items.rows_number;
                        p = pagination.items.rows_number - 1
                        // fila final de la pagina menos el nro de filas a mostrar nos
                        // dara el valor inicial
                        str = end - p;
                        // la vista trabaja con valor inicial cero hasta el elemento final-1
                        str--;
                        // se llena la tabla con los registros desde el valor inicial de la pagina
                        // hasta el valor final de la pagina

                        mytable.list('searchdatapagination', str, end);
                    }
                }).on('page', function (event, page) {
                });
            }

        }).fail(function (jqXHR, textStatus, errorThrown) {
            alert(textStatus + ': ' + errorThrown);
        }).always(function (data) {
            // se actualice el numero de filas que se muestran
            $('input[name="total_rows_count"]').val(pagination.items.count);
        });

    },
}
// si se apreta el boton buscar
function Search() {
    // que no se busque si no hay nada en el input
    if ($('#id_srch').val().length != 0) {
        inputSearch = $('#id_srch').val();
        pagination.items.search = inputSearch;
        pagination.create(pagination.items.rows_number, 'getcount');
        $('input[name="total_rows_count"]').val(pagination.items.count);
    }else{
        alert("no hay datos para buscar");
    }
    $('#id_srch').focus();
    $('#id_srch').select();

}

// es un escuchador para que cuando este quitando letras del input y este quede vacio
// se restablesca el datatable
function SearchWithEmptyInput() {
    //sino hay valores en el input de busqueda
    if ($('#id_srch').val().length === 0) {
        //busqueda default de la tabla
        pagination.items.search = $('#id_srch').val();
        pagination.create(pagination.items.rows_number, 'getcount');
    }
}

function PaginationConstructor(){
    //select para escoger el numero de filas a mostrar
    $('#id_filter_rows').select2({
        theme: "bootstrap4",
        language: 'es',
        allowClear: false,
        //quitar la caja de texto del select2
        minimumResultsForSearch: -1,
        width: '100%',
    }).on('select2:select', function (e) {
        // actualizando el numero de filas a mostrar
        pagination.items.rows_number = parseInt(e.params.data['text']);
        pagination.create(pagination.items.rows_number, 'getcount');
    });
    // agregando elementos al select
    $('#id_filter_rows').append(new Option(10, 1, false, false)).trigger('change');
    $('#id_filter_rows').append(new Option(25, 2, false, false)).trigger('change');
    $('#id_filter_rows').append(new Option(50, 3, false, false)).trigger('change');
    $('#id_filter_rows').append(new Option(100, 4, false, false)).trigger('change');
    // agregando evento para validar si esta vacio el input de busqueda y rellenar el datatable
    document.getElementById("id_srch").addEventListener("input", SearchWithEmptyInput);
    // busqueda default de la tabla
    pagination.create(pagination.items.rows_number, 'getcount');
}
