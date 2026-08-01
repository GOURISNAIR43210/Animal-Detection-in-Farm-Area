# 🐗 Animal Detection in Farm Area using YOLOv8 and Django

An AI-powered web application that detects animals entering farm areas using deep learning. The system enables users to upload surveillance videos, automatically identifies animals using a custom-trained YOLOv8 model, and displays the detection results through a Django-based web interface.

---

## 📖 Project Overview

Crop damage caused by wild animals is a significant challenge in agriculture. This project aims to provide an intelligent and automated solution for monitoring farm areas by detecting animals from uploaded surveillance videos.

The application combines **Computer Vision**, **Deep Learning**, and **Web Development** technologies to build a smart farm monitoring system.

---

## ✨ Features

- 📤 Upload surveillance videos
- 🤖 AI-powered animal detection
- 🎥 Video frame processing
- ⚡ Fast YOLOv8 inference
- 🌐 Django web application
- 📱 Responsive user interface
- 🔊 Plays corresponding animal alert sound
- 📊 Displays final detected animal
- 🚫 Returns "No Animal Detected" when no target animal is found

---

## 🐾 Animals Detected

- 🐗 Wild Boar
- 🐄 Cattle
- 🐕 Dog
- 🐒 Monkey

---

## 🛠 Technologies Used

### Programming Language
- Python

### Web Framework
- Django

### Deep Learning
- YOLOv8 (Ultralytics)

### Computer Vision
- OpenCV

### Machine Learning
- PyTorch
- Torchvision

### Frontend
- HTML5
- CSS3
- Bootstrap
- JavaScript

### Version Control
- Git
- GitHub

---

## 📂 Project Structure

```
Animal-Detection-in-Farm-Area/
│
├── Crops/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│
├── detection/
│   ├── views.py
│   ├── urls.py
│   ├── models.py
│
├── ml/
│   ├── detect_video.py
│   ├── best.pt
│
├── templates/
│   ├── index.html
│   ├── detect.html
│   ├── result.html
│
├── static/
│   ├── css/
│   ├── js/
│   ├── images/
│   └── sounds/
│
├── media/
├── requirements.txt
├── runtime.txt
├── Dockerfile
├── manage.py
└── README.md
```

---

## ⚙️ Workflow

1. User opens the web application.
2. User uploads a surveillance video.
3. Django stores the uploaded video.
4. OpenCV extracts frames from the video.
5. YOLOv8 detects animals in each frame.
6. Detection confidence scores are calculated.
7. A weighted scoring algorithm determines the final prediction.
8. The detected animal is displayed on the result page.
9. The corresponding alert sound is played.

---

## 🧠 Detection Pipeline

```
Video Upload
      │
      ▼
Frame Extraction
      │
      ▼
Image Preprocessing
      │
      ▼
YOLOv8 Detection
      │
      ▼
Confidence Scoring
      │
      ▼
Frame Voting
      │
      ▼
Final Animal Prediction
      │
      ▼
Display Result
```

---

## 📷 Sample Output

| Uploaded Video | Prediction |
|----------------|------------|
| Wild Boar | 🐗 Wild Boar |
| Goat | 🐐 Goat |
| Dog | 🐕 Dog |
| Monkey | 🐒 Monkey |
| Cow | 🐄 Cattle |
| Empty Field | No Animal Detected |

---

## 🚀 Installation

### Clone Repository

```bash
git clone https://github.com/GOURISNAIR43210/Animal-Detection-in-Farm-Area.git
```

### Go to Project Folder

```bash
cd Animal-Detection-in-Farm-Area
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / Mac

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Apply Migrations

```bash
python manage.py migrate
```

### Start Server

```bash
python manage.py runserver
```

Open your browser and visit:

```
http://127.0.0.1:8000/
```

---

## 📦 Main Python Libraries

- Django
- Ultralytics
- OpenCV
- PyTorch
- Torchvision
- NumPy
- Pillow
- Python-dotenv
- Twilio (Optional)

---

## 📈 Future Enhancements

- 📹 Live CCTV camera support
- 📱 Mobile application
- ☁ Cloud deployment
- 📩 SMS notification
- 📧 Email alerts
- 📊 Detection history dashboard
- 📍 GPS-enabled farm monitoring
- 🌐 Multi-user authentication
- 📈 Detection analytics
- 🔔 Real-time notification system

---

## 🌱 Applications

- Smart Agriculture
- Precision Farming
- Wildlife Monitoring
- Farm Security
- Crop Protection
- AI-based Surveillance
- Animal Intrusion Detection

---

## 📸 Screenshots

### Home Page

<img width="887" height="380" alt="image" src="https://github.com/user-attachments/assets/1a50e3a1-3904-49a7-b462-eca3b2cb7179" />


---

### Upload Page

<img width="925" height="413" alt="Screenshot 2026-08-01 223452" src="https://github.com/user-attachments/assets/8398e6e6-0f2f-45ca-8f2f-1102841a098d" />


---

### Detection Result

<img width="882" height="411" alt="image" src="https://github.com/user-attachments/assets/e6531c0c-74ce-424a-ba7e-f9a9bcee51b0" />


---

## 🎯 Skills Demonstrated

- Python Programming
- Django Web Development
- Computer Vision
- Deep Learning
- YOLOv8
- OpenCV
- Machine Learning
- Video Processing
- Git & GitHub
- Backend Development
- Responsive Web Design

---

## 💼 Challenges Faced

- Integrating YOLOv8 with Django
- Processing uploaded videos efficiently
- Improving detection accuracy
- Reducing false positives
- Optimizing inference time
- Managing deployment dependencies

---

## 📚 Learning Outcomes

This project helped me gain practical experience in:

- Developing AI-powered web applications
- Integrating deep learning models into web frameworks
- Processing videos using OpenCV
- Building responsive user interfaces
- Managing project dependencies
- Using Git and GitHub for version control

---

## 👨‍💻 About the Developer

**Gouri S Nair**

🎓 M.Tech Student  
**Computer Science and Engineering**

I am passionate about Artificial Intelligence, Computer Vision, Machine Learning, and Full-Stack Web Development. I enjoy building intelligent systems that solve real-world problems through AI and software engineering.

### Connect with Me

**GitHub:**  
https://github.com/GOURISNAIR43210

---

## 📄 License

This project is developed for educational and research purposes.

© 2026 Gouri S Nair. All Rights Reserved.
