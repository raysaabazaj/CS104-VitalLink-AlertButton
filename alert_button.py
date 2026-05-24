import requests
import time
import RPi.GPIO as GPIO

# --- Configuration ---
# Your full API URL including the token
# --- GPIO Setup ---
GPIO.setmode(GPIO.BOARD)
# Pin 7 (Hardware Board Pin)
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def send_telegram_alert():
    try:
        payload = {
            "chat_id": CHAT_ID,
            "text": "Pressed Button!"
        }
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            print("Alert sent successfully!")
        else:
            print(f"Error: {response.status_code}")
    except Exception as e:
        print(f"Failed to send request: {e}")

print("System Ready. Press the button to send an alert...")

button_pressed = False

try:
    while True:
        # Detect press
        if GPIO.input(7) == GPIO.HIGH and not button_pressed:
            print("Button detected!")
            send_telegram_alert()
            button_pressed = True # Prevents spamming while holding the button
        
        # Detect release
        elif GPIO.input(7) == GPIO.LOW:
            button_pressed = False
            
        time.sleep(0.05) # Short debounce delay

except KeyboardInterrupt:
    print("Cleaning up...")
    GPIO.cleanup()

