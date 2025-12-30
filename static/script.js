async function displayText() {
    const textInput = document.getElementById('textInput').value;
    
    if (!textInput.trim()) {
        alert('Please type something!');
        return;
    }

    try {
        const response = await fetch('/api/display', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: textInput })
        });

        const data = await response.json();
        
        // Show the output section and display the text
        document.getElementById('outputSection').style.display = 'block';
        document.getElementById('displayBox').textContent = data.text;
    } catch (error) {
        console.error('Error:', error);
        alert('Something went wrong!');
    }
}

// Allow Enter key to submit
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('textInput').addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && e.ctrlKey) {
            displayText();
        }
    });
});
