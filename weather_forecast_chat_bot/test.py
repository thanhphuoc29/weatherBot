
import matplotlib.pyplot as plt
from PIL import Image
temperatures = [25, 26, 27, 26, 25, 23, 22]

# Create a list of days of the week
days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

# Plot the temperature data as a line graph
plt.plot(days, temperatures)

# Add labels to the x and y axes
plt.xlabel('Day')
plt.ylabel('Temperature (C)')

# Add a title to the graph
plt.title('Weekly Temperature Forecast')

# Convert the graph to an image
fig = plt.gcf()
fig.canvas.draw()
image = Image.frombytes(
    'RGB', fig.canvas.get_width_height(), fig.canvas.tostring_rgb())

# Display the image
image.show()
