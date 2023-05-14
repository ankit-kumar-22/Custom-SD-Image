import json
import base64

def save_base64_image(json_file):
    # Read the JSON file
    with open(json_file, 'r') as file:
        data = json.load(file)

    # Extract the base64-encoded image from the JSON data
    base64_image = data['output']['images'][0]

    # Decode the base64 image data
    image_data = base64.b64decode(base64_image)

    # Determine the file extension (assuming it's a PNG image)
    file_extension = '.png'

    # Save the image file
    with open('saved_image_1' + file_extension, 'wb') as file:
        file.write(image_data)

    print('Image saved successfully.')

# Example usage
json_file_path = 'test.json'
save_base64_image(json_file_path)
