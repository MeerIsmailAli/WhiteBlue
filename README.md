# 📌 URL Shortener – Assessment 2

## 🧠 Overview
This project implements a simple **URL Shortener** service designed for efficiency and reliability. The system focuses on three core functional requirements:
* **Generation:** Create a short URL from a long URL.
* **Redirection:** Seamlessly redirect users from the short URL to the original destination.
* **Idempotency:** Ensure the same long URL always maps to the same short URL.

---

## ⚙️ Design Decisions

### 🔹 Short URL Generation
* **Hashing:** Used **MD5 hashing** to generate a compressed and fixed-length short code.
* **Deterministic:** Ensures a consistent mapping where the same input always yields the same output.

### 🔹 Collision Handling
While MD5 offers a wide range of values, hash collisions are still possible. 
* **Strategy:** If a generated short code already exists for a *different* long URL, the system appends an `'x'` to the short code until a unique value is found.

**Example:**
`abc123` → `abc123x` → `abc123xx`

---

## ⚡ Performance Considerations

### 🔹 Latency Reduction
Direct database reads can introduce latency at scale. To optimize performance, the system is designed to use **caching systems like Redis** to store "hot keys" (frequently accessed URLs).

**Request Flow:**
`Request` → `Cache` → *(miss)* → `Database` → `Update Cache`

---

## 🛡️ High Availability
To ensure the system remains reliable and fault-tolerant, the following strategies are implemented:

### 🔹 Load Balancing & Scalability
* Deploy multiple API server instances.
* Use load balancers to distribute traffic evenly.
* **Implementation:** Can be achieved via server-based clusters or serverless solutions like **AWS Lambda**.

### 🔹 Database Replication
Using a replicated database setup (e.g., **Amazon RDS**) ensures fault tolerance:
* **Primary (Master):** Handles all write operations.
* **Read Replicas:** Handle the bulk of read operations.
* **Benefit:** Since URL shorteners are **read-heavy**, this significantly improves performance.

### 🔹 Multi-Zone & Global Reach
* **Multi-Zone Deployment:** Replicate database instances across availability zones to ensure automatic failover if one zone goes down.
* **CDN (Optional Enhancement):** Use Content Delivery Networks to reduce latency for global users, speeding up the redirect process regardless of geographic location.
