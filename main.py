from src.gptravel.app import app
from dotenv import load_dotenv

load_dotenv()

if __name__ == '__main__':
    print('Running Flask App')
    app.debug=True
    app.run(host='127.0.0.1', port=5000)