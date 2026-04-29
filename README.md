for the assesment 2:
we use md5 hashing to have a compressed and short url and we handle collisions by simple method:
--> I apppend 'x' to the short url whenever there is a collision and use that as mapping
for latency reduction, we need to use caching systems like reddis to store hot keys in the cache, since fetching from DB directly introduces a lot of latency in scaled environments.
for high availability, we can explore cdn networks or try a serverless managed hosting like AWS lambda or with load balancers, we can setup several server instances or prefer the same in AWS services.We need to replicate DB across zones, to ensure backups in place in case one instance fails, we can use AWS RDS with a master write and multiple read replicas, since the read operation is more generally.
