We're migrating the blog from Jekyll to Pelican because Jekyll requires Ruby, while Pelican is based on Python.

### Requirements
- `sassc` - the sass compiler which builds `.css` files from `.scss`.
- `pelican==4.8.0` or above
- `markdown`
- `beautifulsoup4`

### Serving
To serve locally, clone the repo, run `make html` which populates the `docs` folder. Then run `make serve` to serve it.

Alternatively, run `make devserver` which will both serve and regenerate the blog whenever a change is detected.

### File structure
The posts are in `content`. Pages are in `content/pages`. Theme templates are in `themes/minima`.

### Publishing
The `html` files are stored in `docs`. Github-Pages serves them from there.
