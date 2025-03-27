document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const uploadArea = document.getElementById('upload-area');
    const fileInput = document.getElementById('file-input');
    const selectBtn = document.getElementById('select-btn');
    const loadingElement = document.getElementById('loading');
    const previewContainer = document.getElementById('preview-container');
    const originalPreview = document.getElementById('original-preview');
    const resultPreview = document.getElementById('result-preview');
    const downloadBtn = document.getElementById('download-btn');
    const newImageBtn = document.getElementById('new-image-btn');
    
    // Event Listeners
    uploadArea.addEventListener('click', function() {
        fileInput.click();
    });
    
    selectBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        fileInput.click();
    });
    
    // Drag and drop functionality
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        uploadArea.addEventListener(eventName, preventDefaults, false);
    });
    
    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    ['dragenter', 'dragover'].forEach(eventName => {
        uploadArea.addEventListener(eventName, highlight, false);
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
        uploadArea.addEventListener(eventName, unhighlight, false);
    });
    
    function highlight() {
        uploadArea.classList.add('highlight');
    }
    
    function unhighlight() {
        uploadArea.classList.remove('highlight');
    }
    
    uploadArea.addEventListener('drop', handleDrop, false);
    
    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        if (files.length) {
            handleFiles(files);
        }
    }
    
    fileInput.addEventListener('change', function() {
        if (fileInput.files.length) {
            handleFiles(fileInput.files);
        }
    });
    
    function handleFiles(files) {
        const file = files[0];
        if (!file.type.match('image.*')) {
            alert('Please select an image file');
            return;
        }
        
        // Display original image
        const reader = new FileReader();
        reader.onload = function(e) {
            originalPreview.src = e.target.result;
            // Show loading and hide upload area
            uploadArea.classList.add('hidden');
            loadingElement.classList.remove('hidden');
            
            // Send image to backend for processing
            processImage(file);
        };
        reader.readAsDataURL(file);
    }
    
    function processImage(file) {
        const formData = new FormData();
        formData.append('image', file);
        
        // Send the image to our backend API
        fetch('/process-image', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                // Display the processed image
                resultPreview.src = data.image;
                
                // Hide loading and show preview
                loadingElement.classList.add('hidden');
                previewContainer.classList.remove('hidden');
                
                // Enable download button
                downloadBtn.disabled = false;
            } else {
                throw new Error(data.error || 'Unknown error occurred');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error processing image: ' + error.message);
            
            // Reset UI
            loadingElement.classList.add('hidden');
            uploadArea.classList.remove('hidden');
        });
    }
    
    // Download button functionality
    downloadBtn.addEventListener('click', function() {
        // Use the backend API to download the processed image
        fetch('/download-image', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                image: resultPreview.src
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.blob();
        })
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.download = 'background-removed.png';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            window.URL.revokeObjectURL(url);
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error downloading image: ' + error.message);
        });
    });
    
    // New image button functionality
    newImageBtn.addEventListener('click', function() {
        // Reset the UI
        uploadArea.classList.remove('hidden');
        previewContainer.classList.add('hidden');
        fileInput.value = '';
        originalPreview.src = '';
        resultPreview.src = '';
        downloadBtn.disabled = true;
    });
});
