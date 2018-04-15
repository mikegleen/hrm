#!/usr/bin/env bash
# Create a portrait thumbnail
# sips -Z 484 theatre\ poster.jpg --out theatre_poster_484
sips --resampleWidth 342 $1 --out ${1}_342.jpg
sips -p 484 342 ${1}_342.jpg --out ${1}_pad.jpg --padColor ffffff
