# bclearer development libraries 

**bclearer_libraries** is a modular SDK providing services for core functionality, interop services, and orchestration services. This SDK is designed to offer seamless integration and extendability for the bclearer platform, enabling effective orchestration, data interoperability, and core utilities.

## Features

- **Core Services**: Provides essential functionality for configuration management, constants handling, and other core utilities.
- **Interop Services**: Facilitates data interoperability and communication between different services and systems.
- **Orchestration Services**: Manages workflows and service orchestration to coordinate processes within the bclearer ecosystem.

## Modules

The SDK is divided into the following major modules:

### 1. Core (`bclearer_libraries.core`)
This module includes utilities for configuration management and core functionality:

- **Configuration Managers**: Handles configuration setup and management.
- **Constants**: Provides a centralized location for constant values used across services.
  
Usage example:
```python
from bclearer_libraries.core.bclearer_core import SomeCoreClass

core_instance = SomeCoreClass()
core_instance.do_something()

```

### 2. Interop Services (bclearer_libraries.interop_services)
This module facilitates data interoperability and interactions between services.

bclearer_interop_services: Contains services for interacting with external systems or databases.
Usage example:

```python

from bclearer_libraries.interop_services.bclearer_interop_services import SomeInteropClass

interop_instance = SomeInteropClass()
interop_instance.integrate_with_service()
```

### 3. Orchestration Services (bclearer_libraries.orchestration_services)
This module manages orchestration processes, coordinating workflows and services.

bclearer_orchestration_services: Contains utilities for managing and orchestrating services in your workflow.
Usage example:

```python

from bclearer_libraries.orchestration_services.bclearer_orchestration_services import SomeOrchestrationClass

orchestration_instance = SomeOrchestrationClass()
orchestration_instance.manage_workflow()
```

Installation
To install bclearer_libraries, run the following:

bash
Copy code
pip install bclearer_libraries
This will install all necessary modules and dependencies required to use the SDK.

## Requirements
Python 3.6+
Other dependencies as listed in requirements.txt (e.g., neo4j, pandas)
Usage
After installation, you can start using the SDK by importing the relevant modules:

``` python

from bclearer_libraries.core.bclearer_core import SomeCoreClass
from bclearer_libraries.interop_services.bclearer_interop_services import SomeInteropClass
from bclearer_libraries.orchestration_services.bclearer_orchestration_services import SomeOrchestrationClass
```

Each module has its own set of features and functionality, so refer to the documentation or the module-specific sections above for detailed usage instructions.

## Testing
The project includes a suite of unit and integration tests. You can run the tests using:

```bash
pytest
```

Tests are located in the tests/ directory under each module.


### Contributing
Contributions are welcome! Please follow these steps if you would like to contribute:

Fork the repository.
Create a feature branch (git checkout -b feature/my-feature).
Commit your changes (git commit -am 'Add my feature').
Push to the branch (git push origin feature/my-feature).
Create a new Pull Request.
License
This project is licensed under the MIT License - see the LICENSE file for details.

### Contact
For any issues, questions, or suggestions, feel free to contact the maintainers at:

Mesbah Khan
Your Email: khanm@ontoledgy.io
