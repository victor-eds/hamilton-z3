# hamilton-z3

Given a graph, using Z3, this program states whether there exists a
Hamiltonian graph in it.

## Install

Using [pipenv](https://docs.pipenv.org/), simply run `pipenv install`. This will
install dependencies. Then, use `pipenv shell` to enter the virtual environment.

## Run

Once in the virtual environment, you can run the program with:

```bash
usage: python . [-h] [--nodes N] [--probability P] [--verbose] [--draw] [--drawresult] [filename]
```

Use `-h` flag to see the meaning of each arguments.

## JSON format

The input to the program is the path to a file containing a graph in JSON
format, consisting on an object with two attributes: `nodes` and `edges`,
containing the list of nodes and the list of edges, respectively. An edge
is a list with two arguments. E.g.:

```json
{
    "nodes": [1, 2, 3, 4, 5],
    "edges": [[1, 2], [1, 3], [2, 3], [3, 4], [3, 5], [4, 5]]
}
```

### Examples

Examples of the JSON input format are includes in the [examples](examples)
directory.
