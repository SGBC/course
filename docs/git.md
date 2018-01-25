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

!!! note
    what if my data is really big?
    Usually when you download data that is several gigabytes large, they will usually be compressed
    You can hop-on to the unix lesson - advanced concepts for more information

Let us look at the first few lines of our file:

```bash
head data/data_joined.csv
```

and at how many lines we have

```bash
wc -l data/data_joined.csv
# 34787 data/data_joined.csv
```

### Our first analysis script

we saw when we did the `head` command that all 10 first plots captured rodents.

!!! question
    Is rodent the only taxon that we have captured?

In our csv file, we can see that "taxa" is the 12th column.
We can print only that column using the `cut` command

```bash
cut -d ',' -f 12 data/data_joined.csv | head
```

We still pipe in in head because we do not want to print 34787 line to our screen.
Additionally `head` makes us notice that we still have the column header printed out

```bash
cut -d ',' -f 12 data/data_joined.csv | tail -n +2 | uniq -c
```

But while `uniq` is supposed to count all occurence of a word, it only count similar *adjacent* occurences.
Before counting, we need to sort our input:

```bash
cut -d ',' -f 12 data/data_joined.csv | tail -n +2 | sort | uniq -c
```

We see that although we caught a vast majority of rodents, we also caught reptiles, birds and rabbits!

Now that we have a working one-liner, let us put it into a script

```bash
nano scripts/taxa_count.sh
```

and write

```bash
# script that prints the count of species for csv files
echo "Dealing with $1"
cut -d ',' -f 12 "$1" | tail -n +2 | sort | uniq -c
```

!!! question
    How could you make your script so it can take another column as input?

### Keeping track of things

Now keep track of your script in git

```bash
git add scripts/taxa_count.sh
git commit -m 'added taxa_count'
```

as well as your gitignore

```bash
git add .gitignore
git commit -m 'added gitignore'
```

### Saving the result

```bash
bash scripts/taxa_count.sh data/data_joined.csv > results/taxa_count.txt
```

```bash
cat results/taxa_count.txt
```

```bash
git add results/taxa_count.txt
git commit -m 'added results of taxa_count.sh'
```
