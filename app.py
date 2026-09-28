import streamlit as st
import pandas as pd
import numpy as np
import re
import math
import random
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import Counter
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="ଓଡ଼ିଆ NLP Lab",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# CUSTOM CSS
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    /* Strong contrast + polished classroom-friendly theme */
    .main-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        font-size: 1.15rem;
        color: #a5b4fc !important;
        text-align: center;
        margin-bottom: 2rem;
        font-style: italic;
    }
    .hero-chip {
        display: inline-block;
        padding: 0.45rem 0.85rem;
        margin: 0.2rem;
        border-radius: 999px;
        background: rgba(99, 102, 241, 0.12);
        border: 1px solid rgba(129, 140, 248, 0.35);
        color: #c7d2fe !important;
        font-size: 0.82rem;
        font-weight: 700;
    }
    .card {
        background: #ffffff !important;
        color: #111827 !important;
        border: 1px solid #e5e7eb;
        border-radius: 18px;
        padding: 1.35rem;
        margin: 0.7rem 0;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.08);
        transition: transform 0.2s, box-shadow 0.2s;
        overflow: hidden;
    }
    .card, .card * {
        color: #111827 !important;
        -webkit-text-fill-color: #111827 !important;
    }
    .card h1, .card h2, .card h3, .card h4, .card h5, .card h6 {
        color: #111827 !important;
        font-weight: 800 !important;
    }
    .card p, .card li, .card span, .card div {
        color: #374151 !important;
    }
    .card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 16px rgba(0,0,0,0.08);
    }
    .token-card {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.6rem 1rem;
        border-radius: 10px;
        margin: 0.3rem;
        font-weight: 600;
        font-size: 1.1rem;
        box-shadow: 0 2px 6px rgba(102,126,234,0.4);
    }
    .token-card-odia {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        box-shadow: 0 2px 6px rgba(240,147,251,0.4);
    }
    .pipeline-box {
        background: #f9fafb;
        border: 2px dashed #d1d5db;
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        font-weight: 600;
        color: #374151;
        margin: 0.3rem 0;
    }
    .arrow-down {
        text-align: center;
        font-size: 1.5rem;
        color: #9ca3af;
        margin: 0.1rem 0;
    }
    .highlight-person { background-color: #fef3c7; padding: 2px 6px; border-radius: 6px; border-bottom: 2px solid #f59e0b; font-weight: 600; }
    .highlight-location { background-color: #d1fae5; padding: 2px 6px; border-radius: 6px; border-bottom: 2px solid #10b981; font-weight: 600; }
    .highlight-org { background-color: #dbeafe; padding: 2px 6px; border-radius: 6px; border-bottom: 2px solid #3b82f6; font-weight: 600; }
    .highlight-date { background-color: #fce7f3; padding: 2px 6px; border-radius: 6px; border-bottom: 2px solid #ec4899; font-weight: 600; }
    .pos-noun { background-color: #fef3c7; padding: 2px 6px; border-radius: 6px; }
    .pos-verb { background-color: #d1fae5; padding: 2px 6px; border-radius: 6px; }
    .pos-pron { background-color: #dbeafe; padding: 2px 6px; border-radius: 6px; }
    .pos-adj { background-color: #fce7f3; padding: 2px 6px; border-radius: 6px; }
    .pos-adv { background-color: #ede9fe; padding: 2px 6px; border-radius: 6px; }
    .pos-other { background-color: #f3f4f6; padding: 2px 6px; border-radius: 6px; }
    .step-badge {
        display: inline-block;
        background: #667eea;
        color: white;
        border-radius: 50%;
        width: 28px;
        height: 28px;
        text-align: center;
        line-height: 28px;
        font-weight: 700;
        margin-right: 8px;
    }
    .explain-box {
        background: #f0f9ff !important;
        color: #0f172a !important;
        border-left: 4px solid #0ea5e9;
        padding: 1rem;
        border-radius: 0 8px 8px 0;
        margin: 0.5rem 0;
    }
    .explain-box, .explain-box * {
        color: #0f172a !important;
    }
    .quiz-correct, .quiz-wrong, .quiz-correct *, .quiz-wrong * {
        color: #111827 !important;
    }
    .demo-badge {
        display: inline-block;
        background: #fbbf24;
        color: #78350f;
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
    }
    .quiz-correct { background: #d1fae5; border-left: 4px solid #10b981; padding: 0.8rem; border-radius: 0 8px 8px 0; }
    .quiz-wrong { background: #fee2e2; border-left: 4px solid #ef4444; padding: 0.8rem; border-radius: 0 8px 8px 0; }
    .test-callout {
        background: linear-gradient(135deg, #eef2ff 0%, #f5f3ff 100%) !important;
        color: #111827 !important;
        border: 1px solid #c7d2fe;
        border-radius: 14px;
        padding: 0.95rem 1rem;
        margin-top: 0.75rem;
        margin-bottom: 0.55rem;
        box-shadow: 0 6px 18px rgba(79, 70, 229, 0.08);
    }
    .test-callout, .test-callout * {
        color: #111827 !important;
        -webkit-text-fill-color: #111827 !important;
    }
    .test-callout-title {
        font-weight: 800;
        font-size: 1rem;
        margin-bottom: 0.15rem;
    }
    .test-callout-text {
        font-size: 0.82rem;
        color: #4b5563 !important;
        line-height: 1.35;
    }
    .stButton>button {
        border-radius: 10px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# SESSION STATE
# -----------------------------------------------------------------------------
if 'lang' not in st.session_state:
    st.session_state.lang = 'en'
if 'quiz_score' not in st.session_state:
    st.session_state.quiz_score = 0
if 'quiz_total' not in st.session_state:
    st.session_state.quiz_total = 0
if 'quiz_feedback' not in st.session_state:
    st.session_state.quiz_feedback = None
if 'page_request' not in st.session_state:
    st.session_state.page_request = None

def L(en, or_):
    """Return text based on selected language."""
    return or_ if st.session_state.lang == 'or' else en

# -----------------------------------------------------------------------------
# BUILT-IN DATA
# -----------------------------------------------------------------------------
ODIA_STOPWORDS = set([
    'ଏବଂ', 'ଓ', 'କିନ୍ତୁ', 'ତେବେ', 'ଯେ', 'ଏହା', 'ସେ', 'ମୁଁ', 'ତୁମେ', 'ଆମେ',
    'ତାଙ୍କ', 'ମୋର', 'ତୁମର', 'ଆମର', 'ଏହି', 'ସେହି', 'ଏକ', 'ଏକଟି', 'ରେ', 'ର',
    'କୁ', 'ଠାରୁ', 'ପାଇଁ', 'ସହ', 'ଦ୍ୱାରା', 'ନା', 'ନାହିଁ', 'ଅଛି', 'ଥିଲା', 'ହେବ'
])

ENGLISH_STOPWORDS = set([
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're",
    "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he',
    'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's",
    'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what',
    'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is',
    'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having',
    'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or',
    'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about',
    'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above',
    'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under',
    'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why',
    'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some',
    'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very',
    's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now',
    'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn',
    "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn',
    "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't",
    'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn',
    "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn',
    "wouldn't"
])

# Small Odia demo vocabulary for POS and NER
ODIA_POS_DEMO = {
    'ମୁଁ': ('PRON', 'I / I am'),
    'ତୁମେ': ('PRON', 'You'),
    'ସେ': ('PRON', 'He/She'),
    'ଆମେ': ('PRON', 'We'),
    'ଓଡ଼ିଆ': ('NOUN', 'Odia'),
    'ଭାଷା': ('NOUN', 'Language'),
    'ଭୁବନେଶ୍ୱର': ('NOUN', 'Bhubaneswar'),
    'ଓଡ଼ିଶା': ('NOUN', 'Odisha'),
    'ରାଜଧାନୀ': ('NOUN', 'Capital'),
    'ରାମ': ('NOUN', 'Ram'),
    'ଶିଖୁଛି': ('VERB', 'am learning'),
    'ପାଏ': ('VERB', 'love'),
    'ଗଲେ': ('VERB', 'went'),
    'ସୁନ୍ଦର': ('ADJ', 'beautiful'),
    'ପ୍ରସିଦ୍ଧ': ('ADJ', 'famous'),
    'ଭଲ': ('ADJ', 'good'),
    'ଆଉ': ('ADV', 'and/also'),
    'ବହୁତ': ('ADV', 'very'),
    'ଏବଂ': ('CONJ', 'and'),
    'ଓ': ('CONJ', 'and'),
    '।': ('PUNCT', 'Full stop'),
    ',': ('PUNCT', 'Comma'),
}

ODIA_NER_DEMO = {
    'ରାମ': 'PERSON',
    'ଭୁବନେଶ୍ୱର': 'LOCATION',
    'ଓଡ଼ିଶା': 'LOCATION',
    'ପୁରୀ': 'LOCATION',
    'ଭାରତ': 'LOCATION',
    'ରଥଯାତ୍ରା': 'EVENT',
}

# English demo POS lexicon
EN_POS_DEMO = {
    'i': ('PRON', 'First person pronoun'),
    'you': ('PRON', 'Second person pronoun'),
    'he': ('PRON', 'Third person masculine'),
    'she': ('PRON', 'Third person feminine'),
    'we': ('PRON', 'First person plural'),
    'they': ('PRON', 'Third person plural'),
    'ram': ('NOUN', 'Proper noun'),
    'sita': ('NOUN', 'Proper noun'),
    'bhubaneswar': ('NOUN', 'Proper noun'),
    'odisha': ('NOUN', 'Proper noun'),
    'language': ('NOUN', 'Common noun'),
    'nlp': ('NOUN', 'Proper noun'),
    'love': ('VERB', 'Action verb'),
    'learn': ('VERB', 'Action verb'),
    'learning': ('VERB', 'Action verb'),
    'went': ('VERB', 'Past tense'),
    'go': ('VERB', 'Action verb'),
    'is': ('VERB', 'Copula'),
    'am': ('VERB', 'Copula'),
    'are': ('VERB', 'Copula'),
    'beautiful': ('ADJ', 'Descriptive'),
    'famous': ('ADJ', 'Descriptive'),
    'good': ('ADJ', 'Descriptive'),
    'very': ('ADV', 'Intensifier'),
    'and': ('CONJ', 'Conjunction'),
    'but': ('CONJ', 'Conjunction'),
    'the': ('DET', 'Determiner'),
    'a': ('DET', 'Determiner'),
    'an': ('DET', 'Determiner'),
}

EN_NER_DEMO = {
    'ram': 'PERSON',
    'sita': 'PERSON',
    'bhubaneswar': 'LOCATION',
    'odisha': 'LOCATION',
    'puri': 'LOCATION',
    'india': 'LOCATION',
}

# Word vectors (educational, hand-crafted 2D)
WORD_VECTORS = {
    'king':   [0.9, 0.8],
    'queen':  [0.9, 0.2],
    'man':    [0.7, 0.7],
    'woman':  [0.7, 0.3],
    'prince': [0.8, 0.75],
    'princess':[0.8, 0.25],
    'boy':    [0.5, 0.7],
    'girl':   [0.5, 0.3],
    'apple':  [0.1, 0.9],
    'orange': [0.15, 0.85],
    'car':    [0.3, 0.1],
    'bus':    [0.35, 0.15],
}

TINY_CORPUS = [
    "the king rules the kingdom",
    "the queen rules the kingdom",
    "the man is strong",
    "the woman is wise",
    "the prince is young",
    "the princess is kind",
    "the boy plays in the park",
    "the girl reads a book",
    "the apple is red",
    "the orange is sweet",
    "the car is fast",
    "the bus is slow",
    "i love natural language processing",
    "nlp helps computers understand text",
    "ମୁଁ ଓଡ଼ିଆ ଭାଷାକୁ ଭଲ ପାଏ",
    "ଭୁବନେଶ୍ୱର ଓଡ଼ିଶାର ରାଜଧାନୀ",
    "ରାମ ଭୁବନେଶ୍ୱରକୁ ଗଲେ",
    "ସେ ଓଡ଼ିଆ ଶିଖୁଛି",
]

QUIZ_BANK = [
    {
        'q_en': 'What does NLP stand for?',
        'q_or': 'NLP ର ପୂର୍ଣ୍ଣ ରୂପ କଣ?',
        'options_en': ['Natural Language Processing', 'New Language Program', 'Neural Language Protocol', 'Numeric Language Processing'],
        'options_or': ['ନ୍ୟାଚୁରାଲ ଲାଙ୍ଗୁଏଜ ପ୍ରୋସେସିଂ', 'ନ୍ୟୁ ଲାଙ୍ଗୁଏଜ ପ୍ରୋଗ୍ରାମ', 'ନ୍ୟୁରାଲ ଲାଙ୍ଗୁଏଜ ପ୍ରୋଟୋକଲ', 'ନ୍ୟୁମେରିକ ଲାଙ୍ଗୁଏଜ ପ୍ରୋସେସିଂ'],
        'answer': 0,
        'explanation_en': 'NLP stands for Natural Language Processing — making computers understand human language.',
        'explanation_or': 'NLP ର ଅର୍ଥ ନ୍ୟାଚୁରାଲ ଲାଙ୍ଗୁଏଜ ପ୍ରୋସେସିଂ — କମ୍ପ୍ୟୁଟରକୁ ମାନବ ଭାଷା ବୁଝାଇବା।'
    },
    {
        'q_en': 'What is tokenization?',
        'q_or': 'ଟୋକେନାଇଜେସନ କଣ?',
        'options_en': ['Breaking text into smaller units', 'Translating text', 'Removing all words', 'Making text longer'],
        'options_or': ['ଟେକ୍ସଟକୁ ଛୋଟ ଏକକରେ ବିଭକ୍ତ କରିବା', 'ଟେକ୍ସଟ ଅନୁବାଦ କରିବା', 'ସମସ୍ତ ଶବ୍ଦ ହଟାଇବା', 'ଟେକ୍ସଟ ଲମ୍ବା କରିବା'],
        'answer': 0,
        'explanation_en': 'Tokenization splits text into tokens — words, sentences, or subwords.',
        'explanation_or': 'ଟୋକେନାଇଜେସନ ଟେକ୍ସଟକୁ ଟୋକେନରେ ବିଭକ୍ତ କରେ — ଶବ୍ଦ, ବାକ୍ୟ, କିମ୍ବା ଉପ-ଶବ୍ଦ।'
    },
    {
        'q_en': 'Which of these is a stopword?',
        'q_or': 'ଏଥିମଧ୍ୟରୁ କେଉଁଟି ଏକ ଷ୍ଟପୱାର୍ଡ?',
        'options_en': ['the', 'king', 'run', 'blue'],
        'options_or': ['the', 'king', 'run', 'blue'],
        'answer': 0,
        'explanation_en': '"the" is a common stopword — it carries little meaning on its own.',
        'explanation_or': '"the" ଏକ ସାଧାରଣ ଷ୍ଟପୱାର୍ଡ — ଏହା ନିଜେ ଅଳ୍ପ ଅର୍ଥ ବହନ କରେ।'
    },
    {
        'q_en': 'What is a bigram?',
        'q_or': 'ବାଇଗ୍ରାମ କଣ?',
        'options_en': ['A sequence of 2 words', 'A sequence of 1 word', 'A sequence of 3 words', 'A sentence'],
        'options_or': ['୨ଟି ଶବ୍ଦର କ୍ରମ', '୧ଟି ଶବ୍ଦର କ୍ରମ', '୩ଟି ଶବ୍ଦର କ୍ରମ', 'ଏକ ବାକ୍ୟ'],
        'answer': 0,
        'explanation_en': 'A bigram is a sequence of two consecutive words, like "I love".',
        'explanation_or': 'ବାଇଗ୍ରାମ ହେଉଛି ଦୁଇଟି କ୍ରମିକ ଶବ୍ଦର କ୍ରମ, ଯେପରି "I love"।'
    },
    {
        'q_en': 'What does POS tagging identify?',
        'q_or': 'POS ଟ୍ୟାଗିଂ କଣ ଚିହ୍ନଟ କରେ?',
        'options_en': ['Part of speech of each word', 'Sentiment of text', 'Named entities', 'Word frequency'],
        'options_or': ['ପ୍ରତ୍ୟେକ ଶବ୍ଦର ପାର୍ଟ ଅଫ ସ୍ପିଚ', 'ଟେକ୍ସଟର ସେଣ୍ଟିମେଣ୍ଟ', 'ନାମିତ ସତ୍ତା', 'ଶବ୍ଦ ଆବୃତ୍ତି'],
        'answer': 0,
        'explanation_en': 'POS tagging labels each word as noun, verb, adjective, etc.',
        'explanation_or': 'POS ଟ୍ୟାଗିଂ ପ୍ରତ୍ୟେକ ଶବ୍ଦକୁ ବିଶେଷ୍ୟ, କ୍ରିୟା, ବିଶେଷଣ ଆଦି ଭାବରେ ଲେବଲ କରେ।'
    },
    {
        'q_en': 'What is Named Entity Recognition?',
        'q_or': 'ନାମିତ ସତ୍ତା ଚିହ୍ନଟ କଣ?',
        'options_en': ['Identifying names, places, organizations in text', 'Counting words', 'Translating text', 'Removing punctuation'],
        'options_or': ['ଟେକ୍ସଟରେ ନାମ, ସ୍ଥାନ, ସଂସ୍ଥା ଚିହ୍ନଟ କରିବା', 'ଶବ୍ଦ ଗଣନା', 'ଟେକ୍ସଟ ଅନୁବାଦ', 'ବିରାମ ଚିହ୍ନ ହଟାଇବା'],
        'answer': 0,
        'explanation_en': 'NER finds and classifies entities like persons, locations, and organizations.',
        'explanation_or': 'NER ବ୍ୟକ୍ତି, ସ୍ଥାନ, ସଂସ୍ଥା ଭଳି ସତ୍ତା ଖୋଜି ଶ୍ରେଣୀବଦ୍ଧ କରେ।'
    },
    {
        'q_en': 'What does TF-IDF measure?',
        'q_or': 'TF-IDF କଣ ମାପେ?',
        'options_en': ['Importance of a word in a document', 'Length of a sentence', 'Number of paragraphs', 'Grammar correctness'],
        'options_or': ['ଏକ ଡକ୍ୟୁମେଣ୍ଟରେ ଏକ ଶବ୍ଦର ଗୁରୁତ୍ୱ', 'ଏକ ବାକ୍ୟର ଲମ୍ବ', 'ପାରାଗ୍ରାଫ ସଂଖ୍ୟା', 'ବ୍ୟାକରଣ ଶୁଦ୍ଧତା'],
        'answer': 0,
        'explanation_en': 'TF-IDF balances how often a word appears in a document with how rare it is across documents.',
        'explanation_or': 'TF-IDF ଏକ ଡକ୍ୟୁମେଣ୍ଟରେ ଶବ୍ଦର ଆବୃତ୍ତି ଏବଂ ସମସ୍ତ ଡକ୍ୟୁମେଣ୍ଟରେ ଏହାର ବିରଳତାକୁ ସନ୍ତୁଳିତ କରେ।'
    },
    {
        'q_en': 'What is cosine similarity used for?',
        'q_or': 'କୋସାଇନ ସିମିଲାରିଟି କିପାଇଁ ବ୍ୟବହୃତ ହୁଏ?',
        'options_en': ['Measuring similarity between vectors', 'Counting sentences', 'Tagging POS', 'Splitting words'],
        'options_or': ['ଭେକ୍ଟର ମଧ୍ୟରେ ସମାନତା ମାପିବା', 'ବାକ୍ୟ ଗଣନା', 'POS ଟ୍ୟାଗିଂ', 'ଶବ୍ଦ ବିଭାଜନ'],
        'answer': 0,
        'explanation_en': 'Cosine similarity measures the angle between two vectors — smaller angle means more similar.',
        'explanation_or': 'କୋସାଇନ ସିମିଲାରିଟି ଦୁଇଟି ଭେକ୍ଟର ମଧ୍ୟରେ କୋଣ ମାପେ — ଛୋଟ କୋଣ ଅର୍ଥ ଅଧିକ ସମାନ।'
    },
    {
        'q_en': 'In parsing, what is a parse tree?',
        'q_or': 'ପାର୍ସିଂରେ ଏକ ପାର୍ସ ଟ୍ରି କଣ?',
        'options_en': ['A tree showing grammatical structure', 'A list of words', 'A type of token', 'A sentiment score'],
        'options_or': ['ବ୍ୟାକରଣିକ ଗଠନ ଦର୍ଶାଉଥିବା ଏକ ଟ୍ରି', 'ଶବ୍ଦର ତାଲିକା', 'ଏକ ପ୍ରକାରର ଟୋକେନ', 'ଏକ ସେଣ୍ଟିମେଣ୍ଟ ସ୍କୋର'],
        'answer': 0,
        'explanation_en': 'A parse tree shows how words group into phrases and sentences.',
        'explanation_or': 'ଏକ ପାର୍ସ ଟ୍ରି ଦର୍ଶାଏ ଯେ ଶବ୍ଦଗୁଡ଼ିକ କିପରି ବାକ୍ୟାଂଶ ଏବଂ ବାକ୍ୟରେ ଗଠିତ ହୁଏ।'
    },
    {
        'q_en': 'What is perplexity in language models?',
        'q_or': 'ଭାଷା ମଡେଲରେ ପର୍ପ୍ଲେକ୍ସିଟି କଣ?',
        'options_en': ['A measure of how confused a model is', 'A type of token', 'A grammar rule', 'A vector dimension'],
        'options_or': ['ଏକ ମଡେଲ କେତେ ଦ୍ୱନ୍ଦ୍ୱରେ ଅଛି ତାହାର ମାପ', 'ଏକ ପ୍ରକାରର ଟୋକେନ', 'ଏକ ବ୍ୟାକରଣ ନିୟମ', 'ଏକ ଭେକ୍ଟର ଡାଇମେନ୍ସନ'],
        'answer': 0,
        'explanation_en': 'Lower perplexity means the model is less confused and predicts better.',
        'explanation_or': 'କମ୍ ପର୍ପ୍ଲେକ୍ସିଟି ଅର୍ଥ ମଡେଲ କମ୍ ଦ୍ୱନ୍ଦ୍ୱରେ ଅଛି ଏବଂ ଭଲ ଭବିଷ୍ୟବାଣୀ କରେ।'
    },
]

# -----------------------------------------------------------------------------
# HELPER FUNCTIONS
# -----------------------------------------------------------------------------
def simple_word_tokenize(text):
    """Split text into word tokens (handles Odia and English punctuation)."""
    text = re.sub(r'([।,!?;:])', r' \1 ', text)
    tokens = text.split()
    return [t for t in tokens if t.strip()]

def simple_sentence_tokenize(text):
    """Split text into sentences."""
    parts = re.split(r'([।.!?]+)', text)
    sentences = []
    for i in range(0, len(parts) - 1, 2):
        s = (parts[i] + parts[i+1]).strip()
        if s:
            sentences.append(s)
    if len(parts) % 2 == 1 and parts[-1].strip():
        sentences.append(parts[-1].strip())
    return sentences if sentences else [text.strip()]

def get_stopwords(lang):
    return ODIA_STOPWORDS if lang == 'or' else ENGLISH_STOPWORDS

def remove_stopwords(tokens, lang):
    sw = get_stopwords(lang)
    return [t for t in tokens if t.lower() not in sw and t not in sw]

def simple_stem(word):
    """Very simple English stemmer for demo."""
    w = word.lower()
    for suffix in ['ing', 'edly', 'ed', 'ly', 'es', 's']:
        if w.endswith(suffix) and len(w) > len(suffix) + 2:
            return w[:-len(suffix)]
    return w

def simple_lemmatize(word):
    """Very simple English lemmatizer for demo."""
    w = word.lower()
    irregular = {'went': 'go', 'gone': 'go', 'was': 'be', 'were': 'be', 'is': 'be',
                 'are': 'be', 'am': 'be', 'has': 'have', 'had': 'have', 'did': 'do',
                 'does': 'do', 'children': 'child', 'men': 'man', 'women': 'woman'}
    if w in irregular:
        return irregular[w]
    for suffix, repl in [('ies', 'y'), ('ves', 'f'), ('ses', 's'), ('es', ''), ('s', '')]:
        if w.endswith(suffix) and len(w) > len(suffix) + 1:
            return w[:-len(suffix)] + repl
    return w

def pos_tag_demo(tokens, lang):
    """Rule-based POS tagging for demo."""
    results = []
    lexicon = ODIA_POS_DEMO if lang == 'or' else EN_POS_DEMO
    for tok in tokens:
        key = tok.lower() if lang == 'en' else tok
        if key in lexicon:
            tag, meaning = lexicon[key]
        else:
            # Guessing rules
            if lang == 'en':
                if tok.lower().endswith('ly'):
                    tag, meaning = 'ADV', 'Adverb (guessed)'
                elif tok.lower().endswith('ing'):
                    tag, meaning = 'VERB', 'Verb (guessed)'
                elif tok[0].isupper() and len(tok) > 1:
                    tag, meaning = 'NOUN', 'Proper noun (guessed)'
                elif tok.isdigit():
                    tag, meaning = 'NUM', 'Number'
                else:
                    tag, meaning = 'NOUN', 'Noun (guessed)'
            else:
                if tok.endswith('।') or tok in ('।', ','):
                    tag, meaning = 'PUNCT', 'Punctuation'
                elif tok.endswith('ଛି') or tok.endswith('ଲେ') or tok.endswith('ବ'):
                    tag, meaning = 'VERB', 'କ୍ରିୟା (ଅନୁମାନ)'
                elif tok.endswith('ର') or tok.endswith('ରେ'):
                    tag, meaning = 'NOUN', 'ବିଶେଷ୍ୟ (ଅନୁମାନ)'
                else:
                    tag, meaning = 'NOUN', 'ବିଶେଷ୍ୟ (ଅନୁମାନ)'
        results.append((tok, tag, meaning))
    return results

def ner_demo(tokens, lang):
    """Rule-based NER for demo."""
    entities = []
    lexicon = ODIA_NER_DEMO if lang == 'or' else EN_NER_DEMO
    for tok in tokens:
        key = tok.lower() if lang == 'en' else tok
        if key in lexicon:
            entities.append((tok, lexicon[key]))
    return entities

def generate_ngrams(tokens, n):
    """Generate n-grams from a list of tokens."""
    if len(tokens) < n:
        return []
    return [tuple(tokens[i:i+n]) for i in range(len(tokens) - n + 1)]

def ngram_frequencies(ngrams):
    return Counter(ngrams)

def ngram_probabilities(ngrams, n):
    """Compute probabilities of n-grams."""
    if not ngrams:
        return {}
    if n == 1:
        total = len(ngrams)
        freq = Counter(ngrams)
        return {g: c / total for g, c in freq.items()}
    else:
        # For bigram/trigram, P(w_n | w_1..w_{n-1})
        result = {}
        freq_all = Counter(ngrams)
        if n == 2:
            unigrams = [g[0] for g in ngrams]
            freq_prev = Counter(unigrams)
            for g, c in freq_all.items():
                result[g] = c / freq_prev[g[0]] if freq_prev[g[0]] > 0 else 0
        elif n == 3:
            bigrams = [g[:2] for g in ngrams]
            freq_prev = Counter(bigrams)
            for g, c in freq_all.items():
                result[g] = c / freq_prev[g[:2]] if freq_prev[g[:2]] > 0 else 0
        return result

def cosine_similarity(a, b):
    a = np.array(a, dtype=float)
    b = np.array(b, dtype=float)
    denom = np.linalg.norm(a) * np.linalg.norm(b)
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)

def draw_parse_tree(sentence):
    """Draw a simple parse tree using plotly."""
    words = simple_word_tokenize(sentence)
    words = [w for w in words if w not in ('।', '.', ',')]
    # Simple grammar: S -> NP VP; NP -> DET N | N; VP -> V NP | V
    # We'll just draw a fixed structure for demo
    fig = go.Figure()
    # Simple fixed layout
    positions = {
        'S': (0.5, 1.0),
        'NP': (0.25, 0.7),
        'VP': (0.75, 0.7),
        'V': (0.6, 0.4),
        'NP2': (0.9, 0.4),
    }
    # We'll draw a generic tree with words at bottom
    n = len(words)
    word_x = [i / max(n-1, 1) * 0.8 + 0.1 for i in range(n)]
    # Draw edges
    fig.add_trace(go.Scatter(x=[0.5, 0.25], y=[1.0, 0.7], mode='lines', line=dict(color='#667eea', width=2), showlegend=False))
    fig.add_trace(go.Scatter(x=[0.5, 0.75], y=[1.0, 0.7], mode='lines', line=dict(color='#667eea', width=2), showlegend=False))
    fig.add_trace(go.Scatter(x=[0.25, 0.25], y=[0.7, 0.4], mode='lines', line=dict(color='#667eea', width=2), showlegend=False))
    fig.add_trace(go.Scatter(x=[0.75, 0.75], y=[0.7, 0.4], mode='lines', line=dict(color='#667eea', width=2), showlegend=False))
    # Nodes
    fig.add_trace(go.Scatter(x=[0.5], y=[1.0], mode='markers+text', marker=dict(size=40, color='#764ba2'), text=['S'], textposition='middle center', textfont=dict(color='white', size=14), showlegend=False))
    fig.add_trace(go.Scatter(x=[0.25], y=[0.7], mode='markers+text', marker=dict(size=36, color='#667eea'), text=['NP'], textposition='middle center', textfont=dict(color='white', size=12), showlegend=False))
    fig.add_trace(go.Scatter(x=[0.75], y=[0.7], mode='markers+text', marker=dict(size=36, color='#667eea'), text=['VP'], textposition='middle center', textfont=dict(color='white', size=12), showlegend=False))
    fig.add_trace(go.Scatter(x=[0.75], y=[0.4], mode='markers+text', marker=dict(size=32, color='#f093fb'), text=['V'], textposition='middle center', textfont=dict(color='white', size=11), showlegend=False))
    # Words at bottom
    for i, w in enumerate(words):
        fig.add_trace(go.Scatter(x=[word_x[i]], y=[0.05], mode='markers+text', marker=dict(size=30, color='#fbbf24'), text=[w], textposition='middle center', textfont=dict(color='#78350f', size=11), showlegend=False))
        fig.add_trace(go.Scatter(x=[word_x[i], 0.5], y=[0.05, 0.4], mode='lines', line=dict(color='#d1d5db', width=1, dash='dot'), showlegend=False))
    fig.update_layout(
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0, 1]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0, 1.1]),
        height=350, margin=dict(l=20, r=20, t=20, b=20),
        plot_bgcolor='white', paper_bgcolor='white'
    )
    return fig

def draw_pipeline_steps(steps, lang='en'):
    """Draw a visual pipeline with arrows."""
    html = '<div style="display:flex; flex-direction:column; align-items:center; gap:0;">'
    for i, step in enumerate(steps):
        html += f'<div class="pipeline-box">{step}</div>'
        if i < len(steps) - 1:
            html += '<div class="arrow-down">↓</div>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# SIDEBAR
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🧪 ଓଡ଼ିଆ NLP Lab")
    st.markdown("---")
    lang_choice = st.radio(
        L("Language", "ଭାଷା"),
        options=["English", "ଓଡ଼ିଆ"],
        index=0 if st.session_state.lang == 'en' else 1,
        horizontal=True
    )
    st.session_state.lang = 'en' if lang_choice == "English" else 'or'
    st.markdown("---")

    pages = [
        ("🏠", L("Home", "ଘର")),
        ("📚", L("Learn NLP", "NLP ଶିଖନ୍ତୁ")),
        ("📝", L("Test Yourself", "ନିଜକୁ ପରୀକ୍ଷା କରନ୍ତୁ")),
        ("🧹", L("Text Preprocessing", "ଟେକ୍ସଟ ପ୍ରିପ୍ରୋସେସିଂ")),
        ("🔤", L("Tokenization", "ଟୋକେନାଇଜେସନ")),
        ("🏷️", L("POS Tagging", "POS ଟ୍ୟାଗିଂ")),
        ("📍", L("Named Entity Recognition", "ନାମିତ ସତ୍ତା ଚିହ୍ନଟ")),
        ("😊", L("Sentiment Analysis", "ସେଣ୍ଟିମେଣ୍ଟ ବିଶ୍ଳେଷଣ")),
        ("🔢", L("N-Grams", "ଏନ-ଗ୍ରାମ")),
        ("🧠", L("Language Models", "ଭାଷା ମଡେଲ")),
        ("🌳", L("Parsing", "ପାର୍ସିଂ")),
        ("📐", L("Word Vectors & Semantics", "ଶବ୍ଦ ଭେକ୍ଟର ଏବଂ ଅର୍ଥବିଜ୍ଞାନ")),
        ("🧮", L("NLP Mathematics", "NLP ଗଣିତ")),
        ("🧪", L("Experiment Lab", "ପରୀକ୍ଷାଗାର")),
        ("ℹ️", L("About", "ବିଷୟରେ")),
    ]

    page_options = [f"{icon} {name}" for icon, name in pages]
    requested = st.session_state.get("page_request")
    default_index = 0
    if requested in page_options:
        default_index = page_options.index(requested)
        st.session_state.page_request = None

    selected = st.radio(
        "",
        page_options,
        index=default_index,
        label_visibility="collapsed"
    )

    st.markdown(
        f'''
        <div class="test-callout">
            <div class="test-callout-title">📝 {L("Test Yourself", "ନିଜକୁ ପରୀକ୍ଷା କରନ୍ତୁ")}</div>
            <div class="test-callout-text">
                {L("Check what you learned with a quick NLP test.", "ଏକ ଛୋଟ NLP ପରୀକ୍ଷା ମାଧ୍ୟମରେ ଆପଣ କଣ ଶିଖିଲେ ଯାଞ୍ଚ କରନ୍ତୁ।")}
            </div>
        </div>
        ''',
        unsafe_allow_html=True
    )

    if st.button(
        L("📝 Open Test", "📝 ପରୀକ୍ଷା ଖୋଲନ୍ତୁ"),
        use_container_width=True,
        type="secondary"
    ):
        st.session_state.page_request = page_options[2]
        st.rerun()

    st.markdown("---")
    st.caption(L("Educational app • Your answers stay in this session.", "ଶିକ୍ଷାମୂଳକ ଆପ୍ • ଆପଣଙ୍କ ଉତ୍ତର କେବଳ ଏହି ସେସନରେ ରହିଥାଏ।"))

# Extract page name
page_name = selected.split(" ", 1)[1] if " " in selected else selected

# =============================================================================
# PAGE: HOME
# =============================================================================
if "Home" in selected or "ଘର" in selected:
    st.markdown('<div class="main-title">ଓଡ଼ିଆ NLP Lab</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="subtitle">{L("Learn NLP by Seeing It in Action", "କାର୍ଯ୍ୟରେ ଦେଖି NLP ଶିଖନ୍ତୁ")}</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card">
        <h3>🔍 {L("What is NLP?", "NLP କ'ଣ?")}</h3>
        <p>{L("Natural Language Processing (NLP) is a field of AI that helps computers understand, interpret, and generate human language. It bridges the gap between human communication and computer understanding.", "ନ୍ୟାଚୁରାଲ ଲାଙ୍ଗୁଏଜ ପ୍ରୋସେସିଂ (NLP) ହେଉଛି AI ର ଏକ କ୍ଷେତ୍ର ଯାହା କମ୍ପ୍ୟୁଟରକୁ ମାନବ ଭାଷା ବୁଝିବାରେ, ବ୍ୟାଖ୍ୟା କରିବାରେ ଏବଂ ସୃଷ୍ଟି କରିବାରେ ସାହାଯ୍ୟ କରେ।")}</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="card">
            <h4>🤔 {L("Why do we need NLP?", "ଆମକୁ NLP କାହିଁକି ଦରକାର?")}</h4>
            <ul>
                <li>{L("Computers only understand numbers", "କମ୍ପ୍ୟୁଟର କେବଳ ସଂଖ୍ୟା ବୁଝେ")}</li>
                <li>{L("Human language is complex and ambiguous", "ମାନବ ଭାଷା ଜଟିଳ ଏବଂ ଦ୍ୱନ୍ଦ୍ୱପୂର୍ଣ୍ଣ")}</li>
                <li>{L("We need to search, translate, and analyze text", "ଆମକୁ ଟେକ୍ସଟ ଖୋଜିବା, ଅନୁବାଦ କରିବା ଏବଂ ବିଶ୍ଳେଷଣ କରିବା ଆବଶ୍ୟକ")}</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="card">
            <h4>🌍 {L("Where is NLP used?", "NLP କେଉଁଠି ବ୍ୟବହୃତ ହୁଏ?")}</h4>
            <ul>
                <li>🔎 Google Search</li>
                <li>💬 Chatbots</li>
                <li>🌐 Translation</li>
                <li>🎙️ Voice Assistants</li>
                <li>📧 Spam Detection</li>
                <li>🎬 Recommendations</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="card">
            <h4>🎯 {L("What can you do here?", "ଆପଣ ଏଠାରେ କଣ କରିପାରିବେ?")}</h4>
            <ul>
                <li>{L("Learn NLP concepts step by step", "ପର୍ଯ୍ୟାୟକ୍ରମେ NLP ଧାରଣା ଶିଖନ୍ତୁ")}</li>
                <li>{L("Try interactive examples", "ଇଣ୍ଟରାକ୍ଟିଭ ଉଦାହରଣ ଚେଷ୍ଟା କରନ୍ତୁ")}</li>
                <li>{L("See visualizations", "ଭିଜୁଆଲାଇଜେସନ ଦେଖନ୍ତୁ")}</li>
                <li>{L("Experiment and quiz yourself", "ପରୀକ୍ଷା କରନ୍ତୁ ଏବଂ ନିଜକୁ କୁଇଜ କରନ୍ତୁ")}</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"### 🔄 {L('The NLP Pipeline', 'NLP ପାଇପଲାଇନ')}")
    draw_pipeline_steps([
        L("Human Language", "ମାନବ ଭାଷା"),
        L("Text", "ଟେକ୍ସଟ"),
        L("Processing", "ପ୍ରକ୍ରିୟାକରଣ"),
        L("Analysis", "ବିଶ୍ଳେଷଣ"),
        L("Understanding", "ବୁଝିବା"),
        L("Result", "ଫଳାଫଳ"),
    ])

    st.markdown("---")
    st.markdown(f"### 📦 {L('What You Will Explore', 'ଆପଣ କଣ ଅନ୍ୱେଷଣ କରିବେ')}")
    cols = st.columns(5)
    cards = [
        ("🔤", L("Text", "ଟେକ୍ସଟ")),
        ("🧠", L("Language", "ଭାଷା")),
        ("📊", L("Data", "ଡାଟା")),
        ("🤖", L("AI", "AI")),
        ("📈", L("Visualization", "ଭିଜୁଆଲାଇଜେସନ")),
    ]
    for col, (icon, label) in zip(cols, cards):
        with col:
            st.markdown(f"""
            <div class="card" style="text-align:center;">
                <div style="font-size:2.5rem;">{icon}</div>
                <div style="font-weight:700;">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    test_col1, test_col2 = st.columns([3, 1])
    with test_col1:
        st.markdown(f'''
        <div class="card" style="border:2px solid #c7d2fe; background:linear-gradient(135deg,#eef2ff 0%,#faf5ff 100%);">
            <h3 style="margin-bottom:0.25rem;">📝 {L("Test Yourself", "ନିଜକୁ ପରୀକ୍ଷା କରନ୍ତୁ")}</h3>
            <p style="margin-bottom:0;">{L(
                "Finished learning? Take a quick test and instantly see your score and explanations.",
                "ଶିଖିବା ସରିଲା କି? ଏକ ଛୋଟ ପରୀକ୍ଷା ଦିଅନ୍ତୁ ଏବଂ ସଙ୍ଗେ ସଙ୍ଗେ ସ୍କୋର ଓ ବ୍ୟାଖ୍ୟା ଦେଖନ୍ତୁ।"
            )}</p>
        </div>
        ''', unsafe_allow_html=True)
    with test_col2:
        st.markdown("<div style='height:0.55rem'></div>", unsafe_allow_html=True)
        if st.button(L("📝 Start Test", "📝 ପରୀକ୍ଷା ଆରମ୍ଭ"), use_container_width=True, type="primary"):
            st.session_state.page_request = page_options[2]
            st.rerun()

    st.markdown("")
    if st.button(L("🚀 Start Learning", "🚀 ଶିଖିବା ଆରମ୍ଭ କରନ୍ତୁ"), use_container_width=True):
        st.info(L("👉 Use the sidebar to navigate to 'Learn NLP' or any topic!", "👉 'NLP ଶିଖନ୍ତୁ' କିମ୍ବା ଯେକୌଣସି ବିଷୟକୁ ଯିବା ପାଇଁ ସାଇଡବାର ବ୍ୟବହାର କରନ୍ତୁ!"))

# =============================================================================
# PAGE: LEARN NLP
# =============================================================================
elif "Learn NLP" in selected or "NLP ଶିଖନ୍ତୁ" in selected:
    st.title(f"📚 {L('Learn NLP', 'NLP ଶିଖନ୍ତୁ')}")
    st.markdown(L("A beginner-friendly tour of Natural Language Processing concepts.", "ନ୍ୟାଚୁରାଲ ଲାଙ୍ଗୁଏଜ ପ୍ରୋସେସିଂ ଧାରଣାର ଏକ ଆରମ୍ଭକାରୀ-ବାନ୍ଧବ ଭ୍ରମଣ।"))

    topics = [
        {
            "title": L("What is Text?", "ଟେକ୍ସଟ କ'ଣ?"),
            "what": L("Text is any written language — sentences, paragraphs, documents.", "ଟେକ୍ସଟ ହେଉଛି ଯେକୌଣସି ଲିଖିତ ଭାଷା — ବାକ୍ୟ, ପାରାଗ୍ରାଫ, ଡକ୍ୟୁମେଣ୍ଟ।"),
            "why": L("Computers need text in a structured form to process it.", "କମ୍ପ୍ୟୁଟରକୁ ପ୍ରକ୍ରିୟାକରଣ ପାଇଁ ଟେକ୍ସଟ ଏକ ସଂରଚିତ ରୂପରେ ଆବଶ୍ୟକ।"),
            "how": L("We break text into smaller units like words and sentences.", "ଆମେ ଟେକ୍ସଟକୁ ଶବ୍ଦ ଏବଂ ବାକ୍ୟ ଭଳି ଛୋଟ ଏକକରେ ବିଭକ୍ତ କରୁ।"),
            "example": "ମୁଁ ଓଡ଼ିଆ ଭାଷାକୁ ଭଲ ପାଏ।"
        },
        {
            "title": L("Tokenization", "ଟୋକେନାଇଜେସନ"),
            "what": L("Splitting text into tokens (words, sentences, subwords).", "ଟେକ୍ସଟକୁ ଟୋକେନରେ ବିଭକ୍ତ କରିବା (ଶବ୍ଦ, ବାକ୍ୟ, ଉପ-ଶବ୍ଦ)।"),
            "why": L("Most NLP algorithms work on tokens, not raw text.", "ଅଧିକାଂଶ NLP ଆଲଗୋରିଦମ କଞ୍ଚା ଟେକ୍ସଟ ଉପରେ ନୁହେଁ, ଟୋକେନ ଉପରେ କାମ କରେ।"),
            "how": L("Use rules (spaces, punctuation) or statistical models.", "ନିୟମ (ସ୍ପେସ, ବିରାମ ଚିହ୍ନ) କିମ୍ବା ସାଂଖ୍ୟିକ ମଡେଲ ବ୍ୟବହାର କରନ୍ତୁ।"),
            "example": "ମୁଁ | ଓଡ଼ିଆ | ଶିଖୁଛି | ।"
        },
        {
            "title": L("Stopword Removal", "ଷ୍ଟପୱାର୍ଡ ଅପସାରଣ"),
            "what": L("Removing common words that add little meaning.", "ସାଧାରଣ ଶବ୍ଦ ହଟାଇବା ଯାହା ଅଳ୍ପ ଅର୍ଥ ଯୋଡ଼େ।"),
            "why": L("Reduces noise and focuses on important words.", "ଶବ୍ଦ ହ୍ରାସ କରେ ଏବଂ ଗୁରୁତ୍ୱପୂର୍ଣ୍ଣ ଶବ୍ଦ ଉପରେ ଧ୍ୟାନ ଦିଏ।"),
            "how": L("Maintain a list of stopwords and filter them out.", "ଷ୍ଟପୱାର୍ଡର ଏକ ତାଲିକା ରଖନ୍ତୁ ଏବଂ ସେଗୁଡ଼ିକୁ ଫିଲ୍ଟର କରନ୍ତୁ।"),
            "example": L("'I love NLP' → 'love NLP'", "'ମୁଁ ଓଡ଼ିଆ ଭଲ ପାଏ' → 'ଓଡ଼ିଆ ଭଲ ପାଏ'")
        },
        {
            "title": L("POS Tagging", "POS ଟ୍ୟାଗିଂ"),
            "what": L("Labeling each word with its part of speech.", "ପ୍ରତ୍ୟେକ ଶବ୍ଦକୁ ଏହାର ପାର୍ଟ ଅଫ ସ୍ପିଚ ସହ ଲେବଲ କରିବା।"),
            "why": L("Helps understand grammatical structure.", "ବ୍ୟାକରଣିକ ଗଠନ ବୁଝିବାରେ ସାହାଯ୍ୟ କରେ।"),
            "how": L("Use lexicons, rules, or trained models.", "ଲେକ୍ସିକନ, ନିୟମ, କିମ୍ବା ପ୍ରଶିକ୍ଷିତ ମଡେଲ ବ୍ୟବହାର କରନ୍ତୁ।"),
            "example": "ମୁଁ (PRON) ଓଡ଼ିଆ (NOUN) ଶିଖୁଛି (VERB)"
        },
        {
            "title": L("Named Entity Recognition", "ନାମିତ ସତ୍ତା ଚିହ୍ନଟ"),
            "what": L("Finding names of people, places, organizations.", "ବ୍ୟକ୍ତି, ସ୍ଥାନ, ସଂସ୍ଥାର ନାମ ଖୋଜିବା।"),
            "why": L("Useful for search, recommendations, and information extraction.", "ସନ୍ଧାନ, ସୁପାରିଶ, ଏବଂ ସୂଚନା ନିଷ୍କାସନ ପାଇଁ ଉପଯୋଗୀ।"),
            "how": L("Rule-based, statistical, or neural models.", "ନିୟମ-ଆଧାରିତ, ସାଂଖ୍ୟିକ, କିମ୍ବା ସ୍ନାୟୁ ମଡେଲ।"),
            "example": "ରାମ → PERSON, ଭୁବନେଶ୍ୱର → LOCATION"
        },
        {
            "title": L("Sentiment Analysis", "ସେଣ୍ଟିମେଣ୍ଟ ବିଶ୍ଳେଷଣ"),
            "what": L("Determining if text is positive, negative, or neutral.", "ଟେକ୍ସଟ ସକାରାତ୍ମକ, ନକାରାତ୍ମକ, କିମ୍ବା ନିରପେକ୍ଷ କି ନାହିଁ ନିର୍ଣ୍ଣୟ କରିବା।"),
            "why": L("Helps understand opinions and feedback.", "ମତ ଏବଂ ମତାମତ ବୁଝିବାରେ ସାହାଯ୍ୟ କରେ।"),
            "how": L("Lexicon-based or machine learning models.", "ଲେକ୍ସିକନ-ଆଧାରିତ କିମ୍ବା ମେସିନ ଲର୍ନିଂ ମଡେଲ।"),
            "example": L("'I love this!' → Positive", "'ମୁଁ ଏହାକୁ ଭଲ ପାଏ!' → ସକାରାତ୍ମକ")
        },
        {
            "title": L("N-Grams", "ଏନ-ଗ୍ରାମ"),
            "what": L("Sequences of N consecutive words.", "N କ୍ରମିକ ଶବ୍ଦର କ୍ରମ।"),
            "why": L("Capture local word order and context.", "ସ୍ଥାନୀୟ ଶବ୍ଦ କ୍ରମ ଏବଂ ପ୍ରସଙ୍ଗ ଧରିବା।"),
            "how": L("Slide a window of size N over the text.", "ଟେକ୍ସଟ ଉପରେ N ଆକାରର ଏକ ୱିଣ୍ଡୋ ସ୍ଲାଇଡ କରନ୍ତୁ।"),
            "example": "ମୁଁ ଓଡ଼ିଆ (bigram), ଓଡ଼ିଆ ଶିଖୁଛି (bigram)"
        },
        {
            "title": L("Language Models", "ଭାଷା ମଡେଲ"),
            "what": L("Models that predict the next word in a sequence.", "ଏକ କ୍ରମରେ ପରବର୍ତ୍ତୀ ଶବ୍ଦ ଭବିଷ୍ୟବାଣୀ କରୁଥିବା ମଡେଲ।"),
            "why": L("Power autocomplete, translation, and text generation.", "ଅଟୋକମ୍ପ୍ଲିଟ, ଅନୁବାଦ, ଏବଂ ଟେକ୍ସଟ ଉତ୍ପାଦନକୁ ଶକ୍ତି ଦିଏ।"),
            "how": L("N-gram models or neural networks (RNN, Transformer).", "ଏନ-ଗ୍ରାମ ମଡେଲ କିମ୍ବା ସ୍ନାୟୁ ନେଟୱାର୍କ (RNN, ଟ୍ରାନ୍ସଫର୍ମର)।"),
            "example": L("'I am going to ___' → 'school', 'market', 'sleep'", "'ମୁଁ ଯାଉଛି ___' → 'ସ୍କୁଲ', 'ବଜାର', 'ଘର'")
        },
        {
            "title": L("Parsing", "ପାର୍ସିଂ"),
            "what": L("Analyzing grammatical structure of sentences.", "ବାକ୍ୟର ବ୍ୟାକରଣିକ ଗଠନ ବିଶ୍ଳେଷଣ କରିବା।"),
            "why": L("Helps understand relationships between words.", "ଶବ୍ଦ ମଧ୍ୟରେ ସମ୍ପର୍କ ବୁଝିବାରେ ସାହାଯ୍ୟ କରେ।"),
            "how": L("Use grammar rules to build a parse tree.", "ଏକ ପାର୍ସ ଟ୍ରି ନିର୍ମାଣ କରିବା ପାଇଁ ବ୍ୟାକରଣ ନିୟମ ବ୍ୟବହାର କରନ୍ତୁ।"),
            "example": L("S → NP VP; NP → DET N; VP → V NP", "S → NP VP; NP → DET N; VP → V NP")
        },
        {
            "title": L("Word Vectors & Semantics", "ଶବ୍ଦ ଭେକ୍ଟର ଏବଂ ଅର୍ଥବିଜ୍ଞାନ"),
            "what": L("Representing words as numerical vectors.", "ଶବ୍ଦକୁ ସାଂଖ୍ୟିକ ଭେକ୍ଟର ଭାବରେ ପ୍ରତିନିଧିତ୍ୱ କରିବା।"),
            "why": L("Computers can do math on vectors to find similarity.", "କମ୍ପ୍ୟୁଟର ସମାନତା ଖୋଜିବା ପାଇଁ ଭେକ୍ଟର ଉପରେ ଗଣିତ କରିପାରେ।"),
            "how": L("Word2Vec, GloVe, or contextual embeddings.", "Word2Vec, GloVe, କିମ୍ବା ପ୍ରସଙ୍ଗିକ ଏମ୍ବେଡିଂ।"),
            "example": L("king - man + woman ≈ queen", "king - man + woman ≈ queen")
        },
    ]

    for topic in topics:
        with st.expander(f"📖 {topic['title']}"):
            c1, c2 = st.columns([3, 2])
            with c1:
                st.markdown(f"**📖 {L('What is it?', 'ଏହା କଣ?')}**")
                st.write(topic['what'])
                st.markdown(f"**💡 {L('Why do we use it?', 'ଆମେ ଏହା କାହିଁକି ବ୍ୟବହାର କରୁ?')}**")
                st.write(topic['why'])
            with c2:
                st.markdown(f"**🔬 {L('How does it work?', 'ଏହା କିପରି କାମ କରେ?')}**")
                st.write(topic['how'])
                st.markdown(f"**🧪 {L('Example', 'ଉଦାହରଣ')}**")
                st.code(topic['example'], language=None)

# =============================================================================
# PAGE: TEXT PREPROCESSING
# =============================================================================
elif "Preprocessing" in selected or "ପ୍ରିପ୍ରୋସେସିଂ" in selected:
    st.title(f"🧹 {L('Text Preprocessing', 'ଟେକ୍ସଟ ପ୍ରିପ୍ରୋସେସିଂ')}")
    st.markdown(L("See how raw text is cleaned and prepared step by step.", "କଞ୍ଚା ଟେକ୍ସଟ କିପରି ପରିଷ୍କାର ଏବଂ ପ୍ରସ୍ତୁତ ହୁଏ ପର୍ଯ୍ୟାୟକ୍ରମେ ଦେଖନ୍ତୁ।"))

    default_text = "ମୁଁ ଓଡ଼ିଆ ଭାଷାକୁ ଭଲ ପାଏ। ଭୁବନେଶ୍ୱର ଓଡ଼ିଶାର ରାଜଧାନୀ।"
    if st.session_state.lang == 'en':
        default_text = "I love the Odia language. Bhubaneswar is the capital of Odisha."

    text = st.text_area(L("Enter your text:", "ଆପଣଙ୍କ ଟେକ୍ସଟ ଲେଖନ୍ତୁ:"), value=default_text, height=100)

    if not text.strip():
        st.warning(L("Please enter some text.", "ଦୟାକରି କିଛି ଟେକ୍ସଟ ଲେଖନ୍ତୁ।"))
    else:
        st.markdown("---")
        st.markdown(f"### 🔄 {L('Preprocessing Pipeline', 'ପ୍ରିପ୍ରୋସେସିଂ ପାଇପଲାଇନ')}")

        # Step by step
        steps = []

        # 1. Original
        steps.append((L("Original Text", "ମୂଳ ଟେକ୍ସଟ"), text, ""))

        # 2. Lowercase
        lower = text.lower()
        steps.append((L("Lowercase", "ଲୋଅରକେସ"), lower, L("Makes all letters small so 'The' and 'the' are treated the same.", "ସମସ୍ତ ଅକ୍ଷର ଛୋଟ କରେ ଯାହା 'The' ଏବଂ 'the' ସମାନ ଭାବରେ ବ୍ୟବହୃତ ହୁଏ।")))

        # 3. Sentence split
        sents = simple_sentence_tokenize(text)
        steps.append((L("Sentence Splitting", "ବାକ୍ୟ ବିଭାଜନ"), " | ".join(sents), L("Breaks a paragraph into individual sentences.", "ଏକ ପାରାଗ୍ରାଫକୁ ବ୍ୟକ୍ତିଗତ ବାକ୍ୟରେ ବିଭକ୍ତ କରେ।")))

        # 4. Word tokenization
        words = simple_word_tokenize(lower)
        steps.append((L("Word Tokenization", "ଶବ୍ଦ ଟୋକେନାଇଜେସନ"), " | ".join(words), L("Splits sentences into individual words.", "ବାକ୍ୟକୁ ବ୍ୟକ୍ତିଗତ ଶବ୍ଦରେ ବିଭକ୍ତ କରେ।")))

        # 5. Stopword removal
        words_no_stop = remove_stopwords(words, st.session_state.lang)
        steps.append((L("Stopword Removal", "ଷ୍ଟପୱାର୍ଡ ଅପସାରଣ"), " | ".join(words_no_stop), L("Removes common words like 'the', 'is', 'and' that carry little meaning.", "'the', 'is', 'and' ଭଳି ସାଧାରଣ ଶବ୍ଦ ହଟାଏ ଯାହା ଅଳ୍ପ ଅର୍ଥ ବହନ କରେ।")))

        # 6. Stemming
        stemmed = [simple_stem(w) for w in words_no_stop]
        steps.append((L("Stemming", "ଷ୍ଟେମିଂ"), " | ".join(stemmed), L("Cuts words to their root form (running → run).", "ଶବ୍ଦକୁ ମୂଳ ରୂପକୁ କାଟେ (running → run)।")))

        # 7. Lemmatization
        lemmatized = [simple_lemmatize(w) for w in words_no_stop]
        steps.append((L("Lemmatization", "ଲେମାଟାଇଜେସନ"), " | ".join(lemmatized), L("Finds the dictionary form of a word (better → good).", "ଏକ ଶବ୍ଦର ଅଭିଧାନ ରୂପ ଖୋଜେ (better → good)।")))

        for i, (title, result, explanation) in enumerate(steps):
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown(f"**<span class='step-badge'>{i+1}</span> {title}**", unsafe_allow_html=True)
            with col2:
                st.code(result, language=None)
                if explanation:
                    st.caption(f"💡 {explanation}")

        st.markdown("---")
        st.markdown(f"### 📊 {L('What changed?', 'କଣ ପରିବର୍ତ୍ତନ ହେଲା?')}")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric(L("Original words", "ମୂଳ ଶବ୍ଦ"), len(words))
        with c2:
            st.metric(L("After stopword removal", "ଷ୍ଟପୱାର୍ଡ ଅପସାରଣ ପରେ"), len(words_no_stop))
        with c3:
            st.metric(L("Reduction", "ହ୍ରାସ"), f"{(1 - len(words_no_stop)/max(len(words),1))*100:.0f}%")

        if st.session_state.lang == 'or':
            st.info(L("⚠️ Educational demonstration: Odia stemming and lemmatization are simplified here. Real Odia NLP requires language-specific tools.",
                      "⚠️ ଶିକ୍ଷାମୂଳକ ପ୍ରଦର୍ଶନ: ଓଡ଼ିଆ ଷ୍ଟେମିଂ ଏବଂ ଲେମାଟାଇଜେସନ ଏଠାରେ ସରଳୀକୃତ। ପ୍ରକୃତ ଓଡ଼ିଆ NLP ପାଇଁ ଭାଷା-ନିର୍ଦ୍ଦିଷ୍ଟ ଉପକରଣ ଆବଶ୍ୟକ।"))

# =============================================================================
# PAGE: TOKENIZATION
# =============================================================================
elif "Tokenization" in selected or "ଟୋକେନାଇଜେସନ" in selected:
    st.title(f"🔤 {L('Tokenization', 'ଟୋକେନାଇଜେସନ')}")
    st.markdown(L("Break text into smaller pieces called tokens.", "ଟେକ୍ସଟକୁ ଟୋକେନ ନାମକ ଛୋଟ ଖଣ୍ଡରେ ବିଭକ୍ତ କରନ୍ତୁ।"))

    default = "ମୁଁ ଓଡ଼ିଆ ଶିଖୁଛି।"
    if st.session_state.lang == 'en':
        default = "I am learning Odia."
    text = st.text_area(L("Enter a sentence:", "ଏକ ବାକ୍ୟ ଲେଖନ୍ତୁ:"), value=default, height=80)

    if not text.strip():
        st.warning(L("Please enter some text.", "ଦୟାକରି କିଛି ଟେକ୍ସଟ ଲେଖନ୍ତୁ।"))
    else:
        tab1, tab2 = st.tabs([L("Word Tokenization", "ଶବ୍ଦ ଟୋକେନାଇଜେସନ"), L("Sentence Tokenization", "ବାକ୍ୟ ଟୋକେନାଇଜେସନ")])

        with tab1:
            st.markdown(f"#### {L('Sentence', 'ବାକ୍ୟ')}")
            st.markdown(f"<div class='card' style='font-size:1.2rem;'>{text}</div>", unsafe_allow_html=True)
            st.markdown("<div class='arrow-down'>↓</div>", unsafe_allow_html=True)
            st.markdown(f"#### {L('Tokens', 'ଟୋକେନ')}")
            tokens = simple_word_tokenize(text)
            html = ""
            for i, tok in enumerate(tokens):
                cls = "token-card token-card-odia" if st.session_state.lang == 'or' else "token-card"
                html += f"<span class='{cls}'>{tok}</span>"
            st.markdown(html, unsafe_allow_html=True)
            st.metric(L("Token count", "ଟୋକେନ ସଂଖ୍ୟା"), len(tokens))

        with tab2:
            st.markdown(f"#### {L('Paragraph', 'ପାରାଗ୍ରାଫ')}")
            st.markdown(f"<div class='card' style='font-size:1.2rem;'>{text}</div>", unsafe_allow_html=True)
            st.markdown("<div class='arrow-down'>↓</div>", unsafe_allow_html=True)
            st.markdown(f"#### {L('Sentences', 'ବାକ୍ୟ')}")
            sents = simple_sentence_tokenize(text)
            for i, s in enumerate(sents):
                st.markdown(f"<div class='card'><b>{L('Sentence', 'ବାକ୍ୟ')} {i+1}:</b> {s}</div>", unsafe_allow_html=True)
            st.metric(L("Sentence count", "ବାକ୍ୟ ସଂଖ୍ୟା"), len(sents))

        st.markdown("---")
        st.markdown(f"""
        <div class="explain-box">
            <b>💡 {L("Why tokenize?", "ଟୋକେନାଇଜ କାହିଁକି?")}</b><br>
            {L("Computers cannot understand raw sentences. By breaking text into tokens, we give the computer manageable units to analyze.",
               "କମ୍ପ୍ୟୁଟର କଞ୍ଚା ବାକ୍ୟ ବୁଝିପାରେ ନାହିଁ। ଟେକ୍ସଟକୁ ଟୋକେନରେ ବିଭକ୍ତ କରି ଆମେ କମ୍ପ୍ୟୁଟରକୁ ବିଶ୍ଳେଷଣ ପାଇଁ ପରିଚାଳନାଯୋଗ୍ୟ ଏକକ ଦେଉ।")}
        </div>
        """, unsafe_allow_html=True)

# =============================================================================
# PAGE: POS TAGGING
# =============================================================================
elif "POS" in selected or "ଟ୍ୟାଗିଂ" in selected:
    st.title(f"🏷️ {L('POS Tagging', 'POS ଟ୍ୟାଗିଂ')}")
    st.markdown(L("Label each word with its part of speech.", "ପ୍ରତ୍ୟେକ ଶବ୍ଦକୁ ଏହାର ପାର୍ଟ ଅଫ ସ୍ପିଚ ସହ ଲେବଲ କରନ୍ତୁ।"))

    st.markdown(f"""
    <div class="card">
        <b>{L("Common POS tags:", "ସାଧାରଣ POS ଟ୍ୟାଗ:")}</b><br>
        <span class="pos-noun">NOUN</span> {L("— person, place, thing", "— ବ୍ୟକ୍ତି, ସ୍ଥାନ, ଜିନିଷ")} &nbsp;
        <span class="pos-verb">VERB</span> {L("— action word", "— କ୍ରିୟା")} &nbsp;
        <span class="pos-pron">PRON</span> {L("— replaces a noun", "— ବିଶେଷ୍ୟ ବଦଳାଏ")} &nbsp;
        <span class="pos-adj">ADJ</span> {L("— describes a noun", "— ବିଶେଷ୍ୟକୁ ବର୍ଣ୍ଣନା କରେ")} &nbsp;
        <span class="pos-adv">ADV</span> {L("— modifies a verb", "— କ୍ରିୟାକୁ ପରିବର୍ତ୍ତନ କରେ")}
    </div>
    """, unsafe_allow_html=True)

    default = "ରାମ ଭୁବନେଶ୍ୱରକୁ ଗଲେ।"
    if st.session_state.lang == 'en':
        default = "Ram went to Bhubaneswar."
    text = st.text_area(L("Enter a sentence:", "ଏକ ବାକ୍ୟ ଲେଖନ୍ତୁ:"), value=default, height=80)

    if not text.strip():
        st.warning(L("Please enter some text.", "ଦୟାକରି କିଛି ଟେକ୍ସଟ ଲେଖନ୍ତୁ।"))
    else:
        tokens = simple_word_tokenize(text)
        tagged = pos_tag_demo(tokens, st.session_state.lang)

        st.markdown(f"### 🔍 {L('Analysis', 'ବିଶ୍ଳେଷଣ')}")

        # Visual highlight
        html = ""
        color_map = {
            'NOUN': 'pos-noun', 'VERB': 'pos-verb', 'PRON': 'pos-pron',
            'ADJ': 'pos-adj', 'ADV': 'pos-adv'
        }
        for tok, tag, _ in tagged:
            cls = color_map.get(tag, 'pos-other')
            html += f"<span class='{cls}' style='margin:4px; font-size:1.1rem; display:inline-block; padding:6px 10px;'>{tok}<br><small style='font-size:0.7rem; color:#6b7280;'>{tag}</small></span>"
        st.markdown(f"<div class='card'>{html}</div>", unsafe_allow_html=True)

        # Table
        df = pd.DataFrame([
            {"Word": t, "POS": tag, "Meaning": m}
            for t, tag, m in tagged
        ])
        st.dataframe(df, use_container_width=True, hide_index=True)

        # POS distribution chart
        pos_counts = Counter([t[1] for t in tagged])
        if pos_counts:
            fig = px.bar(
                x=list(pos_counts.keys()),
                y=list(pos_counts.values()),
                labels={'x': L('POS Tag', 'POS ଟ୍ୟାଗ'), 'y': L('Count', 'ଗଣନା')},
                color=list(pos_counts.keys()),
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            fig.update_layout(showlegend=False, height=300)
            st.plotly_chart(fig, use_container_width=True)

        if st.session_state.lang == 'or':
            st.info(L("⚠️ Educational demonstration: This uses a small built-in Odia vocabulary and simple guessing rules. A real POS tagger would be trained on a large annotated corpus.",
                      "⚠️ ଶିକ୍ଷାମୂଳକ ପ୍ରଦର୍ଶନ: ଏହା ଏକ ଛୋଟ ଅନ୍ତର୍ନିହିତ ଓଡ଼ିଆ ଶବ୍ଦକୋଷ ଏବଂ ସରଳ ଅନୁମାନ ନିୟମ ବ୍ୟବହାର କରେ। ଏକ ପ୍ରକୃତ POS ଟ୍ୟାଗର ଏକ ବଡ଼ ଆନୋଟେଟେଡ କର୍ପସ ଉପରେ ପ୍ରଶିକ୍ଷିତ ହେବ।"))

# =============================================================================
# PAGE: NAMED ENTITY RECOGNITION
# =============================================================================
elif "Named Entity" in selected or "ନାମିତ ସତ୍ତା" in selected:
    st.title(f"📍 {L('Named Entity Recognition', 'ନାମିତ ସତ୍ତା ଚିହ୍ନଟ')}")
    st.markdown(L("Find and classify names of people, places, and organizations.", "ବ୍ୟକ୍ତି, ସ୍ଥାନ, ଏବଂ ସଂସ୍ଥାର ନାମ ଖୋଜନ୍ତୁ ଏବଂ ଶ୍ରେଣୀବଦ୍ଧ କରନ୍ତୁ।"))

    default = "ରାମ ଭୁବନେଶ୍ୱରକୁ ଗଲେ।"
    if st.session_state.lang == 'en':
        default = "Ram went to Bhubaneswar."
    text = st.text_area(L("Enter a sentence:", "ଏକ ବାକ୍ୟ ଲେଖନ୍ତୁ:"), value=default, height=80)

    if not text.strip():
        st.warning(L("Please enter some text.", "ଦୟାକରି କିଛି ଟେକ୍ସଟ ଲେଖନ୍ତୁ।"))
    else:
        tokens = simple_word_tokenize(text)
        entities = ner_demo(tokens, st.session_state.lang)

        st.markdown(f"### 🖍️ {L('Highlighted Entities', 'ହାଇଲାଇଟ ହୋଇଥିବା ସତ୍ତା')}")
        html = ""
        for tok in tokens:
            ent = None
            for e_tok, e_type in entities:
                if e_tok == tok:
                    ent = e_type
                    break
            if ent == 'PERSON':
                html += f"<span class='highlight-person' style='font-size:1.2rem;'>{tok}</span> "
            elif ent == 'LOCATION':
                html += f"<span class='highlight-location' style='font-size:1.2rem;'>{tok}</span> "
            elif ent == 'ORG':
                html += f"<span class='highlight-org' style='font-size:1.2rem;'>{tok}</span> "
            elif ent == 'EVENT':
                html += f"<span class='highlight-date' style='font-size:1.2rem;'>{tok}</span> "
            else:
                html += f"<span style='font-size:1.2rem;'>{tok}</span> "
        st.markdown(f"<div class='card'>{html}</div>", unsafe_allow_html=True)

        if entities:
            st.markdown(f"### 📋 {L('Entity Table', 'ସତ୍ତା ଟେବୁଲ')}")
            df = pd.DataFrame([
                {"Text": t, "Entity Type": etype}
                for t, etype in entities
            ])
            st.dataframe(df, use_container_width=True, hide_index=True)

            # Legend
            st.markdown(f"""
            <div style="margin-top:1rem;">
                <span class='highlight-person'>&nbsp;&nbsp;</span> PERSON &nbsp;
                <span class='highlight-location'>&nbsp;&nbsp;</span> LOCATION &nbsp;
                <span class='highlight-org'>&nbsp;&nbsp;</span> ORGANIZATION &nbsp;
                <span class='highlight-date'>&nbsp;&nbsp;</span> EVENT/DATE
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info(L("No entities found in the demo vocabulary.", "ଡେମୋ ଶବ୍ଦକୋଷରେ କୌଣସି ସତ୍ତା ମିଳିଲା ନାହିଁ।"))

        if st.session_state.lang == 'or':
            st.info(L("⚠️ Educational demonstration: This uses a small built-in Odia entity list. A real NER system is trained on large annotated corpora.",
                      "⚠️ ଶିକ୍ଷାମୂଳକ ପ୍ରଦର୍ଶନ: ଏହା ଏକ ଛୋଟ ଅନ୍ତର୍ନିହିତ ଓଡ଼ିଆ ସତ୍ତା ତାଲିକା ବ୍ୟବହାର କରେ। ଏକ ପ୍ରକୃତ NER ସିଷ୍ଟମ ବଡ଼ ଆନୋଟେଟେଡ କର୍ପସ ଉପରେ ପ୍ରଶିକ୍ଷିତ।"))

# =============================================================================
# PAGE: SENTIMENT ANALYSIS
# =============================================================================
elif "Sentiment" in selected or "ସେଣ୍ଟିମେଣ୍ଟ" in selected:
    st.title(f"😊 {L('Sentiment Analysis', 'ସେଣ୍ଟିମେଣ୍ଟ ବିଶ୍ଳେଷଣ')}")
    st.markdown(L("Determine if text is positive, negative, or neutral.", "ଟେକ୍ସଟ ସକାରାତ୍ମକ, ନକାରାତ୍ମକ, କିମ୍ବା ନିରପେକ୍ଷ କି ନାହିଁ ନିର୍ଣ୍ଣୟ କରନ୍ତୁ।"))

    st.markdown(f"""
    <div class="card">
        <b>{L("Sentiment Categories:", "ସେଣ୍ଟିମେଣ୍ଟ ବର୍ଗ:")}</b><br>
        😊 <b>Positive</b> — {L("happy, good, love, great", "ଖୁସି, ଭଲ, ପ୍ରେମ, ମହାନ")}<br>
        😐 <b>Neutral</b> — {L("okay, fine, normal", "ଠିକ, ଭଲ, ସାଧାରଣ")}<br>
        😞 <b>Negative</b> — {L("sad, bad, hate, terrible", "ଦୁଃଖ, ଖରାପ, ଘୃଣା, ଭୟଙ୍କର")}
    </div>
    """, unsafe_allow_html=True)

    default = "ମୁଁ ଓଡ଼ିଆ ଭାଷାକୁ ଭଲ ପାଏ।"
    if st.session_state.lang == 'en':
        default = "I love the Odia language!"
    text = st.text_area(L("Enter text:", "ଟେକ୍ସଟ ଲେଖନ୍ତୁ:"), value=default, height=80)

    if not text.strip():
        st.warning(L("Please enter some text.", "ଦୟାକରି କିଛି ଟେକ୍ସଟ ଲେଖନ୍ତୁ।"))
    else:
        # Simple lexicon-based sentiment for demo
        positive_words_en = {'love', 'great', 'good', 'happy', 'excellent', 'amazing', 'wonderful', 'best', 'joy', 'beautiful'}
        negative_words_en = {'hate', 'bad', 'sad', 'terrible', 'awful', 'worst', 'horrible', 'angry', 'disappointed'}
        positive_words_or = {'ଭଲ', 'ପ୍ରେମ', 'ଖୁସି', 'ମହାନ', 'ସୁନ୍ଦର', 'ଆନନ୍ଦ', 'ପ୍ରସନ୍ନ'}
        negative_words_or = {'ଖରାପ', 'ଦୁଃଖ', 'ଘୃଣା', 'ଭୟଙ୍କର', 'ରାଗ', 'ନିରାଶ'}

        tokens = simple_word_tokenize(text.lower())
        if st.session_state.lang == 'en':
            pos = sum(1 for t in tokens if t in positive_words_en)
            neg = sum(1 for t in tokens if t in negative_words_en)
        else:
            pos = sum(1 for t in tokens if t in positive_words_or)
            neg = sum(1 for t in tokens if t in negative_words_or)

        if pos > neg:
            sentiment = "Positive"
            emoji = "😊"
            color = "#10b981"
        elif neg > pos:
            sentiment = "Negative"
            emoji = "😞"
            color = "#ef4444"
        else:
            sentiment = "Neutral"
            emoji = "😐"
            color = "#6b7280"

        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown(f"""
            <div class="card" style="text-align:center; border:2px solid {color};">
                <div style="font-size:4rem;">{emoji}</div>
                <div style="font-size:1.5rem; font-weight:700; color:{color};">{sentiment}</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            # Bar chart
            fig = go.Figure(data=[
                go.Bar(name='Positive', x=['Score'], y=[pos], marker_color='#10b981'),
                go.Bar(name='Negative', x=['Score'], y=[neg], marker_color='#ef4444'),
            ])
            fig.update_layout(
                barmode='group',
                height=250,
                margin=dict(l=20, r=20, t=20, b=20),
                yaxis_title=L("Count", "ଗଣନା"),
                showlegend=True
            )
            st.plotly_chart(fig, use_container_width=True)

        st.markdown(f"**{L('Words matched:', 'ମେଳ ଖାଉଥିବା ଶବ୍ଦ:')}** ✅ {pos} positive, ❌ {neg} negative")

        if st.session_state.lang == 'or':
            st.info(L("⚠️ Educational demonstration: This uses a small Odia sentiment lexicon. A real sentiment analyzer would be trained on labeled Odia reviews.",
                      "⚠️ ଶିକ୍ଷାମୂଳକ ପ୍ରଦର୍ଶନ: ଏହା ଏକ ଛୋଟ ଓଡ଼ିଆ ସେଣ୍ଟିମେଣ୍ଟ ଲେକ୍ସିକନ ବ୍ୟବହାର କରେ। ଏକ ପ୍ରକୃତ ସେଣ୍ଟିମେଣ୍ଟ ଆନାଲାଇଜର ଲେବଲଯୁକ୍ତ ଓଡ଼ିଆ ସମୀକ୍ଷା ଉପରେ ପ୍ରଶିକ୍ଷିତ ହେବ।"))

# =============================================================================
# PAGE: N-GRAMS
# =============================================================================
elif "N-Grams" in selected or "ଏନ-ଗ୍ରାମ" in selected:
    st.title(f"🔢 {L('N-Grams', 'ଏନ-ଗ୍ରାମ')}")
    st.markdown(L("Explore sequences of N consecutive words.", "N କ୍ରମିକ ଶବ୍ଦର କ୍ରମ ଅନ୍ୱେଷଣ କରନ୍ତୁ।"))

    default = "ମୁଁ ଓଡ଼ିଆ ଶିଖୁଛି"
    if st.session_state.lang == 'en':
        default = "I am learning Odia language"
    text = st.text_area(L("Enter text:", "ଟେକ୍ସଟ ଲେଖନ୍ତୁ:"), value=default, height=80)

    n = st.slider(L("Select N:", "N ଚୟନ କରନ୍ତୁ:"), 1, 3, 2)

    if not text.strip():
        st.warning(L("Please enter some text.", "ଦୟାକରି କିଛି ଟେକ୍ସଟ ଲେଖନ୍ତୁ।"))
    else:
        tokens = simple_word_tokenize(text)
        tokens = [t for t in tokens if t not in ('।', '.', ',')]

        ngrams = generate_ngrams(tokens, n)
        freq = ngram_frequencies(ngrams)

        st.markdown(f"### {L('Tokens', 'ଟୋକେନ')}")
        st.markdown(" ".join([f"<span class='token-card'>{t}</span>" for t in tokens]), unsafe_allow_html=True)

        st.markdown(f"### {L(f'{n}-grams', f'{n}-ଗ୍ରାମ')}")
        if ngrams:
            html = ""
            for g in ngrams:
                label = " | ".join(g)
                html += f"<span class='token-card token-card-odia'>{label}</span>"
            st.markdown(html, unsafe_allow_html=True)

            st.markdown(f"### 📊 {L('Frequency & Probability', 'ଆବୃତ୍ତି ଏବଂ ସମ୍ଭାବ୍ୟତା')}")
            probs = ngram_probabilities(ngrams, n)
            data = []
            for g, c in freq.items():
                label = " | ".join(g)
                p = probs.get(g, 0)
                data.append({"N-gram": label, "Frequency": c, "Probability": round(p, 4)})
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True, hide_index=True)

            # Chart
            fig = px.bar(
                df, x="N-gram", y="Frequency",
                color="Frequency",
                color_continuous_scale="Viridis",
                title=L(f"{n}-gram Frequencies", f"{n}-ଗ୍ରାମ ଆବୃତ୍ତି")
            )
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info(L("Not enough tokens to form n-grams. Try a longer sentence.", "ଏନ-ଗ୍ରାମ ଗଠନ ପାଇଁ ପର୍ଯ୍ୟାପ୍ତ ଟୋକେନ ନାହିଁ। ଏକ ଲମ୍ବା ବାକ୍ୟ ଚେଷ୍ଟା କରନ୍ତୁ।"))

# =============================================================================
# PAGE: LANGUAGE MODELS
# =============================================================================
elif "Language Models" in selected or "ଭାଷା ମଡେଲ" in selected:
    st.title(f"🧠 {L('Language Models', 'ଭାଷା ମଡେଲ')}")
    st.markdown(L("See how a model predicts the next word.", "ଏକ ମଡେଲ କିପରି ପରବର୍ତ୍ତୀ ଶବ୍ଦ ଭବିଷ୍ୟବାଣୀ କରେ ଦେଖନ୍ତୁ।"))

    st.markdown(f"""
    <div class="card">
        <b>{L("How it works:", "ଏହା କିପରି କାମ କରେ:")}</b><br>
        1. {L("The model looks at the previous word(s) — this is the", "ମଡେଲ ପୂର୍ବ ଶବ୍ଦ(ଗୁଡ଼ିକ) ଦେଖେ — ଏହା ହେଉଛି")} <b>context</b>.<br>
        2. {L("It calculates the probability of each possible next word.", "ଏହା ପ୍ରତ୍ୟେକ ସମ୍ଭାବ୍ୟ ପରବର୍ତ୍ତୀ ଶବ୍ଦର ସମ୍ଭାବ୍ୟତା ଗଣନା କରେ।")}<br>
        3. {L("The word with the highest probability is the prediction.", "ସର୍ବୋଚ୍ଚ ସମ୍ଭାବ୍ୟତା ଥିବା ଶବ୍ଦ ହେଉଛି ଭବିଷ୍ୟବାଣୀ।")}
    </div>
    """, unsafe_allow_html=True)

    # Build a simple bigram model from the tiny corpus
    @st.cache_data
    def build_bigram_model(corpus):
        bigrams = []
        for sent in corpus:
            tokens = simple_word_tokenize(sent.lower())
            tokens = [t for t in tokens if t not in ('।', '.', ',')]
            bigrams.extend(generate_ngrams(tokens, 2))
        freq = Counter(bigrams)
        # P(w2 | w1)
        model = {}
        for (w1, w2), c in freq.items():
            if w1 not in model:
                model[w1] = {}
            model[w1][w2] = c
        # Normalize
        for w1 in model:
            total = sum(model[w1].values())
            for w2 in model[w1]:
                model[w1][w2] /= total
        return model, freq

    model, freq = build_bigram_model(tuple(TINY_CORPUS))

    st.markdown(f"### 🧪 {L('Try Next-Word Prediction', 'ପରବର୍ତ୍ତୀ-ଶବ୍ଦ ଭବିଷ୍ୟବାଣୀ ଚେଷ୍ଟା କରନ୍ତୁ')}")
    context = st.text_input(L("Enter a word (context):", "ଏକ ଶବ୍ଦ ଲେଖନ୍ତୁ (ପ୍ରସଙ୍ଗ):"), value="the")

    if context.strip():
        ctx = context.strip().lower()
        if ctx in model:
            predictions = sorted(model[ctx].items(), key=lambda x: -x[1])
            st.markdown(f"**{L('Predictions for', 'ପାଇଁ ଭବିଷ୍ୟବାଣୀ')} \"{ctx} ___\":**")
            for w, p in predictions[:5]:
                st.markdown(f"- **{w}** — {L('Probability', 'ସମ୍ଭାବ୍ୟତା')}: {p:.2%}")

            # Chart
            if predictions:
                words = [w for w, _ in predictions[:8]]
                probs = [p for _, p in predictions[:8]]
                fig = px.bar(
                    x=words, y=probs,
                    labels={'x': L('Predicted Word', 'ଭବିଷ୍ୟବାଣୀ ଶବ୍ଦ'), 'y': L('Probability', 'ସମ୍ଭାବ୍ୟତା')},
                    color=probs,
                    color_continuous_scale="Blues",
                    title=L(f"Next word probabilities after '{ctx}'", f"'{ctx}' ପରେ ପରବର୍ତ୍ତୀ ଶବ୍ଦ ସମ୍ଭାବ୍ୟତା")
                )
                fig.update_layout(height=300, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info(L(f"'{ctx}' not found in the educational corpus. Try: the, i, ମୁଁ, ଓଡ଼ିଆ",
                      f"'{ctx}' ଶିକ୍ଷାମୂଳକ କର୍ପସରେ ମିଳିଲା ନାହିଁ। ଚେଷ୍ଟା କରନ୍ତୁ: the, i, ମୁଁ, ଓଡ଼ିଆ"))

    st.markdown("---")
    st.markdown(f"### 📚 {L('Educational Corpus Used', 'ବ୍ୟବହୃତ ଶିକ୍ଷାମୂଳକ କର୍ପସ')}")
    for s in TINY_CORPUS[:6]:
        st.markdown(f"- {s}")
    st.caption(L("This is a tiny corpus for demonstration. Real language models use billions of words.",
                 "ଏହା ପ୍ରଦର୍ଶନ ପାଇଁ ଏକ ଛୋଟ କର୍ପସ। ପ୍ରକୃତ ଭାଷା ମଡେଲ ଅରବ ଅରବ ଶବ୍ଦ ବ୍ୟବହାର କରେ।"))

# =============================================================================
# PAGE: PARSING
# =============================================================================
elif "Parsing" in selected or "ପାର୍ସିଂ" in selected:
    st.title(f"🌳 {L('Parsing', 'ପାର୍ସିଂ')}")
    st.markdown(L("Visualize the grammatical structure of a sentence.", "ଏକ ବାକ୍ୟର ବ୍ୟାକରଣିକ ଗଠନ ଦୃଶ୍ୟମାନ କରନ୍ତୁ।"))

    st.markdown(f"""
    <div class="card">
        <b>{L("Simple Grammar Rules:", "ସରଳ ବ୍ୟାକରଣ ନିୟମ:")}</b><br>
        <code>S → NP VP</code><br>
        <code>NP → DET N</code><br>
        <code>VP → V NP</code>
    </div>
    """, unsafe_allow_html=True)

    default = "The boy saw the girl"
    if st.session_state.lang == 'or':
        default = "ପିଲାଟି ଝିଅକୁ ଦେଖିଲା"

    text = st.text_area(L("Enter a simple sentence:", "ଏକ ସରଳ ବାକ୍ୟ ଲେଖନ୍ତୁ:"), value=default, height=80)

    if not text.strip():
        st.warning(L("Please enter some text.", "ଦୟାକରି କିଛି ଟେକ୍ସଟ ଲେଖନ୍ତୁ।"))
    else:
        st.markdown(f"### 🌲 {L('Parse Tree', 'ପାର୍ସ ଟ୍ରି')}")
        fig = draw_parse_tree(text)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown(f"### 📋 {L('Parsing Steps', 'ପାର୍ସିଂ ପର୍ଯ୍ୟାୟ')}")
        words = simple_word_tokenize(text)
        words = [w for w in words if w not in ('।', '.', ',')]
        st.markdown(f"""
        <div class="card">
            <b>1. {L('Sentence', 'ବାକ୍ୟ')}:</b> {text}<br>
            <b>2. {L('Words', 'ଶବ୍ଦ')}:</b> {" | ".join(words)}<br>
            <b>3. {L('Constituents', 'ଉପାଦାନ')}:</b> NP (ବିଶେଷ୍ୟ ପଦବାକ୍ୟ) + VP (କ୍ରିୟା ପଦବାକ୍ୟ)<br>
            <b>4. {L('Parse Tree', 'ପାର୍ସ ଟ୍ରି')}:</b> {L('Drawn above', 'ଉପରେ ଅଙ୍କିତ')}
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"### 🔄 {L('Parsing Strategies', 'ପାର୍ସିଂ ରଣନୀତି')}")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="card">
                <b>⬇️ {L('Top-Down Parsing', 'ଟପ-ଡାଉନ ପାର୍ସିଂ')}</b><br>
                {L("Start from S and expand rules until words are reached.", "S ରୁ ଆରମ୍ଭ କରି ଶବ୍ଦ ନ ପହଞ୍ଚିବା ପର୍ଯ୍ୟନ୍ତ ନିୟମ ବିସ୍ତାର କରନ୍ତୁ।")}<br>
                <small>{L("S → NP VP → DET N VP → ...", "S → NP VP → DET N VP → ...")}</small>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="card">
                <b>⬆️ {L('Bottom-Up Parsing', 'ବଟମ-ଅପ ପାର୍ସିଂ')}</b><br>
                {L("Start from words and combine until S is reached.", "ଶବ୍ଦରୁ ଆରମ୍ଭ କରି S ନ ପହଞ୍ଚିବା ପର୍ଯ୍ୟନ୍ତ ମିଶ୍ରଣ କରନ୍ତୁ।")}<br>
                <small>{L("the + boy → NP; saw + NP → VP; NP + VP → S", "the + boy → NP; saw + NP → VP; NP + VP → S")}</small>
            </div>
            """, unsafe_allow_html=True)

# =============================================================================
# PAGE: WORD VECTORS & SEMANTICS
# =============================================================================
elif "Word Vectors" in selected or "ଶବ୍ଦ ଭେକ୍ଟର" in selected:
    st.title(f"📐 {L('Word Vectors & Semantics', 'ଶବ୍ଦ ଭେକ୍ଟର ଏବଂ ଅର୍ଥବିଜ୍ଞାନ')}")
    st.markdown(L("Computers turn words into numbers called vectors.", "କମ୍ପ୍ୟୁଟର ଶବ୍ଦକୁ ଭେକ୍ଟର ନାମକ ସଂଖ୍ୟାରେ ପରିଣତ କରେ।"))

    st.markdown(f"""
    <div class="card">
        <b>{L("Word → Vector → Similarity", "ଶବ୍ଦ → ଭେକ୍ଟର → ସମାନତା")}</b><br>
        {L("Each word is represented as a list of numbers. Words with similar meanings have similar vectors.",
           "ପ୍ରତ୍ୟେକ ଶବ୍ଦ ସଂଖ୍ୟାର ଏକ ତାଲିକା ଭାବରେ ପ୍ରତିନିଧିତ୍ୱ କରାଯାଏ। ସମାନ ଅର୍ଥ ଥିବା ଶବ୍ଦର ସମାନ ଭେକ୍ଟର ଥାଏ।")}
    </div>
    """, unsafe_allow_html=True)

    # Vector table
    st.markdown(f"### 📊 {L('Example Vectors (2D)', 'ଉଦାହରଣ ଭେକ୍ଟର (2D)')}")
    df = pd.DataFrame([
        {"Word": w, "Dim 1": v[0], "Dim 2": v[1]}
        for w, v in WORD_VECTORS.items()
    ])
    st.dataframe(df, use_container_width=True, hide_index=True)

    # 2D scatter
    fig = px.scatter(
        df, x="Dim 1", y="Dim 2", text="Word",
        title=L("Word Vectors in 2D Space", "2D ସ୍ଥାନରେ ଶବ୍ଦ ଭେକ୍ଟର"),
        color="Word"
    )
    fig.update_traces(textposition='top center', marker=dict(size=14))
    fig.update_layout(height=450, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"### 🔍 {L('Compare Two Words', 'ଦୁଇଟି ଶବ୍ଦ ତୁଳନା କରନ୍ତୁ')}")
    col1, col2 = st.columns(2)
    with col1:
        w1 = st.selectbox(L("Word A", "ଶବ୍ଦ A"), list(WORD_VECTORS.keys()), index=0)
    with col2:
        w2 = st.selectbox(L("Word B", "ଶବ୍ଦ B"), list(WORD_VECTORS.keys()), index=1)

    if w1 and w2:
        v1 = WORD_VECTORS[w1]
        v2 = WORD_VECTORS[w2]
        sim = cosine_similarity(v1, v2)
        st.metric(L("Cosine Similarity", "କୋସାଇନ ସମାନତା"), f"{sim:.3f}")
        st.progress(max(0.0, min(1.0, sim)))

        if sim > 0.8:
            st.success(L("These words are very similar!", "ଏହି ଶବ୍ଦଗୁଡ଼ିକ ଅତି ସମାନ!"))
        elif sim > 0.5:
            st.info(L("These words are somewhat similar.", "ଏହି ଶବ୍ଦଗୁଡ଼ିକ କିଛି ମାତ୍ରାରେ ସମାନ।"))
        else:
            st.warning(L("These words are quite different.", "ଏହି ଶବ୍ଦଗୁଡ଼ିକ ଯଥେଷ୍ଟ ଅଲଗା।"))

        st.markdown(f"""
        <div class="explain-box">
            <b>💡 {L("What does this mean?", "ଏହାର ଅର୍ଥ କଣ?")}</b><br>
            {L(f"The cosine similarity between '{w1}' and '{w2}' is {sim:.3f}. A score closer to 1 means the words are more similar in meaning.",
               f"'{w1}' ଏବଂ '{w2}' ମଧ୍ୟରେ କୋସାଇନ ସମାନତା {sim:.3f}। 1 ର ନିକଟତର ସ୍କୋର ଅର୍ଥ ଶବ୍ଦଗୁଡ଼ିକ ଅର୍ଥରେ ଅଧିକ ସମାନ।")}
        </div>
        """, unsafe_allow_html=True)

# =============================================================================
# PAGE: NLP MATHEMATICS
# =============================================================================
elif "Mathematics" in selected or "ଗଣିତ" in selected:
    st.title(f"🧮 {L('NLP Mathematics', 'NLP ଗଣିତ')}")
    st.markdown(L("Interactive math concepts used in NLP.", "NLP ରେ ବ୍ୟବହୃତ ଇଣ୍ଟରାକ୍ଟିଭ ଗଣିତ ଧାରଣା।"))

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        L("Probability", "ସମ୍ଭାବ୍ୟତା"),
        L("Bayes Theorem", "ବେଜ ଥିଓରେମ"),
        L("TF-IDF", "TF-IDF"),
        L("Cosine Similarity", "କୋସାଇନ ସମାନତା"),
        L("Perplexity", "ପର୍ପ୍ଲେକ୍ସିଟି"),
        L("Conditional Prob.", "ସର୍ତ୍ତମୂଳକ ସମ୍ଭାବ୍ୟତା"),
    ])

    with tab1:
        st.markdown(f"### 📖 {L('Probability', 'ସମ୍ଭାବ୍ୟତା')}")
        st.latex(r"P(E) = \frac{\text{Number of favorable outcomes}}{\text{Total number of outcomes}}")
        col1, col2 = st.columns(2)
        with col1:
            fav = st.number_input(L("Favorable outcomes", "ଅନୁକୂଳ ଫଳାଫଳ"), min_value=0, value=3)
        with col2:
            total = st.number_input(L("Total outcomes", "ମୋଟ ଫଳାଫଳ"), min_value=1, value=10)
        if total > 0:
            p = fav / total
            st.metric(L("Probability", "ସମ୍ଭାବ୍ୟତା"), f"{p:.4f}")
            st.progress(min(1.0, p))
            st.info(L(f"P = {fav}/{total} = {p:.4f}", f"P = {fav}/{total} = {p:.4f}"))

    with tab2:
        st.markdown(f"### 📖 {L('Bayes Theorem', 'ବେଜ ଥିଓରେମ')}")
        st.latex(r"P(A|B) = \frac{P(B|A) \cdot P(A)}{P(B)}")
        c1, c2, c3 = st.columns(3)
        with c1:
            p_a = st.slider("P(A)", 0.0, 1.0, 0.3)
        with c2:
            p_b_given_a = st.slider("P(B|A)", 0.0, 1.0, 0.8)
        with c3:
            p_b = st.slider("P(B)", 0.0, 1.0, 0.5)
        if p_b > 0:
            p_a_given_b = (p_b_given_a * p_a) / p_b
            st.metric("P(A|B)", f"{p_a_given_b:.4f}")
            st.info(L(f"P(A|B) = ({p_b_given_a} × {p_a}) / {p_b} = {p_a_given_b:.4f}",
                      f"P(A|B) = ({p_b_given_a} × {p_a}) / {p_b} = {p_a_given_b:.4f}"))

    with tab3:
        st.markdown(f"### 📖 {L('TF-IDF', 'TF-IDF')}")
        st.latex(r"TF(t,d) = \frac{\text{count of } t \text{ in } d}{\text{total terms in } d}")
        st.latex(r"IDF(t) = \log\frac{N}{1 + \text{number of documents containing } t}")
        st.latex(r"TF\text{-}IDF(t,d) = TF(t,d) \times IDF(t)")
        c1, c2, c3 = st.columns(3)
        with c1:
            tf_count = st.number_input(L("Term count in doc", "ଡକ୍ୟୁମେଣ୍ଟରେ ଶବ୍ଦ ଗଣନା"), min_value=0, value=3)
        with c2:
            total_terms = st.number_input(L("Total terms in doc", "ଡକ୍ୟୁମେଣ୍ଟରେ ମୋଟ ଶବ୍ଦ"), min_value=1, value=50)
        with c3:
            n_docs = st.number_input(L("Total documents (N)", "ମୋଟ ଡକ୍ୟୁମେଣ୍ଟ (N)"), min_value=1, value=100)
        doc_freq = st.number_input(L("Docs containing term", "ଶବ୍ଦ ଥିବା ଡକ୍ୟୁମେଣ୍ଟ"), min_value=0, value=5)
        if total_terms > 0 and n_docs > 0:
            tf = tf_count / total_terms
            idf = math.log(n_docs / (1 + doc_freq)) if (1 + doc_freq) > 0 else 0
            tfidf = tf * idf
            c1, c2, c3 = st.columns(3)
            c1.metric("TF", f"{tf:.4f}")
            c2.metric("IDF", f"{idf:.4f}")
            c3.metric("TF-IDF", f"{tfidf:.4f}")

    with tab4:
        st.markdown(f"### 📖 {L('Cosine Similarity', 'କୋସାଇନ ସମାନତା')}")
        st.latex(r"\cos(\theta) = \frac{A \cdot B}{\|A\| \|B\|}")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Vector A**")
            a1 = st.number_input("A1", value=1.0)
            a2 = st.number_input("A2", value=2.0)
            a3 = st.number_input("A3", value=3.0)
        with c2:
            st.markdown("**Vector B**")
            b1 = st.number_input("B1", value=2.0)
            b2 = st.number_input("B2", value=1.0)
            b3 = st.number_input("B3", value=1.0)
        A = np.array([a1, a2, a3])
        B = np.array([b1, b2, b3])
        sim = cosine_similarity(A, B)
        st.metric(L("Cosine Similarity", "କୋସାଇନ ସମାନତା"), f"{sim:.4f}")
        st.progress(max(0.0, min(1.0, sim)))

        with tab5:
            st.markdown(f"### 📖 {L('Perplexity', 'ପର୍ପ୍ଲେକ୍ସିଟି')}")
            st.latex(r"PP(W) = \sqrt[N]{\frac{1}{P(w_1 w_2 \dots w_N)}}")
            st.markdown(L("Lower perplexity = better model (less confused).",
                      "କମ୍ ପର୍ପ୍ଲେକ୍ସିଟି = ଉତ୍ତମ ମଡେଲ (କମ୍ ଦ୍ୱନ୍ଦ୍ୱ)।"))
            probs_str = st.text_input(
            L("Enter word probabilities (comma-separated):",
              "ଶବ୍ଦ ସମ୍ଭାବ୍ୟତା ଲେଖନ୍ତୁ (କମା ଦ୍ୱାରା ପୃଥକ):"),
            value="0.1, 0.2, 0.15, 0.05"
        )
        try:
            probs = [float(x.strip()) for x in probs_str.split(",") if x.strip()]
            if probs and all(0 < p <= 1 for p in probs):
                log_sum = sum(math.log(p) for p in probs)
                pp = math.exp(-log_sum / len(probs))
                st.metric(L("Perplexity", "ପର୍ପ୍ଲେକ୍ସିଟି"), f"{pp:.2f}")
            else:
                st.warning(L("Please enter valid probabilities between 0 and 1.",
                             "ଦୟାକରି 0 ଏବଂ 1 ମଧ୍ୟରେ ବୈଧ ସମ୍ଭାବ୍ୟତା ଲେଖନ୍ତୁ।"))
        except Exception:
            st.warning(L("Please enter numbers separated by commas.",
                         "ଦୟାକରି କମା ଦ୍ୱାରା ପୃଥକ ସଂଖ୍ୟା ଲେଖନ୍ତୁ।"))

    with tab6:
        st.markdown(f"### 📖 {L('Conditional Probability', 'ସର୍ତ୍ତମୂଳକ ସମ୍ଭାବ୍ୟତା')}")
        st.latex(r"P(A|B) = \frac{P(A \cap B)}{P(B)}")
        c1, c2 = st.columns(2)
        with c1:
            p_a_and_b = st.slider("P(A ∩ B)", 0.0, 1.0, 0.2)
        with c2:
            p_b_given = st.slider("P(B)", 0.01, 1.0, 0.5)
        if p_b_given > 0:
            result = p_a_and_b / p_b_given
            st.metric("P(A|B)", f"{result:.4f}")
            st.info(L(f"P(A|B) = {p_a_and_b} / {p_b_given} = {result:.4f}",
                      f"P(A|B) = {p_a_and_b} / {p_b_given} = {result:.4f}"))

# =============================================================================
# PAGE: EXPERIMENT LAB
# =============================================================================
elif "Experiment" in selected or "ପରୀକ୍ଷାଗାର" in selected:
    st.title(f"🧪 {L('Experiment Lab', 'ପରୀକ୍ଷାଗାର')}")
    st.markdown(L("Perform experiments and observe what changes.", "ପରୀକ୍ଷା କରନ୍ତୁ ଏବଂ କଣ ପରିବର୍ତ୍ତନ ହୁଏ ଦେଖନ୍ତୁ।"))

    experiment = st.selectbox(
        L("Choose an experiment:", "ଏକ ପରୀକ୍ଷା ଚୟନ କରନ୍ତୁ:"),
        [
            L("1. Change Preprocessing Steps", "1. ପ୍ରିପ୍ରୋସେସିଂ ପର୍ଯ୍ୟାୟ ପରିବର୍ତ୍ତନ"),
            L("2. Compare N-grams", "2. ଏନ-ଗ୍ରାମ ତୁଳନା"),
            L("3. Compare Word Similarity", "3. ଶବ୍ଦ ସମାନତା ତୁଳନା"),
            L("4. Change Window Size (Word2Vec)", "4. ୱିଣ୍ଡୋ ଆକାର ପରିବର୍ତ୍ତନ (Word2Vec)"),
        ]
    )

    if "1." in experiment:
        st.markdown(f"### 🎯 {L('Objective', 'ଉଦ୍ଦେଶ୍ୟ')}: {L('See how preprocessing changes text.', 'ପ୍ରିପ୍ରୋସେସିଂ ଟେକ୍ସଟକୁ କିପରି ପରିବର୍ତ୍ତନ କରେ ଦେଖନ୍ତୁ।')}")
        text = st.text_area(L("Input text:", "ଇନପୁଟ ଟେକ୍ସଟ:"), value="I love learning NLP and Odia language!")
        steps = st.multiselect(
            L("Select steps to apply:", "ଲାଗୁ କରିବାକୁ ପର୍ଯ୍ୟାୟ ଚୟନ କରନ୍ତୁ:"),
            ["Lowercase", "Tokenize", "Remove Stopwords", "Stem", "Lemmatize"],
            default=["Lowercase", "Tokenize"]
        )
        if st.button(L("Run Experiment", "ପରୀକ୍ଷା ଚଲାନ୍ତୁ")):
            result = text
            if "Lowercase" in steps:
                result = result.lower()
            tokens = simple_word_tokenize(result)
            if "Remove Stopwords" in steps:
                tokens = remove_stopwords(tokens, 'en')
            if "Stem" in steps:
                tokens = [simple_stem(t) for t in tokens]
            if "Lemmatize" in steps:
                tokens = [simple_lemmatize(t) for t in tokens]
            if "Tokenize" in steps:
                result = " | ".join(tokens)
            st.markdown(f"**{L('Result', 'ଫଳାଫଳ')}:**")
            st.code(result)
            st.markdown(f"**{L('Conclusion', 'ସିଦ୍ଧାନ୍ତ')}:** {L('Each step transforms the text differently. More steps = more normalization but less raw information.', 'ପ୍ରତ୍ୟେକ ପର୍ଯ୍ୟାୟ ଟେକ୍ସଟକୁ ଅଲଗା ଭାବରେ ପରିବର୍ତ୍ତନ କରେ। ଅଧିକ ପର୍ଯ୍ୟାୟ = ଅଧିକ ସାଧାରଣୀକରଣ କିନ୍ତୁ କମ୍ କଞ୍ଚା ସୂଚନା।')}")

    elif "2." in experiment:
        st.markdown(f"### 🎯 {L('Objective', 'ଉଦ୍ଦେଶ୍ୟ')}: {L('Compare unigram, bigram, and trigram counts.', 'ୟୁନିଗ୍ରାମ, ବାଇଗ୍ରାମ, ଏବଂ ଟ୍ରାଇଗ୍ରାମ ଗଣନା ତୁଳନା କରନ୍ତୁ।')}")
        text = st.text_area(L("Input text:", "ଇନପୁଟ ଟେକ୍ସଟ:"), value="the cat sat on the mat the cat")
        tokens = simple_word_tokenize(text.lower())
        tokens = [t for t in tokens if t not in ('।', '.', ',')]
        results = {}
        for n in [1, 2, 3]:
            ngs = generate_ngrams(tokens, n)
            results[n] = len(ngs)
        df = pd.DataFrame({
            "N": [1, 2, 3],
            "Type": ["Unigram", "Bigram", "Trigram"],
            "Count": [results[1], results[2], results[3]]
        })
        st.dataframe(df, use_container_width=True, hide_index=True)
        fig = px.bar(df, x="Type", y="Count", color="Type", title=L("N-gram Counts", "ଏନ-ଗ୍ରାମ ଗଣନା"))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(f"**{L('Conclusion', 'ସିଦ୍ଧାନ୍ତ')}:** {L('As N increases, the number of n-grams decreases.', 'N ବଢ଼ିବା ସହିତ ଏନ-ଗ୍ରାମ ସଂଖ୍ୟା କମିଥାଏ।')}")

    elif "3." in experiment:
        st.markdown(f"### 🎯 {L('Objective', 'ଉଦ୍ଦେଶ୍ୟ')}: {L('Compare similarity between word pairs.', 'ଶବ୍ଦ ଯୋଡ଼ି ମଧ୍ୟରେ ସମାନତା ତୁଳନା କରନ୍ତୁ।')}")
        words = list(WORD_VECTORS.keys())
        pairs = [("king", "queen"), ("man", "woman"), ("king", "apple"), ("car", "bus")]
        data = []
        for w1, w2 in pairs:
            if w1 in WORD_VECTORS and w2 in WORD_VECTORS:
                sim = cosine_similarity(WORD_VECTORS[w1], WORD_VECTORS[w2])
                data.append({"Pair": f"{w1} ↔ {w2}", "Similarity": round(sim, 3)})
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        fig = px.bar(df, x="Pair", y="Similarity", color="Similarity", color_continuous_scale="Viridis")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(f"**{L('Conclusion', 'ସିଦ୍ଧାନ୍ତ')}:** {L('Similar words have higher cosine similarity.', 'ସମାନ ଶବ୍ଦର ଅଧିକ କୋସାଇନ ସମାନତା ଥାଏ।')}")

    elif "4." in experiment:
        st.markdown(f"### 🎯 {L('Objective', 'ଉଦ୍ଦେଶ୍ୟ')}: {L('See how window size affects Word2Vec.', 'ୱିଣ୍ଡୋ ଆକାର Word2Vec କୁ କିପରି ପ୍ରଭାବିତ କରେ ଦେଖନ୍ତୁ।')}")
        window = st.slider(L("Window size:", "ୱିଣ୍ଡୋ ଆକାର:"), 1, 5, 2)
        st.info(L(f"With window size {window}, each word learns from {window} neighboring words on each side.",
                  f"ୱିଣ୍ଡୋ ଆକାର {window} ସହିତ, ପ୍ରତ୍ୟେକ ଶବ୍ଦ ପ୍ରତ୍ୟେକ ପାର୍ଶ୍ୱରେ {window} ପଡ଼ୋଶୀ ଶବ୍ଦରୁ ଶିଖେ।"))
        st.markdown(f"""
        <div class="card">
            <b>{L("Example:", "ଉଦାହରଣ:")}</b><br>
            {L("Sentence: 'the quick brown fox jumps'", "ବାକ୍ୟ: 'the quick brown fox jumps'")}<br>
            {L(f"With window={window}, 'brown' learns from:", f"ୱିଣ୍ଡୋ={window} ସହିତ, 'brown' ରୁ ଶିଖେ:")}<br>
            {L("Words within distance", "ଦୂରତା ମଧ୍ୟରେ ଶବ୍ଦ")} {window}: {', '.join(['the', 'quick', 'fox', 'jumps'][:2*window])}
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"**{L('Conclusion', 'ସିଦ୍ଧାନ୍ତ')}:** {L('Larger windows capture broader context; smaller windows capture tighter syntactic relationships.', 'ବଡ଼ ୱିଣ୍ଡୋ ଅଧିକ ପ୍ରସଙ୍ଗ ଧରେ; ଛୋଟ ୱିଣ୍ଡୋ କଡ଼ା ବାକ୍ୟଗତ ସମ୍ପର୍କ ଧରେ।')}")

# =============================================================================
# PAGE: TEST YOURSELF
# =============================================================================
elif "Test Yourself" in selected or "ନିଜକୁ ପରୀକ୍ଷା କରନ୍ତୁ" in selected:
    st.title(f"📝 {L('Test Yourself', 'ନିଜକୁ ପରୀକ୍ଷା କରନ୍ତୁ')}")
    st.markdown(L("Check what you have learned. Answer the questions and submit the test to see your score.", "ଆପଣ କଣ ଶିଖିଛନ୍ତି ଯାଞ୍ଚ କରନ୍ତୁ। ପ୍ରଶ୍ନଗୁଡ଼ିକର ଉତ୍ତର ଦେଇ ଟେଷ୍ଟ ସବମିଟ କରନ୍ତୁ ଏବଂ ସ୍କୋର ଦେଖନ୍ତୁ।"))

    if 'quiz_questions' not in st.session_state or st.button(L("🔄 New Test", "🔄 ନୂଆ ଟେଷ୍ଟ")):
        st.session_state.quiz_questions = random.sample(QUIZ_BANK, min(5, len(QUIZ_BANK)))
        st.session_state.quiz_answers = {}
        st.session_state.quiz_submitted = False
        st.session_state.quiz_score = 0

    questions = st.session_state.quiz_questions

    answered = sum(
        1 for i in range(len(questions))
        if st.session_state.quiz_answers.get(i)
    )
    st.info(
        L(
            f"Answer all questions below. Progress: {answered}/{len(questions)} answered.",
            f"ତଳେ ଥିବା ସମସ୍ତ ପ୍ରଶ୍ନର ଉତ୍ତର ଦିଅନ୍ତୁ। ପ୍ରଗତି: {answered}/{len(questions)} ପ୍ରଶ୍ନର ଉତ୍ତର ଦିଆଯାଇଛି।"
        )
    )

    for i, q in enumerate(questions):
        st.markdown(f"**{L('Question', 'ପ୍ରଶ୍ନ')} {i+1}:** {q['q_en'] if st.session_state.lang == 'en' else q['q_or']}")
        options = q['options_en'] if st.session_state.lang == 'en' else q['options_or']
        ans = st.radio(
            f"Q{i+1}",
            options=options,
            key=f"q_{i}",
            label_visibility="collapsed",
            index=None
        )
        st.session_state.quiz_answers[i] = ans
        st.markdown("")

    if st.button(L("✅ Submit Test", "✅ ଟେଷ୍ଟ ଜମା କରନ୍ତୁ"), type="primary"):
        score = 0
        for i, q in enumerate(questions):
            user_ans = st.session_state.quiz_answers.get(i)
            correct_ans = q['options_en'][q['answer']] if st.session_state.lang == 'en' else q['options_or'][q['answer']]
            if user_ans == correct_ans:
                score += 1
        st.session_state.quiz_score = score
        st.session_state.quiz_submitted = True
        st.session_state.quiz_total = len(questions)

    if st.session_state.get('quiz_submitted'):
        st.markdown("---")
        st.markdown(f"### 📊 {L('Results', 'ଫଳାଫଳ')}")
        c1, c2, c3 = st.columns(3)
        c1.metric(L("Score", "ସ୍କୋର"), f"{st.session_state.quiz_score}/{st.session_state.quiz_total}")
        c2.metric(L("Correct", "ସଠିକ"), st.session_state.quiz_score)
        c3.metric(L("Wrong", "ଭୁଲ"), st.session_state.quiz_total - st.session_state.quiz_score)

        pct = st.session_state.quiz_score / max(st.session_state.quiz_total, 1)
        st.progress(pct)
        if pct == 1.0:
            st.balloons()
            st.success(L("Perfect score! 🎉", "ପୂର୍ଣ୍ଣ ସ୍କୋର! 🎉"))
        elif pct >= 0.6:
            st.info(L("Good job! Keep learning. 👍", "ଭଲ କାମ! ଶିଖିବା ଜାରି ରଖନ୍ତୁ। 👍"))
        else:
            st.warning(L("Keep practicing! You can do it. 💪", "ଅଭ୍ୟାସ ଜାରି ରଖନ୍ତୁ! ଆପଣ କରିପାରିବେ। 💪"))

        st.markdown("---")
        st.markdown(f"### 📝 {L('Review Answers', 'ଉତ୍ତର ସମୀକ୍ଷା')}")
        for i, q in enumerate(questions):
            user_ans = st.session_state.quiz_answers.get(i)
            correct_ans = q['options_en'][q['answer']] if st.session_state.lang == 'en' else q['options_or'][q['answer']]
            explanation = q['explanation_en'] if st.session_state.lang == 'en' else q['explanation_or']
            is_correct = user_ans == correct_ans
            if is_correct:
                st.markdown(f"""
                <div class="quiz-correct">
                    <b>Q{i+1}: {q['q_en'] if st.session_state.lang == 'en' else q['q_or']}</b><br>
                    ✅ {L('Correct!', 'ସଠିକ!')} — {correct_ans}<br>
                    <small>{explanation}</small>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="quiz-wrong">
                    <b>Q{i+1}: {q['q_en'] if st.session_state.lang == 'en' else q['q_or']}</b><br>
                    ❌ {L('Your answer:', 'ଆପଣଙ୍କ ଉତ୍ତର:')} {user_ans or '—'}<br>
                    ✅ {L('Correct answer:', 'ସଠିକ ଉତ୍ତର:')} {correct_ans}<br>
                    <small>{explanation}</small>
                </div>
                """, unsafe_allow_html=True)

# =============================================================================
# PAGE: ABOUT
# =============================================================================
elif "About" in selected or "ବିଷୟରେ" in selected:
    st.title(f"ℹ️ {L('About', 'ବିଷୟରେ')}")
    st.markdown(f"""
    <div class="card">
        <h3>🧪 ଓଡ଼ିଆ NLP Lab</h3>
        <p><b>{L("An Interactive NLP Learning Laboratory", "ଏକ ଇଣ୍ଟରାକ୍ଟିଭ NLP ଶିକ୍ଷଣ ପରୀକ୍ଷାଗାର")}</b></p>
        <p>{L("This application is designed for school and college students to learn Natural Language Processing through interactive examples, visualizations, and experiments.",
             "ଏହି ଆପ୍ଲିକେସନ ସ୍କୁଲ ଏବଂ କଲେଜ ଛାତ୍ରଛାତ୍ରୀଙ୍କ ପାଇଁ ଇଣ୍ଟରାକ୍ଟିଭ ଉଦାହରଣ, ଭିଜୁଆଲାଇଜେସନ, ଏବଂ ପରୀକ୍ଷା ମାଧ୍ୟମରେ ନ୍ୟାଚୁରାଲ ଲାଙ୍ଗୁଏଜ ପ୍ରୋସେସିଂ ଶିଖିବା ପାଇଁ ଡିଜାଇନ କରାଯାଇଛି।")}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"### 🎯 {L('Design Principles', 'ଡିଜାଇନ ନୀତି')}")
    st.markdown(f"""
    - 📖 **{L("Learn", "ଶିଖନ୍ତୁ")}** — {L("Simple explanations", "ସରଳ ବ୍ୟାଖ୍ୟା")}
    - 🔬 **{L("Example", "ଉଦାହରଣ")}** — {L("Real sentences in English & Odia", "ଇଂରାଜୀ ଏବଂ ଓଡ଼ିଆରେ ପ୍ରକୃତ ବାକ୍ୟ")}
    - 🧪 **{L("Try Yourself", "ନିଜେ ଚେଷ୍ଟା କରନ୍ତୁ")}** — {L("Interactive inputs", "ଇଣ୍ଟରାକ୍ଟିଭ ଇନପୁଟ")}
    - 📊 **{L("Visualization", "ଭିଜୁଆଲାଇଜେସନ")}** — {L("Charts, trees, token cards", "ଚାର୍ଟ, ଟ୍ରି, ଟୋକେନ କାର୍ଡ")}
    - 💡 **{L("Simple Explanation", "ସରଳ ବ୍ୟାଖ୍ୟା")}** — {L("Why it matters", "ଏହା କାହିଁକି ଗୁରୁତ୍ୱପୂର୍ଣ୍ଣ")}
    """)

    st.markdown(f"### 📚 {L('Topics Covered', 'ଆଚ୍ଛାଦିତ ବିଷୟ')}")
    topics = [
        L("Text Preprocessing", "ଟେକ୍ସଟ ପ୍ରିପ୍ରୋସେସିଂ"),
        L("Tokenization", "ଟୋକେନାଇଜେସନ"),
        L("POS Tagging", "POS ଟ୍ୟାଗିଂ"),
        L("Named Entity Recognition", "ନାମିତ ସତ୍ତା ଚିହ୍ନଟ"),
        L("Sentiment Analysis", "ସେଣ୍ଟିମେଣ୍ଟ ବିଶ୍ଳେଷଣ"),
        L("N-Grams", "ଏନ-ଗ୍ରାମ"),
        L("Language Models", "ଭାଷା ମଡେଲ"),
        L("Parsing", "ପାର୍ସିଂ"),
        L("Word Vectors & Semantics", "ଶବ୍ଦ ଭେକ୍ଟର ଏବଂ ଅର୍ଥବିଜ୍ଞାନ"),
        L("NLP Mathematics", "NLP ଗଣିତ"),
    ]
    for t in topics:
        st.markdown(f"- {t}")

    st.markdown("---")
    st.markdown(f"""
    <div class="explain-box">
        <b>⚠️ {L("Important Note on Odia NLP", "ଓଡ଼ିଆ NLP ଉପରେ ଗୁରୁତ୍ୱପୂର୍ଣ୍ଣ ଟିପ୍ପଣୀ")}</b><br>
        {L("Many NLP tools are built primarily for English. This app uses educational demonstrations for Odia where standard tools are not available. These are simplified models designed for learning — not production systems.",
           "ଅନେକ NLP ଉପକରଣ ମୁଖ୍ୟତଃ ଇଂରାଜୀ ପାଇଁ ନିର୍ମିତ। ଏହି ଆପ୍ ଓଡ଼ିଆ ପାଇଁ ଶିକ୍ଷାମୂଳକ ପ୍ରଦର୍ଶନ ବ୍ୟବହାର କରେ ଯେଉଁଠାରେ ମାନକ ଉପକରଣ ଉପଲବ୍ଧ ନାହିଁ। ଏଗୁଡ଼ିକ ଶିକ୍ଷଣ ପାଇଁ ଡିଜାଇନ କରାଯାଇଥିବା ସରଳୀକୃତ ମଡେଲ — ଉତ୍ପାଦନ ସିଷ୍ଟମ ନୁହେଁ।")}
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.caption(L("Made with ❤️ for Odia students and NLP beginners.", "ଓଡ଼ିଆ ଛାତ୍ରଛାତ୍ରୀ ଏବଂ NLP ଆରମ୍ଭକାରୀଙ୍କ ପାଇଁ ❤️ ସହିତ ନିର୍ମିତ।"))
