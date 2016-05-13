# Performance Testing for Indy

This is a perf testing setup for [Indy](https://commonjava.github.io/indy/).

## Setup

First, you'll need to download and unpack (or otherwise setup) your Indy deployment. Follow instructions in the Indy User's Guide if you don't know how to do this. Once this is done, you probably want to pre-populate the central repository cache on your local Indy instance to avoid measuring upstream connection latency during your test run (since this could be highly variable depending on your connection). To pre-populate central, you might run something like this (giving your own storage details, of course):

```
    $ ./populate-central.py <path-to-indy>/var/lib/indy/storage/remote-central
```

If you have an existing repository manager you'll use to download the artifacts, you might want to point at that instead:

```
    $ ./populate-central.py <path-to-indy>/var/lib/indy/storage/remote-central http://localhost:8180/api/remote/central
```

## Execution

*NOTE:* Before running your test, don't forget to start your Indy instance!

I've created a convenience script called `start.sh` that helps formulate the command line for a headless JMeter execution. It uses environment variables for the following:

* JMeter executable (*envar:* `JMETER`, default: `$HOME/apps/jmeter/current/bin/jmeter`)
* The test to run (*envar:* `JMETER_TEST`, defualt: `$PWD/tests/build-simulation-existing.jmx`)
* The log file to write (*envar:* `JMETER_LOG`, default: `$(basename $TEST).log`)
* The properties to use to configure the test (*envar:* `JMETER_PROPS`, default: `$PWD/inputs/properties/local5.properties`)

You can override any of these as needed by setting the associated environment variable. In particular, it's important to copy/modify the properties to match your Indy deployment information.

When you have the downloadable artifacts and environment variables setup as needed, you can run the test with:

```
    $ ./start.sh
```

## Suggestions

I've found it useful to start VisualVM and monitor the Indy process' RAM and CPU usage. It's also sometimes useful to look at the thread states, memory sampler (with snapshotting), etc. to get insight into what parts of Indy are responsible for different performance characteristics.
