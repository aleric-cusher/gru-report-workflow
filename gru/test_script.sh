#!/bin/bash

coverage run --source=./api --omit="/tests/*" ./manage.py test "$@"
coverage report -m
