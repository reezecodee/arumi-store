document.getElementById('transaction-form').addEventListener('submit', function(event) {
    event.preventDefault();  // Mencegah reload halaman

    // Ambil nilai input dari form
    const items = document.getElementById('items').value.split(',').map(item => item.trim());

    // Kirim data ke API Flask
    fetch('http://127.0.0.1:8000/recommend', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 'items': items })
    })
    .then(response => response.json())
    .then(data => {
        // Tampilkan rekomendasi
        const recommendationList = document.getElementById('recommendation-list');
        recommendationList.innerHTML = '';  // Bersihkan daftar rekomendasi

        if (data.recommendations.length > 0) {
            data.recommendations.forEach(recommendation => {
                const li = document.createElement('li');
                li.textContent = recommendation;
                recommendationList.appendChild(li);
            });
        } else {
            const li = document.createElement('li');
            li.textContent = 'Tidak ada rekomendasi berdasarkan item yang dimasukkan.';
            recommendationList.appendChild(li);
        }

        document.getElementById('recommendations').style.display = 'block';
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
