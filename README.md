# Latex Line Length Linter

This is a tool, designed for pre-commit, that allows one to check the length of
all lines within the TeX file. This is meant to be run on TeX projects that use
a version control system, to ensure that diffs and commits are more limited in
scope and understandable.

Specific environments can be excluded from the linter to avoid false positives,
such as all equation environments. This is the case even for nested
environments.

To use this tool in your pre-commit configuration file, add the following:

```yaml
repos:
  - repo: https://github.com/Serene-Arc/latex_line_length_linter
    rev: 0.1
    hooks:
      - id: latexlinelengthlinter
        args: ["--max-length", "80",]
```

## Arguments

There are a number of options and arguments that can be used.

- `--max-length`
    - The maximum number of characters in the line that passes the linter
        - The default is 80 characters
- `--ignore-comments`
    - This flag determines whether the linter ignores any comments in the
      TeX file regarding line length
- `--ignore-envs`
    - The environments within which the linter will not check line length
    - Takes a CSV list
    - Can be specified multiple times
- `--ignore-envs-file`
    - Specifies a file containing environments to be ignored, one per line
    - Can be specified multiple times
- `--ignore-starred-envs`
    - Flag that determines whether starred versions of supplied environments
      ignore are also ignored automatically
- `--include-package-imports`
    - Check lines beginning with `\usepackage`
