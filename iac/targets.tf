locals {
  all_targets = [
    {
      status     = "ENABLED"
      source     = "jobsmu",
      domain     = "https://www.jobs.mu",
      source_url = "https://www.jobs.mu/jobs"
    },
    {
      status     = "ENABLED"
      source     = "myjobmu",
      domain     = "https://www.myjob.mu",
      source_url = "https://www.myjob.mu/ShowResults.aspx"
    },
    {
      status     = "ENABLED"
      source     = "mcbmu",
      domain     = "https://ekbd.fa.em2.oraclecloud.com",
      source_url = "https://ekbd.fa.em2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX/requisitions?"
    },
    {
      status     = "ENABLED"
      source     = "absamu",
      domain     = "https://absa.wd3.myworkdayjobs.com",
      source_url = "https://absa.wd3.myworkdayjobs.com/ABSAcareersite?locationCountry=a759018ba6ac489d9f16c086b914e1b6",
    },
    {
      status     = "ENABLED"
      source     = "emtel",
      domain     = "https://www.emtel.com",
      source_url = "https://www.emtel.com/about-us/careers",
    }
  ]
}
