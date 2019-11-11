#!/usr/bin/env python3
"""
Glossaries in markdown should be written as \gls{entry}.

There should be a master file specified somewhere in YAML file as `glossaries`.
The format of this file is same as LaTeX glossaries package.
"""

import os
import re
import panflute as P

gls_ = {}
first_ = []

def readGlossaries(gfile):
    global gsl_
    glpat = re.compile( r'\\newacronym\{\s*(?P<gls>.+?)\}' + \
            r'\s*\{(?P<short>.+?)\}\s*\{(?P<long>.+?)\}', re.DOTALL )

    with open(gfile, 'r') as h:
        glsText = h.read()
        for m in glpat.findall(glsText):
            gls_[m[0]] = m[1:]

def replaceGls(text, gls):
    global first_
    m = re.match(r'\\gls{(\S+)}', text)
    if m:
        key = m.group(1)
        if key in first_:
            if key in gls:
                return gls[key][0]
            else:
                return text
        else:
            first_.append(key)
            if key in gls:
                return gls[key][1] + f' (**{gls[key][0]}**)'
            else:
                return text
    else:
        return text

def prepare_gls(doc):
    glsFile = doc.get_metadata('glossaries')
    # Thanks to snippet here
    # https://github.com/sergiocorreia/panflute/issues/74#issue-308922983
    if doc.format in ['latex', 'context', 'tex']:
        lines =[r'\usepackage[acronym]{glossaries}'
                , r'\loadglsentries{%s}'%glsFile]
        tex = [P.MetaInlines(P.RawInline(l, format='latex')) for l in lines]
        if 'header-includes' not in doc.metadata:
            doc.metadata['header-includes'] = tex
        else:
            doc.metadata['header-includes'].content.extend(tex)
        return
    if glsFile is None or not glsFile.strip():
        return
    if os.path.exists(glsFile.strip()):
        readGlossaries(glsFile.strip())

def action_gls(elem, doc):
    global gls_
    if isinstance(elem, P.RawInline):
        if not gls_:
            return
        if '\\gls' in elem.text:
            new = P.convert_text(replaceGls(elem.text, gls_))[0]
            if isinstance(new, P.Para):
                return list(new.content)
            return P.Str(new.text)

def main(doc=None):
    P.run_filter(action_gls, prepare=prepare_gls, doc=doc)

if __name__ == '__main__':
    main()
