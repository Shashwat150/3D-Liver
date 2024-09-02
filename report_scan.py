import re
from pdf2image import convert_from_path
import pytesseract
import socket
import threading


        
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\shashwat\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
SGOT_list =  ["AST", "AST (SGOT)", "AST(SGOT)"]
SGPT_list =  ["ALT", "ALT (SGPT)", "ALT(SGPT)"]

def replace_synonyms(text):
    # Replace "Bilirubin Total" with "Total Bilirubin"
    text = re.sub(r'\bBilirubin Total\b', 'Total Bilirubin', text, flags=re.IGNORECASE)
    text = re.sub(r'\bBilirubin Direct\b', 'Direct Bilirubin', text, flags=re.IGNORECASE)

    for word in SGOT_list:
      text = re.sub(r'\bword\b', 'SGOT', text, flags=re.IGNORECASE)

    for word in SGPT_list:
      text = re.sub(r'\bword\b', 'SGPT', text, flags=re.IGNORECASE)

    text = re.sub(r'\bProtein Total\b', 'Total Protein', text, flags=re.IGNORECASE)

    return text

def extract_text_from_pdf(pdf_path):
    images = convert_from_path(pdf_path, 500)
    pdf_text = ""

    for i, image in enumerate(images):
        text = pytesseract.image_to_string(image)
        pdf_text += text

    return pdf_text

def extract_numeric_results_from_text(text, parameters_of_interest):
    parameter_results = {}

    for parameter in parameters_of_interest:
        # surrounding_pattern = r"(?:\w+\s*)?"  # Optional non-capturing group for any word and optional whitespace
        # pattern = re.compile(fr"{surrounding_pattern}{re.escape(parameter)}{surrounding_pattern}\s*([0-9.]+)")

        pattern = re.compile(fr"[^\d.]*{re.escape(parameter)}[^\d.]*\s*([0-9.]+)")
        match = pattern.search(text)

        # If a match is found, add the parameter and its numeric result to the dictionary
        if match:
            numeric_result = match.group(1)
            parameter_results[parameter] = numeric_result

    return parameter_results


# pdf_path = r'C:\Users\Ant PC\Shashwat_BTP\LFT Report 1 PDF.pdf'
pdf_path = r'C:\Users\shashwat\Desktop\Shashwat_BTP\LFT Report 1 PDF.pdf'

parameters_of_interest = ["Total Bilirubin","Direct Bilirubin","SGOT", "SGPT", "Total Protein", "Albumin","Alkaline Phosphatase"]
# parameters_of_interest = extract_lft_parameters_from_pdf(pdf_path)
pdf_text = extract_text_from_pdf(pdf_path)
# print(pdf_text)
pdf_text = replace_synonyms(pdf_text)

# Extract numeric results from the OCR text
results = extract_numeric_results_from_text(pdf_text, parameters_of_interest)
temp2 = list(range(5))
a=0
for parameter, value in results.items():
    print(f"{parameter}: {value}")
    if(parameter == "Total Bilirubin" or "Direct Bilirubin" or "SGOT" or "SGPT" or "Total Protein"):
        if(a<5):
            value = (float)(value)
            ###############################
            ######### factor = 100 ########
            ###############################
            temp2[a] = (int)(value*100)
            a+=1
print(temp2)
# temp2 = ["Total Bilirubin" , "Direct Bilirubin" , "SGOT" , "SGPT" , "Total Protein"]

def handle_client(client_socket):
    # Replace this with your logic to fetch values from an external source
    # temp2 = [100, 200, 300, 400]
    response = ','.join(map(str, temp2)).encode()
    client_socket.send(response)
    client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 12345))
    server.listen(5)
    print("[*] Listening on 0.0.0.0:12345")

    while True:
        client, addr = server.accept()
        print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()

if __name__ == '__main__':
    start_server()