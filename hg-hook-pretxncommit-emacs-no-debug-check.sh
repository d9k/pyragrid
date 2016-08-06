#!/bin/bash

##add to .hg/hgrc code like:

#[hooks]
#precommit.emacs-nodebug=./hg-hook-pretxncommit-emacs-no-debug-check.sh

result=`hg diff -U 0 | grep -P "^\+\s+import pdb\;\s*pdb\.set_trace\(\)"`

if [ -n "${result}" ]; then
  exit 1
fi
