This small project uses fast api to provide basic iam local deployment.

`mock_util.py` -> provides cx util capabilities

- /edr-log: log just the edr token for manual checks
- /sts: secure token service
- /presentations/query: credential service just returning VPs for the scopes in question
- /{did-name}: returns a valid DID pointing to the /sts endpoint for credential service

The mock_util only is able to mock the MembershipCredential and the FrameworkAgreements in version 1.0
NO DISMANTLER SUPPORT

# Add to docker compose

Pre-requisite: Create keys so that jwt tokens can be signed

```sh 
mkdir keys
cd keys
openssl ecparam -name prime256v1 -genkey -out private_key.pem
openssl ec -in private_key.pem -pubout -out public_key.pem
```

```shell
docker build -t mock-util-py .
```

Then start docker compose

```shell
docker compose up
```

Following services are now reachable:

| Service           | address                                         | reachable where          |
|-------------------|-------------------------------------------------|--------------------------|
| mock-util-service | http://mock-util-service:80/edr-log             | docker compose (miw net) |
| mock-util-service | http://mock-util-service:80/sts                 | docker compose (miw net) |
| mock-util-service | http://mock-util-service:80/presentations/query | docker compose (miw net) |
| mock-util-service | http://mock-util-service:80/{did-name}          | docker compose (miw net) |
| mock-util-service | localhost:8888/*                                | host machine             |

Use the service to either simulate the central IAM or just to got some logging api
