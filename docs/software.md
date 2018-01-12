# Installing software

Bioinformatics is a relatively new (It's younger that Erik!) and fast-progressing field.
Therefore new software as well as new versions of existing software are released on a regular basis.

During this course as well as during your future career as a bioinformatician ( );-) ) you will be confronted quite often to the installation of new software on UNIX platforms (i.e. the server you are using at the moment)

## Compiled and Interpreted languages

Programming languages in the bioinformatics world - and in general - can be separated in two categories: *intepreted* languages, and *compiled* languages. While with *interpreted* languages you write scripts, and execute them (as we saw with the `bash` scripts during the UNIX lesson) it is different for compiled languages: an extra step is required

### Compilation

As from [Wikipedia](https://en.wikipedia.org/wiki/Compilation), compilation is the translation of source code into object code by a compiler.

That's right. The extra step required by compiled languages is translating the source code, that is the lines of code the programmer(s) wrote into a language that your computer understand better, usually binary (1s and 0s).

The big advantage of compiled languages is that they are much faster than interpreted languages. However, programming in them is usually slower and more difficult than in interpreted languages. Using them or not for a software project is a trade-off between development-time, and how much faster your software could run if it was programmed using a compiled language.

The most popular compiled language is the C programming language, which Linux is mainly written in.
