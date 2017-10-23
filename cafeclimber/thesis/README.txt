----------------------------------------------------------
----------------------------------------------------------

TAMU LaTeX Undergraduate Research Scholars Program Thesis Tamplate

Template by Sean Zachary Roberson
Updated by Parasol Laboratory January 2017

----------------------------------------------------------
----------------------------------------------------------

CONTENTS

I. About
II. Changes and Fixes
III. Usage of This Template
IV. Compiling Your Document
V. Getting Help

----------------------------------------------------------
----------------------------------------------------------
I. About
----------------------------------------------------------
----------------------------------------------------------

This file package contains a template for creating a
thesis or dissertation for submission at Texas A&M
University.  This LaTeX template is designed for use
by students in technical areas such as mathematics,
physics, engineering, statistics, and computer
science. If you are not a student in one of these
areas (or generally, not a STEM student), this
is not the template to use.  This LaTeX template
is best used for theses and dissertations that contain
many equations and mathematical formulas.

----------------------------------------------------------
----------------------------------------------------------
II. Changes and Fixes
----------------------------------------------------------
----------------------------------------------------------

- Added appropriate commands for the title, program,
  advisor, and department. Commands needed for the
  graduate thesis were removed.

- Modified the introduction of the template to be more
  accurate.

- Reformatted the title page to follow URS formatting
  rules.

- Reformatted the abstract page to follow URS formatting
  rules.

- Condensed the appendix's to one page.

- Changed the section file names to chapter to be more
  concise naming convention.

- Added a makefile to compile the document. 

----------------------------------------------------------
----------------------------------------------------------
III. Usage of This Template
----------------------------------------------------------
----------------------------------------------------------

In order to effectively use this template, a TeX editor
is required.  Suggested editors include:

- TeXstudio, available at http://www.texstudio.org/

- TeXworks, available at https://www.tug.org/texworks/

Of course, there are many other editors available. You
will also need a TeX distribution, available at

- https://www.tug.org/protext/ for Windows

- https://tug.org/mactex/ for Mac


To begin editing the template, open, in your editor, the
file "thesis.tex." This is the main file for
the template and it contains references to the other parts
of the document. In order to compile (see below), YOU MUST
COMPILE YOUR DOCUMENT FROM THIS MAIN FILE. Compiling in
the other files of the package will produce an error.
While in this main file, take care in not editing the
block containing the geometry package. This package
sets the margins to the required measurements set by the
Thesis Manual.

All of the required files are in the directory \data after
extraction. Extra files, such as those referring to a new
chapter, section, or appendix may be added as needed; just
be sure to include these files in the main TeX file via
the command \include{data/NewFile}, where NewFile is the
name of the file.

You may require figures in your document. If this is the
case, you will need the graphicx package. This package
is already loded in the main file. You can delete the
files in the folder "graphic" and place your own there.

The command \includegraphics is used to insert pictures.
In the template, these are placed within the figure
environment (\begin{figure} ... \end{figure}). Refer
to the template and the LaTeX Wikibook for more
information.

The footnote package can be removed - it was included
to show an example of including a footnote within a
table. This package does include refinements to the
existing footnote commands. See the package's
documentation on CTAN for more details.

----------------------------------------------------------
----------------------------------------------------------
IV. Compiling Your Document
----------------------------------------------------------
----------------------------------------------------------

TeXworks and TeXstudio can be used to compile your document
into a pdf. To correctly compile your document, you must
make sure the typeset command is either pdfLaTeX or XeLaTeX.
For TeXwork, from the Tools menu, by selecting Commands
and then selecting the appropriate option. For teXstudio,
from the Typeset menu, select the appropriate option. If
you are using another LaTeX editor refer to its reference
for how to change the compiling command.

If you have a BibTeX database created using JabRef or a
similar database editor, you can add your references by
first compiling with latex, then with BibTeX, and twice
more with latex. This ensures that your references are
added to the final document.

It is reccomended that you do not name your reference
database something other than myReference.bib, as that
is what the source code will point to. The file
"myReference.bib" is located in the data folder. If you
do name your reference database something other than
myReference may sure you change the filename in
thesis.tex line 156.

----------------------------------------------------------
----------------------------------------------------------
V. Getting Help
----------------------------------------------------------
----------------------------------------------------------

Google should have enough information for you to figure
out how to solve any problem you are having. Here are some
useful websites:

http://en.wikibooks.org/wiki/LaTeX

http://www.sharelatex.com/learn/Main_Page

http://www.cs.princeton.edu/courses/archive/spr10/cos433/Latex/latex-guide.pdf

http://www.latex-tutorial.com/tutorials/

http://tobi.oetiker.ch/lshort/lshort.pdf

ftp://ftp.ams.org/pub/tex/doc/amsmath/short-math-guide.pdf
