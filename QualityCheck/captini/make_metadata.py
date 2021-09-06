import os

files = os.listdir('/work/ragnarp/samromur-tools/QualityCheck/captini/recordings/1')
files.sort()

metadata_file = f'/work/ragnarp/samromur-tools/QualityCheck/captini/captini_metadata.tsv'

with open(metadata_file, 'w') as f:
    f.write(f"id\tspeaker_id\tfilename\tsentence_norm\tis_valid\n")


f = open("/work/ragnarp/samromur-tools/QualityCheck/captini/captini_recordings_metadata.txt", "r")
old_metadata = f.read()
sentences = [x.split(': ')[1] for x in old_metadata.split('\n')]

i = 1
for file in files:
    with open(metadata_file, 'a') as f:
        if i < 10:
            f.write(f"0{i}\t1\t{file}\t{sentences[i-1]}\t1.0\n")
        else:
            f.write(f"{i}\t1\t{file}\t{sentences[i-1]}\t1.0\n")
        i += 1




