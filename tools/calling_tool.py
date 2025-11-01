import os

from agno.tools import Toolkit
from vapi import Vapi
# Debug: Print all environment variables that start with TWILIO
print("🔍 Debugging Twilio environment variables:")
for key, value in os.environ.items():
    if key.startswith("TWILIO"):
        print(f"  {key} = {'***' if 'TOKEN' in key else value}")

vapi = Vapi(token=os.getenv("VAPI_API_KEY"))
phone_number_id = os.getenv("VAPI_PHONE_NUMBER_ID")
print(phone_number_id)
class CallingTool(Toolkit):
    def __init__(self, **kwargs):
        super().__init__(name="CallingTool", tools=[self.call_phone_number], **kwargs)

    def call_phone_number(self, phone_number: str,user_id: str) -> str:
        """
        Use this Function to call a phone number.If phoneNumber has no +91 in the start it will add it automatically

        Args:
            phone_number (str): The phone number to call (with +91 prefix if not present)
            user_id (str): The user id of the user Whose phone number is being called
        Returns:
            str: The call SID or error message
        """

        # Query users_profile table to get the actual user_id using phone number
        call = vapi.calls.create(
            phone_number_id=os.getenv("VAPI_PHONE_NUMBER_ID"),
            customer={"number": phone_number},
            assistant_id=os.getenv("VAPI_ASSISTANT_ID")
        )
        
        print("Call object details !:", call)
        # Save the call id to a text file in the same directory
        try:
            call_id = getattr(call, "id", None)
            if call_id:
                file_path = os.path.join(os.path.dirname(__file__), "last_call_id.txt")
                with open(file_path, "w") as f:
                    f.write(str(call_id))
                print(f"Call ID {call_id} saved to {file_path}")
            else:
                print("Warning: Call object does not have an 'id' attribute.")
        except Exception as e:
            print(f"Error saving call id to file: {e}")
        return f"Call created: {call.id}"