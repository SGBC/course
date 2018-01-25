# Command-line Blast

## Installing blast

While you should have installed blast during the [installing software](software) tutorial, you can copy/paste the code block below to reinstall it if needed

```bash
sudo apt install ncbi-blast+
```

## Getting data

We will download some cows and human proteins from RefSeq

```bash
wget ftp://ftp.ncbi.nih.gov/refseq/B_taurus/mRNA_Prot/cow.1.protein.faa.gz
wget ftp://ftp.ncbi.nih.gov/refseq/H_sapiens/mRNA_Prot/human.1.protein.faa.gz
```

Both these files are compressed. They are not `tar` archives, like we encountered earlier, but `gzip` files.
To uncompress:

```bash
gzip -d *.gz
```

Let us take a look at the human file

```bash
head human.1.protein.faa
```

Both files contain protein sequences in the [FASTA format](https://en.wikipedia.org/wiki/FASTA_format)

!!! question
    How many sequences do I have in each file?

The files are slightly too big for our first time blasting things at the command-line.
Let's downsize the cow file

```bash
head -6 cow.1.protein.faa > cow.small.faa
```

## Our first blast

Now we can blast these two cow sequences against the set of human sequences.

First we need to build a blast database with our human sequences

```bash
makeblastdb -in human.1.protein.faa -dbtype prot
ls
```

The `makeblastdb` produced a lot of extra files. Those files are indexes and necessary for blast to function.

Now we can run blast

```bash
blastp -query cow.small.faa -db human.1.protein.faa -out cow_vs_human_blast_results.txt
```

We can look at the results using `less`

```bash
less cow_vs_human_blast_results.txt
```

To know about the various options that we can use with blastp:

```bash
blastp -help
```

and for easier reading

```bash
blastp -help | less
```

!!! question
    How could I modify the previous blast command to filter the hits with an e-value of 1e-5

## Bigger dataset

Now that we succeeded using a small dataset of two proteins, let's try with a slightly bigger one.

```bash
head -199 cow.1.protein.faa > cow.medium.faa
```

!!! question
    How many protein sequences does `cow.medium.faa` contain?

We run blast again

```bash
blastp -query cow.medium.faa -db human.1.protein.faa \
    -out cow_vs_human_blast_results.tab -evalue 1e-5 \
    -outfmt 6 -max_target_seqs 1
```

!!! question
    What do `-outfmt` and `-max_target_seqs` do?
