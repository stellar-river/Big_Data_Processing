"""Regenerate the taxonomy figure sources; leaves main.tex untouched."""
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
out = root / 'figures'
out.mkdir(parents=True, exist_ok=True)
bib = (root / 'references.bib').read_text()
entries = {}
for line in bib.splitlines():
    match = re.match(r'@\w+\{([^,]+),', line)
    if match:
        entries[match[1]] = line

def work(name, key):
    entry = entries[key]
    authors = re.search(r'author\s*=\s*\{([^}]+)\}', entry).group(1).split(' and ')
    surnames = [a.split(',')[0].strip() for a in authors]
    author = surnames[0] + (r' et al.' if len(authors) > 2 else ' and ' + surnames[1])
    year = re.search(r'year\s*=\s*\{(\d+)\}', entry).group(1)
    return rf'\mbox{{\textbf{{{name}}}}} {author} ({year})'

def works(*pairs):
    return '; '.join(work(name, key) for name, key in pairs) + '.'

def accent(text, color='treered'):
    return rf'\textcolor{{{color}}}{{{text}}}'

def title(text, section):
    return rf'\textbf{{\textit{{{text}}}}} ({section}): '

leaves = [
    ('a1', 'lm', title('Recommendation-Oriented Adaptation', '3.1.1') +
        accent('Task adaptation: ') + works(('P5','p5'),('InstructRec','instructrec'),('TALLRec','tallrec')) + ' ' +
        accent('Domain-oriented training: ', 'treecyan') + works(('RecGPT','recgpt'),('GenRec','genrec'))),
    ('a2', 'lm', title('Output Representations and Catalog Grounding', '3.1.2') +
        accent('Textual item generation: ') + works(('GenRec','genrec')) + ' ' +
        accent('Query generation: ', 'treecyan') + works(('GPT4Rec','gpt4rec')) + ' ' +
        accent('Catalog grounding: ', 'treegreen') + works(('BIGRec','bigrec'))),
    ('a3', 'rec', title('Generative Retrieval and Semantic IDs', '3.2.1') +
        accent('Semantic-ID generation: ') + works(('TIGER','tiger'))),
    ('a4', 'rec', title('Collaborative and Multimodal Tokenization', '3.2.2') +
        accent('Collaborative alignment: ') + works(('LC-Rec','lcrec'),('LETTER','letter'),('CoST','cost')) + ' ' +
        accent('Multimodal codes: ', 'treecyan') + works(('MMGRec','mmgrec')) + ' ' +
        accent('Behavior--semantic generation: ', 'treegreen') + works(('EAGER','eager'))),
    ('a5', 'rec', title('Joint Tokenization and Generation', '3.2.3') +
        accent('Shared backbone: ') + works(('STORE','store')) + ' ' +
        accent('Tokenizer--recommender alignment: ', 'treecyan') + works(('ETEGRec','etegrec')) + ' ' +
        accent('Collaborative tokenization and retrieval: ', 'treegreen') + works(('TokenRec','tokenrec'))),
    ('a6', 'rec', title('Scalable Sequential and Session Generation', '3.2.4') +
        accent('Multi-behavior modeling: ') + works(('MBGen','mbgen')) + ' ' +
        accent('Scalable sequential transduction: ', 'treecyan') + works(('HSTU','hstu')) + ' ' +
        accent('Recommendation-list generation: ', 'treegreen') + works(('OneRec','onerec'))),
    ('a7', 'diff', title('Interaction and Item Representation Diffusion', '3.3.1') +
        accent('Interaction reconstruction: ') + works(('DiffRec','diffrec')) + ' ' +
        accent('Target item generation: ', 'treecyan') + works(('DreamRec','dreamrec'),('DiffuRec','diffurec')) + ' ' +
        accent('Dynamic preference modeling: ', 'treegreen') + works(('DimeRec','dime'))),
    ('a8', 'diff', title('Discrete-State and Catalog-Aware Generation', '3.3.2') +
        accent('Discrete-to-continuous diffusion: ') + works(('DCRec','dcrec')) + ' ' +
        accent('Discrete-state diffusion: ', 'treecyan') + works(('DDSR','ddsr'))),
    ('a9', 'diff', title('Preference Alignment and Efficient Inference', '3.3.3') +
        accent('Ranking alignment: ') + works(('PreferDiff','preferdiff')) + ' ' +
        accent('Preference-guided recommendation: ', 'treecyan') + works(('PDRec','pdrec')) + ' ' +
        accent('One-step generation: ', 'treegreen') + works(('TA-Rec','tarec'))),
    ('c1', 'representation', accent('Text, semantic codes, and continuous representations: ') +
        'information sharing, semantic transfer, collaborative signals, and representation geometry.'),
    ('c2', 'objectives', accent('Likelihood, denoising, and preference alignment: ') +
        'relationships between generative training signals and recommendation utility.'),
    ('c3', 'inference', accent('Decoding, denoising, and catalog mapping: ') +
        'validity constraints, identifier maintenance, and complete serving costs.'),
    ('c4', 'evaluation', accent('Effectiveness and efficiency: ') +
        'consistent tasks, temporal splits, candidate sets, computational budgets, and pipeline evaluation.'),
]

groups = [
    ('lm', r'Language-model-based\\recommendation\\(Sec.~3.1)', 'a1', 'a2'),
    ('rec', r'Recommendation-specific\\generative systems\\(Sec.~3.2)', 'a3', 'a6'),
    ('diff', r'Diffusion-based\\recommendation\\(Sec.~3.3)', 'a7', 'a9'),
    ('representation', r'Representation and\\inductive bias\\(Sec.~4.1)', 'c1', 'c1'),
    ('objectives', r'Learning objectives\\and decision alignment\\(Sec.~4.2)', 'c2', 'c2'),
    ('inference', r'Inference, validity,\\and catalog dynamics\\(Sec.~4.3)', 'c3', 'c3'),
    ('evaluation', r'Evaluation and\\comparability\\(Sec.~4.4)', 'c4', 'c4'),
]
majors = [
    ('architectures', r'Model-Level\\Generative\\Architectures\\(Sec.~3)', 'a1', 'a9', ['lm','rec','diff']),
    ('comparison', r'Cross-Paradigm\\Comparison\\(Sec.~4)', 'c1', 'c4',
        ['representation','objectives','inference','evaluation']),
]

lines = [r'''% Reference-style taxonomy. All methods and bibliographic metadata
% are drawn from the main.tex and references.bib.
% Section numbers follow the current manuscript's organization.
\begingroup
\definecolor{treeblue}{HTML}{264F95}
\definecolor{treeorange}{HTML}{DF7943}
\definecolor{treegreen}{HTML}{528D36}
\definecolor{treered}{HTML}{D94E42}
\definecolor{treecyan}{HTML}{177FA6}
\begin{tikzpicture}[
    x=1cm,y=1cm,
    every node/.style={font=\fontsize{7.3}{8.6}\selectfont,
        align=left,text=black,outer sep=0pt},
    root/.style={draw=treeblue,line width=.65pt,rounded corners=1.8pt,
        fill=treeblue!2,text width=1.02cm,inner sep=3pt},
    major/.style={draw=treeorange,line width=.6pt,rounded corners=1.8pt,
        fill=treeorange!3,text width=2.25cm,inner sep=3pt},
    category/.style={draw=treegreen,line width=.55pt,rounded corners=1.8pt,
        fill=treegreen!3,text width=2.85cm,inner sep=3pt,
        font=\fontsize{7.1}{8.3}\selectfont},
    detail/.style={draw=black!48,line width=.45pt,rounded corners=2pt,
        fill=black!2,text width=9.05cm,inner sep=3pt,
        minimum height=.98cm},
    link/.style={draw=black!65,line width=.55pt}
]''']

previous = None
previous_group = None
for name, group, content in leaves:
    if previous is None:
        placement = '(8.1,0)'
    else:
        gap = '.16' if group == previous_group else '.25'
        if name == 'c1':
            gap = '.45'
        placement = rf'([yshift=-{gap}cm]{previous}.south west)'
    lines.append(rf'\node[detail,anchor=north west] ({name}) at {placement} {{{content}}};')
    previous, previous_group = name, group

for name, content, first, last in groups:
    lines.append(rf'\coordinate (mid-{name}) at ($({first}.west)!.5!({last}.west)$);')
    lines.append(rf'\node[category,anchor=west] ({name}) at (4.65,0 |- mid-{name}) {{{content}}};')
    lines.append(rf'\draw[link] ({name}.east) -- (7.87,0 |- {name}.east);')
    lines.append(rf'\draw[link] (7.87,0 |- {first}.west) -- (7.87,0 |- {last}.west);')
    for leaf, group, _ in leaves:
        if group == name:
            lines.append(rf'\draw[link] (7.87,0 |- {leaf}.west) -- ({leaf}.west);')

for name, content, first, last, children in majors:
    lines.append(rf'\coordinate (mid-{name}) at ($({first}.west)!.5!({last}.west)$);')
    lines.append(rf'\node[major,anchor=west] ({name}) at (1.72,0 |- mid-{name}) {{{content}}};')
    lines.append(rf'\draw[link] ({name}.east) -- (4.39,0 |- {name}.east);')
    lines.append(rf'\draw[link] (4.39,0 |- {children[0]}.west) -- (4.39,0 |- {children[-1]}.west);')
    for child in children:
        lines.append(rf'\draw[link] (4.39,0 |- {child}.west) -- ({child}.west);')

lines.extend([
    r'\coordinate (mid-root) at ($(a1.west)!.5!(c4.west)$);',
    r'\node[root,anchor=west] (overview) at (0,0 |- mid-root) {Survey\\Overview};',
    r'\draw[link] (overview.east) -- (1.44,0 |- overview.east);',
    r'\draw[link] (1.44,0 |- architectures.west) -- (1.44,0 |- comparison.west);',
])
for name, *_ in majors:
    lines.append(rf'\draw[link] (1.44,0 |- {name}.west) -- ({name}.west);')
lines.extend([r'\end{tikzpicture}', r'\endgroup'])
(out / 'overview.tikz').write_text('\n'.join(lines) + '\n')

standalone = r'''\documentclass[border=5pt]{standalone}
\usepackage[T1]{fontenc}
\usepackage{libertine}
\usepackage{tikz}
\usetikzlibrary{calc}
\begin{document}
\input{overview.tikz}
\end{document}
'''
(out / 'overview.tex').write_text(standalone)

print('Generated figures/overview.tikz and figures/overview.tex from references.bib.')
