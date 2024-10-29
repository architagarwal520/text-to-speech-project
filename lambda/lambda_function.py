import json
import boto3
import uuid

s3 = boto3.client('s3')
polly = boto3.client('polly')

BUCKET_NAME = 'YOUR_BUCKET_NAME' 

def lambda_handler(event,context):
    body = json.loads(event['body'])
    text = body.get("text",'Hello, This is default text as no text was provided')
    voice_id = body.get("voiceId",'Joanna')

    response = polly.synthesize_speech(
        Text = text,
        VoiceId = voice_id,
        OutputFormat = 'mp3'
    )

    audio_stream = response.get('AudioStream')

    if audio_stream:
        file_name = f"{uuid.uuid4()}.mp3"
        s3.put_object(
            Bucket = BUCKET_NAME,
            Key = file_name,
            Body = audio_stream.read(),
            ContentType = 'audio/mpeg'
        )

        # Generate a pre-signed URL valid for a limited time (e.g., 1 hour)
        try:
            presigned_url = s3.generate_presigned_url(
                'get_object',
                Params={'Bucket': BUCKET_NAME, 'Key': file_name},
                ExpiresIn=3600  # URL expires in 1 hour
            )
            return {
                'statusCode': 200,
                'headers': {
                'Access-Control-Allow-Origin': '*',  # or your specific domain
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
                },
                'body': json.dumps({'audioUrl': presigned_url})
            }
        except ClientError as e:
            # Error generating pre-signed URL
            return {
                'statusCode': 500,
                'body': json.dumps({'error': str(e)})
            }

    else:
        return {
            'statusCode':500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body':json.dumps({'error':"Could not synthesize speech"})
        }
    

        