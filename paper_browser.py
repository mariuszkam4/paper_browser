import requests
import xml.etree.ElementTree as ET
from flask import Flask, render_template, request
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

# Initialize Flask application
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    # Initialize necessary varaibles
    publications = []
    start_date = None
    end_date = None
    keywords_list = []

    if request.method == 'POST':
        # Extract all keywords from the dynamically generated form fields
        for key in request.form:
            if "keyword_" in key:
                keyword_value = request.form.get(key) or ''
                if keyword_value:
                    keywords_list.append(keyword_value.strip())
        
        # Get max results and validate it
        max_results = request.form.get('max_results')
        if not max_results.isnumeric():
            return "Invalid numeber of max results", 400

        # Determine the date range based on user input
        date_range = request.form.get('date_range')
        
        # Set start and end dates based on the selected range
        if date_range == "1":
            end_date = date.today()
            start_date = end_date - relativedelta(years=1)
        elif date_range == "2":
            end_date = date.today()
            start_date = end_date - timedelta(days=30)            
        elif date_range == "3":
            end_date = date.today()
            start_date = end_date - relativedelta(weeks=1)            
        elif date_range == "4":
            start_date_str = request.form.get('start_date')
            end_date_str = request.form.get('end_date')
            
           # Convert string dates to date objects for custom range
            start_date_str = request.form.get('start_date')
            end_date_str = request.form.get('end_date')
            start_date = date.fromisoformat(start_date_str)
            end_date = date.fromisoformat(end_date_str)
        
        # Construct the search query for the API
        sortBy = request.form.get ('sortBy', 'relevance')
        sortOrder = request.form.get ('sortOrder', 'ascending')
        keywords_query = " AND ".join([f"ti:\"{keyword}\"" for keyword in keywords_list])
        search_query = f"({keywords_query}) AND submittedDate:[{start_date.strftime('%Y-%m-%d')}T00:00:00Z TO {end_date.strftime('%Y-%m-%d')}T23:59:59Z]"
        
        # Fetch results from arXiv API
        url = "http://export.arxiv.org/api/query"
        parameters = {
            "search_query": search_query,
            "max_results": int(max_results),
            "sortBy": sortBy,
            "sortOrder": sortOrder
        }
        
        # Handle potential API errors
        try:
            response = requests.get(url, params=parameters)
            response.raise_for_status()
        except requests.RequestException as e:
            return "An error occured while processing your request. Please try again later.", 500
        
        # If response is succesfull, pare the XML to extract publictaion data
        if response.status_code == 200:
            root = ET.fromstring(response.text)
            for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):

                # Extract details for each publication
                title = entry.find('{http://www.w3.org/2005/Atom}title').text
                summary = entry.find('{http://www.w3.org/2005/Atom}summary').text
                published = entry.find('{http://www.w3.org/2005/Atom}published').text
                link = entry.find('{http://www.w3.org/2005/Atom}link[@title="pdf"]').attrib['href']
                publications.append({
                    "title": title,
                    "summary": summary,
                    "published": published,
                    "link": link
                })

    # Render the HTML template with the fetched data
    return render_template('index.html', publications=publications, keywords_list=keywords_list, start_date=start_date, end_date=end_date)

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=False)