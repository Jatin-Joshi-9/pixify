
# Pixify: File-to-Image Transcoder

![Pixel Art Concept](https://example.com/pixel-art.jpg) *Imagine your files as beautiful pixel art*

## 🔮 About
Pixify is a Python-based alchemy tool that:
- Transforms any file into a series of 1024×1024 grayscale images
- Magically reconstructs the original file from the image sequence
- Embeds file size metadata in the first image (8-byte header)

## ⚙️ Technical Specifications

### Core Parameters
| Parameter          | Value       | Description                     |
|--------------------|-------------|---------------------------------|
| Image Dimensions   | 1024×1024   | Fixed output image size         |
| Bytes per Image    | 1,048,576   | 1024×1024 pixels × 1 byte/pixel|
| Metadata Size      | 8 bytes     | Stored in first image           |

## 🧙‍♂️ Encoder: File → Pixel Incantation

### Code Architecture
```python
def file_to_bits_with_metadata(filename):
    # 1. Read file bytes
    # 2. Prefix with 8-byte size header
    # 3. Convert to bit array

def save_bits_as_image(bits_chunk, image_path):
    # 1. Create 1024×1024 grayscale image
    # 2. Pack bits into pixel values (8 bits → 1 byte)
    # 3. Save as PNG

def split_bits_to_images(bits, output_folder):
    # 1. Split bitstream into chunks of 8,388,608 bits (1MB)
    # 2. Generate sequential images (f1.png, f2.png...)
```

### Usage Example
```bash
python encoder.py \
    --input "secret_document.pdf" \
    --output "pixel_art_sequence"
```

## 🔍 Decoder: Pixel Resurrection Ritual

### Code Architecture
```python
def image_to_bits(image_path):
    # 1. Read PNG image
    # 2. Extract bits from pixel values (1 byte → 8 bits)

def bits_to_file(bits, output_file):
    # 1. Extract 64-bit file size header
    # 2. Convert remaining bits to bytes
    # 3. Truncate to original size
```

### Usage Example
```bash
python decoder.py \
    --input "pixel_art_sequence" \
    --output "reconstructed.pdf"
```

## 📊 Performance Characteristics

| File Size | Images Generated | Processing Time |
|-----------|------------------|-----------------|
| 1 MB      | 1                | ~2s             |
| 10 MB     | 10               | ~15s            |
| 100 MB    | 96               | ~2m             |

## 🛠️ Installation

```bash
pip install pillow
git clone https://github.com/yourusername/pixify
cd pixify
```

## 🌟 Advanced Features

- **Custom Image Sizes**: Modify `IMAGE_SIZE` constant
- **Color Images**: Change `'L'` to `'RGB'` mode
- **Error Resilience**: Add parity bits for corruption detection

## 📜 License
MIT License - Do whatever, just don't blame us if your tax documents turn into abstract art.

---
> "Any sufficiently advanced technology is indistinguishable from magic."  
> *- Arthur C. Clarke's Third Law, Pixify Edition*
```
