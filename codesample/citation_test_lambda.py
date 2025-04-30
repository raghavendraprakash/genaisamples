import boto3
import uuid
import json

def lambda_handler(event, context):
    # Create a boto3 client for the Bedrock Runtime service
    client = boto3.client(
        "bedrock-agent-runtime",
        region_name='us-east-1'  # Ensure this matches your agent's region
    )

    try:
        session_id = uuid.uuid4().hex

        # Extract input text from the Lambda event
        input_text = "What is Lex?"

        # Call the InvokeAgent operation
        response = client.invoke_agent(
            agentId='6QLSBFG3QE',           # Replace with your Agent ID
            agentAliasId='IVZILLNO3G', # Replace with your Agent Alias ID
            enableTrace=False,
            inputText=input_text,
            sessionId=session_id
        )

        full_response = ""
        sources = set()

        for event in response.get("completion", []):
            chunk = event["chunk"]
            text_output = chunk["bytes"].decode()
            full_response += text_output
            print(chunk)
            if "attribution" in chunk and "citations" in chunk["attribution"]:
                for c in chunk["attribution"]["citations"]:
                    for r in c["retrievedReferences"]:
                        if "kendraDocumentLocation" in r["location"]:
                            sources.add(r["location"]["kendraDocumentLocation"]["uri"])
            print(sources)
        return {
            'statusCode': 200,
            'body': json.dumps({
                'response': full_response,
                'sources': list(sources)
            })
        }

    except Exception as e:
        print(f"Error invoking agent: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }
