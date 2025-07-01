variable "region" {
  description = "Región OCI donde se desplegará la red"
  type        = string
}

variable "compartment_ocid" {
  description = "OCID del compartimento preexistente (okeworkshop)"
  type        = string
}

variable "vcn_cidr" {
  description = "CIDR block de la VCN"
  type        = string
  default     = "10.0.0.0/16"
}

variable "subnet_cidr" {
  description = "CIDR block para la subnet pública"
  type        = string
  default     = "10.0.1.0/24"
}
