# Helper functions
# ================


import string
import xml.dom.minidom

from constants import DELETECHARS


def tokenize(text, length):
    """ Tokeniz a given text and return a dict containing all start and end
    positions for each token.
    Characters defined in the global string DELETECHARS will be ignored.

    Keyword arguments:
    text   -- the text to tokenize
    length -- the length of each token
    """
    tokens = {}
    token = []

    for i in range(0, len(text)):
        if text[i] not in DELETECHARS:
            token.append((i, text[i]))
        if len(token) == length:
            ngram = ''.join([x[1].lower() for x in token])
            if ngram not in tokens:
                tokens[ngram] = []
            tokens[ngram].append((token[0][0], token[-1][0]))
            token = token[1:]

    return tokens


def serialize_features(susp, src, features, outdir):
    """ Serialze a feature list into a xml file.
    The xml is structured as described in the readme file of the
    PAN plagiarism corpus 2012. The filename will follow the naming scheme
    {susp}-{src}.xml and is located in the current directory.
    Existing files will be overwritten.

    Keyword arguments:
    susp     -- the filename of the suspicious document
    src      -- the filename of the source document
    features -- a list containing feature-tuples of the form
                ((start_pos_susp, end_pos_susp),
                 (start_pos_src, end_pos_src))
    """
    impl = xml.dom.minidom.getDOMImplementation()
    doc = impl.createDocument(None, 'document', None)
    root = doc.documentElement
    root.setAttribute('reference', susp)
    doc.createElement('feature')

    for f in features:
        feature = doc.createElement('feature')
        feature.setAttribute('name', 'detected-plagiarism')
        feature.setAttribute('this_offset', str(f[1][0]))
        feature.setAttribute('this_length', str(f[1][1] - f[1][0]))
        feature.setAttribute('source_reference', src)
        feature.setAttribute('source_offset', str(f[0][0]))
        feature.setAttribute('source_length', str(f[0][1] - f[0][0]))
        root.appendChild(feature)

    doc.writexml(open(outdir + susp.split('.')[0] + '-'
                      + src.split('.')[0] + '.xml', 'w'),
                 encoding='utf-8')
