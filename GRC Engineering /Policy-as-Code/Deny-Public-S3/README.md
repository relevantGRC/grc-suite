# Lab 01: No Public Buckets Allowed

### Overview

In this lab, you'll build a lightweight security check that prevents your team from accidentally creating public AWS S3 buckets, a common and dangerous cloud misconfiguration. You'll do this using policy as code with Rego, Conftest, and GitHub Codespaces.
This lab is perfect for beginners. No coding experience or tool setup required.

### By the end, you’ll:
- Understand how policy as code works
- Write a policy using Rego
- Test it against a sample S3 config
- Run everything in GitHub Codespaces

---

## The Lab

### What You’ll Use:
- GitHub (to host the code)
- GitHub Codespaces (runs everything in your browser)
- Rego (the policy language)
- Conftest (a policy testing tool)


### Step 1: Create a GitHub Repo
1. Go to github.com and log in
2. Click the + in the upper-right → New repository
3. Name it something like no-public-s3
4. Check Add a README and click Create repository


### Step 2: Add These Files
1. Click Add file → Create new file
2. Create a file named input.json with:

```
{
  "resource_type": "aws_s3_bucket",
  "acl": "public-read"
}
```

3. Create a folder and file within it labeled policy/input.rego and add the following:

```
package s3policy

deny[message] {
  input.resource_type == "aws_s3_bucket"
  input.acl == "public-read"
  message := "S3 buckets cannot be publicly readable (acl: public-read)"
}
```

4. Create a conftest.toml file in the root directory to make testing easier:

```
policy = "./policy"
```

5. Commit each file to your main branch.


### Step 3: Open in Codespaces
1. Click the green Code button
2. Select Open with Codespaces → Create new codespace

Tip: Codespaces are free for personal GitHub accounts (up to 60 hours/month)


### Step 4: Test the Policy
1. From the terminal inside your Codespace, run:

```
conftest test input.json --all-namespaces
```

You should see:

```
FAIL - input.json - S3 buckets cannot be publicly readable (acl: public-read)
```

### Congratulations! You just:
- Wrote a security policy in code
- Evaluated real IaC (Terraform) against it
- Got a policy-as-code enforcement result




## The Impact

Imagine pushing this code to production without a policy check. You just exposed your data to the world.
With PaC:
- Developers get fast feedback
- Risky misconfigs are caught before they matter
- Compliance teams sleep better




## Mitigate and Retest

Now, make the S3 bucket private.
1. In the left sidebar, open the input.json file.
2. Replace the content with:

```
{
  "resource_type": "aws_s3_bucket",
  "acl": "private"
}
```

3.	Re-run:

```
conftest test input.json --all-namespaces
```

This time, you’ll see:

```
PASS - input.json
```

The policy allowed the secure config to pass. 



## Compliance Mapping

This policy directly addresses critical security and compliance objectives by satisfying the following NIST SP 800-53 controls:

AC-6(10) – Automated enforcement of least privilege: This policy ensures that permissions for data storage are automatically restricted to the absolute minimum necessary. By preventing public access to storage buckets, it directly enforces the principle of least privilege, reducing the attack surface and mitigating risks associated with over-privileged access. This automated enforcement minimizes the potential for human error in configuring access controls.

SC-12 – Preventing unauthorized public access: The core of this policy is to eliminate the possibility of data being unintentionally exposed to the public internet. By strictly prohibiting public buckets, it acts as a preventative measure against unauthorized disclosure of sensitive information. This control is vital for maintaining data confidentiality and integrity, protecting against data breaches, and ensuring compliance with privacy regulations.
