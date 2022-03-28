import bs4
import dotenv
from os import getenv
from pathlib import Path
import requests

dotenv.load_dotenv()
root_path = Path().resolve()
COOKIES = {"session": getenv("AOC_SESSION")}


def get_input(year, day):
    cache_path = Path(f"year{year}_day{day}_input.txt").resolve()
    if cache_path.exists():
        return cache_path.read_text()
    else:
        response = requests.get(url=f"https://adventofcode.com/{year}/day/{day}/input", cookies=COOKIES)
        if not response.ok:
            raise ValueError("bad response")
        input_text = response.text.strip()
        cache_path.write_text(input_text)
        return input_text


def submit_answer(year, day, level, answer):
    print(f"Submitting for YEAR {year}, DAY {day}, LEVEL {level}: {answer}... ", end="")
    response = requests.post(url=f"https://adventofcode.com/{year}/day/{day}/answer", cookies=COOKIES,
                         data={"level": level, "answer": answer})
    if not response.ok:
        raise ValueError("bad response")
    message = bs4.BeautifulSoup(response.text, "html.parser").article.text
    if message.startswith("You don't seem"):
        print("You already submitted a correct answer!")
    elif message.startswith("You gave"):
        print(f"YOU ARE ON COOLDOWN!!!! Time remaining: {str(message)[107:114]}")
    elif message.startswith("That's the"):
        print("Correct!")
    elif message.startswith("That's not"):
        if "too low" in message:
            print("WRONG! Too low")
        else:
            print("WRONG! Too high")
    else:
        raise ValueError(f"An unknown error occured. message: {message}")
