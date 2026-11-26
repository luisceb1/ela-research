# Disposable Hetzner infrastructure smoke test

The first manual run uses a synthetic SHA-256 workload to verify provisioning,
CPU parallelism, result retrieval and resource deletion. No scientific data
or access credentials are included in its artifact. The research repository
is public, so use private storage for any nonpublic research outputs.

Use a write-enabled Hetzner API token belonging exclusively to the **ELA
Research** project. Enter it directly as the GitHub Actions repository secret
`HETZNER_ELA_PILOT_TOKEN`. Never commit the token or include it in job output.

Run "Hetzner disposable compute smoke test" from main. No server is created
by the expiry workflow. The smoke test requests one CCX33 in Nuremberg, with
a single IPv4 address, Ubuntu 24.04 and an ephemeral SSH key. It checks the
gross server price before creating billable resources.

A 20-minute job timeout, finally-block cleanup, separate cleanup-verification
job and a 45-minute expiration label limit the expected resource lifetime.
The expiry workflow checks the labels twice an hour and can also run manually.
The expiry is a best-effort backstop, not a hard billing cap: GitHub scheduled
runs can be delayed or dropped, and provider errors may delay deletion.
Verify that the project has no remaining servers or primary IPs after every
run, even a cancelled one. If the controller is unavailable, delete the
specific disposable pilot resources in the Hetzner Console.

The benchmark ZIP is available in the Actions run for seven days. The
reported serial and parallel SHA-256 values must agree. It measures synthetic
CPU work and basic host capacity; it does not establish the runtime or
reproducibility of a biological alignment workflow.

Disable the expiry workflow and revoke the dedicated API token if closing
this pilot permanently.
