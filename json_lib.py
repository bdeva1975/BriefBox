import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI API client
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

def get_tools():
    tools = [
        {
            "toolSpec": {
                "name": "summarize_email",
                "description": "Summarize email content.",
                "inputSchema": {
                    "json": {
                        "type": "object",
                        "properties": {
                            "summary": {
                                "type": "string",
                                "description": "A brief one-line or two-line summary of the email."
                            },
                            "escalate_complaint": {
                                "type": "boolean",
                                "description": "Indicates if this email is serious enough to be immediately escalated for further review."
                            },
                            "level_of_concern": {
                                "type": "integer",
                                "description": "Rate the level of concern for the above content on a scale from 1-10",
                                "minimum": 1,
                                "maximum": 10
                            },
                            "overall_sentiment": {
                                "type": "string",
                                "description": "The sender's overall sentiment.",
                                "enum": ["Positive", "Neutral", "Negative"]
                            },
                            "supporting_business_unit": {
                                "type": "string",
                                "description": "The internal business unit that this email should be routed to.",
                                "enum": ["Sales", "Operations", "Customer Service", "Fund Management"]
                            },
                            "customer_names": {
                                "type": "array",
                                "description": "An array of customer names mentioned in the email.",
                                "items": { "type": "string" }
                            },
                            "sentiment_towards_employees": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "employee_name": {
                                            "type": "string",
                                            "description": "The employee's name."
                                        },
                                        "sentiment": {
                                            "type": "string",
                                            "description": "The sender's sentiment towards the employee.",
                                            "enum": ["Positive", "Neutral", "Negative"]
                                        }
                                    }
                                }
                            }
                        },
                        "required": [
                            "summary",
                            "escalate_complaint",
                            "overall_sentiment",
                            "supporting_business_unit",
                            "level_of_concern",
                            "customer_names",
                            "sentiment_towards_employees"
                        ]
                    }
                }
            }
        }
    ]

    return tools

def get_json_response(input_content):
    try:
        # OpenAI API call with a specific request
        tools_list = get_tools()

        # Craft the message
        messages = [
            {
                "role": "user",
                "content": f"<content>{input_content}</content>"
            },
            {
                "role": "system",
                "content": "Please use the summarize_email tool to generate the email summary JSON based on the content within the <content> tags."
            }
        ]
        
        # Send a chat completion request
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=2000,
            temperature=0,
            functions=[{
                "name": "summarize_email",
                "description": "Summarize email content",
                "parameters": tools_list[0]['toolSpec']['inputSchema']['json']
            }],
            function_call={"name": "summarize_email"}  # explicitly requesting the function call
        )

        # Extracting the function's response
        function_call = response.choices[0].message.function_call
        if function_call and function_call.name == "summarize_email":
            function_response = function_call.arguments
        else:
            raise ValueError("Expected function call 'summarize_email' not found in the response")

        # Attempt to parse the JSON string
        parsed_response = json.loads(function_response)
        
        print("Raw function response:")
        print(function_response)
        print("\nParsed JSON response:")
        print(json.dumps(parsed_response, indent=2))
        
        return parsed_response

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        print("Raw response causing the error:")
        print(function_response)
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Full response object:")
        print(response)
        return None

# Example usage
if __name__ == "__main__":
    sample_email = """
    Dear Support Team,

    I am writing to express my disappointment with the recent changes to your investment platform. 
    The new interface is confusing and has made it difficult for me to manage my portfolio effectively. 
    Additionally, I've noticed some discrepancies in my account balance that I'd like to discuss.

    I've been a loyal customer for over five years, and I've always appreciated the excellent service 
    provided by your team, especially Sarah from customer support who has been incredibly helpful in the past.

    However, if these issues are not resolved soon, I may need to consider moving my investments elsewhere. 
    I hope we can find a solution quickly.

    Best regards,
    John Smith
    """
    
    result = get_json_response(sample_email)
    if result:
        print("\nSuccessfully processed the email.")
    else:
        print("\nFailed to process the email.")