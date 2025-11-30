document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('upload-form');
    const loading = document.getElementById('loading');
    const output = document.getElementById('output');
    const htmlOutput = document.getElementById('html-output');
    const cssOutput = document.getElementById('css-output');
    const jsOutput = document.getElementById('js-output');
    
    // --- New elements for custom file input ---
    const fileInput = document.getElementById('video-file');
    const fileNameDisplay = document.getElementById('file-name-display');

    // Listener to update the display when a file is selected
    fileInput.addEventListener('change', () => {
        if (fileInput.files.length > 0) {
            fileNameDisplay.textContent = `Selected: ${fileInput.files[0].name}`;
        } else {
            fileNameDisplay.textContent = 'No file selected.';
        }
    });
    // --- End New elements ---


    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        if (fileInput.files.length === 0) {
            alert('Please select a video file.');
            return;
        }

        // 1. Show loading, hide previous results
        output.classList.add('hidden');
        loading.classList.remove('hidden');

        const formData = new FormData();
        formData.append('videoFile', fileInput.files[0]);

        try {
            // 2. Send video file to Flask backend
            const response = await fetch('/generate-code', {
                method: 'POST',
                body: formData,
            });

            const result = await response.json();

            // 3. Handle response
            if (result.success) {
                // Update the code output sections
                htmlOutput.textContent = result.html;
                cssOutput.textContent = result.css;
                jsOutput.textContent = result.js;
                
                // Show the output
                output.classList.remove('hidden');
            } else {
                alert('Code Generation Failed: ' + (result.error || 'An unknown error occurred.'));
            }

        } catch (error) {
            console.error('Error during code generation:', error);
            alert('Network or server error during generation. Check Flask console for details.');
        } finally {
            // 4. Hide loading screen
            loading.classList.add('hidden');
        }
    });
});