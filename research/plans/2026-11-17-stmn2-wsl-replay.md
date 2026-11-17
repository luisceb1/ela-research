# WSL admission extension — 17 November 2026

Luis selected real technical replay on his PC. The original portable entry point
rejects WSL. Before any real alignment, extend admission to verified WSL2 with
its distribution VHD on physical C:, and native ext4 output on that VHD.

Question: can the existing replay enforce both guest and physical-host space
reserves without changing measurement? Unverifiable mapping, insufficient space,
or loss of host telemetry must fail closed. Native Linux behavior is retained.

Keep all twelve raw identities, eight index digests, scientific counter, commands,
six-library ordering and existing caps. Bind distribution/registry/VHD identity
into the plan, require 150 GiB on both filesystems at admission, and sample the
existing verified C: drvfs availability with the guest reserve every 0.5 s.
Require 7 GiB available guest RAM at WSL prepare/run admission for the 6 GiB
worker cap plus headroom. This is admission only, not a RAM reservation.

Test mapping refusals, altered plan/environment, low/unavailable physical space
at admission and during supervision, and existing native software fixtures.
No FASTQ execution or real Windows validation is claimed by Linux-side tests.
Deliver code and tests as a PR, then obtain a real host preparation record before
issuing the hash-bound run command. Preserve failures and all source files.
