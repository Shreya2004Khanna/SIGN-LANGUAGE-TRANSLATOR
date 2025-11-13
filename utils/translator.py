def grammar_fix(sentence):
    words = sentence.lower().split()

    # Join to compare phrases directly
    joined = " ".join(words)

    correction_map = {
        "i engineer": "I am an engineer",
        "i am engineer": "I am an engineer",
        "i student": "I am a student",
        "i am student": "I am a student",
        "i teacher": "I am a teacher",
        "i developer": "I am a developer",
        "i good": "I am good",

        "thank you": "Thank you",
        "you good": "You are good",
        "hello": "Hello!",
        "yes": "Yes",
        "no": "No",
        "stop": "Stop",

        # Eating patterns
        "i want eat": "I want to eat",
        "i want to eat": "I want to eat",

        # Name / introduction
        "what your name": "What is your name?",
        "my name is": "My name is",
        "i love you": "I love you",
        "how are you": "How are you?",

        # Greetings
        "good morning": "Good morning",
        "good afternoon": "Good afternoon",
        "good evening": "Good evening",
        "good night": "Good night",

        "please": "Please",
        "sorry": "Sorry",
        "excuse me": "Excuse me",
    }

    # Apply corrections if match found
    if joined in correction_map:
        return correction_map[joined]

    # Medium fallback: if user says "i want + word"
    if words[:2] == ["i", "want"] and len(words) >= 3:
        return "I want to " + " ".join(words[2:])

    # Final fallback: Capitalize
    return sentence.capitalize()
