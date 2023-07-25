import requests
import json
import time

endpoint = "https://api.weatherbit.io/v2.0/history/daily"
api_key = "a553395fc0634f4ba487c98916fd42d5"
start_date = "2022-7-8"
end_date = "2023-7-8"
print("This application will display the average temperature in an inputted zip code over the past seven (7) days") 
postal_code = input("Enter your zip code here: ")
num_days = 7

url = f"{endpoint}?key={api_key}&country=US&postal_code={postal_code}&start_date={start_date}&end_date={end_date}&units=M"
response = requests.get(url)

if response.status_code == 429:
    retry_after = int(response.headers.get('Retry-After', 1))
    print(f"Rate limit exceeded. Retrying after {retry_after} seconds.")
    time.sleep(retry_after)
    response = requests.get(url)
else:
    if response.status_code == 200:
        data = json.loads(response.text)
        state_code = data["state_code"]
        temperatures = [day["temp"] for day in data["data"]]
        average_temperature = sum(temperatures) / len(temperatures)
        average_fahrenheit = (average_temperature * 1.8) + 32
        average_fahrenheit = round(average_fahrenheit, 2)
        print(f"The average temperature for the {state_code} zip code {postal_code} for the last {num_days} days is {average_fahrenheit}°F.")
    else:
        print(f"Error occurred while fetching data. Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")
