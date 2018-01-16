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
