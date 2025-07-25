#!/bin/bash

docker compose -f docker-compose.yml up -d --build

terraform init

terraform plan

terraform apply --auto-approve
