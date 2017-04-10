# RecEngine python package

###  Installation:

1. all dependencies must be installed with 'sudo pip install <package>' (gensim, polyglot, nltk)

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

### Instructions for integration:

#### Right a script that does the following (single run)

1. Run the database_query script to get all data (articles) available so far
2. Read all english articles using the io module
3. Run the NLP pipeline for each article
4. Save entities (and their frequencies) in the DB
5. Create a new vector space for english by passing the articles (only tokens) to the LSIModel class
5. Save the english model file to disk
7. Repeat all steps for arabic to train a SEPARATE model

**NOTE: remember to take the language factor into account when querying/updating vectors, as both vector spaces
for english are arabic are totally different**

#### Integration with Crawler's code
For a new collection of crawled articles:
1. run the NLP pipeline to extract tokens and entities
2. load the model from disk
3. run model.update_model with the new articles' tokens
4. save the update model back to disk

#### To calculate nearest 5 articles per article/entity
**For each language/entity (we will need to keep track of language of entity as well, (UPDATE THE DB ACCORDINGLY)):**
1. query the db for all articles' vectors within the last week
2. dont forget to separate them by language
3. calculate similarity between the given article/entity and other articles using the arithmetic module
4. Save results (closest articles' IDs) back in DB

#### User onboarding
1. Get all entities user has selected
2. Get their vectors
3. Average them using the arithmetic module
4. Initialize the user's vector to be the output of this averaging
5. We will need to save the user's selected entities (UPDATE THE DB ACCORDINGLY)

#### Update user profile
1. Get user vector
2. Get vectors of all articles this user likes/clicked on
3. Average all vectors using the arithmetic module
4. Update the user's vector to be the output of this averaging

#### Get user timeline
1. Select recent articles (within a certain time frame)
2. Get nearest N artilces to the user's vector
3. In case N was less than the required amount of articles for the timeline, select the articles that has the same entities that the user selected in the onboarding
4. sort them chronologically (would be nice to do that per time period, each 15/30 mins)
5. return sorted timeline
