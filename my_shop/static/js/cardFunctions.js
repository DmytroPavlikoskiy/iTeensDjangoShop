// document.addEventListener('click', function(e) {
//     if (e.target.classList.contains('add-to-cart-btn')) {
//         e.preventDefault();
//         const btn = e.target;
//         const url = btn.getAttribute('data-url');

//         fetch(url, {
//             method: 'POST',
//             headers: { 
//                 'X-Requested-With': 'XMLHttpRequest', 
//                 'X-CSRFToken': '{{ csrf_token }}' 
//             }
//         })
//         .then(res => {
//             if (!res.ok) throw new Error('Network response was not ok');
//             return res.json();
//         })
//         .then(data => {
//             if (data.success) {
//                 // Оновлюємо значок кошика
//                 const badge = document.getElementById('cart-count');
//                 if (badge) {
//                     badge.innerText = data.cart_total_items;
//                 }

//                 // Візуальний фідбек на кнопці
//                 const originalText = btn.innerText;
//                 btn.innerText = 'ДОДАНО!';
//                 btn.style.background = '#2ecc71';
//                 btn.disabled = true; // Захист від подвійного кліку

//                 setTimeout(() => { 
//                     btn.innerText = originalText; 
//                     btn.style.background = ''; 
//                     btn.disabled = false;
//                 }, 2000);
//             }
//         })
//         .catch(error => {
//             console.error('Error:', error);
//             alert('Помилка при додаванні в кошик');
//         });
//     }
// });

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function addToCart(event, btn) {
    event.preventDefault(); // Зупиняємо перехід по посиланню (якщо кнопка в <a>)
    
    const url = btn.getAttribute('data-url');
    const badge = document.getElementById('cart-count');

    // Блокуємо кнопку від повторних натискань до завершення запиту
    btn.style.pointerEvents = 'none';

    fetch(url, {
        method: 'POST',
        headers: { 
            'X-Requested-With': 'XMLHttpRequest', 
            'X-CSRFToken': '{{ csrf_token }}' 
        }
    })
    .then(res => {
        if (!res.ok) throw new Error('Network error');
        return res.json();
    })
    .then(data => {
        if (data.success) {
            // Оновлюємо кількість у кошику
            if (badge) badge.innerText = data.cart_total_items;

            // Фідбек на кнопці
            const originalText = btn.innerText;
            btn.innerText = 'ДОДАНО!';
            btn.style.background = '#2ecc71';

            setTimeout(() => { 
                btn.innerText = originalText; 
                btn.style.background = ''; 
                btn.style.pointerEvents = 'auto'; // Повертаємо можливість кліку
            }, 2000);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        btn.style.pointerEvents = 'auto';
        alert('Помилка при додаванні');
    });
}



function addToCartWithQty(event, btn) {
    event.preventDefault();
    
    const url = btn.getAttribute('data-url');
    const productId = btn.getAttribute('data-product-id');
    const badge = document.getElementById('cart-count');
    const qtyInput = document.getElementById(`product-qty-${productId}`);
    const quantity = qtyInput ? qtyInput.value : 1;

    btn.style.pointerEvents = 'none';

    fetch(url, {
        method: 'POST',
        headers: { 
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest', 
            // Замість {{ csrf_token }} використовуємо функцію:
            'X-CSRFToken': getCookie('csrftoken') 
        },
        body: JSON.stringify({
            'quantity': parseInt(quantity)
        })
    })
    .then(res => {
        if (!res.ok) throw new Error('Network error');
        return res.json();
    })
    .then(data => {
        if (data.success) {
            if (badge) badge.innerText = data.cart_total_items;
            const originalText = btn.innerText;
            btn.innerText = 'ДОДАНО!';
            btn.style.background = '#2ecc71';
            setTimeout(() => { 
                btn.innerText = originalText; 
                btn.style.background = ''; 
                btn.style.pointerEvents = 'auto'; 
            }, 2000);
        } else {
            alert(data.message); // Виведемо повідомлення про від'ємне число, якщо воно прийде
            btn.style.pointerEvents = 'auto';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        btn.style.pointerEvents = 'auto';
        alert('Помилка при додаванні');
    });
}