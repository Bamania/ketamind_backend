import os
import requests

from agno.tools import Toolkit
from agno.utils.log import logger


class GetCallTranscriptTool(Toolkit):
    def __init__(self, **kwargs):
        super().__init__(name="GetCallTranscriptTool", tools=[
            self.get_call_transcript, 
            self.get_call_analysis,
            self.get_last_call_transcript,
            self.get_last_call_analysis
        ], **kwargs)
    
    def _get_vapi_headers(self):
        """Helper method to get VAPI API headers"""
        return {
            'Authorization': f'Bearer {os.getenv("VAPI_API_KEY")}',
        }
    
    def _get_last_call_id(self):
        """Helper method to read the last call ID from file"""
        try:
            file_path = os.path.join(os.path.dirname(__file__), "last_call_id.txt")
            if os.path.exists(file_path):
                with open(file_path, "r") as f:
                    call_id = f.read().strip()
                return call_id
            else:
                return None
        except Exception as e:
            logger.error(f"Error reading last call ID from file: {str(e)}")
            return None

    def get_call_transcript(self,call_id:str) -> str:
        """
        Fetch the transcript of a completed call using the call ID.
        
        Args:
            call_id (str): The call ID to fetch transcript for
            
        Returns:
            str: The call transcript or error message
        """
        try:
       
            headers = self._get_vapi_headers()
            file_path = os.path.join(os.path.dirname(__file__), "last_call_id.txt")
            if os.path.exists(file_path):
                with open(file_path, "r") as f:
                    call_id = f.read().strip()
            response = requests.get(f'https://api.vapi.ai/call/{call_id}', headers=headers)
            
            if response.status_code == 200:
                call_data = response.json()
                print(f'Call details for {call_id}:', call_data)
                
                # Try to get transcript from different possible locations
                transcript = call_data.get('transcript')
                if transcript:
                    return f"Transcript for call {call_id}: {transcript}"
                
                # Try artifact.transcript
                artifact = call_data.get('artifact', {})
                if artifact and artifact.get('transcript'):
                    return f"Transcript for call {call_id}: {artifact['transcript']}"
                
                # Try messages array
                messages = call_data.get('messages', [])
                if messages:
                    conversation = []
                    for msg in messages:
                        role = msg.get('role', 'unknown')
                        content = msg.get('content', 'No content')
                        conversation.append(f"{role}: {content}")
                    return f"Conversation for call {call_id}:\n" + "\n".join(conversation)
                
                # If no transcript found
                status = call_data.get('status', 'unknown')
                return f"Call {call_id} status: {status}. Transcript may not be available yet."
            else:
                print(f'Failed to retrieve call details for {call_id}')
                print(response.text)
                return f"Failed to retrieve call details for {call_id}: {response.text}"
                
        except Exception as e:
            logger.error(f"Error fetching transcript for call {call_id}: {str(e)}")
            return f"Error fetching transcript for call {call_id}: {str(e)}"

    def get_call_analysis(self, call_id: str) -> str:
        """
        Get detailed analysis and summary of a call including transcript if available.
        
        Args:
            call_id (str): The call ID to analyze
            
        Returns:
            str: Detailed call analysis including transcript, duration, status, etc.
        """
        try:
            # Use the working REST API approach
            headers = self._get_vapi_headers()
            response = requests.get(f'https://api.vapi.ai/call/{call_id}', headers=headers)
            
            if response.status_code == 200:
                call_data = response.json()
                print(f'Call details for analysis {call_id}:', call_data)
                
                analysis = []
                analysis.append(f"=== Call Analysis for {call_id} ===")
                
                # Basic call info
                status = call_data.get('status', 'unknown')
                analysis.append(f"Status: {status}")
                
                if 'startedAt' in call_data:
                    analysis.append(f"Started: {call_data['startedAt']}")
                    
                if 'endedAt' in call_data:
                    analysis.append(f"Ended: {call_data['endedAt']}")
                
                if 'cost' in call_data:
                    analysis.append(f"Cost: ${call_data['cost']}")
                
                if 'costBreakdown' in call_data:
                    breakdown = call_data['costBreakdown']
                    analysis.append(f"Cost Breakdown: {breakdown}")
                
                # Try to get transcript from different possible locations
                transcript_found = False
                
                # Method 1: Direct transcript property 
                transcript = call_data.get('transcript')
                if transcript:
                    analysis.append(f"\n=== Transcript ===\n{transcript}")
                    transcript_found = True
                
                # Method 2: Artifact transcript
                artifact = call_data.get('artifact', {})
                if not transcript_found and artifact and artifact.get('transcript'):
                    analysis.append(f"\n=== Transcript ===\n{artifact['transcript']}")
                    transcript_found = True
                
                # Method 3: Messages array
                messages = call_data.get('messages', [])
                if messages:
                    analysis.append("\n=== Conversation Messages ===")
                    for i, message in enumerate(messages):
                        role = message.get('role', 'unknown')
                        content = message.get('content', 'No content')
                        timestamp = message.get('time', message.get('timestamp', 'No timestamp'))
                        analysis.append(f"{i+1}. [{timestamp}] {role}: {content}")
                    transcript_found = True
                
                if not transcript_found:
                    analysis.append("\n⚠️  No transcript available yet. This may be because:")
                    analysis.append("- The call is still in progress")
                    analysis.append("- The call just ended and transcript is being processed")
                    analysis.append("- Transcription was disabled for this call")
                
                return "\n".join(analysis)
            else:
                print(f'Failed to retrieve call analysis for {call_id}')
                print(response.text)
                return f"Failed to retrieve call analysis for {call_id}: {response.text}"
                
        except Exception as e:
            logger.error(f"Error getting call analysis for {call_id}: {str(e)}")
            return f"Error getting call analysis for {call_id}: {str(e)}"

    def get_last_call_transcript(self) -> str:
        """
        Fetch the transcript of the last call made (reads call ID from last_call_id.txt).
        
        Returns:
            str: The call transcript or error message
        """
        call_id = self._get_last_call_id()
        if not call_id:
            return "No last call ID found. Make sure you've made a call first using the calling tool."
        
        print(f"Fetching transcript for last call ID: {call_id}")
        return self.get_call_transcript(call_id)

    def get_last_call_analysis(self) -> str:
        """
        Get detailed analysis of the last call made (reads call ID from last_call_id.txt).
        
        Returns:
            str: Detailed call analysis including transcript, duration, status, etc.
        """
        call_id = self._get_last_call_id()
        if not call_id:
            return "No last call ID found. Make sure you've made a call first using the calling tool."
        
        print(f"Fetching analysis for last call ID: {call_id}")
        return self.get_call_analysis(call_id)
