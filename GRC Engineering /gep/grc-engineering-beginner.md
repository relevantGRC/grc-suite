# GRC Engineering: Beginner's Windows Setup Guide

### From Zero Experience to Your First GRC Engineering Environment

**Experience level:** Beginner — no programming or cloud experience required  
**Operating system:** Windows 11, 64-bit (Windows 10 users should verify software support)  
**Goal:** Install, configure, and test six foundational GRC Engineering tools.

---

## Welcome

If you're interested in GRC Engineering but don't know how to program, use cloud services, or work with command-line tools, this guide is for you.

This guide documents a real beginner's journey through installing the foundational tools needed to begin hands-on GRC Engineering.

You don't have to understand every technical term before starting.

The goal is to learn by doing.

By the end, you'll know how to download software safely, install command-line tools, configure Windows to recognize them, check that they work, and troubleshoot common problems.

## What You'll Be Installing

| Tool | What it does | Why GRC engineers use it |
|---|---|---|
| Git / Git Bash | Tracks changes to files | Version control and change history |
| Terraform | Defines infrastructure using configuration files | Secure cloud infrastructure and repeatable configurations |
| AWS CLI | Communicates with Amazon Web Services | Cloud configuration checks and evidence collection |
| Google Cloud CLI | Communicates with Google Cloud | Cloud assessments and compliance checks |
| Open Policy Agent (OPA) | Evaluates security rules against information | Policy-as-Code and automated control checks |
| Cosign | Signs and verifies software artifacts | Integrity and authenticity verification |

These tools will eventually work together in practical GRC Engineering projects.

**Important:** Installing these tools does not automatically make you a GRC engineer. The next phase is learning how to use them to implement, evaluate, and audit security controls.

---

# PART 1 — PREPARE YOUR COMPUTER

## 1. Confirm You're Using a Compatible Computer

This guide focuses on 64-bit Windows computers.

To check your system:

1. Click the Windows **Start** button.
2. Open **Settings**.
3. Select **System**.
4. Scroll down and select **About**.
5. Look for **System type**.

For the downloads used in this guide, you should see something similar to:

`64-bit operating system, x64-based processor`

If your processor is ARM-based, do not automatically select AMD64 downloads. Choose software compatible with your processor.

### Understanding AMD64

AMD64 does not mean you must have an AMD processor.

It refers to a common 64-bit processor architecture used by both AMD and Intel computers.

## 2. Understand Three Things You'll Use Frequently

### File Explorer

File Explorer is the Windows application used to find, organize, move, and rename files.

Press:

`Windows key + E`

This opens File Explorer.

### PowerShell

PowerShell is a tool that lets you communicate with Windows by typing commands.

To open it:

1. Click Start.
2. Type `PowerShell`.
3. Select **Windows PowerShell**.

You do not need to run PowerShell as an administrator for the basic verification commands in this guide.

### PATH

PATH is a Windows setting that tells the computer where to find programs.

For example, when you type:

`terraform version`

Windows searches locations included in PATH to find Terraform.

Without a correct PATH entry, you may receive an error saying the command is not recognized.

## 3. Understand ZIP Files and Executable Files

You will encounter several file types.

| File type | Meaning |
|---|---|
| `.zip` | A compressed folder that must be extracted |
| `.exe` | A Windows executable program |
| `.msi` | A Windows installation package |
| `.md` | A Markdown document used for GitHub instructions |
| `.ps1` | A PowerShell script |
| `.cmd` | A Windows command script |

Not every downloaded program uses an installation wizard.

Some tools, such as Terraform and OPA, can run directly from an executable file after the appropriate configuration.

## 4. Make Windows Show File Extensions

This is highly recommended.

1. Open File Explorer.
2. Select **View** from the toolbar.
3. Open **Show**.
4. Enable **File name extensions**.

Windows will now display complete filenames.

For example:

`cosign.exe`

instead of simply:

`cosign`

This prevents a common problem where a file accidentally gets renamed to:

`cosign.exe.exe`

## 5. Software Download Safety

Before installing any software:

- Download from the official project website or release page.
- Select the correct Windows architecture.
- Verify the publisher's digital signature when available.
- Use official checksums or verification procedures when provided.
- Never disable Microsoft Defender to install an unfamiliar program.
- Do not automatically click **Run anyway** on an unknown-publisher warning.

A SHA-256 checksum is a digital fingerprint calculated from a file.

PowerShell can calculate one using:

```powershell
Get-FileHash "FULL-PATH-TO-FILE" -Algorithm SHA256
```

Replace `FULL-PATH-TO-FILE` with the actual downloaded file's location.

Compare the complete result against the trusted checksum for the exact release asset.

A checksum provides evidence that the downloaded bytes match the published digest. It does not independently establish that the software itself is safe.

---

# PART 2 — INSTALL GIT AND GIT BASH

## 6. What Is Git?

Git tracks changes to files.

Think of Git as a system that remembers earlier versions of your work.

For example, if you modify a security policy or change an automation script, Git helps you see what changed and maintain a history.

Git Bash provides a terminal where you can use Git commands.

Git and GitHub are related but different:

- **Git** runs on your computer and tracks file changes.
- **GitHub** is an online platform where you can store and collaborate on Git repositories.

## 7. Download and Install Git

Official website:

https://git-scm.com/download/win

1. Open the website.
2. Find the Windows download options.
3. Download the latest supported 64-bit Git for Windows installer.
4. Open your Downloads folder.
5. Double-click the installer.
6. Review any Windows security prompts and verify the installer before proceeding.
7. Follow the setup wizard.

For a beginner, most default settings are appropriate.

Recommended choices include:

- Default installation location
- Initial branch name: `main`
- Git from the command line and third-party software
- Bundled OpenSSH
- Git Credential Manager
- Default terminal emulator: MinTTY
- File system caching enabled

For HTTPS certificate handling, keep the recommended default unless your environment has a specific requirement.

For line-ending handling, the Windows default is generally appropriate. Some projects require a different setting; follow their repository instructions.

When installation finishes, click **Finish**.

## 8. Verify Git

Open **Git Bash**.

Type:

```bash
git --version
```

Press Enter.

Expected result:

```text
git version 2.x.x.windows.x
```

The numbers may be different.

If a version appears without an error, Git is available.

### Troubleshooting

If Git is not recognized:

1. Close Git Bash.
2. Open it again.
3. Run `git --version`.
4. If the error remains, inspect whether Git was installed and available in PATH.

**Checkpoint:** Git is installed and responding to commands.

---

# PART 3 — INSTALL TERRAFORM

## 9. What Is Terraform?

Terraform lets you define cloud infrastructure using written configuration files.

This is known as **Infrastructure as Code (IaC)**.

Instead of manually creating every cloud resource through a website, you describe what should exist.

For example, Terraform can define a cloud storage resource with encryption and access restrictions.

This makes cloud configurations easier to repeat and review.

## 10. Download Terraform

Official website:

https://developer.hashicorp.com/terraform/install

1. Open the website.
2. Locate the Windows installation section.
3. Find the binary download options.
4. Select **AMD64** if your computer uses an x64 processor.
5. Click Download.
6. Open your Downloads folder.
7. Find the Terraform ZIP file.
8. Right-click it and select **Extract All**.
9. Click **Extract**.

You should see:

`terraform.exe`

## 11. Move Terraform Into a Permanent Folder

1. Open File Explorer.
2. Select **This PC**.
3. Open **Local Disk (C:)**.
4. Right-click an empty area and select **New → Folder**.
5. Name the folder `terraform`.
6. Move `terraform.exe` into this folder.

Expected location:

```text
C:\terraform\terraform.exe
```

If Windows prevents you from creating a folder directly under `C:\`, use an accessible folder within your user profile instead and use its actual location in PATH.

## 12. Add Terraform to PATH

1. Click Start.
2. Search for `environment variables`.
3. Open **Edit environment variables for your account**.
4. In User variables, select `Path`.
5. Click **Edit**.
6. Click **New**.
7. Enter:

```text
C:\terraform
```

8. Click OK on every open settings window.

Do not delete existing PATH entries.

## 13. Test Terraform

Close any existing terminal windows and open a new PowerShell window.

Enter:

```powershell
terraform version
```

Expected result:

```text
Terraform vX.X.X
on windows_amd64
```

The version number depends on the release you installed.

### Troubleshooting

If Terraform is not recognized:

```powershell
Test-Path "C:\terraform\terraform.exe"
```

Expected result:

`True`

If `False`, inspect the folder:

```powershell
Get-ChildItem "C:\terraform"
```

Verify the filename and folder location.

If `True`, confirm `C:\terraform` is present in PATH and reopen your terminal.

**Checkpoint:** Terraform displays its version.

---

# PART 4 — INSTALL AWS CLI

## 14. What Is AWS CLI?

AWS stands for Amazon Web Services.

AWS CLI is a command-line tool used to communicate with AWS services.

For GRC work, it can help inspect cloud configurations, collect evidence, and support security assessments.

For example, a properly authorized user can query cloud resource configurations and use the results as part of a control review.

## 15. Download AWS CLI

Official instructions:

https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html

Official Windows installer:

https://awscli.amazonaws.com/AWSCLIV2.msi

1. Open the official instructions.
2. Find the Windows installation section.
3. Download the Windows installer.
4. Open your Downloads folder.
5. Double-click `AWSCLIV2.msi`.
6. Follow the AWS installation wizard.
7. Keep the default installation location.
8. Select **Install**.
9. Click **Finish**.

## 16. Test AWS CLI

Open a new PowerShell window.

Enter:

```powershell
aws --version
```

Expected output begins with:

```text
aws-cli/2.
```

If version information appears, installation is successful.

### Important

AWS CLI installation does not mean you're signed into AWS.

You can verify the program works without providing credentials.

Do not configure production cloud access as part of this beginner installation exercise.

Before future cloud labs, use a separate authorized training account with MFA, limited permissions, and cost controls.

**Checkpoint:** AWS CLI displays version information.

---

# PART 5 — INSTALL GOOGLE CLOUD CLI

## 17. What Is Google Cloud CLI?

Google Cloud CLI allows you to interact with Google Cloud using commands.

Its purpose is similar to AWS CLI, but it works with Google's cloud platform.

For GRC Engineering, it can help inspect permissions, configurations, resource inventories, and cloud security settings.

## 18. Download Google Cloud CLI

Official instructions:

https://cloud.google.com/sdk/docs/install

1. Open the website.
2. Locate the Windows installation instructions.
3. Download the Google Cloud CLI installer.
4. Open the downloaded installer.
5. Select **Single User** if installing for your personal Windows account.
6. Keep the core Google Cloud CLI tools selected.
7. Keep Bundled Python selected if offered.
8. Leave optional beta components unchecked unless a lab specifically needs them.
9. Click **Install**.

Follow the remaining installation prompts.

## 19. Test Google Cloud CLI

Open PowerShell.

Enter:

```powershell
gcloud.cmd version
```

Expected output includes:

```text
Google Cloud SDK
```

and a version number.

### Troubleshooting: PowerShell Script Restrictions

You may encounter an error stating that:

`gcloud.ps1 cannot be loaded because running scripts is disabled`

This can happen because PowerShell restricts script execution.

For basic verification, try:

```powershell
gcloud.cmd version
```

This uses the Windows command-script entry point without changing the PowerShell execution policy.

Do not change Windows security policies unnecessarily.

### Authentication

Google Cloud CLI may offer to sign you into a Google account.

Authentication can be completed later when you're ready for an authorized cloud lab.

You do not need to create cloud resources or enable billing simply to verify that Google Cloud CLI is installed.

**Checkpoint:** Google Cloud CLI displays version information.

---

# PART 6 — INSTALL OPEN POLICY AGENT

## 20. What Is OPA?

OPA stands for **Open Policy Agent**.

OPA evaluates information against rules that you define.

This approach is known as **Policy-as-Code**.

Imagine a security requirement stating that cloud storage must not be publicly accessible.

OPA can evaluate configuration data against a rule that checks whether public access is allowed.

OPA returns a policy decision, which another system can use to block, flag, or report the configuration.

## 21. Download OPA

Official releases:

https://github.com/open-policy-agent/opa/releases

1. Open the GitHub releases page.
2. Select the appropriate stable release.
3. Expand **Assets**.
4. Find the Windows AMD64 executable.
5. Download `opa_windows_amd64.exe`.

Check the official release information before choosing a file.

## 22. Verify and Organize OPA

Before running the executable, verify the download according to the official release instructions.

Create a permanent folder:

```text
C:\opa
```

Move the verified file into this folder and rename it:

```text
opa.exe
```

The final path should be:

```text
C:\opa\opa.exe
```

OPA does not require a traditional Windows installation wizard.

## 23. Add OPA to PATH

1. Open Environment Variables.
2. Select your User `Path`.
3. Click **Edit → New**.
4. Enter:

```text
C:\opa
```

5. Save the changes.

## 24. Test OPA

Open a new PowerShell window.

Enter:

```powershell
opa version
```

Expected output includes:

```text
Version: x.x.x
Platform: windows/amd64
```

### Troubleshooting

If the command is not recognized:

```powershell
Test-Path "C:\opa\opa.exe"
```

If it returns `True`, confirm the PATH setting and reopen PowerShell.

If it returns `False`, check:

```powershell
Get-ChildItem "C:\opa"
```

Use the result to locate any incorrect filename.

**Checkpoint:** OPA displays its version.

---

# PART 7 — INSTALL COSIGN

## 25. What Is Cosign?

Cosign is a tool for digitally signing and verifying software artifacts and other supported files.

A digital signature can help demonstrate that an artifact has not changed since signing and that it is associated with an expected signing identity or trusted key.

For GRC Engineering, this can be useful when designing evidence-integrity workflows.

However, a valid signature doesn't automatically prove that the evidence is accurate or that a control is effective.

## 26. Download Cosign

Official releases:

https://github.com/sigstore/cosign/releases

1. Open the releases page.
2. Select the appropriate stable release.
3. Expand **Assets**.
4. Locate the Windows AMD64 executable.
5. Download:

```text
cosign-windows-amd64.exe
```

Before executing the file, verify it using the official release's verification information.

## 27. Organize the Cosign File

Create this folder:

```text
C:\cosign
```

Move the verified executable into it.

Rename the file to:

```text
cosign.exe
```

Expected location:

```text
C:\cosign\cosign.exe
```

## 28. Common Mistake: Double EXE Extension

During the original installation, Windows displayed the file as:

`cosign.exe`

But PowerShell showed the actual filename was:

`cosign.exe.exe`

This happened because Windows had hidden the final extension.

To see the actual filename, enter:

```powershell
Get-ChildItem "C:\cosign" | Select-Object Name, Extension
```

If the name is `cosign.exe.exe`, correct it:

```powershell
Rename-Item "C:\cosign\cosign.exe.exe" "cosign.exe"
```

Do not run this rename command if the filename is already correct.

## 29. Add Cosign to PATH

1. Open Environment Variables.
2. Select User `Path`.
3. Click **Edit → New**.
4. Enter:

```text
C:\cosign
```

5. Save the settings.
6. Open a new PowerShell window.

## 30. Verify Cosign's Location

First check that the file exists:

```powershell
Test-Path "C:\cosign\cosign.exe"
```

Expected result:

```text
True
```

Then check that Windows can locate it through PATH:

```powershell
Get-Command cosign.exe
```

Expected result should reference:

```text
C:\cosign\cosign.exe
```

Once the official release verification is complete, run:

```powershell
cosign version
```

Expected result: Cosign's version information.

**Checkpoint:** Cosign runs and reports its version.

---

# PART 8 — COMMON BEGINNER PROBLEMS

## 31. PowerShell Doesn't Recognize a Command

An error like this:

`The term 'cosign' is not recognized`

usually means that Windows cannot locate the program using its current command search paths.

Check whether the executable exists.

For example:

```powershell
Test-Path "C:\cosign\cosign.exe"
```

If `True`, check the PATH entries visible to the current terminal:

```powershell
$env:Path -split ';'
```

Look for the program's folder.

If the PATH setting was recently changed, close the terminal application completely and reopen it.

## 32. Find Out What's Inside a Folder

Use:

```powershell
Get-ChildItem "C:\cosign"
```

This shows the files in that folder.

It doesn't change or delete anything.

You can use the same command with other folders.

## 33. File Location Is Different From Expected

Windows may store Desktop files in OneDrive.

For example:

```text
C:\Users\YOUR-USERNAME\OneDrive\Desktop
```

To find the actual location:

1. Right-click the file.
2. Select **Properties**.
3. Open the General tab.
4. Look for **Location**.

Use the real location rather than guessing.

## 34. Windows Displays a Security Warning

A SmartScreen warning means Windows is warning about an application it doesn't recognize or trust sufficiently.

It doesn't prove that the program is malicious or safe.

Confirm the source and use available signature, checksum, and publisher-verification instructions before deciding whether to execute it.

Never disable system protections just to make installation easier.

## 35. A Command Produces an Error

Read the first error message and identify what failed.

For example:

- **CommandNotFoundException:** Windows couldn't resolve the command.
- **PathNotFound:** The specified path couldn't be found.
- **UnauthorizedAccess:** A permission or security restriction prevented an action.
- **Missing argument:** A command requires additional information.

Avoid randomly changing Windows settings.

Use the error to identify the problem before making changes.

---

# PART 9 — FINAL INSTALLATION CHECK

## 36. Verify All Six Tools

Open PowerShell and run these commands one at a time:

```powershell
git --version
terraform version
aws --version
gcloud.cmd version
opa version
cosign version
```

Each command should display version information.

### Completion Checklist

- [ ] Git displays its version
- [ ] Git Bash opens successfully
- [ ] Terraform displays its version
- [ ] AWS CLI displays its version
- [ ] Google Cloud CLI displays its version
- [ ] OPA displays its version
- [ ] Cosign displays its version
- [ ] Download verification completed where applicable
- [ ] Windows PATH settings work
- [ ] No unexpected installation errors remain

### What Does Successful Installation Mean?

It means Windows can locate and run the tools.

It does **not** mean you've connected cloud accounts, deployed infrastructure, implemented security policies, or completed an audit.

Those are separate learning milestones.

---

# PART 10 — WHAT YOU'LL LEARN NEXT

Now that the environment is prepared, the next phase is learning how to use the tools.

## Recommended Learning Path

**Module 1 — Git and GitHub Basics**

Learn repositories, commits, branches, push, and pull.

**Module 2 — Terraform Fundamentals**

Learn configuration files, providers, resources, initialization, validation, and plans.

**Module 3 — Cloud Basics**

Learn AWS and Google Cloud accounts, services, permissions, networking, and billing safeguards.

**Module 4 — Security Controls**

Learn how technical configurations support security requirements.

**Module 5 — Policy-as-Code**

Create and test simple OPA rules.

**Module 6 — Evidence Integrity**

Learn file hashing, digital signatures, and verification using Cosign.

**Module 7 — Practitioner Projects**

Build repeatable security control checks and automation workflows.

**Module 8 — Auditor Projects**

Develop technical testing procedures, independently evaluate control results, document exceptions, and prepare audit evidence.

## Our Learning Principle

Every project should answer four questions:

1. **What are we building or testing?**
2. **Why does it matter for security, risk, or compliance?**
3. **How do we verify that it works?**
4. **How would an auditor independently evaluate the results?**

---

# OFFICIAL LEARNING RESOURCES

- [GRC Engineering Club Labs](https://github.com/GRCEngClub/cgep-labs)
- [Git Documentation](https://git-scm.com/doc)
- [Terraform Documentation](https://developer.hashicorp.com/terraform/docs)
- [AWS CLI Documentation](https://docs.aws.amazon.com/cli/)
- [Google Cloud CLI Documentation](https://cloud.google.com/sdk/docs)
- [Open Policy Agent Documentation](https://www.openpolicyagent.org/docs)
- [Sigstore Cosign Documentation](https://docs.sigstore.dev/cosign/)

## Final Note

This is an independent beginner's learning guide created to help individuals develop hands-on GRC Engineering skills.

Always use authorized training environments and official software sources.

Do not publish passwords, API keys, authentication tokens, private signing keys, confidential company information, or sensitive screenshots.

Software versions and installation screens can change over time, so consult the official documentation when following this guide.

**End of Beginner's Windows Setup Guide — Next Project: Building Your First Compliant Resource
