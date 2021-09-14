import argparse
import os
import os.path
import sys
import re
import tempfile
import shutil
import subprocess
import hashlib
import sqlite3
from contextlib import contextmanager
from tqdm import tqdm
from pathlib import Path
from cuttlepool import CuttlePool

BLOCKSIZE = 65536

# key for performing a natural sort
def natural_sort_key(s, _nsre=re.compile('([0-9]+)')):
        return [int(text) if text.isdigit() else text.lower()
                for text in re.split(_nsre, str(s))] 

class SQLitePool(CuttlePool):
    """Pool for sqlite3 connections."""
    def normalize_resource(self, resource):
        """Modifies properties for connection objects."""
        resource.row_factory = None
    
    def ping(self, resource):
        """Checks that connection is still active."""
        try:
            ret = resource.execute('SELECT 1').fetchall()
            return (1,) in ret
        except sqlite3.Error:
            return False

class HashDB:
        def __init__(self, path):
                self.pool = SQLitePool(factory=sqlite3.connect, database=path, capacity=10)
                
                # Setup the database if it's empty.
                with self.pool.get_resource() as c:
                        c.executescript("""
create table if not exists file_hashes (path text, 
                                        hash text,
                                        unique(path));
                        """)
                        c.commit()

        def _hash(self, f):
                # hash the file
                h = hashlib.md5()
        
                # read the file in as binary
                with f.open('br') as f:
                        while True:
                                buffer = f.read(BLOCKSIZE)
                                
                                if len(buffer) == 0:
                                        break
                                
                                h.update(buffer)
                                
                                # return hash
                return h.hexdigest()
        
        def check_hash(self, f):
                with self.pool.get_resource() as c:
                        hash_in_db = c.execute(('select hash '
                                          'from file_hashes '
                                          'where path=? '
                                          'limit 1;'),
                                         (str(f.resolve()),)).fetchone()
                return hash_in_db is not None and self._hash(f) == hash_in_db[0]
        
        def update_hash(self, f):
                with self.pool.get_resource() as c:
                        c.execute(('insert or replace '
                                   'into file_hashes (path, hash) '
                                   'values (?,?);'),
                                  (str(f.resolve()),self._hash(f)))
                        c.commit()

def wait_prompt(s=None):
        if s is not None:
                print(s)
        print("Press Enter to Continue")
        input()

def run_LaTeX(file, cwd="."):
        try:
                cmd = ['compile_latex', file]
                p = subprocess.run(cmd,
                                   cwd=cwd,
                                   check=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT,
                                   encoding="utf-8")
        except subprocess.CalledProcessError as err:
                if err.stdout is not None:
                        print(err.stdout)
                if err.stderr is not None:
                        print(err.stderr)
                sys.exit(1)

def file_to_pdf_names(f):
        slides = f.parent / f"{f.stem}_slides.pdf"
        handout = f.parent / f"{f.stem}_handout.pdf"
        return (slides, handout)
                
def build_slides(f):
        global db
        
        with tempfile.TemporaryDirectory() as tmpdirname:
                working = Path(tmpdirname) / f"{f.stem}"

                # copy diectory contents is a quick and dirty way to not break any LaTeX includes
                shutil.copytree(f.parent, working, ignore=shutil.ignore_patterns('.*'))

                slides_latex = working / f.name
                slides_pdf = working / f"{f.stem}.pdf"
                finished_slides, finished_handout = file_to_pdf_names(f)

                base = slides_latex.read_text()
                sep = r"\documentclass{beamer}"
                try:
                        top, bottom = base.split(sep, maxsplit=1)
                except ValueError:
                        sep = r"\documentclass[handout]{beamer}"
                        top, bottom = base.split(sep, maxsplit=1)
                
                # build the full slides
                print(f"{f}: building slides")
                slides_latex.write_text(top + r"\documentclass{beamer}" + bottom)
                run_LaTeX(slides_latex, working)
                #print(f"Move {slides_pdf} to {finished_slides}")
                shutil.copy(slides_pdf, finished_slides)
                
                # build the handout
                print(f"{f}: building handout")
                slides_latex.write_text(top + r"\documentclass[handout]{beamer}" + bottom)
                run_LaTeX(slides_latex, working)
                #print(f"Move {slides_pdf} to {finished_handout}")
                shutil.copy(slides_pdf, finished_handout)
                
                # remove working version of pdf if it exists in the parent dir.
                old_pdf = f.parent / f"{f.stem}.pdf"
                if old_pdf.exists():
                        print(f"{old_pdf}: removing old working copy.")
                        old_pdf.unlink()
                
                # update hash
                print(f"{f}: updating hashes in db")
                db.update_hash(f)
                db.update_hash(finished_slides)
                db.update_hash(finished_handout)
                
# d must be a pathlib path. i.e. Path("...")
def build_all_slides(d, pattern):
        global db
        
        d=d.resolve()

        for p in sorted(d.iterdir(), key=natural_sort_key):
                if p.is_dir():
                        if p.name == ".auxiliary":
                                continue
                        build_all_slides(p, pattern)
                if p.is_file() and re.match(pattern, str(p.name)):
                        slides, handout = file_to_pdf_names(p)
                        
                        if db.check_hash(p) and db.check_hash(slides) and db.check_hash(handout):
                                print(f"{p} is up to date")
                        else:
                                build_slides(p)

db = HashDB('hashes.sqlite')
build_all_slides(Path("./CCC/MA205/OpenIntro/"), r"chapter\_.\_section\_.\.tex")
