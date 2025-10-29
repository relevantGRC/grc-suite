resource "null_resource" "example" {
  triggers = {
    open_sg = jsonencode({
      name        = "open_sg"
      description = "Allows SSH from anywhere"
      ingress = [{
        from_port   = 22
        to_port     = 22
        protocol    = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
      }]
      egress = [{
        from_port   = 0
        to_port     = 0
        protocol    = "-1"
        cidr_blocks = ["0.0.0.0/0"]
      }]
    })
  }
}
