# DocToSpeech
A Python script for making nice text-to-speech audio files out of common document formats.   
Uses coqui-tts for realistic-sounding text-to-speech models. **NVIDIA GPU recommended for better performance.** 
## Supported formats:
- .epub,
- .pdf,
- .djvu,
- .html,
- .htm,
- .docx,
- .doc,
- .txt and all other raw text formats
# To-do
- Add chapters (one doc, multiple audio files) (preferably convert doc to .chp, which is a text file with chapter marks added)
- Add doc-to-text conversion for all supported formats
- Add directory conversion - all docs in dir will be turned into .txt, then synthesized into .wav
- (optional) add worse-sounding but lighter pyttsx3 version
# Credits
Started on July 12th, 2026 by C0m3b4ck. 
Used coqui-tts from [@idiap](https://github.com/idiap)
