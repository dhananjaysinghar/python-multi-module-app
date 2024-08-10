# Multi-Module Project setup for Python

# Install poetry
~~~
python -m pip install --upgrade poetry
~~~


## Make Command to build and run the project
~~~
make build
make test
make cover
make package
make ssap # This will generate a requirements.txt [pip install -r requirements.txt]
make help



clean-parent                    Remove distribution and report directories
clean                           Clean all applications
dist-clean                      Deep clean all applications
build                           Build all applications
update                          Update all applications
test                            Test all applications
cover                           Generate coverage reports for all applications
ssap                            generate required reports for ssap
package                         Package all applications
ci-prebuild                     Install specified version of Poetry
ci                              Clean, build, and package all applications
help                            Show make target documentation

~~~

~~~
my_app.zip
├── my_module.py
├── my_package/
│   ├── __init__.py
│   └── other_module.pymake clean
└── main.py


python -m zipfile -c my_app.zip
python -m zipfile -c my_app.zip main.py

or
python -m my_app.zip main

~~~

## from python file
~~~
import sys
import runpy

# Path to the zip file
zip_path = 'path/to/your/my_app.zip'

# Add the zip file to the system path
sys.path.insert(0, zip_path)

# Run the main script inside the zip file
runpy.run_module('main', run_name='__main__')
~~~