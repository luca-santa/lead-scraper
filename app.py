import streamlit as st
import requests
import csv
import io

st.set_page_config(page_title="Yelp Lead Scraper (API Powered)", layout="centered")
st.title("🧲 Yelp Lead Scraper (API Powered)")

API_KEY = "7403d231366e002293783ed72c00047c"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def yelp_search(term, location, limit=10):
    url = "https://api.yelp.com/v3/businesses/search"
    params = {
        "term": term,
        "location": location,
        "limit": limit
    }
    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code != 200:
        st.error(f"Error fetching data: {response.status_code} {response.text}")
        return []

    data = response.json()
    businesses = data.get("businesses", [])
    results = []
    for biz in businesses:
        results.append({
            "Name": biz.get("name", ""),
            "Address": ", ".join(biz.get("location", {}).get("display_address", [])),
            "Phone": biz.get("display_phone", ""),
            "Rating": biz.get("rating", ""),
            "URL": biz.get("url", "")
        })
    return results

def convert_to_csv(data):
    output = io.StringIO()
    fieldnames = ["Name", "Address", "Phone", "Rating", "URL"]
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)
    return output.getvalue()

term = st.text_input("Business Type (e.g. plumber)", "")
location = st.text_input("Location (e.g. Dallas, TX)", "")
max_results = st.slider("Max Results", min_value=5, max_value=50, value=10)
search_button = st.button("Search")

if search_button:
    if not term or not location:
        st.warning("Please enter both business type and location.")
    else:
        st.info("Searching Yelp...")
        leads = yelp_search(term, location, max_results)
        if leads:
            st.success(f"Found {len(leads)} results.")
            for lead in leads:
                st.markdown(f"**[{lead['Name']}]({lead['URL']})**  \n{lead['Address']}  \n{lead['Phone']}  \nRating: {lead['Rating']}")
            csv_data = convert_to_csv(leads)
            st.download_button("Download CSV", csv_data, "yelp_leads.csv", "text/csv")
        else:
            st.warning("No results found.")
