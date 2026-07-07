document.addEventListener('DOMContentLoaded', function() {
    const greetBtn = document.getElementById('greetBtn');
    const moodSelect = document.getElementById('mood');
    const resultBox = document.getElementById('result');

    if (!greetBtn || !resultBox) return;

    // API endpoint for greeting
    const API_URL = '/api/greeting';

    greetBtn.addEventListener('click', async function() {
        const mood = moodSelect.value;
        
        try {
            let response;
            
            if (mood) {
                // Make API call with mood parameter
                response = await fetch(`${API_URL}?mood=${encodeURIComponent(mood)}`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });
            } else {
                // Call without mood for default greeting
                response = await fetch(API_URL, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });
            }

            if (!response.ok) {
                throw new Error('API call failed');
            }

            const data = await response.json();
            
            // Display result with animation
            showResult(data.message, true);
            
        } catch (error) {
            console.error('Error:', error);
            showResult('Fehler beim Abrufen der Begrüßung. Bitte versuchen Sie es erneut.', false);
        }
    });

    function showResult(message, isSuccess) {
        resultBox.textContent = message;
        
        // Reset classes and add appropriate one
        resultBox.className = 'result-box';
        if (isSuccess) {
            resultBox.classList.add('success');
        } else {
            resultBox.classList.add('error');
        }

        // Add fade animation
        resultBox.style.opacity = '0';
        setTimeout(() => {
            resultBox.style.transition = 'opacity 0.3s ease';
            resultBox.style.opacity = '1';
        }, 10);
    }

    // Allow Enter key to trigger greeting
    moodSelect.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            greetBtn.click();
        }
    });
});
