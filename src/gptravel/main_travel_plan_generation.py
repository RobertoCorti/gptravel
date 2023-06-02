import json
import os
from typing import Optional

import openai
from dotenv import load_dotenv

from gptravel.core.travel_planner.openai_engine import ChatGPTravelEngine
from gptravel.core.travel_planner.prompt import PromptFactory

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def main(
    destination_place: str,
    start_travel_place: str,
    n_days: str,
    travel_theme: Optional[str] = None,
):
    travel_parameters = {
        "travel_departure": start_travel_place,
        "travel_destination": destination_place,
        "n_travel_days": n_days,
        "travel_theme": travel_theme,
    }

    prompt_factory = PromptFactory()

    prompt = prompt_factory.build_prompt(**travel_parameters)

    engine = ChatGPTravelEngine()

    travel_plan_in_json_format = engine.get_travel_plan_json(prompt)

    print(travel_plan_in_json_format.travel_plan)
    with open(
        "trave-l_plan_{}_{}.json".format(destination_place, n_days), "w"
    ) as jfile:
        json.dump(travel_plan_in_json_format.travel_plan, jfile)


if __name__ == "__main__":
    main(
        destination_place="Milan",
        start_travel_place="Rome",
        n_days="3",
        travel_theme="romantic",
    )
