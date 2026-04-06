import socket
import threading
from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://localhost:27017/")
db = client["leaderboardDB"]
collection = db["scores"]

lock = threading.Lock()

users = {}

def register(username, password):
    if username in users:
        return "User already exists"
    users[username] = password
    return "Registered successfully"

def login(username, password):
    if users.get(username) == password:
        return "Login successful"
    return "Invalid credentials"

def update_score(username, score):
    with lock:
        existing = collection.find_one({"username": username})

        if existing:
            if score > existing["score"]:
                collection.update_one(
                    {"username": username},
                    {"$set": {"score": score, "timestamp": datetime.now()}}
                )
        else:
            collection.insert_one({
                "username": username,
                "score": score,
                "timestamp": datetime.now()
            })

def get_leaderboard():
    data = list(collection.find().sort("score", -1))
    result = []
    rank = 1

    for item in data:
        suffix = "th"
        if rank == 1: suffix = "st"
        elif rank == 2: suffix = "nd"
        elif rank == 3: suffix = "rd"

        result.append(f"{rank}{suffix} - {item['username']}: {item['score']}")
        rank += 1

    return "\n".join(result)

def handle_client(client_socket):
    logged_in_user = None

    while True:
        try:
            data = client_socket.recv(1024).decode().strip()
            if not data:
                break

            print("Received:", data)

            parts = data.split()

            if parts[0] == "REGISTER":
                response = register(parts[1], parts[2])
                print("Sending:", response)
                client_socket.send((response + "\n").encode())

            elif parts[0] == "LOGIN":
                response = login(parts[1], parts[2])
                if response == "Login successful":
                    logged_in_user = parts[1]
                print("Sending:", response)
                client_socket.send((response + "\n").encode())

            elif parts[0] == "UPDATE":
                if not logged_in_user:
                    print("Sending: Login first")
                    client_socket.send("Login first\n".encode())
                    continue

                score = int(parts[1])
                update_score(logged_in_user, score)
                print("Sending: Score updated")
                client_socket.send("Score updated\n".encode())

            elif parts[0] == "GET":
                leaderboard = get_leaderboard()
                print("Sending leaderboard")
                client_socket.send((leaderboard + "\n").encode())

        except Exception as e:
            print("Error:", e)
            break

    client_socket.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 12345))
server.listen(5)

print("Server running...")

while True:
    client_socket, addr = server.accept()
    thread = threading.Thread(target=handle_client, args=(client_socket,))
    thread.start()