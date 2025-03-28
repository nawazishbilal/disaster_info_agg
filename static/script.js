


document.addEventListener("DOMContentLoaded", () => {
    console.log("DOM fully loaded");

    function waitForElement(selector, callback, interval = 100, attempts = 10) {
        let tries = 0;
        const check = setInterval(() => {
            const element = document.querySelector(selector);
            if (element) {
                clearInterval(check);
                callback();
            } else if (++tries >= attempts) {
                clearInterval(check);
                console.error(`Error: ${selector} not found after ${attempts} attempts.`);
            }
        }, interval);
    }

    waitForElement("#gdacs-list", fetchLatestGDACS);
});

async function fetchEarthquakes() {
    const location = document.getElementById("location").value.trim();
    const limit = 5; // Default limit

    if (!location) {
        alert("Enter location for earthquake data!");
        console.error("Please enter a location!");
        return;
    }

    try {
        const response = await fetch(`/earthquakes?location=${encodeURIComponent(location)}&limit=${limit}`);
        const data = await response.json();

        if (!data.earthquakes || !Array.isArray(data.earthquakes)) {
            console.error("Unexpected response format:", data);
            return;
        }

        const list = document.getElementById('earthquake-list');
        list.innerHTML = '';

        data.earthquakes.forEach(eq => {
            const item = document.createElement('li');
            item.textContent = `Magnitude: ${eq.magnitude}, Location: ${eq.place}`;
            list.appendChild(item);
        });
    } catch (error) {
        console.error("Error fetching earthquake data:", error);
    }
}

function fetchLatestGDACS() {
    fetch('/gdacs')
    .then(response => response.json())
    .then(data => {
        console.log("Received GDACS Data:", data);  // Debugging step

        if (!data || !Array.isArray(data.gdacs_alerts)) {  // Use 'gdacs_alerts' instead of 'alerts'
            console.error("Invalid GDACS data format:", data);
            return;
        }

        const latestAlerts = data.gdacs_alerts.slice(0, 10);  // Limit to 10 alerts
        const alertsList = document.getElementById("gdacs-list");

        alertsList.innerHTML = ""; // Clear old alerts
        latestAlerts.forEach(alert => {
            const listItem = document.createElement("li");
            listItem.innerHTML = `
                <div class="alert-card">
                    <h3 class="alert-title">${alert.title}</h3>
                    <p class="alert-summary">${alert.summary}</p>
                    <p class="alert-time">${alert.published}</p>
                    <a href="${alert.link}" target="_blank">Read More</a>
                </div>
            `;
            alertsList.appendChild(listItem);
        });
    })
    .catch(error => console.error("Error fetching GDACS alerts:", error));

}

// ✅ Fix: Fetch alerts based on date range for alerts page
function fetchFilteredGDACS() {
    const startDate = document.getElementById("start-date").value;
    const endDate = document.getElementById("end-date").value;

    if (!startDate || !endDate) {
        alert("Please select both start and end dates.");
        return;
    }

    fetch(`/gdacs?start_date=${startDate}&end_date=${endDate}`)
        .then(response => response.json())
        .then(data => {
            if (!data.gdacs_alerts || !Array.isArray(data.gdacs_alerts)) {
                throw new Error("Unexpected response format");
            }

            const gdacsList = document.getElementById("gdacs-list");
            gdacsList.innerHTML = "";

            if (data.gdacs_alerts.length === 0) {
                gdacsList.innerHTML = "<p>No alerts found for the selected date range.</p>";
                return;
            }

            data.gdacs_alerts.forEach(alert => {
                const li = document.createElement("li");
                li.innerHTML = `<strong>${alert.title}</strong> - ${alert.summary} (Published: ${alert.published})`;
                gdacsList.appendChild(li);
            });
        })
        .catch(error => console.error("Error fetching filtered GDACS alerts:", error));
}




function fetchWeather() {
    const location = document.getElementById("city").value.trim();
    
    if (!location) {
        console.error("Location is required!");
        return;
    }

    fetch(`/weather?location=${encodeURIComponent(location)}`)
        .then(response => response.json())
        .then(data => {
            //console.log("Weather API Response:", data); //debugging line

            if (data.error) {
                console.error("Weather API Error:", data.error);
                return;
            }

            const list = document.getElementById("weather-list");
            list.innerHTML = "";

            // Correctly display weather details
            const weatherDetails = `
                <li><strong>Location:</strong> ${data.weather_alerts.location}</li>
                <li><strong>Temperature:</strong> ${data.weather_alerts.temperature}°C</li>
                <li><strong>Weather:</strong> ${data.weather_alerts.weather}</li>
                <li><strong>Humidity:</strong> ${data.weather_alerts.humidity}%</li>
                <li><strong>Wind Speed:</strong> ${data.weather_alerts.wind_speed} m/s</li>
            `;
            
            list.innerHTML = weatherDetails;
        })
        .catch(error => console.error("Error fetching weather alerts:", error));
}

function fetchTweets() {
    const keyword = document.getElementById("keyword").value;
    fetch(`/tweets?query=${keyword}`)
        .then(response => response.json())
        .then(data => {
            const list = document.getElementById("tweets-list");
            list.innerHTML = "";
            data.tweets.forEach(tweet => {
                const item = document.createElement("li");
                item.textContent = tweet.text;
                list.appendChild(item);
            });
        })
        .catch(error => console.error("Error fetching tweets:", error));
}
