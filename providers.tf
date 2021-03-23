provider "google" {
  # version     = "2.7.0"
  credentials = file("/google/auth/tcb-gcp2-moodle.json")
  project     = var.project
  region      = var.region
}
