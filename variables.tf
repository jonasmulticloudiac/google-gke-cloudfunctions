variable "project" {
  default = "tcb-gcp-moodle"
}

variable "region" {
  default = "us-east1"
}

variable "zone" {
  default = "us-east1-d"
}

variable "cluster" {
  default = "tcb-k8smoodle"
}

variable "credentials" {
  default = "tcb-gcp2-moodle.json"
}

variable "kubernetes_min_ver" {
  default = "latest"
}

variable "kubernetes_max_ver" {
  default = "latest"
}

variable "machine_type" {
  default = "e2-standard-2"
}

variable "app_name" {
  default = "moodle-app"
}
