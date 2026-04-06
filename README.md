# Distributed Leaderboard Management System
*Computer Networks Mini Project*

This project implements a real-time leaderboard system using a TCP client-server architecture. It allows multiple users to register, log in, participate in a quiz, and update their scores, which are reflected in a dynamic leaderboard.

## Features
- Multi-client support using sockets
- User registration and login system
- Real-time leaderboard updates
- Quiz-based score generation
- GUI interface using Tkinter
- MongoDB database integration
- Thread-safe concurrent updates

## Technologies Used
- Python (Socket Programming, Tkinter)
- MongoDB (Database)
- Multithreading

## Requirements
- Python 3.x
- MongoDB
- pymongo library

Install dependencies:
pip install pymongo

## How to Run
### 1. Start MongoDB
Make sure MongoDB is running on your system.

### 2. Run the Server
Open terminal and run:
python server.py

### 3. Run the Client
Open another terminal and run:
python client_gui.py

## Running with Multiple Clients (Different Devices)
To connect multiple clients from different systems over a network:
### Server Setup
- Update binding to allow external connections:
server.bind(("0.0.0.0", 12345))
- Run the server on one system
- Find server IPv4 address using ipconfig (in Windows)
### Client Setup
- On other systems update:
  client.connect(("SERVER_IP_ADDRESS", 12345))
- Run client_gui on multiple systems
- All clients will connect to the same server and share the leaderboard

## How It Works
1. The server handles multiple clients using threads.
2. Users register/login through the GUI.
3. Users take a quiz and receive a score.
4. Scores are stored in MongoDB.
5. Leaderboard is updated and displayed in real-time.

## Future Scope
- Implement real-time leaderboard updates without manual refresh
- GUI with better design and user experience
- Add difficulty levels and more questions in the quiz
- Deploy the system on cloud for remote access
- Add secure authentication (hashed passwords) 
- Support more advanced ranking algorithms
