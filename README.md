
# Disaster Information Aggregation using Machine Learning

This project aims to aggregate and analyze disaster-related information using machine learning techniques. It collects data from various sources, processes it, and provides insights to aid in disaster response and management.

## Features

- **Data Collection**: Gathers disaster-related data from multiple sources.
- **Data Processing**: Cleans and structures the collected data for analysis.
- **Machine Learning Analysis**: Applies machine learning models to identify patterns and insights.
- **Web Interface**: Provides a user-friendly interface to visualize and interact with the data.

## Requirements

Ensure you have the following installed:

- Python 3.x
- Flask
- Python-dotenv
- Requests
- Feedparser
- Flask-SQLAlchemy
- Psycopg2

You can install the required Python packages using:

```bash
pip install flask python-dotenv requests feedparser flask_sqlalchemy psycopg2
```

## Setup Instructions

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/nawazishbilal/disaster_info_agg.git
   ```

2. **Navigate to the Project Directory**:

   ```bash
   cd disaster_info_agg
   ```

3. **Set Up Environment Variables**:

   - Create a `.env` file in the project root directory.
   - Add necessary environment variables as required by your application.

4. **Initialize the Database**:

   - Run the `init_db.py` script to set up the database schema:

     ```bash
     python init_db.py
     ```

5. **Run the Application**:

   ```bash
   python app.py
   ```

6. **Access the Web Interface**:

   - Open your web browser and navigate to the URL displayed in the terminal (e.g., `http://127.0.0.1:5000/`).

## Project Structure

- `app.py`: Main application file that starts the Flask server.
- `config.py`: Configuration settings for the application.
- `db.py`: Database connection and setup.
- `models.py`: Defines the database models.
- `routes.py`: Handles the web routes and API endpoints.
- `init_db.py`: Initializes the database with the required schema.
- `twitter_api.py`: Manages interactions with the Twitter API.
- `static/`: Contains static files like CSS, JavaScript, and images.
- `templates/`: Contains HTML templates for rendering the web pages.
- `tweets.csv`: Sample dataset of collected tweets.
- `test.txt`: Placeholder file for testing purposes.

## Usage

- **Navigation**: Use the web interface to navigate between different components of the project.
- **Data Visualization**: View aggregated data and analysis results through interactive charts and tables.
- **Customization**: Modify the machine learning models and data sources as needed to fit specific requirements.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Acknowledgments

Special thanks to all contributors and the open-source community for their invaluable support.
