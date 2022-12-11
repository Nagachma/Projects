jobs {
    "multibranch-job" {
        jobType = "MULTIBRANCH_JOB"
        jobDisplayName = "MII Automated builds"
        jobDescription = "<h1>Automated Builds for MII</h1>"
        pipelineDefinitionFile = "Jenkins/branching.Jenkinsfile"
    }
}

folders {
    deployments{
        displayName = "Manual Deployments"
        jobs {
            "deploy-to-testing" {
                jobType = "PIPELINE_JOB"
                pipelineDefinitionFile = "Jenkins/uat-man-deploy.Jenkinsfile"
            }
            "deploy-to-production" {
                jobType = "PIPELINE_JOB"
                pipelineDefinitionFile = "Jenkins/production-man-deploy.Jenkinsfile"
            }
        }
    }
}
