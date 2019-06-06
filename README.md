# Description 
Creates a pdf/epub out of [https://rework.withgoogle.com](https://rework.withgoogle.com)

# Releases

You can find the last release of the pdf/epub [here](https://github.com/daniperez/rework/releases).

# Disclaimer

The content processed by this tool belongs to Google Inc. and it is governed by [these terms](https://rework.withgoogle.com/terms/).

I am not affiliated nor endorsed by Google Inc.

The tool itself is bound to [these license](LICENSE.md) (MIT).

# Compile the book by yourself

## Dependencies

See `requirements.txt` for Python's dependencies. On addition to that, you will
need:
- Pandoc
- Sane latex environment
- Some latex fonts (in Fedora: `yum install texlive-collection-fontsextra texlive-collection-fontsrecommended`)

## Compilation

The compilation of the book has 3 phases:

1. Scrapping [rework.withgoogle.com](rework.withgoogle.com), save as JSON.
2. Convert JSON to Markdown
3. Convert Markdown to a human readable format (e.g. pdf, epub)

In the shell, that translates to:

```shell
./bin/scrap | ./bin/json2markdown  | ./bin/markdown2humanreadable
```

or the same:

```shell
./bin/main
```

The first command line is more convenient if you are debugging or changing
things because you have the opportunity to skip any of the steps if you save
the intermediate output to a file.
