import requests
from tqdm import tqdm
from multiprocessing import Pool
import time
import argparse

url = "https://www.guessthepin.com/prg.php"


def guess(num):
    try:
        r = requests.post(url, data={"guess": str(num)})
        return num, r.url
    except requests.exceptions.ConnectionError:
        return None, None


def format_time(seconds):
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    time_string = f"{minutes}:{remaining_seconds:02d}"
    return time_string


def run_script():
    start_time = time.time()
    last_tried_pin = None

    with Pool(60) as pool:
        for num, url in pool.imap_unordered(guess, tqdm(range(0, 9999), bar_format='|{bar:50}| {n_fmt}/{total_fmt} ({percentage:.0f}%) [ETA: {remaining}, {rate_fmt}]')):
            if num is None:
                continue
            last_tried_pin = num
            if url != "https://www.guessthepin.com/":
                break

    end_time = time.time()
    amount_of_time = int(end_time - start_time)
    time_string = format_time(amount_of_time)

    print(f"PIN Solved in {time_string}!")
    print(f"The Correct PIN is: {last_tried_pin}!")

    return last_tried_pin


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--infinite", action="store_true", help="Run the script again after finding the PIN")
    args = parser.parse_args()

    found_pin = run_script()

    if args.infinite:
        print("Re-running script!")
        while True:
            found_pin = run_script()
            print("Re-running script!")
