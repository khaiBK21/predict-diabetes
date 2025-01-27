output "project_id" {
    value       = var.project_id
    description = "Project ID"
}

output "kubernetes_cluster_name" {
    value       = google_container_cluster.primary.name
    description = "GKE cluster name"
}