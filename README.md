# API Chat

## Introduction

Welcome to **API Chat**, a cutting-edge Python-based chat application designed to facilitate seamless communication through a RESTful API. This project provides a robust foundation for building chat functionalities, enabling users to send and receive messages efficiently. The application leverages advanced technologies to offer a unique blend of traditional chat features and innovative astrology integration.

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Folder Structure](#folder-structure)
- [Getting Started](#getting-started)
- [API Endpoints](#api-endpoints)
- [Deployement](#deployement)
- [License](#license)
- [Contact](#contact)

## Features

- **Message Sending**: Allows users to send messages to the chat server, ensuring efficient communication.
- **Message Retrieval**: Enables users to retrieve messages from the chat server, facilitating easy access to conversation history.
- **User Management**: Supports functionalities for user registration and authentication, ensuring a secure and personalized experience.
- **Astrology Integration**: Provides features for generating horoscopes, Advices, Recommendations, Sleep Schedules, birth charts, gemstone recommendations and much more based on user input, offering a unique and engaging experience.

## Tech Stack

- **Python**: The primary programming language used for developing the application, ensuring a robust and scalable foundation.
- **Flask**: A lightweight WSGI web application framework used for building the RESTful API, providing a flexible and modular architecture.
- **Docker**: Utilized for containerizing the application to ensure consistency across different environments, simplifying deployment and management.
- **FastAPI**: Used for building the astrology integration features, offering a fast and efficient way to handle complex calculations and data processing.
- **Groq**: Utilized for generating AI-enhanced predictions and advice, providing users with personalized insights and guidance.
- **OpenCage Geocoder**: Used for geocoding locations for astrology calculations, ensuring accurate and reliable data processing.
- **Swisseph**: Utilized for calculating planetary positions and generating birth charts, offering a comprehensive and accurate astrology integration.
- **AWS**: Hosted on AWS, ensuring high availability and scalability.

## Folder Structure

```
api-chat/
├── components/
│   ├── BirthTransit.py
│   ├── FindHoroscope.py
│   ├── Prediction.py
│   └── CurrentTransit.py
│   └── Kundli.py
├── assets/
│   ├── Images
├── Horoscope/
│   ├── Cache
├── main.py
├── gems.py
├── DockerFile
├── requirements.txt
├── LICENSE
└── README.md
```

## Getting Started

### Prerequisites

- **Python 3.x**: Ensure that Python is installed on your system, as it is the primary language used for the application.
- **Docker**: Required for containerizing and running the application, ensuring a consistent and reliable environment.

### Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/NeonKazuha/api-chat.git
   cd api-chat
   ```

2. **Install Dependencies**:

   It's recommended to use a virtual environment to manage dependencies, ensuring a clean and isolated environment for the application.

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. **Run the Application**:

   ```bash
   python main.py
   ```

   The application will start, and you can access the API endpoints at `http://localhost:8000`.

### Docker Setup

To run the application using Docker:

1. **Build the Docker Image**:

   ```bash
   docker build -t api-chat .
   ```

2. **Run the Docker Container**:

   ```bash
   docker run -p 8000:8000 api-chat
   ```

   The API will be accessible at `http://localhost:8000`.

   Additionally, to run the gemstone recommendations service, use the following command:

   ```bash
   docker run -p 4000:4000 api-chat-gems
   ```

   The gemstone recommendations service will be accessible at `http://localhost:4000`.

## API Endpoints

- **`POST /horoscope/`**: Endpoint to generate horoscope data, offering users personalized astrology insights.
- **`POST /gemstones/`**: Endpoint to get gemstone recommendations based on location, providing users with unique and personalized suggestions.
  
## Deployement

http://13.203.67.150:4000/gemstones

![Screenshot 2025-01-19 072527](https://github.com/user-attachments/assets/c315ca4c-42a6-4e6c-949e-3595f5f4de2c)

http://13.203.67.150/horoscope

![Screenshot 2025-01-19 072737](https://github.com/user-attachments/assets/61addf94-cf62-4155-81fe-6d9b9e12cbca)
![Screenshot 2025-01-19 072802](https://github.com/user-attachments/assets/4d5bbc3a-8006-422b-9908-da2e59e5df1a)
![Screenshot 2025-01-19 072813](https://github.com/user-attachments/assets/ade14706-4fab-4227-99af-d477d8a97188)

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/NeonKazuha/api-chat/blob/main/LICENSE) file for details.

## Contact

For any inquiries or issues, please open an issue on the GitHub repository, ensuring a transparent and open communication channel.
