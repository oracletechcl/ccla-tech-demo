output "vcn_id" {
  value = oci_core_vcn.workshop_vcn.id
}

output "subnet_id" {
  value = oci_core_subnet.public_subnet.id
}
