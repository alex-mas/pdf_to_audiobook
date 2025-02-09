
# About
This project uses kokoro and pypdf to convert pdf files to audio 


# Requisites
- Python
- Cuda compatible GPU if you wish to use GPU's to generate the audio

# Installation
- Wonder why kokoro uses so many dependencies
- Ask yourself if you trust the dependencies of the project
- If you still decide to go ahead, setup a venv(or not, up to you) and 
```
pip install requirements.txt
```

# Usage


```
python ./src/pdf_to_audiobook.py path/to/pdf.pdf out_name
```

For more information:
```
python ./src/pdf_to_audiobook.py -h
```


