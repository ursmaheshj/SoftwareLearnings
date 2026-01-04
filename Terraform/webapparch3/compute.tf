
resource "aws_instance" "web_server1" {
  ami             = var.ami
  instance_type   = var.instance_type
  security_groups = [aws_security_group.web_app.name]
  user_data       = <<-EOF
              #!/bin/bash
              echo "Hello, World 1" > index.html
              python3 -m http.server 8080 &
              EOF
}

resource "aws_instance" "web_server2" {
  ami             = var.ami
  instance_type   = var.instance_type
  security_groups = [aws_security_group.web_app.name]
  user_data       = <<-EOF
              #!/bin/bash
              echo "Hello, World 2" > index.html
              python3 -m http.server 8080 &
              EOF
}
