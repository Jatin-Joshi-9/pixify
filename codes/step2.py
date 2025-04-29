"""This is the decoder code which effectively and smartly converts the seuence of images back into the original file."""


import os
from PIL import Image

def image_to_bits(image_path):
    img = Image.open(image_path).convert('L')
    pixels = list(img.getdata())

    bits = []
    for pixel_val in pixels:
        for i in range(7, -1, -1):
            bits.append((pixel_val >> i) & 1)
    return bits

def bits_to_file(bits, output_file):
    # Extract file size from first 64 bits (8 bytes)
    size_bits = bits[:64]
    file_size = 0
    for bit in size_bits:
        file_size = (file_size << 1) | bit

    print(f"[INFO] Extracted file size from metadata: {file_size} bytes")

    # Convert remaining bits into bytes
    bits = bits[64:]  # exclude metadata
    byte_array = bytearray()

    for i in range(0, len(bits), 8):
        byte_bits = bits[i:i+8]
        if len(byte_bits) < 8:
            break
        byte_val = 0
        for bit in byte_bits:
            byte_val = (byte_val << 1) | bit
        byte_array.append(byte_val)

    # Truncate to actual original file size
    byte_array = byte_array[:file_size]

    with open(output_file, 'wb') as f:
        f.write(byte_array)

    print(f"[SUCCESS] Reconstructed original file: {output_file}")

def main():
    # CHANGE THESE
    image_sequence_folder = r
    output_file = r

    # Get sorted image paths like f1.png, f2.png, ...
    image_files = sorted([
        os.path.join(image_sequence_folder, f)
        for f in os.listdir(image_sequence_folder)
        if f.lower().endswith('.png')
    ], key=lambda x: int(os.path.splitext(os.path.basename(x))[0][1:]))

    print(f"[INFO] Found {len(image_files)} images in sequence.")

    all_bits = []
    for img_path in image_files:
        all_bits.extend(image_to_bits(img_path))

    bits_to_file(all_bits, output_file)

if __name__ == "__main__":
    main()
