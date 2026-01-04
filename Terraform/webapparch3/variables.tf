variable "ami" {
  type    = string
  default = "ami-0720c0a2e1e125edd"
}

variable "instance_type" {
  type    = string
  default = "t4g.micro"
}

variable "cidr_blocks" {
  type = string
}