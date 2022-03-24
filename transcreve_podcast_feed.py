#!/usr/bin/env python3

from vosk import Model, KaldiRecognizer, SetLogLevel
import feedparser
import sys
import os
import wave
import subprocess
import srt
import json
import datetime
import requests

SetLogLevel(-1)

if len(sys.argv) != 3:
   print('Uso:')
   print('python3 {} <URL do feed> <diretório de saida>'.format(sys.argv[0]))
   exit(1)

if not os.path.exists("model"):
    print ("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
    exit (1)

WORDS_PER_LINE = 20

def transcribe():
    results = []
    subs = []
    while True:
       data = process.stdout.read(4000)
       if len(data) == 0:
           break
       if rec.AcceptWaveform(data):
           results.append(rec.Result())
    results.append(rec.FinalResult())

    for i, res in enumerate(results):
       jres = json.loads(res)
       if not 'result' in jres:
           continue
       words = jres['result']
       for j in range(0, len(words), WORDS_PER_LINE):
           line = words[j : j + WORDS_PER_LINE]
           s = srt.Subtitle(index=len(subs),
                   content=" ".join([l['word'] for l in line]),
                   start=datetime.timedelta(seconds=line[0]['start']),
                   end=datetime.timedelta(seconds=line[-1]['end']))
           subs.append(s)
    return subs

sample_rate=16000
model = Model("model")
rec = KaldiRecognizer(model, sample_rate)
rec.SetWords(True)

if os.path.exists('/tmp/semaforo_transcreve_podcast_feed.{}'.format(sys.argv[2])):
    print ('já em processamento')
    exit (1)
arq_semaforo = open('/tmp/semaforo_transcreve_podcast_feed.{}'.format(sys.argv[2]), 'w')
arq_semaforo.write('em execução')
arq_semaforo.close()

feed = feedparser.parse(sys.argv[1])

for i in feed.entries:
    print('Tratando "{}"...'.format(i['title']))
    nome_arq_saida = i['title'].replace('/', '_')
    if not os.path.exists('{}/{}'.format(sys.argv[2].replace('/', '_'), nome_arq_saida)):
        print('Fazendo download...')
        r = requests.get(i['links'][1]['href'])
        open('/tmp/arq_media_podcast.{}'.format(sys.argv[2].replace('/', '_')), 'wb').write(r.content)
        print('Processando...')
        process = subprocess.Popen(['ffmpeg', '-loglevel', 'quiet', '-i',
                                    '/tmp/arq_media_podcast.{}'.format(sys.argv[2].replace('/', '_')),
                                    '-ar', str(sample_rate) , '-ac', '1', '-f', 's16le', '-'],
                                    stdout=subprocess.PIPE)

        arq_saida = open('{}/{}'.format(sys.argv[2].replace('/', '_'), nome_arq_saida), 'w')
        arq_saida.write(srt.compose(transcribe()))
        arq_saida.close()
        os.remove('/tmp/arq_media_podcast.{}'.format(sys.argv[2].replace('/', '_')))

os.remove('/tmp/semaforo_transcreve_podcast_feed.{}'.format(sys.argv[2].replace('/', '_')))
