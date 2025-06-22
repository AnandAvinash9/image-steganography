from PIL import Image
import numpy as np

def text_to_binary(text):
    """Convert string to binary representation"""
    return ''.join(format(ord(char), '08b') for char in text)

def binary_to_text(binary):
    """Convert binary string back to text"""
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    return ''.join([chr(int(b, 2)) for b in chars])

def encode_image(img, message):
    """Hide message in image using LSB steganography"""
    img = img.convert('RGB')
    np_img = np.array(img)

    # Use a more reliable 16-bit delimiter (0xFFFF)
    binary_message = text_to_binary(message) + '1111111111111111'  # New delimiter
    binary_index = 0

    for row in np_img:
        for pixel in row:
            for channel in range(3):  # R, G, B channels
                if binary_index < len(binary_message):
                    pixel[channel] = (int(pixel[channel]) & 0b11111110) | int(binary_message[binary_index])
                    binary_index += 1

    if binary_index < len(binary_message):
        raise ValueError("Message too long for this image.")

    return Image.fromarray(np_img)

def decode_image(img):
    """Extract hidden message from image"""
    img = img.convert('RGB')
    np_img = np.array(img)

    binary_data = ''
    for row in np_img:
        for pixel in row:
            for channel in range(3):
                binary_data += str(pixel[channel] & 1)

    # Look for our 16-bit delimiter (0xFFFF)
    delimiter_index = binary_data.find('1111111111111111')
    
    if delimiter_index == -1:
        return "No message found or invalid format"
    
    message_bits = binary_data[:delimiter_index]
    
    # Convert binary to text
    chars = [message_bits[i:i+8] for i in range(0, len(message_bits), 8)]
    try:
        return ''.join([chr(int(b, 2)) for b in chars if len(b) == 8])
    except:
        return "Error decoding message"