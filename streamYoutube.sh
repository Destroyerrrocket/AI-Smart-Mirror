#!/bin/bash
lynx -dump "https://www.youtube.com/results?search_query=\"$1\"" | egrep -o "http.*watch.*" | vlc -
