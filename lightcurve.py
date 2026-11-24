import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
# Module 5 - AI/ML Validation

# Sample training data
X_train = [
    [1.00, 0.001],
    [0.99, 0.002],
    [0.98, 0.003],
    [1.00, 0.002],
    [0.97, 0.004],
    [0.995, 0.001]
]

# 0 = Normal signal, 1 = Transit-like signal
y_train = [0, 0, 1, 0, 1, 0]
# Create the ML model
model = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the model
model.fit(X_train, y_train)

print("AI/ML Model Training Completed!")
# Predict signal type
test_signal = [[0.98, 0.003]]

prediction = model.predict(test_signal)

if prediction[0] == 1:
    print("AI Result: Possible Transit Signal")
else:
    print("AI Result: Normal Signal")
# Module 6 - Candidate Ranking

if prediction[0] == 1:
    candidate_score = 85
else:
    candidate_score = 40

print("\n===== ASTRA-SIGNAL RESULTS =====")
print("AI Prediction:", prediction[0])
print("Candidate Score:", candidate_score, "%")
print("================================")
# Candidate Status
if candidate_score >= 80:
    print("Candidate Status: High Priority")
else:
    print("Candidate Status: Low Priority")

print("Analysis Status: Completed")
print("System: ASTRA-SIGNAL")
# Create observation time
time = np.linspace(0, 10, 100)

# Create normal star brightness
brightness = np.ones(100)

# Simulate a planet transit
brightness[20:25] = 0.98
brightness[40:45] = 0.98
brightness[60:65] = 0.98
# Add noise to the signal
noise = np.random.normal(0, 0.005, 100)
brightness = brightness + noise

# Smooth the noisy signal
smooth_brightness = pd.Series(brightness).rolling(
    window=5,
    center=True,
    min_periods=1
).mean()
# Transit Detection
threshold = 0.995

transit_points = np.where(smooth_brightness < threshold)[0]

print("Transit Detection Results:")
print("Possible transit points:", transit_points)
# Estimate orbital period
if len(transit_points) > 1:
    orbital_period = np.mean(np.diff(transit_points))

    print("Estimated orbital period:", orbital_period)
# Periodicity Analysis
if len(transit_points) > 0:
    transit_times = time[transit_points]

    print("Transit times:", transit_times)
else:
    print("No transit detected")
    # Estimate transit duration
if len(transit_points) > 0:
    transit_duration = transit_times[-1] - transit_times[0]

    print("Estimated transit duration:", transit_duration)

# Store the data
data = pd.DataFrame({
    "Time": time,
    "Brightness": brightness
})

print(data)
# Plot the light curve
# Plot the light curve
plt.figure(figsize=(12, 6))

# Original noisy signal in orange
plt.scatter(
    time,
    brightness,
    color="orange",
    label="Noisy Signal",
    s=25
)

# Smoothed signal in blue
plt.plot(
    time,
    smooth_brightness,
    color="blue",
    label="Smoothed Signal",
    linewidth=2
)

# Graph labels
plt.xlabel("Time")
plt.ylabel("Star Brightness")

plt.title("ASTRA-SIGNAL - Noisy and Smoothed Light Curve")

plt.legend()
print("Maximum difference:", np.max(np.abs(brightness - smooth_brightness)))
print("Maximum difference:", np.max(np.abs(brightness - smooth_brightness)))
# Highlight detected transit points
plt.scatter(
    time[transit_points],
    brightness[transit_points],
    color="red",
    label="Detected Transit",
    s=45
)
plt.grid(True)
plt.tight_layout()

plt.show()
# Transit Detection
threshold = np.mean(smooth_brightness) - 0.005

transit_points = smooth_brightness < threshold

print("Transit detected:", np.any(transit_points))
print("Number of transit points:", np.sum(transit_points))

