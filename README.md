# Scorpio Flask Chatbot

A web-based chatbot application built with Flask, providing an interactive conversational interface.

## Features

- Real-time chat interface
- Flask backend server
- WebSocket support for instant messaging
- Responsive web design
- Simple and intuitive user interface

## Prerequisites

- Python 3.7+
- Flask
- Flask-SocketIO
- Python-dotenv

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/scorpio-flask-chatbot.git
cd scorpio-flask-chatbot
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

1. Create a `.env` file in the project root
2. Add your configuration variables:
```
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your_secret_key
```

## Usage

1. Start the Flask server:
```bash
flask run
```

2. Open your browser and navigate to `http://localhost:5000`

## Project Structure

```
scorpio-flask-chatbot/
├── app.py
├── static/
│   ├── css/
│   └── js/
├── templates/
├── requirements.txt
└── README.md
```

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
=======
# Steps to use 
1. Clone this repository 'git clone git-link'.
2. Create a python virtual env (Optional but recommended).
3. install the packages in requirements.txt
   Activate the virutal env then
   ```bash
   pip install -r requirements.txt
4. use 'flask run' command in the root directory to run the flask app.
5. The App will run at given ip link by your wsgi server.