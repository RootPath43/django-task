$(document).ready(function() {
    const token = localStorage.getItem('authToken');
   
$('#saveButton').click(function() {
    
    var aircraft= parseInt(document.getElementById("aircraftDropDown").value);
    
    $.ajax({
        url: `/api/dashboard/`,
        type: 'POST',
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
            alert(response.message);
            window.location.href = '/dashboard/';
        },
        error: function(xhr) {
            const response = JSON.parse(xhr.responseText); 
            alert(response.message);
            window.location.href =window.location.href;
        }
    });
});


});
