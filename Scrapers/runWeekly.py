import subprocess

if __name__ == "main":
    # Run the Python files
    subprocess.run(["python", "topKWeeklyPostsScraper.py"])
    subprocess.run(["python", "scrapeLinks.py"])
    subprocess.run(["python", "textToSpeech.py"])