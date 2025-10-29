# KubernetesSubmissions

## Exercises

### Chapter 2

- [1.1.](https://github.com/JVilo/KubernetesSubmissions/tree/1.1/log_output)
- [1.2.](https://github.com/jvilo/KubernetesSubmissions/tree/1.2/todo_app)
- [1.3.](https://github.com/JVilo/KubernetesSubmissions/tree/1.3/log_output)
- [1.4.](https://github.com/jvilo/KubernetesSubmissions/tree/1.4/todo_app)
- [1.5.](https://github.com/jvilo/KubernetesSubmissions/tree/1.5/todo_app)
- [1.6.](https://github.com/jvilo/KubernetesSubmissions/tree/1.6/todo_app)
- [1.7.](https://github.com/JVilo/KubernetesSubmissions/tree/1.7/log_output)
- [1.8.](https://github.com/jvilo/KubernetesSubmissions/tree/1.8/todo_app)
- [1.9.](https://github.com/jvilo/KubernetesSubmissions/tree/1.9/ping-pong)
- [1.10.](https://github.com/jvilo/KubernetesSubmissions/tree/1.10/log_output)
- [1.11.log_output ](https://github.com/jvilo/KubernetesSubmissions/tree/1.11/log_output)[1.11.ping-pong](https://github.com/jvilo/KubernetesSubmissions/tree/1.11/ping-pong)
- [1.12.](https://github.com/jvilo/KubernetesSubmissions/tree/1.12/todo_app)
- [1.13.](https://github.com/jvilo/KubernetesSubmissions/tree/1.13/todo_app)

### Chapter 3

- [2.1.log_output ](https://github.com/jvilo/KubernetesSubmissions/tree/2.1/log_output)[2.1.ping-pong](https://github.com/jvilo/KubernetesSubmissions/tree/2.1/ping-pong)
- [2.2.](https://github.com/jvilo/KubernetesSubmissions/tree/2.2/todo_app)
- [2.3.log_output ](https://github.com/jvilo/KubernetesSubmissions/tree/2.3/log_output)[2.3.ping-pong](https://github.com/jvilo/KubernetesSubmissions/tree/2.3/ping-pong)
- [2.4.](https://github.com/jvilo/KubernetesSubmissions/tree/2.4/todo_app)
- [2.5.](https://github.com/jvilo/KubernetesSubmissions/tree/2.5/ping-pong)
- [2.6.](https://github.com/jvilo/KubernetesSubmissions/tree/2.6/todo_app)
- [2.7.](https://github.com/jvilo/KubernetesSubmissions/tree/2.7/ping-pong)
- [2.8.](https://github.com/jvilo/KubernetesSubmissions/tree/2.8/todo_app)
- [2.9.](https://github.com/jvilo/KubernetesSubmissions/tree/2.9/todo_app)
- [2.10.](https://github.com/jvilo/KubernetesSubmissions/tree/2.10/todo_app)

### Chapter 4

- [3.1.](https://github.com/jvilo/KubernetesSubmissions/tree/3.1/ping-pong)
- [3.2.log_output ](https://github.com/jvilo/KubernetesSubmissions/tree/3.2/log_output)[3.2.ping-pong](https://github.com/jvilo/KubernetesSubmissions/tree/3.2/ping-pong)
- [3.3.log_output ](https://github.com/jvilo/KubernetesSubmissions/tree/3.3/log_output)[3.3.ping-pong](https://github.com/jvilo/KubernetesSubmissions/tree/3.3/ping-pong)
- [3.5.](https://github.com/jvilo/KubernetesSubmissions/tree/3.5/todo_app)
- [3.6.](https://github.com/jvilo/KubernetesSubmissions/tree/3.6/todo_app)
- [3.7.](https://github.com/jvilo/KubernetesSubmissions/tree/3.7/todo_app)
- [3.8.](https://github.com/jvilo/KubernetesSubmissions/tree/3.8/todo_app)
- [3.9.]()
    ## 3.9 DBaaS vs DIY

When deploying PostgreSQL on Google Cloud, there are two main options:

- **DBaaS (Database as a Service)** — use **Google Cloud SQL for PostgreSQL**, a fully managed database.
- **DIY (Do It Yourself)** — deploy your own PostgreSQL container inside **Google Kubernetes Engine (GKE)**, using **PersistentVolumeClaims (PVCs)** for storage.

The table below compares the two approaches across setup, maintenance, backup, cost, and control.

---

| # | Category | Subtopic | **DBaaS (Cloud SQL)** | **DIY (Postgres on GKE)** |
|:-:|:----------|:----------|:----------------------|:---------------------------|
| **1** | **Setup & Initialization** | Setup time | Quick and automated setup via Google Console or `gcloud`. | Requires building Docker images, writing manifests, and setting up Services and PVCs. |
|  |  | Configuration | Managed automatically — replication, scaling, and patching handled by Google. | Must be manually configured and tuned in YAML or Helm charts. |
| **2** | **Maintenance** | Patching & upgrades | Google handles updates and patching automatically. | Must be done manually — can cause downtime if not automated. |
|  |  | Monitoring & logging | Integrated with Cloud Monitoring and Cloud Logging. | Requires setup of Prometheus, Grafana, or similar tools. |
|  |  | High availability | Built-in multi-zone failover and automatic replication. | Needs StatefulSets and custom HA setup. |
| **3** | **Backups & Recovery** | Automatic backups | Built-in automated daily backups and PITR (point-in-time recovery). | Must create CronJobs or manual scripts using `pg_dump` to a bucket. |
|  |  | Restore process | One-click restore via console or API. | Manual restore of PVCs or import from dump file. |
| **4** | **Cost** | Billing model | Pay per instance uptime and managed service overhead. | Pay for compute (nodes) and storage only; cheaper but requires ops time. |
|  |  | Scaling cost | Easy vertical/horizontal scaling, but more expensive for large databases. | Scaling possible but complex and manual; needs Kubernetes tuning. |
| **5** | **Control & Flexibility** | Access level | Limited — no superuser or OS-level access. | Full root and configuration access; can install any extensions. |
|  |  | Portability | Locked to Google Cloud. | Portable to any Kubernetes cluster. |
| **6** | **Overall Evaluation** | Best use case | Ideal for **production** systems requiring reliability and minimal ops. | Ideal for **learning**, **testing**, or custom database configurations. |

---

### **Summary**

| **Area** | **Best Option** |
|:----------|:----------------|
| Ease of setup & maintenance | ✅ **DBaaS (Cloud SQL)** |
| Customization & control | ✅ **DIY (Postgres on GKE)** |
| Cost efficiency (small scale) | ✅ **DIY** |
| Reliability, backups, HA | ✅ **DBaaS** |
| Learning & experimentation | ✅ **DIY** |

---

### **Conclusion**

- **DBaaS (Google Cloud SQL)** — best suited for production use where uptime, backup automation, and ease of management are priorities.  
- **DIY (Postgres on GKE)** — better for developers or teams who need more control and want to learn Kubernetes database operations.

---

### 📖 **References**
- [Google Cloud SQL for PostgreSQL](https://cloud.google.com/sql/docs/postgres/introduction)  
- [Google Cloud — Database options on GKE](https://cloud.google.com/kubernetes-engine/docs/concepts/database-options)  
- [NetApp Blog — Managed vs Self-Managed PostgreSQL](https://www.netapp.com/blog/gcp-cvo-blg-google-cloud-postgresql-managed-or-self-managed/)  
- [Bytebase — PostgreSQL Hosting Options in 2025](https://www.bytebase.com/blog/postgres-hosting-options-pricing-comparison/)

