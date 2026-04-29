📌 URL Shortener – Assessment 2
🧠 Overview

This project implements a simple URL Shortener service that:

Generates a short URL from a long URL
Redirects users from the short URL to the original URL
Ensures idempotency (same long URL → same short URL)
⚙️ Design Decisions
🔹 Short URL Generation
Used MD5 hashing to generate a compressed and fixed-length short code
Ensures deterministic mapping (same input → same output)
🔹 Collision Handling
Although rare, hash collisions are possible
Implemented a simple strategy:
If a generated short code already exists for a different URL
Append 'x' to the short code until a unique value is found

Example:

abc123 → abc123x → abc123xx ...
⚡ Performance Considerations
🔹 Latency Reduction
Direct database reads can introduce latency at scale
To optimize:
Use caching systems like Redis
Store frequently accessed short URLs (hot keys) in cache

Flow:

Request → Cache → (miss) → Database → Update Cache
🛡️ High Availability

To ensure the system remains reliable and fault-tolerant:

🔹 Load Balancing & Scalability
Deploy multiple API server instances
Use load balancers to distribute traffic
Can be implemented using:
Server-based deployment (multiple instances)
Serverless solutions like AWS Lambda
🔹 Database Replication
Use a replicated database setup for fault tolerance
Example using Amazon RDS:
Primary (Master) → Handles write operations
Read Replicas → Handle read operations

This is effective because:

URL shortener systems are read-heavy
Improves performance and availability
🔹 Multi-Zone Deployment
Replicate database instances across availability zones
Ensures backup and failover if one instance goes down
🔹 CDN (Optional Enhancement)
Use CDN networks to reduce latency for global users
Improves response time for redirects
