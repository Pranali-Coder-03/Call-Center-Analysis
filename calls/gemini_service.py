import os
import json

from google import genai
from google.genai import types


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def analyze_audio(file_path):

    uploaded_file = client.files.upload(
        file=file_path
    )

    prompt = """
You are an AI quality analyst for a professional call center.

Analyze the uploaded customer service call.

Return the result ONLY as valid JSON.

Use exactly this structure:

{
    "summary": "",
    "customer_issue": "",
    "resolution": "",
    "sentiment": "",
    "agent_performance": "",
    "key_topics": [],
    "action_items": []
}

Instructions:

1. summary:
Give a concise but useful summary of the entire conversation.

2. customer_issue:
Explain why the customer contacted the company.

3. resolution:
Explain how the issue was resolved.
If it was not resolved, clearly say so.

4. sentiment:
Identify the customer's overall sentiment.
Examples:
Positive
Neutral
Negative
Frustrated
Satisfied
Angry

5. agent_performance:
Evaluate the agent's communication, professionalism,
clarity, empathy and effectiveness.

6. key_topics:
Return important topics discussed in the call.

7. action_items:
Return actions that should be taken after the call.

Do not invent information that is not present in the recording.
"""


    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            types.Part.from_uri(
                file_uri=uploaded_file.uri,
                mime_type=uploaded_file.mime_type,
            ),
            prompt,
        ],
        config=types.GenerateContentConfig(
            response_mime_type="application/json"
        ),
    )

    result = json.loads(response.text)

    return result