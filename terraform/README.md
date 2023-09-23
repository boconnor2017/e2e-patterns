# Terraform Templates
Each directory contains a `main.tf` file to perform the action associated with the directory naming convention. 

To install Terraform, use Pattern `A-03` (The Terraform Container). Then run the following commands in order:
```
docker  run  -v $(pwd):$(pwd) -w $(pwd) -i -t hashicorp/terraform init
```
```
docker  run  -v $(pwd):$(pwd) -w $(pwd) -i -t hashicorp/terraform validate
```
```
docker  run  -v $(pwd):$(pwd) -w $(pwd) -i -t hashicorp/terraform plan
```
```
docker  run  -v $(pwd):$(pwd) -w $(pwd) -i -t hashicorp/terraform apply
```
