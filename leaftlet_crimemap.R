# Load required packages
library(leaflet)
library(dplyr)
library(readr)
library(htmlwidgets)

# Read the geocoded data from CSV
data <- read_csv("/Users/devin/NIU_CrimeLogReader/updated_crime_data_google_with_coords.csv")  # Replace with your CSV file path

# Check the data structure
head(data)

# Create a Leaflet map
leaflet_map<- leaflet(data) %>%
  addTiles() %>%  # Add default OpenStreetMap tiles
  addMarkers(
    ~Longitude, ~Latitude,  # Use the Longitude and Latitude columns
    popup = ~paste(
      "<b>Place:</b>", Current_Column, "<br>",
      "<b>Address:</b>", Full_Address, "<br>",
      "<b>Offense:</b>", Offense, "<br>",
      "<b>Latitude:</b>", Latitude, "<br>",
      "<b>Longitude:</b>", Longitude
    )  # Add popups with place details
  ) %>%
  setView(
    lng = mean(data$Longitude, na.rm = TRUE),  # Center the map on average longitude
    lat = mean(data$Latitude, na.rm = TRUE),   # Center the map on average latitude
    zoom = 14  # Adjust the zoom level
  )



saveWidget(leaflet_map, "crime_map_with_offense.html", selfcontained = TRUE)
