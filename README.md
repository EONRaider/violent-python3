# Python 3 "Violent Python" Source Code

Source code for the book "Violent Python" by TJ O'Connor. The code has been
 fully converted to Python 3, reformatted to comply with PEP8 standards and refactored to eliminate issues of dependency resolution involving deprecated modules.

## Usage
Simply make a new directory (DIR) for the project, create a new
 virtual environment or `venv` for it (recommended), clone this repository
  using `git clone` and install the requirements using `pip install`.

```
user@host:~$ mkdir DIR
user@host:~$ cd DIR
user@host:~/DIR$ python3 -m venv venv
user@host:~/DIR$ source venv/bin/activate
(venv) user@host:~/DIR$ git clone https://github.com/EONRaider/violent-python3
(venv) user@host:~/DIR$ pip install -r requirements.txt
```

## Notes

- The directories and files have been named in a way that they can be easily
 related to the content that is presented at each chapter.
## Refactoring

- The frequent use of string concatenation by the author has been replaced by
 string interpolation in order to allow greater readability and conform to a
  more modern standard.

## Contributing

As a matter of common sense, first try to discuss the change you wish to make to
this repository via an issue.

1. Ensure the modifications you wish to introduce actually lead to a pull
request. The change of one line or two should be requested through an issue
 instead.
2. If necessary, update the README.md file with details relative to changes to
 the project structure.
3. Make sure the commit messages that include the modifications follow a
 standard. If you don't know how to proceed, [HERE](https://chris.beams.io/posts/git-commit/)
  is a great reference on how to do it.
4. Your request will be reviewed as soon as possible (usually within one day).

