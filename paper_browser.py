import requests
import xml.etree.ElementTree as ET
from flask import Flask, render_template, request
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    publications = []
    start_date = None
    end_date = None

    if request.method == 'POST':
        keyword = request.form.get('keyword')
        print (f"Słowo kluczowe: {keyword}")
        date_range = request.form.get('date_range')
        print (f"Opcja daty: {date_range}")
        
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
            
            # Konwersja łańcuchów znaków na obiekty daty
            start_date = date.fromisoformat(start_date_str)
            end_date = date.fromisoformat(end_date_str)
                    
        url = "http://export.arxiv.org/api/query"
        parameters = {
            "search_query": f"{keyword} AND submittedDate:[{start_date.strftime('%Y-%m-%d')}T00:00:00Z TO {end_date.strftime('%Y-%m-%d')}T23:59:59Z]",
            "max_results": 10
        }
        
        response = requests.get(url, params=parameters)

        if response.status_code == 200:
            root = ET.fromstring(response.text)
            for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
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

    return render_template('index.html', publications=publications)

if __name__ == '__main__':
    app.run(debug=True)