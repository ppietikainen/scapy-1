Requirements: python-afl-0.5.3, afl (2.04b and 2.18b tested)

Workflow:

0. Create initial test stubs (optional, this has already been done, use tests-with-corpus.json):
   initial-list.py > initial.json

1. Create test stubs from json description:
    generate-stubs.py tests-with-corpus.json

2. Run AFL for all tests for some time:
    cd stub; for i in *; do (cd $i; timeout 60s sh ../../run.sh); done

3. Report crashes

    python crashes-to-tests.py > crashes.py
    
crashes-to-tests takes crashing samples from stub/* and dumps the reproducing command to stdout. It also
creates a seen-crashes.json that details what exceptions different classes have thrown.

4. Add allowed exceptions to test descriptions (See config.py):

Currently, "Scapy_Exception", "ValueError", "struct.error" are not considered as bugs. 

    python update-from-seen.py tests-with-corpus.json > newtests.json
    
5. Any new coverage found by AFL can also be fed back into the test corpus:
     (cd stub/PROTOCOL; sh ../../minimize.sh)
     python update-corpus.py newtests.json > tests-with-corpus.json
     
Regenerate stubs and continue fuzzing (1.)

