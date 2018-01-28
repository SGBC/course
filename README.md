# Bioinformatics Course

Resources for our bioinformatics course

## Development

First install mkdocs (and the theme) in a virtual environment

```bash
virtualenv mkdocs_env
source mkdocs_env/bin/activate
pip install mkdocs
pip install mkdocs-cinder
```

Then clone the directory

```bash
git clone https://github.com/SGBC/course.git
cd course
git submodule update
```

The lessons are located in the `docs/` directory.
For the lessons under `docs/tutorials/` the development is happening at <https://github.com/HadrienG/tutorials>

For a live preview in your browser do

```bash
mkdocs serve &
```

## Deployment

From the (up-to-date) `master` branch, do

```bash
mkdocs gh-deploy
```

## Contributing

Please see how to contribute [here](CONTRIBUTING.md)

## License

This work is licensed under the Creative Commons Attribution 4.0 International License.
To view a copy of this license, visit http://creativecommons.org/licenses/by/4.0/ or send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.
