import json
import os

import openai
from dotenv import load_dotenv

from gptravel.core.travel_planner.openai_engine import ChatGPTravelEngine
from gptravel.core.travel_planner.prompt import PlainTravelPrompt

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def main(destination_place: str, start_travel_place: str, n_days: str):
    prompt = PlainTravelPrompt(
        starting_travel_place=start_travel_place,
        travel_destination=destination_place,
        n_travel_days=n_days,
    )

    engine = ChatGPTravelEngine()

    travel_plan_in_json_format = engine.get_travel_plan_json(prompt)

    print(travel_plan_in_json_format)
    with open("travel_plan_{}_{}.json".format(destination_place, n_days), "w") as jfile:
        json.dump(travel_plan_in_json_format, jfile)


if __name__ == "__main__":
    main(destination_place="Thailand", start_travel_place="Milan", n_days="3")
