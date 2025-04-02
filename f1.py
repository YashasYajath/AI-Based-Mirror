import cv2
import openai
import base64

# ✅ Function to capture an image from the webcam
def capture_image():
    print("Starting webcam... Press 'c' to capture, 'q' to quit.")

    cap = cv2.VideoCapture(1)  # Open webcam
    if not cap.isOpened():
        print("ERROR: Could not open webcam.")
        return None

    while True:
        ret, frame = cap.read()
        if not ret:
            print("ERROR: Could not read frame.")
            break

        cv2.imshow("Webcam Feed", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('c'):
            print("Capturing image...")
            image_path = "captured_image.jpg"
            cv2.imwrite(image_path, frame)
            print(f"Image saved as '{image_path}'")
            cap.release()
            cv2.destroyAllWindows()
            return image_path  # Return the image path
        elif key == ord('q'):
            print(" Quitting without capturing.")
            break

    cap.release()
    cv2.destroyAllWindows()
    return None

# ✅ Function to encode the image in Base64
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# ✅ Function to send image to GPT-4-Vision
def send_image_to_ai(image_path):
    API_KEY = "Api_Key"

    encoded_image = encode_image(image_path)

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",  # ✅ Ensure you're using GPT-4-Vision
        messages=[
            {"role": "system", "content": "You are an AI fashion assistant."},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Rate this outfit and provide recommendations."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}}
                ]
            }
        ],
        api_key=API_KEY  # Pass API Key
    )

    return response

# ✅ Main function
def main():
    # Step 1: Capture an image from the webcam
    image_path = capture_image()

    if image_path:
        # Step 2: Send the image to AI for outfit rating
        ai_response = send_image_to_ai(image_path)

        if ai_response:
            # Step 3: Display the results
            print("\n AI Response:")
            print("Outfit Rating:", ai_response["choices"][0]["message"]["content"])
        else:
            print("Failed to get a response from the AI.")
    else:
        print(" No image captured.")

if __name__ == "__main__":
    main()

