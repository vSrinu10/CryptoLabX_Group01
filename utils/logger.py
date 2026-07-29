from datetime import datetime

def write_log(option):
    with open("outputs/cryptolab.log", "a") as file:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"{now} - {option}\n")
