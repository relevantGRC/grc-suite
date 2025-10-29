# Lab 02: Block Open Security Groups

### Overview

In this lab, you'll write a policy that blocks open security group rules. Like allowing the entire internet (`0.0.0.0/0`) to access sensitive ports such as SSH (22) or RDP (3389). These are among the most common and dangerous misconfigurations in cloud environments and are frequently exploited in attacks.
You’ll write a policy using Rego, test it with Conftest, and run everything inside GitHub Codespaces with no local setup required.
This lab is beginner-friendly and perfect for GRC professionals who want to see how policy as code can enforce real security requirements.

### By the end, you’ll:
- Understand why open security group rules are dangerous
- Write a Rego policy to block them
- Use Conftest to test your policy
- Run it all inside GitHub Codespaces

---

## The Lab

### What You’ll Use:

- GitHub (to host the code)
- GitHub Codespaces (runs everything in your browser)
- Rego (the policy language)
- Conftest (a policy testing tool)
- Terraform (sample input to simulate a misconfigured security group)


### Step 1: Create a GitHub Repo
1. Go to github.com and log in
2. Click the + in the upper-right → New repository
3. Name it something like no-open-sg
4. Check Add a README 
5. Click Create repository


### Step 2: Add These Files
1. Click Add file → Create new file
2. Create a file named `sg.tf` with:
```
resource "null_resource" "example" {
  triggers = {
    open_sg = jsonencode({
      name        = "open_sg"
      description = "Allows SSH from anywhere"
      ingress = [{
        from_port   = 22
        to_port     = 22
        protocol    = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
      }]
      egress = [{
        from_port   = 0
        to_port     = 0
        protocol    = "-1"
        cidr_blocks = ["0.0.0.0/0"]
      }]
    })
  }
}
```
3. Create a folder and file within it labeled `policy/deny-open-sg.rego` and add the following:
```
package main

# Decode the embedded JSON string
open_sg = decoded {
  input.resource_changes[_].change.after.triggers["open_sg"] != ""
  json.unmarshal(input.resource_changes[_].change.after.triggers["open_sg"], decoded)
}

# Deny if any ingress rule allows SSH from the public internet
deny[msg] {
  ing := open_sg.ingress[_]
  ing.cidr_blocks[_] == "0.0.0.0/0"
  ing.from_port == 22
  msg := "Open SSH access (port 22) to the internet is not allowed."
}

# Deny if any ingress rule allows RDP from the public internet
deny[msg] {
  ing := open_sg.ingress[_]
  ing.cidr_blocks[_] == "0.0.0.0/0"
  ing.from_port == 3389
  msg := "Open RDP access (port 3389) to the internet is not allowed."
}
```

4. Create a conftest.toml file in the root directory to make testing easier:
```
policy = ["policy"]
```

5. Commit each file to your main branch.


### Step 3: Open in Codespaces
1. Click the green Code button
2. Select Open with Codespaces → Create new codespace

Tip: Codespaces are free for personal GitHub accounts (up to 60 hours/month)


### Step 4: Convert to JSON
In the terminal run:
```
terraform init

terraform plan -out=tfplan.binary

terraform show -json tfplan.binary > input.json
```
Now you'll have a file called input.json that Conftest will analyze.


### Step 5: Test the Policy
From the terminal inside your Codespace, run:
```
conftest test input.json --all-namespaces
```
You should see:
```
FAIL - input.json - main - Open SSH access (port 22) to the internet is not allowed.
```


### Congratulations!
You’ve just blocked one of the most common cloud misconfigurations using policy as code.
This exact type of check can be added to your CI/CD pipeline to stop insecure deployments before they hit production.

---

## The Impact

Open security groups are like leaving your front door wide open to the world. Even if you don’t intend to expose critical systems, attackers constantly scan for these entry points.
Not fixing this can lead to:
- Remote shell access from malicious actors
- Ransomware planted directly on cloud instances
- Non-compliance with standards like NIST, FedRAMP, or CMMC
- Loss of customer trust and public credibility
And the worst part? It’s usually an accident. One that policy as code could have blocked before it ever went live.

---

## Mitigate and Retest

Now let’s fix the insecure configuration.
1. In the left sidebar, open the sg.tf file.
2. Update the `cidr_blocks` to a restricted network:
```
cidr_blocks = ["10.0.0.0/16"]
```
3.	Re-run:
```
terraform plan -out=tfplan.binary
terraform show -json tfplan.binary > input.json
conftest test input.json --all-namespaces
```
This time, you’ll see:
```
2 tests, 2 passed, 0 warnings, 0 failures, 0 exceptions
```

The policy allowed the secure config to pass. 

---

### Compliance Mapping

This policy directly addresses critical security and compliance objectives by satisfying the following NIST SP 800-53 controls:

AC-4 – Information Flow Enforcement: This policy prevents unauthorized traffic by explicitly blocking open ingress rules. It enforces controlled access at the infrastructure layer, stopping unrestricted data flow into sensitive systems.

AC-6(9) – Least Privilege: Limitation on Access by Port: By denying public access to ports 22 (SSH) and 3389 (RDP), the policy ensures that only authorized and minimal access is granted, reducing attack surface.

SC-7 – Boundary Protection: The policy enforces clear network boundaries by preventing open exposure to external sources. This is critical for segmenting systems and protecting internal components.

SC-7(3) – Access Points: Deny by Default: Rather than allowing traffic by default, this policy requires explicit safe configuration. It aligns with deny-by-default principles foundational to zero-trust architectures.

SI-4(20) – System Monitoring for Unauthorized Communications: While not a monitoring tool, the policy acts as a preventative measure by blocking high-risk misconfigurations before they occur—supporting broader monitoring and detection goals.
