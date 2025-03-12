import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

file_path = "/Users/aayushkumbhare/Desktop/SSMSOC/new_df.csv"
df = pd.read_csv(file_path)
df["ts"] = pd.to_datetime(df["ts"])

df["delta_v"] = df["v"].diff().fillna(0)  # Change in speed
df["delta_a"] = df["a"].diff().fillna(0)  # Change in acceleration
df["delta_pl"] = df["pl"].diff().fillna(0)  # Change in player load
df.ffill(inplace=True)  # Forward fill

features = ["v", "a", "delta_v", "delta_a", "mp", "delta_pl", "sl", "pl"]

# Scale numerical features
scaler = StandardScaler()
df[features] = scaler.fit_transform(df[features])


#Change to add delta_v and delta_a
df["risk_score"] = (
    (0.3 * abs(df["a"])) +   # Acceleration
    (0.2 * df["v"]) +        # Speed
    (0.2 * df["mp"]) +       # Metabolic Power
    (0.15 * df["pl"]) +      # Player Load
    (0.1 * df["sl"]) +       # Smooth Load
    (0.05 * df["delta_pl"])  # Change in Player Load
)

df["risk_score"] = (df["risk_score"] - df["risk_score"].min()) / (df["risk_score"].max() - df["risk_score"].min())

# Define input (X) and target (y)
X = df[features]
y = df["risk_score"]

# Train-test split (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=True, random_state=42)

# Train Linear Regression
lr_model = LinearRegression()
lr_model.fit(X_train, y_train)
lr_pred = lr_model.predict(X_test)

# Train Random Forest
rf_model = RandomForestRegressor(n_estimators=100, max_depth=6, random_state=42)
rf_model.fit(X_train, y_train)
rf_pred = rf_model.predict(X_test)

lr_mae = mean_absolute_error(y_test, lr_pred)
rf_mae = mean_absolute_error(y_test, rf_pred)
lr_r2 = r2_score(y_test, lr_pred)
rf_r2 = r2_score(y_test, rf_pred)

print(f"Linear Regression - MAE: {lr_mae:.4f}, R²: {lr_r2:.4f}")
print(f"Random Forest - MAE: {rf_mae:.4f}, R²: {rf_r2:.4f}")

# Predict risk scores using the best model (Random Forest)
df["predicted_risk"] = rf_model.predict(X)

# Define high-risk moments (risk score > 0.7)
df["high_risk_flag"] = (df["predicted_risk"] > 0.7).astype(int)

# Show high-risk timestamps
high_risk_moments = df[df["high_risk_flag"] == 1][["ts", "predicted_risk", "v", "a", "mp", "sl", "pl"]]
print(high_risk_moments.head())

high_risk_moments.to_csv("high_risk_predictions.csv", index=False)