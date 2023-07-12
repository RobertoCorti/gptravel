import json
from inspect import cleandoc

from gptravel.core.utils.regex_tool import JsonExtractor


class TestJsonExtractor:
    def test_simple_json(self, extractor: JsonExtractor):
        text = '{"name": "John", "age": 30}'
        expected_output = [text]
        assert json.loads(extractor(text)[0]) == json.loads(expected_output[0])

    def test_nested_json(self, extractor):
        text = '{"name": "John", "age": 30, "address": {"street": "123 Main St", "city": "Anytown USA"}}'
        expected_output = [text, '{"street": "123 Main St", "city": "Anytown USA"}']
        assert json.loads(extractor(text)[0]) == json.loads(expected_output[0])

    def test_no_json(self, extractor):
        text = "This is not a JSON string"
        expected_output = []
        assert extractor(text) == expected_output

    def test_output_gpt(self, extractor):
        text_gpt = cleandoc(
            """Sure! Here a json
                      {
                        "Day 1": {
                            "Bangkok": [
                            "Visit Grand Palace",
                            "Take a boat trip along the Chao Phraya River",
                            "Shop at Chatuchak Weekend Market"
                            ]
                        },
                        "Day 2": {
                            "Chiang Mai": [
                            "Explore Doi Suthep temple",
                            "Experience the traditional Thai massage",
                            "Visit Elephant Nature Park"
                            ]
                        },
                        "Day 3": {
                            "Phuket": [
                            "Relax on the beautiful beaches of Phuket",
                            "Take a speedboat cruise to visit Koh Phi Phi",
                            "Watch the sunset at Promthep Cape"
                            ]
                        }
                        }

                        Note: Keep in mind that this is just a sample travel plan and activities can be customized according to individual preferences."""
        )
        expected_output = '{\n"Day 1": {\n    "Bangkok": [\n    "Visit Grand Palace",\n    "Take a boat trip along the Chao Phraya River",\n    "Shop at Chatuchak Weekend Market"\n    ]\n},\n"Day 2": {\n    "Chiang Mai": [\n    "Explore Doi Suthep temple",\n    "Experience the traditional Thai massage",\n    "Visit Elephant Nature Park"\n    ]\n},\n"Day 3": {\n    "Phuket": [\n    "Relax on the beautiful beaches of Phuket",\n    "Take a speedboat cruise to visit Koh Phi Phi",\n    "Watch the sunset at Promthep Cape"\n    ]\n}\n}'
        assert json.loads(extractor(text_gpt)[0]) == json.loads(expected_output)
