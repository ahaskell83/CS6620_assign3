#!/bin/bash

docker compose -f docker-compose-tests.yml up -d --build

terraform init

terraform plan

terraform apply --auto-approve

pytest test_assign3.py