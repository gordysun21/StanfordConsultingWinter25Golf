
import pandas as pd
import ace_tools as tools
services = {
    "Body Care": [160, 170, 165, 175, 165, 175, 165, 175],
    "Just for Men": [190, 200, 55, 65, 75, 85],
    "Nail Services": [60, 70, 85, 95, 75, 85, 70, 90, 35, 45, 30, 10],
    "Facials": [160, 170, 250, 260, 250, 260, 300, 320, 170, 180, 170, 180, 170, 180, 180, 190, 150, 160, 25],
    "Massages": [160, 170, 330, 340, 160, 170, 320, 330, 190, 200, 190, 200, 320, 330, 165, 175, 330, 340, 160, 170, 
                 165, 175, 150, 160, 320, 340, 25]
}

# Calculate the average price for each category
average_prices = {category: sum(prices) / len(prices) for category, prices in services.items()}




df = pd.DataFrame(average_prices.items(), columns=["Category", "Average Price"])
tools.display_dataframe_to_user(name="Average Service Prices", dataframe=df)