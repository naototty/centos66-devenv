#!/bin/bash

wget https://raw.githubusercontent.com/rabbitmq/rabbitmq-management/rabbitmq_v3_4_4/bin/rabbitmqadmin -O /usr/local/bin/rabbitmqadmin

chmod +x /usr/local/bin/rabbitmqadmin

rabbitmqadmin --bash-completion > /etc/bash_completion.d/rabbitmqadmin


