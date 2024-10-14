const submitButton= document.getElementById("loginButton");
submitButton.addEventListener("click",()=>{
    loginUser();
});

function loginUser() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    fetch('/api/login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken() // CSRF token ekliyoruz.
        },
        body: JSON.stringify({ username, password })
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            return response.json().then(data => { throw new Error(data.error); });
        }
    })
    .then(data => {
        alert('Login successful!');
        console.log('Token:', data.token);
        // Token'ı local storage'a veya cookie'ye kaydedebilirsin.
        localStorage.setItem('authToken', data.token);
        window.location.href = '/dashboard/'; // Başarılı giriş sonrası yönlendirme
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Invalid credentials, please try again.');
    });
}

function getCSRFToken() {
    const name = 'csrftoken';
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}
