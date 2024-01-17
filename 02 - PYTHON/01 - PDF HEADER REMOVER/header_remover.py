# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 12:27:49 2023

@author: pmbarral
"""

import os
from PyPDF2 import PdfReader, PdfWriter

# Function to remove header from a PDF page
def remove_header_from_page(page, header_height):
    """
    Remove the header from a page by adjusting the media box.

    Args:
        page (Page): The page object from which the header should be removed.
        header_height (int): The height of the header to be removed.

    Returns:
        None
    """
    # Get the media box of the page
    media_box = page.mediabox
    
    # Calculate the new upper right corner of the media box
    new_upper_right = (media_box.right, media_box.top - header_height)
    
    # Update the media box with the new upper right corner
    media_box.upper_right = new_upper_right


# Function to remove header from a PDF file
from PyPDF2 import PdfReader, PdfWriter

from PyPDF2 import PdfReader, PdfWriter

def remove_header_from_pdf(input_path: str, output_path: str, header_height: int) -> None:
    """
    Remove header from PDF file and save the modified PDF to the output path.

    Args:
        input_path (str): The path of the input PDF file.
        output_path (str): The path where the modified PDF will be saved.
        header_height (int): The height of the header to be removed.
    """
    # Open the input PDF file
    input_pdf = PdfReader(open(input_path, 'rb'))

    # Create a new PDF writer
    output_pdf = PdfWriter()

    # Iterate over each page in the input PDF
    for page_num in range(len(input_pdf.pages)):
        # Get the current page
        page = input_pdf.pages[page_num]

        # Remove the header from the page
        remove_header_from_page(page, header_height)

        # Add the modified page to the output PDF
        output_pdf.add_page(page)

    # Save the modified PDF to the output file
    with open(output_path, 'wb') as output_file:
        output_pdf.write(output_file)

if __name__ == "__main__":
    input_folder = "input"
    output_folder = "output"

    if not os.path.exists(input_folder):
        os.makedirs(input_folder)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(".pdf"):
            input_pdf_path = os.path.join(input_folder, filename)
            output_pdf_path = os.path.join(output_folder, filename)

            header_height = 45  # Adjust this value according to the header height (in points)
            remove_header_from_pdf(input_pdf_path, output_pdf_path, header_height)