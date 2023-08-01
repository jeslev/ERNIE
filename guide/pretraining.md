# Pre-Training
The pre-processing done by ERNIE takes entities from links in Wikipedia and associated them to Nodes Embeddings (TransE). To create the input instances, it will check for a phrase from a Wikipedia page, identify its entities and apply MLM, NSP and dEA tasks.

The needed files to generate the pretraining are:
- kg_embed: The TransE embeddings created from Wikidata5M triplets (given by the authors ERNIE - local path: downloaded_files/kg_embed)
- anchor2id.txt: List of URL (entity mention from Wikipedia) and Wikidata ID. It does requests to Wikidata API (takes too much time!). I am using the one facilitated in ERNIE repo.
- Wikipedia: We use the Dic 2018 dump (from Internet Archive). This will generate a merge.idx and merge.bin file to be read by the Language Model.


## Results
We compare the theoric results (from the ERNIE paper) and the results obtained after fine-tuning the ERNIE model given by the authors in the repository. Finally, we also pre-trained an ERNIE on our own with different settings.

### Relation Classification - FewRel


| Model | P | R | F1 |
| --- | --- | --- | --- |
| paper | 88.49 | 88.44 | 88.32 |
| code | 88.00 | 88.00 | 88.00 |
| --- | --- | --- | ---|
|2018_epoch 3| 86.75 | 86.75 | 86.75|



### Relation Classification - TACRED



| Model | P | R | F1 |
| --- | --- | --- | --- |
| paper | 69.97 | 66.08 | 67.97 |
| code | 68.61 | 64.69 | 66.59 |
| --- | --- | --- | --- |
|2018_epoch 3| 65.34 | 66.11 | 65.73|




### Entity Typing - OpenEntity



| Model | P | R | F1 |
| --- | --- | --- | --- |
| paper | 78.42 | 72.90 | 75.56 |
| code | 78.57 | 71.64 | 74.95 |
| --- | --- | --- | --- |
|2018_epoch 3| 77.64 | 68.22 | 72.63|



