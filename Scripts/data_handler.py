import pandas as pd

class DataHandler:
    def save_to_csv(self, data, filename="facebook_data.csv"):
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")
