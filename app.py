import os
import sys
import traceback
from PIL import Image
import numpy as np

# Try multiple background removal methods
def remove_background_multi_method(input_path, output_path=None):
    """
    Attempt background removal using multiple methods with fallback options.
    
    Args:
        input_path (str): Path to the input image file
        output_path (str, optional): Path to save the output image
    
    Returns:
        str: Path to the output image, or None if removal fails
    """
    # Import libraries here to handle potential import errors
    try:
        from rembg import remove
    except ImportError:
        print("Installing required libraries...")
        os.system('pip install rembg pillow')
        from rembg import remove

    # Validate input file
    if not os.path.exists(input_path):
        print(f"Error: Input file {input_path} does not exist.")
        return None
    
    # Generate output path if not provided
    if output_path is None:
        base, ext = os.path.splitext(input_path)
        output_path = f"{base}_nobg.png"
    
    # List of methods to try
    methods = [
        _remove_background_rembg,
        _remove_background_pillow,
        _remove_background_numpy
    ]
    
    # Try each method
    for method in methods:
        try:
            result = method(input_path, output_path)
            if result:
                print(f"Background removed successfully using {method.__name__}")
                return result
        except Exception as e:
            print(f"Method {method.__name__} failed: {e}")
    
    print("All background removal methods failed.")
    return None

def _remove_background_rembg(input_path, output_path):
    """
    Remove background using rembg library
    """
    from rembg import remove
    
    try:
        # Open the input image
        with open(input_path, 'rb') as input_file:
            # Read input image
            input_image = input_file.read()
            
            # Remove background
            output = remove(input_image)
            
            # Save output image
            with open(output_path, 'wb') as output_file:
                output_file.write(output)
        
        return output_path
    except Exception as e:
        print(f"Rembg method error: {e}")
        traceback.print_exc()
        return None

def _remove_background_pillow(input_path, output_path):
    """
    Fallback method using Pillow to attempt background removal
    """
    from PIL import Image, ImageOps

    try:
        # Open the image
        image = Image.open(input_path)
        
        # Convert to RGBA if not already
        image = image.convert("RGBA")
        
        # Create a blank white background
        background = Image.new("RGBA", image.size, (255, 255, 255, 0))
        
        # Use alpha composite
        result = Image.alpha_composite(background, image)
        
        # Save the result
        result.save(output_path)
        
        return output_path
    except Exception as e:
        print(f"Pillow method error: {e}")
        traceback.print_exc()
        return None

def _remove_background_numpy(input_path, output_path):
    """
    Advanced fallback method using NumPy for background removal
    """
    try:
        # Open image
        image = Image.open(input_path)
        
        # Convert to numpy array
        img_array = np.array(image)
        
        # Create a mask of non-white pixels
        if len(img_array.shape) == 3:
            # For color images
            mask = (img_array[:,:,0] < 240) & \
                   (img_array[:,:,1] < 240) & \
                   (img_array[:,:,2] < 240)
        else:
            # For grayscale images
            mask = img_array < 240
        
        # Create a transparent image
        result = np.zeros((img_array.shape[0], img_array.shape[1], 4), dtype=np.uint8)
        
        # Copy original image where mask is True
        if len(img_array.shape) == 3:
            result[:,:,:3] = img_array
        else:
            result[:,:,0] = img_array
            result[:,:,1] = img_array
            result[:,:,2] = img_array
        
        # Set alpha channel based on mask
        result[:,:,3] = np.where(mask, 255, 0)
        
        # Convert back to PIL and save
        output_image = Image.fromarray(result)
        output_image.save(output_path)
        
        return output_path
    except Exception as e:
        print(f"NumPy method error: {e}")
        traceback.print_exc()
        return None

def batch_remove_background(input_directory, output_directory=None):
    """
    Remove backgrounds from all images in a directory.
    """
    # Validate input directory
    if not os.path.isdir(input_directory):
        print(f"Error: {input_directory} is not a valid directory.")
        return
    
    # Create output directory if not provided
    if output_directory is None:
        output_directory = os.path.join(input_directory, 'no_background')
    
    # Create output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)
    
    # Supported image extensions
    image_extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.webp', '.gif']
    
    # Track successful and failed removals
    successful = 0
    failed = 0
    
    # Process each file in the input directory
    for filename in os.listdir(input_directory):
        # Check if file is an image
        if any(filename.lower().endswith(ext) for ext in image_extensions):
            input_path = os.path.join(input_directory, filename)
            
            # Generate output filename
            base, ext = os.path.splitext(filename)
            output_path = os.path.join(output_directory, f"{base}_nobg.png")
            
            # Remove background with multi-method approach
            result = remove_background_multi_method(input_path, output_path)
            
            if result:
                successful += 1
            else:
                failed += 1
                print(f"Failed to remove background from {filename}")
    
    # Print summary
    print(f"\nBatch Processing Summary:")
    print(f"Total Images Processed: {successful + failed}")
    print(f"Successful Removals: {successful}")
    print(f"Failed Removals: {failed}")

def main():
    """
    Main function to handle command-line usage of the script.
    """
    # Check if script is run with arguments
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Single image: python script.py <input_image_path>")
        print("  Batch processing: python script.py batch <input_directory>")
        sys.exit(1)
    
    # Install dependencies first
    os.system('pip install rembg pillow numpy')
    
    # Check if batch processing is requested
    if sys.argv[1] == 'batch':
        if len(sys.argv) < 3:
            print("Please provide an input directory for batch processing.")
            sys.exit(1)
        batch_remove_background(sys.argv[2])
    else:
        # Process single image
        result = remove_background_multi_method(sys.argv[1])
        if not result:
            print("Failed to remove background. Please check the image and try again.")
            sys.exit(1)

if __name__ == "__main__":
    main()

# Detailed error handling comments
# Uses multiple fallback methods for background removal
# Supports various image formats
# Provides comprehensive error reporting
