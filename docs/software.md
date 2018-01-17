# Installing software

Bioinformatics is a relatively new (It's younger that Erik!) and fast-progressing field.
Therefore new software as well as new versions of existing software are released on a regular basis.

During this course as well as during your future career as a bioinformatician ( ;-) ) you will be confronted quite often to the installation of new software on UNIX platforms (i.e. the server you are using at the moment)

## Compiled and Interpreted languages

Programming languages in the bioinformatics world - and in general - can be separated in two categories: *intepreted* languages, and *compiled* languages. While with *interpreted* languages you write scripts, and execute them (as we saw with the `bash` scripts during the UNIX lesson) it is different for compiled languages: an extra step is required

### Compilation

As from [Wikipedia](https://en.wikipedia.org/wiki/Compilation), compilation is the translation of source code into object code by a compiler.

That's right.
The extra step required by compiled languages is translating the source code, that is the lines of code the programmer(s) wrote into a language that your computer understand better, usually binary (1s and 0s).

The big advantage of compiled languages is that they are much faster than interpreted languages.
However, programming in them is usually slower and more difficult than in interpreted languages. Using them or not for a software project is a trade-off between development-time, and how much faster your software could run if it was programmed using a compiled language.

The most popular compiled language is the C programming language, which Linux is mainly written in.

## Package Managers

All modern linux distributions come with a [package manager](https://en.wikipedia.org/wiki/Package_manager), i.e. a tool that automates installation of software.
In most cases the software manager download already compiled binaries and installs them in your system. We'll see how it works in a moment

Let us install our first package!

The package manager for [Ubuntu](https://www.ubuntu.com) is called [APT](https://en.wikipedia.org/wiki/APT_(Debian)). Like most package managers, the syntax will look like this:

```
[package_manager] [action] [package_name]
```

We'll use apt to install a local version of [ncbi-blast](https://blast.ncbi.nlm.nih.gov/Blast.cgi?PROGRAM=) that you've use previously.

First we search if the package is available

```bash
apt search ncbi-blast
```

There seems to be two versions of it. The legacy version is probably outdated, so let us investigate the other one

```bash
apt show ncbi-blast+
```

It seems to be what we are looking for, we install it with:

```bash
apt install ncbi-blast+
```

!!! question
    Did it work? What could have been wrong?


You should have gotten an error message asking if you are `root`.  
The user `root` is the most powerful user in a linux system and usually has extra rights that a regular user does not have.  
To install software in the default system location with apt, you have to have special permissions.  
We can "borrow" those permissions from `root` by prefixing our command with `sudo`.

```bash
sudo apt install ncbi-blast+
```

Now if you execute

```bash
blastn -help
```

it should print the (rather long) error message of the blastn command.

!!! question
    Why does blast has different executable?  
    What is the difference between blastn and blastp?  

## Downloading and unpacking

Although most popular software can be installed with your distribution's package manager, sometimes (especially in some fast-growing areas of bioinformatics) the software you want isn't available through a package manager.

We'll install [spades](http://cab.spbu.ru/software/spades/), a popular genome assembly tool. Let's imagine it is not available in the apt sources. We'd have to:

- download the source code
- compile the software
- move it at the right place on our system

Which is quite cumbersome, especially the compilation.
Luckily, it is fairly common for developers to make linux binaries - that is compiled version of the software - already available for download.

First let us create a directory for all our future installs:

```bash
mkdir -p ~/install
cd ~/install
```

The spades binaries are available on their website, <http://cab.spbu.ru/software/spades/>

Download them with

```bash
wget http://cab.spbu.ru/files/release3.11.1/SPAdes-3.11.1-Linux.tar.gz
```

and uncompress

```bash
tar xvf SPAdes-3.11.1-Linux.tar.gz
```

```bash
cd SPAdes-3.11.1-Linux/bin/
```

and now if we execute `spades.py`

```bash
./spades.py
```

we get the help of the spades assembler!

A minor inconvenience is that right now

```bash
pwd
# /home/hadrien/install/SPAdes-3.11.1-Linux/bin
```

we have to always go to this directory to run `spades.py`, or call the software with the full path.
We'd like to be able to execute `spades` from anywhere, like we do with `ls` and `cd`.

In most linux distributions, which directory can contain software that are executed from anywhere is defined by an environment variable: `$PATH`

Let us take a look:

```bash
echo $PATH
# /home/hadrien/bin:/home/hadrien/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
```

To make `spades.py` available from anywhere we have to put it in one of the above locations.

!!! note
    When `apt` installs software it usually places it in `/usr/bin`, which requires administration privileges.
    This is why we needed `sudo` for installing packages earlier.

```bash
mkdir -p ~/.local/bin
mv * ~/.local/bin/
```

Et voilà! Now you can execute `spades.py` from anywhere!

## Installing from source

For some bioinformatics software, binaries are not available. In that case you have to download the source code, and compile it yourself for your system.

This is the case of [samtools](http://www.htslib.org) per example. [samtools](http://www.htslib.org) is one of the most popular bioinformatics software and allows you to deal with `bam` and `sam` files (more about that later)

We'll need a few things to be able to compile samtools, notably [make](https://www.gnu.org/software/make/) and a C compiler, [gcc](https://www.gnu.org/software/gcc/)

```bash
sudo apt install make gcc
```

samtools also need some libraries that are not installed by default on an ubuntu system.

```
sudo apt install libncurses5-dev libbz2-dev liblzma-dev libcurl4-gnutls-dev
```

Now we can download and unpack the source code:

```bash
wget https://github.com/samtools/samtools/releases/download/1.6/samtools-1.6.tar.bz2
tar xvf samtools-1.6.tar.bz2
cd samtools-1.6
```

Compiling software written in C usually follows the same 3 steps.

1. `./configure` to configure the compilation options to our machine architecture
2. we run `make` to compile the software
3. we run `make install` to move the compiled binaries into a location in the `$PATH`

```bash
./configure
make
make install
```

!!! warning
    Did `make install` succeed? Why not?

As we saw before, we need `sudo` to install packages to system locations with `apt`.
`make install` follows the same principle and tries by default to install software in `/usr/bin`

We can change that default behavior by passing options to `configure`, but first we have to clean our installation:

```bash
make clean
```

than we can run configure, make and make install again

```bash
./configure --prefix=/home/$(whoami)/.local/
make
make install
```

```bash
samtools
```

!!! question
    The bwa source code is available on github, a popular code sharing platform (more on this in the git lesson!).
    Navigate to <https://github.com/lh3/bwa> then in release copy the link behind `bwa-0.7.17.tar.bz2`  
    - Install bwa!
