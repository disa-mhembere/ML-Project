#!/bin/bash

# clean.sh
# Created by Disa Mhembere on 2014-04-01.
# Email: disa@jhu.edu
# Copyright (c) 2014. All rights reserved.

echo "Cleanig writeup files"
find . -type f | grep "out\|blg\|log\|bbl\|sync\|aux" | xargs rm -vf
