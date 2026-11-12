"""Build the figure and manuscript using only files in survey/."""
import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
FIGURES = ['overview', 'paradigms', 'semantic_id']


def tex_environment(tex_bin):
    env = os.environ.copy()
    if tex_bin:
        directory = Path(tex_bin).expanduser().resolve()
        if not (directory / 'latexmk').is_file():
            raise SystemExit(f'latexmk not found in {directory}')
        env['PATH'] = str(directory) + os.pathsep + env.get('PATH', '')
    elif not shutil.which('latexmk'):
        # Optional local installation from the course workspace; no files
        # outside survey are needed when TeX Live is already on PATH.
        local = ROOT.parent / '.tools' / 'texlive' / 'bin' / 'x86_64-linux'
        if (local / 'latexmk').is_file():
            env['PATH'] = str(local) + os.pathsep + env.get('PATH', '')
    for tool in ['latexmk', 'pdflatex', 'bibtex']:
        if not shutil.which(tool, path=env.get('PATH')):
            raise SystemExit(f'Missing {tool}. Install TeX Live or use --tex-bin /path/to/texlive/bin.')
    # Preserve TeX's system search paths through the final path separator.
    for key, directory in [('TEXINPUTS', ROOT / 'styles'),
                           ('BSTINPUTS', ROOT / 'styles'),
                           ('BIBINPUTS', ROOT)]:
        env[key] = str(directory) + os.pathsep + env.get(key, '') + os.pathsep
    return env


def compile_tex(source, working_directory, build_directory, env):
    build_directory.mkdir(parents=True, exist_ok=True)
    log_path = build_directory / 'build.log'
    command = ['latexmk', '-pdf', '-interaction=nonstopmode', '-halt-on-error',
               '-file-line-error', '-outdir=' + str(build_directory), source]
    with log_path.open('w') as log:
        result = subprocess.run(command, cwd=working_directory, env=env,
                                stdout=log, stderr=subprocess.STDOUT)
    if result.returncode:
        print('\n'.join(log_path.read_text(errors='replace').splitlines()[-30:]), file=sys.stderr)
        raise SystemExit(f'LaTeX build failed; full log: {log_path}')
    return build_directory / (Path(source).stem + '.pdf')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--tex-bin', help='Directory containing latexmk, pdflatex and bibtex')
    parser.add_argument('--figure-only', action='store_true', help='Build only the figure PDFs')
    parser.add_argument('--regenerate-figure', action='store_true',
                        help='Regenerate TikZ sources from generate_overview.py before compiling')
    args = parser.parse_args()
    env = tex_environment(args.tex_bin)
    if args.regenerate_figure:
        subprocess.run([sys.executable, str(ROOT / 'scripts' / 'generate_overview.py')], check=True)
    for name in FIGURES:
        figure = compile_tex(name + '.tex', ROOT / 'figures', ROOT / 'build' / 'figure', env)
        shutil.copy2(figure, ROOT / 'figures' / (name + '.pdf'))
        print(f'Built figures/{name}.pdf')
    if not args.figure_only:
        paper = compile_tex('main.tex', ROOT, ROOT / 'build' / 'paper', env)
        (ROOT / 'output').mkdir(exist_ok=True)
        shutil.copy2(paper, ROOT / 'output' / 'survey.pdf')
        print('Built output/survey.pdf')
    print('Intermediate files and logs: survey/build/ (ignored by Git)')


if __name__ == '__main__':
    main()
