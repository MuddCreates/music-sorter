# logan-salomon

Implementation of the algorithm described
in [the paper by Logan and Salomon][ls].

## Dependencies

* [Git](https://git-scm.com/) (to obtain and contribute to the code)
* [Python 3](https://www.python.org/) (to run the code)
* [pip](https://pypi.python.org/pypi/pip) (to install the
  dependencies)
* [Virtualenv](https://pypi.python.org/pypi/virtualenv) (to isolate
  the dependencies)

### Installation on macOS

Install the command-line tools:

    $ xcode-select --install

Install Homebrew:

    $ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

Install Python from Homebrew:

    $ brew install python3

Install Virtualenv:

    $ pip3 install virtualenv

## Development

Clone the repo:

    $ git clone https://github.com/MuddCreates/music-sorter.git
    $ cd music-sorter/logan-salomon

Create a virtualenv:

    $ virtualenv --python=python3 venv

Activate the virtualenv:

    $ source venv/bin/activate

Install the dependencies:

    $ pip install -r requirements.txt

Once you are done with the project, deactivate the virtualenv:

    $ deactivate

[ls]: https://github.com/MuddCreates/music-papers/blob/master/papers/LoganSalomon01-ContentBased.pdf
