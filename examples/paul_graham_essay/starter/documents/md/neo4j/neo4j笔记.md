```console
docker run --name neo4j01 --publish=7474:7474 --publish=7687:7687 --volume=E:/docker-disk/neo4j/data:/data --env=NEO4J_AUTH=none neo4j
```