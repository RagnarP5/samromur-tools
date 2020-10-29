from functools import partial

from os import environ
from os.path import join, abspath, dirname, isdir, exists
from config import conf

class MarosijoError(Exception):
    pass

class MarosijoCommon:
    """MarosijoCommon
    ==================

    Paths, data and other settings for the MarsijoModule

    """
    _REQUIRED_FILES = ('tree', 'acoustic_mdl', 'symbol_tbl',
                       'lexicon_fst', 'disambig_int', 'oov_int',
                       'sample_freq', 'phone_lm', 'lexicon.txt')

    #: Not required to exist when compiling graphs, obviously.
    _REQUIRED_FILES_AFTER_COMPILE = ('graphs.scp', )

    def __init__(self, modelPath=None, downsample=False, graphs=True):
        """
        Parameters:

          modelPath    Path to directory containing model files.
                       Should contain the following files: tree,
                       acoustic_mdl, symbol_tbl, lexicon_fst,
                       disambig_int, unk_int, sample_freq.  These
                       files are generated by
                       ../scripts/train_acoustic_model.sh

        """
        if modelPath is None:
            modelPath = join(dirname(__file__), 'local/')
        self.modelPath = abspath(modelPath)
        self._validateModel(modelPath=self.modelPath, graphs=graphs)
        self.downsample = downsample

        mkpath = partial(join, self.modelPath)
        self.treePath = mkpath('tree')
        self.acousticModelPath = mkpath('acoustic_mdl')
        self.symbolTablePath = mkpath('symbol_tbl')
        self.lexiconFstPath = mkpath('lexicon_fst')
        self.disambigIntPath = mkpath('disambig_int')
        self.oovIntPath = mkpath('oov_int')
        #: File contains sample freq of acoustic model
        self.sampleFreqPath = mkpath('sample_freq')
        self.phoneLmPath = mkpath('phone_lm')
        self.lexiconTxtPath = mkpath('lexicon.txt')

        if graphs:
            self.graphsScpPath = mkpath('graphs.scp')

        with open(self.oovIntPath) as f_:
            self.oov = int(f_.read().strip())

        with open(self.sampleFreqPath) as f_:
            self.sampleFreq = int(f_.read().strip())

        with open(self.disambigIntPath) as f_:
            self.disambigInt = [int(l.strip()) for l in f_]

        with open(self.symbolTablePath) as f_:
            self.symbolTable = dict(line.strip().split() for line in f_)

        self.symbolTableToInt = dict((val, key) for key, val in
                                     self.symbolTable.items())

        with open(self.lexiconTxtPath) as f_:
            # self.lexicon = {}
            # for line in f_:
            #     try:
            #         self.lexicon[line.strip().split('\t')[0]] = line.strip().split('\t')[1].split(' ')
            #     except IndexError as e:
            #         print(line)
            self.lexicon = {line.strip().split('\t')[0]:line.strip().split('\t')[1].split(' ')
                            for line in f_}

        self.avgPhonemeCount = round(sum([len(key) for val, key in self.lexicon.items()]) / max(len(self.lexicon), 1)) # thanks, NPE, http://stackoverflow.com/a/7716358/5272567

        try:
            #: Absolute path to Kaldi top-level dir
            self.kaldiRoot = conf['kaldi_root']
        except KeyError:
            print("Can't find Kaldi")
    
    

    @classmethod
    def _validateModel(cls, modelPath, graphs=True ):
        missingFiles = []
        if not isdir(modelPath):
            raise MarosijoError(
                f"The supplied modelPath '{modelPath}' either does not exist or is not a directory")

        if graphs:
            requiredFiles = cls._REQUIRED_FILES + cls._REQUIRED_FILES_AFTER_COMPILE
            extraMsg = 'Did you forget to run the graph generation script?'
        else:
            requiredFiles = cls._REQUIRED_FILES
            extraMsg = 'Did you forget the model preparation step?'

        for file_ in requiredFiles:
            fileExists = exists(join(modelPath, file_))
            if not fileExists:
                missingFiles.append(file_)

        if missingFiles:
            raise MarosijoError('Following model files are missing from "{}": {}.  {}'
                                .format(modelPath, ', '.join(f_ for f_ in missingFiles),
                                        extraMsg))
                                        
    def symToInt(self, token: str, forceLowercase=True) -> str:
        def lower(s, lower=True):
            return s.lower() if lower else s        
    
        int_tokens = ' '.join(self.symbolTable.get(token_, str(self.oov)) for token_ in lower(token, lower=forceLowercase).split())

        return ' '.join(self.symbolTable.get(token_, str(self.oov)) for
                        token_ in lower(token, lower=forceLowercase).split())

    def intToSym(self, tokenInts: list) -> list:
        return [self.symbolTableToInt[token_] for token_ in tokenInts]

