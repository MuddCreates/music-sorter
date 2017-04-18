# music-sorter

This is an exploratory project to investigate the task of sorting
music files by various metrics that might relate in some way to the
music's "mood".

We're focusing first on MIDI files, but hope to later tackle MP3s
(since that is what people generally have in their iTunes libraries).

With an appropriate sorting mechanism, this library could be used as
the kernel for a smart playlist generator which charts a smooth course
through the varying moods in one's music library. Somewhat
like [smarter-playlist][smarter-playlist], but even smarter!

## Dependencies

* You will need [Git][git] to clone the repository and to contribute
  changes. On macOS, you will be prompted to install
  the [command line tools][clt] the first time you use Git. After that
  Git will be available.

* The bulk of the code is written in [Clojure][clojure] using
  the [Leiningen][leiningen] build manager. As such, you will need to
  install Leiningen. On macOS, use [Homebrew][homebrew]:

      $ brew install leiningen

* To convert between MIDI and CSV formats, we use [MIDICSV][midicsv].
  On macOS, use [Homebrew][homebrew]:

      $ brew install midicsv

## Development

* Clone the repository:

      $ git clone https://github.com/MuddCreates/music-sorter.git

* To start a REPL for development, run:

      $ lein repl

* For a better development experience, install [CIDER][cider]
  for [Emacs][emacs] and run `M-x cider-jack-in` to launch a REPL
  inside Emacs.

[cider]: https://cider.readthedocs.io/
[clojure]: https://clojure.org/
[clt]: https://developer.apple.com/xcode/features/
[emacs]: https://www.gnu.org/software/emacs/
[git]: https://git-scm.com/
[homebrew]: https://brew.sh/
[leiningen]: https://leiningen.org/
[midicsv]: http://www.fourmilab.ch/webtools/midicsv/
[smarter-playlist]: https://github.com/raxod502/smarter-playlist
