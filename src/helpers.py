# Helper functions
# ================

import xml.dom.minidom
import json

from constants import DELETECHARS, contractions


def sum_vect(vect1, vect2):
    if len(vect1) == 0:
        vect1 = [0] * len(vect2)
    res = [x + y for x, y in zip(vect1, vect2)]
    return res

# def sum_vect(dic1,dic2):
#     res=dic1
#     for i in dic2.keys():
#         if res.has_key(i):
#             res[i]+=dic2[i]
#         else:
#             res[i]=dic2[i]
#     return res


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


def serialize_to_json(susp, src, features, outdir):
    response = {
        'src_file': src,
        'susp_file': susp,
        'fragments': []
    }

    for f in features:
        fragment = {
            'src_offset': str(f[0][0]),
            'src_len': str(f[0][1] - f[0][0]),
            'susp_offset': str(f[1][0]),
            'susp_len': str(f[1][1] - f[1][0])
        }
        response['fragments'].append(fragment)

    with open(outdir + susp.split('.')[0] + '-' + src.split('.')[0] + '.json', 'w') as outfile:
        json.dump(response, outfile)
        