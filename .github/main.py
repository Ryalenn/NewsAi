import subprocess
import time

def run_script(script_name):
    try:
        result = subprocess.run(['python', script_name], check=True, capture_output=True, text=True)
        print(f"Output of {script_name}:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running {script_name}:\n{e.stderr}")
        
        
        
def run_sum_script():
    try:
        result = subprocess.run(['python', 'sum.py'], check=True, capture_output=True, text=True)
        print(f"Output of sum.py:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running sum.py:\n{e.stderr}")        
        
def main():
    scripts = ['frandroid.py', 'techcrunch.py', 'verge.py']

    for script in scripts:
        print(f"Running {script}...")
        run_script(script)
        
    import json
    with open('articles_after_date.json', 'r') as infile:
        articles = json.load(infile)

    num_links = len(articles)
    print(f"Total number of articles: {num_links}")

    # Call sum.py every 8 seconds, limited to 10 calls per minute
    for i in range(num_links):
        run_sum_script()
        if (i + 1) % 10 == 0:
            print("Sleeping for 60 seconds to avoid exceeding API rate limit...")
            time.sleep(60)
        else:
            time.sleep(30)

if __name__ == "__main__":
    main()
