from os import getcwd
from os.path import join

conf = dict(
    #Needed both for the training and evaluation steps
    kaldi_root = '/opt/kaldi',  # Alternative path: '/home/derik/work/kaldi'
    sample_rate = 16000,

    #Path to recordings and subsequent metadata file. Used to train the acustic monophone model
    #and can also be used to decode and examine recordings.
    # recs = '/work/smarig/h1/samromur-data/as_of_050221/050221_audio_clips/audio_correct_names',
    recs = '/work/ragnarp/samromur-tools/QualityCheck/captini/recordings',
    # metadata = '/work/smarig/h1/samromur-data/as_of_050221/050221_metadata/metadata_all_clips_inspect_scored_normalized.tsv',
    metadata = '/work/ragnarp/samromur-tools/QualityCheck/captini/captini_metadata.tsv',
  
  
    #Variables that you mostlikely wont have to change
    model = join(getcwd(), 'modules', 'local'),
    reports_path = join(getcwd(), 'reports'), 
) 

print("done")