# Introduction to protein sequences and structures analysis


<hr>

**ToolBox that could be useful for protein sequences analysis:**

<http://expasy.org/>

<http://www.uniprot.org/>

<http://www.ebiokit.eu/>

<http://npsa-pbil.ibcp.fr>

<http://blast.ncbi.nlm.nih.gov/Blast.cgi>

[https://www.ebi.ac.uk/interpro](https://www.ebi.ac.uk/interpro/search/sequence-search)

<http://www.rcsb.org/pdb>

<hr>


After cloning and sequencing of coding DNA, the sequence of the X
protein had been determined. The sequence of X is given here:

*LAAVSVDCSEYPKPACTLEYRPLCGSDNKTYGNKCNFCNAVVESNGTLTLSHFGKC*

In normal conditions, this X protein is expressed but we have no idea
about it function. The goal of this practical work is to collect the
maximum of information about structure and function of the X protein.

## I - Search Patterns, Profiles

A way to identify the function of X is to look if it contains signatures
(pattern) of a function or a protein family.

2 options:

<http://prosite.expasy.org/scanprosite/>

[NPS@](http://npsa-pbil.ibcp.fr) and follow the link "ProScan: scan a
sequence for sites/signatures against PROSITE database" (activate:
Include documentation in result file).

!!! question
    1.  Which signature(s) could you identify? Which specific features in
        this protein?

    2.  Try to change the parameters and comment the results.

!!! note
    InterPro gives a summary of several methods. You can find it at the
    [EBI](http://www.ebi.ac.uk/interpro/index.html).

Keep the signatures that could attest the function in your notepad.

- What do you think about the function of X?

## II - Search homolog proteins with BLAST

1.  Go to the [NCBI BLAST](http://blast.ncbi.nlm.nih.gov/Blast.cgi) page

2.  Choose the Protein Blast (blastp)

3.  Paste your sequence

4.  Select the Swissprot database

!!! question
    Did you identify homologs? What are their function(s)?

## III - Multiple sequences alignment

1.  Select several homolog sequences from the Blast results.

2.  Perform a multiple sequence alignment (MSA) of these sequence using
    Clustal Omega for example

3.  Try other MSA tools (for example Tcoffee and Muscle)

!!! question
    Do you observe differences between the results obtained from
    different algorithms?

    What can you observe in these MSAs?

**Info**: You could also retrieve the selected sequences in Fasta format
and perform MSAs elsewhere

Clustal Omega and Muscle: available in Seaview alignment viewer

Tcoffee: <http://tcoffee.vital-it.ch/apps/tcoffee/index.html>

Other tools: <http://expasy.org/genomics/sequence_alignment>

## IV - The Y protein

Another experiment had shown that the X protein was interacting
specifically with another protein: Y.

After purification of the active Y protein, from the complex, a partial
sequence of Y was obtained (by protein extremity sequencing).

The corresponding peptide could be:

*ISGGD* or *ISGGN*

### 1. Identification of the Y sequence using PROSITE patterns

1.  Design the pattern (regular expression) corresponding to these
    peptides.

2.  Search the sequences containing this pattern in SwissProt using
    [PATTERN SEARCH](http://hits.isb-sib.ch/cgi-bin/pattern_search) at
    SIB or
    [PATTINPROT](http://npsa-pbil.ibcp.fr/cgi-bin/npsa_automat.pl?page=/NPSA/npsa_pattinprot.html)
    at NPS@.

If needed, use the help to design your pattern.

!!! question
    How many results do you get? How can you identify the right one?

Once the Y protein sequence identified, copy the FASTA sequence in your
notepad.

### 2. Composition analysis

After purification of the Y active protein, the amino-acid composition
has been determined (% of each aa in the protein) and is given in the
following table:

|   |      |   |       |   |      |   |      |   |   |
|:--|:-----|:--|:------|:--|:-----|:--|:-----|:--|:--|
| **A** | 8.11 | **F** | 2.70  | **L** | 3.78 | **R** | 4.32 | **X** | 0 |
| **B** | 0 | **G** | 17.30  | **M** | 1.08 | **S** | 11.89 | **Y** | 5.41 |
| **C** | 2.16 | **H** | 1.08  | **N** | 5.41 | **T** | 15.14 | **Z** | 0 |
| **D** | 3.78 | **I** | 3.78  | **P** | 2.70 | **V** | 7.57 |
| **E** | 1.08 | **K** | 0.54  | **Q** | 1.08 | **W** | 1.08 |



1.  Compute the composition of the sequence that you retrieve. Use
    [PROTPARAM](http://web.expasy.org/protparam/) or the tool
    'Amino-acid composition' at [NPS@](http://npsa-pbil.ibcp.fr)

2.  Compare this computed composition with the composition of Y
    experimentally determined.

!!! question
    Do you observe differences? Explain.

### 3. Search pattern in Y

Once the correct sequence of Y obtained, keep it in your notepad, you
will need it for the following analyses.

!!! question
    Identify the signatures (motifs, Pfam profiles) of Y using PROSCAN
    and/or Interpro.

### 4. Identification of homologs to Y

1.  Use NCBI BLASTP or NPS@
    [BLASTP](https://npsa-prabi.ibcp.fr/cgi-bin/npsa_automat.pl?page=/NPSA/npsa_blast.html)
    against SwissProt database to search sequences similar to Y.

2.  Use PSI-BLAST (with SwissProt) to see if you can detect more distant
    sequences.

3.  Select sequences from BLAST and/or PSI-BLAST results to perform a
    multiple sequence alignment.

!!! question
    1. Did you observe difference in the results of BLAST and PSI-BLAST?
    Comment.
    2. Propose a strategy to retrieve all the proteins having the same
    catalytic activity as Y protein.

## V - Secondary structure prediction for X and Y

1.  Go to the [consensus secondary structure
    prediction](http://npsa-pbil.ibcp.fr/cgi-bin/npsa_automat.pl?page=/NPSA/npsa_seccons.html)
    page at NPS@.

2.  Analyze the secondary structure of the protein Y. Include secondary
    structure predictions by methods (DPM, GOR1, PREDATOR, SIMPA96).

!!! question
    1. Conclude on the organization of secondary structures.
    2. Perform the same analysis for X protein.

## VI - Comparison with solved structures

### 1. The Z protein

The structure of a protein Z has just been published. The sequence of
protein Z is shown below:

*IAGGEAITTGGSRCSLGFNVSVNGVAHALTAGHCTNISASWSIGTRTGTSFPNNDYGIIRHSNPAAANGRVYLYNGSYQD*

*ITTAGNAFVGQAVQRSGSTTGLRSGSVTGLNATVNYGSSGIVYGMIQTNVCAQPGDSGGSLFAGSTALGLTSGGSGNCRT*

*GGTTFYQPVTEALSAYGATVL*

!!! question
    Could you use this information for the study of protein Y? Make your
    own analysis.

### 2. Find the correct structures

1.  Download and install [Deep-View -
    SwissPDBViewer](http://spdbv.vital-it.ch/disclaim.html). You can
    find the tutorial and user guide of DeepView
    [here](http://spdbv.vital-it.ch/).

2.  Download to the archive [PDB\_files\_part6.zip]() and unzip it.

3.  You might find 8 PDB files in the directory.

4.  Open them with DeepView.

5.  Display the secondary structure representation mode (see part
    VII-A-5 and/or the user guide).

!!! question
    Try to identify the structures corresponding to X and Y proteins.

## VII - Tridimensional protein structure: Play with 3D structures using SwissPDBViewer (DeepView)

1.  Go to the [Protein Data Bank](http://www.rcsb.org/pdb/home/home.do)

2.  Search and download the following PDB files: 1CRN, 1LDM.

You will visualize these protein structures using DeepView

### A - Analyze protein structures with DeepView

#### 1. Load a 3D structure

File =\> Open

Choose the 1CRN.pdb file that you have downloaded from the PDB.

#### 2. Visualize the number of chains

Is it only the protein or can we find ligands? Is it a monomer or a
polymer?

#### 3. Visualize the general shape

Try to get the actual space taken by the molecule. You need to use the
control panel and use the ':v' column to activate the space-filling
spheres representation (+ menu Display \> Render in solid 3D).

Test also the Slab mode to visualize the space within the molecule:
Display \> Slab

#### 4. Display a distance between 2 atoms, angle between 3 atoms

Use the graphical panel. You can now measure the real dimensions of your
protein

#### 5. Visualize secondary structure elements

In the control panel, activate "ribbon" (rbn). You can also color the
molecule by secondary structures.

#### 6. Visualize ligands (if there is any)

Select and color them. You could also remove the rest, or better, have a
look at the residues that are around those ligands (radius function in
the graphical panel).

#### 7. Analysis of other protein structures

The teacher will give PDB codes of other structures to analyze. Choose
DeepView or Rasmol/Jmol to do so, that is up to you!

### B - Optional: if you want to use RasMol/Jmol

#### 1. Load a 3D structure

File =\> Open

Choose the 1CRN.pdb file that you have downloaded from the PDB.

<hr>
**HELP SECTION FOR RASMOL**

Molecule main moves with the mouse:

Left button: XY rotation

Left button + Shift: Zoom

Right button: Translation

Right button + Shift: Z rotation

Keep the graphical window and the command (text) window on your screen
(\> ​​is a command to type in the text window).

For each selection (SELECT command), the number of selected atoms
appears in the text window. After you can apply an action to be able to
visualize the elements that you have selected (e.g. COLOR GREEN).

Ctrl+Z does not exist in Rasmol. You can type the command RESET.

If you want to come back in a standard representation of your molecule,
type:
```
SELECT ALL

CPK
```
=\> This will reset previous actions on representation modes (but keep
colors). CPK: space-filling spheres representation

COLOR CPK: colors \'atom\' objects by the atom (element) type

<hr>

**Help for Jmol:**

A lot of "actions" (color, selection...) are available by right clicking
on the main screen

To get the terminal window: menu File \> Console

<hr>

#### 2. Example: visualize the disulfide bonds

Type in the text window

```
SELECT CYS
```

The text window \"answers\" 36 atoms selected (selected cysteine's
atoms)
```
COLOR GREEN
```
- Observe the graphics window.
```
RESTRICT CYS
```
- Compare with the SELECT command

Highlight the disulfide bonds:
```
SSBONDS

COLOR YELLOW

SSBONDS 75

COLOR CPK
```
#### 3. Visualize secondary structure elements
```
SSBONDS OFF (remove SS bonds)

SELECT ALL

CARTOONS

COLOR STRUCTURE
```
#### 4. Display a distance between 2 atoms

Activate the compute distance mode typing:
```
SET PICKING DISTANCE
```
Then, you can click the 2 atoms.

You can display angle values typing:
```
SET PICKING ANGLE
```
Then pick the 3 atoms

5. Other useful commands
------------------------
```
SHOW SEQUENCE

SHOW INFO

SELECT ALL

CPK ON

RESTRICT NOT HOH (remove water molecules)

CPK OFF

HBONDS

SELECT CYCLIC AND NOT PRO

STEREO ON
```
Try them to better understand the Rasmol command language.

6. Store a command script and reload it
---------------------------------------

Repeat the actions described in paragraph 2
```
WRITE SCRIPT MY_SCRIPT.SC
```
Exit the software (File =\> Quit)

Restart the software
```
SOURCE MY_SCRIPT.SC
```
7. Select the atoms in a sphere
-------------------------------

File =\> Close

Load the file 1LDM.pdb

Discover and analyze the molecule (number of channels, ligands, *etc*.)

To select all the atoms in a 3Å radius sphere centered on a ligand
(*e.g.* NAD)
```
SELECT ALL

COLOR CHAIN

SELECT WITHIN (3.0, NAD)

CPK
```
Option =\> Slab Mode (comment).
