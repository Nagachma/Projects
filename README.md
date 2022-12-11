# Accounts
* DEV: 525972751958/mmc-did-ninfrmgi
* SIT: 106485546313/mmc-dit-ninfrmgi
* PROD: 939433633862/mmc-dip-ninfrmgi

# Project Info
* CI Name: ninfrmgi
* Project Docs: https://share.merck.com/pages/viewpage.action?pageId=927006849

# Source Tree

```
mii
│   .pylintrc
│   environment.yml
│   jobs-configuration.groovy
│   Makefile
│   pytest.ini
│   README.md
│   sonar-project.properties
│
├───AWS
│   ├───glue
│   │   │   aws_common.py
│   │   │   configuration.py
│   │   │   custom_exception.py
│   │   │   load_study_data.py
│   │   │   log.py
│   │   │   ninfrmgi_mii_run.py
│   │   │   settings.py
│   │   │   submit_study_data.py
│   │   │   transform_study_data.py
│   │   │
│   │   └───config_templates
│   │           config.json
│   │           inform_payload_template.xml
│   │           inform_sample_template.xml
│   │
│   └───lambda
│       ├───dynamic_sns_topic_selection
│       │   └───src
│       │           dynamic_sns_topic_selection.py
│       │
│       ├───glue_job_failed
│       │   └───src
│       │           glue_job_failed.py
│       │
│       ├───odmsubmit_password_reset
│       │   └───src
│       │           odmsubmit_password_reset.py
│       │
│       ├───odmws_password_reset
│       │   └───src
│       │           odmws_password_reset.py
│       │
│       └───password_reset_common
│           └───src
│                   password_reset_common.py
│                   requirements.txt
│
├───Jenkins
│   │   branching.Jenkinsfile
│   │   {env}elop.Jenkinsfile
│   │   feature.Jenkinsfile
│   │   master.Jenkinsfile
│   │   production-man-deploy.Jenkinsfile
│   │   pull-request.Jenkinsfile
│   │   uat-man-deploy.Jenkinsfile
│   │
│   └───scripts
│           terraform_cmds.sh
│
├───Terraform
│   │   {env}.tfvars
│   │   eventbridge_rule.tf
│   │   glue.tf
│   │   lambda.tf
│   │   main.tf
│   │   parameter_store.tf
│   │   prod.tfvars
│   │   s3_buckets.tf
│   │   sit.tfvars
│   │   sns_topic.tf
│   │   variables.tf
│   │
│   └───remote_backend
│           {env}.conf
│           {env}.tfvars
│           main.tf
│           prod.conf
│           prod.tfvars
│           sit.conf
│           sit.tfvars
│           variables.tf
│
└───tests
    │   test_custom_exception.py
    │   test_dynamic_sns_topic_selection.py
    │   test_glue_job_failed.py
    │   test_load_study_data.py
    │   test_ninfrmgi_mii_run.py
    │   test_odmsubmit_password_reset.py
    │   test_submit_study_data.py
    │   test_transform_study_data.py
    │
    └───data
        ├───InForm
        │       InForm_5_records.xml
        │
        └───Medidata
                Medidata_5_records.xml
                medidata_view_last_refresh_datetime.txt

```

# Infrasctucture and App Deployment Steps
* Jenkins jobs that auto deplys Infrastructure along with App code can be found [here](https://builds.merck.com/job/BITBUCKET/job/MRLTDC/job/mii/job/multibranch-job/)
* Jobs for manual deployments can be found [here](https://builds.merck.com/job/BITBUCKET/job/MRLTDC/job/mii/job/deployments/)
* In order to run the deployment from a local machine, you need to have 'terraform(at least v1.0.6)' and 'python 3.7' as the current env and then run below commands. 

## Deploy Remote Backend

```
        cd <path-to>/mii/terraform/remote_backend
        terraform init -backend-config=<env>.conf
        terraform fmt
        terraform validate
        terraform plan --var-file=<env>.tfvars
        terraform apply --var-file=<env>.tfvars
```

## Deploy Infrastructure

```
        cd <path-to>/mii/terraform
        terraform init -backend-config=<env>.backend
        terraform fmt
        terraform validate
        terraform plan --var-file=<env>.tfvars
        terraform apply --var-file=<env>.tfvars
```

# Deploys:

```
Roles
	ninfrmgi-athena-role
	ninfrmgi-glue-role
        ninfrmgi-lambda-role
	ninfrmgi-password-reset-role
		
Secrets
        MediData-Credentials
	Lambda-Credentials
	InForm-WCFUser-Credentials
	InForm-User-Credentials
        KmsKeyId
	
Buckets
	ninfrmgi-athena-logs-{env}-s3
	ninfrmgi-glue-scripts-{env}-s3
        ninfrmgi-inform-{env}-s3
	ninfrmgi-medidata-{env}-s3
	ninfrmgi-processlogs-{env}-s3

Glue Files
	scripts/aws_common.py 
        scripts/config.json 
        scripts/configuration.py 
        scripts/custom_exception.py 
        scripts/inform_payload_template.xml 
        scripts/inform_sample_template.xml 
        scripts/load_study_data.py 
        scripts/log.py 
        scripts/ninfrmgi_mii_run.py 
        scripts/settings.py 
        scripts/submit_study_data.py 
        scripts/transform_study_data.py 

lambda layer
        ninfrmgi-{env}-password-reset-common

lambdas(FunctionName)
        ninfrmgi-{env}-inform-user-credentials-password-reset
        ninfrmgi-{env}-inform-wcf-user-credentials-password-reset
        ninfrmgi-{env}-glue-job-failed-admin-email 
        ninfrmgi-{env}-error-email 

glue_job(Name)
        ninfrmgi-{env}-glue-job 

parameters(Name)
        ninfrmgi-parameters 
		
events(Name)
        ninfrmgi-{env}-glue-job-failure 
		
logs(/aws/lambda/ninfrmgi)
        /aws/lambda/ninfrmgi-{env}-glue-job-failed-admin-email 
        /aws/lambda/ninfrmgi-{env}-error-email 
        /aws/lambda/ninfrmgi-{env}-inform-user-credentials-password-reset
        /aws/lambda/ninfrmgi-{env}-inform-wcf-user-credentials-password-reset
	
sns_topics() 
        arn:aws:sns:us-east-1:525972751958:ninfrmgi-{env}-0001-008-error-email  
        arn:aws:sns:us-east-1:525972751958:ninfrmgi-{env}-glue-job-failed-admin-email 
```

