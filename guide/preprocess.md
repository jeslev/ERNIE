# Preprocessing
This document will show step-by-step preprocessing for the ERNIE model with explicative examples.

```shell
# Download Wikidump
wget https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2
```

However, the original ERNIE wikipedia is from 2018 (not specific month). It should be a good idea to use the [internet archive](https://archive.org/download/enwiki-20181220) dump to get the results. The type of file to use is the *pages-articles* that uses the brackets format to specify links or special data.

Then, we will need to clean the Wikipedia pages into plain text with the following line, keeping all the links.

```shell
# WikiExtractor
python3 pretrain_data/WikiExtractor.py enwiki-latest-pages-articles.xml.bz2 -o pretrain_data/output -l --min_text_length 100 --filter_disambig_pages -it abbr,b,big --processes 4
```

> <doc id="1624" url="https://en.wikipedia.org/wiki?curid=1624" title="Andrew Johnson">
> Andrew Johnson
> Andrew Johnson (December 29, 1808July 31, 1875) was the 17th <a href="president%20of%20the%20United%20States">president of the United States</a>, serving from 1865 to 1869. He assumed the presidency following <a href="assassination%20of%20Abraham%20Lincoln">the assassination</a> of <a href="Abraham%20Lincoln">Abraham Lincoln</a>, as he was <a href="vice%20president%20of%20the%20United%20States">vice president</a> at that time. Johnson was a <a href="Democratic%20Party%20%28United%20States%29">Democrat</a> who ran with Lincoln on the <a href="National%20Union%20Party%20%28United%20States%29">National Union Party</a> ticket, coming to office as the <a href="American%20Civil%20War">Civil War</a> concluded. He favored quick restoration of the <a href="Secession%20in%20the%20United%20States">seceded states to the Union</a> without protection for the <a href="Emancipation%20Proclamation">newly freed people</a> who were formerly <a href="Slavery%20in%20the%20United%20States">enslaved</a>. This led to conflict with the <a href="Republican%20Party%20%28United%20States%29">Republican</a>-dominated Congress, culminating in <a href="Impeachment%20of%20Andrew%20Johnson">his impeachment</a> by the House of Representatives in 1868. He was <a href="Impeachment%20trial%20of%20Andrew%20Johnson">acquitted in the Senate</a> by one vote.
> Johnson was born into poverty and never attended school. He was apprenticed as a tailor and worked in several frontier towns before settling in <a href="Greeneville%2C%20Tennessee">Greeneville, Tennessee</a>. He served as alderman and mayor there before being elected to the Tennessee House of Representatives in 1835. After briefly serving in the <a href="Tennessee%20Senate">Tennessee Senate</a>, Johnson was elected to the House of Representatives in 1843, where he served five two-year terms. He became governor of Tennessee for four years, and was elected by the legislature to the Senate in 1857. During his congressional service, he sought passage of the <a href="Homestead%20Bill">Homestead Bill</a> which was enacted soon after he left his Senate seat in 1862. Southern slave states seceded to form the <a href="Confederate%20States%20of%20America">Confederate States of America</a>, including Tennessee, but Johnson remained firmly with the Union. He was the only sitting senator from a Confederate state who did not resign his seat upon learning of his states secession. In 1862, Lincoln appointed him as Military Governor of Tennessee after most of it had been retaken. In 1864, Johnson was a logical choice as running mate for Lincoln, who wished to send a message of national unity in his re-election campaign, and became vice president after a victorious election in <a href="1864%20United%20States%20presidential%20election">1864</a>.

Next, we extract the data parsing the html. We process each document from the Wikipedia dump. First, it extracts the content, then concatenate with "[end]" and a list of all the entities (or links) found in the document, and add "sepsepsep" where links were found in the content. Example:

> Andrew Johnson (December 29, 1808July 31, 1875) was the 17th  sepsepsep president of the United States sepsepsep , serving from 1865 to 1869. He assumed the presidency following  sepsepsep the assassination sepsepsep  of  sepsepsep Abraham Lincoln sepsepsep , as he was  sepsepsep vice president sepsepsep  at that time. Johnson was a  sepsepsep Democrat sepsepsep  who ran with Lincoln on the  sepsepsep National Union Party sepsepsep  ticket, coming to office as the  sepsepsep Civil War sepsepsep  concluded. He favored quick restoration of the  sepsepsep seceded states to the Union sepsepsep  without protection for the  sepsepsep newly freed people sepsepsep  who were formerly  sepsepsep enslaved sepsepsep . This led to conflict with the  sepsepsep Republican sepsepsep -dominated Congress, culminating in  sepsepsep his impeachment sepsepsep  by the House of Representatives in 1868. He was  sepsepsep acquitted in the Senate sepsepsep  by one vote.Johnson was born into poverty and never attended school. He was apprenticed as a tailor and worked in several frontier towns before settling in  sepsepsep Greeneville, Tennessee sepsepsep . He served as alderman and mayor there before being elected to the Tennessee House of Representatives in 1835. After briefly serving in the  sepsepsep Tennessee Senate sepsepsep , Johnson was elected to the House of Representatives in 1843, where he served five two-year terms. He became governor of Tennessee for four years, and was elected by the legislature to the Senate in 1857. During his congressional service, he sought passage of the  sepsepsep Homestead Bill sepsepsep  which was enacted soon after he left his Senate seat in 1862. Southern slave states seceded to form the  sepsepsep Confederate States of America sepsepsep , including Tennessee, but Johnson remained firmly with the Union. He was the only sitting senator from a Confederate state who did not resign his seat upon learning of his states secession. In 1862, Lincoln appointed him as Military Governor of Tennessee after most of it had been retaken. In 1864, Johnson was a logical choice as running mate for Lincoln, who wished to send a message of national unity in his re-election campaign, and became vice president after a victorious election in  sepsepsep 1864 sepsepsep ...... [_end_]
> president of the United States[_map_]president%20of%20the%20United%20States[_end_]
> the assassination[_map_]assassination%20of%20Abraham%20Lincoln[_end_]
> Abraham Lincoln[_map_]Abraham%20Lincoln[_end_]
> vice president[_map_]vice%20president%20of%20the%20United%20States[_end_]
> Democrat[_map_]Democratic%20Party%20%28United%20States%29[_end_]
> National Union Party[_map_]National%20Union%20Party%20%28United%20States%29[_end_]
> Civil War[_map_]American%20Civil%20War[_end_]
> seceded states to the Union[_map_]Secession%20in%20the%20United%20States[_end_]
> newly freed people[_map_]Emancipation%20Proclamation[_end_]
> enslaved[_map_]Slavery%20in%20the%20United%20States[_end_]
> Republican[_map_]Republican%20Party%20%28United%20States%29[_end_]
> his impeachment[_map_]Impeachment%20of%20Andrew%20Johnson[_end_]
> acquitted in the Senate[_map_]Impeachment%20trial%20of%20Andrew%20Johnson[_end_]
> Greeneville, Tennessee[_map_]Greeneville%2C%20Tennessee[_end_]
> Tennessee Senate[_map_]Tennessee%20Senate[_end_]
> Homestead Bill[_map_]Homestead%20Bill[_end_]
> Confederate States of America[_map_]Confederate%20States%20of%20America[_end_]
> 1864[_map_]1864%20United%20States%20presidential%20election[_end_]

## Creating anchor2id.txt
We can re-used the given anchord2id.txt file from the repository. Or we can create for ourselves following the code. Since we are using our own version of Wikipedia, we should create it by ourselves.

```shell
# extract anchors
python3 pretrain_data/utils.py get_anchors
```

For each cleaned document from the previous step, it will extract all [_map_] and [_end_] tag, and it will create a list all anchors (2nd argument from [map][end]). A sample:

> ["butterfly", "Nymphalidae", "Guinea-Bissau", "Guinea", "Sierra%20Leone", "Liberia", "Ivory%20Coast", "Ghana", "Togo", "Benin", "Nigeria", "Cameroon", "Equatorial%20Guinea", "Gabon", "Central%20African%20Republic", "Angola", "Democratic%20Republic%20of%20the%20Congo", "Sudan", "Uganda" ...


Next, we query the Wikipedia api to get information about the entities. We get the Wikipedia ID (Qid) if it exists, else we use the '#UNK' id.

```shell
# query Mediawiki api using anchor link to get wikibase item id. For more details, see https://en.wikipedia.org/w/api.php?action=help.
python3 pretrain_data/create_anchors.py 256 
```

> DONE[TODO] : Check how many UNKs exists. From my own script I found that Wikidata API banned my requests so I had many UNK for entities that existed. For now, I am using the anchor2id.txt file given by the authors.

Finally, it creates a single file anchor2id.txt

```shell
# aggregate anchors 
python3 pretrain_data/utils.py agg_anchors
```

## Back to the Wikipedia pre-processing

We will tokenize the input (doing it offline to improve performance at training). For each input file, it will create two file '_token' and '_entity'.
It will tokenize the input text (the content part) and maps the entities IDs with their corresponding id from the anchord2id.txt file, it it exists.

```shell
# Preprocess with 4 processes
python3 pretrain_data/create_ids.py 4
```

Then, it will create the '_token' file with all the tokens from the input (ignoring the sepsepsep token), and the '_entity' file with with the Qid from the anchord2id.txt file, or '#UNK' if it is a textual token or the entity is not recognized. It removes phrases without entities mentions. The format of the vectors are (number of sentences) (sentence length) (sentencen tokens) (sentence length)... Similarly for entities.


Finally, we create the training instances with the following code:

```shell
# create instances
python3 pretrain_data/create_insts.py 4
# merge
python3 code/merge.py
```

It first loads the entity2id.txt used to train the transE embeddings, with the format:

> Qxxxx 12345678

Now, it loads the '_token' and '_entity' files from previous step. It creates a vector full of -1 for the entity, when it is '#UNK', if it is a wikipedia ID (Q*) it will replace it with the ID, or -1 it is not in the list (or if multi token entity, it put ID only in the first token). 

Then, it will iterate the sentences from the document until getting enough length for the input (or using all document). It creates 2 sentences, to sample NSP.
Finally, it create an input with the format:
1. Input ids + input masks + segment ids + masked LM labels
2. entity (ids) + entitiy mask (1 for entities, 0 for unk)
3. NSP label

