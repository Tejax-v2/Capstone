#******************************************TEST CODE*****************************************

import requests

def search_cve_ids(keywords):
    base_url = 'https://services.nvd.nist.gov/rest/json/cves/1.0'
    query_url = f'{base_url}?keyword={keywords}'
    
    try:
        response = requests.get(query_url)
        response.raise_for_status()
        data = response.json()
        
        if 'result' in data and 'CVE_Items' in data['result']:
            cve_ids = [item['cve']['CVE_data_meta']['ID'] for item in data['result']['CVE_Items']]
            return cve_ids
        else:
            print("No CVEs found for the given keywords.")
            return []
    except requests.exceptions.RequestException as e:
        print("Error fetching data:", e)
        return []

if __name__ == "__main__":
    keywords = input("Enter keywords to search for CVEs: ")
    cve_ids = search_cve_ids(keywords)
    if cve_ids:
        print("CVE IDs found:")
        for cve_id in cve_ids:
            print(cve_id)
