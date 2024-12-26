import socket
import random
import requests
import threading
import tkinter as tk
from tkinter import ttk, messagebox

# Server Side Code
def fetch_questions(category_id):
    url = f"https://opentdb.com/api.php?amount=10&category={category_id}&type=multiple"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data['results']
    else:
        print("Failed to fetch questions from the API")
        return []

class QuizServer:
    def __init__(self, host="127.0.0.1", port=12345):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        self.categories = [
            "General Knowledge", "Science", "Geography", "Science & Nature",
            "Sports", "History", "Entertainment: Film",
            "Entertainment: Music", "Mythology", "Art"
        ]
        print("Server started on", host, ":", port)

    def start(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"New connection: {client_address}")
            # Start a new thread to handle the client without blocking the server
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

    def handle_client(self, client_socket):
        try:
            # Receive player name from client
            player_name = client_socket.recv(1024).decode()
            if not player_name:
                player_name = "Player"
            print(f"Player's name: {player_name}")
            # client_socket.send(f"Welcome {player_name} to the Quiz Game!".encode())

            # Send categories to client
            categories = "\n".join(self.categories)
            client_socket.send(f"Available Categories:\n{categories}".encode())

            while True:
                score = 0
                category = client_socket.recv(1024).decode()
                if not category:
                    break
                print(f"Client selected category: {category}")
                category_id = self.get_category_id(category)
                questions = fetch_questions(category_id)
                if questions:
                    for question in questions:
                        question_text = question['question']
                        options = question['incorrect_answers'] + [question['correct_answer']]
                        random.shuffle(options)
                        question_data = f"{question_text}\n" + "\n".join(options)
                        client_socket.send(question_data.encode())
                        feedback = client_socket.recv(1024).decode()
                        correct_answer = question['correct_answer']
                        selected_answer = options[int(feedback) - 1]

                        # Check if the answer is correct and update score
                        if selected_answer == correct_answer:
                            client_socket.send(f"Correct! The answer was {correct_answer}".encode())
                            score += 1
                        else:
                            client_socket.send(f"Incorrect! The correct answer was {correct_answer}, but you selected {selected_answer}".encode())

                    # Send final score after quiz is completed
                    client_socket.send(f"Quiz completed! {player_name}, your final score is: {score}/10".encode())
                    # Display the client's score on the server
                    print(f"Player {player_name}'s final score: {score}/10")
        except Exception as e:
            print(f"Error with client: {e}")
        finally:
            client_socket.close()

    def get_category_id(self, category_name):
        categories_map = {
            "General Knowledge": 9,
            "Science": 17,
            "Geography": 22,
            "Science & Nature": 17,
            "Sports": 21,
            "History": 23,
            "Entertainment: Film": 11,
            "Entertainment: Music": 12,
            "Mythology": 20,
            "Art": 25
        }
        return categories_map.get(category_name, 9)

if __name__ == "__main__":
    server = QuizServer()
    server.start()