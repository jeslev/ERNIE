import indexed_dataset
import os

builder = indexed_dataset.IndexedDatasetBuilder('pretrain_data/merge2018.bin')
for filename in os.listdir("pretrain_data/data_2018"):
    if filename[-4:] == '.bin':
        builder.merge_file_("pretrain_data/data_2018/"+filename[:-4])
builder.finalize("pretrain_data/merge2018.idx")