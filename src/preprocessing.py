import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler

def load_data(path):
    return pd.read_csv(path)

def preprocess_data(df):
    print("--- Starting Preprocessing ---")
    df = df.dropna().copy()

    # 1. Map label to binary (0 for normal, 1 for attack)
    # This creates the 'y' variable
    if 'label' in df.columns:
        df['label'] = df['label'].apply(lambda x: 0 if 'normal' in str(x).lower() else 1)
    else:
        # Fallback if label isn't named correctly
        df['label'] = 0 

    # 2. Force encode categorical columns
    le = LabelEncoder()
    categorical_cols = ["protocol_type", "service", "flag"]
    for col in categorical_cols:
        if col in df.columns:
            df[col] = le.fit_transform(df[col].astype(str))

    # 3. Select the 10 specific features for the API
    features = ["duration", "protocol_type", "service", "src_bytes", "dst_bytes", 
                "count", "srv_count", "serror_rate", "srv_serror_rate", "same_srv_rate"]
    
    # Create X and y
    X = df[features].copy()
    X = X.apply(pd.to_numeric, errors='coerce').fillna(0)
    y = df['label'] # Defining y here clearly

    # 4. Create and fit the scaler
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    print("--- Preprocessing Complete! ---")
    
    # Return all three items
    return X_scaled, y, scaler