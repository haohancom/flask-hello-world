#!/bin/bash

echo "Testing GET method with hello world:"
curl -X GET "http://127.0.0.1:8080/demo/echo?message=hello+world"

echo -e "\n\nTesting POST method with hello world:"
curl -X POST -H "Content-Type: application/json" -d '{"message": "hello world"}' "http://127.0.0.1:8080/demo/echo"

echo ""
