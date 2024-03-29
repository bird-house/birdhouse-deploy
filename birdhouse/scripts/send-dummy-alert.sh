#!/bin/bash
# https://gist.githubusercontent.com/cherti/61ec48deaaab7d288c9fcf17e700853a/raw/a69ddd1d96507f6d94059071d500fe499631e739/alert.sh
# Useful to test receiving alert on UI and via email notif.

name=${RANDOM}
url='http://localhost:9093/api/v1/alerts'

echo "firing up alert ${name}" 

# change url o
curl -XPOST $url -d "[{ 
	\"status\": \"firing\",
	\"labels\": {
		\"alertname\": \"${name}\",
		\"service\": \"my-service\",
		\"severity\":\"warning\",
		\"instance\": \"${name}.example.net\"
	},
	\"annotations\": {
		\"summary\": \"High latency is high!\"
	},
	\"generatorURL\": \"http://prometheus.int.example.net/<generating_expression>\"
}]"

echo ""

echo "press enter to resolve alert (Ctrl-C to cancel)"
read -r

echo "sending resolve"
curl -XPOST "${url}" -d "[{
	\"status\": \"resolved\",
	\"labels\": {
		\"alertname\": \"${name}\",
		\"service\": \"my-service\",
		\"severity\":\"warning\",
		\"instance\": \"${name}.example.net\"
	},
	\"annotations\": {
		\"summary\": \"High latency is high!\"
	},
	\"generatorURL\": \"http://prometheus.int.example.net/<generating_expression>\"
}]"

echo ""
