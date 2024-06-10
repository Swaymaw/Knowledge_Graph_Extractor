import PyPDF2
import spacy 
from nltk.corpus import stopwords
import nltk 
from openie import StanfordOpenIE
import ast
import re
from nltk.tokenize import RegexpTokenizer


def extract_text_from_pdf(file):
    pdf_text = ""
    file = ast.literal_eval(file)
    with open("tmp.pdf", "wb") as f: 
        f.write(file)
    
    f = open("tmp.pdf", "rb")

    reader = PyPDF2.PdfReader(f, strict=False)
    for page in reader.pages: 
        content = page.extract_text()
        pdf_text += content + "\n"
    
    return pdf_text

nltk.download('stopwords')
nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"]) 
spacy_words = set(nlp.vocab.strings)
stop_words = set(stopwords.words("english"))


def text_cleanup(inp_str: str): 
    vocab = spacy_words

    # 1) Lower Casing ✅
    inp_str = inp_str.lower()

    # 2) Remove redundant whitespaces ✅
    inp_str = inp_str.replace('{html}',"") 
    inp_str = inp_str.replace("\n", " ")
    inp_str = inp_str.replace("\t", " ").strip()

    # 3) Cleaning Unncessary Characters and URLs ✅
    cleanr = re.compile('<.*?>')
    inp_str = re.sub(cleanr, '', inp_str)
    inp_str = re.sub(r'http\S+', '', inp_str)
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(inp_str)  
    filtered_words = [w for w in tokens if len(w) > 2]

    # 3) Stop Words Removal ✅ Gives Worse Results
    # inp_str_splitted = [w for w in inp_str_splitted if w not in stop_words]

    cleaned_str = " ".join(filtered_words)

    # 4) Punctuation removal and Lemmatization ✅
    doc = nlp(cleaned_str)
    text_no_punc = [token.lemma_ for token in doc if not token.is_punct]

    # 5) Removing WhiteSpaces caused due to Parsing Errors and Special Character removal ✅ 
    out_words = []
    i = 0 
    while i < len(text_no_punc): 
        word = text_no_punc[i]
        if word not in vocab and i+1 < len(text_no_punc): 
            next_word = text_no_punc[i+1]
            joined = word + next_word
            if joined.strip() in vocab: 
                word = joined
                i += 1
            else:
                if (i-1) > 0: 
                    prev_word = text_no_punc[i-1]
                    joined = prev_word + word 

                    if joined.strip() in vocab: 
                        word = joined 
                        del out_words[-1] 
        out_words.append(word)
        i += 1
    cleaned_str = " ".join(out_words)

    return cleaned_str

properties = {
    "openie.affinity_probability_cap": 3/4, 
}

def chunked_triplet_extractor(text, chunk_size=200, step_size=100): 
    fin_triplets = []
    text_splitted = text.split()
    with StanfordOpenIE(properties=properties) as client: 
        for i in range(0, len(text_splitted) - chunk_size, step_size):
            work_text = text_splitted[i:i+chunk_size]
            work_text = " ".join(work_text)
            for triple in client.annotate(work_text):
                if triple not in fin_triplets[-10:]: 
                    fin_triplets.append(triple)
        client.generate_graphviz_graph(text, "graph.png")
    
    return fin_triplets
