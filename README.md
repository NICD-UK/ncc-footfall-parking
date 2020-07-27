# NCC Footfall & Parking

[![Dependabot badge](https://flat.badgen.net/dependabot/wbkd/webpack-starter?icon=dependabot)](https://dependabot.com/)

A responsive single page web application for visualizing car parking data and footfall on Northumberland Street in Newcastle.

## Development Environment

Development of the web application relies on Node.js. For downloads and installation instructions go to [https://nodejs.org/en/download/](https://nodejs.org/en/download/).

### Features

* ES6 Support via [babel](https://babeljs.io/) (v7)
* SASS Support via [sass-loader](https://github.com/jtangelder/sass-loader)
* Linting via [eslint-loader](https://github.com/MoOx/eslint-loader)

When you run `npm run build` we use the [mini-css-extract-plugin](https://github.com/webpack-contrib/mini-css-extract-plugin) to move the css to a separate file. The css file gets included in the head of the `index.html`.

### Installation

From the root level of the respository run the following command to install all the dependencies.

```bash
npm install
```

### Development

To start the development server with a file watch and hot deploy, run:

```bash
npm start
```

A new tab will open in your browser, but if it doesn't navigate to [http://localhost:8080](http://localhost:8080) to view the application. The page should reload automatically as the file watcher detects changes.

### Build

To run a local build to output only the static files, run:

```bash
npm run build
```

## Production

Deployment is handled via a GitHub actions workflow in `./.github/workflows`. The action runs the production build command and then copies the build directory to a static web enabled BlobStorage container on Azure account hosted by NICD.
