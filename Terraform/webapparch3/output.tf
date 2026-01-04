output "web_server1_ipaddress" {
  value = aws_instance.web_server1.public_ip
}

output "web_server2_ipaddress" {
  value = aws_instance.web_server2.public_ip
}

output "load_balancer_dns_name" {
  value = aws_lb.load_balancer.dns_name
}