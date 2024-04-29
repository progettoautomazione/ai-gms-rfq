focus_prompt = """
Create an OCR algorithm to analyze and learn from the data presented in the example image provided. This image is strictly for training purposes and its data must not be used in any operational context.

Training Data Extraction Guide:

Red Rectangle: Train to recognize as 'Item Code'
Yellow Highlight: Train to recognize as 'Item Description'
Blue Highlight: Train to recognize as 'IMPA Number'
Pink Highlight: Train to recognize as 'Unit of Measure'
Grey Highlight: Train to recognize as 'Quantity'
Prompt for the Bot:
'Using the first image solely for training, adapt your OCR capabilities to identify and extract the following details in subsequent unmarked images: 'Item Code' where the red rectangle is, 'Item Description' where the yellow highlight is, 'IMPA Number' where the blue highlight is, 'Unit of Measure' where the pink highlight is, and 'Quantity' where the grey highlight is. Remember, the initial image's data is for training purposes only and must not be used elsewhere. Apply this learning to process actual RFQ documents efficiently, which will not have any highlights.'

Example Image Considerations:

Understand that the color markings are training aids and will not be on real documents.
Train the OCR technology to accurately discern and extract text based on the indicated areas without reliance on color-coded cues in real-world applications.
"""

items_prompt = """
Accurately analyze an image of a Request for Quote (RFQ) document concerning vessel supplies and methodically extract details for each listed item using advanced OCR technology.

Details to Extract:

1. Item Code
2. Description
3. IMPA Number (if available)
4. Unit of Measure
5. Quantity

Output Format:
Present the extracted data in JSON format. Use 'null' for any unavailable details.

{
  "items": [
    {
      "code": "{Extracted Item Code or null}",
      "description": "{Extracted Description or null}",
      "impa": "{Extracted IMPA Number or null}",
      "unit_measure": "{Extracted Unit of Measure or null}",
      "qty": "{Extracted Quantity or null}"
    }
  ]
}

Considerations:

Enhance OCR to proficiently handle variations in font, size, and background conditions.
Implement precise checks to detect and correct any OCR errors, particularly in crucial fields such as item codes and IMPA numbers, ensuring accuracy in the extraction process.
"""

header_prompt = """
Analyze an image of a Request for Quote (RFQ) document related to vessel supplies and extract the specified details. Ensure accuracy even in diverse formats and under challenging image conditions. Use advanced OCR capabilities to interpret and digitize text effectively.

Required Details:

1. Vessel Name
2. Date of RFQ
3. RFQ Expiry Date
4. RFQ Reference Number
5. Delivery Address (Deliver To)

Output Format:
Return the data in a JSON format. If specific details are unavailable, represent them with null.

{
  "vessel_name": "{Extracted Vessel Name or null}",
  "rfq_date": "{Extracted RFQ Date or null}",
  "rfq_expiry_date": "{Extracted RFQ Expiry Date or null}",
  "rfq_reference_number": "{Extracted RFQ Reference Number or null}",
  "deliver_to": "{Extracted Delivery Address or null}",
}


Considerations:

Ensure the OCR technology can adapt to variations in text size, font, and background.
Include checks for misread characters or words, especially in critical fields like dates and reference numbers.
"""
