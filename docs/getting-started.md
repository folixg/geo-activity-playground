# Getting Started

This project is still in a very early stage, it will likely be a bit rough. Please feel free to contact me when you encounter issues.

## Installation

You can install it either system-wide or for your user. The user installation might be the best option, though it might require setting the `PATH` variable.

Install the project with the following:

```bash
pip install --user geo-activity-playground
```

Make sure that `~/.local/bin` is part of your `PATH` variable. Otherwise you will need to call the command line tool with `~/.local/bin/geo-activity-playground`.

Alternatively you can install it system-wide:

```bash
sudo pip install geo-activity-playground
```

Then you don't need to adjust the path.

## Set up your data

Create a directory somewhere where we can play around with this. For me I have it in `~/Dokumente/Karten/Playground`. The directory should not contain anything else.

Then you need to decide which data source you want to use. You can either use a directory with GPX and FIT files (also mixed). This is the right option if you collect the data yourself. Alternatively you can use Strava as a data source. You can either access it via the API or you a downloaded export. Setting up the API is a bit involved, the export is a bit easier but doesn't allow for incremental updates. We'll go through these options now.

### Directory source

Within your directory, create a directory called `Activities`. Then just put all your activities in there. You can create subdirectories and nest them as deep as you like. The program will do a recursive traversal of all files within that structure. Later on the directories might start to mean something, at the moment they don't.

### Strava checkout source

If you have requested all your data from Strava you will get a ZIP archive. Extract this into a subdirectory called `Strava Export`.

### Strava API source

TODO: Document how to set this up.

## Run the program

Once you have set it up and copied your data into the right place, you can start the webserver and play with it:

```bash
cd path/to/your/playground
geo-activity-playground --source directory serve
```

Then open <http://127.0.0.1:5000/> and you should be able to access the web interface.

At this point it will likely break. It would be great if you could [file those as an issue](https://github.com/martin-ueding/geo-activity-playground/issues) and also attach the traceback.

## Running from source

If you want to use the latest version, you can also clone the repository and launch from there:

```bash
git clone https://github.com/martin-ueding/geo-activity-playground.git
cd geo-activity-playground
poetry install
poetry run geo-activity-playground --basedir ~/path/to/your/playground --source directory serve
```

You might need to install Poetry via `pip install poetry` beforehand.