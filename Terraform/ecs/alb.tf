# Application Load Balancer
resource "aws_lb" "fastapi_alb" {
  name               = "${var.app_name}-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb_sg.id]
  subnets            = [aws_subnet.public_subnet_1.id, aws_subnet.public_subnet_2.id]

  enable_deletion_protection = false

  tags = {
    Name = "${var.app_name}-alb"
  }
}

# Target Group
resource "aws_lb_target_group" "fastapi_tg" {
  name        = "${var.app_name}-tg"
  port        = var.container_port
  protocol    = "HTTP"
  vpc_id      = aws_vpc.fastapi_vpc.id
  target_type = "ip"

  health_check {
    healthy_threshold   = 2
    unhealthy_threshold = 2
    timeout             = 3
    interval            = 30
    path                = var.health_check_path
    matcher             = "200"
  }

  tags = {
    Name = "${var.app_name}-tg"
  }
}

# ALB Listener (HTTP)
resource "aws_lb_listener" "fastapi_listener" {
  load_balancer_arn = aws_lb.fastapi_alb.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.fastapi_tg.arn
  }
}

# Optional: ALB Listener (HTTPS) - Uncomment if you have SSL certificate
# resource "aws_lb_listener" "fastapi_listener_https" {
#   load_balancer_arn = aws_lb.fastapi_alb.arn
#   port              = 443
#   protocol          = "HTTPS"
#   ssl_policy        = "ELBSecurityPolicy-TLS-1-2-2017-01"
#   certificate_arn   = var.ssl_certificate_arn
#
#   default_action {
#     type             = "forward"
#     target_group_arn = aws_lb_target_group.fastapi_tg.arn
#   }
# }

# Optional: HTTP to HTTPS redirect - Uncomment if using HTTPS
# resource "aws_lb_listener" "fastapi_listener_http_redirect" {
#   load_balancer_arn = aws_lb.fastapi_alb.arn
#   port              = 80
#   protocol          = "HTTP"
#
#   default_action {
#     type = "redirect"
#
#     redirect {
#       port        = "443"
#       protocol    = "HTTPS"
#       status_code = "HTTP_301"
#     }
#   }
# }
