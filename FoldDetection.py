import base64
import cv2
import speech_recognition as sr
from openai import OpenAI
import socket
import pyttsx3

# Initialize OpenAI client with API key
client = OpenAI()
engine = pyttsx3.init()

def initialize_voice():
    """Sets the desired voice properties like language and speaking rate."""
    voices = engine.getProperty('voices')
    selected_voice_index = 100 
    engine.setProperty('voice', voices[selected_voice_index].id)

def speak(text):
    """Speaks the given text."""
    engine.say(text)
    engine.runAndWait()
    return


def encode_image(image_path):
    """Encodes an image to base64 format."""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    except FileNotFoundError:
        print(f"Error: The file {image_path} was not found.")
        return None


def capture_image(step):
    """Captures an image from the webcam and saves it with a step-specific name."""
    output_path = f"step_{step}.png"
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    if ret:
        cv2.imwrite(output_path, frame)
        print(f"Image for step {step} saved to {output_path}")
        return output_path
    else:
        print("Error: Failed to capture image from webcam.")
        return None


def query_llm(instruction, groundtruth, current, past):
    if groundtruth == "":
        response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
          {
            "role": "user",
            "content": [
              {
                "type": "text",
                "text": f"{instruction}",
              },
              {
                "type": "image_url",
                "image_url": {
                  "url":  f"data:image/jpeg;base64,{current}",
                },
              },
            ]
          }
        ]
        )
    else:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
              {
                "role": "user",
                "content": [
                  {
                    "type": "text",
                    "text": f"all three images contain a sheet of paper. Currently we are analyzing the second/current sheet of paper to see if the correct origami fold occured. The instruction was to {instruction}. Does the second/current sheet of paper look like the result of applying this instruction to the third/past sheet of paper or does it look very similar to the first/groundtruth sheet of paper, if either is true, then it works! explain why or why not. Format your answer with either amazing or horrible at the start based on your answer ",
                  },
                  {
                    "type": "image_url",
                    "image_url": {
                      "url":  f"data:image/jpeg;base64,{groundtruth}",
                    },
                  },
                  {
                    "type": "image_url",
                    "image_url": {
                      "url":  f"data:image/jpeg;base64,{current}",
                    },
                  },
                  {
                    "type": "image_url",
                    "image_url": {
                      "url":  f"data:image/jpeg;base64,{past}",
                    },
                  },
                ],
              }
            ],
        )
    return response.choices[0].message.content



def listen_for_trigger():
    """
    Listens for a trigger word from the user to capture an image.

    :return: True if the user says "capture," otherwise False.
    """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Adjusting for ambient noise. Please wait...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        speak("Say 'capture' to take an image...")
        print("Say 'capture' to take an image...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
            user_input = recognizer.recognize_google(audio)
            if "capture" in user_input.lower():
                print("Capture command detected!")
                return 1
            if "skip" in user_input.lower():
                print("skipping step")
                return 2
        except sr.WaitTimeoutError:
            print("No speech detected within the timeout period.")
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand what you said.")
        except sr.RequestError as e:
            print(f"Microphone error: {e}")
        return 0

#verify first sheet of paper
def verify_flat_sheet():
    """Ensures the initial step contains a flat sheet of paper."""
    while True:
        if listen_for_trigger():
            image_path = capture_image(0)
            if not image_path:
                continue

            base64_image = encode_image(image_path)
            if not base64_image:
                continue

            instruction = "Does the image contain a flat sheet of paper? Respond with 'yes' or 'no'."
            response = query_llm(instruction,"", base64_image, "")
            print(f"LLM Flat Sheet Check Response: {response}")

            if "yes" in response.lower():
                print("Flat sheet verified.")
                speak("next step!")
                sock.sendto("yes".encode(), (UDP_IP, UDP_PORT))
                return base64_image
            else:
                speak("check and make sure you have a flat sheet of paper oriented properly.")
                print("The sheet is not flat. Please adjust and recapture.")

#dictionary if instructions and the names of your ground thruth images
instructions = {
    1: {
        "instruction": "Fold the right edge over to the left edge of the sheet of paper forming a triangle shape.",
        "ground_truth": "true_0.png"
    },
    2: {
        "instruction": "Unfold the sheet of paper; this should leave a crease down the middle and a diamond shape.",
        "ground_truth": "true_1.png"
    },
    3: {
        "instruction": "Fold the right and left edge of the sheet of paper and align it with the crease in the middle.",
        "ground_truth": "true_2.png"
    },
    4: {
        "instruction": "Rotate the sheet of paper so that the wide end is at the bottom.",
        "ground_truth": "true_3.png"
    },
    5: {
        "instruction": "Fold the bottom point of the sheet of paper to meet the bottom of the two left and right front flaps.",
        "ground_truth": "true_4.png"
    },
    6: {
        "instruction": "Fold the lower left and right diagonal edges of the sheet of paper to align with the central vertical crease.",
        "ground_truth": "true_5.png"
    },
    7: {
        "instruction": "Fold the sheet of paper in half horizantally by bringing the bottom edge up, the end should look like a triangle.",
        "ground_truth": "true_6.png"
    },
    8: {
        "instruction": "Fold the front flap of the sheet of paper back down, leaving a small overlap behind.",
        "ground_truth": "true_7.png"
    },
    9: {
        "instruction": "Flip the sheet of paper over.",
        "ground_truth": "true_8.png"
    }
}


# Main execution
if __name__ == "__main__":
    #IP of meta headset
    UDP_IP = "172.26.167.181"
    UDP_PORT = 6005

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    initialize_voice()
    previous_image_base64 = verify_flat_sheet()
    current_step = 1
    previous_ground_truth_path = ""

    while current_step in instructions:
        print(f"Waiting for user to capture an image for step {current_step}...")

        x = listen_for_trigger()
        if x > 0:
            current_image_path = capture_image(current_step)
            if not current_image_path:
                continue

            current_image_base64 = encode_image(current_image_path)
            if not current_image_base64:
                continue


            # Load the ground truth image for the current step
            ground_truth_path =instructions[current_step]["ground_truth"]
            ground_truth_base64 = encode_image(ground_truth_path)
            if not ground_truth_base64:
                print("Error: Could not load ground truth image.")
                continue
            if not previous_image_base64:
                print("Error: Could not load ground truth image.")
                continue

            # Get theinstruction for the current step
            instruction = instructions[current_step]["instruction"]

            # Query the LLM with the user image and the ground truth
            speak("Processing")
            
            if x == 2:
                current_step += 1
                previous_image_base64 = current_image_base64
                sock.sendto("yes".encode(), (UDP_IP, UDP_PORT))
                continue

            response = query_llm(instruction, ground_truth_base64, current_image_base64, previous_image_base64)
            print(f"LLM Response: {response}")

            if "amazing" in response.lower():
                print("Step completed. Moving to the next step.")
                speak("Step completed..")
                current_step += 1
                previous_image_base64 = current_image_base64
                sock.sendto("yes".encode(), (UDP_IP, UDP_PORT))
                
            else:
                speak("check your fold again.")
                print("Step validation failed. Repeating the current step.")
        
