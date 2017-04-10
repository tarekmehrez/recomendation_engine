# RecEngine python package

###  Installation:

1. install dependencies must with 'pip install <package>' (gensim, polyglot, nltk)

2. nltk stop words must be downloaded via the nltk downlaod module
in ipython:

    ```python
    import nltk
    nltk.download()
    ```

   In the GUI window that opens simply go to the 'Corpora' tab and only english stop words list


3. as for polyglot run the following commands (after you install the package) in the terminal

    ```shell
    polyglot download ner2.en
    polyglot download ner2.ar
    polyglot download embeddings2.en
    polyglot download embeddings2.ar
    ```


4. in the project's root directory run:

    ````shell
    python setup.py install
    ````

### Usage:

1. To extract entities:

    ```python
    from tbont_text_engine.nlp import pipeline
    tagged_text = pipeline.start_pipeline(article, language ='en') # or 'ar'
    tokens = tagged_text.tokens
    entities = tagged_text.entities
    ```

2. to create vector space (runs only one time):

    ```python
    from tbont_text_engine.vector_space import LSIModel
    model = LSIModel()
    model.train_model(articles_dict) # articles_dict {'id': [list of tokens]}
    ````

3. to update vector space:

    ```python
    model.update_model(articles_dict) # articles_dict {'id': [list of tokens]}
    ```

4. to get article vector:

    ```python
    model.get_article_vector(article_id)
    ```

5. to get token vector:

    ```python
    model.get_token_vector(token) # token as a str or unicode
    ```

6. to get closest vector to other list of vectors:

    ```python
    from tbont_text_engine.vector_space import arithmetic
    arithmetic.get_closest(vector, vectors_dict) # vectors_dict {'id': vector}, vector is a numpy array
    ```

7. to get average of vectors:

    ```python
    from tbont_text_engine.vector_space import arithmetic
    arithmetic.average_vectors(vectors) # list of vectors you want to average
    ```


8. to load/save models:

    ```python
    model.save(file_path)
    model.load(file_path)
    ```
9. to read txt files:

    ```python
    from tbont_text_engine.utils import io
    io.read('file.txt')
    ```
