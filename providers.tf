provider "google" {
  # version     = "2.7.0"
  credentials = file("<caminho/Nome_do_seu_arquivo_json>")
  project     = var.project
  region      = var.region
}
