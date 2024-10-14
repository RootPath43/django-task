$(document).ready(function () {
    const token = localStorage.getItem('authToken');
    const addNewButton = document.getElementById('addButton');
    var table = null
    // AJAX isteği
    $.ajax({
        url: '/api/dashboard/', // API URL'nizi buraya ekleyin
        method: 'GET',
        dataType: 'json',
        headers: {
            'Authorization': `Token ${token}` // Replace with your actual token
        },
        success: function (data) {
            console.log(data)
            //gruba göre tablonun verilerini dolduruyoruz
            if (data.length == 0) {
                var columns = null
            } else if (data[0].produced_part_id) {
                var columns = [

                    { data: 'produced_part_id' },
                    { data: 'part.part_name' },
                    { data: 'is_used' },
                    { data: 'produced_time' },
                    { data: 'aircraft.aircraft_name' },
                    { data: 'producer.first_name' }
                ]
            } else {
                var columns = [
                    { data: 'product_id' },
                    { data: 'aircraft.aircraft_name' },
                    { data: 'produced_time' },
                    { data: 'producer.first_name' },
                ]
            }
            // DataTable'a veri eklemek için tabloyu başlatıyoruz
            table = $('#example').DataTable({
                data: data,
                columns: columns,

            });
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.error('AJAX request failed: ' + textStatus, errorThrown);
        }
    });
    $('#example tbody').on('click', 'tr', function () {
        var data = table.row(this).data();
        //tıklanan listenin idsine göre editleme sayfasına yönlendirme
        if (data.produced_part_id) {
            window.location.href = '/dashboard/' + data.produced_part_id;
        } else {
            window.location.href = '/dashboard/' + data.product_id;
        }
        // 
    });

    addNewButton.addEventListener("click", () => {
        console.log("clickelndi");
        window.location.href = '/dashboard/add/';
    });
});
