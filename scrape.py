import requests
from bs4 import BeautifulSoup
import json
import os

def scrape_data():
    data_dict = {}
    url = "https://delhihighcourt.nic.in/court/dhc_case_status_list_new?sno=1&ctype=W.P.%28C%29&cno=432&cyear=2020"
    
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        
        table_present = soup.find('table', {'class': "table table-bordered table-hover table-striped"})
        
        if table_present:
            key_row = soup.find_all("th")
            if key_row:
                for keys in key_row:
                    key_text = keys.text.strip()
                    data_dict[key_text] = ""
            
            value_rows = soup.find_all("td")
            if value_rows:
                for i in range(len(value_rows)):
                    value_text = value_rows[i].text.strip().replace("\u00a0", " ").replace('\r', '').replace('\n', ' ')
                    data_dict[list(data_dict.keys())[i]] = value_text

            # Write the data_dict to a JSON file
            with open("data.json", "w") as json_file:
                json.dump(data_dict, json_file, indent=4)

            next_links = table_present.find_all("a")
            for link in next_links:
                href = link.get("href")
                print(href)

            # Assuming 'href' contains the URL of page_2
            page_2 = requests.get(href)
            soup_2 = BeautifulSoup(page_2.text, "html.parser")

            try:
                pdf_table = soup_2.find("div", {"class": "inner-page-content rti-page two-column"})
                pdf_links = pdf_table.find_all("a")
                for link in pdf_links:
                    p_href = link.get("href")
                    
                    folder_path = "C:/Codes/New folder/DHCFlask/SavedFiles"

                    if p_href and p_href.endswith(".pdf"):
                        filename = os.path.basename(p_href)
                        pdf_response = requests.get(p_href)

                        # Combine the folder path and filename to create the complete file path
                        file_path = os.path.join(folder_path, filename)

                        with open(file_path, "wb") as pdf_file:
                            pdf_file.write(pdf_response.content)
                            print(f"Downloaded {filename} to {file_path}")

            except AttributeError:
                print("Attribute Error in second")

    except Exception as e:
        print(f"Scraping error: {str(e)}")
        return None

    return data_dict
