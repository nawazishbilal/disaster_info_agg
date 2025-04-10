# 🌍 Disaster Information Aggregation Web App

A real-time, multi-source disaster data aggregator that provides live alerts, weather reports, earthquake data, and a dynamic weather map interface. Built using **Flask**, **PostgreSQL**, and **JavaScript**, the app integrates several APIs for timely and actionable insights.

---

## 🔧 Features

- 📡 **Real-time Earthquake Data** from USGS API
- 🌊 **Global Disaster Alerts** via GDACS RSS Feed
- ☁️ **Live Weather Forecasts** using OpenWeatherMap API
- 🌪 **Interactive Weather Map** powered by Windy API
- 🧭 Search-based filtering (by location, disaster type, date)
- 🗺️ Responsive UI with map and data split view
- 🌐 Toggle navigation to switch between views

---

## 📁 Project Structure

```
📦 disaster-info-aggregator/
├── app.py
├── config.py
├── db.py
├── init_db.py
├── models.py
├── routes.py
├── templates/
│   ├── index.html
│   ├── alerts.html
│   ├── earthquakes.html
│   ├── weather.html
├── static/
│   ├── script.js
│   ├── style.css
├── .env
└── README.md
```

---

## 🔌 APIs Used

| Feature              | API Provider           | Endpoint Type     |
|---------------------|------------------------|-------------------|
| Earthquakes         | USGS                   | GeoJSON           |
| Global Alerts       | GDACS                  | RSS Feed          |
| Weather Forecast    | OpenWeatherMap         | REST + Geocoding  |
| Weather Map         | Windy.com              | Embedded JS SDK   |

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/disaster-info-aggregator.git
cd disaster-info-aggregator
```

### 2. Create a Python Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up `.env`

Create a `.env` file and add your credentials:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/disaster_db
OPENWEATHER_API_KEY=your_openweather_api_key
WINDY_API_KEY=your_windy_api_key
```

### 5. Initialize Database

```bash
python init_db.py
```

### 6. Run the App

```bash
flask run
```

Visit: `http://127.0.0.1:5000/`

---

## 🧪 Features by Page

- **Home (`/`)**  
  View 5 latest high-alert disasters from GDACS

- **Earthquakes (`/earthquakes`)**  
  Search and filter USGS earthquake data by location

- **Weather (`/weather`)**  
  Fetch live weather details and view the Windy map

- **Alerts (`/alerts`)**  
  Filter global disaster alerts by date and disaster type

---

## 🎨 UI Highlights

- Responsive glassmorphism design
- Sticky floating navbar
- Weather and map views aligned side-by-side
- Input validation with user-friendly error prompts

---

## 📌 Author

**Developed by Nawazish Bilal, Abhi Uranw**  
GitHub: [@nawazishbilal](https://github.com/nawazishbilal) [@Apps1289](https://github.com/Apps1289)