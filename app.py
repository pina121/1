import os
import sys
import traceback
import cv2
import numpy as np
from PIL import Image

def install_dependencies():
    """Install required dependencies"""
    os.system('pip install opencv-python-headless pillow numpy')

def remove_background_advanced(input_path, output_path=None):
    """
    Advanced background removal with multiple techniques
    
    Args:
        input_path (str): Path to input image
        output_path (str, optional): Path to save output image
    
    Returns:
        str: Path to output image or None if failed
    """
    # Ensure dependencies are installed
    install_dependencies()

    # Validate input file
    if not os.path.exists(input_path):
        print(f"Error: Input file {input_path} does not exist.")
        return None

    # Generate default output path if not provided
    if output_path is None:
        base, ext = os.path.splitext(input_path)
        output_path = f"{base}_nobg.png"

    try:
        # Read image
        image = cv2.imread(input_path)
        
        if image is None:
            print(f"Failed to read image: {input_path}")
            return None

        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply GaussianBlur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Use Otsu's thresholding
        _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
        # Find contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Create mask
        mask = np.zeros(gray.shape, np.uint8)
        
        # Draw contours on mask
        cv2.drawContours(mask, contours, -1, (255, 255, 255), -1)
        
        # Invert mask
        mask_inv = cv2.bitwise_not(mask)
        
        # Create transparent background
        b, g, r = cv2.split(image)
        rgba = [b, g, r, mask_inv]
        
        # Merge channels
        dst = cv2.merge(rgba, 4)
        
        # Save result
        cv2.imwrite(output_path, dst)
        
        print(f"Background removed successfully. Saved to {output_path}")
        return output_path

    except Exception as e:
        print(f"Background removal failed: {e}")
        traceback.print_exc()
        return None

def batch_remove_background(input_directory, output_directory=None):
    """
    Remove backgrounds from all images in a directory
    """
    # Validate input directory
    if not os.path.isdir(input_directory):
        print(f"Error: {input_directory} is not a valid directory.")
        return
    
    # Create output directory
    if output_directory is None:
        output_directory = os.path.join(input_directory, 'no_background')
    
    os.makedirs(output_directory, exist_ok=True)
    
    # Supported image extensions
    image_extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.webp']
    
    # Process images
    successful = 0
    failed = 0
    
    for filename in os.listdir(input_directory):
        # Check file extension
        if any(filename.lower().endswith(ext) for ext in image_extensions):
            input_path = os.path.join(input_directory, filename)
            
            # Generate output path
            base, ext = os.path.splitext(filename)
            output_path = os.path.join(output_directory, f"{base}_nobg.png")
            
            # Try to remove background
            result = remove_background_advanced(input_path, output_path)
            
            if result:
                successful += 1
            else:
                failed += 1
                print(f"Failed to process: {filename}")
    
    # Print summary
    print("\nBackground Removal Summary:")
    print(f"Total Images: {successful + failed}")
    print(f"Successfully Processed: {successful}")
    print(f"Failed: {failed}")

def main():
    """
    Main function to handle command-line usage
    """
    # Check arguments
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Single image: python script.py <input_image_path>")
        print("  Batch processing: python script.py batch <input_directory>")
        sys.exit(1)
    
    # Install dependencies
    install_dependencies()
    
    # Process based on arguments
    if sys.argv[1] == 'batch':
        if len(sys.argv) < 3:
            print("Please provide an input directory for batch processing.")
            sys.exit(1)
        batch_remove_background(sys.argv[2])
    else:
        # Process single image
        result = remove_background_advanced(sys.argv[1])
        if not result:
            print("Failed to remove background. Please check the image and try again.")
            sys.exit(1)

if __name__ == "__main__":
    main()

# Usage Examples:
# python script.py image.jpg
# python script.py batch /path/to/images/
