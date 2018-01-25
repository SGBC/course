# Introduction to Git

Most of the introduction to Git material can be found at <https://software-carpentry.org>

Many thanks to them for existing!

## Useful resources

* [Link to the course material from software carpentry](http://swcarpentry.github.io/git-novice/)
* [reference of concepts and commands seen during the lesson](http://swcarpentry.github.io/git-novice/reference/)
* [The official git website](https://git-scm.com)
* [Comparison of popular git hosting services - Medium article](https://medium.com/flow-ci/github-vs-bitbucket-vs-gitlab-vs-coding-7cf2b43888a1)
* <https://choosealicense.com>

## Group Exercise

This exercise combines the knowledge you have acquired during the [unix](unix), [git](git) and [project organisation](project_org) lessons.

You have designed an experiment where you are studying the species and weight of animals caught in plots in a study area.
Data was collected by a third party a deposited in [figshare](https://figshare.com/articles/Portal_Project_Teaching_Database/1314459), a public database.

Our goals are to download and exploring the data, while keeping an organised project directory, that we will version control using git!

### Set up

First we go to our Desktop and create a project directory

```bash
cd ~/Desktop
mkdir 2018_animals
cd 2018_animals
```

and initialize 2018_animals as a git repository

```bash
git init
```

#### Project organization

As we saw on our project organization module, it is good practice to separate data, results and scripts.
Let us create those three directories

```bash
mkdir data results scripts
```

### Downloading the data

```bash
cd data
wget https://ndownloader.figshare.com/files/2292169
mv 2292169 survey_data.csv
chmod -w survey_data.csv
cd ..
```

Since the file is rather big and we do not *ever* want to modify it, we add a .gitignore and tell git to not track the `data/`
directory

```bash
nano .gitignore
```
