#!/bin/bash

if ls cloudrouter-release-centos*.rpm
then
    echo "Running test"
    py.test -v ./cloudrouter-release-test.py
else
    echo "Unable to locate cloudrouter-release-centos*.rpm. Please copy them to this directory after build"
fi

