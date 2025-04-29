"""This code converts a file into a sequence of images, where each image contains a portion of the file's binary data. The first 8 bytes of the first image store the size of the original file."""

import os
from PIL import Image

IMAGE_SIZE = 1024  # 1024x1024 image
BYTES_PER_IMAGE = IMAGE_SIZE * IMAGE_SIZE  # 1,048,576 bytes

def file_to_bits_with_metadata(filename):
    with open(filename, 'rb') as f:
        file_data = f.read()

    file_size = len(file_data)
    # 8 bytes = 64 bits
    size_bytes = file_size.to_bytes(8, byteorder='big')  
    full_data = size_bytes + file_data

    bits = []
    for byte in full_data:
        bits.extend([int(bit) for bit in f'{byte:08b}'])
    return bits

def save_bits_as_image(bits_chunk, image_path):
    img = Image.new('L', (IMAGE_SIZE, IMAGE_SIZE))
    pixels = img.load()

    bit_index = 0
    for y in range(IMAGE_SIZE):
        for x in range(IMAGE_SIZE):
            byte_bits = bits_chunk[bit_index:bit_index+8]
            if len(byte_bits) < 8:
                byte_bits += [0] * (8 - len(byte_bits))


            byte_val = 0
            for bit in byte_bits:
                byte_val = (byte_val << 1) | bit

            pixels[x, y] = byte_val
            bit_index += 8
            if bit_index >= len(bits_chunk):
                break
        if bit_index >= len(bits_chunk):
            break

    img.save(image_path, format='PNG')

def split_bits_to_images(bits, output_folder):
    bits_per_image = BYTES_PER_IMAGE * 8
    total_images = (len(bits) + bits_per_image - 1) // bits_per_image

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for i in range(total_images):
        start = i * bits_per_image
        end = start + bits_per_image
        chunk = bits[start:end]
        image_path = os.path.join(output_folder, f"f{i+1}.png")
        save_bits_as_image(chunk, image_path)

def main():
    input_file = r"/workspaces/pixify/input files/[Jurafsky,_Martin.]_Speech_and_Language_Processing.pdf"
    output_base_folder = r"/workspaces/pixify/intermediate files"

    filename_only = os.path.splitext(os.path.basename(input_file))[0]
    output_folder = os.path.join(output_base_folder, f"{filename_only}_sequence")

    bits = file_to_bits_with_metadata(input_file)
    split_bits_to_images(bits, output_folder)

    print(f"[SUCCESS] File converted to image sequence in folder:\n{output_folder}")

if __name__ == "__main__":
    main()
