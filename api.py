import pandas as pd
import json

df = pd.read_csv("normal.csv")
pid = 4021469
results = df.loc[df["pid"] == pid]

json_data = df.to_json(orient='records')
json.dump(json_data, "file.json", indent=4)
# Print or save JSON data
print(json_data)