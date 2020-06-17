# isim
Python client for IBM Security Identity Manager (ISIM/ITIM) web services (SOAP and REST APIs) <br>
Tested on ISIM7.0.1.13 and ISIM7.0.2.
Due to API limitations some functionalities are served through ISIM's REST API and some other through ISIM SOAP Web Services. <br>
You probably will need to import ISIMs Root Certificate into Certifi for the connection to work.

- Functionalities
    - Authentication
    - Access request
    - Complete Manual Activities
        - Approval
        - Work Order
    - Create:
        - Person
            - Need to Modify isimws.classes.Person to match your attributes (for now)
        - BPPerson
            - Need to Modify isimws.classes.BPPerson to match your attributes (for now)
        - Static Roles
        - Provisioning Policies
    - Modify:
        - Static Roles
        - Provisioning Policies
    - Delete:
        - Services
    - Search: 
        - Workflow
        - Service
        - Static Role
        - Provisioning Policy
        - Person
        - BPPerson
        - OrgUnit
        - Access
        - Manual activities
        - Forms
        - Groups
    - Unit testing:
        - Creating people
        - Requesting multiple accesses
        - Automatically completing all approvals and work orders from the request

- TODO:
    - Improve project structure
        - Use english for everything
    - Improve documentation
        - Basic usage
        - Batch loads
        - Requirements
    - Create class bindings for Service and Access items
    - Generalize Person and BPPerson attribute handling
        - *Abstract* class?
    - Add search to class initialization:
        - Person
        - Business Partner Person
        - Static Role
        - Provisioning Policy
    - Add at least modify and delete operations for Person classes
    - Generalize policy and role creation
        - Should not always require a full CSV file but only a dict or some structure for ease of use
