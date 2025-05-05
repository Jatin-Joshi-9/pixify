"""This is the decoder code which reconstructs the original file from a sequence of images."""

import os
from PIL import Image

IMAGE_SIZE = 2048  # 2048x2048 image
HEADER_SIZE_BITS = 96  # 64 bits for File ID + 32 bits for Sequence Number

def image_to_bits(image_path):
    """Extract bits from a grayscale image and return the sequence number."""
    img = Image.open(image_path).convert('L')
    pixels = list(img.getdata())

    bits = []
    for pixel_val in pixels:
        for i in range(7, -1, -1):
            bits.append((pixel_val >> i) & 1)

    # Extract the sequence number from the header (last 32 bits of the first 96 bits)
    sequence_number_bits = bits[64:96]
    sequence_number = 0
    for bit in sequence_number_bits:
        sequence_number = (sequence_number << 1) | bit

    # Return the sequence number and the remaining bits
    return sequence_number, bits[HEADER_SIZE_BITS:]

def bits_to_file(bits, output_file):
    """Reconstruct the original file from bits."""
    # Extract file size from the first 64 bits (metadata)
    size_bits = bits[:64]
    file_size = 0
    for bit in size_bits:
        file_size = (file_size << 1) | bit

    print(f"[INFO] Extracted file size from metadata: {file_size} bytes")

    # Remove the metadata and convert remaining bits into bytes
    bits = bits[64:]  # Exclude metadata
    byte_array = bytearray()

    for i in range(0, len(bits), 8):
        byte_bits = bits[i:i+8]
        if len(byte_bits) < 8:
            break
        byte_val = 0
        for bit in byte_bits:
            byte_val = (byte_val << 1) | bit
        byte_array.append(byte_val)

    # Truncate to the actual original file size
    byte_array = byte_array[:file_size]

    with open(output_file, 'wb') as f:
        f.write(byte_array)

    print(f"[SUCCESS] Reconstructed original file: {output_file}")

def main():
    # Hardcoded paths for input folder and output file
    image_sequence_folder = r"C:\Users\jhjos\OneDrive\Desktop\YoutubeVault\opfiles\nodev22140x64_sequence"
    output_file = r"C:\Users\jhjos\OneDrive\Desktop\YoutubeVault\ipfiles\node_reconstructed.msi"

    # Get all image paths
    image_files = [
        os.path.join(image_sequence_folder, f)
        for f in os.listdir(image_sequence_folder)
        if f.lower().endswith('.png')
    ]

    if not image_files:
        print(f"[ERROR] No valid image files found in folder: {image_sequence_folder}")
        return

    print(f"[INFO] Found {len(image_files)} images in sequence.")

    all_bits = []
    image_data = []

    for img_path in image_files:
        # Extract sequence number and bits from each image
        sequence_number, bits = image_to_bits(img_path)
        image_data.append((sequence_number, bits))

    # Sort images by sequence number
    image_data.sort(key=lambda x: x[0])

    # Collect all bits in the correct order
    for _, bits in image_data:
        all_bits.extend(bits)

    # Reconstruct the original file from the collected bits
    bits_to_file(all_bits, output_file)

if __name__ == "__main__":
    main()
