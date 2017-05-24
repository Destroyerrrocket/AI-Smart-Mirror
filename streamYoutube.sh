#!/bin/bash
lynx -dump "https://www.youtube.com/results?search_query=\"$1\"" | egrep -o "http.*watch.*" | vlc -
#Now it's not used any more. It's useless. but it still can be used from the command line!
