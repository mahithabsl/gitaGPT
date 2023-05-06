import openai
import streamlit as st
import os
import requests
from bs4 import BeautifulSoup

# openai.api_key = os.getenv("OPENAI_API_KEY")
st.header("Jai Shree Krishna, Understand Gita today !")
openai.api_key = st.text_input("Enter your Openai API key", type="password")

base_audio_url = "https://www.holy-bhagavad-gita.org/public/audio/"
verse_url = 'https://www.holy-bhagavad-gita.org/chapter/'

def generate_response(prompt):

    try:
        completion = openai.Completion.create(
            engine='text-davinci-003',
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.6,
        )
        message = completion.choices[0].text
    except:
        message = ''
    return message


def main():

    random_question = st.text_input('Ask any question below/ Use the side navbar for meanings and summaries')

    languages = ['English', 'Marathi', 'Telugu', 'Tamil', 'Malayalam', 'Odisha', 'Kannada', 'Punjabi']
    language = st.sidebar.selectbox('Select Language', languages)
    aim = st.sidebar.radio('Summary/Meaning', ['Summary', 'Meaning'])
    chapter = st.sidebar.number_input('Chapter', 1, 18)


    # uncomment below when u have open ai key
    response1 = get_result(aim, chapter, language)

    if response1:
        placeholder = st.empty()
        placeholder.write("")
        placeholder.write(response1)

    if random_question:
        placeholder = st.empty()
        placeholder.write("")
        print(random_question)
        response2 = generate_response(random_question)
        placeholder.write(response2)

def get_audio_url(base_audio_url, chapter,verse):
    chapter = str(chapter).zfill(3)
    verse = str(verse).zfill(3)
    updated_audio_url = base_audio_url + chapter+'_' + verse + '.mp3'
    return updated_audio_url

def get_verse(verse_url,chapter,verse):
    updated_verse_url = verse_url+str(chapter)+'/verse/'+str(verse)

    response = requests.get(updated_verse_url)
    if response.ok:
        soup = BeautifulSoup(requests.get(updated_verse_url).text, "lxml")

        originalVerse_div = soup.find("div", {"id": "originalVerse"})
        originalVerse = originalVerse_div.get_text()
        return originalVerse

def get_result(aim, chapter, language):
    if aim == 'Meaning' and language:

        verse = st.sidebar.number_input('Verse', 1, 100)
        audio_url = get_audio_url(base_audio_url,chapter,verse)
        verse = get_verse(verse_url,chapter,verse)
        st.write(verse)
        st.audio(audio_url, format="audio/mp3")
        prompt_gpt = "You act as a Bhagavadgita teacher who tells the summary and meaning of Bhagavadgita" \
                     " to make others lives better. Keeping this is mind, Do the following: 1.Display" + " Chapter " + str(chapter) + " verse " + str(verse) + \
                     " as mentioned in Bhagavadgita in "+ language + \
                     " 2. Please explain to humans in the easiest way possible the meaning of the same in " + language

    elif aim == 'Summary' and chapter and language:
        prompt_gpt = "You act as a Bhagavadgita summariser to preach and make others lives better. Keeping this is mind, Do the following: " \
         "1.Summarise chapter " + str(chapter) + " of Bhagavadgita in " \
        + language+" 2.Provide your entire response in the same language"

    if st.sidebar.button("Answer"):
        print(prompt_gpt)
        response = generate_response(prompt_gpt)
        print(response)
        return response


main()
