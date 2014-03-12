#!/usr/bin/env python

import tests
import os, sys, getopt

if len(sys.argv) > 1 and sys.argv[1] == "update":
    if len(sys.argv) > 2:
        config = tests.get_config(os.path.dirname(sys.argv[2]))
        root, ext = os.path.splitext(sys.argv[2])
        if ext == config.get(tests.get_section(os.path.basename(root), config), 'input_ext'):
            tests.generate(root, config)
        else:
            print(file, 'does not have a valid file extension. Check config.')
    else:
        tests.generate_all()
else:
    tests.run()
