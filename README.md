# Paper Browser Web Application

## Overview
Paper Browser is a web application that integrates with the arXiv API, allowing users to browse and select scientific data for download. Users can search for publications based on specified keywords and publication dates.

## Technology Stack
- **Backend**: Python (Flask framework)
- **Frontend**: HTML, JavaScript
- **API**: arXiv API

## Features
1. **Keyword-based Search**: Users can input multiple keywords to refine their search.
2. **Customizable Date Range**: Users can select specific time frames such as the last year, month, week, or a custom date range.
3. **Max Results**: Set a limit to the number of results returned.
4. **Sort Options**: Sort results by relevance, last updated date, or submitted date in ascending or descending order.

## Installation & Setup
1. Ensure you have Python installed on your machine.
2. Clone this repository:
   git clone https://github.com/mariuszkam4/paper_browser.git
3. Navigate to the directory and install the necessary Python packages:
   cd <repository_directory>
   pip install Flask requests
4. Run the Flask application:
   python paper_browser.py

This will start the application. Navigate to `http://localhost:5000` in your browser to access the application.

## Usage
1. Input one or multiple keywords related to the papers you're interested in.
2. Select the maximum number of results you'd like to see.
3. Choose a date range (last year, last month, last week, or a custom date range).
4. Select sorting criteria.
5. Click "Search".

The results will be displayed below the search form, and you can click on the paper titles to access their PDF versions on arXiv.

## Future Enhancements
- Add pagination for results.
- Implement user accounts and save search histories.
- Integrate more scientific data APIs for a broader search.

## License
MIT License.

## Feedback
Feel free to submit issues or pull requests, or simply contact me at `<your_email>` for any suggestions or feedback.

