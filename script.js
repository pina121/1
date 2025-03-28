// Initialize the background remover
const bgRemoval = await backgroundRemoval.createBackgroundRemoval();

document.getElementById('imageInput').addEventListener('change', async function(e) {
    const file = e.target.files[0];
    if (!file) return;
    
    const reader = new FileReader();
    reader.onload = async function(event) {
        const originalImage = document.getElementById('originalImage');
        originalImage.src = event.target.result;
        originalImage.style.display = 'block';
        
        // Show loading state
        document.getElementById('resultImage').src = '';
        document.getElementById('downloadBtn').disabled = true;
        
        try {
            // Process with background removal
            const imageBlob = await bgRemoval.removeBackground(file);
            const resultUrl = URL.createObjectURL(imageBlob);
            
            document.getElementById('resultImage').src = resultUrl;
            document.getElementById('downloadBtn').disabled = false;
        } catch (error) {
            console.error("Background removal failed:", error);
            alert("Background removal failed. Please try another image.");
        }
    };
    reader.readAsDataURL(file);
});

// Rest of your download button code remains the same
