## Project organization and management

Most of the the project organization material can be found at <https://software-carpentry.org> and <http://www.datacarpentry.org>

Many thanks to them for existing!

### Structure or architecture of a data science project


Some good practice when you will organise your project directory on the server, on the cloud or any other machine where you will compute:

> Create 3 or 4 different directories within you project directory (use `mkdir`):
>
> `data/` for keeping the raw data
>
> `results/` for all the outputs from the multiple analyses that you will perform
>
> `docs/` for all the notes written about the analyses carried out (ex: `history > 20180125.logs` for the commands executed today)
>
> `scripts/` for all the scripts that you will use to produce the results
>


!!! note
    You should always have the raw data in (at least) one place and not modify them

### More about data structure and metadata

* direct link to the tutorial used fo the lesson: [Shell genomics: project organisation](http://www.datacarpentry.org/shell-genomics/06-organization/)

* good practice for the structure of data and metadata of a genomics project: [Organisation of genomics project](http://www.datacarpentry.org/organization-genomics/)

* Some extra material: [Spreadsheet ecology lesson](http://www.datacarpentry.org/spreadsheet-ecology-lesson/)

## Exercise

This exercise combines the knowledge you have acquired during the [unix](unix), [git](git) and [project organisation](project_org) lessons.

You have designed an experiment where you are studying the species and weight of animals caught in plots in a study area.
Data was collected by a third party a deposited in [figshare](https://figshare.com/articles/Portal_Project_Teaching_Database/1314459), a public database.

Our goals are to download and exploring the data, while keeping an organised project directory that we will version control using git!

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

As we saw during the project organization tutorial, it is good practice to separate data, results and scripts.
Let us create those three directories

```bash
mkdir data results scripts
```

### Downloading the data

First we go to our `data` directory

```bash
cd data
```

then we download our data file and give it a more appropriate name

```bash
wget https://ndownloader.figshare.com/files/2292169
mv 2292169 survey_data.csv
```

Since we'll never modify our raw data file (or at least we *do not want to!*) it is safer to remove the writing permissions

```bash
chmod -w survey_data.csv
```

Additionally since we are now unable to modify it, we do not want to track it in our git repository.
We add a .gitignore and tell git to not track the `data/` directory

```bash
nano .gitignore
```

!!! note
    what if my data is really big?
    Usually when you download data that is several gigabytes large, they will usually be compressed.
    You learnt about compression during the [installing software](software) lesson.

Let us look at the first few lines of our file:

```bash
head data/data_joined.csv
```

Our data file is a `.csv` file, that is a file where fields are separated by commas `,`.
Each row represent an animal that was caught in a plot, and each column contains information about that animal.

!!! question
    How many animals do we have?

```bash
wc -l data/data_joined.csv
# 34787 data/data_joined.csv
```

It seems that our dataset contains 34787 lines.
Since each line is an animals, we caught a grand total of 34787 animals over the course of our study.

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

But while `uniq` is supposed to count all occurrence of a word, it only count similar *adjacent* occurrences.
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
cut -d ',' -f 12 "$1" | tail -n +2 | sort | uniq -c
```

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

### Improving our script

We would also like to know the distribution of the numbers of animals caught in plots each year.
The year is the 4th column in our dataset and our script, in its current state, always selects the 12th columns of a file.

We can change our script to make it flexible so that the user can chose which columns they wishes to work on.

```bash
nano scripts/taxa_count.sh
```

```bash
# script that prints the count of occurrence in one column for csv files
cut -d ',' -f "$2" "$1" | tail -n +2 | sort | uniq -c
```

Now it doesn't make much sense to have it named `taxa_count.sh`

```bash
mv scripts/taxa_count.sh scripts/column_count.sh
```

and let us not forget to keep track of our changes in git!

```bash
git add -A
git commit -m 'made script more flexible about which column to cut on'
```

!!! question
    which year did we catch the most animals?
    try to answer programmatically.

!!! question
    save the sorted output to a file in the `results` directory and keep track of it in git.

### Investigating further

We'd like to refine our animal count and knowing how many animals of each taxon were captured every year

we can use `cut` on several columns like this:

```bash
cut -d ',' -f 4,12 "data/data_joined.csv" | tail -n +2 | sort | uniq -c
```

Now that we are ahhpy with our one-liner, let us save it in a script:

```bash
nano scripts/taxa_per_year.sh
```

then save the output to `results/taxa_per_year.txt`

```
bash scripts/taxa_per_year.sh > results/taxa_per_year.txt
```

!!! question
    Which year was the first reptile captured?

The next step would be to refine our analysis by year. We will save one individual output for each year count

#### The seq command

To perform what we want to do, we need to be able to loop over the years.
The `seq` command can help us with that.

First we try

```bash
seq 1 10
```

then

```bash
seq 1997 2002
```

and what about the span of years we are interested in?

```bash
seq 1977 2002
```

Great! So now does it work with a for loop?

```bash
for year in $(seq 1977 2002)
    do
        echo $year
    done
```

It does!

Before doing our analysis on each year, we still have to figure out how to do it on one year.

```bash
grep 1998 results/taxa_per_year.txt
```

"Grepping" the year seems to work.
Now we need to save it into a file containing the year

First let's create a directory where to store our results

```bash
mkdir results/years
```

and we try to redirect our yearly count into a file

```bash
grep 1998 results/taxa_per_year.txt > results/years/1998-count.txt
```

```
bash
cat results/years/1998-count.txt
```

It seems to have worked.
Now with the loop

```bash
for year in $(seq 1977 2002)
    do
        grep $year results/taxa_per_year.txt > results/years/$year-count.txt
    done
```

```bash
ls results/years
```

!!! question
    Put your loop in a script, and commit everything with `git`
