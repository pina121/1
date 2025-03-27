import os
import sys
from rembg import remove
from PIL import Image

def remove_background(input_path, output_path=None):
    """
    Remove background from an image using rembg library.
    
    Args:
        input_path (str): Path to the input image file
        output_path (str, optional): Path to save the output image. 
                                     If not provided, creates a default output path.
    """
    # Validate input file
    if not os.path.exists(input_path):
        print(f"Error: Input file {input_path} does not exist.")
        return None
    
    # Generate output path if not provided
    if output_path is None:
        # Create output filename based on input filename
        base, ext = os.path.splitext(input_path)
        output_path = f"{base}_nobg{ext}"
    
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
        
        print(f"Background removed successfully. Saved to {output_path}")
        return output_path
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def batch_remove_background(input_directory, output_directory=None):
    """
    Remove backgrounds from all images in a directory.
    
    Args:
        input_directory (str): Path to directory containing input images
        output_directory (str, optional): Path to save output images. 
                                          If not provided, creates a subdirectory in input directory.
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
    image_extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.webp']
    
    # Process each file in the input directory
    for filename in os.listdir(input_directory):
        # Check if file is an image
        if any(filename.lower().endswith(ext) for ext in image_extensions):
            input_path = os.path.join(input_directory, filename)
            
            # Generate output filename
            base, ext = os.path.splitext(filename)
            output_path = os.path.join(output_directory, f"{base}_nobg{ext}")
            
            # Remove background for this image
            remove_background(input_path, output_path)

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
    
    # Check if batch processing is requested
    if sys.argv[1] == 'batch':
        if len(sys.argv) < 3:
            print("Please provide an input directory for batch processing.")
            sys.exit(1)
        batch_remove_background(sys.argv[2])
    else:
        # Process single image
        remove_background(sys.argv[1])

if __name__ == "__main__":
    main()

# Example usage:
# python script.py image.jpg                  # Remove background from a single image
# python script.py batch /path/to/images/     # Remove background from all images in a directory
