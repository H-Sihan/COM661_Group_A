import random
import json

def generate_data():
    
    towns = ['London','Liverpool', 'Camden', 'Ilford',
             'Manchester','Richmond','Portsmouth', 'Worthing',
             'Belfast','Tower Hill']
    
    business_list = []
    
    for i in range(100):
        name = "Biz " + str(i)
        town = random.choice(towns)
        rating = random.randint(1,5)
        business_list.append({
            "name":name,
            "town":town,
            "rating":rating,
            "reviews":[]
        })
    return business_list

businesses = generate_data()

with open("data.json", "w") as fout:
    json.dump(businesses, fout, indent=4)