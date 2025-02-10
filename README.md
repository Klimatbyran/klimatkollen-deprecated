## Klimatkollen

This is the official source code for [klimatkollen.se](https://klimatkollen.se).

## Free our climate data!

Klimatkollen is an open source and citizen-driven climate data platform aimed at visualising local climate data in Sweden.

<b>The problem:</b> Sweden’s 290 cities and municipalities are not slashing carbon emissions fast enough to be in line with the Paris Agreement. Climate data that can help us is often locked behind paywalls, or sits in complex government databases. If we can’t clearly see how much CO<sub>2</sub> is being emitted, from which sources and how quickly we need to decarbonise – we can’t create a public opinion strong enough to change the course of our future. This needs to change.

That’s why we’re building a data-driven movement of climate-savvy developers to help us find and visualise climate data for the public. Climb aboard!

<b>Join our [Discord](https://discord.gg/N5P64QPQ6v)</b> and set our climate data free!

#Klimatkollen #FreeClimateData

## Building and running locally

If you're starting from scratch, and working with GitHub, NodeJS and so on is new to you, read [doc/getting-started.md](doc/getting-started.md).

We use next.js and Typescript and it's pretty straightforward to get started. After cloning the repo run:

    npm ci
    npm run dev

This opens up a webserver on http://localhost:3000. Just edit the code and see the live refresh.

The project can also be run with `docker compose` with `--watch` (v2.22.0+) for live refresh:

    docker compose up --build --watch


# Data overview

In very general terms, Klimatkollen presents:

- Detailed information about Swedish municipalities' emissions...
- ...and their remaining emission budget based on the Paris Agreement.
- Other key point indicators for sustainability transition, such as electric car charger density.
- Contextual information to help understand the significance of the above.

# File overview

The toplevel directory contains a lot of files and folders. You can just ignore most of them. Take note of:

- `README.md` - this document.
- `data`: Our data processing pipeline, written in Python. This can more or less be used/edited independently of the rest of the repository. See `data/README.md`.
  - `data/facts`: Copies of source datasets.
- `doc`: Documentation and guides, they might answer many questions.
  - `doc/getting-started.md`: Detailed setup instructions for the web project.
  - `doc/contributing.md`: Good to know before making your first contribution.
- `pages` and `components`: Source code for almost everything visible on the website's pages.
- `public`: Files that will be served directly on the website.
  - `public/locales`: Language files defining translations of the website.

# Code architecture overview

How does everything fit together, code-wise?

- Copies of source datasets are under `data/facts`.
- We run the Python scripts under `data` to produce `data/output/climate-data.json` from those datasets.
- The latest copy of `data/output/climate-data.json` is always checked into version control.
- The rest of the website source code loads `data/output/climate-data.json`.
- The framework `next.js` is used to compile actual HTML pages at runtime.
- `next.js` caches each page for serving, to serve it faster for each new visitor.

## Contributing

The idea behind Klimatkollen is to give citizens access to the climate data we need to meet the goals of the Paris Agreement – and save our own future.

Do you have an idea for a feature you think should be added to the project? Before jumping into the code, it's a good idea to discuss your idea in the Discord server. That way you can find out if someone is already planning work in that area, or if your suggestion aligns with other people's thoughts. You can always submit an [issue](https://github.com/Klimatbyran/klimatkollen/issues) explaining your suggestion. We try to review the issues as soon as possible, but be aware that the team is at times very busy. Again, feel free to ask for a review on Discord!

Looking for ideas on what needs to be done? We appreciate help on existing [issues](https://github.com/Klimatbyran/klimatkollen/issues) very much. If you pick one up, remember to leave a comment saying you're working on it, and roughly when you expect to report progress. This helps others avoid double work and know what to expect.

Testing, bug fixes, typos or fact checking of our data is highly appreciated.

See [doc/contributing.md](./doc/contributing.md) before making your first contribution.

## Contact

Join the Discord server in the introduction or send an email to [hej@klimatkollen.se](mailto:hej@klimatkollen.se).

## Supporters and Partners

This work wouldn't have been possible without the support from

Google.org, Postkodstiftelsen.

We'd also like to thank our current and former partners

ClimateView, Klimatklubben.se, Researcher's Desk, Exponential Roadmap, WWF, We Don't Have Time, Våra Barns Klimat, Argand, StormGeo, Iteam, Precisit, Climate AI Nordics.

## LICENSE

This project is licensed under the terms of the [Apache 2.0](LICENSE) © Klimatbyrån Ideell Förening.
