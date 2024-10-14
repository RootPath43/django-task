$(document).ready(function() {
    const token = localStorage.getItem('authToken');
    var pk= window.location.href.split("/").at(-2);//bulunan objenin pk'si
$('#saveButton').click(function() {
    
    var aircraft= parseInt(document.getElementById("aircraftDropDown").value);
    
    $.ajax({
        url: `/api/dashboard/${pk}/`,
        type: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${token}` // Replace with your actual token
        },
        data: JSON.stringify({
            // Gönderilecek veri
            aircraft
        }),
        contentType: 'application/json',
        success: function(response) {
            alert("Success");
            window.location.href = '/dashboard/';
        },
        error: function(error) {
            alert("Fail");
            window.location.href =window.location.href;
        }
    });
});

// Delete button için DELETE isteği
$('#deleteButton').click(function() {
    
    $.ajax({
        url: `/api/dashboard/${pk}/`,
        type: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${token}` // Replace with your actual token
        },
        success: function(response) {
            alert("Success");
            window.location.href = '/dashboard/';
        },
        error: function(error) {
            alert("Fail");
            window.location.href =window.location.href;
        }
    });
});
});
