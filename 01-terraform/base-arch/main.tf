provider "oci" {
  region = var.region
}

resource "oci_core_vcn" "workshop_vcn" {
  cidr_block     = var.vcn_cidr
  compartment_id = var.compartment_ocid
  display_name   = "workshop-vcn"
  dns_label      = "workshopvcn"
}

resource "oci_core_internet_gateway" "igw" {
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.workshop_vcn.id
  display_name   = "workshop-igw"
  enabled        = true
}

resource "oci_core_route_table" "rt" {
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.workshop_vcn.id
  display_name   = "workshop-rt"

  route_rules {
    network_entity_id = oci_core_internet_gateway.igw.id
    destination       = "0.0.0.0/0"
    destination_type  = "CIDR_BLOCK"
  }
}

resource "oci_core_subnet" "public_subnet" {
  compartment_id      = var.compartment_ocid
  vcn_id              = oci_core_vcn.workshop_vcn.id
  cidr_block          = var.subnet_cidr
  display_name        = "workshop-subnet-public"
  dns_label           = "workshopsubnet"
  route_table_id      = oci_core_route_table.rt.id
  prohibit_public_ip_on_vnic = false
}
