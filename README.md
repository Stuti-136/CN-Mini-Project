# Distributed Leaderboard Management System
*Computer Networks Mini Project*

This project implements a real-time leaderboard system using a TCP client-server architecture. It allows multiple users to register, log in, participate in a quiz, and update their scores, which are reflected in a dynamic leaderboard.

## Features
-> Multi-client support using sockets
-> User registration and login system
-> Real-time leaderboard updates
-> Quiz-based score generation
-> GUI interface using Tkinter
-> MongoDB database integration
-> Thread-safe concurrent updates

## Technologies Used
-> Python (Socket Programming, Tkinter)
-> MongoDB (Database)
-> Multithreading

### Requirements
i) Python 3.x
ii) MongoDB
iii) pymongo library

Install dependencies:
pip install pymongo

## How to Run the Project
### 1. Start MongoDB
Make sure MongoDB is running on your system.
### 2. Run the Server
Open terminal and run:
python server.py
### 3. Run the Client
Open another terminal and run:
python client_gui.py
