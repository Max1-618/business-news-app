# Business News App

This application aggregates the latest business news from two major sources: **BBC** and **Les Echos**. The app collects headlines and displays them on a user-friendly interface built with Flask and Bootstrap.

## Features

- Fetches the latest business news from **BBC** and **Les Echos**.
- Displays news articles along with their publication timestamps and a link to read more.
- Simple and clean interface with Bootstrap for responsive design.
- Pagination for better navigation of news articles.
- Built with Flask, Selenium, BeautifulSoup, and Requests.

## Tech Stack

- **Flask**: Web framework for Python.
- **Bootstrap**: Front-end framework for building responsive UI.
- **Requests**: For making HTTP requests to fetch BBC news.
- **BeautifulSoup**: For parsing HTML and extracting news headlines from BBC.
- **Selenium**: For scraping news from Les Echos (requires web driver).
- **Python 3.x**: Programming language.

## Installation

Follow the steps below to get the app running locally.

### Prerequisites

1. Ensure you have Python 3.x installed. You can check by running:

2. Install the required dependencies. First, clone the repository:

3. Navigate to the project directory:
git clone https://github.com/Max1-618/business-news-app.git

4. Install the required Python packages:

### Running the App

Once you have the dependencies installed, run the app using:


The app will be accessible in your web browser at `http://127.0.0.1:5000/`.

## Usage

- The main page will display the latest business headlines from **BBC** and **Les Echos**.
- Click on the "Read More" button for more details on each headline.

## Contributing

Feel free to fork this repository and submit pull requests. If you find any bugs or want to suggest improvements, open an issue, and we will address it!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
