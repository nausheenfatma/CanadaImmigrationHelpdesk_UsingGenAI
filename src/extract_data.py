"""

This script takes URL(s) and scrapes relevant information. 
Business specific rules are applied to understand which parts of website we are interested and care about
"""



import requests
from bs4 import BeautifulSoup, Tag

headers = {"User-Agent": "Mozilla/5.0"}


# Headers we care about
valid_headers = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']

CONTENT_START_HEADER_TEXT = "You are here"
CONTENT_ENDS_HEADER_TEXT = "Page details"

    
def extract_page(url:str):  
    """
    This method takes a string URL, extracts the text from the webpage we need and saves output in a file.
    """  

    # Fetch the content from the url
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')


    # Iterate through elements and organize them
    content = []
    current_header = None
    start_scrape_flag = False

    for element in soup.body.descendants:
        if isinstance(element, Tag):
            
            #scrape only after the header  "You are here:" is found
            #skip all the text after "Page details"  
            
            if element.get_text().startswith(CONTENT_START_HEADER_TEXT):
                start_scrape_flag = True
            
            if element.get_text().startswith(CONTENT_ENDS_HEADER_TEXT):
                #stop reading the file
                break
                    
            if start_scrape_flag:
                if element.name in valid_headers:
                        
                        
                            header_text = element.get_text(strip=True)

                            if element.name in ['h1', 'h2']:
                                
                                header_text = "\n\n\n"+header_text
                            else:
                                header_text = "\n"+header_text
                                                    
                            current_header = {
                                "header": header_text,
                                "paragraphs": []
                            }
                            content.append(current_header)
                            
                            
                elif element.name == 'p' and current_header:
                    paragraph_text = element.get_text()
                    
                    if paragraph_text:
                        
                        # Extract urls using the <a> tag
                        a_tag = element.find('a')
                        if a_tag:
                            link_text = a_tag.text
                            href = a_tag['href']
                            p_tag = element.get_text('p')
                            paragraph_text+=f" (Refer page: {href})"
                            
                        current_header["paragraphs"].append("\n"+paragraph_text)
                                    
                        
                elif element.name == 'dt' and current_header:
                    paragraph_text = element.get_text(strip=True)
                    if paragraph_text:
                        current_header["paragraphs"].append("\n"+paragraph_text+": ")
                        
                
                        
                # extract all bullet points      
                elif current_header and element.name in ["ul", "ol"]:         
                    #bullet_text = element.get_text(strip=True)
                        
                    collected_data = [li.get_text() for li in element.find_all('li')]
                    collected_data = "\n - ".join(collected_data)
                    collected_data = "- " + collected_data #For first bullet
                    current_header["paragraphs"].append(collected_data)


    # Save clean extracted content in docs
    page_name = url.split("https://www.canada.ca/en/")[1]
    page_name = "_".join(page_name.split("/"))
    fw = open(f"../data/docs/{page_name}.txt", "w")
    fw.write(f"This is content for {url}")

    for section in content:
        fw.write(f"\n{section['header']}")
        for para in section['paragraphs']:
            fw.write(f"\n {para}")   
    fw.close()


if __name__ == "__main__":
    weblinks_file = open("../data/crawled_page_links.txt")
    for line in weblinks_file:
        url = line.strip()
        extract_page(url)
        
        