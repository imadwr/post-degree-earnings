from bs4 import BeautifulSoup
import requests
import csv

URL = "https://www.payscale.com/college-salary-report/majors-that-pay-you-back/bachelors"

response = requests.get(url=URL)
website = response.text

soup = BeautifulSoup(website, "html.parser")

all_degrees = soup.find_all(name="td", class_="csr-col--school-name")
degrees_titles = [degree.getText().split(":")[1] for degree in all_degrees]

salaries_data = soup.find_all(name="td", class_="csr-col--right")
all_salaries = [number.getText() for number in salaries_data]

early_salary = []
mid_salary = []

for item in all_salaries:
    if "Early" in item:
        early_salary.append(float(item.split(":")[1].replace("$", "").replace(",", "")))
    elif "Mid-Career" in item:
        mid_salary.append(float(item.split(":")[1].replace("$", "").replace(",", "")))


print(degrees_titles)
print(early_salary)
print(mid_salary)

csv_rows = []

for item in degrees_titles:
    index = degrees_titles.index(item)
    new_dict = {
        "major": item,
        "early-career-pay": early_salary[index],
        "mid-career-pay": mid_salary[index],
    }
    csv_rows.append(new_dict)

print(csv_rows)

with open("post-degree-earnings.csv", "w", encoding="utf8", newline="") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=csv_rows[0].keys())

    writer.writeheader()
    writer.writerows(csv_rows)





