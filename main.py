import time
import board
import adafruit_dht
import threading
import requests
import tensorflow as tf
from sklearn.preprocessing import StandardScaler

# Sensor data pin is connected to GPIO 4
sensor = adafruit_dht.DHT11(board.D4)
temp = 0.0
hum = 0.0
pred = 0.0

# Load model
model_path = '/home/pi/dishan/Pi_iot_ml/my_model.h5'
model = tf.keras.models.load_model(model_path)

# StandardScaler for data preprocessing
scaler = StandardScaler()
scaler.fit([[0, 0, 0]])  # Fit with dummy data, assuming shape [temperature, humidity, pressure]

# Replace with your ThingSpeak Channel ID and Write API Key
channel_id = "Y2453103"
write_api_key = "PUJNPO73X3G2AT56"

# Termination flag for threads
terminate_threads = False

def dht_read():
    global temp, hum
    try:
        # Print the values to the serial port
        temperature_c = sensor.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = sensor.humidity
        print("Temp={0:0.1f}ºC, Temp={1:0.1f}ºF, Humidity={2:0.1f}%".format(temperature_c, temperature_f, humidity))
        time.sleep(0.1)
        return temperature_c, humidity

    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(2.0)
    except Exception as error:
        sensor.exit()
        raise error

def data_preprocess(t, h):
    data = [[t, h, 1016]]
    scaled_data = scaler.transform(data)
    scaled_temperature, scaled_humidity, scaled_p = scaled_data[0]
    return scaled_temperature, scaled_humidity, scaled_p

def data_pred():
    global temp, hum, pred
    while not terminate_threads:
        try:
            temp, hum = dht_read()
            scaled_temperature, scaled_humidity, scaled_p = data_preprocess(temp, hum)
            data = [[scaled_temperature, scaled_humidity, scaled_p]]
            pred_array = model.predict(data)
            
            # Extract the float value from the NumPy array
            pred = float(pred_array[0][0])
            
            print("Predicted Rain: {:.2f}".format(pred))
        except Exception as e:
            print(f"Error in data_pred thread: {e}")
        finally:
            time.sleep(2.0)



def data_send():
    global temp, hum, pred
    while not terminate_threads:
        time.sleep(0.3)
        data = {"Temp": temp, "Humidity": hum, "Rain": pred}
        base_url = f"https://api.thingspeak.com/update?api_key={write_api_key}"
        
        try:
            response = requests.post(base_url, data=data)
            if response.status_code == 200:
                print("Data sent successfully!")
                print(temp,hum,pred)
            else:
                print(f"Error sending data: {response.status_code}")
        except Exception as e:
            print(f"Error sending data: {e}")

# Threads
sensor_thread = threading.Thread(target=data_pred)
cloud_thread = threading.Thread(target=data_send)

# Start threads
sensor_thread.start()
cloud_thread.start()


