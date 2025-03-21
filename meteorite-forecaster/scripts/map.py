import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point

# Define a global variable to store the country name
country_name = None


def maps():
    global country_name  # Declare the variable as global

    # Read in world map data
    world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))

    # Create a function to get country name from a Point object
    def get_country_name(point):
        # Loop through each country
        for index, row in world.iterrows():
            # Check if the point is within the country's geometry
            if row["geometry"].contains(point):
                # Return the country name
                return row["name"]
        # Return None if no country contains the point
        return None

    # Create a function to handle click events
    def on_click(event):
        global country_name  # Access the global variable

        # Get the coordinates of the clicked point
        lon, lat = event.xdata, event.ydata
        # Create a Point object from the coordinates
        point = Point(lon, lat)
        # Get the name of the country at the clicked location
        country_name = get_country_name(point)
        # Close the map window
        plt.close()

    # Create a plot of the world map
    fig, ax = plt.subplots(figsize=(10, 6))
    world.plot(ax=ax)
    ax.set_title("World Map")
    plt.tight_layout()
    # Remove the toolbar from the plot
    plt.rcParams["toolbar"] = "None"
    # Add a click event listener to the plot
    cid = fig.canvas.mpl_connect("button_press_event", on_click)
    # Show the plot
    plt.show()


