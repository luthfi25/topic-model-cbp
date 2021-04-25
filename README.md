# topic-model-cbp
Topic Model for Consensus Building Process

Contains the source code and binary required to perform topic modeling specifically to improve consensus bulding process.
Used in "Analaysis on the Usage of Topic Model with Background Knowledge inside Discussion Activity in Industrial Engineering Context" (Luthfi, 2020)

## Quickstart

### Step 1: Preparing the environment
Make sure to install and download the following stuffs before running the program:

* java (current version)
* python3
* nltk (python package)
* pandas (python package)
* scipy (python packaage)
* Wikipedia Corpus ([Here](#)) **Put the file in topic_model folder!**
* Global Vectors ([Here](https://nlp.stanford.edu/projects/glove/))  **Put the file in dataset folder!**

### Step 2: Running Topic Model for CBP
The following inputs are necessary. ***Always keep it in dataset folder!***

* **Dataset**, a .csv file conisting sentences to be analyzed. Based on our research scope, the sentence must have their respective institution (company) IDs.
Mandatory fields are `sentence_english` (string, raw sentence written in english) and `company_id` (integer)
 
* **Background Knowledge**, a .csv file consisting topic-definition pairs used as background knowledge to determine the number of topic and topic probability.
Mandatory fields are `label` (string, topic name) and `definition` (string, a paragraph defining topic)

To run the program, please use the following syntax  
`$ python main.py --input_dataset=[DATASET_FILE_PATH] --input_background=[BACKGROUND_KNOWLEDGE_FILE_PATH]`

### Step 3: Output
Complete output of the program can be found in  
`dataset/[DATASET_FILE_NAME]/[TIMESTAMP_OF_PROGRAM_EXECUTION/results/`

Output list:
* `[DATASET_FILE_NAME].phi` (word probability for each topics)
* `[DATASET_FILE_NAME].theta` (topic probability for each sentences)
* `[DATASET_FILE_NAME].average_topic` (topic probability for each institutions / companies)
* `[DATASET_FILE_NAME].similarity_matrix` (similarity of topic probabilites between two institutions / companies()
* `[DATASET_FILE_NAME].topWords` (top 10 probable words for each topics)
* `[DATASET_FILE_NAME].vocabulary` (word - word_id pair)

Note: during program execution, additional files other than above such as cleaned sentences and augmented sentences will be generated.  
The files can be found in `dataset/[DATASET_FILE_NAME]/` and `dataset/[BACKGROUND_KNOWLEDGE_FILE_NAME]/` folder, it was intended for reference only.

## Contributing
Feel free to fork this repository and provide suggestions either by **Issue** or **Pull Request**.  
You can contact me on weekdays (Japanese Time) on [luthfi.muhammad825@gmail.com](mailto:luthfi.muhammad825@gmail.com)
