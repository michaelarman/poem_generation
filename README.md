# NLP - Poems

Natural Language Processing (NLP) has evolved very rapidly in the past decade. It's a very complex field and it's always improving. 
This repo was made to try a few NLP tasks and algorithms on a specific type of corpus - **poems**.
These poems were scraped from [poemhunter](https://www.poemhunter.com) and the code for the scraping can be found [here](https://github.com/michaelarman/poem_generation/blob/main/poem_scraper.py)

## Types of Tasks
There are two main tasks that can be performed with the data available in this repo:
1) Text Generation - generating poems
2) Text Classification - classifiying topics or forms of poems

## Dataset
This dataset is comprised of two folders, both containing subfolders of poems.

These poems are categorized by the form (e.g. haiku, sonnet, etc.) or topic (love, nature, joy, peace, etc.).

Since the data is in this structure, it makes very simple to for API such as fastai or keras to get the text files.

## Poem Generation
Generating poems can be very simple with transformers. It's also possible to build a model from scratch and train it on the poems but the former is much easier and faster since it 
only requires you to finetune the model. There are a lot of transformers available on the [huggingface website](https://huggingface.co/models) with instructions for how to 
load them. There is also a very well done [tutorial](https://huggingface.co/blog/how-to-generate) for text generation using transformers.
I've finetuned a model on ballads using the GPT2 transformer. The results can be found in this [notebook](https://github.com/michaelarman/poem_generation/blob/main/PoemGenerator_FastAi.ipynb)

## Ideas and Future Work
It would be really interesting to create a model that would keep the same form throughout all its output. For example, if we train a model on haikus then it would be awesome to 
generate a haiku with the same syllable structure. Or another example would be generating rhymes using a poem form with rhythm. Since the data has a folder for topics you can also
generate poems of different topics but that would be much easier since you would just need to create a prompt with a distinguishable subject such as "I love it when" to indicate a love poem.

A webapp for generating poems is a great task with this data. The webapp can have a dropdown menu for what poem structure it should generate and what topic.

The scraping can also be sped up using multithreading.
