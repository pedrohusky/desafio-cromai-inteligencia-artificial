import os
import shutil
import cv2
import numpy as np
from tqdm import tqdm

# Define some constants for better readability and maintainability

# The path of the input folder with images to be processed
INPUT_FOLDER = "./case_segmentacao/inputs"

# The path of the output folder where the segmented images will be saved
OUTPUT_FOLDER = "outputs"

# The lower bound for green colors in HSV format
LOWER_GREEN_COLOR = np.array([19, 35, 35])  # Adjust the hue value for green

# The upper bound for green colors in HSV format
UPPER_GREEN_COLOR = np.array([90, 255, 255])  # Adjust the hue value for green

# The background color to be used for the segmented image in BGR format
BACKGROUND_COLOR = [0, 0, 0]

def create_output_folder(output_folder):
    """Create the output folder if it does not exist, or clear it if it does."""
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.makedirs(output_folder, exist_ok=True)

def find_green_pixels(input_image):
    """Find all green pixels in the input image and return a mask with them."""

    # Convert the image to the HSV color space
    hsv_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2HSV)

    # Create a mask to filter out green colors
    green_mask = cv2.inRange(hsv_image, LOWER_GREEN_COLOR, UPPER_GREEN_COLOR)

    return green_mask

def segment_green_pixels(input_path, output_path):
    """Segment the green pixels in the input image and save the result in the output path."""

    # Load the input image
    input_image = cv2.imread(input_path)

    # Find green pixels
    green_mask = find_green_pixels(input_image)

    # Apply the mask to the original image to get the segmented image
    segmented_image = input_image.copy()
    segmented_image[green_mask == 0] = BACKGROUND_COLOR

    # Save the segmented image
    result_image = np.hstack((input_image, segmented_image))  # Concatenate side by side
    cv2.imwrite(output_path, result_image)

def main():
    """Process all images in the input folder and save them in the output folder."""

    create_output_folder(OUTPUT_FOLDER)

    # Process all images in the input folder
    for image_file in tqdm(os.listdir(INPUT_FOLDER)):
        input_path = os.path.join(INPUT_FOLDER, image_file)
        output_path = os.path.join(OUTPUT_FOLDER, image_file)
        segment_green_pixels(input_path, output_path)

    print("Processamento concluído. Imagens segmentadas salvas na pasta 'outputs' lado a lado com as imagens originais.")

if __name__ == "__main__":
    main()
