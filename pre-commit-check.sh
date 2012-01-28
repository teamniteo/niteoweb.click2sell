#!/bin/bash

echo 'Running tests'
bin/test -s niteoweb.click2sell

echo '====== Running ZPTLint ======'
for pt in `find src/niteoweb/click2sell/ -name "*.pt"` ; do bin/zptlint $pt; done

echo '====== Running PyFlakes ======'
bin/pyflakes src/niteoweb/click2sell
bin/pyflakes setup.py

echo '====== Running pep8 =========='
bin/pep8 --ignore=E501 src/niteoweb/click2sell
bin/pep8 --ignore=E501 setup.py
