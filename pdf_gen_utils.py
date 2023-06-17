import os
import tempfile

import numpy as np
import cv2
from PIL import Image
from PyPDF2 import PdfMerger
from reportlab.pdfgen import canvas
from reportlab.platypus import Frame, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFont



font_path = 'fonts/KGNeatlyPrinted.ttf'
font_name = 'KGNeatlyPrinted'
font = TTFont(font_name, font_path)
registerFont(font)

title_font_path = 'fonts/ArchitectsDaughter.ttf'
title_font_name = 'ArchitectsDaughter'
title_font = TTFont(title_font_name, title_font_path)
registerFont(title_font)


def add_text_and_convert(image_path, text, output_filename, page_number, image_size=(1360,1024), ): #1174 height after adding white space
    width, height = image_size

    # Open image and resize
    img = cv2.imread(image_path)
    img = cv2.resize(img, image_size)

    # Generate fading mask: Only fade the bottom 20% of the image
    mask = np.zeros((img.shape[0], img.shape[1]), dtype=np.uint8)
    mask = cv2.rectangle(mask, (0, 0), (img.shape[1], int(img.shape[0] * 0.95)), 255, cv2.FILLED)
    mask = cv2.GaussianBlur(mask, (99, 99), 0)

    # Convert to RGB for consistency
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Convert the image and mask to PIL format
    img_pil = Image.fromarray(img_rgb)
    mask_pil = Image.fromarray(mask)

    # Generate white image in PIL format
    white_img_pil = Image.new('RGB', image_size, color='white')

    # Blend the image, white image and the mask
    blended_img_pil = Image.composite(img_pil, white_img_pil, mask_pil)

    new_image = Image.new('RGB', (width, height + 150), color='white')
    new_image.paste(blended_img_pil, (0, 0))

    # Save the modified image temporarily
    new_image.save("temp.jpg")

    # Generate PDF with the same size as the new image
    c = canvas.Canvas(output_filename, pagesize=(width, height + 150))

    # Draw the image on the PDF
    c.drawImage("temp.jpg", 0, 0)

    # Use a basic paragraph style from the sample style sheet
    style = getSampleStyleSheet()['BodyText']
    style.alignment = 1
    style.fontName = font_name
    style.fontSize = 42  # Increase font size


    text_list = split_paragraph(text, 80)
    for i, element in enumerate(text_list):
        story = [Paragraph(element, style)]
        frame_x = width * 0.015
        frame_y = (height * 0.07) - (i * 35)

        frame = Frame(frame_x, frame_y, width * 0.97, height * 0.1, id='normal')
        frame.addFromList(story, c)

    # Add page number in the bottom right corner
    c.setFont(font_name, 16)  # Increase font size
    c.drawString(width-80, 50, str(page_number))  # Position higher

    # Save the PDF
    c.save()




def build_title_page(image_path, text, output_filename, image_size=(1360, 1174)):
    # Open and resize image
    img = Image.open(image_path)
    img = img.resize(image_size)

    # Save image temporarily
    img.convert('RGB').save("temp.jpg")

    # Create a new PDF with the image
    width, height = image_size
    c = canvas.Canvas(output_filename, pagesize=(width, height))
    c.drawImage("temp.jpg", 0, 0)

    style = getSampleStyleSheet()['BodyText']
    style.alignment = 1
    style.fontName = title_font_name
    style.fontSize = 50  # Increase font size

    line_height = style.leading  # The leading property gives the height of a line of text in the given style
    padding = 50

    # Define the dimensions for the white background rectangle
    rect_height = line_height + 2 * padding  # Add padding
    rect_width = width * 0.8  # Use 80% of the page width for the rectangle
    rect_x = (width - rect_width) / 2  # Center the rectangle
    rect_y = height - 200  # Position rectangle

    # Draw the white background rectangle
    c.setFillColor('white')
    c.rect(rect_x, rect_y - rect_height, rect_width, rect_height, fill=1)

    # Add frames for each line of text
    frame_x = rect_x + padding
    frame_y = rect_y - line_height - 100

    frame = Frame(frame_x - 20, frame_y, rect_width - 1 * padding, 100, id='normal', showBoundary=0)
    story = [Paragraph(text, style)]
    frame.addFromList(story, c)

    # Save the PDF
    c.save()


def split_paragraph(paragraph, length):
    words = paragraph.split(' ')
    result = []
    current_length = 0
    current_words = []
    for word in words:
        if current_length + len(word) <= length:
            current_length += len(word) + 1  # +1 for the space
            current_words.append(word)
        else:
            result.append(' '.join(current_words))
            current_words = [word]
            current_length = len(word)
    result.append(' '.join(current_words))  # Add the last words
    return result




def build_pdf(pages, result_filename):
    pdf_files = []
    images = []

    image_path, text = pages[0]
    images.append(image_path)
    temp_file = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
    temp_file.close()
    build_title_page(image_path, text, temp_file.name)
    pdf_files.append(temp_file.name)

    for i, page in enumerate(pages[1:]):
        image_path, text = page
        images.append(image_path)
        temp_file = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
        temp_file.close()
        add_text_and_convert(image_path, text, temp_file.name, page_number=i+1)
        pdf_files.append(temp_file.name)

    merger = PdfMerger()
    for temp_file in pdf_files:
        merger.append(temp_file)

    merger.write(result_filename)
    merger.close()

    for temp_file in pdf_files:
        os.remove(temp_file)
    os.remove('temp.jpg')
    return result_filename






