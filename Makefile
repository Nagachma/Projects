#Makefile allows for a definition of simple shell commands, removes the need to add difficult to read commands in Jenkins files.
#Called from Jenkins "Unit Testing" stages within Jenkins pipeline files.

.PHONY = test lint mypy pre-check post-check check

test:
	pytest --verbose --color=yes --junit-xml=tests/results.xml -o junit_family=xunit1 --cov-report xml:tests/coverage.xml --cov=.

lint:
	pylint --rcfile=.pylintrc --exit-zero \
	AWS/glue \
	AWS/lambda/dynamic_sns_topic_selection \
	AWS/lambda/glue_job_failed \
	AWS/lambda/odmsubmit_password_reset \
	AWS/lambda/odmws_password_reset \
	AWS/lambda/password_reset_common \
	tests -r n --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" > sonar-result

mypy:
	mypy --install-types --non-interactive \
	AWS/glue \
	AWS/lambda/dynamic_sns_topic_selection \
	AWS/lambda/glue_job_failed \
	AWS/lambda/odmsubmit_password_reset \
	AWS/lambda/odmws_password_reset \
	AWS/lambda/password_reset_common \
	--junit-xml=tests/mypy.xml &2>> /dev/null

pre-check: mypy lint
	cat sonar-result

post-check: test

check: pre-check post-check

