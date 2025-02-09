# 3️⃣ Initalize a pipeline
import argparse
import io
import os
from codecs import StreamReader, StreamWriter
from pathlib import Path
from typing import Generator

import soundfile as sf
from fastapi import FastAPI, Response
from fastapi.responses import FileResponse, StreamingResponse
from kokoro import KPipeline
from pypdf import PdfReader
from torch import Tensor


def split_at_size(text:str, size:int):
  return[text[y-size:y] for y in range(size, len(text)+size,size)]

def preprocess(text:str):
  text.replace("—","")
  return text

def pdf_to_wav(path:str, target_file: str, pipeline: KPipeline):
  reader = PdfReader(path)
  soundfile = sf.SoundFile(target_file,mode='x',samplerate=24000,channels=1)
  for page in reader.pages:
    text = preprocess(page.extract_text())
    texts= text.split('.')
    for txt in texts:
      for i, (gs, ps, audio) in enumerate(pipeline(txt, voice='af_heart', speed=1, split_pattern=None)):
        samples = audio.shape[0] if audio is not None else 0
        if samples > 0:
          try: 
            soundfile.write(audio) # save each audio file
          except Exception as e: 
            print(e)
            print('Error parsing text: ',gs)


if __name__ == "__main__":  

  parser = argparse.ArgumentParser("pdf_to_audiobook")
  parser.add_argument("path", help="Path to the pdf that should be converted into an audiobook", type=str)
  parser.add_argument("out_name", help="The name of the file that should be created with the audio of the pdf.", type=str)
  parser.add_argument("--out_path", help="The name of the file that should be created with the audio of the pdf.", type=str, default=None)
  parser.add_argument("--device", help="Decide what compute device to use to translate text to speech.'cuda' or 'cpu'. Make sure your system supports cuda if you want to pass that option",default='cpu')
  args = parser.parse_args()
  out_path = args.out_path
  cwd = os.getcwd()
  target_path = out_path if out_path else cwd
  file_name = args.out_name

  pipeline = KPipeline(lang_code='a',device=args.device)
  path = args.path
  target_file = target_path+'/'+file_name+".wav"
  wav_buffer = pdf_to_wav(path,target_file, pipeline)
