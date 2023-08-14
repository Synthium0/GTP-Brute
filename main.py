import requests
from tqdm import tqdm
from multiprocessing import Pool
import time

url = "https://www.guessthepin.com/prg.php"


def guess(num):
    r = requests.post(url, data={"guess": str(num)})
    return num, r.url


def format_time(seconds):
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    time_string = f"{minutes}:{remaining_seconds:02d}"
    return time_string


if __name__ == "__main__":
    start_time = time.time()

    with Pool(60) as pool:
        for num, url in pool.imap_unordered(guess, tqdm(range(0, 9999), bar_format='|{bar:50}| {n_fmt}/{total_fmt} ({percentage:.0f}%) [ETA: {remaining}, {rate_fmt}]')):
            if url != "https://www.guessthepin.com/":
                break

    end_time = time.time()
    amount_of_time = int(end_time - start_time)
    time_string = format_time(amount_of_time)

    print(f"PIN Solved in {time_string}!")
    print(f"The Correct PIN is: {num}!")
