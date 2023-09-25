# **Description**

Supernova Surfers' PocketQube is a meticulously designed satellite tailored for a rocket flight reaching altitudes of up to 9000m. Our primary objective is to capture a diverse range of data encompassing pressure, temperature, altitude, humidity, orientation, and location during the anticipated rocket flight. Post-flight, our team will delve deep into this data, aiming to extract valuable insights about the flight dynamics and the surrounding environment.

# **Used Hardware:**
Arduino Nano Every, GY-91 (BMP280 & MPU9250), DHT22, MQ131, MQ135, SD Card Module, and an onboard buzzer.

Given the memory constraints associated with the Arduino Nano Every, coupled with our ambition to achieve rapid data recording rates (we've successfully achieved rates up to 20Hz), the flight-centric version of our program is laser-focused on recording data to the SD card in ".txt" format. It abstains from real-time data processing, allowing for comprehensive post-flight analysis. To ensure optimal performance during the flight, we've minimized debugging methods, retaining only essential indicators like the Nano's LED and specific EEPROM logs. However, specialized debugging versions, crafted to assist during the project's development phase, are available.

For the post-flight data analysis, we'll leverage spreadsheet tools for their graphing capabilities, utilize frameworks like Matplotlib, and employ a unique Flight Replay feature. This feature enables our PocketQube to read and simulate data from the SD card as if it were real-time sensor data. To visualize this data and potentially simulate the flight in 3D, we're considering tools like Processing 3/4 or similar software, connecting directly to our device via USB.

# **Functional Diagram:**
Supernova Surfers' PocketQube Functional Diagram Image

# **Repository Structure:**
Dive into our repository, structured as follows:

# **Code:**
Houses the Arduino source code tailored for both flight and debugging. Additionally, you'll find software for 3D visualizations, including Processing sketches.

# **Schematic:** 
Discover the intricate circuit schematic that powers our PocketQube.
<img width="1754" alt="SCHEMA ELECTRONICA" src="SCHEMA ELECTRONICA.png">


# **PCB:** 
Delve into the Gerber files for our custom-designed PCBs. Our PocketQube boasts 5 stacked PCBs, interconnected using wires.
