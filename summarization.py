# install transformers module
from transformers import pipeline
import textwrap
import numpy as np
import pandas as pd
from pprint import pprint

def wrap(x):
    return textwrap.fill(x, replace_whitespace = False, fix_sentence_endings=True)

 # A key market indicator hasn’t been this high since the Great Recession


text = "10-year Treasury yields are flirting with 5% for the first time since 2007, before the global financial crisis. The 30-year fixed rate mortgage has been advancing towards 8% — a level not seen since the dot-com bubble popped in 2000. \
Rates may fluctuate, but it’s clear that we’re in the middle of a paradigm shift, said Rob Almeida at MFS Investment Management. It’s unlikely that rates will return to pre-pandemic lows, he said.\
There are a few reasons that the 10-year has advanced so quickly since last year, when it sat around 4%: Strong economic growth and elevated inflation tend to push yields higher. The US Treasury has issued a lot of government debt\
in recent months, and with expensive wars in Ukraine and the Middle East looming, more could be coming soon. \
Those things bring down bond prices and push yields higher, attracting buyers.\
Regardless of why it’s happening, for American consumers, an elevated 10-year Treasury return means economic pain: more costly car loans, credit card rates and even student debt.\
It also means more expensive mortgage rates. Mortgage rates tend to track the yield on 10-year US Treasuries. When Treasury yields go up, so do mortgage rates; when they go down, mortgage rates tend to follow.\
But what’s bad for the economy tends to be good for bringing prices down. Fed officials, including Powell, have indicated that rates could be high enough to help lower inflation towards their target goal of 2%.\
But they’re leaving the door open for further hikes based on future economic data."

# install sentencepiece for google-pegasus
#pip install protobuf==3.20.*
#pip install sentencepiece 
summarizer = pipeline('summarization',  model="google/pegasus-large")
summary_list = summarizer(text)
summary = summary_list[0]["summary_text"]

print(summary)

#distilbart-cnn-12-6 model
"""10-year Treasury yields are flirting with 5% for the first time since 2007, before the global financial crisis . \
    The 30-year fixed rate mortgage has been advancing towards 8% \
    — a level not seen since the dot-com bubble popped in 2000 . Strong economic growth \
    and elevated inflation tend to push yields higher ."""

#bart is trained on CNN daily
#bart-large-cnn
"""10-year Treasury yields are flirting with 5% for the first time since 2007, before the global financial crisis.\
      The 30-year fixed rate mortgage has been advancing towards 8% — a level not seen since the dot-com bubble popped in 2000.\
      Strong economic growth and elevated inflation tend to push yields higher."""

#google-pegasus
"""It’s unlikely that rates will return to pre-pandemic lows, he said.There are a few reasons that the 10-year \
    has advanced so quickly since last year,\
      when it sat around 4%: Strong economic growth and elevated inflation tend to push yields higher."""