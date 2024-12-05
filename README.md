# GPTravel ✈️
[![python](https://img.shields.io/badge/python-3.9_%7C_3.10_%7C_3.11-blue?link=https%3A%2F%2Fwww.python.org%2F)](https://www.python.org)
![Tests](https://github.com/RobertoCorti/gptravel/actions/workflows/python-tests.yml/badge.svg)
![GitHub Tags](https://img.shields.io/github/tag/RobertoCorti/gptravel.svg)
[![Streamlit](https://img.shields.io/pypi/v/streamlit?logo=streamlit&logoColor=white&label=Streamlit&color=magenta)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

GPTravel is a Web App that generates a travel plan based on Large-Language Models (LLMs). It helps users create personalized itineraries giving the best destinations, activities, and routes.

## Idea 💡
Our goal is to build an AI-powered travel assistant that could help people on planning their trips. We understand that planning a trip can be overwhelming, with countless options for destinations, activities, and prices. GPTravel aims to simplify this process by providing users with personalized recommendations and insights.

By leveraging GPT models, GPTravel generates customized itineraries tailored to each user's specific travel needs and preferences. Whether it's a weekend getaway or a month-long adventure, GPTravel aims to assist users at every step of their travel planning journey.

The AI travel assistant that we aim to build would provide recommendations for destinations, attractions, accommodations, transportation options, and even estimated budgets. It takes into account factors such as travel duration, budget constraints, travel interests, and any specific preferences or requirements provided by the user. GPTravel aims to make trip planning more efficient, enjoyable, and stress-free by offering intelligent suggestions and insights.

At this moment we prepared a prototype on a Streamlit app with few of these functionalities. The future work will be focused on adding to the app a more strong and reliable travel assistant.

## Installation ⚙️

This project uses the package manager poetry. To install poetry then run
```
pip install poetry
```
After installing poetry then you must config the following flag
```
poetry config virtualenvs.in-project true
```
To install the dependendencies then run the command
```
poetry install
```
To activate the virtual environment then run
```
poetry shell
```

## Usage 🚀
Our prototype application is available on [Streamlit Cloud](https://gptravel-prototype.streamlit.app/); you will only need an OpenAI API key and a willingness to travel.

To run the GPTravel web app on your local machine, use the following command:
```
streamlit run Home.py
```
This will start the GPTravel app using Streamlit. You can then access the web app through your browser.

## Next Steps 🌟
Here are some suggested next steps to enhance GPTravel:

* Implement a user interface (different from Streamlit) for the web app to provide a seamless experience for users when generating travel plans.
* Enhance the recommendation algorithm to consider user preferences, such as budget constraints, travel interests, and accommodation preferences.
* Integrate with external APIs to fetch real-time data on flights options, weather conditions and tourist attractions tickets.
* Implement user authentication and user profile management to allow users to save and revisit their travel plans.
* Enable social sharing features to allow users to share their travel plans with friends and family.

Contributions are welcome! Feel free to explore the GitHub repository and submit pull requests or open issues to contribute to the development of GPTravel.

## License 📄
This project is licensed under the MIT License.

## Authors ✍️
GPTravel is developed and maintained by:
- [Roberto Corti](https://github.com/RobertoCorti)
- [Stefano Polo](https://github.com/stefano-polo)
