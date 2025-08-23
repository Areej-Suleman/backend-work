def generate_response(text: str) -> str:
    text = text.lower().strip()

    if "hello" in text or "hi" in text:
        return "Hey there! How can I help you with your skincare today?"

    elif "recommend" in text or "suggest" in text:
        return "Sure! Can you tell me your skin type and what you're looking for?"

    elif "dry skin" in text:
        return "For dry skin, I recommend using a hydrating cleanser and a moisturizer with hyaluronic acid."

    elif "oily skin" in text:
        return "For oily skin, try a gentle foaming cleanser and a lightweight, oil-free moisturizer."

    elif "thank you" in text or "thanks" in text:
        return "You're welcome! Let me know if you need anything else."

    elif "bye" in text or "goodbye" in text:
        return "Take care! Hope your skin glows brighter than ever."

    else:
        return "I'm still learning! Could you rephrase that or tell me more about your skin concerns?"