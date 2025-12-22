from tensorflow.keras.models import load_model

# Load your old .h5 model
model = load_model("signbridge_robust_model.h5", compile=False)

# Save as SavedModel format (folder)
model.save("signbridge_robust_savedmodel")
print("Model converted to SavedModel format successfully!")
