## Guidelines

### Git Branches

* `develop`: This is the **next release** branch. Changes to this branch should done only through pull requests
* `primary`: This is the release branch.  Hotfixes are merged here and non-development deployments will be made from this branch.

We use git-flow, get familiar with it. No EXCEPTIONS.

Create your feature-branches work on them and make the pull-request. But before you do pull request do this

### Automated Deployments Branch

This is work in progress but deployments will be automated on commit to
* `develop` branch
* `primary` branch

The release will be triggered from jenkins

## Developer Build

Tools you will need.
* Visual Code
* python
### Setting up the Development Environment

```sh
cd src
make dev-env
source .env/bin/activate
```

* `make dev-env`: creates the virtualenv in .policy_env folder
* `make deps`: installs requirements.txt and activates policy set commmand

### About Project

*********************************Gmail Data Filter*************************************

* `gmail_searcher` - This tries to fetch data from Gmail and filter based on specific conditions
* `conditions` -
    header_rule = {
        "Subject": "HappyFox",
        "From": "happyfox",
        "Date": "Less than 2 days"
    }
* `store_data_in_sqllite` -
    Connect to Sqllite DB
    Store the details in the below structure
        ***
        Subject VARCHAR(255) NOT NULL,
        Email VARCHAR(255) NOT NULL,
        DateReceived VARCHAR(255) NOT NULL
        ***
