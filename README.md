# Raspberry Pi IoT with Machine Learning Prediction

Welcome to the Raspberry Pi IoT with Machine Learning Prediction project! This guide walks you through the code that reads sensor data from a Raspberry Pi, makes predictions using a pre-trained machine learning model, and sends the data to ThingSpeak for visualization.

## Components:

- **Raspberry Pi:** A single-board computer serving as the data collection and processing device.
- **DHT11 sensor:** A temperature and humidity sensor connected to the Raspberry Pi.
- **Machine Learning model:** A pre-trained TensorFlow model saved on the Raspberry Pi (model file: my_model.h5). This model predicts rain probability based on sensor readings.
- **ThingSpeak:** A cloud platform for storing and visualizing sensor data.

## Functionality:

### Sensor Data Collection:

The code reads temperature and humidity values from the DHT11 sensor connected to the Raspberry Pi's GPIO pin 4.
Error-handling mechanisms are in place to manage potential issues during sensor communication.

### Data Preprocessing:

The collected data (temperature and humidity) is scaled for better compatibility with the machine learning model. Scaling enhances the model's prediction accuracy.
Currently, the code uses placeholder data for initial scaling. Adjust this to use more representative data from your environment.

### Machine Learning Prediction:

The scaled sensor data is fed into the pre-trained machine learning model (my_model.h5).
The model predicts the probability of rain based on the temperature and humidity readings.

### Data Transmission to ThingSpeak:

The collected sensor readings (temperature, humidity) and the predicted rain probability are packaged together.
The data is sent to your ThingSpeak channel using the internet connection on your Raspberry Pi. Your ThingSpeak channel requires a Channel ID and Write API Key for secure communication (refer to ThingSpeak's documentation for setup).
Upon successful transmission, you can view the data on your ThingSpeak channel's dashboard.

## Code Structure:

The code is organized into several functions for better readability and maintainability:

- **dht_read:** Reads data from the DHT11 sensor.
- **data_preprocess:** Scales the sensor data.
- **data_pred:** Runs in a separate thread to collect sensor data, preprocess it, and make predictions using the model.
- **data_send:** Runs in another thread to send the collected sensor data and prediction to ThingSpeak.

## Additional Considerations:

- Ensure the file path (model_path) and model format (my_model.h5) are correct for loading the TensorFlow model.
- Adjust sleep intervals (time.sleep) in the code based on your desired sensor reading frequency and data transmission needs.
- Consider logging errors to a file for better debugging and analysis.
- Add comments to the code to explain specific sections for future reference.

## Getting Started:

### Setup:

1. Connect the DHT11 sensor to your Raspberry Pi according to the sensor's wiring diagram.  ![circuit](https://i0.wp.com/randomnerdtutorials.com/wp-content/uploads/2023/08/Raspberry-Pi-DHT-Circuit_bb.png?quality=100&strip=all&ssl=1)

2. Install the required Python libraries: `pip install -r requirements.txt`
3. Ensure you have a pre-trained TensorFlow model (my_model.h5) saved on your Raspberry Pi that predicts rain probability based on temperature and humidity.
4. Create a ThingSpeak account at [ThingSpeak](https://thingspeak.com/).
5. Click on "Channels" and then "Create New Channel."
6. Give your channel a name and description (e.g., "Raspberry Pi Data").
7. Choose the number of fields you want to send data to (up to 8). These fields will represent different data points (e.g., temperature, humidity).
8. Click "Save Channel." You will be provided with a Channel ID and Write API Key.

### Modify the Code:

1. Replace the placeholder data in the `data_preprocess` function with more relevant values for your environment.
2. Update `channel_id` and `write_api_key` variables with your ThingSpeak channel credentials.

### Run the Code:

1. Save the code as a Python file (e.g., `main.py`).
2. Open a terminal on your Raspberry Pi and navigate to the directory where you saved the file.
3. Run the script using the following command: `python3 main.py`

### Verify Data:

If successful, you should see sensor readings and predicted rain probability printed in the terminal.
Log in to your ThingSpeak channel's dashboard. You should see the data points (temperature, humidity, and rain prediction) being uploaded and displayed in real-time or through graphs.

## Conclusion:

This code demonstrates how to leverage a Raspberry Pi, sensor data, and a pre-trained machine learning model to create an IoT application that sends valuable insights (including predictions) to a cloud platform like ThingSpeak. By customizing the code and model, you can build more advanced IoT projects for various applications.
