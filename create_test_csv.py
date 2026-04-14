import pandas as pd

# 1. Load your existing dataset
# We use the one you already created with the correct headers
df = pd.read_csv("data/dataset.csv")

# 2. Define the 10 specific columns the API is looking for
target_columns = [
    "duration", "protocol_type", "service", "src_bytes", "dst_bytes", 
    "count", "srv_count", "serror_rate", "srv_serror_rate", "same_srv_rate"
]

# 3. Take the first 20 rows and only the columns we need
test_batch = df[target_columns].head(20)

# 4. Save it as a new CSV
test_batch.to_csv("data/test_batch.csv", index=False)

print("✅ test_batch.csv created successfully in the data folder!")
print("It contains 20 rows of real network traffic.")