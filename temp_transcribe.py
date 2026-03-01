import whisper

model = whisper.load_model('turbo')
result = model.transcribe(r'C:\Users\USER\.openclaw\media\inbound\file_2---9057454b-a828-4e6a-9196-63e087e7eb25.ogg', language='zh')
print(result['text'])