"""This code converts a file into a sequence of images, where each image contains a portion of the file's binary data. Each image includes a header with metadata (File ID and Sequence Number)."""

import os
import logging
from PIL import Image

logging.basicConfig(level=logging.INFO)

IMAGE_SIZE = 2048  # 2048x2048 image
BYTES_PER_IMAGE = IMAGE_SIZE * IMAGE_SIZE  # 4,194,304 bytes

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

def generate_header(file_id, sequence_number):
    """
    Generate a header containing the file ID and sequence number.
    Header structure:
    - File ID: 64 bits
    - Sequence Number: 32 bits
    """
    header = []
    file_id_bits = [int(bit) for bit in f'{file_id:064b}']
    sequence_number_bits = [int(bit) for bit in f'{sequence_number:032b}']
    header.extend(file_id_bits)
    header.extend(sequence_number_bits)
    return header

def save_bits_as_image(bits_chunk, image_path, file_id, sequence_number):
    # Generate the header
    header = generate_header(file_id, sequence_number)
    bits_chunk = header + bits_chunk  # Prepend the header to the data

    img = Image.new('L', (IMAGE_SIZE, IMAGE_SIZE))
    pixels = img.load()

    bit_index = 0
    for y in range(IMAGE_SIZE):
        for x in range(IMAGE_SIZE):
            if bit_index < len(bits_chunk):
                byte_bits = bits_chunk[bit_index:bit_index+8]
                if len(byte_bits) < 8:
                    byte_bits += [0] * (8 - len(byte_bits))

                byte_val = 0
                for bit in byte_bits:
                    byte_val = (byte_val << 1) | bit

                pixels[x, y] = byte_val
                bit_index += 8
            else:
                # Fill remaining pixels with zero if bits_chunk is exhausted
                pixels[x, y] = 0

    img.save(image_path, format='PNG')

def split_bits_to_images(bits, output_folder):
    bits_per_image = BYTES_PER_IMAGE * 8 - 96  # Reserve 96 bits for the header
    total_images = (len(bits) + bits_per_image - 1) // bits_per_image

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Generate a unique file ID (e.g., hash of the output folder name)
    file_id = abs(hash(output_folder)) % (2**64)

    for i in range(total_images):
        start = i * bits_per_image
        end = start + bits_per_image
        chunk = bits[start:end]

        # Pad the last chunk with zeros if it's smaller than bits_per_image
        if len(chunk) < bits_per_image:
            chunk += [0] * (bits_per_image - len(chunk))

        print(f"[DEBUG] Creating image {i+1}/{total_images} with {len(chunk)} bits")
        image_path = os.path.join(output_folder, f"f{i+1}.png")
        save_bits_as_image(chunk, image_path, file_id, i + 1)

def main():
    # Hardcoded paths for input file and output folder
    input_file = r"C:\Users\jhjos\OneDrive\Desktop\YoutubeVault\ipfiles\nodev22140x64.msi"
    output_base_folder = r"C:\Users\jhjos\OneDrive\Desktop\YoutubeVault\opfiles"

    if not os.path.exists(input_file):
        print(f"[ERROR] Input file '{input_file}' does not exist.")
        return

    filename_only = os.path.splitext(os.path.basename(input_file))[0]
    output_folder = os.path.join(output_base_folder, f"{filename_only}_sequence")

    bits = file_to_bits_with_metadata(input_file)
    split_bits_to_images(bits, output_folder)

    logging.info(f"File converted to image sequence in folder:\n{output_folder}")

if __name__ == "__main__":
    main()