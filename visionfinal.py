import cv2
import numpy as np
import pandas as pd
import face_recognition
import pyttsx3 as s
import speech_recognition as sr
import wikipedia
import webbrowser
from ecapture import ecapture as ec
import time
import datetime


engine = s.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

c = 0  #set camera

def speak(audio):
    engine.setProperty('rate', 150)  # Adjust speech rate
    engine.setProperty('volume', 0.8)  # Adjust volume
    engine.say(audio)
    engine.runAndWait()

def tellTime():
    time = str(datetime.datetime.now())
    hour = int(time[11:13])
    minute = time[14:16]

    # Determine whether it's AM or PM
    period = "AM"
    if hour >= 12:
        period = "PM"
        if hour > 12:
            hour -= 12  # Convert to 12-hour format

    # Handle the case when it's exactly 12:00
    if hour == 0:
        hour = 12

    speak("The time is " + str(hour) + " Hours and " + minute + " Minutes " + period)
    
def tellDate():
    current_date = datetime.datetime.now().strftime('%d-%m-%Y')
    speak("The date today is" + current_date)
    
def tellDay():
    day = datetime.datetime.today().weekday() + 1
    Day_dict = {1: 'Monday', 2: 'Tuesday',
                3: 'Wednesday', 4: 'Thursday',
                5: 'Friday', 6: 'Saturday',
                7: 'Sunday'}
     
    if day in Day_dict.keys():
        day_of_the_week = Day_dict[day]
        print(day_of_the_week)
        speak("The day is " + day_of_the_week)
        
def wishMe():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning!")
        speak("Hello I am your Humanoid Robot Receptionist. Tell me how may I help you.")

    elif 12 <= hour < 18:
        speak("Good Afternoon!")
        speak("Hello I am your Humanoid Robot Receptionist. Tell me how may I help you.")
    else:
        speak("Good Evening!") 
        speak("Hello I am your Humanoid Robot Receptionist. Tell me how may I help you.")


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        print("Listening...")
        audio = r.listen(source, phrase_time_limit=10)  # Adjust phrase time limit

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print(e)
        print("Say that again please...")
        return "None"
    return query


#def sendEmail(to, content):
 #   pass


def takeAttendance():
    r = sr.Recognizer()
    current_date = datetime.datetime.now().strftime('%d-%m-%Y')
    time = str(datetime.datetime.now())
    day = datetime.datetime.today().weekday() + 1
    Day_dict = {1: 'Monday', 2: 'Tuesday',
                3: 'Wednesday', 4: 'Thursday',
                5: 'Friday', 6: 'Saturday',
                7: 'Sunday'}
     
    if day in Day_dict.keys():
        day_of_the_week = Day_dict[day]
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = r.listen(source, phrase_time_limit=10)
        try:
            print("Recognizing...")

# Load the known images and encode them
            imgElon = face_recognition.load_image_file("C:/Users/Mohammad Shayan/Desktop/Face/Elon_Musk.jpg")
            imgElon_encoding = face_recognition.face_encodings(imgElon)[0]

            imgBill = face_recognition.load_image_file("C:/Users/Mohammad Shayan/Desktop/Face/Bill_Gates.jpeg")
            imgBill_encoding = face_recognition.face_encodings(imgBill)[0]

            imgshayan1 = face_recognition.load_image_file("C:/Users/Mohammad Shayan/Desktop/Face/Mohammad_Shayan.png")
            imgshayan1_encoding = face_recognition.face_encodings(imgshayan1)[0]

            imgshayan2 = face_recognition.load_image_file("C:/Users/Mohammad Shayan/Desktop/Face/Mohammad_Shayan1.jpg")
            imgshayan2_encoding = face_recognition.face_encodings(imgshayan2)[0]

            imgshahmeer = face_recognition.load_image_file("C:/Users/Mohammad Shayan/Desktop/Face/Shahmeer_Fareed.jpg")
            imgshahmeer_encoding = face_recognition.face_encodings(imgshahmeer)[0]

            imgshahmeer2 = face_recognition.load_image_file("C:/Users/Mohammad Shayan/Desktop/Face/Shahmeer_Fareed1.jpg")
            imgshahmeer2_encoding = face_recognition.face_encodings(imgshahmeer2)[0]


# Create a dictionary to keep track of attendance
            attendance = {
            day_of_the_week : time,
            "Elon Musk": False,
            "Bill Gates": False,
            "Mohammad Shayan" : False,
            "Mohammad Shayan" : False,
            "Shahmeer Fareed" : False,
            "Shahmeer Fareed" : False
            
    
            }

# Set up the camera
            cap = cv2.VideoCapture(c)

            while True:
    # Capture a frame
                ret, frame = cap.read()

    # Convert the frame to RGB format
                rgb_frame = frame[:, :, ::-1]

    # Detect faces in the frame
                face_locations = face_recognition.face_locations(rgb_frame)
                face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    # For each face, check if it matches a known face
                for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                    matches = face_recognition.compare_faces([imgElon_encoding, imgBill_encoding, imgshayan1_encoding, imgshayan2_encoding, imgshahmeer_encoding, imgshahmeer2_encoding], face_encoding)
                    name = "Unknown"

        # Find the best match
                    face_distances = face_recognition.face_distance([imgElon_encoding, imgBill_encoding, imgshayan1_encoding, imgshayan2_encoding, imgshahmeer_encoding, imgshahmeer2_encoding], face_encoding)
                    best_match_index = np.argmin(face_distances)

                    if matches[best_match_index]:
                        name = ["Elon Musk", "Bill Gates", "Mohammad Shayan", "Mohammad Shayan", "Shahmeer Fareed", "Shahmeer Fareed"][best_match_index]

            # Mark attendance for this person
                        attendance[name] = True

        # Draw a box around the face and label it
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                    cv2.putText(frame, name, (left, bottom+20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    # Display the resulting image
                cv2.imshow('Face Recognition', frame)

    # Exit the loop if the 'q' key is pressed
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

# Print the attendance report
            print("Attendance Report:")
            for name, present in attendance.items():
                print(name + ": " + ("Present" if present else "Haven't came yet"))

# Release the capture and destroy all windows
            cap.release()
            cv2.destroyAllWindows()



# Create a new DataFrame with the attendance data
            df = pd.DataFrame(list(attendance.items()), columns=['Name', 'Present'])

# Write the DataFrame to an Excel file
            filename = f'attendance_{current_date}.xlsx'
            df.to_excel(filename, index=False)
            print(f"Attendance data saved to {filename}")
            speak("Your attendance has been Marked")
        except Exception as e:
            print(e)
            print("Say that again please...")
            return

if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()
        if 'attendance' in query:
            speak('Sure')
            takeAttendance()
        elif "shayan" in query:
            speak("Shayan is the student of batch 22 0 9 E 0 1 in aptech garden center")
            continue
        elif "shahmeer" in query:
            speak("Shahmeer is the student of batch 22 0 9 E 0 1 in aptech garden center")
            continue
        elif "open google" in query:
            speak("Opening Google")
            webbrowser.open("www.google.com")
            continue 
        elif "day" in query:
                tellDay()
                continue
        elif "time" in query:
                tellTime()
                continue
        elif "date" in query:
                tellDate()
                continue
        elif "from wikipedia" in query:
                speak("Checking Wikipedia")
                query = query.replace("wikipedia", "")
                result = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                speak(result)
                continue
        elif "your name" in query:
                speak("I your Humanoid Robot Receptionist.")
                continue
        elif "camera" in query or "take a photo" in query:
                ec.capture(c,"camera","img.jpg")
                continue
        elif 'search'  in query:
             query = query.replace("search", "")
             webbrowser.open_new_tab(query)
             time.sleep(5)
             continue
        elif  'bye' in query:
            speak("Bye. Do remeber me if you need any assistance. Thank you!")
            exit()
        else:
            speak('Sorry, I didn\'t understand what you said. Please try again.')
