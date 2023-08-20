# disney-comics-covers

This Python script scrapes data from [Inducks](https://inducks.org/) (the most important Disney comics database) to get the covers of all Disney publications of the country chosen by the user.

Each publication gets its own folder, inside which the covers of the individual issues are saved and named with a combination of the code of the publication and the number of the issue.

## Installation

You can install the tool by downloading the release binary (currently available only for Windows):

[disney-comics-covers.exe](https://github.com/giovanni-cutri/italian-disney-comics-covers/releases/download/first/disney-comics-covers.exe)

## Dependencies

All the necessary libraries are listed in the *requirements.txt* file.

You can install them by running:

```
pip install -r requirements.txt
```

## Usage

```
disney-comics-covers [country]
```

Replace *[country]* with the code of the country you want to download the publications of.

Type ```--help``` for further details.


## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/giovanni-cutri/italian-disney-comics-covers/blob/main/LICENSE) file for details.
